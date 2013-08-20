from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse 
from django.views.generic.edit import ModelFormMixin
from .models import Textbook, Own
from .forms import OwnForm
 
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class TextbookMixin(LoginRequiredMixin):
	model = Textbook
	def get_success_url(self):
		return reverse('exchange:own_create')
	def get_queryset(self):
		return Textbook.objects.all()

class OwnMixin(LoginRequiredMixin):
	model = Own
	form_class = OwnForm
	def get_success_url(self):
		return reverse('exchange:library')
	def get_queryset(self):
		return self.request.user.person.owns.all()
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.owner_id = self.request.user.person.id
		self.object.save()
		return super(ModelFormMixin, self).form_valid(form)

class SellingListView(LoginRequiredMixin, ListView):
	model = Own
	template_name = 'exchange/selling_list.html'
	def get_queryset(self):
		if self.request.GET and self.request.GET.get('search'):
			return Own.objects.filter(textbook__title__icontains=self.request.GET.get('search'))
		else:
			return Own.objects.all()

class TextbookListView(TextbookMixin, ListView):
	pass
class TextbookDetailView(TextbookMixin, DetailView):
	pass
class TextbookCreateView(TextbookMixin, CreateView):
	pass
class TextbookDeleteView(TextbookMixin, DeleteView):
	pass
class TextbookUpdateView(TextbookMixin, UpdateView):
	pass

class OwnListView(OwnMixin, ListView):
	pass
class OwnDetailView(OwnMixin, DetailView):
	pass
class OwnCreateView(OwnMixin, CreateView):
	pass
class OwnDeleteView(OwnMixin, DeleteView):
	pass
class OwnUpdateView(OwnMixin, UpdateView):
	pass
