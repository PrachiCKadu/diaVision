from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

HISTORY_PATH = (
    PROJECT_ROOT
    / "results"
    / "reports"
    / "baseline_history.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "training_curves"
)

OUTPUT_PATH = OUTPUT_DIR / "baseline_training_curves.png"


def main():

    history = pd.read_csv(HISTORY_PATH)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ----------------------------------------------
    # Accuracy
    # ----------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        history["accuracy"],
        label="Training Accuracy",
    )

    plt.plot(
        history["val_accuracy"],
        label="Validation Accuracy",
    )

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Baseline CNN Accuracy")

    plt.legend()
    plt.grid(True)

    accuracy_path = OUTPUT_DIR / "baseline_accuracy.png"

    plt.savefig(
        accuracy_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    # ----------------------------------------------
    # Loss
    # ----------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        history["loss"],
        label="Training Loss",
    )

    plt.plot(
        history["val_loss"],
        label="Validation Loss",
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Baseline CNN Loss")

    plt.legend()
    plt.grid(True)

    loss_path = OUTPUT_DIR / "baseline_loss.png"

    plt.savefig(
        loss_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    print("Training curves created successfully.")

    print(f"\nAccuracy curve:")
    print(accuracy_path)

    print(f"\nLoss curve:")
    print(loss_path)


if __name__ == "__main__":
    main()