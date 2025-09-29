from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    ROLE_CHOICES = (
        ("staff", "Staff"),
        ("admin", "Admin"),
    )

    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="staff")
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No extra required fields

    objects = CustomUserManager() 

    def is_staff_user(self):
        return self.role == "staff"

    def is_admin_user(self):
        return self.role == "admin"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    def __str__(self):
        return self.get_full_name()


# Staff invitation model
class StaffInvitation(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.email} - {'Used' if self.is_used else 'Pending'}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRY_HOURS)


class PasswordResetAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]
    
    @staticmethod
    def recent_attempts(user, minutes=30):
        """
        Count attempts in the last `minutes` minutes.
        """
        cutoff = timezone.now() - timedelta(minutes=minutes)
        return PasswordResetAttempt.objects.filter(user=user, created_at__gte=cutoff).count()

