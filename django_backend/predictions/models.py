from django.db import models

from patients.models import RetinalImage


class Prediction(models.Model):
    retinal_image = models.OneToOneField(
        RetinalImage,
        on_delete=models.CASCADE,
        related_name="prediction",
    )

    gradcam_image = models.ImageField(
    upload_to="gradcam/",
    null=True,
    blank=True,
    )

    predicted_class = models.CharField(
        max_length=50,
    )

    confidence = models.FloatField()

    no_dr_probability = models.FloatField()
    mild_probability = models.FloatField()
    moderate_probability = models.FloatField()
    severe_probability = models.FloatField()
    proliferative_dr_probability = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"Prediction - "
            f"{self.retinal_image.patient.user.username} - "
            f"{self.predicted_class}"
        )