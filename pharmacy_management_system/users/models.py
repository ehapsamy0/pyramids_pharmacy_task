from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from auditlog.registry import auditlog

class User(AbstractUser):
    """
    Default custom user model for Pharmacy Management System.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_patient = models.BooleanField(default=True)  # Default is_patient to True
    is_pharmacist = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_pharmacist:
            self.is_patient = False
        if self.is_patient:
            self.is_pharmacist = False
        super().save(*args, **kwargs)



    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Patient(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    insurance_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Patient: {self.user.username}"


class Pharmacist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="pharmacist_profile"
    )
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Pharmacist: {self.user.username}"


auditlog.register(User)
auditlog.register(Patient)
auditlog.register(Pharmacist)
