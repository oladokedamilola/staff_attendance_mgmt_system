# attendance/views.py
from datetime import date
import csv

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Attendance


@login_required
def mark_attendance(request):
    """Allow staff to mark their own attendance."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    today = date.today()
    attendance, _ = Attendance.objects.get_or_create(staff=request.user, date=today)

    if request.method == "POST":
        attendance.status = request.POST.get("status", "present")
        attendance.save()
        messages.success(request, f"Attendance marked as {attendance.status}")
        return redirect("staff_dashboard")

    return render(request, "attendance/mark_attendance.html", {"attendance": attendance})


@login_required
def manage_attendance(request):
    """Admins can view/manage attendance records."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    records = Attendance.objects.all().order_by("-date")
    return render(request, "attendance/manage_attendance.html", {"records": records})


@login_required
def attendance_report(request):
    """Admins can view or export attendance reports."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    records = Attendance.objects.all().order_by("staff", "-date")

    # CSV export
    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="attendance_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Staff", "Date", "Status"])
        for r in records:
            writer.writerow([r.staff.username, r.date, r.status])

        return response

    return render(request, "attendance/attendance_report.html", {"records": records})
