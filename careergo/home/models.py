from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from test.models import course



class CustomUser(AbstractUser):
    STUDENT = 1
    COURSE_PROVIDER = 2
    MENTOR = 3

    ROLE_CHOICE = (
        (STUDENT, 'student'),
        (COURSE_PROVIDER, 'course_provider'),
        (MENTOR , 'mentor'),
    )

    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')




    object = UserManager() 
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_no','first_name','last_name']

    def _str_(self):
        return self.name 