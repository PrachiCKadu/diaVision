from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_STATE = 42

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "dataset" / "raw" / "aptos2019"
METADATA_DIR = BASE_DIR / "dataset" / "metadata"

CSV_PATH = DATA_DIR / "train.csv"

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_csv(CSV_PATH)

print(f"Total samples: {len(df)}")


# ============================================================
# VALIDATION
# ============================================================

required_columns = {"id_code", "diagnosis"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        f"CSV must contain columns: {required_columns}"
    )

if df["id_code"].duplicated().any():
    raise ValueError("Duplicate image IDs found.")

if not df["diagnosis"].isin([0, 1, 2, 3, 4]).all():
    raise ValueError("Unexpected diagnosis labels found.")


# ============================================================
# CHECK IMAGE FILES
# ============================================================

image_dir = DATA_DIR / "train_images"

missing_images = []

for image_id in df["id_code"]:
    image_path = image_dir / f"{image_id}.png"

    if not image_path.exists():
        missing_images.append(image_id)

if missing_images:
    raise FileNotFoundError(
        f"{len(missing_images)} images are missing."
    )

print("Image validation: PASSED")


# ============================================================
# TRAIN + TEMP SPLIT
# ============================================================

train_df, temp_df = train_test_split(
    df,
    test_size=(1 - TRAIN_RATIO),
    stratify=df["diagnosis"],
    random_state=RANDOM_STATE,
)


# ============================================================
# VALIDATION + TEST SPLIT
# ============================================================

relative_test_ratio = TEST_RATIO / (VALIDATION_RATIO + TEST_RATIO)

val_df, test_df = train_test_split(
    temp_df,
    test_size=relative_test_ratio,
    stratify=temp_df["diagnosis"],
    random_state=RANDOM_STATE,
)


# ============================================================
# SAVE METADATA
# ============================================================

METADATA_DIR.mkdir(parents=True, exist_ok=True)

train_path = METADATA_DIR / "train.csv"
val_path = METADATA_DIR / "validation.csv"
test_path = METADATA_DIR / "test.csv"

train_df.to_csv(train_path, index=False)
val_df.to_csv(val_path, index=False)
test_df.to_csv(test_path, index=False)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("DATASET SPLIT COMPLETE")
print("=" * 60)

print(f"\nTrain      : {len(train_df)}")
print(f"Validation : {len(val_df)}")
print(f"Test       : {len(test_df)}")
print(f"Total      : {len(train_df) + len(val_df) + len(test_df)}")

print("\nTrain distribution:")
print(train_df["diagnosis"].value_counts().sort_index())

print("\nValidation distribution:")
print(val_df["diagnosis"].value_counts().sort_index())

print("\nTest distribution:")
print(test_df["diagnosis"].value_counts().sort_index())

print("\nFiles saved:")
print(train_path)
print(val_path)
print(test_path)

print("\nRandom seed:", RANDOM_STATE)