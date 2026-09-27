from pathlib import Path
import sys

import pandas as pd
import tensorflow as tf


# --------------------------------------------------
# Project Root / Import Path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Project Imports
# --------------------------------------------------

from ml.training.baseline_model import build_baseline_cnn
from ml.utils.dataset_loader import create_dataset
from ml.utils.class_weights import calculate_class_weights


# --------------------------------------------------
# Configuration
# --------------------------------------------------

TRAIN_CSV = PROJECT_ROOT / "dataset" / "metadata" / "train.csv"
VALIDATION_CSV = PROJECT_ROOT / "dataset" / "metadata" / "validation.csv"

IMAGE_DIR = (
    PROJECT_ROOT
    / "dataset"
    / "raw"
    / "aptos2019"
    / "train_images"
)

MODEL_DIR = PROJECT_ROOT / "models" / "baseline"
MODEL_PATH = MODEL_DIR / "baseline_cnn.keras"

HISTORY_PATH = (
    PROJECT_ROOT
    / "results"
    / "reports"
    / "baseline_history.csv"
)

BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 1e-3

SEED = 42


# --------------------------------------------------
# Reproducibility
# --------------------------------------------------

tf.keras.utils.set_random_seed(SEED)


# --------------------------------------------------
# Main Training Function
# --------------------------------------------------

def main():

    print("=" * 60)
    print("BASELINE MODEL TRAINING")
    print("=" * 60)

    # --------------------------------------------------
    # Load datasets
    # --------------------------------------------------

    print("\nLoading datasets...")

    train_dataset = create_dataset(
        TRAIN_CSV,
        IMAGE_DIR,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    validation_dataset = create_dataset(
        VALIDATION_CSV,
        IMAGE_DIR,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    print("Datasets loaded successfully.")

    # --------------------------------------------------
    # Calculate class weights
    # --------------------------------------------------

    class_weights = calculate_class_weights(TRAIN_CSV)

    print("\nClass weights:")

    for class_id, weight in class_weights.items():
        print(f"Class {class_id}: {weight:.4f}")

    # --------------------------------------------------
    # Build model
    # --------------------------------------------------

    print("\nBuilding model...")

    model = build_baseline_cnn()

    # --------------------------------------------------
    # Compile model
    # --------------------------------------------------

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print("\nModel compiled successfully.")

    model.summary()

    # --------------------------------------------------
    # Create output directories
    # --------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    HISTORY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # Callbacks
    # --------------------------------------------------

    callbacks = [

        # Save model with the best validation loss
        tf.keras.callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_loss",
            save_best_only=True,
            mode="min",
            verbose=1,
        ),

        # Stop training if validation loss stops improving
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            mode="min",
            restore_best_weights=True,
            verbose=1,
        ),

        # Reduce learning rate when validation loss plateaus
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            mode="min",
            verbose=1,
        ),
    ]

    # --------------------------------------------------
    # Train model
    # --------------------------------------------------

    print("\nStarting baseline training...")

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    # --------------------------------------------------
    # Save training history
    # --------------------------------------------------

    history_df = pd.DataFrame(history.history)

    history_df.to_csv(
        HISTORY_PATH,
        index=False,
    )

    # --------------------------------------------------
    # Final information
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("BASELINE TRAINING COMPLETE")
    print("=" * 60)

    print("\nTraining history saved to:")
    print(HISTORY_PATH)

    print("\nBest model saved to:")
    print(MODEL_PATH)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    main()