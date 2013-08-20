from django.views.generic import TemplateView, FormView, CreateView
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse 
from message.forms import CustomRegistrationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from registration import signals

class HomepageView(TemplateView):
	template_name = "index.html"

class CustomRegistrationView(RegistrationView):
	form_class = CustomRegistrationForm
	def get_success_url(self, request, user):
		return reverse("exchange:library")
	def register(self, request, **cleaned_data):
		username, email, password, first_name, last_name = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1'], cleaned_data['first_name'], cleaned_data['last_name']
		User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

		new_user = authenticate(username=username, password=password)
		login(request, new_user)
		signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
		return new_user

