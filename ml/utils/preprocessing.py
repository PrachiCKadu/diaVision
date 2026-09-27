from pathlib import Path
import numpy as np
from PIL import Image


# --------------------------------------------------
# Configuration
# --------------------------------------------------

IMAGE_SIZE = (224, 224)


# --------------------------------------------------
# Image Loading
# --------------------------------------------------

def load_image(image_path: str | Path) -> Image.Image:
    """
    Load a retinal image and convert it to RGB.
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")

    return image


# --------------------------------------------------
# Image Resizing
# --------------------------------------------------

def resize_image(
    image: Image.Image,
    image_size: tuple[int, int] = IMAGE_SIZE
) -> Image.Image:
    """
    Resize image to the required model input size.
    """
    return image.resize(image_size)


# --------------------------------------------------
# NumPy Conversion + Normalization
# --------------------------------------------------

def image_to_array(image: Image.Image) -> np.ndarray:
    """
    Convert PIL image to float32 NumPy array
    and normalize pixel values from [0, 255] to [0, 1].
    """
    image_array = np.asarray(image, dtype=np.float32)

    image_array /= 255.0

    return image_array


# --------------------------------------------------
# Complete Preprocessing Pipeline
# --------------------------------------------------

def preprocess_image(
    image_path: str | Path,
    image_size: tuple[int, int] = IMAGE_SIZE
) -> np.ndarray:
    """
    Complete deterministic preprocessing pipeline:

    Image
      -> RGB
      -> Resize
      -> NumPy array
      -> Normalize [0, 1]
    """
    image = load_image(image_path)
    image = resize_image(image, image_size)
    image_array = image_to_array(image)

    return image_array