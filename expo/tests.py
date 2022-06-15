# from unicodedata import name
from django.test import TestCase
from .models import Project,User, Profile

# Create your tests here.
class ProfileTest(TestCase):
    '''
    test class for Profile model
    '''
    def setUp(self):
        '''
        test method to create Profile instances called before all tests
        '''
        self.new_user = User(username='victor')
        self.new_user.save()
        # self.project_test = Project(user=self.new_user)
        # self.project_test.save()
        # self.user = User.objects.create(id=2, username='victor')

        
        self.new_profile = Profile(name='sniff',pic='images/picture.jpeg',bio='i love expo',user=self.new_user,location='nairobi',contact='vic@gamil.com')
        self.new_profile.save()

    def tearDown(self):
        '''
        test method to delete Profile instances after each test is run
        '''
        Profile.objects.all().delete()

    def test_save_profile(self):
        '''
        test method to ensure a Profile instance has been correctly saved
        '''
        self.assertTrue(len(Profile.objects.all()) == 1)     

    def test_delete_profile(self):
        '''
        test method to ensure a Profile instance has been correctly deleted
        '''
        self.new_profile.save()
        self.new_profile.delete()
        self.assertTrue(len(Profile.objects.all()) == 0)    





class ProjectTest(TestCase):
    '''
    test class for Images model
    '''
    def setUp(self):
        '''
        test method to create project instances called before all tests
        '''
        self.new_user = User(username='victor')
        self.new_user.save()
        
        self.new_project = Project(project_image='images/picture.jpeg', project_name='Image title', project_description='sth random', user=self.new_user, language='python')
        self.new_project.save()
        self.another_project = Project(project_image='images/photo.jpg', project_name='Another title', project_description='sth else more random', user=self.new_user, language='python')
        self.another_project.save()

    def tearDown(self):
        '''
        test method to delete Project instances after each test is run
        '''
        Project.objects.all().delete()

    def test_save_project(self):
        '''
        test method to ensure an Project instance has been correctly saved
        '''
        self.assertTrue(len(Project.objects.all()) == 2)
        
    def test_instances(self):
        '''
        test method to assert instances created during setUp
        '''
        self.assertTrue(isinstance(self.new_project,Project))



    def test_delete_project(self):
        '''
        test method to ensure an Image instance has been correctly deleted
        '''
        self.new_project.delete()
        self.assertTrue(len(Project.objects.all()) == 1)



    def test_filter_by_user(self):
        '''
        test method to obtain image instances by user
        '''
        obtained_project = Project.filter_by_user(self.another_project.user)
        print(obtained_project)



