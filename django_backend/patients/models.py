from django.conf import settings
from django.db import models
from .validators import validate_retinal_image

class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
    )

    date_of_birth = models.DateField(
    null=True,
    blank=True,
)

    diabetes_duration_years = models.PositiveIntegerField(
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
        return f"Patient: {self.user.get_full_name() or self.user.username}"

class RetinalImage(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="retinal_images",
    )

    image = models.ImageField(
    upload_to="retinal_images/",
    validators=[validate_retinal_image],
    )

    

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"Retinal Image - "
            f"{self.patient.user.username} - "
            f"{self.uploaded_at:%Y-%m-%d %H:%M:%S}"
        )