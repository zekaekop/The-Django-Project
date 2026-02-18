from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.CharField(max_length=400, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True ,null=True)
    user_age = models.IntegerField(null=True, blank=True)

    generated_pic = models.JSONField(default=list, blank=True, null=True,)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    