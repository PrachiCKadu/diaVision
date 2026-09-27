from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """
    Allows access only to authenticated users
    whose role is PATIENT.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "PATIENT"
        )


class IsDoctor(BasePermission):
    """
    Allows access only to authenticated users
    whose role is DOCTOR.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "DOCTOR"
        )


class IsAdminUser(BasePermission):
    """
    Allows access only to authenticated users
    whose application role is ADMIN.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )