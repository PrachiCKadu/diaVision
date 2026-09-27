from rest_framework import serializers

from .models import DoctorReview


class DoctorReviewSerializer(serializers.ModelSerializer):

    doctor_id = serializers.IntegerField(
        source="doctor.id",
        read_only=True,
    )

    doctor_name = serializers.CharField(
        source="doctor.user.username",
        read_only=True,
    )

    reviewed_at = serializers.DateTimeField(
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        read_only=True,
    )

    class Meta:
        model = DoctorReview

        fields = [
            "id",
            "retinal_image",
            "doctor_id",
            "doctor_name",
            "review_notes",
            "reviewed_at",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "doctor_id",
            "doctor_name",
            "reviewed_at",
            "created_at",
        ]

    def validate_review_notes(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Clinical review notes cannot be empty."
            )

        return value