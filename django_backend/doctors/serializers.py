from rest_framework import serializers

from patients.models import RetinalImage


class DoctorCaseSerializer(serializers.ModelSerializer):

    patient_id = serializers.IntegerField(
        source="patient.id",
        read_only=True,
    )

    image = serializers.ImageField(
        read_only=True,
    )

    prediction = serializers.SerializerMethodField()

    doctor_review = serializers.SerializerMethodField()

    medical_report = serializers.SerializerMethodField()

    class Meta:
        model = RetinalImage

        fields = [
            "id",
            "patient_id",
            "image",
            "uploaded_at",
            "prediction",
            "doctor_review",
            "medical_report",
        ]

        read_only_fields = fields

    def get_prediction(self, obj):

        try:
            prediction = obj.prediction

        except Exception:
            return None

        return {
            "id": prediction.id,

            "predicted_class":
                prediction.predicted_class,

            "confidence":
                prediction.confidence,

            "no_dr_probability":
                prediction.no_dr_probability,

            "mild_probability":
                prediction.mild_probability,

            "moderate_probability":
                prediction.moderate_probability,

            "severe_probability":
                prediction.severe_probability,

            "proliferative_dr_probability":
                prediction.proliferative_dr_probability,

            "gradcam_image":
                (
                    prediction.gradcam_image.url
                    if prediction.gradcam_image
                    else None
                ),

            "created_at":
                prediction.created_at,
        }

    def get_doctor_review(self, obj):

        try:
            review = obj.doctor_review

        except Exception:
            return None

        return {
            "id": review.id,

            "doctor_id":
                review.doctor_id,

            "doctor_name":
                (
                    review.doctor.user.get_full_name()
                    or review.doctor.user.username
                ),

            "review_notes":
                review.review_notes,

            "reviewed_at":
                review.reviewed_at,

            "created_at":
                review.created_at,
        }

    def get_medical_report(self, obj):

        try:
            report = obj.medical_report

        except Exception:
            return None

        return {
            "id": report.id,

            "report_title":
                report.report_title,

            "ai_prediction":
                report.ai_prediction,

            "ai_confidence":
                report.ai_confidence,

            "clinical_summary":
                report.clinical_summary,

            "doctor_notes":
                report.doctor_notes,

            "recommendation":
                report.recommendation,

            "generated_at":
                report.generated_at,

            "updated_at":
                report.updated_at,
        }


class DoctorCaseDetailSerializer(
    DoctorCaseSerializer
):

    patient_username = serializers.CharField(
        source="patient.user.username",
        read_only=True,
    )

    patient_age = serializers.IntegerField(
        source="patient.age",
        read_only=True,
    )

    patient_gender = serializers.CharField(
        source="patient.gender",
        read_only=True,
    )

    diabetes_duration_years = serializers.IntegerField(
        source="patient.diabetes_duration_years",
        read_only=True,
    )

    class Meta(
        DoctorCaseSerializer.Meta
    ):

        fields = [
            "id",
            "patient_id",
            "patient_username",
            "patient_age",
            "patient_gender",
            "diabetes_duration_years",
            "image",
            "uploaded_at",
            "prediction",
            "doctor_review",
            "medical_report",
        ]

        read_only_fields = fields