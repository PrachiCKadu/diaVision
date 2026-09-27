import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from ml.inference import predictor
from ml.utils.gradcam_optimized import (
    generate_gradcam_for_image,
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "optimized"
    / "final_optimized_retinal_cnn.keras"
)

predictor.MODEL_PATH = str(MODEL_PATH)


def predict_retinal_image(image_path):
    """
    Run the existing retinal-disease predictor on an uploaded image.

    The existing predictor.py remains the single source of truth
    for image preprocessing and model inference.
    """

    image_path = Path(image_path).resolve()

    if not image_path.exists():
        raise FileNotFoundError(
            f"Retinal image not found: {image_path}"
        )

    return predictor.predict_image(str(image_path))

from .models import Prediction


def save_prediction(retinal_image, result):
    """
    Save an ML prediction for a retinal image.
    """

    probabilities = result["probabilities"]

    prediction, created = Prediction.objects.update_or_create(
        retinal_image=retinal_image,
        defaults={
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "no_dr_probability": probabilities["No DR"],
            "mild_probability": probabilities["Mild"],
            "moderate_probability": probabilities["Moderate"],
            "severe_probability": probabilities["Severe"],
            "proliferative_dr_probability": probabilities[
                "Proliferative DR"
            ],
        },
    )

    return prediction, created


def generate_retinal_gradcam(retinal_image, prediction):
    """
    Generate and persist Grad-CAM visualization for a prediction.
    """

    image_path = Path(
        retinal_image.image.path
    ).resolve()

    if not image_path.exists():
        raise FileNotFoundError(
            f"Retinal image not found: {image_path}"
        )

    class_index = predictor.CLASS_NAMES.index(
        prediction.predicted_class
    )

    result = generate_gradcam_for_image(
        image_path=image_path,
        predicted_index=class_index,
        predicted_class=prediction.predicted_class,
        confidence=prediction.confidence,
    )

    gradcam_path = Path(
        result["gradcam_path"]
    ).resolve()

    if not gradcam_path.exists():
        raise FileNotFoundError(
            f"Grad-CAM output not found: {gradcam_path}"
        )

    with gradcam_path.open("rb") as gradcam_file:
        prediction.gradcam_image.save(
            gradcam_path.name,
            gradcam_file,
            save=True,
        )

    result["stored_gradcam"] = prediction.gradcam_image.name

    return result