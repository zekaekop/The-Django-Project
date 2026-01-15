from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    
    GENDER_CHOICES = (
        ('other', 'Other'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    user_age = models.IntegerField(null=True, blank=True)

    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    