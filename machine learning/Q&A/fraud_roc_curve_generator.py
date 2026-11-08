"""
Generates fraud_roc_curve.png, used in the Q&A note
"Your Model Scores 95% Offline but Fails in Production" (EN and PT-BR).

The curve is synthetic (binormal model): negative scores ~ N(0, 1) and positive
scores ~ N(d, 1), with d chosen so that AUC = 0.95 exactly. The point of the
chart is to show that a great ROC curve can hide a poor precision when positives
are rare (0.5% of the transactions).
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.stats import norm

TARGET_AUC = 0.95
PREVALENCE = 0.005  # share of fraudulent transactions
OPERATING_FPR = 0.05  # false positive rate of the chosen threshold

# Light-mode tokens (reference palette)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e6e5e1"
SERIES = "#2a78d6"  # categorical slot 1
HIGHLIGHT = "#eb6834"  # categorical slot 2

# Binormal ROC: AUC = Phi(d / sqrt(2))  ->  d = sqrt(2) * Phi^-1(AUC)
d_prime = np.sqrt(2) * norm.ppf(TARGET_AUC)
fpr = np.linspace(0, 1, 2001)
tpr = norm.cdf(d_prime + norm.ppf(fpr))  # ppf(0) = -inf -> tpr = 0, ppf(1) = +inf -> tpr = 1
auc_value = np.trapezoid(tpr, fpr)

# Operating point and what it means with rare positives
op_tpr = float(norm.cdf(d_prime + norm.ppf(OPERATING_FPR)))
op_precision = op_tpr * PREVALENCE / (op_tpr * PREVALENCE + OPERATING_FPR * (1 - PREVALENCE))
print(f"AUC = {auc_value:.3f}")
print(f"Operating point: FPR = {OPERATING_FPR:.0%}, TPR = {op_tpr:.1%}, precision = {op_precision:.1%}")

fig, ax = plt.subplots(figsize=(8, 7), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

ax.fill_between(fpr, tpr, color=SERIES, alpha=0.08, linewidth=0)
ax.plot([0, 1], [0, 1], color=INK_SECONDARY, linewidth=1.5, linestyle=(0, (5, 4)), label="Aleatório (AUC = 0,50)")
ax.plot(fpr, tpr, color=SERIES, linewidth=2.5, label=f"Modelo de fraude (AUC = {auc_value:.2f})".replace(".", ","))

# Operating point, with a 2px surface ring so it separates from the curve
ax.plot(
    OPERATING_FPR, op_tpr, "o", markersize=10, color=HIGHLIGHT,
    markeredgecolor=SURFACE, markeredgewidth=2, zorder=5,
    label="Ponto de operação (limiar escolhido)",
)
ax.annotate(
    f"Limiar escolhido\n"
    f"FPR = {OPERATING_FPR:.0%} | recall = {op_tpr:.0%}\n"
    f"mas precisão ≈ {op_precision:.0%}\n"
    f"(com {PREVALENCE:.1%} de fraudes)".replace(".", ","),
    xy=(OPERATING_FPR, op_tpr), xytext=(0.52, 0.30),
    fontsize=11, color=INK, va="center",
    arrowprops=dict(arrowstyle="-", color=INK_SECONDARY, linewidth=1),
)

ax.set_xlabel("Taxa de falsos positivos (FPR)", fontsize=12, color=INK_SECONDARY)
ax.set_ylabel("Taxa de verdadeiros positivos (TPR = recall)", fontsize=12, color=INK_SECONDARY)
ax.set_title("Curva ROC do detector de fraude", fontsize=13,
             fontweight="bold", color=INK, loc="left", pad=14)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.01)
ax.set_aspect("equal", adjustable="box")

ax.grid(True, color=GRID, linewidth=1, linestyle="-")
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GRID)
ax.tick_params(colors=INK_SECONDARY, labelsize=10)
decimal_comma = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))
ax.xaxis.set_major_formatter(decimal_comma)
ax.yaxis.set_major_formatter(decimal_comma)

ax.legend(loc="lower right", fontsize=10, frameon=False, labelcolor=INK)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fraud_roc_curve.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor=SURFACE)
print(f"Plot saved to: {output_path}")
