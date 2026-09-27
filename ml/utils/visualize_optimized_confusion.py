import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# ============================================================
# PATHS
# ============================================================

ROOT = Path(".")

CM_PATH = (
    ROOT
    / "results"
    / "reports"
    / "optimized_confusion_matrix.csv"
)

OUTPUT_DIR = (
    ROOT
    / "results"
    / "confusion_matrix"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "optimized_confusion_matrix.png"
)


# ============================================================
# LOAD MATRIX
# ============================================================

cm = pd.read_csv(
    CM_PATH,
    index_col=0,
)


# ============================================================
# VISUALIZE
# ============================================================

plt.figure(
    figsize=(9, 7)
)

plt.imshow(
    cm.values,
    aspect="auto",
)

plt.colorbar(
    label="Number of Images"
)

plt.xticks(
    range(len(cm.columns)),
    cm.columns,
    rotation=30,
    ha="right",
)

plt.yticks(
    range(len(cm.index)),
    cm.index,
)

plt.xlabel(
    "Predicted Class"
)

plt.ylabel(
    "True Class"
)

plt.title(
    "Optimized Retinal CNN - Confusion Matrix"
)


# Add values inside cells

for i in range(cm.shape[0]):

    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            str(cm.iloc[i, j]),
            ha="center",
            va="center",
        )


plt.tight_layout()

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight",
)

plt.close()


print("=" * 70)
print("CONFUSION MATRIX VISUALIZATION COMPLETE")
print("=" * 70)

print("\nSaved to:")
print(OUTPUT_PATH)