from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken



from .models import User
from doctors.models import Doctor
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
)


from .serializers import (
    UserRegistrationSerializer,
    AdminDoctorVerificationSerializer,
    AdminDoctorVerificationActionSerializer,
    PendingDoctorSerializer,
)


from .permissions import IsAdminUser
from django.shortcuts import render

from patients.models import Patient, RetinalImage
from predictions.models import Prediction
from doctors.models import Doctor, DoctorReview
from reports.models import MedicalReport

from rest_framework.views import APIView
from rest_framework import status

from .models import User
from doctors.models import Doctor

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "error": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            try:
                user_by_email = User.objects.get(
                    email__iexact=username
                )
            except User.DoesNotExist:
                user_by_email = None

            if user_by_email is not None:
                user = authenticate(
                    username=user_by_email.username,
                    password=password,
                )

        if user is None:
            return Response(
                {
                    "error": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {
                    "error": "User account is inactive."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not user.is_active:
            return Response(
                {
                    "error": "User account is inactive."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if (
            user.role == User.Role.DOCTOR
            and user.doctor_verification_status
            != User.DoctorVerificationStatus.APPROVED
        ):
            return Response(
                {
                    "error": (
                        "Doctor account is awaiting administrator "
                        "verification."
                        if user.doctor_verification_status
                        == User.DoctorVerificationStatus.PENDING
                        else "Doctor account verification was rejected."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )

class CurrentUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        return Response(
            {
                "message": "Authentication successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )

def LoginPageView(request):
    return render(request, "auth/login.html")

def RegisterPageView(request):
    return render(request, "auth/register.html")

class PendingDoctorListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    serializer_class = PendingDoctorSerializer

    def get_queryset(self):

        return (
            Doctor.objects
            .select_related("user")
            .filter(
                user__role=User.Role.DOCTOR,
                user__doctor_verification_status=(
                    User.DoctorVerificationStatus.PENDING
                ),
            )
            .order_by("-user__date_joined")
        )

class AdminStatisticsView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):

        return Response(
            {
                "users": User.objects.count(),

                "patients": Patient.objects.count(),

                "doctors": Doctor.objects.count(),

                "pending_doctors": User.objects.filter(
                    role=User.Role.DOCTOR,
                    doctor_verification_status=(
                        User.DoctorVerificationStatus.PENDING
                    ),
                ).count(),

                "approved_doctors": User.objects.filter(
                    role=User.Role.DOCTOR,
                    doctor_verification_status=(
                        User.DoctorVerificationStatus.APPROVED
                    ),
                ).count(),

                "retinal_cases": RetinalImage.objects.count(),

                "predictions": Prediction.objects.count(),

                "doctor_reviews": DoctorReview.objects.count(),

                "medical_reports": MedicalReport.objects.count(),
            },
            status=status.HTTP_200_OK,
        )

class AdminDoctorVerificationView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    serializer_class = AdminDoctorVerificationActionSerializer

    def patch(self, request, doctor_id, *args, **kwargs):
        try:
            doctor = User.objects.get(
                id=doctor_id,
                role=User.Role.DOCTOR,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "error": "Doctor account not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            data=request.data,
            context={
                "doctor": doctor,
            },
        )

        serializer.is_valid(raise_exception=True)

        doctor.doctor_verification_status = (
            serializer.validated_data["status"]
        )

        doctor.save(
            update_fields=[
                "doctor_verification_status",
            ]
        )

        return Response(
            {
                "message": (
                    "Doctor verification status updated successfully."
                ),
                "doctor": {
                    "id": doctor.id,
                    "username": doctor.username,
                    "doctor_verification_status": (
                        doctor.doctor_verification_status
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )


class AdminDoctorDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def get(self, request, doctor_id):

        try:
            doctor = (
                Doctor.objects
                .select_related("user")
                .get(
                    id=doctor_id,
                    user__role=User.Role.DOCTOR,
                )
            )

        except Doctor.DoesNotExist:

            return Response(
                {
                    "detail": "Doctor not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        user = doctor.user

        return Response(
            {
                "id": doctor.id,
                "user_id": user.id,

                "username": user.username,
                "email": user.email,

                "first_name": user.first_name,
                "last_name": user.last_name,

                # Doctor verification details
                "medical_registration_number":
                    user.medical_registration_number,

                "medical_council":
                    user.medical_council,

                "qualification":
                    user.qualification,

                "specialization":
                    user.specialization,

                # Doctor profile details
                "hospital_clinic":
                    doctor.hospital_clinic,

                "license_number":
                    doctor.license_number,

                # Verification status
                "verification_status":
                    user.doctor_verification_status,
            },
            status=status.HTTP_200_OK
        )
class AdminUserListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):

        patients = []

        for patient in Patient.objects.select_related("user").all():

            patients.append({
                "id": patient.id,
                "user_id": patient.user.id,

                "username": patient.user.username,
                "email": patient.user.email,

                "first_name": patient.user.first_name,
                "last_name": patient.user.last_name,

                "age": patient.age,
                "gender": patient.gender,

                "retinal_cases":
                    patient.retinal_images.count(),
            })


        doctors = []

        for doctor in (
            Doctor.objects
            .select_related("user")
            .filter(
                user__doctor_verification_status=
                    User.DoctorVerificationStatus.APPROVED
            )
        ):

            doctors.append({
                "id": doctor.id,
                "user_id": doctor.user.id,

                "username": doctor.user.username,
                "email": doctor.user.email,

                "first_name": doctor.user.first_name,
                "last_name": doctor.user.last_name,

                "specialization":
                    doctor.user.specialization,

                "hospital_clinic":
                    doctor.hospital_clinic,

                "license_number":
                    doctor.license_number,

                "medical_registration_number":
                    doctor.user.medical_registration_number,

                "medical_council":
                    doctor.user.medical_council,

                "qualification":
                    doctor.user.qualification,

                "verification_status":
                    doctor.user.doctor_verification_status,
            })


        return Response({
            "patients": patients,
            "doctors": doctors,
        })

class AdminDeletePatientView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def delete(self, request, patient_id, *args, **kwargs):
        from patients.models import Patient

        try:
            patient = Patient.objects.select_related("user").get(
                id=patient_id
            )
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        username = patient.user.username

        patient.user.delete()

        return Response(
            {
                "message": f"Patient '{username}' deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


class AdminDeleteDoctorView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    def delete(self, request, doctor_id, *args, **kwargs):
        from doctors.models import Doctor

        try:
            doctor = Doctor.objects.select_related("user").get(
                id=doctor_id
            )
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        username = doctor.user.username

        doctor.user.delete()

        return Response(
            {
                "message": f"Doctor '{username}' deleted successfully."
            },
            status=status.HTTP_200_OK,
        )