import os
import numpy as np
# import tensorflow as tf
from PIL import Image


MODEL_PATH = os.path.join(
    "models",
    "optimized",
    "final_optimized_retinal_cnn.keras"
)

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR"
]


def load_model():
    """Load the trained optimized retinal CNN."""

    import tensorflow as tf

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return tf.keras.models.load_model(MODEL_PATH)


def preprocess_image(image_path):
    """Preprocess retinal image for prediction."""
    image = Image.open(image_path).convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(image, dtype=np.float32)
    image_array = image_array / 255.0

    image_array = np.expand_dims(image_array, axis=0)

    return image_array


def predict_image(image_path):
    """
    Predict diabetic retinopathy class.

    Returns:
        dict containing predicted class,
        confidence and all class probabilities.
    """

    model = load_model()

    image = preprocess_image(image_path)

    predictions = model.predict(image, verbose=0)[0]

    predicted_index = int(np.argmax(predictions))
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(predictions[predicted_index])

    probabilities = {
        CLASS_NAMES[i]: float(predictions[i])
        for i in range(len(CLASS_NAMES))
    }

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities
    }


if __name__ == "__main__":
    print("=" * 70)
    print("RETINAL DISEASE PREDICTOR")
    print("=" * 70)

    sample_image = os.path.join(
        "dataset",
        "raw",
        "aptos2019",
        "train_images",
        "000c1434d8d7.png"
    )

    result = predict_image(sample_image)

    print("\nPrediction:")
    print(f"Class      : {result['predicted_class']}")
    print(f"Confidence : {result['confidence'] * 100:.2f}%")

    print("\nClass probabilities:")

    for class_name, probability in result["probabilities"].items():
        print(
            f"{class_name:<20}: "
            f"{probability * 100:.2f}%"
        )

    print("\n" + "=" * 70)