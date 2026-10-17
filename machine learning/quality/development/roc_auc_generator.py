"""
Gera o gráfico da ROC Curve (roc_curve.png) usado na nota ROC-AUC.

Os scores são sintéticos: positivos ~ N(separação, 1) e negativos ~ N(0, 1).
Quanto maior a separação entre as médias, maior o AUC.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc, roc_curve

rng = np.random.default_rng(42)
n = 2000
y_true = rng.integers(0, 2, n)

# (nome, separação entre as médias, cor) -> AUC esperado ~0.50, ~0.70 e ~0.90
modelos = [
    ("Fraco", 0.0, "red"),
    ("Bom", 0.75, "orange"),
    ("Excelente", 1.8, "green"),
]

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot([0, 1], [0, 1], "k--", linewidth=2, alpha=0.7, label="Aleatório (diagonal)")

for nome, separacao, cor in modelos:
    scores = rng.normal(0, 1, n) + y_true * separacao
    fpr, tpr, _ = roc_curve(y_true, scores)
    valor_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=cor, linewidth=2.5, label=f"{nome} (AUC = {valor_auc:.2f})")
    print(f"{nome}: AUC = {valor_auc:.2f}")

ax.set_xlabel("False Positive Rate (Taxa de Falsos Positivos)", fontsize=12, fontweight="bold")
ax.set_ylabel("True Positive Rate (Taxa de Verdadeiros Positivos)", fontsize=12, fontweight="bold")
ax.set_title("ROC Curve - Classificação Binária", fontsize=14, fontweight="bold", pad=20)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=11, loc="lower right", framealpha=0.9)

saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roc_curve.png")
plt.tight_layout()
plt.savefig(saida, dpi=150, bbox_inches="tight")
print(f"Gráfico salvo em: {saida}")
