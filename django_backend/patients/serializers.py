from rest_framework import serializers

from .models import RetinalImage


class RetinalImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetinalImage
        fields = ["id", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]