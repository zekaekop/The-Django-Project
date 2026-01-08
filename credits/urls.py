from django.urls import path
from . import views

app_name = "credits"

urlpatterns = [
    path("thank-you", views.thanks, name = "thanks"),
]