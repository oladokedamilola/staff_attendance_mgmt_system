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
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    today = date.today()
    attendance, _ = Attendance.objects.get_or_create(staff=request.user, date=today)

    if request.method == "POST":
        status = request.POST.get("status", "present")
        attendance.status = status
        attendance.save()
        messages.success(request, f"Your attendance for today has been marked as '{attendance.status}'.")
        return redirect("staff_dashboard")
    else:
        if attendance.status:
            messages.info(request, f"Today's attendance already marked as '{attendance.status}'. You can update it if needed.")

    return render(request, "attendance/mark_attendance.html", {"attendance": attendance})


@login_required
def manage_attendance(request):
    """Admins can view/manage attendance records."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("login")

    records = Attendance.objects.all().order_by("-date")

    if not records.exists():
        messages.info(request, "No attendance records available yet.")

    return render(request, "attendance/manage_attendance.html", {"records": records})


@login_required
def attendance_report(request):
    """Admins can view or export attendance reports."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("login")

    records = Attendance.objects.all().order_by("staff", "-date")

    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="attendance_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Staff", "Date", "Status"])
        for r in records:
            writer.writerow([r.staff.username, r.date, r.status])

        messages.success(request, "Attendance report exported successfully as CSV.")
        return response

    if not records.exists():
        messages.warning(request, "No attendance records found to display.")

    return render(request, "attendance/attendance_report.html", {"records": records})
