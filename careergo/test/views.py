from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from .models import course  # Import your Course model



# Create your views here.
def assesment(request):
    return render(request,'assesment.html')
def coursess(request):
    courses = course.objects.all()
    return render(request, 'course.html', {'courses': courses})

# test/views.py



