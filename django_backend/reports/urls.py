from django.urls import path

from .views import (
    MedicalReportDetailView,
    MedicalReportPDFView,
    MedicalReportGenerateView,
)


urlpatterns = [
    path(
        "<int:case_id>/",
        MedicalReportDetailView.as_view(),
        name="medical-report-detail",
    ),

    path(
        "<int:case_id>/pdf/",
        MedicalReportPDFView.as_view(),
        name="medical-report-pdf",
    ),
    path(
    "<int:case_id>/generate/",
    MedicalReportGenerateView.as_view(),
    name="medical-report-generate",
),
]