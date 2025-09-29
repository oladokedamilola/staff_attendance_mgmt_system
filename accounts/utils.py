# accounts/utils.py
import secrets
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


# ===================================
# 🔑 Password reset token handling
# ===================================
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = getattr(settings, "PASSWORD_RESET_TOKEN_EXPIRY_HOURS", 1)

def generate_password_reset_token():
    """Generates a random secure token."""
    return secrets.token_urlsafe(32)

def send_password_reset_email(user, token, request=None):
    """Send password reset email with proper absolute URL."""
    try:
        if request:
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", args=[token])
            )
        else:
            # fallback: construct with domain if request not passed
            domain = getattr(settings, "DOMAIN", "http://localhost:8000")
            reset_url = f"{domain}{reverse('password_reset_confirm', args=[token])}"

        subject = "🔑 Reset Your Password - SignalTrackr"
        message = f"""
Hi {user.get_full_name() or user.email},

You requested to reset your password. Click the link below to set a new password:

{reset_url}

This link will expire in 24 hours.

If you did not request this, you can ignore this email.

Thanks,  
SignalTrackr Team
"""

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"⚠️ Error in send_password_reset_email: {str(e)}")