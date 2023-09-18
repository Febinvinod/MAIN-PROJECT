from django.urls import path,include
from.import views
from django.contrib.auth import views as auth_views

app_name = 'test'

urlpatterns = [
    path('assessment', views.assessment,name="assessment"),
    path('course', views.coursess,name="course"),
   
   
]




   