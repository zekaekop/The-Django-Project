from django.urls import path, re_path

from . import views

app_name = "home"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('top_day', views.popular_post_filter_top_day, name='top_day'),
    path('top_month', views.popular_post_filter_top_month, name='top_month'),
    re_path(r'^(?P<id>\d+)/upvote/$', views.upvote_post, name = "upvote_post"),
    re_path(r'^(?P<id>\d+)/delete_home/$', views.post_delete_home, name = "delete_home"),
]