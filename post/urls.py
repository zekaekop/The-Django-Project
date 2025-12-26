from django.urls import re_path, path
from . import views
from .views import ListPosts, PostActions

app_name = "post"

posts = ListPosts()
post_actions = PostActions()

urlpatterns = [
    # Misc
    path("about/", views.Info.about_us, name = "about"),
    path("contact/", views.Info.contact_us, name = "contact"),

    # Posts
    path("index/", posts.list_blog_posts, name = "index"),
    re_path(r'^(?P<id>\d+)/$', posts.list_post_in_detail, name = "detail"), 
    # r'^(?P<id>\d+)/$' doesnt work with path
    path("create/", views.post_create, name = "create"),
    path("create/preview", views.post_create_preview, name = "preview"),

    # Post actions
    re_path(r'^(?P<id>\d+)/update/$', post_actions.post_update, name = "update"),
    re_path(r'^(?P<id>\d+)/delete/$', post_actions.post_delete, name = "delete"),
    re_path(r'^(?P<id>\d+)/report/$', post_actions.post_report, name = "report"),

    re_path(r'^(?P<id>\d+)/upvote/$', post_actions.upvote_in_blog, name = "upvote_post"),
    re_path(r'^(?P<id>\d+)/upvote/detail/$', post_actions.upvote_in_detail, name = "upvote_post_detail"),

    # Web
    re_path(r'^(?P<id>\d+)/web/$', posts.render_web_view, name = "web"), 
]
