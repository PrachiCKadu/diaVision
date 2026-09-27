import pandas as pd


def calculate_class_weights(csv_path: str) -> dict[int, float]:
    """
    Calculate balanced class weights from the training split.

    Formula:
        weight_i = N / (K * n_i)

    where:
        N = total training samples
        K = number of classes
        n_i = samples in class i
    """

    df = pd.read_csv(csv_path)

    class_counts = df["diagnosis"].value_counts().sort_index()

    total_samples = len(df)
    num_classes = len(class_counts)

    class_weights = {
        int(class_id): total_samples / (num_classes * count)
        for class_id, count in class_counts.items()
    }

    return class_weights


if __name__ == "__main__":

    weights = calculate_class_weights(
        "dataset/metadata/train.csv"
    )

    print("Class weights:")

    for class_id, weight in weights.items():
        print(f"Class {class_id}: {weight:.4f}")