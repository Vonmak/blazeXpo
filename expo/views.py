from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def index(request):
    projects = Project.objects.all().order_by('-date')
    profiles= Profile.objects.all()
    return render(request,'index.html',locals())


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
                return redirect(index)
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
    projects = Project.filter_by_user(user.id).order_by('-date')
    return render(request,"profile/profile.html",locals())

def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile =form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect(index)
    else:
        form=ProfileForm()

    return render(request, 'profile/update.html', locals())


def project_add(request):  
    current_user = request.user
    if request.method == 'POST':   
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid(): 
            post = form.save(commit=False) 
            post.user=request.user
            post.profile=request.user.profile
            post.save() 
            return redirect(index) 
              
            # return HttpResponseRedirect(request.path_info)  
    else:  
        form = ProjectForm()  
  
    return render(request, 'project.html', locals())  
