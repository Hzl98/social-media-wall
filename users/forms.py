from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_additional_info

class UserRegForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AdditionalInfoForm(forms.ModelForm):
	class Meta:
		model = User_additional_info
		fields = ['image']