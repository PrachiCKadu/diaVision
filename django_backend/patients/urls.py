from django.urls import path

from .views import RetinalImageUploadView


urlpatterns = [
    path(
        "upload/",
        RetinalImageUploadView.as_view(),
        name="retinal-image-upload",
    ),
]