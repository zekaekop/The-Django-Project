from django.urls import path

from .views import ListProfilePage, ProfileEdit

app_name = "user_profile"

list_profile = ListProfilePage() 
edit_profile = ProfileEdit() 

urlpatterns = [
    path('credentials/', list_profile.change_credentials , name="change_credentials"),
    path('<str:username>/', list_profile.profile , name="profile"),
    path('<str:username>/edit_profile/', edit_profile.profile_update , name="profile_edit"),
]