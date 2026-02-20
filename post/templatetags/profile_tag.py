from django import template
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.views import create_user_profile

register = template.Library()

@register.inclusion_tag('profile_templates/generated_profile_pic.html')
def render_profile(user_or_profile=None):
    context = {}
    
    if user_or_profile:
        if isinstance(user_or_profile, User):
            # Get profile from user
            try:
                context['profile'] = UserProfile.objects.get(user=user_or_profile)
            except UserProfile.DoesNotExist:
                context['profile'] = create_user_profile(user_or_profile, user_or_profile)
        else:
            # Assume it's already a profile object
            context['profile'] = user_or_profile
    
    return context