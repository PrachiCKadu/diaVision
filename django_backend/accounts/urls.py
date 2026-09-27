from django.urls import path

from .views import (
    CurrentUserView,
    UserLoginView,
    UserRegistrationView,
    RegisterPageView,
    PendingDoctorListView,
    AdminDoctorVerificationView,
    AdminStatisticsView,
    AdminUserListView,
    AdminDeletePatientView,
    AdminDeleteDoctorView,
    AdminDoctorDetailView,
)

from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register",
    ),
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),
    path(
    "admin/doctors/pending/",
    PendingDoctorListView.as_view(),
    name="pending-doctors",
    ),
    path(
        "admin/doctors/<int:doctor_id>/verification/",
        AdminDoctorVerificationView.as_view(),
        name="doctor-verification",
    ),
        path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
        path(
        "admin/statistics/",
        AdminStatisticsView.as_view(),
        name="admin-statistics",
    ),
        path(
        "admin/users/",
        AdminUserListView.as_view(),
        name="admin-users",
    ),

        path(
            "admin/patients/<int:patient_id>/delete/",
            AdminDeletePatientView.as_view(),
            name="admin-delete-patient",
    ),

        path(
            "admin/doctors/<int:doctor_id>/delete/",
            AdminDeleteDoctorView.as_view(),
            name="admin-delete-doctor",
    ),
   path(
    "admin/doctors/<int:doctor_id>/",
    AdminDoctorDetailView.as_view(),
    name="admin-doctor-detail",
),
    
]