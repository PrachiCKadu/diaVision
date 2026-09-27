from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "dataset" / "metadata" / "train.csv"
IMAGE_DIR = PROJECT_ROOT / "dataset" / "raw" / "aptos2019" / "train_images"

SAMPLE_IDS = [
    "000c1434d8d7",
    "001639a390f0",
    "0024cdab0c19",
    "003f0afdcd15",
    "004396fa1430",
    "009c019a730a",
]


def find_retinal_bbox(image):
    """
    Detect the main retinal field and return its bounding box.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

    x, y, w, h = cv2.boundingRect(
        largest_contour,
    )

    return x, y, w, h


def crop_and_pad_to_square(image):
    """
    Crop the detected retinal field while preserving
    its aspect ratio, then pad the shorter dimension
    to create a square image.

    No image stretching is performed.
    """

    x, y, w, h = find_retinal_bbox(image)

    cropped = image[
        y:y + h,
        x:x + w,
    ]

    height, width = cropped.shape[:2]

    side = max(height, width)

    top = (side - height) // 2
    bottom = side - height - top

    left = (side - width) // 2
    right = side - width - left

    padded = cv2.copyMakeBorder(
        cropped,
        top,
        bottom,
        left,
        right,
        borderType=cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )

    return padded, x, y, w, h

def check_crop_retention(image):
    """
    Verify how much non-dark image content is retained
    inside the detected retinal bounding box.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    x, y, w, h = find_retinal_bbox(image)

    original_non_dark = gray >= 10

    cropped_gray = gray[
        y:y + h,
        x:x + w,
    ]

    cropped_non_dark = cropped_gray >= 10

    original_count = np.sum(original_non_dark)
    cropped_count = np.sum(cropped_non_dark)

    if original_count == 0:
        return 0.0

    retention = cropped_count / original_count

    return retention

df = pd.read_csv(CSV_PATH)

available_ids = set(df["id_code"].astype(str))

sample_ids = [
    image_id
    for image_id in SAMPLE_IDS
    if image_id in available_ids
]

if not sample_ids:
    raise ValueError(
        "None of the selected sample IDs were found "
        "in the training metadata."
    )


fig, axes = plt.subplots(
    len(sample_ids),
    2,
    figsize=(10, 4 * len(sample_ids)),
)


if len(sample_ids) == 1:
    axes = [axes]


for row_index, image_id in enumerate(sample_ids):

    image_path = IMAGE_DIR / f"{image_id}.png"

    image = cv2.imread(
        str(image_path)
    )

    retention = check_crop_retention(image)

    print(
        f"{image_id}: "
        f"retained non-dark pixels = "
        f"{retention * 100:.2f}%"
    )

    if image is None:
        raise FileNotFoundError(
            f"Could not read: {image_path}"
        )

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB,
    )

    cropped, x, y, w, h = crop_and_pad_to_square(image)

    cropped_rgb = cv2.cvtColor(
        cropped,
        cv2.COLOR_BGR2RGB,
    )

    axes[row_index][0].imshow(image_rgb)
    axes[row_index][0].set_title(
        f"Original: {image_id}"
    )
    axes[row_index][0].axis("off")

    axes[row_index][1].imshow(cropped_rgb)
    axes[row_index][1].set_title(
        f"Crop + aspect-ratio-preserving padding\n"
        f"x={x}, y={y}, w={w}, h={h}"
    )
    axes[row_index][1].axis("off")


plt.tight_layout()

output_dir = PROJECT_ROOT / "results" / "training_curves"
output_dir.mkdir(
    parents=True,
    exist_ok=True,
)

output_path = (
    output_dir /
    "retinal_crop_diagnostic.png"
)

plt.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight",
)

plt.show()

print()
print("=" * 60)
print("RETINAL CROP DIAGNOSTIC")
print("=" * 60)
print(f"Saved visualization to:")
print(output_path)
print("=" * 60)