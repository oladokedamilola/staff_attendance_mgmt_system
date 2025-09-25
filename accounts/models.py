from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ("staff", "Staff"),
        ("admin", "Admin"),
    )

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="staff")

    USERNAME_FIELD = "email"   # <--- Email is the login field
    REQUIRED_FIELDS = []      

    def is_staff_user(self):
        return self.role == "staff"

    def is_admin_user(self):
        return self.role == "admin"


# Staff invitation model
class StaffInvitation(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.email} - {'Used' if self.is_used else 'Pending'}"
