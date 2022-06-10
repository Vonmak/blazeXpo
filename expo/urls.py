from django.urls import path, re_path
from .views import *

urlpatterns=[
    path('',index, name='index'),
    path('register/',register),
    path('login/',login_user),
    path('logout',logout_user),
    re_path(r'^profile/(\d+)',profile, name='profile'),
    path('profile/',update_profile,name ='newprofile'),
    path('project/', project_add, name = "project"),
 
]