#metric #classification 

**Precision** measures how many of the items a model predicted as positive are actually positive. It answers: *"When the model says positive, how often is it right?"*

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{\text{hits}}{\text{attempts}}
$$

- **TP** (True Positive): predicted positive and actually positive
- **FP** (False Positive): predicted positive but actually negative

The denominator ($\text{TP} + \text{FP}$) is everything the model *predicted* as positive. Range: 0 to 1 (or 0% to 100%).

## Precision vs Recall

Unlike [[Recall]], which is about the total number of possible hits (it looks at $\text{FN}$), precision is about the total number of attempts (it looks at $\text{FP}$).

| Metric | Question | Penalizes |
|---|---|---|
| [[Precision]] | Of everything predicted positive, how much was correct? | False positives |
| [[Recall]] | Of everything actually positive, how much was found? | False negatives |

## Example

Fishing: I cast the rod 160 times and catch 70 fish.

$$
\text{Precision} = \frac{70}{160} \approx 0.44 \; (44\%)
$$

Every cast is an attempt (a positive prediction); only 70 were hits.

## Interpretation

- A high precision means the model rarely raises false alarms: few false positives when predicting the positive class.
- Precision alone can be gamed: a model that predicts positive only for the single most certain case can reach 100% precision while missing almost every real positive. Always read it together with [[Recall]].
- Raising the decision threshold usually increases precision and decreases recall (the precision-recall trade-off). [[F1-Score]] combines both into a single number.

## When to prioritize precision

Use precision when a false positive is costly:

- Spam filter: sending a legitimate email to spam is worse than letting some spam through.
- Fraud alerts that trigger an account block.
- Recommendation or search results where irrelevant items hurt user trust.
- RAG retrieval: irrelevant retrieved chunks pollute the LLM context (context precision).

## Edge cases and multi-class

- If the model makes no positive predictions ($\text{TP} + \text{FP} = 0$), precision is undefined (0/0). Libraries usually return 0 with a warning.
- For multi-class problems, precision is computed per class and then averaged:
  - **Macro**: unweighted mean across classes (treats all classes equally)
  - **Weighted**: mean weighted by class support
  - **Micro**: computed from the global TP and FP counts

## Code

```python
from sklearn.metrics import precision_score

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 0, 1, 1, 1]

precision_score(y_true, y_pred)  # TP=3, FP=1 -> 0.75

# multi-class
precision_score(y_true, y_pred, average="macro")
```

## Related

- [[Confusion Matrix]] - source of TP, FP, FN, TN
- [[Recall]]
- [[F1-Score]]
- [[Accuracy]]
- [[Evaluation classification model metrics]]
