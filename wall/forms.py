from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Sources, wall

class SourceForm(forms.ModelForm):
	class Meta:
		model = Sources
		fields = ['source', 'tag']

class wallUpdateForm(forms.ModelForm):
	class Meta:
		model = wall
		fields = ['name', 'visibility', 'design']
		widgets = {
			'visibility' : forms.RadioSelect(),
			'design' : forms.RadioSelect()
		}

