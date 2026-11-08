"""
Generates the accuracy-decay plot (model_drift_decay.png) used in the Model drift note.

The values are illustrative (same series as the code example in the note):
accuracy measured with ground truth at a few points in time after deployment.
"""

import os

import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
SERIES = "#2a78d6"
ALERT = "#e34948"

days = [1, 30, 60, 90, 180, 365]
accuracy = [0.85, 0.82, 0.78, 0.71, 0.65, 0.55]

baseline = accuracy[0]
threshold = baseline * 0.95  # alert when the relative drop is greater than 5%

fig, ax = plt.subplots(figsize=(9, 5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

ax.axhline(baseline, color=TEXT_SECONDARY, linestyle="--", linewidth=1)
ax.axhline(threshold, color=ALERT, linestyle="--", linewidth=1)
ax.plot(days, accuracy, color=SERIES, linewidth=2, marker="o", markersize=8,
        markeredgecolor=SURFACE, markeredgewidth=2)

ax.text(365, baseline + 0.008, "Baseline at deploy (0.85)", ha="right", va="bottom",
        color=TEXT_SECONDARY, fontsize=10)
ax.text(365, threshold + 0.008, "Alert threshold: 5% relative drop (0.81)", ha="right",
        va="bottom", color=TEXT_SECONDARY, fontsize=10)

for d, a in zip(days, accuracy):
    ax.annotate(f"{a:.2f}", (d, a), textcoords="offset points", xytext=(0, -18),
                ha="center", color=TEXT_PRIMARY, fontsize=10)

ax.set_xlabel("Days since deployment", color=TEXT_SECONDARY, fontsize=11)
ax.set_ylabel("Accuracy (with ground truth)", color=TEXT_SECONDARY, fontsize=11)
ax.set_title("Model drift: accuracy decays after deployment", color=TEXT_PRIMARY,
             fontsize=13, fontweight="bold", loc="left")
ax.set_ylim(0.45, 0.92)
ax.set_xlim(-20, 380)
ax.set_xticks(days)
ax.tick_params(colors=TEXT_SECONDARY)
ax.grid(axis="y", alpha=0.25)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(TEXT_SECONDARY)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_drift_decay.png")
plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor=SURFACE)
print(f"Plot saved to: {output_path}")
