from django.urls import path
from . import views

urlpatterns = [
    path('credits/', views.credits, name='credits'),
]
