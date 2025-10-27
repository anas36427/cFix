from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards for different roles
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    path('dashboard/provost/', views.provost_dashboard, name='provost_dashboard'),
    path('dashboard/dsw/', views.dsw_dashboard, name='dsw_dashboard'),
    path('dashboard/exam/', views.exam_dashboard, name='exam_dashboard'),

    # Complaint system URLs
    path('complaints/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaints/my/', views.my_complaints, name='my_complaints'),
    path('complaints/delete/', views.delete_complaint, name='delete_complaint'),
    path('complaints/all/', views.all_complaints, name='all_complaints'),
    path('complaints/update-status/', views.update_complaint_status, name='update_complaint_status'),
    path('complaints/<int:complaint_id>/', views.complaint_details, name='complaint_details'),

    # Application system URLs
    path('applications/submit/', views.submit_application, name='submit_application'),
    path('applications/my/', views.my_applications, name='my_applications'),
    path('applications/delete/', views.delete_application, name='delete_application'),
    path('applications/<str:application_id>/', views.application_details, name='application_details'),

    # API endpoints
    path('complaints/', views.api_all_complaints, name='api_complaints'),
    path('complaints/<str:complaint_id>/', views.complaint_details, name='api_complaint_details'),
]
