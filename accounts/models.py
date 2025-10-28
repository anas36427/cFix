from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, college_id, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        if not college_id:
            raise ValueError('The College ID field is required')

        email = self.normalize_email(email)
        user = self.model(email=email, college_id=college_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, college_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, college_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('provost', 'Provost'),
        ('dsw', 'DSW'),
        ('exam_controller', 'Exam Controller'),
    ]
    email = models.EmailField(unique=True)
    college_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=15, default='')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['college_id']
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.college_id})"


class Complaint(models.Model):
    DEPARTMENT_CHOICES = [
        ('staff', 'Staff/General'),
        ('provost', 'Provost/Hall Management'),
        ('dsw', 'DSW/Student Welfare'),
        ('exam_controller', 'Exam Controller'),
    ]

    CATEGORY_CHOICES = [
        ('infrastructure', 'Infrastructure'),
        ('food', 'Food Services'),
        ('maintenance', 'Maintenance'),
        ('security', 'Security'),
        ('other', 'Other'),
    ]

    HALL_CHOICES = [
        # Boys Halls
        ('aftab', 'Aftab Hall'),
        ('ambedkar', 'Dr. B.R. Ambedkar Hall'),
        ('hadi-hasan', 'Hadi Hasan Hall'),
        ('mohsinul-mulk', 'Mohsinul Mulk Hall'),
        ('mohd-habib', 'Mohd. Habib Hall'),
        ('nadeem-tarin', 'Nadeem Tarin Hall'),
        ('ross-masood', 'Ross Masood Hall'),
        ('sir-shah-sulaiman', 'Sir Shah Sulaiman Hall'),
        ('sir-syed-north', 'Sir Syed Hall (North)'),
        ('sir-syed-south', 'Sir Syed Hall (South)'),
        ('sir-ziauddin', 'Sir Ziauddin Hall'),
        ('viqarul-mulk', 'Viqarul Mulk Hall'),
        # Girls Halls
        ('abdullah', 'Abdullah Hall'),
        ('bibi-fatima', 'Bibi Fatima Hall'),
        ('begum-sultan-jahan', 'Begum Sultan Jahan Hall'),
        ('begum-azeezun-nisa', 'Begum Azeezun Nisa Hall'),
        ('indira-gandhi', 'Indira Gandhi Hall'),
        ('sarojini-naidu', 'Sarojini Naidu Hall'),
        # Other
        ('nrsc', 'Non-Resident Students\' Centre (NRSC)'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='staff')
    hall = models.CharField(max_length=50, choices=HALL_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.college_id}"

    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    APPLICATION_TYPES = [
        ('room-change', 'Room Change Request'),
        ('library-subscription', 'Library Subscription'),
        ('exam-revaluation', 'Exam Re-evaluation'),
        ('fee-concession', 'Fee Concession'),
        ('other', 'Other'),
    ]

    DEPARTMENTS = [
        ('dsw', 'Dean of Student Welfare'),
        ('provost', 'Provost/Hall Management'),
        ('library', 'Library'),
        ('examination', 'Examination Controller'),
        ('accounts', 'Accounts'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    verified = models.BooleanField(default=False)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.college_id}"

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('complaint', 'Complaint Update'),
        ('application', 'Application Update'),
        ('system', 'System Notification'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    related_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.student.first_name}"
