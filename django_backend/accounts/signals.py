from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from patients.models import Patient
from doctors.models import Doctor


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == User.Role.PATIENT:
        Patient.objects.get_or_create(user=instance)

    elif instance.role == User.Role.DOCTOR:
        Doctor.objects.get_or_create(user=instance)