from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from home.models import CustomUser


CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name' ,'email', 'phone_no']
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'Enter Name',
                'id':'uname'
            }),
            'first_name': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'first name'
            }),
            'last_name': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'last name'
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Email'
            }),
            'phone_no': forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Phone Number'
            }),
            # 'role': forms.Select(attrs={
            #     "class": "form-control form-control-lg"
            # }),

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        
        if commit:
            user.save()
        return user
    
    
    
    def clean_username(self):
        username = self.cleaned_data['username']

        # Check if a user with this username already exists
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username is already taken.')

        # Add your username length validation logic here
        if len(username) < 4:
            raise ValidationError('Username must be at least 4 characters long.')

        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        # Add your first name validation logic here
        if not all(char.isalpha() or char.isspace() for char in first_name):
            raise ValidationError('First name should only contain alphabetic characters.')
        
        if len(first_name) < 2:
            raise ValidationError('First name must be at least 2 characters long.')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        # Add your last name validation logic here
        if not all(char.isalpha() or char.isspace() for char in last_name):
            raise ValidationError('Last name should only contain alphabetic characters.')
        
        if len(last_name) < 2:
            raise ValidationError('Last name must be at least 2 characters long.')

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']

        # Check if a user with this email address already exists
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email is already taken.')

        # Add your email format validation logic here (e.g., check for a valid format)

        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']

        # Check if a user with this phone number already exists
        if CustomUser.objects.filter(phone_no=phone_no).exists():
            raise ValidationError('Phone number is already taken.')

        # Add your phone number format validation logic here (e.g., check for a valid format)
        if not phone_no.isdigit() or len(phone_no) != 10:
            raise ValidationError('Phone number must be a 10-digit number.')

        return phone_no

    
    
