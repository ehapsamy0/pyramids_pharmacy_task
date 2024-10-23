from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("MEDICATION_REQUEST", "Medication Request"),
        ("MEDICATION_FULFILL", "Medication Fulfillment"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp}"
