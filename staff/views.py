from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from attendance.models import Attendance
from leave.models import Leave

from datetime import date
from django.utils.timezone import now

@login_required
def staff_dashboard(request):
    """Staff dashboard showing attendance & leave summaries."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    today = date.today()
    records = Attendance.objects.filter(staff=request.user)

    # Attendance summary
    total_attendance = records.count()
    present_count = records.filter(status="present").count()
    absent_count = records.filter(status="absent").count()
    late_count = records.filter(status="late").count()

    # Monthly stats
    this_month = now().month
    this_year = now().year
    month_records = records.filter(date__month=this_month, date__year=this_year)
    days_present = month_records.filter(status="present").count()
    total_days = month_records.count()
    attendance_percentage = round((days_present / total_days) * 100, 1) if total_days > 0 else 0

    # Leave summary
    total_leaves = Leave.objects.filter(staff=request.user).count()
    approved_leaves = Leave.objects.filter(staff=request.user, status="approved").count()
    pending_leaves = Leave.objects.filter(staff=request.user, status="pending").count()
    rejected_leaves = Leave.objects.filter(staff=request.user, status="rejected").count()

    # Check if today is already marked
    today_record = records.filter(date=today).first()

    # Recent activity
    recent_attendance = records.order_by("-date")[:5]

    context = {
        "total_attendance": total_attendance,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "days_present": days_present,
        "total_days": total_days,
        "attendance_percentage": attendance_percentage,
        "total_leaves": total_leaves,
        "approved_leaves": approved_leaves,
        "pending_leaves": pending_leaves,
        "rejected_leaves": rejected_leaves,
        "recent_attendance": recent_attendance,
        "today_record": today_record,
    }
    return render(request, "dashboard/staff_dashboard.html", context)



@login_required
def attendance_history(request):
    """Staff can view their attendance history with summary counts."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    records = Attendance.objects.filter(staff=request.user).order_by("-date")

    # Summary counts
    present_count = records.filter(status="present").count()
    late_count = records.filter(status="late").count()
    absent_count = records.filter(status="absent").count()

    if not records.exists():
        messages.info(request, "No attendance records found yet.")

    context = {
        "records": records,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
    }
    return render(request, "staff/attendance_history.html", context)



@login_required
def my_leave_requests(request):
    """Staff can view their submitted leave requests with summary counts."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    leaves = Leave.objects.filter(staff=request.user).order_by("-applied_at")

    # Pre-calculate counts
    total_requests = leaves.count()
    approved_count = leaves.filter(status="approved").count()
    pending_count = leaves.filter(status="pending").count()
    rejected_count = leaves.filter(status="rejected").count()

    if not leaves.exists():
        messages.info(request, "You have not submitted any leave requests yet.")

    context = {
        "leaves": leaves,
        "total_requests": total_requests,
        "approved_count": approved_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
    }
    return render(request, "leave/my_leave_requests.html", context)


