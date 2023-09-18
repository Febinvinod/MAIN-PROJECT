from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login ,authenticate,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib  import messages,auth
from .models import CustomUser
from courseprovider.models import Courseprovider_profile
User = get_user_model()


# Create your views here.
def index(request):
    return render(request,'index.html',{'user':request.user})
# def loginn(request):
#      if request.method =='POST':
#          username=request.POST.get('uname')
#          password=request.POST.get('pwd')
#          user=authenticate(request,username=username,password=password)
#          if user is not None:
#               login(request,user)
#               return redirect('index')
#          else:
#               messages.info(request,"Invalid User")
#               return redirect('login')
#      else:
#       return render(request,'login.html')

# def signup(request):
#     if request.method =='POST':
#         username=request.POST.get('uname')
#         email=request.POST.get('email')
#         password=request.POST.get('pwd')
#         Cpassword=request.POST.get('cpwd')

#         if password==Cpassword:
#              if User.objects.filter(username=username).exists():  
#                     messages.info(request,"Username already taken")
#                     return redirect('/signup')
             
#              elif User.objects.filter(email=email).exists():     
#                     messages.info(request,"Email already taken")  
#                     return redirect('/signup')
         
#              else:
#                   user_reg=User.objects.create_user(username=username,email=email,password=password)                
#                   user_reg.save()
#                   messages.info(request,"Registered") 
#                   return redirect('login')
#         else:
#               return redirect('/signup')
#     else:
#           return render(request,'signup.html')
def login(request):
    if request.method == 'POST':
     #     captcha_token = request.POST.get("g-recaptcha-response")
     #     cap_url = "https://www.google.com/recaptcha/api/siteverify"
     #     cap_secret = "6LcJj44nAAAAADDjTqz0n5e7UM5HRFzMtC54swC3"
     #     cap_data = {"secret": cap_secret, "response": captcha_token}
         
         
     #     cap_server_response = requests.post(url=cap_url, data=cap_data)
     #     cap_json = json.loads(cap_server_response.text)
         
     #     if not cap_json['success']:
     #          error_message = "Captcha validation failed. Please try again."
     #          return render(request, 'login.html', {'error_message': error_message})
         
         
         username = request.POST.get('username')
         password = request.POST.get('password')

         if username  and password:
              user = authenticate(request, username=username, password=password)
              if user is not None:
                   auth_login(request, user)
                   return redirect('/')
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
                 messages.info(request,"Username already taken")
                 return redirect('/signup')
                # error_message = "Username is already registered."
                # return render(request, 'signup.html', {'error_message': error_message})
            elif User.objects.filter(email=email).exists():
                 messages.info(request,"Email already taken")  
                 return redirect('/signup')
                # error_message = "Email is already registered."
                # return render(request, 'signup.html', {'error_message': error_message})
            elif User.objects.filter(phone_no=phone).exists():
                messages.info(request,"Phone number already taken")  
                return redirect('/signup')

            else:
                user = User(username=username,first_name=first_name,last_name=last_name, email=email, phone_no=phone,role=role)
                user.set_password(password)  # Set the password securely
                user.save()
                Courseprovider_profile = Courseprovider_profile(user=user)
                user.save()
                messages.info(request,"Registered")
                return redirect('login')  
            
    return render(request, 'signup.html')  

def profile(request):
    return render(request,'profile.html')

def logout(request):
     auth.logout(request)
     return redirect('/')


 
