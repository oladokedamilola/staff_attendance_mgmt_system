# attendance/urls.py
from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("mark/", views.mark_attendance, name="mark_attendance"),
    path("manage/", views.manage_attendance, name="manage_attendance"),
    path("report/", views.attendance_report, name="attendance_report"),
]
