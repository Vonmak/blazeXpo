from django.urls import path, re_path
from .views import *

urlpatterns=[
    path('',index, name='index'),
    path('register/',register),
    path('login/',login_user),
    path('logout',logout_user),
    re_path(r'^profile/(\d+)',profile, name='profile'),
    path('search/',search, name='search'),
    path('search/',search_results, name='search'),
    # path('api/projects/', ProjectList.as_view()),
    # path('api/profiles/', ProfileList.as_view()),
    path('api/users/', UserList.as_view()),
    path('project/<project>', project, name='project'),
]