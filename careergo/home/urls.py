
from django.urls import path,include
from.import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path("accounts/", include("allauth.urls")),
    path('profile',views.profile,name='profile'),
    path('adminpage',views.adminpage,name='adminpage'),
    path('providerpage',views.providerpage,name='providerpage'),
    # path('coursedetail',views.coursedetail,name='coursedetail'),
 

     path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
