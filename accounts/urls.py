# accounts/urls.py
from django.urls import path
from . import views

# app_name = "accounts"

urlpatterns = [
    path("register/<str:token>/", views.staff_register, name="staff_register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # 🔄 Password Reset
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("reset-password/<str:token>/", views.password_reset_confirm, name="password_reset_confirm"),

    
    path("profile/", views.profile_view, name="profile"),

]
