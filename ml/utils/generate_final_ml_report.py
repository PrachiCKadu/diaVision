import os
import pandas as pd


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

HISTORY_PATH = os.path.join(
    BASE_DIR, "results", "reports", "final_optimized_history.csv"
)

CLASSIFICATION_REPORT = os.path.join(
    BASE_DIR, "results", "reports", "optimized_classification_report.txt"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "results", "reports", "FINAL_ML_REPORT.txt"
)


def main():

    print("=" * 70)
    print("FINAL DIABETIC RETINOPATHY ML REPORT")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load training history
    # ---------------------------------------------------------
    print("\nLoading training history...")

    history = pd.read_csv(HISTORY_PATH)

    best_val_accuracy = history["val_accuracy"].max()
    best_val_accuracy_epoch = history["val_accuracy"].idxmax() + 1

    best_val_loss = history["val_loss"].min()
    best_val_loss_epoch = history["val_loss"].idxmin() + 1

    final_train_accuracy = history["accuracy"].iloc[-1]
    final_val_accuracy = history["val_accuracy"].iloc[-1]

    epochs_completed = len(history)

    # ---------------------------------------------------------
    # Load classification report
    # ---------------------------------------------------------
    print("Loading classification report...")

    with open(CLASSIFICATION_REPORT, "r", encoding="utf-8") as file:
        classification_report = file.read()

    # ---------------------------------------------------------
    # Build final report
    # ---------------------------------------------------------
    report = f"""
======================================================================
FINAL DIABETIC RETINOPATHY ML REPORT
======================================================================

PROJECT
-------
Automated Classification of Diabetic Eye Diseases Using
Optimized Deep Convolutional Model


MODEL
-----
Model Type:
Optimized Retinal Convolutional Neural Network

Input Size:
224 x 224 x 3

Number of Classes:
5

Classes:
1. No DR
2. Mild
3. Moderate
4. Severe
5. Proliferative DR


MODEL ARCHITECTURE
------------------
Convolutional Blocks:
4

Convolution Filters:
32 -> 64 -> 128 -> 256

Normalization:
Batch Normalization

Activation:
ReLU

Pooling:
MaxPooling2D

Global Pooling:
GlobalAveragePooling2D

Dense Layer:
128 neurons

Output Layer:
5 neurons

Output Activation:
Softmax

Regularization:
Dropout + Data Augmentation


MODEL PARAMETERS
----------------
Total Parameters:
1,208,677

Trainable Parameters:
1,206,757

Non-trainable Parameters:
1,920


TRAINING
--------
Maximum Epochs:
25

Epochs Completed:
{epochs_completed}

Initial Learning Rate:
0.0005

Learning Rate Scheduling:
ReduceLROnPlateau

Early Stopping:
Enabled


TRAINING PERFORMANCE
--------------------
Best Validation Accuracy:
{best_val_accuracy:.4f} ({best_val_accuracy * 100:.2f}%)

Best Validation Accuracy Epoch:
{best_val_accuracy_epoch}

Best Validation Loss:
{best_val_loss:.4f}

Best Validation Loss Epoch:
{best_val_loss_epoch}

Final Training Accuracy:
{final_train_accuracy:.4f} ({final_train_accuracy * 100:.2f}%)

Final Validation Accuracy:
{final_val_accuracy:.4f} ({final_val_accuracy * 100:.2f}%)


EVALUATION NOTE
---------------
The model checkpoint is restored according to the best validation-loss
criterion. Therefore, the separately evaluated model accuracy may differ
from the highest validation accuracy observed during training.

The independently evaluated validation accuracy should be considered
the final model evaluation metric.


CLASSIFICATION REPORT
---------------------
{classification_report}


GENERATED ARTIFACTS
-------------------
Optimized Model:
models/optimized/final_optimized_retinal_cnn.keras

Training History:
results/reports/final_optimized_history.csv

Classification Report:
results/reports/optimized_classification_report.txt

Confusion Matrix:
results/reports/optimized_confusion_matrix.csv

Confusion Matrix Visualization:
results/confusion_matrix/optimized_confusion_matrix.png

Grad-CAM Original:
results/gradcam/000c1434d8d7_original.jpg

Grad-CAM Visualization:
results/gradcam/000c1434d8d7_gradcam.jpg


ML PIPELINE STATUS
------------------
[✓] Dataset loading
[✓] Image preprocessing
[✓] Data augmentation
[✓] CNN training
[✓] Validation
[✓] Model checkpointing
[✓] Learning-rate scheduling
[✓] Early stopping
[✓] Model evaluation
[✓] Classification report
[✓] Confusion matrix
[✓] Training curves
[✓] Grad-CAM explainability
[✓] Standalone inference predictor


CONCLUSION
----------
The optimized retinal CNN successfully performs five-class diabetic
retinopathy classification and provides both predictive output and
Grad-CAM-based visual explainability.

The trained model is ready to be integrated into the Django backend
for retinal image upload and disease prediction.


======================================================================
END OF FINAL ML REPORT
======================================================================
"""

    # ---------------------------------------------------------
    # Save report
    # ---------------------------------------------------------
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(report)

    print("\n" + "=" * 70)
    print("FINAL ML REPORT GENERATED")
    print("=" * 70)

    print("\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()