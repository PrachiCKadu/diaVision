from django.http import HttpResponse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import RetinalImage

from .services import (
    generate_medical_report,
    generate_medical_report_pdf,
)

from .models import MedicalReport
from .serializers import MedicalReportSerializer

class MedicalReportGenerateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, case_id):

        if request.user.role != "DOCTOR":
            return Response(
                {"detail": "Only doctors can generate medical reports."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            retinal_image = RetinalImage.objects.select_related(
                "prediction",
                "patient__user",
            ).get(id=case_id)

        except RetinalImage.DoesNotExist:
            return Response(
                {"detail": "Retinal case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            doctor = request.user.doctor_profile
        except Exception:
            return Response(
                {"detail": "Doctor profile not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            report, created = generate_medical_report(
                retinal_image,
                doctor=doctor,
            )

        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MedicalReportSerializer(report)

        return Response(
            {
                "message": (
                    "Medical report generated successfully."
                    if created
                    else "Medical report updated successfully."
                ),
                "created": created,
                "report": serializer.data,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

class MedicalReportDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):

        try:
            retinal_image = RetinalImage.objects.get(
                id=case_id
            )
        except RetinalImage.DoesNotExist:
            return Response(
                {"detail": "Retinal case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            report = retinal_image.medical_report
        except MedicalReport.DoesNotExist:
            return Response(
                {"detail": "Medical report not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MedicalReportSerializer(report)

        return Response(serializer.data)


class MedicalReportPDFView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, case_id):

        try:
            retinal_image = RetinalImage.objects.select_related(
                "patient__user",
                "prediction",
            ).get(id=case_id)

        except RetinalImage.DoesNotExist:
            return Response(
                {"detail": "Retinal case not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            report = retinal_image.medical_report

        except MedicalReport.DoesNotExist:
            return Response(
                {"detail": "Medical report not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pdf_file = generate_medical_report_pdf(report)

        response = HttpResponse(
            pdf_file.read(),
            content_type="application/pdf",
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; '
            f'filename="{pdf_file.name}"'
        )

        return response