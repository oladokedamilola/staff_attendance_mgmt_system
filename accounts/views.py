# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StaffInvitation, User


def staff_register(request, token):
    """Handle staff registration via invitation token."""
    invitation = get_object_or_404(StaffInvitation, token=token, is_used=False)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=invitation.email,
                password=password,
                role="staff",
            )
            invitation.is_used = True
            invitation.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("login")

    return render(request, "accounts/staff_register.html", {"email": invitation.email})


def login_view(request):
    """Custom login view with role-based redirects."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == "admin":
                return redirect("admin_dashboard")
            return redirect("staff_dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    """Logout the current user and redirect to login page."""
    logout(request)
    return redirect("login")



from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})