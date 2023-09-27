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
from django.http import JsonResponse

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Oncourse, Video,Payment
from django.views.generic.edit import UpdateView, DeleteView
from collections import defaultdict
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
from django.urls import reverse




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
            Video.objects.create(course=new_course, video_file=video, section_name=section)
                
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
    course = Oncourse.objects.get(id=course_id)
    sections = Video.objects.filter(course=course).values_list('section_name', flat=True).distinct()
    videos_by_section = {}
    for section in sections:
        videos_by_section[section] = Video.objects.filter(course=course, section_name=section)

    context = {
        'oncourse': course,
        'sections': sections,
        'videos_by_section': videos_by_section,
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
                video, created = Video.objects.get_or_create(course=course, section_name=section_names[i])
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
    if user.role == CustomUser.STUDENT:
        assessments = StudentAssessment.objects.filter(student=user)
        return render(request, 'studash.html', {'user': user, 'assessments': assessments})

    return render(request, 'studash')

def intern(request):
    return render(request, 'addintern.html')


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))




@csrf_exempt
def paymenthandler(request):
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
            return render(request, 'courselist.html')
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

    context = {
        'user_courses': user_courses,
    }

    return render(request, 'providerdash.html', context)


def confirm(request,course_id):
    
    
    course = Oncourse.objects.get(pk=course_id)


    # For Razorpay integration
    currency = 'INR'
    amount = course.price  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    #course_title = course.course_title
    

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/courseprovider/paymenthandler/'  # Define your callback URL here


    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
   # payment.course_title.add(course_title)
    payment.save()

    # Prepare the context data
    context = {
        'user': request.user,
        'oncourse':course,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        
    }

    return render(request, 'confirm.html', context)