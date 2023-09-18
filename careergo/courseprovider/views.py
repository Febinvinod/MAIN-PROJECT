from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib  import messages,auth
from home.models import CustomUser,UserProfile
from courseprovider.models import Courseprovider_profile
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
from .forms import CustomUserForm
from test.models import StudentAssessment

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Oncourse
from django.views.generic.edit import UpdateView, DeleteView
from collections import defaultdict


# from .decorators import user_not_authenticated
# from .tokens import account_activation_token

@login_required
def addCourseprovider(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']

            # Send welcome email
            send_welcome_email(user.username, password, user.first_name,user.email)

            user.set_password(password)
            user.is_active = True

            user.role = CustomUser.COURSE_PROVIDER 
            user.save()

            # Check if the user has the role=2 
            if user.role == CustomUser.COURSE_PROVIDER:
                Courseprovider = Courseprovider_profile(user=user)  
                Courseprovider.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            return redirect('index')

    else:
        user_form = CustomUserForm()

    context = {
        'user_form': user_form,
    }

    return render(request, 'addprovider.html', context)



def send_welcome_email(username, password, name,email):

    login_url = 'http://127.0.0.1:8000/login'  # Update with your actual login URL
    login_button = f'Click here to log in: {login_url}\n'


    subject = 'CareeGo - Course Provider Registration'
    message = f"Hello {name},\n\n"
    message += f"Welcome to Careergo, We are thrilled to have you on board as a part of our dedicated team of providers.\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Username: {username}\nPassword: {password}\n\n"
    message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    message += login_button 
    message += "Thank you for joining the CareerGo community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe CareerGo Team\n\n"
    


    from_email='amalraj89903@gmail.com'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)


def addcourses(request):
    
    category = Oncourse.CATEGORY_CHOICES
    context = {'category': category} 
    if request.method == 'POST':
        
        new_course = Oncourse()
        user = request.user
        course_title = request.POST['course_title']
        description = request.POST['description']
        duration = request.POST['duration']
        price = request.POST['price']
        instructor =  request.POST['instructor']
        thumbnail = request.FILES['thumbnail']
        category = request.POST['category']
      
        video = request.FILES.get('video')
       
        
        
       
        
        new_course = Oncourse(user=user, course_title = course_title ,price=price, 
                            description=description,duration=duration,instructor=instructor, thumbnail=thumbnail ,category=category,video=video)
                            
        
        new_course.save()
        
                
        return redirect('courseprovider:courselist')
    
    return render(request, 'addcourse.html',context)


def courselist(request):
    # single_course = Oncourse.objects.all() 
    # return render(request,'courselist.html', {'single_course':single_course})

    all_courses = Oncourse.objects.all()

    # Group courses by category
    courses_by_category = defaultdict(list)
    for course in all_courses:
        courses_by_category[course.get_category_display()].append(course)

    context = {
        'courses_by_category': dict(courses_by_category),  # Convert defaultdict to a regular dictionary
    }

    return render(request, 'courselist.html', context)

def coursedetail(request,course_id):
     course = Oncourse.objects.get(id=course_id)
     context = {'oncourse': course}
     return render(request,'course_detail.html', context)

def edit_course(request, course_id):
    course = get_object_or_404(Oncourse, id=course_id)
    
    if request.method == 'POST':
        # Handle form submission and update the course details
        course.course_title = request.POST['course_title']
        course.description = request.POST['description']
        course.duration = request.POST['duration']
        course.price = request.POST['price']
        course.instructor = request.POST['instructor']
        course.category = request.POST['category']
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail']
        if 'video' in request.FILES:
            course.video = request.FILES['video']
        course.save()
        return redirect('courseprovider:courselist')

    context = {
        'course': course,
    }
    return render(request, 'edit_course.html', context)

def delete_course(request, course_id):
    course = get_object_or_404(Oncourse, id=course_id)
    
    if request.method == 'POST':
        # Handle course deletion
        course.delete()
        return redirect('courseprovider:courselist')

    context = {
        'course': course,
    }
    return render(request, 'delete_course.html', context)

def admindash(request):
    users = CustomUser.objects.filter(role__in=[CustomUser.STUDENT, CustomUser.COURSE_PROVIDER, CustomUser.MENTOR])

    #course_providers = users.filter(role=CustomUser.COURSE_PROVIDER)
    assessments = StudentAssessment.objects.filter(student__in=users)
    return render(request, 'admindash.html', {'users': users,'assessments': assessments})

def toggle_user_status(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    
    if request.method == 'POST':
        # Toggle the user's status
        user.is_active = not user.is_active
        user.save()
    
    return redirect('/courseprovider/admindash')
def studash(request):
     return render(request,'studash.html')
