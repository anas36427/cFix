

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import random
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ComplaintForm, ApplicationForm
from .decorators import role_required
from .models import Complaint, Application, Notification

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
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
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
            pass  # Let the form handle the error message
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')



@login_required
@role_required(['student'])
def student_dashboard(request):
    notifications = request.user.notifications.filter(is_read=False)[:5]  # Get latest 5 unread notifications
    context = {
        'notifications': notifications,
        'unread_count': request.user.notifications.filter(is_read=False).count(),
    }
    return render(request, 'dashboard/student.html', context)

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


@login_required
@role_required(['student'])
@csrf_exempt
@require_POST
def submit_complaint(request):
    """Handle AJAX complaint submission"""
    try:
        data = json.loads(request.body)
        form = ComplaintForm(data)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()

            return JsonResponse({
                'success': True,
                'message': 'Complaint submitted successfully!',
                'complaint_id': complaint.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while submitting your complaint.'
        })


@login_required
@role_required(['student'])
@csrf_exempt
@require_POST
def submit_application(request):
    """Handle AJAX application submission"""
    try:
        data = json.loads(request.body)
        form = ApplicationForm(data)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()

            return JsonResponse({
                'success': True,
                'message': 'Application submitted successfully!',
                'application_id': application.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while submitting your application.'
        })


@login_required
@role_required(['student'])
def my_complaints(request):
    """Return JSON data for student's complaints"""
    complaints = Complaint.objects.filter(student=request.user).values(
        'id', 'title', 'description', 'category', 'hall', 'priority',
        'status', 'created_at', 'updated_at'
    )

    # Format data for frontend
    complaints_data = []
    for complaint in complaints:
        complaints_data.append({
            'id': f'C{complaint["id"]:03d}',  # Format as C001, C002, etc.
            'title': complaint['title'],
            'description': complaint['description'],
            'category': complaint['category'].replace('-', ' ').title(),
            'hall': complaint['hall'].replace('-', ' ').title(),
            'priority': complaint['priority'].title(),
            'status': complaint['status'],
            'date': complaint['created_at'].strftime('%Y-%m-%d'),
            'updated_at': complaint['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({
        'success': True,
        'complaints': complaints_data
    })


@login_required
@role_required(['student'])
def my_applications(request):
    """Return JSON data for student's applications"""
    applications = Application.objects.filter(student=request.user).values(
        'id', 'title', 'description', 'application_type', 'department',
        'status', 'created_at', 'updated_at'
    )

    # Format data for frontend
    applications_data = []
    for application in applications:
        applications_data.append({
            'id': f'A{application["id"]:03d}',  # Format as A001, A002, etc.
            'title': application['title'],
            'description': application['description'],
            'category': application['application_type'].replace('-', ' ').title(),
            'department': application['department'].replace('-', ' ').title(),
            'status': application['status'],
            'date': application['created_at'].strftime('%Y-%m-%d'),
            'updated_at': application['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({
        'success': True,
        'applications': applications_data
    })


@login_required
@role_required(['staff', 'provost', 'dsw', 'exam_controller'])
def all_complaints(request):
    """Return JSON data for complaints based on user role"""
    user_role = request.user.role

    # Filter complaints based on user role
    if user_role == 'staff':
        complaints = Complaint.objects.filter(department='staff').select_related('student')
    elif user_role == 'provost':
        complaints = Complaint.objects.filter(department='provost').select_related('student')
    elif user_role == 'dsw':
        complaints = Complaint.objects.filter(department='dsw').select_related('student')
    elif user_role == 'exam_controller':
        complaints = Complaint.objects.filter(department='exam_controller').select_related('student')
    else:
        # Fallback for any other admin roles
        complaints = Complaint.objects.all().select_related('student')

    complaints_data = complaints.values(
        'id', 'title', 'description', 'category', 'department', 'hall', 'priority',
        'status', 'created_at', 'updated_at', 'student__first_name',
        'student__last_name', 'student__college_id'
    )

    # Format data for frontend
    complaints_data = []
    for complaint in complaints_data:
        complaints_data.append({
            'id': f'C{complaint["id"]:03d}',
            'title': complaint['title'],
            'description': complaint['description'],
            'category': complaint['category'].replace('-', ' ').title(),
            'department': complaint['department'].replace('_', ' ').title(),
            'hall': complaint['hall'].replace('-', ' ').title(),
            'priority': complaint['priority'].title(),
            'status': complaint['status'],
            'student_name': f"{complaint['student__first_name']} {complaint['student__last_name']}",
            'student_id': complaint['student__college_id'],
            'date': complaint['created_at'].strftime('%Y-%m-%d'),
            'updated_at': complaint['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({
        'success': True,
        'complaints': complaints_data
    })


@login_required
@role_required(['staff', 'provost', 'dsw', 'exam_controller'])
def api_all_complaints(request):
    """API endpoint for all complaints (admin/staff roles)"""
    return all_complaints(request)


@login_required
@role_required(['staff', 'provost', 'dsw', 'exam_controller'])
@require_POST
def update_complaint_status(request):
    """Update complaint status (admin/staff roles)"""
    try:
        data = json.loads(request.body)
        complaint_id = data.get('complaint_id')
        new_status = data.get('status')

        if not complaint_id or not new_status:
            return JsonResponse({
                'success': False,
                'message': 'Complaint ID and status are required.'
            })

        # Remove 'C' prefix if present
        if isinstance(complaint_id, str) and complaint_id.startswith('C'):
            complaint_id = int(complaint_id[1:])

        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = new_status
        complaint.save()

        return JsonResponse({
            'success': True,
            'message': 'Complaint status updated successfully.',
            'complaint_id': f'C{complaint.id:03d}',
            'new_status': new_status
        })

    except Complaint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Complaint not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while updating the complaint status.'
        })


@login_required
def complaint_details(request, complaint_id):
    """Return detailed information for a specific complaint"""
    try:
        # Remove 'C' prefix if present
        if isinstance(complaint_id, str) and complaint_id.startswith('C'):
            complaint_id = int(complaint_id[1:])

        complaint = Complaint.objects.select_related('student').get(id=complaint_id)

        # Check permissions: students can only view their own complaints
        if request.user.role == 'student' and complaint.student != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You do not have permission to view this complaint.'
            })

        complaint_data = {
            'id': f'C{complaint.id:03d}',
            'title': complaint.title,
            'description': complaint.description,
            'category': complaint.category.replace('-', ' ').title(),
            'department': complaint.department.replace('_', ' ').title(),
            'hall': complaint.hall.replace('-', ' ').title(),
            'priority': complaint.priority.title(),
            'status': complaint.status,
            'student_name': f"{complaint.student.first_name} {complaint.student.last_name}",
            'student_id': complaint.student.college_id,
            'date': complaint.created_at.strftime('%Y-%m-%d'),
            'updated_at': complaint.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({
            'success': True,
            'complaint': complaint_data
        })

    except Complaint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Complaint not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while retrieving complaint details.'
        })


@login_required
def application_details(request, application_id):
    """Return detailed information for a specific application"""
    try:
        # Remove 'A' prefix if present
        if isinstance(application_id, str) and application_id.startswith('A'):
            application_id = int(application_id[1:])

        application = Application.objects.select_related('student').get(id=application_id)

        # Check permissions: students can only view their own applications
        if request.user.role == 'student' and application.student != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You do not have permission to view this application.'
            })

        application_data = {
            'id': f'A{application.id:03d}',
            'title': application.title,
            'description': application.description,
            'application_type': application.application_type.replace('-', ' ').title(),
            'department': application.department.replace('_', ' ').title(),
            'status': application.status,
            'student_name': f"{application.student.first_name} {application.student.last_name}",
            'student_id': application.student.college_id,
            'date': application.created_at.strftime('%Y-%m-%d'),
            'updated_at': application.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({
            'success': True,
            'application': application_data
        })

    except Application.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Application not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while retrieving application details.'
        })


@login_required
@role_required(['student'])
@require_POST
def delete_complaint(request):
    """Delete a pending complaint (students only)"""
    try:
        data = json.loads(request.body)
        complaint_id = data.get('complaint_id')

        if not complaint_id:
            return JsonResponse({
                'success': False,
                'message': 'Complaint ID is required.'
            })

        # Remove 'C' prefix if present
        if isinstance(complaint_id, str) and complaint_id.startswith('C'):
            complaint_id = int(complaint_id[1:])

        complaint = Complaint.objects.get(id=complaint_id)

        # Check if complaint belongs to the user and is pending
        if complaint.student != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You can only delete your own complaints.'
            })

        if complaint.status != 'pending':
            return JsonResponse({
                'success': False,
                'message': 'You can only delete pending complaints.'
            })

        complaint.delete()

        return JsonResponse({
            'success': True,
            'message': 'Complaint deleted successfully.'
        })

    except Complaint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Complaint not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while deleting the complaint.'
        })


@login_required
@role_required(['student'])
@require_POST
def delete_application(request):
    """Delete a pending application (students only)"""
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')

        if not application_id:
            return JsonResponse({
                'success': False,
                'message': 'Application ID is required.'
            })

        # Remove 'A' prefix if present
        if isinstance(application_id, str) and application_id.startswith('A'):
            application_id = int(application_id[1:])

        application = Application.objects.get(id=application_id)

        # Check if application belongs to the user and is pending
        if application.student != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You can only delete your own applications.'
            })

        if application.status != 'pending':
            return JsonResponse({
                'success': False,
                'message': 'You can only delete pending applications.'
            })

        application.delete()

        return JsonResponse({
            'success': True,
            'message': 'Application deleted successfully.'
        })

    except Application.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Application not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while deleting the application.'
        })
