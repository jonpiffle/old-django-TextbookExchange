from django import forms
from .models import Message
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		exclude = ('sender, conversation, recipient')
		widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 10, 'class':'sent', 'placeholder':'New Message'},),
    }

class CustomRegistrationForm(RegistrationForm):
	def __init__(self, *args, **kwargs):
		super(RegistrationForm,self).__init__(*args, **kwargs)
#		del self.fields['email']
		last_name = forms.CharField()
		self.fields['first_name'] = forms.CharField(required=False)
		self.fields['last_name'] = forms.CharField(required=False)
		self.fields = {'first_name':self.fields['first_name'], 
									'last_name':self.fields['last_name'], 
									'username':self.fields['username'], 
									'password1':self.fields['password1'], 
									'password2':self.fields['password2'],
									'email':forms.CharField(required=False)}
