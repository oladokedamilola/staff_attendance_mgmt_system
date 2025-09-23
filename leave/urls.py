# leave/urls.py
from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path("apply/", views.apply_leave, name="apply_leave"),
    path("manage/", views.manage_leave, name="manage_leave"),
    path("report/", views.leave_report, name="leave_report"),
]
