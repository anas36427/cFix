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
]

