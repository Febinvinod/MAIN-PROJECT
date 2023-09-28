from django.urls import path,include
from.import views


app_name = 'courseprovider'

urlpatterns = [
    
   path('', views.addcourses, name='addcourses'),
   path('addCourseprovider/',views.addCourseprovider,name='addprovider'),
   path('courselist/', views.courselist, name='courselist'),
   path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
   path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
   path('coursedetail/<int:course_id>/', views.coursedetail, name='coursedetail'),
   path('admindash/', views.admindash, name='admindash'),
   path('toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
   path('update_assessment_status/<int:assessment_id>/', views.update_assessment_status, name='update_assessment_status'),
   path('studash/', views.studash, name='studash'),
   path('intern/', views.intern, name='intern'),
   path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
   path('providerdash/', views.providerdash, name='providerdash'),
   path('confirm/<int:course_id>/', views.confirm, name='confirm'),
   path('enroll/', views.enroll, name='enroll'),
   
]
