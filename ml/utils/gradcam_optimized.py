from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT
    / "models"
    / "optimized"
    / "final_optimized_retinal_cnn.keras"
)

IMAGE_DIR = (
    ROOT
    / "dataset"
    / "raw"
    / "aptos2019"
    / "train_images"
)

OUTPUT_DIR = (
    ROOT
    / "results"
    / "gradcam"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR",
]


# ============================================================
# FIND SAMPLE IMAGE
# ============================================================

def find_sample_image():
    """
    Find the first supported retinal image
    from the training image directory.
    """

    extensions = [
        "*.png",
        "*.jpg",
        "*.jpeg",
    ]

    for extension in extensions:
        images = sorted(IMAGE_DIR.glob(extension))

        if images:
            return images[0]

    raise FileNotFoundError(
        f"No retinal images found in:\n{IMAGE_DIR}"
    )


# ============================================================
# LOAD AND PREPROCESS IMAGE
# ============================================================

def load_image(image_path):
    """
    Load retinal image and preprocess it
    using the same 224x224 RGB scaling
    used by the model.
    """

    image = cv2.imread(
        str(image_path)
    )

    if image is None:
        raise ValueError(
            f"Unable to read image:\n{image_path}"
        )

    # OpenCV BGR -> RGB
    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB,
    )

    # Resize
    resized = cv2.resize(
        image_rgb,
        IMAGE_SIZE,
    )

    # Normalize to [0, 1]
    normalized = (
        resized.astype(np.float32) / 255.0
    )

    # Add batch dimension
    input_tensor = np.expand_dims(
        normalized,
        axis=0,
    )

    return image_rgb, normalized, input_tensor


# ============================================================
# FIND LAST CONVOLUTIONAL LAYER
# ============================================================

def find_last_conv_layer(model):
    """
    Locate the last Conv2D layer in the model.
    """

    for layer in reversed(model.layers):

        if isinstance(
            layer,
            tf.keras.layers.Conv2D,
        ):
            return layer.name

    raise ValueError(
        "No Conv2D layer found in model."
    )


# ============================================================
# GRAD-CAM
# ============================================================

def generate_gradcam(
    model,
    input_tensor,
    layer_name,
    class_index,
):
    """
    Generate Grad-CAM heatmap for the
    requested prediction class.
    """

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(layer_name).output,
            model.output,
        ],
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = (
            grad_model(input_tensor)
        )

        class_score = predictions[
            :, class_index
        ]

    gradients = tape.gradient(
        class_score,
        conv_outputs,
    )

    # Average gradients over spatial dimensions
    pooled_gradients = tf.reduce_mean(
        gradients,
        axis=(1, 2),
    )

    conv_outputs = conv_outputs[0]

    pooled_gradients = pooled_gradients[0]

    # Weight feature maps
    heatmap = tf.reduce_sum(
        conv_outputs
        * pooled_gradients,
        axis=-1,
    )

    # ReLU
    heatmap = tf.maximum(
        heatmap,
        0,
    )

    # Normalize
    max_value = tf.reduce_max(
        heatmap
    )

    heatmap = tf.where(
        max_value > 0,
        heatmap / max_value,
        heatmap,
    )

    return heatmap.numpy()


# ============================================================
# CREATE OVERLAY
# ============================================================

def create_overlay(
    original_image,
    heatmap,
):
    """
    Resize Grad-CAM heatmap and overlay it
    on the original retinal image.
    """

    height, width = (
        original_image.shape[:2]
    )

    heatmap_resized = cv2.resize(
        heatmap,
        (width, height),
    )

    heatmap_uint8 = np.uint8(
        255 * heatmap_resized
    )

    colored_heatmap = cv2.applyColorMap(
        heatmap_uint8,
        cv2.COLORMAP_JET,
    )

    original_bgr = cv2.cvtColor(
        original_image,
        cv2.COLOR_RGB2BGR,
    )

    overlay = cv2.addWeighted(
        original_bgr,
        0.60,
        colored_heatmap,
        0.40,
        0,
    )

    return overlay


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    original_image,
    overlay,
    image_path,
    predicted_class,
    confidence,
):
    """
    Save original retinal image and
    Grad-CAM visualization.
    """

    image_name = image_path.stem

    original_output = (
        OUTPUT_DIR
        / f"{image_name}_original.jpg"
    )

    gradcam_output = (
        OUTPUT_DIR
        / f"{image_name}_gradcam.jpg"
    )

    cv2.imwrite(
        str(original_output),
        cv2.cvtColor(
            original_image,
            cv2.COLOR_RGB2BGR,
        ),
    )

    cv2.imwrite(
        str(gradcam_output),
        overlay,
    )

    print("\nSaved original image:")
    print(original_output)

    print("\nSaved Grad-CAM image:")
    print(gradcam_output)


# ============================================================
# REUSABLE GRAD-CAM FUNCTION
# ============================================================

def generate_gradcam_for_image(
    image_path,
    predicted_index,
    predicted_class,
    confidence,
):
    """
    Generate and save Grad-CAM for a specific retinal image.

    This function reuses the existing Grad-CAM implementation
    and is intended for Django/backend integration.
    """

    image_path = Path(image_path).resolve()

    if not image_path.exists():
        raise FileNotFoundError(
            f"Retinal image not found:\n{image_path}"
        )

    # Load model
    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    # Find target convolutional layer
    last_conv_layer = find_last_conv_layer(
        model
    )

    # Load and preprocess image
    original_image, processed_image, input_tensor = (
        load_image(image_path)
    )

    # Generate Grad-CAM
    heatmap = generate_gradcam(
        model=model,
        input_tensor=input_tensor,
        layer_name=last_conv_layer,
        class_index=predicted_index,
    )

    # Create visualization
    overlay = create_overlay(
        original_image,
        heatmap,
    )

    # Save results
    save_results(
        original_image=original_image,
        overlay=overlay,
        image_path=image_path,
        predicted_class=predicted_class,
        confidence=confidence,
    )

    gradcam_output = (
        OUTPUT_DIR
        / f"{image_path.stem}_gradcam.jpg"
    )

    return {
        "gradcam_path": str(gradcam_output),
        "layer_name": last_conv_layer,
        "predicted_class": predicted_class,
        "confidence": float(confidence),
    }

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("OPTIMIZED RETINAL CNN - GRAD-CAM")
    print("=" * 70)

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    print("\nLoading optimized model...")

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    # --------------------------------------------------------
    # FIND CONVOLUTIONAL LAYER
    # --------------------------------------------------------

    last_conv_layer = find_last_conv_layer(
        model
    )

    print(
        "\nLast convolutional layer:",
        last_conv_layer,
    )

    # --------------------------------------------------------
    # FIND SAMPLE IMAGE
    # --------------------------------------------------------

    image_path = find_sample_image()

    print(
        "\nSample retinal image:",
        image_path,
    )

    # --------------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------------

    original_image, processed_image, input_tensor = (
        load_image(image_path)
    )

    print(
        "\nImage preprocessing complete."
    )

    print(
        "Processed image shape:",
        processed_image.shape,
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    print(
        "\nGenerating prediction..."
    )

    predictions = model.predict(
        input_tensor,
        verbose=0,
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    # --------------------------------------------------------
    # DISPLAY PREDICTION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PREDICTION")
    print("=" * 70)

    print(
        "\nPredicted class:",
        predicted_class,
    )

    print(
        "Confidence:",
        f"{confidence * 100:.2f}%",
    )

    print("\nClass probabilities:")

    for class_name, probability in zip(
        CLASS_NAMES,
        predictions,
    ):

        print(
            f"{class_name:20s}: "
            f"{probability * 100:.2f}%"
        )

    # --------------------------------------------------------
    # GENERATE GRAD-CAM
    # --------------------------------------------------------

    print(
        "\nGenerating Grad-CAM..."
    )

    heatmap = generate_gradcam(
        model=model,
        input_tensor=input_tensor,
        layer_name=last_conv_layer,
        class_index=predicted_index,
    )

    print(
        "Grad-CAM heatmap generated successfully."
    )

    # --------------------------------------------------------
    # CREATE OVERLAY
    # --------------------------------------------------------

    overlay = create_overlay(
        original_image,
        heatmap,
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_results(
        original_image=original_image,
        overlay=overlay,
        image_path=image_path,
        predicted_class=predicted_class,
        confidence=confidence,
    )

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("GRAD-CAM GENERATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()