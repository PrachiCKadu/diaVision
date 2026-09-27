from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPatient
from patients.models import RetinalImage

from .serializers import PredictionSerializer


class PatientPredictionDetailView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPatient,
    ]

    def get(self, request, retinal_image_id):
        try:
            retinal_image = RetinalImage.objects.get(
                id=retinal_image_id,
                patient__user=request.user,
            )
        except RetinalImage.DoesNotExist:
            return Response(
                {
                    "detail": "Retinal image not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            prediction = retinal_image.prediction
        except Exception:
            return Response(
                {
                    "detail": "Prediction not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            PredictionSerializer(prediction).data,
            status=status.HTTP_200_OK,
        )

class PatientPredictionHistoryView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPatient,
    ]

    def get(self, request):
        retinal_images = (
            RetinalImage.objects
            .filter(patient__user=request.user)
            .select_related("prediction")
            .order_by("-uploaded_at")
        )

        predictions = []

        for retinal_image in retinal_images:
            try:
                predictions.append(retinal_image.prediction)
            except Exception:
                continue

        return Response(
            PredictionSerializer(predictions, many=True).data,
            status=status.HTTP_200_OK,
        )