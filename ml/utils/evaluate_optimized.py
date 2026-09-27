import tensorflow as tf
import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

from ml.utils.dataset_loader_retinal import create_dataset


# ============================================================
# PATHS
# ============================================================

ROOT = Path(".")

MODEL_PATH = (
    ROOT
    / "models"
    / "optimized"
    / "final_optimized_retinal_cnn.keras"
)

VAL_CSV = (
    ROOT
    / "dataset"
    / "metadata"
    / "validation.csv"
)

IMAGE_DIR = (
    ROOT
    / "dataset"
    / "raw"
    / "aptos2019"
    / "train_images"
)

REPORT_DIR = (
    ROOT
    / "results"
    / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONFIG
# ============================================================

BATCH_SIZE = 16

CLASS_NAMES = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR",
}


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("OPTIMIZED RETINAL CNN EVALUATION")
print("=" * 70)

print("\nLoading optimized model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model loaded successfully.")


# ============================================================
# LOAD VALIDATION DATA
# ============================================================

print("\nLoading validation dataset...")

val_ds = create_dataset(
    VAL_CSV,
    IMAGE_DIR,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print("Validation dataset loaded successfully.")


# ============================================================
# PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

y_true = []
y_pred = []

for images, labels in val_ds:

    predictions = model.predict(
        images,
        verbose=0,
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1,
    )

    y_true.extend(
        labels.numpy()
    )

    y_pred.extend(
        predicted_classes
    )


y_true = np.array(y_true)
y_pred = np.array(y_pred)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_true,
    y_pred,
)

print("\n" + "=" * 70)
print("OVERALL PERFORMANCE")
print("=" * 70)

print(
    f"\nValidation Accuracy: {accuracy:.4f}"
)

print(
    f"Validation Accuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

report = classification_report(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3, 4],
    target_names=[
        CLASS_NAMES[i]
        for i in range(5)
    ],
    digits=4,
    zero_division=0,
)

print("\n")
print(report)


# ============================================================
# SAVE CLASSIFICATION REPORT
# ============================================================

report_path = (
    REPORT_DIR
    / "optimized_classification_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8",
) as file:

    file.write(
        "OPTIMIZED RETINAL CNN\n"
    )

    file.write(
        "=" * 70
        + "\n\n"
    )

    file.write(
        f"Validation Accuracy: "
        f"{accuracy:.4f}\n\n"
    )

    file.write(
        report
    )


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3, 4],
)

cm_df = pd.DataFrame(
    cm,
    index=[
        CLASS_NAMES[i]
        for i in range(5)
    ],
    columns=[
        CLASS_NAMES[i]
        for i in range(5)
    ],
)

cm_path = (
    REPORT_DIR
    / "optimized_confusion_matrix.csv"
)

cm_df.to_csv(
    cm_path
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)

print(
    "\nClassification report:"
)

print(
    report_path
)

print(
    "\nConfusion matrix:"
)

print(
    cm_path
)