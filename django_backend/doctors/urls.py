from django.urls import path

from .views import (
    DoctorCaseListView,
    DoctorCaseDetailView,
    DoctorReviewCreateView,
    DoctorReviewDetailView,
    DoctorDashboardOverviewView,
)


urlpatterns = [
    path(
        "cases/",
        DoctorCaseListView.as_view(),
        name="doctor-case-list",
    ),
    path(
        "cases/<int:retinal_image_id>/",
        DoctorCaseDetailView.as_view(),
        name="doctor-case-detail",
    ),
    path(
    "cases/<int:retinal_image_id>/review/",
    DoctorReviewCreateView.as_view(),
    name="doctor-review-create",
    ),
    path(
    "cases/<int:retinal_image_id>/review/detail/",
    DoctorReviewDetailView.as_view(),
    name="doctor-review-detail",
    ),
    path(
    "dashboard/overview/",
    DoctorDashboardOverviewView.as_view(),
    name="doctor-dashboard-overview",
),
]