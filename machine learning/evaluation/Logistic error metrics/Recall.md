#metric #classification

**Recall** (also called sensitivity or true positive rate) measures how many of the actual positive items the model found. It answers: *"Of everything that was really positive, how much did the model catch?"*

$$
\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{\text{hits}}{\text{possible hits}}
$$

- **TP** (True Positive): predicted positive and actually positive
- **FN** (False Negative): predicted negative but actually positive (a missed positive)

The denominator ($\text{TP} + \text{FN}$) is everything that is *actually* positive. Range: 0 to 1 (or 0% to 100%).

## Recall vs Precision

Unlike [[Precision]], which is about the total number of attempts (it looks at $\text{FP}$), recall is about the total number of possible hits (it looks at $\text{FN}$).

| Metric | Question | Penalizes |
|---|---|---|
| [[Precision]] | Of everything predicted positive, how much was correct? | False positives |
| [[Recall]] | Of everything actually positive, how much was found? | False negatives |

## Examples

- Fishing: I caught 70 fish and there were 100 in the lake.

$$
\text{Recall} = \frac{70}{100} = 0.70 \; (70\%)
$$

- Car recall: when a manufacturer finds a defect in a batch, it recalls every car that may have the defect. The goal is to miss none (high recall), even if some recalled cars turn out to be fine (lower precision).

## Interpretation

- A high recall means the model rarely misses a real positive: few false negatives.
- Recall alone can be gamed: a model that predicts positive for everything reaches 100% recall (no false negatives) but has terrible precision. Always read it together with [[Precision]].
- Lowering the decision threshold usually increases recall and decreases precision (the precision-recall trade-off). [[F1-Score]] combines both into a single number.

## When to prioritize recall

Use recall when a false negative is costly:

- Medical screening: missing a sick patient is worse than a false alarm.
- Fraud and intrusion detection: a missed attack costs more than a manual review.
- Safety systems and content moderation of harmful content.
- RAG retrieval: if the relevant chunk is not retrieved, the LLM cannot use it (context recall).

## Edge cases and multi-class

- If there are no actual positives ($\text{TP} + \text{FN} = 0$), recall is undefined (0/0). Libraries usually return 0 with a warning.
- For multi-class problems, recall is computed per class and then averaged:
  - **Macro**: unweighted mean across classes (treats all classes equally)
  - **Weighted**: mean weighted by class support
  - **Micro**: computed from the global TP and FN counts (equals accuracy in single-label multi-class)

## Code

```python
from sklearn.metrics import recall_score

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 0, 1, 1, 1]

recall_score(y_true, y_pred)  # TP=3, FN=1 -> 0.75

# multi-class
recall_score(y_true, y_pred, average="macro")
```

## Related

- [[Confusion Matrix]] - source of TP, FP, FN, TN
- [[Precision]]
- [[F1-Score]]
- [[Accuracy]]
- [[Evaluation classification model metrics]]
