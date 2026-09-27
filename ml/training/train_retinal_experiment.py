from pathlib import Path

import tensorflow as tf

from ml.utils.dataset_loader_retinal import create_dataset


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRAIN_CSV = PROJECT_ROOT / "dataset" / "metadata" / "train.csv"
VAL_CSV = PROJECT_ROOT / "dataset" / "metadata" / "validation.csv"

IMAGE_DIR = (
    PROJECT_ROOT
    / "dataset"
    / "raw"
    / "aptos2019"
    / "train_images"
)

MODEL_DIR = PROJECT_ROOT / "models" / "optimized"
MODEL_PATH = MODEL_DIR / "retinal_experiment_cnn.keras"

HISTORY_DIR = PROJECT_ROOT / "results" / "reports"
HISTORY_PATH = HISTORY_DIR / "retinal_experiment_history.csv"

IMAGE_SIZE = (224, 224)
NUM_CLASSES = 5
BATCH_SIZE = 32
EPOCHS = 20


# ============================================================
# CLASS WEIGHTS
# ============================================================

CLASS_WEIGHTS = {
    0: 0.4059,
    1: 1.9792,
    2: 0.7333,
    3: 3.7970,
    4: 2.4763,
}


# ============================================================
# MODEL
# Same architecture as baseline
# Only preprocessing is changed.
# ============================================================

def build_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Input(
            shape=(*IMAGE_SIZE, 3)
        ),

        tf.keras.layers.Conv2D(
            32,
            (3, 3),
            activation="relu",
            padding="same",
        ),

        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(
            64,
            (3, 3),
            activation="relu",
            padding="same",
        ),

        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(
            128,
            (3, 3),
            activation="relu",
            padding="same",
        ),

        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(
            128,
            activation="relu",
        ),

        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(
            NUM_CLASSES,
            activation="softmax",
        ),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("RETINAL PREPROCESSING EXPERIMENT")
print("=" * 60)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

print("\nLoading training dataset...")

train_ds = create_dataset(
    TRAIN_CSV,
    IMAGE_DIR,
    batch_size=BATCH_SIZE,
    shuffle=True,
)

print("Training dataset loaded successfully.")

print("\nLoading validation dataset...")

val_ds = create_dataset(
    VAL_CSV,
    IMAGE_DIR,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

print("Validation dataset loaded successfully.")


print("\nBuilding model...")

model = build_model()

model.summary()

print("\nModel compiled successfully.")


# ============================================================
# CALLBACKS
# ============================================================

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=str(MODEL_PATH),
    monitor="val_loss",
    save_best_only=True,
    verbose=1,
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
    verbose=1,
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-6,
    verbose=1,
)


# ============================================================
# TRAIN
# ============================================================

print("\nStarting retinal preprocessing experiment...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=CLASS_WEIGHTS,
    callbacks=[
        checkpoint,
        early_stopping,
        reduce_lr,
    ],
)


# ============================================================
# SAVE HISTORY
# ============================================================

import pandas as pd

history_table = pd.DataFrame(history.history)

history_table.to_csv(
    HISTORY_PATH,
    index=False,
)

import pandas as pd

history_table = pd.DataFrame(history.history)

history_table.to_csv(
    HISTORY_PATH,
    index=False,
)


print("\n" + "=" * 60)
print("RETINAL EXPERIMENT COMPLETE")
print("=" * 60)

print("\nTraining history saved to:")
print(HISTORY_PATH)

print("\nBest model saved to:")
print(MODEL_PATH)

best_epoch = (
    history_table["val_loss"].idxmin() + 1
)

best_val_loss = (
    history_table["val_loss"].min()
)

best_val_accuracy = (
    history_table["val_accuracy"].max()
)

best_acc_epoch = (
    history_table["val_accuracy"].idxmax() + 1
)

print("\nBest validation loss epoch:", best_epoch)
print(
    "Best validation loss:",
    round(best_val_loss, 4),
)

print(
    "Best validation accuracy epoch:",
    best_acc_epoch,
)

print(
    "Best validation accuracy:",
    round(best_val_accuracy, 4),
)