from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StaffInvitation, User
from accounts.forms import LoginForm, ProfileUpdateForm, StaffRegisterForm


def login_view(request):
    """Custom login view with email-only login and role-based redirects."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        if request.user.role == "admin":
            return redirect("admin_dashboard")
        return redirect("staff_dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")

            if user.role == "admin":
                return redirect("admin_dashboard")
            return redirect("staff_dashboard")

        messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "accounts/login.html", {"form": form})



def staff_register(request, token):
    """Handle staff registration via invitation token."""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("admin_dashboard" if request.user.role == "admin" else "staff_dashboard")

    invitation = get_object_or_404(StaffInvitation, token=token, is_used=False)

    if request.method == "POST":
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = invitation.email  # Use the invited email
            user.role = "staff"
            user.save()
            invitation.is_used = True
            invitation.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
    else:
        form = StaffRegisterForm()

    return render(request, "accounts/staff_register.html", {"form": form, "email": invitation.email})




def logout_view(request):
    """Logout the current user and redirect to login page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    """Allow user to update their profile."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)  # include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("admin_dashboard" if request.user.role == "admin" else "staff_dashboard")
        else:
            messages.error(request, "There were errors in your form. Please correct them below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})

