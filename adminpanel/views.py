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
from django.core.mail import EmailMultiAlternatives
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


from datetime import timedelta, date
from django.db.models import Count, Q

@login_required
def admin_dashboard(request):
    """Admin dashboard with stats overview and attendance trends by percentage."""
    if not request.user.is_admin_user():
        messages.error(request, "You do not have access to the admin dashboard.")
        return redirect("home")

    today = date.today()
    total_staff = User.objects.filter(role="staff").count()
    today_attendance = Attendance.objects.filter(date=today)

    # --- Attendance Chart Range ---
    range_option = request.GET.get("range", "7")  # default 7 days
    try:
        range_days = int(range_option)
    except ValueError:
        range_days = 7

    start_date = today - timedelta(days=range_days - 1)
    date_list = [start_date + timedelta(days=i) for i in range(range_days)]
    chart_labels = [d.strftime("%b %d") for d in date_list]

    trend_present = []
    trend_absent = []
    trend_late = []

    for d in date_list:
        records = Attendance.objects.filter(date=d)
        # Calculate percentage based on total staff
        trend_present.append(round((records.filter(status="present").count() / total_staff) * 100, 2) if total_staff else 0)
        trend_absent.append(round((records.filter(status="absent").count() / total_staff) * 100, 2) if total_staff else 0)
        trend_late.append(round((records.filter(status="late").count() / total_staff) * 100, 2) if total_staff else 0)

    # Recent leaves
    recent_leaves = Leave.objects.order_by("-applied_at")[:5]

    context = {
        "total_staff": total_staff,
        "present_today": today_attendance.filter(status="present").count(),
        "absent_today": today_attendance.filter(status="absent").count(),
        "late_today": today_attendance.filter(status="late").count(),
        "pending_leaves": Leave.objects.filter(status="pending").count(),
        "recent_leaves": recent_leaves,
        "chart_labels": chart_labels,
        "trend_present": trend_present,
        "trend_absent": trend_absent,
        "trend_late": trend_late,
        "selected_range": range_days,
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
            messages.success(request, f"Staff member {staff} updated successfully.")
            return redirect("manage_staff")
        else:
            messages.error(request, "There was an error updating this staff member. Please review the form.")
    else:
        form = StaffForm(instance=staff)

    return render(request, "adminpanel/edit_staff.html", {"form": form})

from leave.utils import send_leave_notification
from django.core.paginator import Paginator

@login_required
def leave_requests(request):
    """
    Admin view to manage leave requests:
    - Display pending and approved leaves
    - Approve/reject leaves
    - Send notifications
    - Paginate both tables (5 per page)
    """
    if not request.user.is_admin_user():
        messages.error(request, "You do not have access to leave requests.")
        return redirect("home")

    # Querysets
    pending_leaves_qs = Leave.objects.filter(status="pending").order_by("-applied_at")
    approved_leaves_qs = Leave.objects.filter(status="approved").order_by("-applied_at")

    # Pagination: 5 per page
    pending_paginator = Paginator(pending_leaves_qs, 5)
    approved_paginator = Paginator(approved_leaves_qs, 5)

    pending_page_number = request.GET.get("pending_page")
    approved_page_number = request.GET.get("approved_page")

    pending_leaves = pending_paginator.get_page(pending_page_number)
    approved_leaves = approved_paginator.get_page(approved_page_number)

    # Handle POST for approve/reject
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(Leave, id=leave_id)

        try:
            if action == "approve":
                leave.status = "approved"
                leave.save()
                messages.success(request, f"Leave request for {leave.staff.get_full_name()} approved.")

                # Notify staff
                send_leave_notification(
                    sender=request.user,
                    recipient=leave.staff,
                    subject="Leave Request Approved",
                    message=(
                        f"Your leave request ({leave.leave_type}) from {leave.start_date} "
                        f"to {leave.end_date} has been approved."
                    ),
                    request=request  # optional on-site notification
                )

            elif action == "reject":
                leave.status = "rejected"
                leave.save()
                messages.info(request, f"Leave request for {leave.staff.get_full_name()} rejected.")

                # Notify staff
                send_leave_notification(
                    sender=request.user,
                    recipient=leave.staff,
                    subject="Leave Request Rejected",
                    message=(
                        f"Your leave request ({leave.leave_type}) from {leave.start_date} "
                        f"to {leave.end_date} has been rejected."
                    ),
                    request=request
                )
            else:
                messages.error(request, "Invalid action provided for leave request.")

        except Exception:
            messages.warning(
                request,
                "Leave status updated, but failed to send notification. Error logged."
            )

        return redirect("leave_requests")

    # Inform admin if no pending requests
    if not pending_leaves_qs.exists():
        messages.info(request, "No pending leave requests at the moment.")

    context = {
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves,
    }
    return render(request, "adminpanel/leave_requests.html", context)
