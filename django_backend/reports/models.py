from django.conf import settings
from django.db import models

from patients.models import RetinalImage


class MedicalReport(models.Model):

    retinal_image = models.OneToOneField(
        RetinalImage,
        on_delete=models.CASCADE,
        related_name="medical_report",
    )

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_medical_reports",
    )

    report_title = models.CharField(
        max_length=255,
        default="Diabetic Retinopathy Assessment Report",
    )

    clinical_summary = models.TextField(
        blank=True,
    )

    ai_prediction = models.CharField(
        max_length=100,
        blank=True,
    )

    ai_confidence = models.FloatField(
        null=True,
        blank=True,
    )

    doctor_notes = models.TextField(
        blank=True,
    )

    recommendation = models.TextField(
        blank=True,
    )

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return (
            f"Report for Retinal Case #{self.retinal_image.id}"
        )