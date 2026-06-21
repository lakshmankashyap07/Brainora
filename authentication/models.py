from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
from datetime import timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Admin'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    
    # Required/Custom fields
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # College details
    college = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    semester = models.IntegerField(default=1, blank=True, null=True)
    college_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Personal details
    phone_contact = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Roles & verification
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    is_verified = models.BooleanField(default=False)
    
    # OTP verification
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    
    # Lockout safety & 2FA security
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_otp(self):
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_expiry = timezone.now() + timedelta(minutes=10)
        self.save()
        return self.otp

    def is_otp_valid(self, code):
        if self.otp == code and self.otp_expiry and self.otp_expiry > timezone.now():
            return True
        return False

    def clear_otp(self):
        self.otp = None
        self.otp_expiry = None
        self.save()

    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lockout_until = timezone.now() + timedelta(minutes=15)
        self.save()

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.lockout_until = None
        self.save()

    def is_locked_out(self):
        if self.lockout_until and self.lockout_until > timezone.now():
            return True
        return False

    def __str__(self):
        return f"{self.username} ({self.role})"


class LoginHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='login_histories')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    login_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-login_time']
        verbose_name_plural = "Login Histories"

    def __str__(self):
        return f"{self.user.username} logged in from {self.ip_address} on {self.login_time}"
