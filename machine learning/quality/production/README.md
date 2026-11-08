Model quality in **production**: how to keep a deployed model reliable over time. Unlike software, a model ages even when nothing in the code changes, because the world it learned from keeps changing. For quality before deployment, see [[machine learning/quality/development/README|Development quality]].

## Core idea

> **Drift ≠ degradation.** Drift is the *change* (in data or in the concept); degradation is the *consequence* (a drop in the metric). Monitoring only the final metric is not enough, because labels (ground truth) can take days or months to arrive.

So production monitoring has two layers:

1. **Fast signals, no ground truth:** feature distributions, prediction distributions, model confidence, feature ranges. Used as an early alert (see [[Population Stability Index (PSI)]]).
2. **Confirmation, with ground truth:** [[Accuracy]], [[Precision]], [[Recall]], [[F1-Score]], [[ROC-AUC]] computed once real labels arrive. See [[Monitor Accuracy in Production Continuously]].

## Notes in this folder

| Note | What it covers | Status |
|---|---|---|
| [[Model drift]] | Performance loss because data or concept changed after training; detection, mitigation, when to retrain | Detailed |
| [[champion and challenger]] | Promote a new (challenger) model only if it beats the current (champion) on the metrics; evaluation modes, promotion rule, pitfalls | Detailed |
| [[concept drift]] | Change in the relationship between inputs and the target (concept drift); why it is hard to detect and how to mitigate | Detailed |
| [[model performance monitoring]] | Overview of monitoring a deployed model; open loop vs closed loop | Detailed |
| [[Open loop monitoring]] | Monitoring without ground truth: input and prediction drift, data quality | Detailed |
| [[Closed loop monitoring]] | Monitoring with ground truth feedback: real metrics, retraining | Detailed |

## Drift types

Model drift = [[data drift]] + [[concept drift]]

| Type | What changed | Example |
|---|---|---|
| Data drift | Distribution of the input features | A new customer segment starts using the product |
| Target drift | Distribution of the target / predicted classes | Fraud rate rises |
| Concept (context) drift | Relationship between features and target | Fraudsters change technique |

## Typical lifecycle

1. Record predictions and inputs in production
2. Monitor fast signals ([[Population Stability Index (PSI)]], KS-test, confidence)
3. Confirm with ground truth when labels arrive
4. Alert when the metric falls beyond a threshold
5. Retrain on recent data and validate against the current model ([[champion and challenger]])
6. Deploy the winner, keep the model history for rollback

## Related

- [[machine learning/quality/development/README|Development quality]]: metrics and validation before deployment
- [[Overfitting]]: a training-time problem, not to be confused with drift
- [[machine learning/concepts/Ground Truth|Ground Truth]]
- [[Evaluation classification model metrics]]
- [[evaluation]]
- [[Machine Learning|Machine Learning]]
