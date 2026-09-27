from django.core.serializers import python
from django.shortcuts import render


def patient_dashboard(request):
    return render(
        request,
        "patient/dashboard.html",
    )

def admin_dashboard(request):
    return render(
        request,
        "admin_dashboard/dashboard.html",
    )

def doctor_dashboard(request):
    return render(
        request,
        "doctor/dashboard.html",
    )

def home(request):
    return render(
        request,
"home/home.html",
    )


def doctor_case_detail(request, retinal_image_id):
    return render(
        request,
        "doctor/case_detail.html",
        {
            "retinal_image_id": retinal_image_id,
        },
    )


def patient_upload(request):
    return render(request, "patient/upload.html")

def patient_prediction_result(request, retinal_image_id):
    return render(
        request,
        "patient/prediction_result.html",
        {
            "retinal_image_id": retinal_image_id,
            "retinal_image_url": "",
        },
    )
