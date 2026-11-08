"""
Generates fraud_pr_curve.png, used in the Q&A note
"Your Model Scores 95% Offline but Fails in Production" (EN and PT-BR).

It uses the same synthetic binormal model as fraud_roc_curve_generator.py
(ROC-AUC = 0.95, 0.5% positives), so both charts describe the same classifier:

    recall    = TPR
    precision = TPR * p / (TPR * p + FPR * (1 - p))        with p = prevalence

The point of the chart is that the same model that has a ROC-AUC of 0.95 has a
much lower PR-AUC when positives are rare.
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


def precision_at(tpr, fpr):
    """Precision for a given TPR/FPR pair and the class prevalence."""
    return tpr * PREVALENCE / (tpr * PREVALENCE + fpr * (1 - PREVALENCE))


# Binormal ROC: AUC = Phi(d / sqrt(2))  ->  d = sqrt(2) * Phi^-1(AUC)
d_prime = np.sqrt(2) * norm.ppf(TARGET_AUC)

# Log-spaced FPR: with rare positives the interesting part is at very low FPR
fpr = np.concatenate([[1e-9], np.logspace(-8, 0, 4000)])
tpr = norm.cdf(d_prime + norm.ppf(fpr))
precision = precision_at(tpr, fpr)

# Anchor the curve at recall = 0 (precision of the top-scored case is ~1)
recall = np.concatenate([[0.0], tpr])
precision = np.concatenate([[1.0], precision])
pr_auc = np.trapezoid(precision, recall)

op_tpr = float(norm.cdf(d_prime + norm.ppf(OPERATING_FPR)))
op_precision = precision_at(op_tpr, OPERATING_FPR)
print(f"PR-AUC = {pr_auc:.3f} (baseline = prevalence = {PREVALENCE:.3f})")
print(f"Operating point: recall = {op_tpr:.1%}, precision = {op_precision:.1%}")


def comma(text):
    return text.replace(".", ",")


fig, ax = plt.subplots(figsize=(8, 7), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

ax.fill_between(recall, precision, color=SERIES, alpha=0.08, linewidth=0)
ax.plot(
    [0, 1], [PREVALENCE, PREVALENCE], color=INK_SECONDARY, linewidth=1.5, linestyle=(0, (5, 4)),
    label=comma(f"Aleatório (precisão = prevalência = {PREVALENCE:.1%})"),
)
ax.plot(recall, precision, color=SERIES, linewidth=2.5, label=comma(f"Modelo de fraude (PR-AUC = {pr_auc:.2f})"))

# Operating point, with a 2px surface ring so it separates from the curve
ax.plot(
    op_tpr, op_precision, "o", markersize=10, color=HIGHLIGHT,
    markeredgecolor=SURFACE, markeredgewidth=2, zorder=5,
    label="Ponto de operação (limiar escolhido)",
)
ax.annotate(
    comma(
        f"Limiar escolhido\n"
        f"recall = {op_tpr:.0%} | precisão ≈ {op_precision:.0%}\n"
        f"(FPR = {OPERATING_FPR:.0%}, com {PREVALENCE:.1%} de fraudes)"
    ),
    xy=(op_tpr, op_precision), xytext=(0.45, 0.55),
    fontsize=11, color=INK, va="center",
    arrowprops=dict(arrowstyle="-", color=INK_SECONDARY, linewidth=1),
)

ax.set_xlabel("Recall (TPR)", fontsize=12, color=INK_SECONDARY)
ax.set_ylabel("Precisão", fontsize=12, color=INK_SECONDARY)
ax.set_title("Curva precisão-recall do detector de fraude", fontsize=13,
             fontweight="bold", color=INK, loc="left", pad=14)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.01)

ax.grid(True, color=GRID, linewidth=1, linestyle="-")
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GRID)
ax.tick_params(colors=INK_SECONDARY, labelsize=10)
decimal_comma = FuncFormatter(lambda v, _: comma(f"{v:.1f}"))
ax.xaxis.set_major_formatter(decimal_comma)
ax.yaxis.set_major_formatter(decimal_comma)

ax.legend(loc="upper right", fontsize=10, frameon=False, labelcolor=INK)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fraud_pr_curve.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor=SURFACE)
print(f"Plot saved to: {output_path}")
