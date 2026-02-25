"""
URL configuration for testing_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home'
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('feed/', include('feed.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from home.views import home_view
from home.views import upvote_post

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('post/', include('post.urls')),
    
    path('accounts/', include('accounts.urls')),
    path('profile/', include('user_profile.urls')),
    path('procedural_pfp', include("procedural_pfp.urls")),
    path("friendship/", include("friendship.urls")),

    path('admin_panel/', include('admin_panel.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    
    path('info/', include('info.urls')),
    path('secret/', include('secret.urls')),
    path('', include('credits.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)