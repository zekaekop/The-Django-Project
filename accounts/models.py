from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRegularMailAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    account_age = models.DateTimeField(verbose_name="Date/Time ", auto_now_add=True)

    select_gender = (
        ('Other', 'Other'),
        ('Male', 'Male'),
        ('Female', 'Female'),)
    
    gender = models.CharField(max_length=8, choices=select_gender, default="other")

    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)

class UserModerator(models.Model):
    pass

class UserAdmin(models.Model):
    pass