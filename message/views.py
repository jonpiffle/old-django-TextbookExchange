from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.models import User
from .models import Message, Conversation, Person, Notification
from .forms import MessageForm
from datetime import datetime

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class MessageMixin(LoginRequiredMixin):
	model = Message
	form_class = MessageForm
	def get_success_url(self):
		return reverse('message:conversation_detail', args=[self.object.conversation_id])
	def get_queryset(self):
		return self.request.user.person.received_messages.all()
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.sender_id = self.request.user.person.id
		self.object.save()
		return super(ModelFormMixin, self).form_valid(form)

class ConversationMixin(LoginRequiredMixin):
	model = Conversation
	def get_success_url(self):
		return reverse('message:conversation_list')
	def get_queryset(self):
		return self.request.user.person.conversations_without_self()

class MessageCreateView(MessageMixin, CreateView):
	pass
class ConversationListView(ConversationMixin, ListView):
	pass

class ConversationDetailView(ConversationMixin, CreateView):
	form_class = MessageForm
	template_name = 'message/conversation_detail.html'

	def get_context_data(self, **kwargs):
		ctx = super(ConversationDetailView, self).get_context_data(**kwargs)
		conversation = Conversation.objects.get(pk=self.kwargs['pk'])
		for message in conversation.messages.all():
			if message.sender == self.request.user.person:
				message.sent_or_received = 'sent'
			else:
				message.sent_or_received = 'received'
		ctx['conversation'] = conversation
		for n in conversation.notifications():
			if n[0].person_id == self.request.user.person.id:
				n.delete()
		return ctx

	def get_success_url(self):
		return reverse('message:conversation_detail', args=[self.kwargs['pk']]) + "#id_content"

	def form_valid(self, form):
		self.object = form.save(commit = False)
		conversation = Conversation.objects.get(pk=self.kwargs['pk'])
		self.object.conversation_id = conversation.id
		self.object.sender_id = self.request.user.person.id
		if len(conversation.people.all()) == 1:
			self.object.recipient_id = conversation.people.all()[0].id
		else:
			self.object.recipient_id = conversation.people.exclude(id=self.object.sender_id)[0].id
		self.object.save()
		conversation.updated_at = self.object.created_at
		conversation.save()
		Notification.objects.create(person_id=self.object.recipient_id, message_id=self.object.id)
		return super(ModelFormMixin, self).form_valid(form)


def conversation_router(request):
	recipient = Person.objects.get(pk=request.GET.get('recipient_id'))
	sender = request.user.person

	conversation = Conversation.objects.filter(people__id = sender.id)
	
	try:
		conversation = conversation.get(people__id = recipient.id)
	except Conversation.DoesNotExist:
		conversation = Conversation.objects.create(updated_at = datetime.now())
		conversation.people.add(sender)
		conversation.people.add(recipient)
	
	return redirect(str(reverse('message:conversation_detail', args=[conversation.id])) + "?recipient_id="+str(recipient.id))

