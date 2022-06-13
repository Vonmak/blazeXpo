from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from rest_framework import viewsets

# Create your views here.
def index(request):
    project=Project.objects.latest('date')
    projects = Project.objects.all().order_by('-date')
    profiles= Profile.objects.all()
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
        
    return render(request,"profile/profile.html",locals())

def lookup_profile(request, id):
    profile = Profile.objects.get(user=id)
    projects = Project.filter_by_user(id)
    user_prof = get_object_or_404(User, id=id)
    if request.user == user_prof:
      return redirect('profile', id=request.id)
    
    return render(request,'profile/profile.html',locals())

def search_results(request):
    if 'project_name' in request.GET and request.GET["project_name"]:
        search_term = request.GET.get("project_name")
        searched_projects = Project.search_by_project_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',locals())

    else:
        message = "You haven't searched for any term"
        return render(request, 'pro.html',{"message":message})


class UserList(APIView):
    def get(self, request, format=None):
        projects = User.objects.all()
        serializers = UserSerializer(projects, many=True)
        return Response(serializers.data)
    
class ProjectList(APIView):
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)
    
class ProfileList(APIView):
    def get(self, request, format=None):
        projects = Profile.objects.all()
        serializers = ProfileSerializer(projects, many=True)
        return Response(serializers.data)
    
def project(request, project):
    project = Project.objects.get(project_name=project)
    ratings = Rating.objects.filter(user=request.user, project=project).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            project_ratings = Rating.objects.filter(project=project)

            design_ratings = [d.design for d in project_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in project_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in project_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            # print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
  
    return render(request, 'pro.html', locals())

