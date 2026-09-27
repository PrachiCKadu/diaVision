from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsDoctor
from patients.models import RetinalImage

from reports.models import MedicalReport

from .serializers import (
    DoctorCaseDetailSerializer,
    DoctorCaseSerializer,
)

from .review_serializers import DoctorReviewSerializer
from .models import DoctorReview


class DoctorCaseListView(ListAPIView):
    permission_classes = [
        IsAuthenticated,
        IsDoctor,
    ]

    serializer_class = DoctorCaseSerializer

    queryset = (
        RetinalImage.objects
        .select_related(
            "patient__user",
            "prediction",
        )
        .order_by("-uploaded_at")
    )


class DoctorCaseDetailView(RetrieveAPIView):
    permission_classes = [
        IsAuthenticated,
        IsDoctor,
    ]

    serializer_class = DoctorCaseDetailSerializer

    lookup_field = "id"
    lookup_url_kwarg = "retinal_image_id"

    queryset = (
        RetinalImage.objects
        .select_related(
            "patient__user",
            "prediction",
        )
    )

class DoctorReviewCreateView(CreateAPIView):

    permission_classes = [
        IsAuthenticated,
        IsDoctor,
    ]

    serializer_class = DoctorReviewSerializer

    def perform_create(self, serializer):

        doctor = self.request.user.doctor_profile

        review = serializer.save(
            doctor=doctor,
        )

        from reports.services import generate_medical_report

        generate_medical_report(
            review.retinal_image,
            doctor=doctor,
        )

class DoctorReviewDetailView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAuthenticated,
        IsDoctor,
    ]

    serializer_class = DoctorReviewSerializer

    lookup_field = "retinal_image_id"

    def get_queryset(self):

        return DoctorReview.objects.filter(
            doctor=self.request.user.doctor_profile
        ).select_related(
            "doctor__user",
            "retinal_image",
        )

    def perform_update(self, serializer):

        review = serializer.save()

        from reports.services import generate_medical_report

        generate_medical_report(
            review.retinal_image,
            doctor=self.request.user.doctor_profile,
        )

class DoctorDashboardOverviewView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsDoctor,
    ]

    def get(self, request):

        total_cases = RetinalImage.objects.count()

        reviewed_cases = DoctorReview.objects.count()

        pending_reviews = (
            RetinalImage.objects
            .filter(doctor_review__isnull=True)
            .count()
        )

        reports_generated = MedicalReport.objects.count()

        return Response({
            "total_cases": total_cases,
            "pending_reviews": pending_reviews,
            "reviewed_cases": reviewed_cases,
            "reports_generated": reports_generated,
        })