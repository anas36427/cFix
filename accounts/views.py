from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import random
from .forms import CustomUserCreationForm
from .decorators import role_required

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = True
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id')
        password = request.POST.get('password')

        user = authenticate(request, college_id=college_id, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.role.title()}!")

            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'staff':
                return redirect('staff_dashboard')
            elif user.role == 'provost':
                return redirect('provost_dashboard')
            elif user.role == 'dsw':
                return redirect('dsw_dashboard')
            elif user.role == 'exam_controller':
                return redirect('exam_dashboard')
            elif user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')



@login_required
@role_required(['student'])
def student_dashboard(request):
    return render(request, 'dashboard/student.html')

@login_required
@role_required(['staff'])
def staff_dashboard(request):
    return render(request, 'dashboard/staff.html')

@login_required
@role_required(['provost'])
def provost_dashboard(request):
    return render(request, 'dashboard/provost.html')

@login_required
@role_required(['dsw'])
def dsw_dashboard(request):
    return render(request, 'dashboard/dsw.html')

@login_required
@role_required(['exam_controller'])
def exam_dashboard(request):
    return render(request, 'dashboard/exam.html')
