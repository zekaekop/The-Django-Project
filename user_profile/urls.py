from django.urls import path

from .views import ListProfilePage, ProfileEdit

app_name = "user_profile"

list_profile = ListProfilePage() 
edit_profile = ProfileEdit() 

# apperantly the urlpattern scans through the list in order meaning the ordering needs attention

urlpatterns = [
    path('credentials/', list_profile.change_credentials , name="change_credentials"),
    path('<str:username>/edit_profile/', edit_profile.profile_update , name="profile_edit"),
    
    path('<str:username>/accept_friendship_req', list_profile.accept_friend_request , name="accept_friend_req"),
    path('<str:username>/reject_friendship_req', list_profile.reject_friend_request , name="reject_friend_req"),
    path('<str:username>/request_friend', list_profile.request_friend , name="friend_req"),
    path('<str:username>/remove_friend', list_profile.remove_friend , name="remove_friend"),

    path('<str:username>/', list_profile.profile , name="profile"),
]