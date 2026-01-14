from django.shortcuts import render, redirect
from user_profile.forms import UserProfileForm
# Create your views here.

class ListProfilePage():

    def profile(self, request):
        return render(request, "profile_templates/profile.html")

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
            "title":"Hello world",
            "account": name,
            "user_form" : user_form,
        }
        
        return render(request, "profile_templates/change_credentials.html", context)
