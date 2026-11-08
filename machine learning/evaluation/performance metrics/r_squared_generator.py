"""Generate R-squared.png: a visual explanation of the coefficient of determination.

Left panel : error of the laziest baseline (always predict the mean)  -> SS_tot
Right panel: error of the regression model                            -> SS_res
R^2 = 1 - SS_res / SS_tot

Each square has a side equal to the error of one point, so its area is the squared error.
Usage: .venv/bin/python3 r_squared_generator.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

OUT = Path(__file__).parent / "R-squared.png"

# Colors: one hue per role, text always in neutral ink
INK = "#1f2933"
MUTED = "#616e7c"
POINT = "#323f4b"
BASELINE = "#d9730d"   # mean baseline (SS_tot)
MODEL = "#2a6fdb"      # regression model (SS_res)

# Data: a noisy linear relationship
rng = np.random.default_rng(7)
x = np.array([1.0, 2.2, 3.1, 4.3, 5.2, 6.4, 7.3, 8.5])
y = 1.2 + 0.85 * x + rng.normal(0, 1.1, x.size)

slope, intercept = np.polyfit(x, y, 1)
y_hat = intercept + slope * x
y_bar = y.mean()

ss_res = np.sum((y - y_hat) ** 2)
ss_tot = np.sum((y - y_bar) ** 2)
r2 = 1 - ss_res / ss_tot

fig, axes = plt.subplots(1, 2, figsize=(12, 6.4), sharex=True, sharey=True)
fig.patch.set_facecolor("white")

xs = np.linspace(0, 10, 100)


def draw_panel(ax, pred, color, title, ss_label, ss_value, line_label, line_y, label_xy):
    ax.set_facecolor("white")
    # Squared-error squares (side = |error|, area = squared error), drawn to the right
    for xi, yi, pi in zip(x, y, pred):
        side = abs(yi - pi)
        bottom = min(yi, pi)
        ax.add_patch(Rectangle((xi, bottom), side, side, facecolor=color, alpha=0.22,
                               edgecolor=color, linewidth=1.0))
        ax.plot([xi, xi], [yi, pi], color=color, linewidth=1.4)
    ax.plot(xs, line_y, color=color, linewidth=2.2)
    ax.scatter(x, y, s=46, color=POINT, zorder=3, edgecolor="white", linewidth=1.2)

    ax.set_title(title, fontsize=14, fontweight="bold", color=INK, loc="left", pad=12)
    ax.text(0.03, 0.96, f"{ss_label} = {ss_value:.1f}", transform=ax.transAxes,
            fontsize=13, color=INK, va="top", fontweight="bold")
    ax.text(0.03, 0.89, "sum of the areas of all squares", transform=ax.transAxes,
            fontsize=10.5, color=MUTED, va="top")
    # Direct label for the line, placed where no square is drawn
    ax.text(*label_xy, line_label, color=color, fontsize=11, fontweight="bold",
            ha="right", va="top")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal", adjustable="box")  # equal scale so a square looks like a square
    ax.set_xlabel("x (feature)", fontsize=11, color=MUTED)
    ax.grid(color="#e4e7eb", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#cbd2d9")
    ax.tick_params(colors=MUTED, labelsize=10)


draw_panel(axes[0], np.full_like(y, y_bar), BASELINE,
           "Baseline: always predict the mean", r"$SS_{tot}$", ss_tot,
           r"mean $\bar{y}$", np.full_like(xs, y_bar), (9.8, y_bar - 0.25))
draw_panel(axes[1], y_hat, MODEL,
           "Model: regression line", r"$SS_{res}$", ss_res,
           r"model $\hat{y}$ (regression line)", intercept + slope * xs, (9.8, 2.0))
axes[0].set_ylabel("y (target)", fontsize=11, color=MUTED)

fig.suptitle(r"$R^2 = 1 - \dfrac{SS_{res}}{SS_{tot}}$" + f"  =  1 - {ss_res:.1f} / {ss_tot:.1f}  =  {r2:.2f}",
             fontsize=18, color=INK, fontweight="bold", y=0.99)
fig.text(0.5, 0.02,
         f"The model removes {r2:.0%} of the squared error left by the mean baseline: "
         f"it explains {r2:.0%} of the variance in y.",
         ha="center", fontsize=12, color=INK)

fig.tight_layout(rect=(0, 0.08, 1, 0.94))
fig.savefig(OUT, dpi=160, facecolor="white")
print(f"saved {OUT}  (R2 = {r2:.3f})")
