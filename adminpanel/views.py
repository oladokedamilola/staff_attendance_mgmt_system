# adminpanel/views.py
from uuid import uuid4
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from accounts.models import StaffInvitation, User
from attendance.models import Attendance
from leave.models import Leave
from .forms import StaffInvitationForm, StaffForm


@login_required
def send_staff_invite(request):
    """Allow admin to invite staff via email."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    if request.method == "POST":
        form = StaffInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.token = uuid4()
            invitation.save()

            # Send email with token link
            invite_link = f"http://127.0.0.1:8000/accounts/register/{invitation.token}/"
            send_mail(
                subject="You are invited to join the Staff Portal",
                message=f"Click this link to register: {invite_link}",
                from_email="no-reply@school.com",
                recipient_list=[invitation.email],
            )
            messages.success(request, f"Invitation sent to {invitation.email}")
            return redirect("adminpanel:send_staff_invite")
    else:
        form = StaffInvitationForm()

    return render(request, "adminpanel/send_invite.html", {"form": form})


@login_required
def admin_dashboard(request):
    """Admin dashboard with stats overview."""
    if not request.user.is_admin_user():
        return redirect("accounts:login")

    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)

    context = {
        "total_staff": User.objects.filter(role="staff").count(),
        "present_count": today_attendance.filter(status="present").count(),
        "absent_count": today_attendance.filter(status="absent").count(),
        "late_count": today_attendance.filter(status="late").count(),
        "pending_leaves": Leave.objects.filter(status="pending").count(),
    }
    return render(request, "adminpanel/dashboard.html", context)


@login_required
def manage_staff(request):
    """List staff members for management."""
    if not request.user.is_admin_user():
        return redirect("accounts:login")

    staff_list = User.objects.filter(role="staff")
    return render(request, "adminpanel/manage_staff.html", {"staff_list": staff_list})


@login_required
def edit_staff(request, staff_id):
    """Edit staff details."""
    if not request.user.is_admin_user():
        return redirect("accounts:login")

    staff = get_object_or_404(User, id=staff_id, role="staff")
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff updated successfully")
            return redirect("adminpanel:manage_staff")
    else:
        form = StaffForm(instance=staff)

    return render(request, "adminpanel/edit_staff.html", {"form": form})


@login_required
def leave_requests(request):
    """Approve or reject leave requests."""
    if not request.user.is_admin_user():
        return redirect("accounts:login")

    pending_leaves = Leave.objects.filter(status="pending").order_by("-applied_at")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(Leave, id=leave_id)

        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        leave.save()

    return render(request, "adminpanel/leave_requests.html", {"pending_leaves": pending_leaves})


@login_required
def attendance_reports(request):
    """View attendance reports with filtering."""
    if not request.user.is_admin_user():
        return redirect("accounts:login")

    records = Attendance.objects.all().order_by("-date")

    staff_id = request.GET.get("staff")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if staff_id:
        records = records.filter(staff__id=staff_id)
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)

    return render(request, "adminpanel/attendance_reports.html", {"records": records})
