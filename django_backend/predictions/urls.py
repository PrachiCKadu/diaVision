from django.urls import path

from .views import (
    PatientPredictionDetailView,
    PatientPredictionHistoryView,
)

urlpatterns = [
    path(
        "patient/history/",
        PatientPredictionHistoryView.as_view(),
        name="patient-prediction-history",
    ),
    path(
        "patient/<int:retinal_image_id>/",
        PatientPredictionDetailView.as_view(),
        name="patient-prediction-detail",
    ),
]