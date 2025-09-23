# leave/views.py
import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from .models import Leave


@login_required
def apply_leave(request):
    """Allow staff to apply for leave."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

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
        messages.success(request, "Leave request submitted")
        return redirect("staff_dashboard")

    return render(request, "leave/apply_leave.html")


@login_required
def manage_leave(request):
    """Admins can approve/reject leave requests."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    leaves = Leave.objects.all().order_by("-applied_at")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(Leave, id=leave_id)

        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        leave.save()
        messages.success(request, f"Leave request {action}d")
        return redirect("leave:manage_leave")

    return render(request, "leave/manage_leave.html", {"leaves": leaves})


@login_required
def leave_report(request):
    """Admins can view or export leave reports."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied")
        return redirect("accounts:login")

    leaves = Leave.objects.all().order_by("staff", "-applied_at")

    # CSV export
    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="leave_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Staff", "Leave Type", "Start Date", "End Date", "Status"])
        for l in leaves:
            writer.writerow([l.staff.username, l.leave_type, l.start_date, l.end_date, l.status])

        return response

    return render(request, "leave/leave_report.html", {"leaves": leaves})
