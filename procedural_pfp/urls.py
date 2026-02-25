from django.urls import path, reverse
from . import views

app_name = "procedural_pfp"

PfpAssembly = views.PfpAssembly()

# apperantly the urlpattern scans through the list in order meaning the ordering needs attention

urlpatterns = [
    path('pfp_regen_debug/', PfpAssembly.pfp_regen_debug , name="pfp_regen_debug"),
    path('pfp_reroll/', PfpAssembly.pfp_reroll , name="pfp_reroll"),
]