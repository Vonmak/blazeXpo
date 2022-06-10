from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def register(request):
    form = RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            form.save()
        return redirect(login_user)
    return render(request, 'auth/register.html',locals())

def login_user(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            usern=form.cleaned_data['email']
            passw=form.cleaned_data['password']
            user=authenticate(request,username=usern,password=passw)
            if user is not None:
                login(request,user)
                return redirect(register)
            else:
                return HttpResponse('Such a user does not exist')
        else:
            return HttpResponse("Form is not Valid")
    
    return render(request,'auth/login.html',locals())

def logout_user(request):
    logout(request)
    return redirect('/login')

def profile(request, id):  
    user=User.objects.filter(id=id).first()
    profile = Profile.objects.get(user=id)
    # projects = request.user.projects.all().order_by('date')
    projects = Project.filter_by_user(user.id).order_by('date')
    return render(request,"profile/profile.html",locals())
