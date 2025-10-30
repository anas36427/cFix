from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import validators
from .models import CustomUser, Complaint, Application

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(validators=[validators.validate_email], widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'college_id', 'phone_number', 'role', 'password1', 'password2')
    

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Invalid College ID or password.",
    }
    username_field = 'college_id'

    username = forms.CharField(label="College ID", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your College ID','autocomplete':'off'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password','autocomplete':'off'}))


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'hall', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of your complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide detailed information about your complaint'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'application_type', 'department']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of your application'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide detailed information about your application'}),
            'application_type': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
