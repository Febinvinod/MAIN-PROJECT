from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login ,authenticate,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib  import messages,auth
from .models import CustomUser,UserProfile
from courseprovider.models import Oncourse
from courseprovider.models import Courseprovider_profile
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
User = get_user_model()


# Create your views here.
def index(request):
    return render(request,'index.html',{'user':request.user})
def adminpage(request):
    return render(request,'adminpage.html')
def providerpage(request):
    return render(request,'providerpage.html')




def login(request):
    if request.method == 'POST':
        
         
         username = request.POST.get('username')
         password = request.POST.get('password')

         if username  and password:
              user = authenticate(request, username=username, password=password)
              if user is not None:
                   auth_login(request, user)
                   if request.user.role == CustomUser.ADMIN:
                       
                        return redirect(reverse('adminpage'))
                   
                   elif request.user.role == CustomUser.STUDENT:
                       
                        return redirect(reverse('index'))
                   elif request.user.role == CustomUser.COURSE_PROVIDER:
                       
                        return redirect(reverse('providerpage'))
              else:
                   messages.info(request,"Invalid User")
                   return redirect('login')
                #    error_message = "Invalid login credentials."
                #    return render(request, 'login.html', {'error_message': error_message})
        
    return render(request,'login.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        role = User.STUDENT

        if username and first_name and last_name and email and phone and password and role:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('/signup')
            elif User.objects.filter(phone_no=phone).exists():
                messages.info(request, "Phone number already taken")
                return redirect('/signup')
            else:
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone, role=role)
                user.set_password(password)
                user.save()

                # Create a user profile associated with the registered user
                user_profile = UserProfile(user=user)
                user_profile.save()

                messages.info(request, "Registered")
                return redirect('login')

    return render(request, 'signup.html')


def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
   
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_no = request.POST.get('phone_no')
        #user.password = request.POST.get('password')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the old password is correct
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Update session to prevent logout
        elif new_password:
            messages.error(request, "Passwords do not match")

        user.save()
        

        # Update user profile fields
        new_profile_pic = request.FILES.get('profile_pic')
        if new_profile_pic:
            user_profile.profile = new_profile_pic
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.pin_code = request.POST.get('pin_code')
        user_profile.save()

        return redirect('profile') 
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    
    return render(request, 'profile.html',context)

def logout(request):
     auth.logout(request)
     return redirect('/')


 
