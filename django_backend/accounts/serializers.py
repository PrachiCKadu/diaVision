from rest_framework import serializers

from .models import User
from doctors.models import Doctor


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    date_of_birth = serializers.DateField(
        required=False,
        allow_null=True,
    )

    gender = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "date_of_birth",
            "gender",
            "medical_registration_number",
            "medical_council",
            "qualification",
            "specialization",
        )

        extra_kwargs = {
            "medical_registration_number": {
                "required": False,
                "allow_blank": True,
            },
            "medical_council": {
                "required": False,
                "allow_blank": True,
            },
            "qualification": {
                "required": False,
                "allow_blank": True,
            },
            "specialization": {
                "required": False,
                "allow_blank": True,
            },
        }

    def validate(self, attrs):
        role = attrs.get("role")

        if role not in {
            User.Role.PATIENT,
            User.Role.DOCTOR,
        }:
            raise serializers.ValidationError(
                {
                    "role": "Registration is allowed only for Patient or Doctor."
                }
            )

        doctor_fields = [
            "medical_registration_number",
            "medical_council",
            "qualification",
            "specialization",
        ]

        if role == User.Role.DOCTOR:
            missing_fields = [
                field
                for field in doctor_fields
                if not attrs.get(field)
            ]

            if missing_fields:
                raise serializers.ValidationError(
                    {
                        "doctor_verification": (
                            "All doctor verification details are required."
                        ),
                        "missing_fields": missing_fields,
                    }
                )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        date_of_birth = validated_data.pop(
            "date_of_birth",
            None,
        )

        gender = validated_data.pop(
            "gender",
            "",
        )

        role = validated_data.get("role")

        user = User(**validated_data)

        user.set_password(password)

        if role == User.Role.DOCTOR:
            user.doctor_verification_status = (
                User.DoctorVerificationStatus.PENDING
            )
        else:
            user.doctor_verification_status = (
                User.DoctorVerificationStatus.NOT_REQUIRED
            )

        user.save()

        if role == User.Role.PATIENT:
            patient = user.patient_profile
            patient.date_of_birth = date_of_birth
            patient.gender = gender
            patient.save(
                update_fields=[
                    "date_of_birth",
                    "gender",
                    "updated_at",
                ]
            )

        elif role == User.Role.DOCTOR:
            doctor = user.doctor_profile
            doctor.specialization = user.specialization or ""
            doctor.save(
                update_fields=[
                    "specialization",
                    "updated_at",
                ]
            )

        return user


class AdminDoctorVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "doctor_verification_status",
            "medical_registration_number",
            "medical_council",
            "qualification",
            "specialization",
        )



class PendingDoctorSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(source="user.id", read_only=True)

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    doctor_verification_status = serializers.CharField(
        source="user.doctor_verification_status",
        read_only=True
    )

    medical_registration_number = serializers.CharField(
        source="user.medical_registration_number",
        read_only=True
    )

    medical_council = serializers.CharField(
        source="user.medical_council",
        read_only=True
    )

    qualification = serializers.CharField(
        source="user.qualification",
        read_only=True
    )

    specialization = serializers.CharField(
        source="user.specialization",
        read_only=True
    )

    class Meta:
        model = Doctor

        fields = (
            "id",
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "doctor_verification_status",
            "medical_registration_number",
            "medical_council",
            "qualification",
            "specialization",
            "hospital_clinic",
            "license_number",
        )

        read_only_fields = fields



class AdminDoctorVerificationActionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[
            User.DoctorVerificationStatus.APPROVED,
            User.DoctorVerificationStatus.REJECTED,
        ]
    )

    def validate(self, attrs):
        doctor = self.context["doctor"]

        if doctor.role != User.Role.DOCTOR:
            raise serializers.ValidationError(
                "Only doctor accounts can be verified."
            )

        if (
            doctor.doctor_verification_status
            != User.DoctorVerificationStatus.PENDING
        ):
            raise serializers.ValidationError(
                "Only pending doctor accounts can be approved or rejected."
            )

        return attrs