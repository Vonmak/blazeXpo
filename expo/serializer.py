from rest_framework import serializers
from .models import *

class ProjectSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='user.profile')
    class Meta:
        model = Project
        fields = ['project_image','project_name','project_description','project_url','language','profile']
        
        
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Profile
        fields = ('username','name','pic', 'bio', 'email', 'location',)
        
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'profile', 'projects']