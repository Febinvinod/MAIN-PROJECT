from django.db import models
from django.conf import settings

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
    


class StudentAssessment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logical_reasoning_score = models.PositiveIntegerField(default=0)
    communication_skills_score = models.PositiveIntegerField(default=0)
    quantitative_aptitude_score = models.PositiveIntegerField(default=0)
    analytical_skills_score = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)
    stream = models.CharField(max_length=50, choices=[('science', 'Science'), ('commerce', 'Commerce'), ('humanities', 'Humanities')], blank=True, null=True)
    plus_two_cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    assessment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username}'s Assessment"
