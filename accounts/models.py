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
    
# Handles the model friendship relation system
# a friendship can be sent and it will be pending
# friendship invites can be declined or accepted

# Source - https://stackoverflow.com/a/52915586
# Posted by Hugo Trentesaux
# Retrieved 2026-02-18, License - CC BY-SA 4.0

class Friend(models.Model):
    to_user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name='_unused_friend_relation')

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_received')
