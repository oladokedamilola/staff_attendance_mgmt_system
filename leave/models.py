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
    evidence = models.FileField(upload_to="leave_evidence/", blank=True, null=True)  # 👈 Evidence file
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.username} - {self.leave_type} ({self.start_date} to {self.end_date}) - {self.status}"


from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.recipient.email} - {self.subject}"