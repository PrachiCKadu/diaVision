from pathlib import Path
import sys

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


# --------------------------------------------------
# Project Root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Imports
# --------------------------------------------------

from ml.utils.dataset_loader import create_dataset


# --------------------------------------------------
# Configuration
# --------------------------------------------------

TEST_CSV = (
    PROJECT_ROOT
    / "dataset"
    / "metadata"
    / "test.csv"
)

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
    / "baseline"
    / "baseline_cnn.keras"
)

REPORT_DIR = (
    PROJECT_ROOT
    / "results"
    / "reports"
)

CONFUSION_DIR = (
    PROJECT_ROOT
    / "results"
    / "confusion_matrix"
)

BATCH_SIZE = 32


CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR",
]


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("BASELINE MODEL TEST EVALUATION")
    print("=" * 60)

    # --------------------------------------------------
    # Load test dataset
    # --------------------------------------------------

    print("\nLoading test dataset...")

    test_dataset = create_dataset(
        TEST_CSV,
        IMAGE_DIR,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    print("Test dataset loaded successfully.")

    # --------------------------------------------------
    # Load best baseline model
    # --------------------------------------------------

    print("\nLoading best baseline model...")

    model = tf.keras.models.load_model(MODEL_PATH)

    print("Model loaded successfully.")

    # --------------------------------------------------
    # Collect predictions
    # --------------------------------------------------

    print("\nGenerating predictions...")

    y_true = []
    y_pred = []

    for images, labels in test_dataset:

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

    print(f"Test samples evaluated: {len(y_true)}")

    # --------------------------------------------------
    # Overall metrics
    # --------------------------------------------------

    accuracy = accuracy_score(
        y_true,
        y_pred,
    )

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

    # --------------------------------------------------
    # Print overall metrics
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("OVERALL TEST RESULTS")
    print("=" * 60)

    print(f"Accuracy         : {accuracy:.4f}")
    print(f"Macro Precision  : {macro_precision:.4f}")
    print(f"Macro Recall     : {macro_recall:.4f}")
    print(f"Macro F1         : {macro_f1:.4f}")
    print(f"Weighted F1      : {weighted_f1:.4f}")

    # --------------------------------------------------
    # Classification report
    # --------------------------------------------------

    report = classification_report(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3, 4],
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0,
    )

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)

    print(report)

    # --------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1, 2, 3, 4],
    )

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    print(cm)

    # --------------------------------------------------
    # Save metrics
    # --------------------------------------------------

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_path = (
        REPORT_DIR
        / "baseline_test_metrics.txt"
    )

    with open(
        metrics_path,
        "w",
        encoding="utf-8",
    ) as f:

        f.write("BASELINE MODEL TEST EVALUATION\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(
            f"Macro Precision: {macro_precision:.4f}\n"
        )
        f.write(
            f"Macro Recall: {macro_recall:.4f}\n"
        )
        f.write(
            f"Macro F1: {macro_f1:.4f}\n"
        )
        f.write(
            f"Weighted F1: {weighted_f1:.4f}\n"
        )

        f.write("\n\nCLASSIFICATION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(report)

        f.write("\nCONFUSION MATRIX\n")
        f.write("=" * 60 + "\n")
        f.write(str(cm))

    # --------------------------------------------------
    # Save confusion matrix CSV
    # --------------------------------------------------

    CONFUSION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cm_df = pd.DataFrame(
        cm,
        index=CLASS_NAMES,
        columns=CLASS_NAMES,
    )

    cm_path = (
        CONFUSION_DIR
        / "baseline_confusion_matrix.csv"
    )

    cm_df.to_csv(cm_path)

    # --------------------------------------------------
    # Complete
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("BASELINE TEST EVALUATION COMPLETE")
    print("=" * 60)

    print("\nMetrics saved to:")
    print(metrics_path)

    print("\nConfusion matrix saved to:")
    print(cm_path)


if __name__ == "__main__":
    main()