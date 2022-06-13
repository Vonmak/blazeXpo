from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class RegistrationForm( UserCreationForm, forms.ModelForm):
    email=forms.EmailField(max_length=100, required=False)
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

class LoginForm(forms.Form):
    email=forms.CharField(max_length=50)
    password=forms.CharField(max_length=20, widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name','bio','email','location','pic')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_image','project_name','project_description','project_url','language']
 
class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']