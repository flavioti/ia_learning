#metrics #classification #evaluation #classification-metric

## Overview

Classification metrics compare a **predicted class** with the **actual class**. Most are built from the four cells of the [[Confusion Matrix]].

| Metric                                 | What it measures                                     | Better if | Best for...                                                     |
| -------------------------------------- | ---------------------------------------------------- | --------- | --------------------------------------------------------------- |
| [[Accuracy]]                           | % of predictions that are correct                    | Higher    | Balanced classes, a quick first look                            |
| [[Precision]]                          | Of the predicted positives, how many are real        | Higher    | When false alarms are costly (spam filter, fraud review queue)  |
| [[Recall]]                             | Of the real positives, how many were found           | Higher    | When misses are costly (disease screening, fraud detection)     |
| [[F1-Score]]                           | Harmonic mean of Precision and Recall                | Higher    | Imbalanced classes, one number that balances both errors        |
| Specificity                            | Of the real negatives, how many were correctly kept  | Higher    | When false positives must be kept low                           |
| Balanced Accuracy                      | Average of Recall and Specificity                    | Higher    | Imbalanced classes, an honest replacement for accuracy          |
| MCC (Matthews Correlation Coefficient) | Correlation between prediction and truth (-1 to 1)   | Higher    | Imbalanced data, one balanced score from all four matrix cells  |
| [[ROC-AUC]]                            | Ability to rank positives above negatives (0.5 to 1) | Higher    | Comparing models regardless of the decision threshold           |
| [[PR-AUC]]                             | Precision vs. Recall trade-off across thresholds     | Higher    | Rare positive class, when the positives are what you care about |
| Log Loss (cross-entropy)               | Quality of the predicted **probabilities**           | Lower     | When confident wrong predictions should be punished heavily     |
| Brier Score                            | Mean squared error of the predicted probabilities    | Lower     | Checking probability calibration                                |

## Confusion matrix

|                     | Predicted positive      | Predicted negative      |
| ------------------- | ----------------------- | ----------------------- |
| **Actual positive** | **TP** (true positive)  | **FN** (false negative) |
| **Actual negative** | **FP** (false positive) | **TN** (true negative)  |

- **FP** is a false alarm (Type I error).
- **FN** is a miss (Type II error).

## Math notation

$$
\begin{aligned}
\text{Accuracy} &= \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}} \\[1.5em]
\text{Precision} &= \frac{\text{TP}}{\text{TP} + \text{FP}} \\[1.5em]
\text{Recall} &= \frac{\text{TP}}{\text{TP} + \text{FN}} \\[1.5em]
\text{Specificity} &= \frac{\text{TN}}{\text{TN} + \text{FP}} \\[1.5em]
\text{F}_1\text{-Score} &= 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\,\text{TP}}{2\,\text{TP} + \text{FP} + \text{FN}} \\[1.5em]
\text{Balanced Accuracy} &= \frac{\text{Recall} + \text{Specificity}}{2} \\[1.5em]
\text{MCC} &= \frac{\text{TP} \cdot \text{TN} - \text{FP} \cdot \text{FN}}{\sqrt{(\text{TP}+\text{FP})(\text{TP}+\text{FN})(\text{TN}+\text{FP})(\text{TN}+\text{FN})}}
\end{aligned}
$$

Log Loss for binary classification, where $p_i$ is the predicted probability of the positive class:

$$
\text{LogLoss} = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \ln(p_i) + (1 - y_i) \ln(1 - p_i) \right]
$$

## Example: why accuracy can mislead

Fraud detection with 1,000 transactions, of which only 20 are fraud:

|                     | Predicted fraud | Predicted legit |
| ------------------- | --------------- | --------------- |
| **Actual fraud**    | TP = 12         | FN = 8          |
| **Actual legit**    | FP = 10         | TN = 970        |

| Metric | Calculation | Value |
|--------|-------------|-------|
| Accuracy | (12 + 970) / 1000 | **98.2%** |
| Precision | 12 / (12 + 10) | **54.5%** |
| Recall | 12 / (12 + 8) | **60.0%** |
| Specificity | 970 / (970 + 10) | **99.0%** |
| F1-Score | 2·12 / (2·12 + 10 + 8) | **57.1%** |
| Balanced Accuracy | (0.600 + 0.990) / 2 | **79.5%** |
| MCC | (12·970 − 10·8) / √(22·20·980·978) | **0.563** |

Accuracy looks excellent, but the model finds only 60% of the fraud, and 45% of its alerts are false alarms.

A model that **always predicts "legit"** scores 98.0% accuracy, yet it has Recall 0% and F1 0%. With imbalanced classes, accuracy alone says almost nothing.

## Python

```python
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    balanced_accuracy_score, matthews_corrcoef, confusion_matrix,
    classification_report,
)

y_true = np.array([1] * 20 + [0] * 980)
y_pred = np.array([1] * 12 + [0] * 8 + [1] * 10 + [0] * 970)

print(confusion_matrix(y_true, y_pred))          # [[970  10]
                                                 #  [  8  12]]
print(accuracy_score(y_true, y_pred))            # 0.982
print(precision_score(y_true, y_pred))           # 0.545
print(recall_score(y_true, y_pred))              # 0.600
print(f1_score(y_true, y_pred))                  # 0.571
print(balanced_accuracy_score(y_true, y_pred))   # 0.795
print(matthews_corrcoef(y_true, y_pred))         # 0.563
print(classification_report(y_true, y_pred))     # all per-class metrics at once
```

The threshold-free metrics ([[ROC-AUC]], [[PR-AUC]], log loss, Brier score) need **predicted probabilities**, not class labels: use `roc_auc_score(y, proba)`, `average_precision_score(y, proba)` (the PR-AUC estimate), `log_loss(y, proba)` and `brier_score_loss(y, proba)`.

## Precision vs. Recall

Raising the decision threshold gives **fewer but surer** positives (precision up, recall down). Lowering it gives the opposite. The F1-Score and the PR curve summarize this trade-off.

| Priority | Favor | Example |
|----------|-------|---------|
| Do not miss positives | **Recall** | Cancer screening, fraud detection |
| Do not raise false alarms | **Precision** | Spam filter, automatic account blocking |
| Both matter equally | **F1-Score** | General imbalanced problems |

## Multiclass and multilabel

Precision, Recall and F1 are computed per class and then combined with an `average` option:

| Average | How | Use when |
|---------|-----|----------|
| **macro** | Unweighted mean over classes | Every class matters equally, including rare ones |
| **micro** | Pools all TP, FP and FN | You care about overall instance-level performance |
| **weighted** | Mean weighted by class size | You want to reflect the class distribution |

For ROC-AUC, scikit-learn uses `multi_class="ovr"` (one-vs-rest) or `"ovo"` (one-vs-one).

## How to choose

| Situation | Recommended metrics |
|-----------|---------------------|
| Balanced classes | Accuracy, F1 |
| Imbalanced classes | Precision, Recall, F1, PR-AUC, MCC, Balanced Accuracy |
| Rare positives (fraud, disease) | **Recall**, **PR-AUC** |
| Compare models without choosing a threshold | ROC-AUC, PR-AUC |
| You need trustworthy probabilities | Log Loss, Brier Score, calibration plots |
| Unequal error costs | A **cost-weighted** metric, or tune the threshold on the cost |

>[!warning] ROC-AUC can look good on highly imbalanced data because true negatives dominate the false positive rate. Check **PR-AUC** as well.

## Classification vs. regression metrics

| | Classification | Regression |
|---|---|---|
| Target | A class | A number |
| Compares | Predicted class with the real class | Predicted value with the real value |
| Metrics | This note | [[Evaluating regression model metrics]] |

## Related

- [[Confusion Matrix]]
- [[Accuracy]]
- [[Precision]]
- [[Recall]]
- [[F1-Score]]
- [[ROC-AUC]]
- [[PR-AUC]]
- [[Model Evaluation]]
- [[Evaluating regression model metrics]]
