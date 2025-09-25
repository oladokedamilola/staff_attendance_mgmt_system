from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from attendance.models import Attendance
from leave.models import Leave
from .forms import StaffProfileForm


@login_required
def staff_dashboard(request):
    """Staff dashboard showing attendance & leave summaries."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    # Attendance summary
    total_attendance = Attendance.objects.filter(staff=request.user).count()
    present_count = Attendance.objects.filter(staff=request.user, status="present").count()
    absent_count = Attendance.objects.filter(staff=request.user, status="absent").count()
    late_count = Attendance.objects.filter(staff=request.user, status="late").count()

    # Leave summary
    total_leaves = Leave.objects.filter(staff=request.user).count()
    approved_leaves = Leave.objects.filter(staff=request.user, status="approved").count()
    pending_leaves = Leave.objects.filter(staff=request.user, status="pending").count()
    rejected_leaves = Leave.objects.filter(staff=request.user, status="rejected").count()

    context = {
        "total_attendance": total_attendance,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "total_leaves": total_leaves,
        "approved_leaves": approved_leaves,
        "pending_leaves": pending_leaves,
        "rejected_leaves": rejected_leaves,
    }
    return render(request, "dashboard/staff_dashboard.html", context)


@login_required
def attendance_history(request):
    """Staff can view their attendance history."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    records = Attendance.objects.filter(staff=request.user).order_by("-date")
    if not records.exists():
        messages.info(request, "No attendance records found yet.")
    return render(request, "staff/attendance_history.html", {"records": records})


@login_required
def apply_leave(request):
    """Staff can apply for leave from their dashboard."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    if request.method == "POST":
        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        Leave.objects.create(
            staff=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
        )
        messages.success(request, "Your leave request has been submitted successfully.")
        return redirect("staff_dashboard")

    return render(request, "staff/apply_leave.html")


@login_required
def my_leave_requests(request):
    """Staff can view their submitted leave requests."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    leaves = Leave.objects.filter(staff=request.user).order_by("-applied_at")
    if not leaves.exists():
        messages.info(request, "You have not submitted any leave requests yet.")
    return render(request, "staff/my_leave_requests.html", {"leaves": leaves})


