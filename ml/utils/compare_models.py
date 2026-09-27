from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "results" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = REPORT_DIR / "model_comparison.csv"
TEXT_OUTPUT_PATH = REPORT_DIR / "model_comparison.txt"


# ============================================================
# RESULTS
# ============================================================

results = [
    {
        "Model": "Baseline CNN",
        "Accuracy": 0.6818,
        "Macro Precision": 0.4973,
        "Macro Recall": 0.5087,
        "Macro F1": 0.4835,
        "Weighted F1": 0.6861,
    },
    {
        "Model": "Retinal Preprocessing CNN",
        "Accuracy": 0.7073,
        "Macro Precision": 0.5073,
        "Macro Recall": 0.5359,
        "Macro F1": 0.5063,
        "Weighted F1": 0.7120,
    },
    {
        "Model": "Optimized CNN",
        "Accuracy": 0.5564,
        "Macro Precision": 0.3856,
        "Macro Recall": 0.3908,
        "Macro F1": 0.3414,
        "Weighted F1": 0.5562,
    },
]


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(results)


# ============================================================
# IMPROVEMENT OVER BASELINE
# ============================================================

baseline = df.iloc[0]

df["Accuracy Change vs Baseline"] = (
    df["Accuracy"] - baseline["Accuracy"]
)

df["Macro F1 Change vs Baseline"] = (
    df["Macro F1"] - baseline["Macro F1"]
)

df["Macro Recall Change vs Baseline"] = (
    df["Macro Recall"] - baseline["Macro Recall"]
)


# ============================================================
# SAVE CSV
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# PRINT REPORT
# ============================================================

print("=" * 80)
print("MODEL COMPARISON")
print("=" * 80)

print()

print(
    df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


# ============================================================
# BEST MODELS
# ============================================================

best_accuracy = df.loc[
    df["Accuracy"].idxmax()
]

best_macro_f1 = df.loc[
    df["Macro F1"].idxmax()
]

best_macro_recall = df.loc[
    df["Macro Recall"].idxmax()
]


print("\n" + "=" * 80)
print("BEST RESULTS")
print("=" * 80)

print(
    f"\nBest Accuracy: "
    f"{best_accuracy['Model']} "
    f"({best_accuracy['Accuracy']:.4f})"
)

print(
    f"Best Macro F1: "
    f"{best_macro_f1['Model']} "
    f"({best_macro_f1['Macro F1']:.4f})"
)

print(
    f"Best Macro Recall: "
    f"{best_macro_recall['Model']} "
    f"({best_macro_recall['Macro Recall']:.4f})"
)


# ============================================================
# ACADEMIC CONCLUSION
# ============================================================

conclusion = """
MODEL SELECTION CONCLUSION
============================================================

The Retinal Preprocessing CNN achieved the best overall
performance among the three evaluated models.

Compared with the Baseline CNN:

Accuracy:
68.18% -> 70.73%

Macro F1:
0.4835 -> 0.5063

Macro Recall:
0.5087 -> 0.5359

The Retinal Preprocessing CNN therefore provides a measurable
improvement over the baseline.

The current Optimized CNN did not outperform the baseline.
Its Macro F1 and minority-class performance were substantially
lower.

Therefore, the current Optimized CNN should NOT be selected as
the final model.

The next optimization stage should focus on improving
minority-class recognition, particularly:

- Mild
- Severe
- Proliferative DR

The Retinal Preprocessing CNN will remain the current reference
model for the next optimization experiment.
"""


print("\n" + conclusion)


# ============================================================
# SAVE TEXT REPORT
# ============================================================

with open(
    TEXT_OUTPUT_PATH,
    "w",
    encoding="utf-8",
) as f:

    f.write(
        "MODEL COMPARISON\n"
    )

    f.write("=" * 80 + "\n\n")

    f.write(
        df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    f.write("\n\n")

    f.write(conclusion)


# ============================================================
# COMPLETE
# ============================================================

print("=" * 80)
print("FILES SAVED")
print("=" * 80)

print(
    f"\nCSV:\n{OUTPUT_PATH}"
)

print(
    f"\nReport:\n{TEXT_OUTPUT_PATH}"
)

print("\nModel comparison completed successfully.")