from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    registration_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    pending_address = models.TextField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    admin_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = str(uuid.uuid4())[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.registration_number})"


class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('phone_verification', 'Phone Verification')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.purpose}"


class Report(models.Model):
    REPORT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report by {self.user.username} on {self.report_date}"