from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('mod', 'Moderator'),
        ('admin', 'Administrator'),
    )
    
    GENDER_CHOICES = (
        ('other', 'Other'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    bio = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    