import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from .models import Leave
from .forms import LeaveApplicationForm

@login_required
def apply_leave(request):
    """Allow staff to apply for leave."""
    if not request.user.is_staff_user():
        messages.error(request, "Access denied. Staff account required.")
        return redirect("login")

    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = request.user
            leave.save()
            messages.success(request, "Your leave request has been submitted successfully.")
            return redirect("staff_dashboard")
    else:
        form = LeaveApplicationForm()

    return render(request, "leave/apply_leave.html", {"form": form})


@login_required
def manage_leave(request):
    """Admins can approve/reject leave requests."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("login")

    leaves = Leave.objects.all().order_by("-applied_at")

    if not leaves.exists():
        messages.info(request, "No leave requests available at the moment.")

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(Leave, id=leave_id)

        if action == "approve":
            leave.status = "approved"
            messages.success(request, f"Leave request for {leave.staff.username} has been approved.")
        elif action == "reject":
            leave.status = "rejected"
            messages.warning(request, f"Leave request for {leave.staff.username} has been rejected.")
        else:
            messages.error(request, "Invalid action provided.")
            return redirect("manage_leave")

        leave.save()
        return redirect("manage_leave")

    return render(request, "leave/manage_leave.html", {"leaves": leaves})


@login_required
def leave_report(request):
    """Admins can view or export leave reports."""
    if not request.user.is_admin_user():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("login")

    leaves = Leave.objects.all().order_by("staff", "-applied_at")

    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="leave_report.csv"'

        writer = csv.writer(response)
        writer.writerow(["Staff", "Leave Type", "Start Date", "End Date", "Status"])
        for l in leaves:
            writer.writerow([l.staff.username, l.leave_type, l.start_date, l.end_date, l.status])

        messages.success(request, "Leave report exported successfully as CSV.")
        return response

    if not leaves.exists():
        messages.warning(request, "No leave records found to display.")

    return render(request, "leave/leave_report.html", {"leaves": leaves})
