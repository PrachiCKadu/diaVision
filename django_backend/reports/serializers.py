from rest_framework import serializers

from .models import MedicalReport


class MedicalReportSerializer(serializers.ModelSerializer):

    case_id = serializers.IntegerField(
        source="retinal_image.id",
        read_only=True,
    )

    class Meta:
        model = MedicalReport
        fields = [
            "id",
            "case_id",
            "report_title",
            "clinical_summary",
            "ai_prediction",
            "ai_confidence",
            "doctor_notes",
            "recommendation",
            "generated_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "case_id",
            "generated_at",
            "updated_at",
        ]