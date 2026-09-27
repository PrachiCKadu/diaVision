from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    email = models.EmailField(
        unique=True,
    )

    class DoctorVerificationStatus(models.TextChoices):
        NOT_REQUIRED = "NOT_REQUIRED", "Not Required"
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    doctor_verification_status = models.CharField(
        max_length=20,
        choices=DoctorVerificationStatus.choices,
        default=DoctorVerificationStatus.NOT_REQUIRED,
    )

    medical_registration_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    medical_council = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    qualification = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    specialization = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"