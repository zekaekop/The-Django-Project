from django.urls import  path
from . import views

app_name = "info"

urlpatterns = [
    path("about/", views.Info.about_us, name = "about"),
    path("contact/", views.Info.contact_us, name = "contact"),
]
