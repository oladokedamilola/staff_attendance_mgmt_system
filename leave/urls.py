# leave/urls.py
from django.urls import path
from . import views

# app_name = "leave"

urlpatterns = [
    path("apply/", views.apply_leave, name="apply_leave"),
    path("report/", views.leave_report, name="leave_report"),
    path("report/export/<str:export_format>/", views.leave_export, name="leave_export"),

]