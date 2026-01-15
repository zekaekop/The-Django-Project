from django.shortcuts import render, redirect
from user_profile.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib.auth.models import User

# Create your views here.

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

class ListProfilePage():

    def profile(self, request, username):
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
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

        if request.method == "POST":

            POST_data = self.get_profile_POST_data(request)
            profile = self.apply_profile_POST_data(request, POST_data)

            profile.save()
            return render(request, "profile_templates/profile_edit.html",context)

        context = {
            "user": user,
            "userprofile":UserProfile,
        }

        return render(request, "profile_templates/profile_edit.html",context)
    
    def get_profile_POST_data(self, request, username): 

        class POST_data:

            bio = request.POST.get("bio")
            location = request.POST.get("location")
            user_Age = request.POST.get("user_age")
            gender = request.POST.get("gender")
            profile_pic = request.FILES.get("profile_pic")

        return POST_data
    
    def apply_profile_POST_data(self, request, POST_data, username):

        profile = Profile(
            bio= POST_data.bio,
            location= POST_data.location,
            user_Age= POST_data.user_Age,
            gender = request.POST.get("gender"),
            profile_pic= POST_data.profile_pic,
            )

        return profile
