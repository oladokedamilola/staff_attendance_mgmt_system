# staff/urls.py
from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path("dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("attendance-history/", views.attendance_history, name="attendance_history"),
    path("apply-leave/", views.apply_leave, name="apply_leave"),
    path("my-leave-requests/", views.my_leave_requests, name="my_leave_requests"),
    path("profile/", views.profile, name="profile"),
]
