from django.urls import path

from .views import ListProfilePage

app_name = "user_profile"

list_profile = ListProfilePage() 

urlpatterns = [
    path('credentials/', list_profile.change_credentials , name="change_credentials"),
    path('<str:username>/', list_profile.profile , name="profile"),
]