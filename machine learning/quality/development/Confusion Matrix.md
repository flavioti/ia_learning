---
tags:
  - classic-ml
---
#metric #classification 

A **confusion matrix** compares the model's predictions against the ground truth. It is the fundamental summary for binary and multiclass classification, and nearly every classification metric is derived from its four cells.

For a binary problem with a positive class:

| Actual \ Predicted | Positive | Negative |
|---|---:|---:|
| **Positive** | TP | FN |
| **Negative** | FP | TN |

Where:

- **TP**: true positive — predicted positive and actually positive
- **FP**: false positive — predicted positive but actually negative
- **FN**: false negative — predicted negative but actually positive
- **TN**: true negative — predicted negative and actually negative

## Why it matters

The matrix answers a more useful question than overall accuracy:

- How many cases were correctly identified?
- Which errors are being made?
- Is the model mostly missing positives, or mostly generating false alarms?

This matters when classes are imbalanced or when false positives and false negatives have different business costs.

## Example

Suppose a spam filter is evaluated on 1,000 emails, of which 150 are spam.

| Actual \ Predicted | Spam | Not spam |
|---|---:|---:|
| **Spam** | 120 | 30 |
| **Not spam** | 40 | 810 |

From this table:

- **TP = 120**: spam correctly classified as spam
- **FN = 30**: spam mistakenly classified as not spam
- **FP = 40**: legitimate email incorrectly flagged as spam
- **TN = 810**: legitimate email correctly kept

The matrix also gives the main metrics:

$$
\text{Accuracy} = \frac{TP + TN}{TP + FP + FN + TN} = \frac{120 + 810}{1000} = 0.93
$$

$$
\text{Precision} = \frac{TP}{TP + FP} = \frac{120}{160} = 0.75
$$

$$
\text{Recall} = \frac{TP}{TP + FN} = \frac{120}{150} = 0.80
$$

## Multiclass confusion matrix

For more than two classes, the matrix becomes $k \times k$:

- one row = actual class
- one column = predicted class
- diagonal cells = correct predictions
- off-diagonal cells = misclassifications

This is used for multiclass problems such as image classification or product categorization. For evaluation, you often aggregate metrics such as macro, weighted, or micro averages.

## Interpretation

- A model with a strong diagonal and little off-diagonal error is performing well.
- If the matrix is dominated by **FP**, the model is over-alerting.
- If it is dominated by **FN**, the model is missing positives.
- In high-stakes settings, choose the metric based on the cost of each error type, not just accuracy.

## Code

```python
from sklearn.metrics import confusion_matrix

# y_true: actual labels
# y_pred: predicted labels

cm = confusion_matrix([1, 0, 1, 0, 1], [1, 0, 0, 0, 1])
print(cm)
# [[2, 0],
#  [1, 2]]
```

## Related

- [[Accuracy]]
- [[Precision]]
- [[Recall]]
- [[F1-Score]]
- [[ROC-AUC]]
- [[Evaluating classification model metrics]]
 
