from django.db import models
from home.models import CustomUser
from django.utils import timezone
# Create your models here.

class Courseprovider_profile(models.Model):

   user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
   

def __str__(self):
        return self.title



class Video(models.Model):
    course = models.ForeignKey('Oncourse', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/', null=True)
    section_name = models.CharField(max_length=100,default='')

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
    #video = models.FileField(upload_to='videos/', null=True,default='')
    course_title = models.CharField(max_length=100)
    description=models.CharField("Description",max_length=500)
    duration = models.CharField(max_length=100)  # Assuming duration is in days or some other unit
    instructor = models.CharField(max_length=100)
    price=models.IntegerField("Price", default=0)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Programming',  # You can set a default category if needed
    ) 
    is_free = models.BooleanField(default=True)

    

    def _str_(self):
        return f"Oncourse ID{self.pk}"
    

    
class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)  # Link the payment to a user
    # course_title = models.ForeignKey(Oncourse, on_delete=models.CASCADE,null=True)
    razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
    payment_id = models.CharField(max_length=255)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=3)  # Currency code (e.g., "INR")
    payment_date = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    
   

    def __str__(self):
        return f"Payment by {self.user.username}"

    class Meta:
        ordering = ['-payment_date']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.payment_date).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()

# class Internship(models.Model):
#     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
#     internship_title = models.CharField(max_length=255)
#     description = models.TextField()
#     duration = models.IntegerField()
#     instructor = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=5, decimal_places=2,default=0)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     positions = models.PositiveIntegerField()
#     internship_type = models.CharField(max_length=20, default='unpaid', choices=[("unpaid", "Unpaid")])
#     internship_mode = models.CharField(max_length=20, default='online',choices=[("online", "Online")])
#     application_deadline = models.DateField()
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     company_website = models.URLField(max_length=200, blank=True, null=True)
#     category = models.CharField(max_length=255, choices=[("Category 1", "Category 1"), ("Category 2", "Category 2")])
#     other_category = models.CharField(max_length=255, blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='internship_thumbnails', blank=True, null=True)
    
#     def __str__(self):
#         return self.internship_title