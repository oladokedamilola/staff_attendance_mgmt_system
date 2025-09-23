from django.db import models
from accounts.models import User

class Attendance(models.Model):
    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
    )

    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="present")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('staff', 'date')  # Ensure one record per day per staff

    def __str__(self):
        return f"{self.staff.username} - {self.date} - {self.status}"
