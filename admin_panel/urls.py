from django.urls import path, re_path

from . import views

app_name = "admin_panel"

urlpatterns = [
    # Admin panel contact & post
    re_path(r'^(?P<id>\d+)/delete_post_adminpanel/$', views.delete_post_adminpanel, name = "delete_post_adminpanel"),
    re_path(r'^(?P<id>\d+)/delete_contact_adminpanel/$', views.delete_contact_adminpanel, name = "delete_contact_adminpanel"),
    re_path(r'^(?P<id>\d+)/modify_contact_adminpanel/$', views.modify_contact_adminpanel, name = "modify_contact_adminpanel"),

    # Displays Admin Panel Category Information
    path("category/", views.admin_panel_posts, name = "admin_panel"), # this is default admin panel function but since there is no authentication it will just go to post
    path("category/users", views.admin_panel_users, name = "admin_panel_users"),
    path("category/posts", views.admin_panel_posts, name = "admin_panel_posts"),
    path("category/contacts", views.admin_panel_contact, name = "admin_panel_contact"),
    path("category/achivements", views.admin_panel_achivements, name = "admin_panel_achivements"),

    # Admin Panel User Action logic
    re_path(r'^(?P<id>\d+)/active_state_user_account/$', views.active_state_user_account, name = "active_state_user_account"),
    re_path(r'^(?P<id>\d+)/password_change_user_account/$', views.password_change_user_account, name = "password_change_user_account"),
    re_path(r'^(?P<id>\d+)/set_user_perms_staff_adminpanel/$', views.set_user_perms_staff_adminpanel, name = "set_user_perms_staff_adminpanel"),
    re_path(r'^(?P<id>\d+)/set_user_perms_superuser_adminpanel/$', views.set_user_perms_superuser_adminpanel, name = "set_user_perms_superuser_adminpanel"),
]