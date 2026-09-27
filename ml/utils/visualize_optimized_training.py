import os
import pandas as pd
import matplotlib.pyplot as plt


HISTORY_PATH = os.path.join(
    "results",
    "reports",
    "final_optimized_history.csv"
)

OUTPUT_DIR = os.path.join(
    "results",
    "training_curves"
)


def main():

    print("=" * 70)
    print("OPTIMIZED TRAINING CURVES")
    print("=" * 70)

    print("\nLoading training history...")

    if not os.path.exists(HISTORY_PATH):
        raise FileNotFoundError(
            f"Training history not found: {HISTORY_PATH}"
        )

    history = pd.read_csv(HISTORY_PATH)

    print("Training history loaded successfully.")

    # Create epoch numbers because CSV does not contain an epoch column
    history["epoch"] = range(1, len(history) + 1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # =========================================================
    # ACCURACY CURVE
    # =========================================================

    plt.figure(figsize=(10, 6))

    plt.plot(
        history["epoch"],
        history["accuracy"],
        label="Training Accuracy"
    )

    plt.plot(
        history["epoch"],
        history["val_accuracy"],
        label="Validation Accuracy"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Optimized Retinal CNN - Accuracy")

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    accuracy_path = os.path.join(
        OUTPUT_DIR,
        "optimized_accuracy.png"
    )

    plt.savefig(
        accuracy_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nSaved accuracy curve:")
    print(accuracy_path)

    # =========================================================
    # LOSS CURVE
    # =========================================================

    plt.figure(figsize=(10, 6))

    plt.plot(
        history["epoch"],
        history["loss"],
        label="Training Loss"
    )

    plt.plot(
        history["epoch"],
        history["val_loss"],
        label="Validation Loss"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Optimized Retinal CNN - Loss")

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    loss_path = os.path.join(
        OUTPUT_DIR,
        "optimized_loss.png"
    )

    plt.savefig(
        loss_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nSaved loss curve:")
    print(loss_path)

    # =========================================================
    # SUMMARY
    # =========================================================

    best_val_loss_epoch = (
        history["val_loss"].idxmin() + 1
    )

    best_val_accuracy_epoch = (
        history["val_accuracy"].idxmax() + 1
    )

    best_val_loss = history["val_loss"].min()
    best_val_accuracy = history["val_accuracy"].max()

    print("\n" + "=" * 70)
    print("TRAINING SUMMARY")
    print("=" * 70)

    print(
        f"Best validation loss epoch: "
        f"{best_val_loss_epoch}"
    )

    print(
        f"Best validation loss: "
        f"{best_val_loss:.4f}"
    )

    print(
        f"Best validation accuracy epoch: "
        f"{best_val_accuracy_epoch}"
    )

    print(
        f"Best validation accuracy: "
        f"{best_val_accuracy:.4f}"
    )

    print("\n" + "=" * 70)
    print("TRAINING CURVES COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()