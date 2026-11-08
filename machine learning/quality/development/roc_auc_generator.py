"""
Generates the ROC curve plot (roc_curve.png) used in the ROC-AUC note.

Scores are synthetic: positives ~ N(separation, 1) and negatives ~ N(0, 1).
The larger the gap between the means, the higher the AUC.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc, roc_curve

rng = np.random.default_rng(42)
n = 2000
y_true = rng.integers(0, 2, n)

# (name, gap between the means, color) -> expected AUC ~0.50, ~0.70 and ~0.90
models = [
    ("Weak", 0.0, "red"),
    ("Good", 0.75, "orange"),
    ("Excellent", 1.8, "green"),
]

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot([0, 1], [0, 1], "k--", linewidth=2, alpha=0.7, label="Random (diagonal)")

for name, separation, color in models:
    scores = rng.normal(0, 1, n) + y_true * separation
    fpr, tpr, _ = roc_curve(y_true, scores)
    auc_value = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=color, linewidth=2.5, label=f"{name} (AUC = {auc_value:.2f})")
    print(f"{name}: AUC = {auc_value:.2f}")

ax.set_xlabel("False Positive Rate", fontsize=12, fontweight="bold")
ax.set_ylabel("True Positive Rate", fontsize=12, fontweight="bold")
ax.set_title("ROC Curve - Binary Classification", fontsize=14, fontweight="bold", pad=20)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=11, loc="lower right", framealpha=0.9)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roc_curve.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"Plot saved to: {output_path}")
