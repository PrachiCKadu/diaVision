from pathlib import Path

import tensorflow as tf
import pandas as pd


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
MODEL_PATH = MODEL_DIR / "optimized_diabetic_retinopathy.keras"

RESULTS_DIR = PROJECT_ROOT / "results"
REPORT_DIR = RESULTS_DIR / "reports"

HISTORY_PATH = REPORT_DIR / "optimized_training_history.csv"

IMAGE_SIZE = (224, 224)
NUM_CLASSES = 5
BATCH_SIZE = 32
EPOCHS = 30


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
# DATA AUGMENTATION
# ============================================================

def build_augmentation():

    return tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip(
                mode="horizontal"
            ),

            tf.keras.layers.RandomRotation(
                factor=0.05
            ),

            tf.keras.layers.RandomZoom(
                height_factor=0.10,
                width_factor=0.10,
            ),

            tf.keras.layers.RandomContrast(
                factor=0.10
            ),
        ],
        name="retinal_augmentation",
    )


# ============================================================
# OPTIMIZED CNN
# ============================================================

def build_model():

    inputs = tf.keras.Input(
        shape=(*IMAGE_SIZE, 3),
        name="retinal_image",
    )

    x = build_augmentation()(inputs)

    # --------------------------------------------------------
    # Block 1
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.Conv2D(
        32,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D()(x)

    # --------------------------------------------------------
    # Block 2
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.Conv2D(
        64,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D()(x)

    # --------------------------------------------------------
    # Block 3
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.Conv2D(
        128,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.MaxPooling2D()(x)

    # --------------------------------------------------------
    # Block 4
    # --------------------------------------------------------

    x = tf.keras.layers.Conv2D(
        256,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.Conv2D(
        256,
        (3, 3),
        padding="same",
        use_bias=False,
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    # --------------------------------------------------------
    # Classification head
    # --------------------------------------------------------

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(
        0.40
    )(x)

    x = tf.keras.layers.Dense(
        128,
        activation="relu",
    )(x)

    x = tf.keras.layers.Dropout(
        0.30
    )(x)

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="disease_class",
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="optimized_retinal_cnn",
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0003
        ),
        loss="sparse_categorical_crossentropy",
        metrics=[
            "accuracy",
        ],
    )

    return model


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("OPTIMIZED DIABETIC RETINOPATHY CNN")
print("=" * 70)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# DATASETS
# ============================================================

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


# ============================================================
# MODEL
# ============================================================

print("\nBuilding optimized model...")

model = build_model()

model.summary()

print("\nOptimized model compiled successfully.")


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
    patience=6,
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
# TRAINING
# ============================================================

print("\nStarting optimized model training...")

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

history_table = pd.DataFrame(
    history.history
)

history_table.to_csv(
    HISTORY_PATH,
    index=False,
)


# ============================================================
# FINAL INFORMATION
# ============================================================

best_loss_epoch = (
    history_table["val_loss"].idxmin() + 1
)

best_loss = (
    history_table["val_loss"].min()
)

best_accuracy_epoch = (
    history_table["val_accuracy"].idxmax() + 1
)

best_accuracy = (
    history_table["val_accuracy"].max()
)


print("\n" + "=" * 70)
print("OPTIMIZED MODEL TRAINING COMPLETE")
print("=" * 70)

print("\nBest validation loss epoch:")
print(best_loss_epoch)

print("Best validation loss:")
print(round(best_loss, 4))

print("\nBest validation accuracy epoch:")
print(best_accuracy_epoch)

print("Best validation accuracy:")
print(round(best_accuracy, 4))

print("\nTraining history:")
print(HISTORY_PATH)

print("\nBest model:")
print(MODEL_PATH)