from django.db import models
from home.models import CustomUser
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.

class Courseprovider_profile(models.Model):

   user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
   

def __str__(self):
        return self.title



class Mentor_profile(models.Model):

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
    
class Video(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='video_user',null=True)
    course = models.ForeignKey(Oncourse, on_delete=models.CASCADE,related_name='video_course',null=True)
    video_file = models.FileField(upload_to='videos/', null=True)
    section_name = models.CharField(max_length=100,default='')
    checked = models.BooleanField(default=False)
class UserVideo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Oncourse, on_delete=models.CASCADE,null=True)
    video=models.ForeignKey(Video,on_delete=models.CASCADE,null=True)
    checked=models.BooleanField(default=False)

class Internship(models.Model):

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
    internship_title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    instructor = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2,default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    positions = models.PositiveIntegerField()
    internship_type = models.CharField(max_length=20, default='unpaid', choices=[("unpaid", "Unpaid")])
    internship_mode = models.CharField(max_length=20, default='online',choices=[("online", "Online")])
    application_deadline = models.DateField()
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Programming',  # You can set a default category if needed
    ) 
    thumbnail = models.ImageField(upload_to='internship_thumbnails', blank=True, null=True)
    
    def __str__(self):
        return self.internship_title

    
class MentorSupportSession(models.Model):
    mentor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mentor_sessions')
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='student_sessions')
    scheduled_date_time = models.DateTimeField()
    zoom_link = models.URLField()
    passcode = models.CharField(max_length=255,default=0)
    price=models.IntegerField("Price", default=0)

    def __str__(self):
        return f'Mentor Session for {self.student.username} with {self.mentor.username}'
    


class Webinar(models.Model):

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    webinar_title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    speaker = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2,default=0)
    date_time = models.DateTimeField()
    positions = models.PositiveIntegerField()
    application_deadline = models.DateField()
    organizer_name = models.CharField(max_length=255, blank=True, null=True)
    organizer_email = models.EmailField(blank=True)
    platform = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='webinar_thumbnails', blank=True, null=True)
    selected_benefits = models.TextField(blank=True, null=True)

    def save_selected_benefits(self, benefits):
        self.selected_benefits = ",".join(benefits)

    def get_selected_benefits(self):
        return self.selected_benefits.split(",") if self.selected_benefits else []
    
    def __str__(self):
        return self.webinar_title


class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)  # Link the payment to a user
    course = models.ForeignKey(Oncourse, on_delete=models.CASCADE,null=True)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE,null=True)
    mentorSupportSession = models.ForeignKey(MentorSupportSession, on_delete=models.CASCADE,null=True)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE,null=True)
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



class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Oncourse, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    # Add any other fields you need for the certificate

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.course_title}"


class Benefit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Message(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


    
class QuestionPaper(models.Model):
    exam_type_choices = [
        ('KEAM', 'KEAM'),
        ('NEET', 'NEET'),
        ('JEE', 'JEE'),
        # Add more exam types as needed
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    exam_type = models.CharField(max_length=50, choices=exam_type_choices)
    year = models.IntegerField()
    subject = models.CharField(max_length=100)
    question_paper = models.FileField(upload_to='question_papers/')
    solution = models.FileField(upload_to='solutions/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.exam_type} {self.year}"
    

class Review(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Oncourse, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"