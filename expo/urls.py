from django.urls import path, re_path
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('',index, name='index'),
    path('register/',register),
    path('login/',login_user),
    path('logout',logout_user),
    re_path(r'^profile/(\d+)',profile, name='profile'),
    re_path(r'^look/(\d+)', lookup_profile, name='look'),
    path('search/',search_results, name='search'),
    path('api/projects/', ProjectList.as_view()),
    path('api/profiles/', ProfileList.as_view()),
    path('api/users/', UserList.as_view()),
    path('project/<project>', project, name='project'),
    # path('hello/', HelloView.as_view(), name='hello'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('jwtobt/',TokenObtainPairView.as_view()),
    # path('jwtref/',TokenRefreshView.as_view())
]