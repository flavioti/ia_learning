"""
Generates fraud_confusion_matrix.png, used in the Q&A note
"Your Model Scores 95% Offline but Fails in Production" (EN and PT-BR).

It uses the same synthetic binormal model and the same operating point as
fraud_roc_curve_generator.py and fraud_pr_curve_generator.py (ROC-AUC = 0.95,
0.5% positives, threshold with FPR = 5%), applied to 100,000 transactions.

Layout follows the vault's Confusion Matrix note: rows are the actual class,
columns are the predicted class, positive class first.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

TARGET_AUC = 0.95
N_TRANSACTIONS = 100_000
PREVALENCE = 0.005  # share of fraudulent transactions
OPERATING_FPR = 0.05  # false positive rate of the chosen threshold

# Light-mode tokens (reference palette). Identity of the cell type is carried by
# the hue (blue = correct, orange = error) and by the label inside each cell.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
CORRECT = "#d4e4f8"  # tint of categorical slot 1 (blue)
CORRECT_EDGE = "#2a78d6"
ERROR = "#fbdccd"  # tint of categorical slot 2 (orange)
ERROR_EDGE = "#eb6834"

# Binormal model at the chosen threshold
d_prime = np.sqrt(2) * norm.ppf(TARGET_AUC)
tpr = float(norm.cdf(d_prime + norm.ppf(OPERATING_FPR)))

positives = round(N_TRANSACTIONS * PREVALENCE)
negatives = N_TRANSACTIONS - positives
tp = round(tpr * positives)
fn = positives - tp
fp = round(OPERATING_FPR * negatives)
tn = negatives - fp

recall = tp / (tp + fn)
precision = tp / (tp + fp)
accuracy = (tp + tn) / N_TRANSACTIONS
print(f"TP={tp} FN={fn} FP={fp} TN={tn}")
print(f"recall={recall:.1%} precision={precision:.1%} accuracy={accuracy:.1%}")


def thousands(value):
    """pt-BR number formatting: 94525 -> '94.525'."""
    return f"{value:,}".replace(",", ".")


def percent(value):
    return f"{value:.1%}".replace(".", ",")


# cells[row][col]: row = actual (fraud, legit), col = predicted (fraud, legit)
cells = [
    [("VP", tp, CORRECT, CORRECT_EDGE, "fraude capturada"),
     ("FN", fn, ERROR, ERROR_EDGE, "fraude não detectada")],
    [("FP", fp, ERROR, ERROR_EDGE, "alarme falso"),
     ("VN", tn, CORRECT, CORRECT_EDGE, "legítima aprovada")],
]
row_totals = [tp + fn, fp + tn]

fig, ax = plt.subplots(figsize=(8, 7), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.set_xlim(0, 2)
ax.set_ylim(2, 0)  # row 0 on top
ax.set_aspect("equal")
ax.axis("off")

gap = 0.03  # surface gap between cells
for r in range(2):
    for c in range(2):
        tag, count, face, edge, meaning = cells[r][c]
        ax.add_patch(plt.Rectangle(
            (c + gap, r + gap), 1 - 2 * gap, 1 - 2 * gap,
            facecolor=face, edgecolor=edge, linewidth=1.5,
        ))
        ax.text(c + 0.5, r + 0.30, tag, ha="center", va="center", fontsize=13,
                fontweight="bold", color=INK_SECONDARY)
        ax.text(c + 0.5, r + 0.52, thousands(count), ha="center", va="center", fontsize=26,
                fontweight="bold", color=INK)
        ax.text(c + 0.5, r + 0.72, meaning, ha="center", va="center", fontsize=11, color=INK)
        ax.text(c + 0.5, r + 0.85, f"{percent(count / row_totals[r])} da linha", ha="center",
                va="center", fontsize=10, color=INK_SECONDARY)

# Axis labels, outside the grid
for c, label in enumerate(["Previsto: fraude", "Previsto: legítima"]):
    ax.text(c + 0.5, -0.06, label, ha="center", va="bottom", fontsize=12, color=INK_SECONDARY)
for r, label in enumerate([f"Real: fraude\n({thousands(positives)})",
                           f"Real: legítima\n({thousands(negatives)})"]):
    ax.text(-0.06, r + 0.5, label, ha="right", va="center", fontsize=12, color=INK_SECONDARY)

fig.suptitle("Matriz de confusão do detector de fraude", fontsize=13, fontweight="bold",
             color=INK, x=0.05, ha="left", y=0.97)
fig.text(
    0.05, 0.915,
    f"{thousands(N_TRANSACTIONS)} transações, {percent(PREVALENCE)} de fraudes | limiar com FPR = {OPERATING_FPR:.0%}",
    fontsize=10.5, color=INK_SECONDARY, ha="left",
)
fig.text(
    0.5, 0.06,
    f"Recall = VP / (VP + FN) = {percent(recall)}     "
    f"Precisão = VP / (VP + FP) = {percent(precision)}     "
    f"Acurácia = {percent(accuracy)}",
    fontsize=11, color=INK, ha="center",
)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fraud_confusion_matrix.png")
fig.subplots_adjust(left=0.22, right=0.97, top=0.82, bottom=0.12)
plt.savefig(output_path, dpi=150, facecolor=SURFACE)
print(f"Plot saved to: {output_path}")
