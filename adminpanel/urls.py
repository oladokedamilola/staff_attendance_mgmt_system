# adminpanel/urls.py
from django.urls import path
from . import views

# app_name = "adminpanel"

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff/manage/", views.manage_staff, name="manage_staff"),
    path("staff/edit/<int:staff_id>/", views.edit_staff, name="edit_staff"),
    path("leave-requests/", views.leave_requests, name="leave_requests"),
    path("attendance-reports/", views.attendance_reports, name="attendance_reports"),
    path("send-invite/", views.send_staff_invite, name="send_staff_invite"),
]
