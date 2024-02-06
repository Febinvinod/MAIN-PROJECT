from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from test.models import course




class CustomUser(AbstractUser):
    STUDENT = 1
    COURSE_PROVIDER = 2
    MENTOR = 3
    ADMIN = 4

    ROLE_CHOICE = (
        (STUDENT, 'student'),
        (COURSE_PROVIDER, 'course_provider'),
        (MENTOR , 'mentor'),
        (ADMIN , 'admin'),
    )

    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12,unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')




    object = UserManager() 
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_no','first_name','last_name','role']

    def _str_(self):
        return self.name 
    

class UserProfile(models.Model):
        # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
        user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
        profile=models.FileField(upload_to='profile_pic/',blank=True,null=True)
        country = models.CharField(max_length=15, blank=True, null=True)
        state = models.CharField(max_length=15, blank=True, null=True)
        city = models.CharField(max_length=15, blank=True, null=True)
        pin_code = models.CharField(max_length=6, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        modified_at = models.DateTimeField(auto_now=True)
    
        def _str_(self):
            if self.user:
                return self.user.username
            else:
                return "UserProfile with no associated user" 
    