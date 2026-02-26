from django.db import models
from django.contrib.auth.models import User

# Create your models here.

AUTH_USER_MODEL = 'accounts.UserProfile'

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    bio = models.CharField(max_length=400, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True ,null=True)
    user_age = models.PositiveSmallIntegerField(null=True, blank=True)

    generated_pic = models.JSONField(default=list, blank=True, null=True,)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    profile_views = models.PositiveIntegerField(null=True, default = 0)
    post_count = models.PositiveIntegerField(null=True, default = 0)

    BZ = models.PositiveIntegerField(null=False, default = 150) # possible virtual currency for cosmetics??
    
    # a bunch more statistics could be added but i will leave it simple for now

class Achievement(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievement_icons/', null=True, blank=True)

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

# Handles the model friendship relation system
# a friendship can be sent and it will be pending
# friendship invites can be declined or accepted

# Source - https://stackoverflow.com/a/52915586
# Posted by Hugo Trentesaux
# Retrieved 2026-02-18, License - CC BY-SA 4.0