from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Project

class RegistrationForm( UserCreationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')
   