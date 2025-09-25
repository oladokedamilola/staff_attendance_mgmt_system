from uuid import uuid4
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import StaffInvitation, User
from attendance.models import Attendance
from leave.models import Leave
from .forms import StaffInvitationForm, StaffForm

from uuid import uuid4
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

from .forms import StaffInvitationForm


@login_required
def send_staff_invite(request):
    """Allow admin to invite staff via email and see invitations status."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("home")

    # Handle revoking
    if request.method == "POST" and "revoke_id" in request.POST:
        invitation = get_object_or_404(StaffInvitation, id=request.POST["revoke_id"], is_used=False)
        invitation.delete()
        messages.success(request, f"Invitation to {invitation.email} revoked.")
        return redirect("send_staff_invite")

    # Handle sending new invitation
    if request.method == "POST" and "email" in request.POST:
        form = StaffInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.token = uuid4()
            invitation.save()

            # Generate full URL
            invite_link = request.build_absolute_uri(f"/accounts/register/{invitation.token}/")

            # Email content
            subject = "You are invited to join StaffHub 🎉"
            text_message = f"You have been invited to join StaffHub.\nClick the link to register:\n{invite_link}"
            html_message = f"""
                <p>Hello,</p>
                <p>You have been invited to join <strong>StaffHub</strong>.</p>
                <p><a href="{invite_link}" style="background:#0d6efd;color:#fff;padding:10px 15px;border-radius:6px;text-decoration:none;">Register Now</a></p>
                <p>If the button doesn’t work, copy and paste this link: {invite_link}</p>
                <br><p>Best regards,<br>StaffHub Team</p>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[invitation.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, f"Invitation sent to {invitation.email}.")
            return redirect("send_staff_invite")
        else:
            messages.error(request, "There was an error with the invitation form.")
    else:
        form = StaffInvitationForm()

    # Invitations for display
    used_invitations = StaffInvitation.objects.filter(is_used=True).order_by("-created_at")
    pending_invitations = StaffInvitation.objects.filter(is_used=False).order_by("-created_at")

    context = {
        "form": form,
        "used_invitations": used_invitations,
        "pending_invitations": pending_invitations,
    }
    return render(request, "adminpanel/send_invite.html", context)



@login_required
def admin_dashboard(request):
    """Admin dashboard with stats overview."""
    if not request.user.is_admin_user():
        messages.error(request, "You do not have access to the admin dashboard.")
        return redirect("home")

    today = date.today()
    today_attendance = Attendance.objects.filter(date=today)

    context = {
        "total_staff": User.objects.filter(role="staff").count(),
        "present_count": today_attendance.filter(status="present").count(),
        "absent_count": today_attendance.filter(status="absent").count(),
        "late_count": today_attendance.filter(status="late").count(),
        "pending_leaves": Leave.objects.filter(status="pending").count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def manage_staff(request):
    """List staff members for management."""
    if not request.user.is_admin_user():
        messages.error(request, "You do not have permission to view staff management.")
        return redirect("home")

    staff_list = User.objects.filter(role="staff")
    if not staff_list.exists():
        messages.info(request, "No staff members found. Invite or add new staff.")
    return render(request, "adminpanel/manage_staff.html", {"staff_list": staff_list})


@login_required
def edit_staff(request, staff_id):
    """Edit staff details."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("home")

    staff = get_object_or_404(User, id=staff_id, role="staff")
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff member {staff.username} updated successfully.")
            return redirect("manage_staff")
        else:
            messages.error(request, "There was an error updating this staff member. Please review the form.")
    else:
        form = StaffForm(instance=staff)

    return render(request, "adminpanel/edit_staff.html", {"form": form})


@login_required
def leave_requests(request):
    """Approve or reject leave requests."""
    if not request.user.is_admin_user():
        messages.error(request, "You do not have access to leave requests.")
        return redirect("home")

    pending_leaves = Leave.objects.filter(status="pending").order_by("-applied_at")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(Leave, id=leave_id)

        if action == "approve":
            leave.status = "approved"
            leave.save()
            messages.success(request, f"Leave request for {leave.staff.username} approved.")
        elif action == "reject":
            leave.status = "rejected"
            leave.save()
            messages.info(request, f"Leave request for {leave.staff.username} rejected.")
        else:
            messages.error(request, "Invalid action provided for leave request.")

        return redirect("leave_requests")

    if not pending_leaves.exists():
        messages.info(request, "No pending leave requests at the moment.")

    return render(request, "adminpanel/leave_requests.html", {"pending_leaves": pending_leaves})


@login_required
def attendance_reports(request):
    """View attendance reports with filtering."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("home")

    records = Attendance.objects.all().order_by("-date")

    staff_id = request.GET.get("staff")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if staff_id:
        records = records.filter(staff__id=staff_id)
        messages.info(request, f"Filtered records for staff ID {staff_id}.")
    if start_date:
        records = records.filter(date__gte=start_date)
        messages.info(request, f"Showing records from {start_date}.")
    if end_date:
        records = records.filter(date__lte=end_date)
        messages.info(request, f"Showing records until {end_date}.")

    if not records.exists():
        messages.warning(request, "No attendance records found for the selected filters.")

    return render(request, "adminpanel/attendance_reports.html", {"records": records})
