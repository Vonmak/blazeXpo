import email
from django.db import models
from django.db import models
import datetime as dt
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from tinymce.models import HTMLField
    

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=50)
    pic = CloudinaryField('image')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=50,default="I love this Expo!")
    location = models.CharField(max_length=60, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    
    def save_profile(self):
            self.save()
        
    def delete_profile(self):
        self.delete()
        
    @classmethod
    def get_all(cls):
        profiles = Profile.objects.all()
        return profiles
    
    
class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.TextField()
    project_url = models.URLField()
    project_image = CloudinaryField('image')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    language = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f'{self.project_name} Project'
    
    @classmethod
    def get_all(cls):
        projects = Project.objects.all()
        return projects
    
    @classmethod
    def get_project_by_id(cls, id):
        retrieved = Project.objects.get(id = id)
        return retrieved
    
    @classmethod
    def search_projects(cls, search_term):
        projects = cls.objects.filter(project_name__icontains=search_term)
        return projects

    def update_project(self, new_project):
        try:
            self.project_name = new_project
            self.save()
            return self
        except self.DoesNotExist:
            print('project already exists')
    
    @classmethod
    def filter_by_user(cls, user):
        projects = cls.objects.filter(user__id__icontains=user).all()
        return projects
     
    @classmethod  
    def search_by_project_name(cls, search_term):
        projects = cls.objects.filter(project_name__icontains=search_term)
        return projects

    
class Rating(models.Model):
    rating = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.project} Rating'