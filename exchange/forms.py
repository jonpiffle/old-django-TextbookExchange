from django import forms
from .models import Own, Textbook

class OwnForm(forms.ModelForm):
	textbook = forms.ModelChoiceField(queryset=Textbook.objects.order_by('dept', 'course_num'))

	class Meta:
		model = Own
		exclude = ('owner')
