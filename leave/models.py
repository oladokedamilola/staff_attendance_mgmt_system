from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User

class Leave(models.Model):
    LEAVE_TYPES = (
        ("sick", "Sick Leave"),
        ("casual", "Casual Leave"),
        ("vacation", "Vacation"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.username} - {self.leave_type} ({self.start_date} to {self.end_date}) - {self.status}"
