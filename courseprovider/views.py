from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib  import messages,auth
from home.models import CustomUser,UserProfile
from courseprovider.models import Courseprovider_profile,Mentor_profile
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
from .forms import CustomUserForm
from test.models import StudentAssessment
from django.http import JsonResponse
from django.http import HttpResponse
import pdfkit
from django.template import Context, loader

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Oncourse, Video,Payment,Internship,UserVideo,Certificate
from django.views.generic.edit import UpdateView, DeleteView
from collections import defaultdict
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
import datetime

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files import File
from django.db.models import Count

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MentorSupportSession
from django.utils import timezone
from datetime import timedelta,time
import secrets
from datetime import datetime, timedelta, time
from twilio.rest import Client





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



@login_required
def addmentor(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']

            # Send welcome email
            send_welcome_email(user.username, password, user.first_name,user.email)

            user.set_password(password)
            user.is_active = True

            user.role = CustomUser.MENTOR 
            user.save()

            # Check if the user has the role=2 
            if user.role == CustomUser.MENTOR:
                Mentor = Mentor_profile(user=user)  
                Mentor.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            return redirect('index')

    else:
        user_form = CustomUserForm()

    context = {
        'user_form': user_form,
    }

    return render(request, 'addmentor.html', context)



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
        price_str = request.POST.get('price', '')
        price = int(price_str) if price_str else 0
        instructor= request.POST.get('instructor')
        thumbnail = request.FILES['thumbnail']
        category = request.POST['category']
        is_free = request.POST.get('is_free') == 'on'

       
      
        #video = request.FILES.get('video')
        if category == 'other':
            category = request.POST.get('other_category')
         

        # If "Other" is selected, use the value from the "Other Category" input field
        print({price})
    
        print({is_free})
        new_course = Oncourse(user=user, course_title = course_title ,price=price, 
                            description=description,duration=duration, thumbnail=thumbnail ,category=category, instructor=instructor,is_free=is_free,)
                            
        
        new_course.save()

        sections = request.POST.getlist('section_name[]')

        videos = request.FILES.getlist('videos[]')
        for section, video in zip(sections, videos):
            Video.objects.create(course=new_course, video_file=video, section_name=section,user_id=request.user.id)
                
        return redirect('courseprovider:courselist')
    
    return render(request, 'addcourse.html',context)


def courselist(request):
    query = request.GET.get('q')
    show_carousel = not bool(query)

    if query:
        # Perform a case-insensitive search on relevant fields
        if query.lower() == 'free':
            free_courses = Oncourse.objects.filter(is_free=True)
            all_courses = free_courses
        else:
            # Perform a case-insensitive search on relevant fields
            all_courses = Oncourse.objects.filter(
                Q(course_title__icontains=query) |
                Q(instructor__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
    else:
         all_courses = Oncourse.objects.all()
    

    free_courses = all_courses.filter(is_free=True)
    # Group courses by category
    courses_by_category = defaultdict(list)
    for course in all_courses:
        if not course.is_free:
            courses_by_category[course.get_category_display()].append(course)

    context = {
        'courses_by_category': dict(courses_by_category), 
        'query': query,
        'show_carousel': show_carousel,
        'free_courses': free_courses, # Convert defaultdict to a regular dictionary
    }

    return render(request, 'courselist.html', context)

# def coursedetail(request,course_id):
#      course = Oncourse.objects.get(id=course_id)
#      sections = Video.objects.filter(course=course).values_list('section_name', flat=True).distinct()
#      videos_by_section = {}
#      for section in sections:
#         videos_by_section[section] = Video.objects.filter(course=course, section_name=section)

#      context = {'oncourse': course,
#                 'sections': sections,
#                 'videos_by_section': videos_by_section,}
     
#      return render(request,'course_detail.html', context)
def coursedetail(request, course_id):
    #course = Oncourse.objects.get(id=course_id)
    course = get_object_or_404(Oncourse, pk=course_id)
    payment = Payment.objects.filter(user=request.user, course=course, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)
    user = request.user
    videos = Video.objects.filter(course_id=course_id)
    all_videos_completed = all(UserVideo.objects.filter(user=user, video=video, checked=True).exists() for video in videos)
    checked_video_ids = UserVideo.objects.filter(user=user, checked=True).values_list('video__id', flat=True)

    sections = Video.objects.filter(course=course).values_list('section_name', flat=True).distinct()
    videos_by_section = {}
    for section in sections:
        videos_by_section[section] = Video.objects.filter(course=course, section_name=section)

    context = {
        'user': user,
        'oncourse': course,
        'sections': sections,
        'videos_by_section': videos_by_section,
        'payment' : payment,
        'all_videos_completed': all_videos_completed,
        'checked_video_ids': checked_video_ids, 
    }

    # Create a Razorpay Order
   

    return render(request, 'course_detail.html', context)





# def edit_course(request, course_id):
#     course = get_object_or_404(Oncourse, id=course_id)
    
#     if request.method == 'POST':
#         # Handle form submission and update the course details
#         course.course_title = request.POST['course_title']
#         course.description = request.POST['description']
#         course.duration = request.POST['duration']
#         course.price = request.POST['price']
#         course.category = request.POST['category']
#         if 'thumbnail' in request.FILES:
#             course.thumbnail = request.FILES['thumbnail']
#         if 'video' in request.FILES:
#             course.video = request.FILES['video']
#         course.save()
#         return redirect('courseprovider:providerdash')

#     context = {
#         'course': course,
#     }
#     return render(request, 'edit_course.html', context)

def edit_course(request, course_id):
    course = get_object_or_404(Oncourse, id=course_id)
    videos = Video.objects.filter(course=course)  # Get related videos
    category = Oncourse.CATEGORY_CHOICES
    context = {'category': category} 
    
    if request.method == 'POST':
        # Handle form submission and update the course details
        course.course_title = request.POST['course_title']
        course.description = request.POST['description']
        course.duration = request.POST['duration']
        course.price = request.POST['price']
        course.category = request.POST['category']
        course.instructor=request.POST['instructor']
        
        # Handle the "Other" category option
        if course.category == 'other':
            course.category = request.POST['other_category']
        
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail']
        
        course.save()
        
        # Update or create videos
        video_files = request.FILES.getlist('videos[]')
        section_names = request.POST.getlist('section_name[]')
        
        # Delete existing videos not in the form
        Video.objects.filter(course=course).exclude(section_name__in=section_names).delete()
        
        for i, video_file in enumerate(video_files):
            if video_file:
                video, created = Video.objects.get_or_create(course_id=course_id, section_name=section_names[i],user_id=request.user.id)
                video.video_file = video_file
                video.save()
        
        return redirect('courseprovider:providerdash')

    context = {
        'course': course,
        'videos': videos,
        'category': category,
    }
    return render(request, 'edit_course.html', context)


def delete_course(request, course_id):
    course = get_object_or_404(Oncourse, id=course_id)
    
    if request.method == 'POST':
        # Handle course deletion
        course.delete()
        return redirect('courseprovider:providerdash')

    context = {
        'course': course,
    }
    return render(request, 'delete_course.html', context)

def admindash(request):
    users = CustomUser.objects.filter(role__in=[CustomUser.STUDENT, CustomUser.COURSE_PROVIDER, CustomUser.MENTOR])

    course_providers = users.filter(role=CustomUser.COURSE_PROVIDER)
    courses_by_provider = {}
    for provider in course_providers:
        courses = Oncourse.objects.filter(user=provider)
        courses_by_provider[provider] = courses

    # Retrieve internships for each course provider
    internships_by_provider = {}
    for provider in course_providers:
        internships = Internship.objects.filter(user=provider)
        internships_by_provider[provider] = internships
    #course_providers = users.filter(role=CustomUser.COURSE_PROVIDER)
    assessments = StudentAssessment.objects.filter(student__in=users)
    return render(request, 'admindash.html', {'users': users,'assessments': assessments,'courses_by_provider': courses_by_provider,
        'internships_by_provider': internships_by_provider,})
    

def toggle_user_status(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    
    if request.method == 'POST':
        # Toggle the user's status
        user.is_active = not user.is_active
        user.save()
    
    return redirect('/courseprovider/admindash')

def update_assessment_status(request, assessment_id):
    assessment = get_object_or_404(StudentAssessment, id=assessment_id)
    
    if request.method == 'POST':
        # Update the assessment_status based on the checkbox value
        assessment.assessment_status = request.POST.get('assessment_status') == 'on'
        assessment.save()
    
    return redirect('/courseprovider/admindash')  

@login_required
def studash(request):
    user = request.user
    enrolled_courses = Payment.objects.filter(user=request.user,course__isnull=False,payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)
    enrolled_internships = Payment.objects.filter(user=request.user, internship__isnull=False,payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)
    certificates = Certificate.objects.filter(user=user)
    mentor_sessions = MentorSupportSession.objects.filter(student=user)
    #enrolled_courses = Payment.objects.filter(user=request.user,payment_status=Payment.PaymentStatusChoices.SUCCESSFUL )
    if user.role == CustomUser.STUDENT:
        assessments = StudentAssessment.objects.filter(student=user)
        return render(request, 'studash.html', {'user': user, 'assessments': assessments, 'enrolled_courses': enrolled_courses, 'enrolled_internships': enrolled_internships,'certificates': certificates, 'mentor_sessions': mentor_sessions})

    return render(request, 'studash')



def intern(request):
    category = Internship.CATEGORY_CHOICES
    context = {'category': category} 

    if request.method == 'POST':
      
      new_intern = Internship()
      user = request.user
      internship_title = request.POST['course_title']
      description = request.POST['description']
      duration = int(request.POST['duration'])
      price = request.POST.get('price','')
      #price = Decimal(price)
      instructor= request.POST.get('instructor')
      start_date = request.POST['start_date']
      end_date = request.POST['end_date']
      positions = int(request.POST['positions'])
      internship_type = request.POST['internship_type']
      internship_mode = request.POST['internship_mode']
      application_deadline = request.POST['application_deadline']
      company_name = request.POST['company_name']
      company_website = request.POST['company_website']

      thumbnail = request.FILES['thumbnail']
      category = request.POST['category']

      if category == 'other':
            
            category = request.POST.get('other_category')

   

      new_intern = Internship(user=user, internship_title = internship_title ,price=price, 
                            description=description,duration=duration, thumbnail=thumbnail ,category=category, instructor=instructor,start_date=start_date,end_date=end_date,positions=positions,internship_type=internship_type,internship_mode=internship_mode,application_deadline=application_deadline,company_name=company_name,company_website=company_website)
                                
      new_intern.save()
      return redirect('courseprovider:internlist')
    
    return render(request, 'addintern.html',context)
     
   




razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def paymenthandler(request):
    #course = get_object_or_404(Oncourse, id=course_id)
    # Only accept POST requests.
    
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        print(result)

        if result is not None:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.amount * 100)  # Convert Decimal to paise

            # Capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

           
     # Update the order with payment ID and change status to "Successful"
            payment.payment_id = payment_id
            payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
            payment.save()

            
            # Render success page on successful capture of payment
            return redirect('courseprovider:success')
        else:
            # If signature verification fails, render the payment failure page
            return render(request, 'paymentfail.html')

    else:
        # If a request other than POST is made, return a bad request
        return HttpResponseBadRequest()


def providerdash(request):
    # Get the courses added by the logged-in user
    user = request.user
    user_courses = Oncourse.objects.filter(user=user)
    user_internships = Internship.objects.filter(user=user)

    context = {
        'user_courses': user_courses,
        'user_internships': user_internships,
    }

    return render(request, 'providerdash.html', context)

def mentordash(request):
    mentor = request.user

    # Retrieve mentor support sessions created by the current mentor
    mentor_sessions = MentorSupportSession.objects.filter(mentor=mentor)

    return render(request, 'mentordash.html', {'mentor_sessions': mentor_sessions})


def enrollment_details(request, course_id):
    # Get the course for which you want to display enrollment details
    course = Oncourse.objects.get(id=course_id)
    
    # Get all payment records for this course
    enrollments = Payment.objects.filter(course=course, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)

    context = {
        'course': course,
        'enrollments': enrollments,
    }

    return render(request, 'enrollment_details.html', context)


def internenroll(request,internship_id):
    internship = Internship.objects.get(id=internship_id)

    enrollments = Payment.objects.filter(internship=internship, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)

    context = {
       
        'internship': internship,
        'enrollments': enrollments,
    }
    return render(request, 'internenroll.html', context)


# def confirm(request,course_id):
    
#     course = Oncourse.objects.get(id=course_id)


#     # For Razorpay integration
#     currency = 'INR'
#     amount = course.price  # Get the subscription price
#     amount_in_paise = int(amount * 100)  # Convert to paise
#     
    

#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(
#         amount=amount_in_paise,
#         currency=currency,
#         payment_capture='0'
#     ))

#     # Order ID of the newly created order
#     razorpay_order_id = razorpay_order['id']
#     callback_url = '/courseprovider/paymenthandler/'  # Define your callback URL here


#     payment = Payment.objects.create(
#         user=request.user,
#         razorpay_order_id=razorpay_order_id,
#         course=course,  
#         payment_id="",
#         amount=amount,
#         currency=currency,
#         payment_status=Payment.PaymentStatusChoices.PENDING,
#     )
#    
#     payment.save()

#     # Prepare the context data
#     context = {
#         'user': request.user,
#         'oncourse':course,
#         'razorpay_order_id': razorpay_order_id,
#         'razorpay_merchant_key': settings.RAZOR_KEY_ID,
#         'razorpay_amount': amount_in_paise,
#         'currency': currency,
#         'amount': amount_in_paise / 100,
#         'callback_url': callback_url,
        
#     }

#     return render(request, 'confirm.html', context)

def confirm(request, course_id):
    course = get_object_or_404(Oncourse, pk=course_id)
    user = request.user
    # Check if the user is already enrolled in the course
    existing_payment = Payment.objects.filter(user=request.user, course=course, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL).first()
    
    if existing_payment:
        # User is already enrolled, redirect to a page indicating this
        return render(request, 'already_enrolled.html')
    
    if course.is_free:
        # For free courses, create a payment entry with a "successful" status
        Payment.objects.create(
            user=request.user,
            course=course,
            razorpay_order_id="",
            payment_id="",
            amount=0,  # Set the amount to 0 for free courses
            currency="INR",  # Update with the appropriate currency code
            payment_status=Payment.PaymentStatusChoices.SUCCESSFUL  # Set to "successful" for free courses
        )
        
        # Redirect to the success page or course details page
        return redirect('courseprovider:success')
    
    # Continue with payment confirmation logic
    currency = 'INR'
    amount = course.price  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/courseprovider/paymenthandler/'  # Define your callback URL here

    payment = Payment.objects.create(
        user=request.user,
        course=course,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    payment.save()

    context = {
        'user': request.user,
        'oncourse': course,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
    }

    return render(request, 'confirm.html', context)


def enroll(request, course_id):
    course = get_object_or_404(Oncourse, id=course_id)
    context = {
        'course' : course,
    }

    return render(request,'already_enrolled.html', context)

def internlist(request):
    internships_by_category = {} 

    query = request.GET.get('q', '')
    

    # Filter internships based on the search query
    internships = Internship.objects.filter(
        Q(internship_title__icontains=query) |
        Q(duration__icontains=query) |
        Q(instructor__icontains=query) |
        Q(category__icontains=query)
    )

    # Group filtered internships by category
    for internship in internships:
        category = internship.get_category_display()
        if category not in internships_by_category:
            internships_by_category[category] = []
        internships_by_category[category].append(internship)

    return render(request, 'internlist.html', {'internships_by_category': internships_by_category, 'query': query})

def delete_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)

    # Check if the logged-in user is the owner of the internship
    if request.user == internship.user:
        if request.method == 'POST':
            # Delete the internship
            internship.delete()

            # Redirect to the dashboard or a success page after deleting
            return redirect('courseprovider:providerdash')

        return render(request, 'delete_internship.html', {'internship': internship})
    

def edit_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    category = Internship.CATEGORY_CHOICES
    print(internship.start_date)  # Check if this prints the start date value
    print(internship.end_date) 
   
    # Check if the logged-in user is the owner of the internship
    if request.user == internship.user:
        if request.method == 'POST':

            # Handle form submission to update the internship
            # You can create an internship edit form and process it here
            internship.internship_title = request.POST['course_title']
            internship.description = request.POST['description']
            internship.duration = int(request.POST['duration'])
            internship.price = request.POST.get('price','')
      
            internship.instructor= request.POST.get('instructor')
            internship.start_date = request.POST['start_date']
            internship.end_date = request.POST['end_date']
            internship.positions = int(request.POST['positions'])
            internship.internship_type = request.POST['internship_type']
            internship.internship_mode = request.POST['internship_mode']
            internship.application_deadline = request.POST['application_deadline']
            internship.company_name = request.POST['company_name']
            internship.company_website = request.POST['company_website']
            if internship.category == 'other':
                     internship.category = request.POST['other_category']
            
            if 'thumbnail' in request.FILES:
                    internship.thumbnail = request.FILES['thumbnail']

            internship.save()


            # Redirect to the dashboard or a success page after editing
            return redirect('courseprovider:providerdash')

        return render(request, 'edit_internship.html', {'internship': internship,'category': category})
    
def confirmintern(request, internship_id):
    internship=get_object_or_404(Internship, pk=internship_id)

    existing_payment = Payment.objects.filter(user=request.user, internship=internship, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL).first()
    
    if existing_payment:
        # User is already enrolled, redirect to a page indicating this
        return render(request, 'already_enrolled.html')
    
    if internship.application_deadline < timezone.now().date():
        # Application deadline has passed, do not allow registration
        return render(request, 'dead.html')
    
    enrolled_users_count = Payment.objects.filter(internship=internship, payment_status=Payment.PaymentStatusChoices.SUCCESSFUL).count()
    if enrolled_users_count >= internship.positions:
        # Maximum positions reached, do not allow registration
        return render(request, 'max_positions_reached.html')
    
    # Continue with payment confirmation logic
    currency = 'INR'
    amount = internship.price  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/courseprovider/paymenthandler/'  # Define your callback URL here

    payment = Payment.objects.create(
        user=request.user,
        internship=internship,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    payment.save()

    context = {
        'user': request.user,
        'internship': internship,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
    }

    return render(request, 'confirmintern.html', context)

def success(request):
    return render(request, 'success.html')
def dead(request):
    return render(request,'dead.html') 


@csrf_exempt
def mark_video_as_checked(request, video_id, course_id):
    print(video_id)
    try:
        # Assuming you have a way to authenticate the user, for example, using request.user
        user = request.user
        # video = Video.objects.get(id=video_id, course_id=course_id)


        # Check if the UserVideo record exists, and if not, create one
        user_video, created = UserVideo.objects.get_or_create(user=user, video_id=video_id,course_id=course_id)

        # Set the checked field to True
        user_video.checked = True
        user_video.save()

        return JsonResponse({"success": "success"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def generate_certificate(request, course_id):
    # Fetch course details, user name, and other required data
    course = Oncourse.objects.get(pk=course_id)
    user = request.user
    existing_certificate = Certificate.objects.filter(user=user, course=course).first()

    if existing_certificate:
        # If a certificate already exists, return it without creating a new one
        return existing_certificate
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Create and save the certificate in the database
    certificate = Certificate(user=user, course=course, issued_date=current_date)
    certificate.save()

    return certificate

def view_certificate(request, course_id):
    course = Oncourse.objects.get(pk=course_id)  # Adjust this based on your models
    #current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    certificate = generate_certificate(request, course_id)
    if isinstance(certificate, HttpResponse):
        return certificate  
    context = {
        'course': certificate.course,
        'current_date': certificate.issued_date.strftime("%Y-%m-%d"),
        'user': certificate.user,
        'certificate_id': certificate.id ,
    }
    
    return render(request, 'download_certificate.html', context)



def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)

    # Load the HTML template as a Django template
    template = loader.get_template('certificate_with_download_button.html')

    # Define the context as a dictionary
    context = {
        'user': certificate.user,
        'course': certificate.course,
        'current_date': certificate.issued_date.strftime("%Y-%m-%d"),
        'certificate':certificate,
    }

    # Render the template with the context
    rendered_html = template.render(context)

    # Create a PDF response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{certificate.user.username}_certificate.pdf"'

    # Specify the path to wkhtmltopdf executable in a list of options
    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'quiet': '',  # Disable wkhtmltopdf console output
    }

    # Generate the PDF from the HTML content using pdfkit with the config
    pdf_data = pdfkit.from_string(rendered_html, False, options=pdfkit_options, configuration=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'))

    # Write the PDF data to the response
    response.write(pdf_data)

    return response

def certificate_template_no_buttons(request):
    return render(request, 'certificate_with_download_button.html')




def generate_zoom_link():
    # Replace these with your Zoom API credentials
    api_key = "eyfacwRzQvVPMWWqxg"
    api_secret = "JHpDF4MfDnMPkal6W232ruCSoCKfy2yD"

    # Generate a random meeting ID using the secrets module
    meeting_id = "7431680782"

    # Construct the Zoom link
    zoom_link = f"https://zoom.us/j/{meeting_id}?pwd={api_secret}&api_key={api_key}"

    return zoom_link

def mentor_support_session_list(request):
    mentor_sessions = MentorSupportSession.objects.all().order_by('-scheduled_date_time')[:1]
    return render(request, 'mentor_support_session_list.html', {'mentor_sessions': mentor_sessions})


def generate_time_slots():
    current_date = timezone.now().date() + timedelta(days=1)  # Start from tomorrow
    time_slots_by_date = {}

    for days_offset in range(3):  # Generate time slots for the next three days
        current_date_key = current_date + timedelta(days=days_offset)
        time_slots = []

        for hour in [9, 11, 14, 17, 19]:  # 9 am, 11 am, 2 pm, 5 pm, 7 pm
            current_time = datetime.combine(current_date_key, time(hour, 0))
            formatted_time = current_time.strftime('%Y-%m-%d %I:%M %p')
            time_slot_data = {'formatted_time': formatted_time, 'readonly': False}

            # Check if the time slot is already booked
            if MentorSupportSession.objects.filter(scheduled_date_time=current_time).exists():
                time_slot_data['readonly'] = True

            time_slots.append(time_slot_data)

        time_slots_by_date[current_date_key] = time_slots

    return time_slots_by_date

# def schedule_mentor_session(request):
#     mentors = get_user_model().objects.filter(role=CustomUser.MENTOR)
#     students = get_user_model().objects.filter(role=CustomUser.STUDENT)

#     if request.method == 'POST':
#         mentor_id = request.POST.get('mentor')
#         student_id = request.POST.get('student')
#         selected_time = request.POST.get('selected_time')

#         mentor = get_user_model().objects.get(id=mentor_id)
#         student = get_user_model().objects.get(id=student_id)

#         # Convert selected_time to a datetime object
#         scheduled_time = datetime.strptime(selected_time, '%Y-%m-%d %I:%M %p')

#         # Check if the time slot is already booked
#         if MentorSupportSession.objects.filter(scheduled_date_time=scheduled_time).exists():
#             # Handle the case where the time slot is already booked
#             # You can redirect to an error page or show a message to the user
#             pass
#         else:
#             zoom_link = generate_zoom_link()  # Implement a function to generate Zoom link

#             passcode = "3Tf3aa"
#             MentorSupportSession.objects.create(
#                 mentor=mentor,
#                 student=student,
#                 scheduled_date_time=scheduled_time,
#                 zoom_link=zoom_link,
#                 passcode=passcode,
#                 price=1500,
#             )


#             mentor_whatsapp_number = "+916238994851"
#             session_datetime = scheduled_time.strftime('%Y-%m-%d %I:%M %p')

#             send_whatsapp_notification(mentor_whatsapp_number, session_datetime,student.username, student.email)

#             return redirect('courseprovider:mentor_support_session_list')

#     time_slots_by_date = generate_time_slots()

#     return render(request, 'schedule_mentor_session.html', {'mentors': mentors, 'students': students, 'time_slots_by_date': time_slots_by_date})


def send_whatsapp_notification(to_number, session_datetime, student_username, student_email):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_body = (
        f"Hello! You have a mentor support session scheduled for {session_datetime} with {student_username} "
        f"({student_email}). Please be prepared."
    )
    from_whatsapp = f"whatsapp:{settings.TWILIO_PHONE_NUMBER}"
    to_whatsapp = f"whatsapp:{to_number}"

    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp,
        to=to_whatsapp
    )

    print(f"WhatsApp message sent to {to_number} successfully. SID: {message.sid}")




from urllib.parse import parse_qs

@csrf_exempt
def paymenthandl(request):
    #course = get_object_or_404(Oncourse, id=course_id)
    # Only accept POST requests.
    user = request.user  # Initialize with a default value\
    mentor = get_user_model().objects.filter(role=CustomUser.MENTOR).first()
    scheduled_time_param = request.GET.get('scheduled_time', '')

    if scheduled_time_param:
        scheduled_time = datetime.strptime(scheduled_time_param, '%Y-%m-%d %I:%M %p')


    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        print(result)

        if result is not None:

            zoom_link = generate_zoom_link()  # Implement a function to generate Zoom link
            passcode = "3Tf3aa"
            mentorSupportSession = MentorSupportSession.objects.create(
                mentor=mentor,
                student=user,
                scheduled_date_time=scheduled_time,
                zoom_link=zoom_link,
                passcode=passcode,
                price=1500,
            )
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            amount = int(payment.amount * 100)  # Convert Decimal to paise

            # Capture the payment
            razorpay_client.payment.capture(payment_id, amount)
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

           
     # Update the order with payment ID and change status to "Successful"
            payment.payment_id = payment_id
            payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
            payment.mentorSupportSession = mentorSupportSession
            payment.save()

            
            student = user

            mentor_whatsapp_number = "+916238994851"
            session_datetime = scheduled_time.strftime('%Y-%m-%d %I:%M %p')

            send_whatsapp_notification(mentor_whatsapp_number, session_datetime,student.username, student.email)

            # Render success page on successful capture of payment
            return redirect('courseprovider:mentor_support_session_list')
        else:
            # If signature verification fails, render the payment failure page
            return render(request, 'paymentfail.html')

    else:
        # If a request other than POST is made, return a bad request
        return HttpResponseBadRequest()



def schedule_mentor_session(request):
    mentors = get_user_model().objects.filter(role=CustomUser.MENTOR)
    students = get_user_model().objects.filter(role=CustomUser.STUDENT)

    if request.method == 'POST':
        mentor = request.POST.get('mentor')
        student = request.POST.get('student')
        selected_time = request.POST.get('selected_time')

        # Convert selected_time to a datetime object
        scheduled_time = datetime.strptime(selected_time, '%Y-%m-%d %I:%M %p')

        # Check if the time slot is already booked
        if MentorSupportSession.objects.filter(scheduled_date_time=scheduled_time).exists():
            # Handle the case where the time slot is already booked
            # You can redirect to an error page or show a message to the user
            pass
        else:
            return redirect('courseprovider:confirmsession',scheduled_time=scheduled_time)

    time_slots_by_date = generate_time_slots()

    return render(request, 'schedule_mentor_session.html', {'mentors': mentors, 'students': students, 'time_slots_by_date': time_slots_by_date})


from urllib.parse import urlencode

def confirmsession(request,scheduled_time):
    user = request.user  # Initialize with a default value\
    mentor = get_user_model().objects.filter(role=CustomUser.MENTOR).first()

    scheduled_time = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')

           
    currency = 'INR'
    amount = 1500  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise

    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))
    razorpay_order_id = razorpay_order['id']
    scheduled_time_param = scheduled_time.strftime('%Y-%m-%d %I:%M %p')
    callback_url_params = {'scheduled_time': scheduled_time_param}
    callback_url = f'/courseprovider/paymenthandl/?{urlencode(callback_url_params)}'
    
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    payment.save()

    mentor_whatsapp_number = "+916238994851"
    
    context = {
        'user': request.user,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'mentor': mentor,
        'scheduled_time': scheduled_time,
    }

    return render(request, 'confirmsession.html', context)


def addwebinar(request):
    all_benefits = ["Live Interaction", "Q&A Session", "Certificate of Completion", "Networking Opportunities"]
    return render(request, 'addwebinar.html', {'all_benefits': all_benefits})











    