from django.urls import path


from .views import (
    home,
    patient_dashboard,
    patient_upload,
    admin_dashboard,
    patient_prediction_result,
    doctor_dashboard,
    doctor_case_detail,
)

urlpatterns = [
    path(
    "",
    home,
    name="home",
    ),
    path(
        "patient/dashboard/",
        patient_dashboard,
        name="patient-dashboard",
    ),
    path("patient/upload/", patient_upload, name="patient-upload"),

    path(
        "patient/prediction/<int:retinal_image_id>/",
        patient_prediction_result,
        name="patient-prediction-result",
    ),


    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin-dashboard",
    ),
    path(
    "doctor/dashboard/",
    doctor_dashboard,
    name="doctor-dashboard",
    ),
    path(
    "doctor/cases/<int:retinal_image_id>/",
    doctor_case_detail,
    name="doctor-case-detail-page",
),


]