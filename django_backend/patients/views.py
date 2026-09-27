from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPatient
from .serializers import RetinalImageUploadSerializer
from predictions.services import (
    predict_retinal_image,
    save_prediction,
    generate_retinal_gradcam,
)

class RetinalImageUploadView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            patient = request.user.patient_profile
        except Exception:
            return Response(
                {
                    "detail": "Patient profile not found."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RetinalImageUploadSerializer(
            data=request.data
        )

        if serializer.is_valid():
            retinal_image = serializer.save(patient=patient)

            result = predict_retinal_image(retinal_image.image.path)

            prediction, created = save_prediction(
                retinal_image,
                result,
            )

            generate_retinal_gradcam(
                retinal_image,
                prediction,
            )

            return Response(
                RetinalImageUploadSerializer(retinal_image).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )