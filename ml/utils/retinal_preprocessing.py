import cv2
import numpy as np


def find_retinal_bbox(image: np.ndarray) -> tuple[int, int, int, int]:
    """
    Detect the main retinal field and return its bounding box.

    Returns:
        x, y, width, height
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY,
    )

    _, mask = cv2.threshold(
        gray,
        10,
        255,
        cv2.THRESH_BINARY,
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (15, 15),
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    if not contours:
        height, width = image.shape[:2]
        return 0, 0, width, height

    largest_contour = max(
        contours,
        key=cv2.contourArea,
    )

    x, y, width, height = cv2.boundingRect(
        largest_contour,
    )

    return x, y, width, height


def crop_and_pad_to_square(
    image: np.ndarray,
) -> np.ndarray:
    """
    Crop the detected retinal field and pad the shorter
    dimension to produce a square image.

    The retinal image is not stretched or geometrically
    distorted.
    """

    x, y, width, height = find_retinal_bbox(image)

    cropped = image[
        y:y + height,
        x:x + width,
    ]

    crop_height, crop_width = cropped.shape[:2]

    side = max(
        crop_height,
        crop_width,
    )

    top = (side - crop_height) // 2
    bottom = side - crop_height - top

    left = (side - crop_width) // 2
    right = side - crop_width - left

    padded = cv2.copyMakeBorder(
        cropped,
        top,
        bottom,
        left,
        right,
        borderType=cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )

    return padded