from pathlib import Path

import cv2
import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "dataset" / "metadata" / "train.csv"
IMAGE_DIR = PROJECT_ROOT / "dataset" / "raw" / "aptos2019" / "train_images"

SAMPLE_SIZE = 200


# ---------------------------------------------------------
# Load training metadata
# ---------------------------------------------------------

df = pd.read_csv(CSV_PATH)

if df.empty:
    raise ValueError("Training CSV is empty.")

sample_df = df.sample(
    n=min(SAMPLE_SIZE, len(df)),
    random_state=42,
)


# ---------------------------------------------------------
# Analyze images
# ---------------------------------------------------------

black_border_ratios = []
brightness_values = []
contrast_values = []
image_sizes = []

failed_images = []

for _, row in sample_df.iterrows():

    image_id = row["id_code"]
    image_path = IMAGE_DIR / f"{image_id}.png"

    image = cv2.imread(
        str(image_path),
        cv2.IMREAD_GRAYSCALE,
    )

    if image is None:
        failed_images.append(str(image_path))
        continue

    height, width = image.shape

    image_sizes.append((width, height))

    # Pixels below this threshold are considered
    # effectively black for this diagnostic.
    black_pixels = np.sum(image < 10)

    total_pixels = image.size

    black_ratio = black_pixels / total_pixels

    black_border_ratios.append(black_ratio)

    # Statistics are calculated only on non-black pixels
    # to better represent the retinal region.
    retinal_pixels = image[image >= 10]

    if len(retinal_pixels) > 0:
        brightness_values.append(
            float(np.mean(retinal_pixels))
        )

        contrast_values.append(
            float(np.std(retinal_pixels))
        )


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

print("=" * 60)
print("RETINAL IMAGE PREPROCESSING ANALYSIS")
print("=" * 60)

print(f"Images requested: {len(sample_df)}")
print(f"Images analyzed:  {len(black_border_ratios)}")
print(f"Failed images:    {len(failed_images)}")

print()

if black_border_ratios:

    print("BLACK / DARK PIXEL ANALYSIS")
    print("-" * 60)

    print(
        f"Mean dark-pixel ratio: "
        f"{np.mean(black_border_ratios):.4f}"
    )

    print(
        f"Median dark-pixel ratio: "
        f"{np.median(black_border_ratios):.4f}"
    )

    print(
        f"Minimum dark-pixel ratio: "
        f"{np.min(black_border_ratios):.4f}"
    )

    print(
        f"Maximum dark-pixel ratio: "
        f"{np.max(black_border_ratios):.4f}"
    )

print()

if brightness_values:

    print("RETINAL BRIGHTNESS")
    print("-" * 60)

    print(
        f"Mean brightness: "
        f"{np.mean(brightness_values):.2f}"
    )

    print(
        f"Brightness std: "
        f"{np.std(brightness_values):.2f}"
    )

    print(
        f"Minimum brightness: "
        f"{np.min(brightness_values):.2f}"
    )

    print(
        f"Maximum brightness: "
        f"{np.max(brightness_values):.2f}"
    )

print()

if contrast_values:

    print("RETINAL CONTRAST")
    print("-" * 60)

    print(
        f"Mean contrast: "
        f"{np.mean(contrast_values):.2f}"
    )

    print(
        f"Contrast std: "
        f"{np.std(contrast_values):.2f}"
    )

    print(
        f"Minimum contrast: "
        f"{np.min(contrast_values):.2f}"
    )

    print(
        f"Maximum contrast: "
        f"{np.max(contrast_values):.2f}"
    )

print()

if image_sizes:

    unique_sizes = sorted(set(image_sizes))

    print("IMAGE DIMENSIONS")
    print("-" * 60)

    print(f"Unique dimensions in sample: {len(unique_sizes)}")

    for size in unique_sizes[:20]:
        print(f"  {size[0]} x {size[1]}")

print()

if failed_images:

    print("FAILED IMAGES")
    print("-" * 60)

    for path in failed_images[:10]:
        print(path)

print("=" * 60)