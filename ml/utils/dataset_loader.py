from pathlib import Path

import pandas as pd
import tensorflow as tf


IMAGE_SIZE = (224, 224)
NUM_CLASSES = 5


def load_split_csv(csv_path: str | Path) -> pd.DataFrame:
    """
    Load a dataset split CSV and validate its structure.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    required_columns = {"id_code", "diagnosis"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns: {required_columns}"
        )

    if df.empty:
        raise ValueError(f"CSV is empty: {csv_path}")

    return df


def create_dataset(
    csv_path: str | Path,
    image_dir: str | Path,
    batch_size: int = 32,
    shuffle: bool = False,
) -> tf.data.Dataset:
    """
    Create a TensorFlow dataset from an APTOS split CSV.

    Pipeline:
        CSV
        -> image path
        -> image loading
        -> RGB conversion
        -> resize
        -> normalization [0, 1]
        -> batching
    """

    df = load_split_csv(csv_path)

    image_dir = Path(image_dir)

    image_paths = [
        str(image_dir / f"{image_id}.png")
        for image_id in df["id_code"]
    ]

    labels = df["diagnosis"].astype("int32").to_numpy()

    # Verify that every referenced image exists.
    missing_images = [
        path for path in image_paths
        if not Path(path).exists()
    ]

    if missing_images:
        raise FileNotFoundError(
            f"{len(missing_images)} images are missing. "
            f"First missing image: {missing_images[0]}"
        )

    dataset = tf.data.Dataset.from_tensor_slices(
        (image_paths, labels)
    )

    if shuffle:
        dataset = dataset.shuffle(
            buffer_size=len(df),
            seed=42,
            reshuffle_each_iteration=True,
        )

    def load_and_preprocess(image_path, label):
        image = tf.io.read_file(image_path)

        image = tf.image.decode_png(
            image,
            channels=3,
        )

        image = tf.image.resize(
            image,
            IMAGE_SIZE,
        )

        image = tf.cast(
            image,
            tf.float32,
        ) / 255.0

        return image, label

    dataset = dataset.map(
        load_and_preprocess,
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    dataset = dataset.batch(batch_size)

    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    return dataset