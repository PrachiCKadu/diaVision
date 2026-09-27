from django.core.serializers import python
from rest_framework import serializers

from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    gradcam_image = serializers.ImageField(
        read_only=True,
    )
    retinal_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            "id",
            "retinal_image",
            "retinal_image_url",
            "predicted_class",
            "confidence",
            "no_dr_probability",
            "mild_probability",
            "moderate_probability",
            "severe_probability",
            "proliferative_dr_probability",
            "gradcam_image",
            "created_at",
        ]
        read_only_fields = fields

    def get_retinal_image_url(self, obj):
        if obj.retinal_image and obj.retinal_image.image:
            return obj.retinal_image.image.url
        return None

