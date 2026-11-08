---
aliases:
  - Context drift
---
#monitoring #drift

**Context drift** (more commonly called **concept drift**) is a change in the relationship between the inputs and the target after the model was trained. The meaning of the data changes, even if the data itself looks the same.

$$
P_{\text{train}}(y \mid X) \neq P_{\text{prod}}(y \mid X)
$$

It is one of the two components of [[Model drift]], together with [[data drift]] (which changes $P(X)$).

## Why it is dangerous

The input distributions can stay identical, so fast signals that need no labels ([[Population Stability Index (PSI)]], KS-test) may not raise any alarm. The model keeps receiving "normal" inputs and keeps answering confidently, but the answers are wrong. Only [[machine learning/concepts/Ground Truth|Ground Truth]] confirms it.

## Examples

- **Fraud:** the same transaction profile used to be legitimate, but fraudsters changed technique and now it is fraud.
- **Credit risk:** after an economic shock, the same income and debt profile has a much higher default rate.
- **Churn:** a competitor launches a cheaper plan, so the same usage pattern no longer predicts that a customer stays.
- **Spam:** the same words that marked spam are now used in legitimate marketing.
- **Language and recommendations:** slang, trends and tastes change what a "relevant" result means.

## Data drift vs context drift

| | Data drift | Context drift (concept drift) |
|---|---|---|
| What changes | $P(X)$: the inputs | $P(y \mid X)$: the input-to-target relationship |
| Detectable without labels | Yes ([[Population Stability Index (PSI)]], KS-test) | Mostly no: needs ground truth |
| Always hurts the model | No (only if it reaches regions the model handles badly) | Yes, by definition |
| Typical fix | Retrain, or fix the pipeline if it is a data bug | Retrain on recent data; the old pattern is obsolete |

Both can happen at the same time, and a pure change in $P(y)$ is called target (label) drift.

## How it appears over time

- **Sudden:** abrupt change (new regulation, a pandemic, a pricing change)
- **Gradual:** the old and the new pattern coexist for a while
- **Incremental:** small continuous steps
- **Recurring:** the pattern comes back periodically (seasonality)

Seasonality that is expected and repeats is not necessarily drift: put it in the features or in the training data.

## How to detect it

1. **Ground-truth metrics:** a sustained drop in [[Accuracy]], [[Precision]], [[Recall]], [[F1-Score]] or [[ROC-AUC]] over time (see [[model performance monitoring]]). This is the primary signal.
2. **Delayed labels:** compare windows of recent labeled data against the baseline measured at deploy time.
3. **Indirect signals:** a drop in model confidence, or a change in the share of predicted classes without a matching change in the inputs, suggests concept drift. They are hints, not proof.
4. **Error analysis by segment:** the drop often starts in one segment before it shows up in the global metric.

## How to mitigate

- Retrain on recent data, possibly weighting recent examples more or using a sliding window
- Promote the new model safely with [[champion and challenger]]
- Revisit the features: if the old signal stopped being predictive, a new one may be needed
- Shorten the label feedback loop, since detection speed is limited by label delay

## Related

- [[Model drift]]
- [[data drift]]
- [[model performance monitoring]]
- [[champion and challenger]]
- [[Population Stability Index (PSI)]]
