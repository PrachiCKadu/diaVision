from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from ml.utils.dataset_loader_retinal import create_dataset


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_CSV = PROJECT_ROOT / "dataset" / "metadata" / "test.csv"

IMAGE_DIR = (
    PROJECT_ROOT
    / "dataset"
    / "raw"
    / "aptos2019"
    / "train_images"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "optimized"
    / "retinal_experiment_cnn.keras"
)

REPORT_DIR = PROJECT_ROOT / "results" / "reports"
CONFUSION_DIR = PROJECT_ROOT / "results" / "confusion_matrix"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CONFUSION_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

BATCH_SIZE = 32

CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR",
]


# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("RETINAL EXPERIMENT — TEST EVALUATION")
print("=" * 60)

print("\nChecking required files...")

if not TEST_CSV.exists():
    raise FileNotFoundError(f"Test CSV not found: {TEST_CSV}")

if not IMAGE_DIR.exists():
    raise FileNotFoundError(f"Image directory not found: {IMAGE_DIR}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print("Test CSV:", TEST_CSV)
print("Image directory:", IMAGE_DIR)
print("Model:", MODEL_PATH)

# ============================================================
# LOAD TEST DATASET
# ============================================================

print("\nLoading test dataset...")

test_ds = create_dataset(
    str(TEST_CSV),
    str(IMAGE_DIR),
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print("Test dataset loaded successfully.")

# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading retinal experiment model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")

# ============================================================
# PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

y_true = []
y_pred = []

for images, labels in test_ds:
    predictions = model.predict(images, verbose=0)

    predicted_classes = np.argmax(predictions, axis=1)

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_classes)

y_true = np.array(y_true)
y_pred = np.array(y_pred)

print("Predictions generated.")
print("Test samples:", len(y_true))

# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

macro_precision = precision_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

macro_recall = recall_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

macro_f1 = f1_score(
    y_true,
    y_pred,
    average="macro",
    zero_division=0,
)

weighted_f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0,
)

report = classification_report(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3, 4],
    target_names=CLASS_NAMES,
    zero_division=0,
)

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3, 4],
)

# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 60)
print("RETINAL EXPERIMENT TEST RESULTS")
print("=" * 60)

print(f"Accuracy:         {accuracy:.4f}")
print(f"Macro Precision:  {macro_precision:.4f}")
print(f"Macro Recall:     {macro_recall:.4f}")
print(f"Macro F1:         {macro_f1:.4f}")
print(f"Weighted F1:      {weighted_f1:.4f}")

print("\nClassification Report:")
print(report)

print("Confusion Matrix:")
print(cm)

# ============================================================
# SAVE METRICS REPORT
# ============================================================

metrics_path = REPORT_DIR / "retinal_experiment_test_metrics.txt"

with open(metrics_path, "w", encoding="utf-8") as f:
    f.write("RETINAL EXPERIMENT TEST RESULTS\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Test samples: {len(y_true)}\n")
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Macro Precision: {macro_precision:.4f}\n")
    f.write(f"Macro Recall: {macro_recall:.4f}\n")
    f.write(f"Macro F1: {macro_f1:.4f}\n")
    f.write(f"Weighted F1: {weighted_f1:.4f}\n\n")

    f.write("Classification Report\n")
    f.write("=" * 60 + "\n")
    f.write(report)

    f.write("\nConfusion Matrix\n")
    f.write("=" * 60 + "\n")
    f.write(np.array2string(cm))

# ============================================================
# SAVE CONFUSION MATRIX
# ============================================================

cm_path = CONFUSION_DIR / "retinal_experiment_confusion_matrix.csv"

cm_df = pd.DataFrame(
    cm,
    index=CLASS_NAMES,
    columns=CLASS_NAMES,
)

cm_df.to_csv(cm_path)

# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("FILES SAVED")
print("=" * 60)

print(metrics_path)
print(cm_path)

print("\nRetinal experiment test evaluation completed successfully.")