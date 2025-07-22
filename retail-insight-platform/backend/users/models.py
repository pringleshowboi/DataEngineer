from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('monitor', 'Data Monitor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='monitor')
    full_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.username} ({self.role})'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    assigned_region = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)