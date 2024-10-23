from django.db import models
from pharmacy_management_system.users.models import Patient
from pharmacy_management_system.users.models import Pharmacist


class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class RefillRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)
    pharmacist = models.ForeignKey(
        Pharmacist, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )  # New field

    def __str__(self):
        return (
            f"Refill request for {self.medication.name} by {self.patient.user.username}"
        )
