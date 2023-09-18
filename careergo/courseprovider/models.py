from django.db import models
from home.models import CustomUser
# Create your models here.

class Courseprovider_profile(models.Model):

   user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
   

def __str__(self):
        return self.title