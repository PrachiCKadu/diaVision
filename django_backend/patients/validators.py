from io import BytesIO

from django.core.exceptions import ValidationError
from PIL import Image


ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG"}
MAX_IMAGE_SIZE_MB = 10


def validate_retinal_image(image_file):
    """
    Validate an uploaded retinal image.

    Checks:
    - File size
    - Supported image format
    - Whether the file can actually be opened as an image
    """

    if image_file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Image size must not exceed {MAX_IMAGE_SIZE_MB} MB."
        )

    try:
        image = Image.open(BytesIO(image_file.read()))
        image.verify()
    except Exception:
        raise ValidationError(
            "Uploaded file is not a valid image."
        )
    finally:
        image_file.seek(0)

    image_file.seek(0)

    image = Image.open(image_file)

    if image.format not in ALLOWED_IMAGE_FORMATS:
        raise ValidationError(
            "Only JPEG and PNG images are allowed."
        )

    image_file.seek(0)