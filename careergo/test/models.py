from django.db import models

# Create your models here.
class course(models.Model):
    COURSE_TYPES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('Diploma', 'Diploma'),
    ]

    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    eligibility = models.CharField(max_length=20)
    entrance_exam = models.CharField(max_length=100, blank=True)
    college = models.TextField(max_length=400)

    def __str__(self):
        return self.title