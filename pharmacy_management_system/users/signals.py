# users/signals.py
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Patient
from .models import Pharmacist
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a related Patient or Pharmacist profile when a new user is created.
    """
    if created:
        # If the user is a patient, create a Patient profile
        if instance.is_patient:
            Patient.objects.create(user=instance)
        # If the user is a pharmacist, create a Pharmacist profile
        elif instance.is_pharmacist:
            Pharmacist.objects.create(user=instance)


@receiver(pre_save, sender=User)
def manage_user_profiles(sender, instance, **kwargs):
    """
    Manage Patient and Pharmacist profiles when switching roles.
    """
    if not instance.pk:
        # If user is new, skip this step as it will be handled in `create_user_profile`
        return

    # Fetch the current user from the database to check their existing roles
    current_user = User.objects.get(pk=instance.pk)

    # If the user is switching from Patient to Pharmacist
    if current_user.is_patient and instance.is_pharmacist:
        # Remove Patient profile
        Patient.objects.filter(user=instance).delete()
        # Create Pharmacist profile
        Pharmacist.objects.get_or_create(user=instance)

    # If the user is switching from Pharmacist to Patient
    elif current_user.is_pharmacist and instance.is_patient:
        # Remove Pharmacist profile
        Pharmacist.objects.filter(user=instance).delete()
        # Create Patient profile
        Patient.objects.get_or_create(user=instance)
