from django.shortcuts import render, redirect
from user_profile.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from accounts.views import create_user_profile

# Create your views here.

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

class ListProfilePage():

    def profile(self, request, username):

        user = User.objects.get(username=username)

        try:
            user_profile = UserProfile.objects.get(user=user) # if it doesnt exist than create it, support for older accounts that dont have this
        except UserProfile.DoesNotExist:
            user_profile = create_user_profile(user, user) 

        # profile = ProfileAssembly.profile_update(request)

        context = {
            "user": user,
            "profile":user_profile,
        }

        return render(request, "profile_templates/profile.html", context)

    def change_credentials(self, request):
        if request.user.is_authenticated:
            name = {"name" : request.user.username}
            user_instance = request.user
        else:
            name = {"name" : "Guest",}


        user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=user_instance) 
            
        if user_form.is_valid():
            user = user_form.save(commit=False)

            new_password = user_form.cleaned_data.get("password")
            confirm = user_form.cleaned_data.get("confirm_password")

            if new_password and confirm and new_password == confirm:
                user.set_password(new_password)

            user.save()

            return redirect("/accounts/login")
        
        context = {
            "account": name,
            "user_form" : user_form,
        }
        
        return render(request, "profile_templates/change_credentials.html", context)

class ProfileEdit():

    def profile_update(self, request, username):
        user = User.objects.get(username=username)
        authenticate_users(request)

        try:
            userprofile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            userprofile = None

        context = {
            "user": user,
            "userprofile":userprofile,
        }

        if request.method == "POST":

            POST_data = self.get_profile_POST_data(request)
            profile = self.apply_profile_POST_data(request, POST_data, user)

            profile.user = request.user
            profile.save()
            return render(request, "profile_templates/profile_edit.html",context)

        return render(request, "profile_templates/profile_edit.html",context)
        
    def get_profile_POST_data(self, request): 
            return { # apperantly its better to do it with a dict instead of a class
                'bio': request.POST.get("bio"),
                'location': request.POST.get("location"),
                'user_age': request.POST.get("user_age"),
                'gender': request.POST.get("gender"),
                'image': request.FILES.get("image"),
            }
    
    def apply_profile_POST_data(self, request, POST_data, user):
        # POST_data is now a dictionary
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': POST_data.get('bio', ''),
                'location': POST_data.get('location', ''),
                'user_age': POST_data.get('user_age'),
                'gender': POST_data.get('gender'),
            }
        )
        
        # If profile already existed, update its fields
        if not created:
            # Only update if the field is provided in POST_dataz
            if POST_data.get('bio') is not None:
                profile.bio = POST_data['bio']
            if POST_data.get('location') is not None:
                profile.location = POST_data['location']
            if POST_data.get('user_age') is not None:
                profile.user_age = POST_data['user_age']
            if POST_data.get('gender') is not None:
                profile.gender = POST_data['gender']
        
        # Handle image separately
        if POST_data.get('image'):
            profile.image = POST_data['image']

        if POST_data.get('user_age') == '':
            profile.user_age = None

        return profile