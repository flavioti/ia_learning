---
aliases:
  - F-beta
  - classic-ml
---
#metric #classification 

**F1-Score** balances [[Precision]] and [[Recall]] in a single number: their harmonic mean. It answers: *"Is the model good at both avoiding false alarms and avoiding misses?"*

$$
\text{F}_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\,\text{TP}}{2\,\text{TP} + \text{FP} + \text{FN}}
$$

Range: 0 to 1. It is 1 only when both precision and recall are 1, and 0 if either is 0.

## Why harmonic mean

The harmonic mean is dominated by the lower of the two values, so a model cannot hide a weak metric behind a strong one.

Example: precision = 0.80 and recall = 0.40

- Arithmetic mean: $(0.80 + 0.40) / 2 = 0.60$
- Harmonic mean (F1): $2 \times \frac{0.80 \times 0.40}{0.80 + 0.40} \approx 0.53$

A degenerate model that predicts everything as positive has recall = 1 but very low precision, and F1 stays low. The arithmetic mean would still look decent.

## F-beta score

F1 weights precision and recall equally. The generalization $\text{F}_\beta$ lets you favor one:

$$
\text{F}_\beta = (1 + \beta^2) \times \frac{\text{Precision} \times \text{Recall}}{\beta^2 \times \text{Precision} + \text{Recall}}
$$

- $\beta < 1$ (e.g. F0.5): favors precision (false positives are costlier)
- $\beta = 1$: F1, balanced
- $\beta > 1$ (e.g. F2): favors recall (false negatives are costlier)

## When to use

- Imbalanced classes, where [[Accuracy]] is misleading (e.g. 99% negatives: predicting always negative gives 99% accuracy but F1 = 0).
- When both false positives and false negatives matter and you need one number to compare models.

## Limitations

- Ignores true negatives ($\text{TN}$), so it says nothing about how well the negative class is handled.
- Hides the precision/recall trade-off: the same F1 can come from very different (precision, recall) pairs. Check both when the cost of errors is asymmetric.
- Depends on the decision threshold. Use [[ROC-AUC]] or a precision-recall curve to evaluate across thresholds.
- Undefined (0/0) when precision and recall are both 0. Libraries usually return 0 with a warning.

## Multi-class

F1 is computed per class and then averaged:

- **Macro**: unweighted mean across classes (treats all classes equally)
- **Weighted**: mean weighted by class support
- **Micro**: computed from the global TP, FP and FN counts

## Code

```python
from sklearn.metrics import f1_score, fbeta_score

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 0, 1, 1, 1]

f1_score(y_true, y_pred)                # TP=3, FP=1, FN=1 -> 0.75
fbeta_score(y_true, y_pred, beta=2)     # favors recall

# multi-class
f1_score(y_true, y_pred, average="macro")
```

## Related

- [[Confusion Matrix]] - source of TP, FP, FN, TN
- [[Precision]]
- [[Recall]]
- [[Accuracy]]
- [[ROC-AUC]]
- [[Evaluating classification model metrics]]
