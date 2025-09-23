# accounts/urls.py
from django.urls import path
from . import views

# app_name = "accounts"

urlpatterns = [
    path("register/<str:token>/", views.staff_register, name="staff_register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("profile/", views.profile_view, name="profile"),

]
