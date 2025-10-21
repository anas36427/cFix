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
