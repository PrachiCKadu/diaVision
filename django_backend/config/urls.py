"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

def login_page(request):
    return render(request, "auth/login.html")

def register_page(request):
    return render(request, "auth/register.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path(
    "api/predictions/",
    include("predictions.urls"),
    ),
    path(
    "api/doctors/",
    include("doctors.urls"),
    ),
    path("", include("pages.urls")),
    path("login/", login_page, name="login-page"),
    path("register/", register_page, name="register-page"),
    path(
    "api/reports/",
    include("reports.urls"),
),
    
    path(
    "patient/dashboard/",
    lambda request: render(
        request,
        "patient/dashboard.html",
    ),
    name="patient-dashboard",
),

    
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)