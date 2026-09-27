from django.conf import settings
from django.db import models


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    specialization = models.CharField(
        max_length=100,
        blank=True,
    )

    hospital_clinic = models.CharField(
        max_length=200,
        blank=True,
    )

    license_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class DoctorReview(models.Model):
    retinal_image = models.OneToOneField(
        "patients.RetinalImage",
        on_delete=models.CASCADE,
        related_name="doctor_review",
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    review_notes = models.TextField(
        blank=True,
    )

    reviewed_at = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"Review for RetinalImage "
            f"{self.retinal_image_id} by "
            f"{self.doctor}"
        )