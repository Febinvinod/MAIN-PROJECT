from django.urls import path,include
from.import views
from .views import schedule_mentor_session

app_name = 'courseprovider'

urlpatterns = [
    
   path('', views.addcourses, name='addcourses'),
   path('addCourseprovider/',views.addCourseprovider,name='addprovider'),
   path('addmentor/',views.addmentor,name='addmentor'),
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
   path('confirmintern/<int:internship_id>/', views.confirmintern, name='confirmintern'),
   path('enroll/', views.enroll, name='enroll'),
   path('course/<int:course_id>/enrollments/', views.enrollment_details, name='enrollment_details'),
   path('internship/<int:internship_id>/enrollments/', views.internenroll, name='internenroll'),
   path('internlist/', views.internlist, name='internlist'),
   path('edit_internship/<int:internship_id>/', views.edit_internship, name='edit_internship'),
   path('delete_internship/<int:internship_id>/', views.delete_internship, name='delete_internship'),
   path('success/', views.success, name='success'),
   path('dead/', views.dead, name='dead'),
   path('mark_video_as_checked/<int:video_id>/<int:course_id>/', views.mark_video_as_checked, name='mark_video_as_checked'),
   path('view_certificate/<int:course_id>/', views.view_certificate, name='view_certificate'),
   path('generate_certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
   path('certificate_template_no_buttons/', views.certificate_template_no_buttons, name='certificate_template_no_buttons'),
   path('download_certificate/<int:certificate_id>/', views.download_certificate, name='download_certificate'),
   path('schedule_mentor_session/', views.schedule_mentor_session, name='schedule_mentor_session'),
   path('mentor_support_session_list/', views.mentor_support_session_list, name='mentor_support_session_list'),
   path('mentordash/', views.mentordash, name='mentordash'),
   path('paymenthandl/',views.paymenthandl,name='paymenthandl'),
   path('confirmsession/<str:scheduled_time>/', views.confirmsession, name='confirmsession'),
   path('addwebinar/', views.addwebinar, name='addwebinar'),

   # path('generate_certificate/', views.generate_certificate, name='generate_certificate'),
   # path('certificate_download/<int:certificate_id>/', views.certificate_download, name='certificate_download'),
]
