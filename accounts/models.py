from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("staff", "Staff"),
        ("admin", "Admin"),
    )

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="staff")
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_staff_user(self):
        return self.role == "staff"

    def is_admin_user(self):
        return self.role == "admin"

    def get_full_name(self):
        """Return user's first + last name, or fallback to email if not provided."""
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
