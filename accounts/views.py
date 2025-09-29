from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StaffInvitation, User, PasswordResetAttempt, PasswordResetToken
from accounts.forms import LoginForm, ProfileUpdateForm, StaffRegisterForm
from .forms import PasswordResetForm, PasswordResetRequestForm
from .utils import *
import pycountry

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




# ----------------------------
# 🔄 Password Reset Views
# ----------------------------
RESET_LIMIT = 3
RESET_WINDOW_MINUTES = 30

def password_reset_request(request):
    """Request password reset (step 1)."""
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "❌ Email not found.")
                return redirect("password_reset_request")
            
            # Rate limiting
            attempts = PasswordResetAttempt.recent_attempts(user, minutes=RESET_WINDOW_MINUTES)
            if attempts >= RESET_LIMIT:
                messages.error(
                    request,
                    f"⚠️ Maximum {RESET_LIMIT} reset attempts allowed in {RESET_WINDOW_MINUTES} minutes. Try later."
                )
                return redirect("password_reset_request")
            
            # Log attempt
            PasswordResetAttempt.objects.create(user=user)
            
            # Generate token
            token = generate_password_reset_token()
            PasswordResetToken.objects.create(user=user, token=token)
            
            # Send email
            send_password_reset_email(user, token)
            messages.success(
                        request,
                        "✅ If an account exists with that email, we’ve sent a password reset link. Please check your inbox."
                    )
            return redirect("login")
    else:
        form = PasswordResetRequestForm()
    
    return render(request, "accounts/password_reset_request.html", {"form": form})


def password_reset_confirm(request, token):
    """Reset password using token (step 2)."""
    reset_token = get_object_or_404(PasswordResetToken, token=token, used=False)
    
    if reset_token.is_expired():
        messages.error(request, "❌ This reset link has expired.")
        return redirect("password_reset_request")
    
    if request.method == "POST":
        form = PasswordResetForm(reset_token.user, request.POST)
        if form.is_valid():
            form.save()
            reset_token.used = True
            reset_token.save()
            messages.success(request, "✅ Password reset successful. You can now log in.")
            return redirect("login")
    else:
        form = PasswordResetForm(reset_token.user)
    
    return render(request, "accounts/password_reset_confirm.html", {"form": form})




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
    user = request.user
    countries = list(pycountry.countries)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            # redirect based on role
            return redirect("admin_dashboard" if user.role == "admin" else "staff_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "accounts/profile.html", {"form": form, "countries": countries})

