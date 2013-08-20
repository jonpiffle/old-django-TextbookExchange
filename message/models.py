from django.db import models
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login
#from django.core.forms import AuthForm
from registration.signals import *
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Person(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	textbooks = models.ManyToManyField('exchange.Textbook', through="exchange.Own")

	def conversations_without_self(self):
		conversations = self.conversation_set.all().order_by('-updated_at').exclude(messages__isnull=True)
		for c in conversations:
			others = c.people.all().exclude(pk=self.pk)
			c.other = others[0] if len(others) > 0 else None
		return conversations

	class Meta:
		verbose_name_plural = "people"

	def __unicode__(self):
		if self.user.first_name or self.user.last_name:
			return self.user.first_name + " " + self.user.last_name
		else:
			return self.user.username

def createUserProfile(sender, user, request, **kwargs):
	Person.objects.get_or_create(user=user)

user_registered.connect(createUserProfile)

class Conversation(models.Model):
	people = models.ManyToManyField(Person)
	updated_at = models.DateTimeField(editable=True)

	def __unicode__(self):
		return " & ".join([p.__unicode__() for p in self.people.all()])

	def notifications(self):
		return [m.notifications.all() for m in self.messages.all() if len(m.notifications.all()) > 0 ]

	def most_recent(self):
		return self.messages.all().order_by('-created_at')[0]

	def unread(self):
		return len(self.notifications()) > 0

class Message(models.Model):
	sender = models.ForeignKey(Person, related_name = 'messages_sent')
	recipient = models.ForeignKey(Person, related_name = 'messages_received')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True, editable = False)
	conversation = models.ForeignKey(Conversation, related_name="messages")

	def unread(self):
		return len(self.notifications.all()) > 0

	def __unicode__(self):
		if len(self.content) > 50:
			return self.content[:50] + "..."
		else:
			return self.content

class Notification(models.Model):
	person = models.ForeignKey(Person, related_name='notifications')
	message = models.ForeignKey(Message, related_name='notifications')
	created_at = models.DateTimeField(auto_now_add = True, editable = False)

