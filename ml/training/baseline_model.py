import tensorflow as tf
from tensorflow.keras import layers, models


IMAGE_SIZE = (224, 224, 3)
NUM_CLASSES = 5


def build_baseline_cnn():
    """
    Build a simple baseline CNN for 5-class
    diabetic retinopathy classification.
    """

    model = models.Sequential([
        layers.Input(shape=IMAGE_SIZE),

        # Block 1
        layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        # Block 2
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        # Block 3
        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.MaxPooling2D((2, 2)),

        # Classification head
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),

        layers.Dense(NUM_CLASSES, activation="softmax"),
    ])

    return model


if __name__ == "__main__":
    model = build_baseline_cnn()

    model.summary()