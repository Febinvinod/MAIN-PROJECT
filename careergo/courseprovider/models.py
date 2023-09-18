from django.db import models
from home.models import CustomUser
# Create your models here.

class Courseprovider_profile(models.Model):

   user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
   

def __str__(self):
        return self.title

class Oncourse(models.Model):


    CATEGORY_CHOICES = (
        ('Programming', 'Programming'),
        ('Web_Development', 'Web_Development'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Cloud_Computing', 'Cloud_Computing'),
        ('Machine_Learning', 'Machine_Learning'),
        ('Data_Science', 'Data_Science'),
        ('DevOps', 'DevOps'),
    )
   
     
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    thumbnail=models.FileField(upload_to='thumbnail/')
    video = models.FileField(upload_to='videos/', null=True,default='')
    course_title = models.CharField(max_length=100)
    description=models.CharField("Description",max_length=500)
    duration = models.CharField(max_length=100)  # Assuming duration is in days or some other unit
    instructor = models.CharField(max_length=100)
    price=models.IntegerField("Price")
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Programming',  # You can set a default category if needed
    )
    
    
   
   

    

    def _str_(self):
        return f"Oncourse ID{self.pk}"