Model drift = [[data drift]] + [[concept drift]]

## What is it?

**Model drift** = loss of model performance in production because the world (the data, or the relationships between variables) changed after training. It is not a code bug: the model keeps running exactly the same, but what it learned stops being valid.

Unlike conventional software, a model **ages** even when nothing is changed.

> **Drift ≠ degradation.** Drift is the *change* (in the data or in the concept); degradation is the *consequence* (a drop in the metric). Data drift can happen without any performance drop, so monitoring only the final metric is not enough.

**Examples:**
- 🏠 Real estate prices: model trained before a sharp price increase
- 📱 Fraud: fraudsters change technique
- 💰 Credit score: the economy changes and so do payment patterns
- 📊 Sales forecast: market and competition evolve

---

## Types of drift

Terms differ between sources. In terms of probabilities, with inputs $X$ and target $y$:

| Type | What changes | Also called | Example |
|---|---|---|---|
| **Data drift** | $P(X)$: distribution of the inputs | Covariate shift | A new customer segment starts using the product |
| **Target drift** | $P(y)$: distribution of the target or predicted classes | Label (prior) shift | The fraud rate rises |
| **Concept drift** | $P(y \mid X)$: relationship between inputs and target | Context drift | Same transaction profile, but fraudsters now behave differently |

Concept drift is the most dangerous: the inputs can look the same, so fast signals without labels may not catch it. Only ground truth confirms it.

### How the change happens over time

| Pattern | Description | Example |
|---|---|---|
| **Sudden** | Abrupt change | A new regulation, a pandemic, a pricing change |
| **Gradual** | The old and the new pattern coexist for a while | A new competitor slowly takes share |
| **Incremental** | Small continuous steps | Sensor wear |
| **Recurring / seasonal** | The pattern comes back periodically | Holiday shopping |

> **Seasonality is not necessarily drift.** If the pattern is expected and repeats (weekday vs weekend, holiday peak), include it in the training data or in the features, and compare against the same period, not against the previous week. Otherwise every season triggers a false alarm.

---

## How to detect it?

Detection has two layers. Signals **without ground truth** are fast and work as an alert; signals **with ground truth** are slow and serve as confirmation (see [[Monitor Accuracy in Production Continuously]]). The reason for layer 1 is label delay: the true label may take days, weeks or months to arrive.

### Layer 1: Fast signals (without [[machine learning/concepts/Ground Truth|Ground Truth]])

| Signal | What to observe | Speed |
|---|---|---|
| **Feature distributions** | KS-test (continuous), chi-square (categorical), or [[Population Stability Index (PSI)]] (both, after binning continuous variables) | ⚡ Seconds/minutes |
| **Prediction distribution** | The share of each predicted class changed | ⚡ Minutes |
| **Model confidence** | Mean maximum probability dropped | ⚡ Seconds |
| **Feature range** | Values outside the training min/max | ⚡ Seconds |

```python
from scipy.stats import ks_2samp

# Data drift on a continuous feature
statistic, pvalue = ks_2samp(X_train["age"], X_prod["age"])
if pvalue < 0.05:
    print("⚠️ Possible data drift in 'age'")

# Values outside the range seen in training
outside = (X_prod["price"] < X_train["price"].min()) | (X_prod["price"] > X_train["price"].max())
if outside.mean() > 0.01:  # more than 1% of rows
    print("⚠️ Feature 'price' outside the training range")
```

**KS-test caveats:**
- With very large samples, the p-value becomes tiny even for irrelevant differences. Combine it with an effect size (the KS statistic) or with PSI.
- When testing many features, some false alarms are expected. Adjust the threshold (e.g. Bonferroni) or prioritize the most important features.

### Layer 2: Confirmation (with ground truth)

Only possible once the true label shows up, which can take days or weeks.

| Metric | Note |
|---|---|
| [[machine learning/quality/development/Accuracy\|Accuracy]] | Good for balanced classes |
| [[Precision]] / [[Recall]] / [[F1-Score]] | Preferable with imbalanced classes |
| [[ROC-AUC]] | Threshold-independent |

```python
baseline = 0.85  # accuracy measured on the test set at deploy time

accuracies = {"day_1": 0.85, "day_30": 0.82, "day_60": 0.78, "day_90": 0.71}

if accuracies["day_90"] < baseline * 0.95:  # relative drop > 5%
    print("❌ Degradation confirmed")
```

### When labels take too long

If the ground truth is very delayed or never arrives, performance can be *estimated* without labels. Open-source libraries such as Evidently, NannyML and Alibi Detect cover drift detection, and NannyML also estimates performance from the model's own confidence. Treat these estimates as an alert, not as proof.

---

## Impact

Illustrative, the numbers vary by problem. The values below are the same ones used in the code example above:

![Accuracy decay after deployment](model_drift_decay.png)

The accuracy crosses the alert threshold (a relative drop greater than 5%) between day 30 and day 60. By day 90 the drop is already clear, and without action the model becomes less useful every month, which erodes the business value it was built for. The plot is generated by `model_drift_generator.py` (same folder).

---

## How to mitigate?

### 1. Periodic retraining
Retrain on recent data and only promote the new model if it beats the current one on an up-to-date test set. Require a minimum margin or a significance test, so that noise does not trigger a promotion.

```python
MARGIN = 0.01  # minimum gain required to promote

new_model = train(X_recent, y_recent)
if evaluate(new_model, X_test_recent, y_test_recent) > evaluate(current, X_test_recent, y_test_recent) + MARGIN:
    deploy(new_model)
```

(`train`, `evaluate` and `deploy` are placeholders for your own pipeline.)

- ✅ Adapts the model to the new pattern
- ❌ Expensive (collect data, retrain, validate)

### 2. Champion-Challenger
The compare-then-promote step above, formalized: the model in production (*champion*) is evaluated against one or more *challengers*, ideally on live traffic in shadow mode or on a split, and the challenger is promoted only if it surpasses the champion. See [[champion and challenger]]. Challengers are usually produced by the periodic retraining of mitigation 1.

- ✅ Safe promotion, and it makes the retraining decision objective
- ❌ Needs a reliable, recent evaluation set and extra serving cost during the comparison

### 3. Online learning
The model is updated incrementally with the data that arrives. It requires an estimator that supports incremental training.

```python
# e.g. sklearn's SGDClassifier. Classifiers need the full class list on the first call.
model.partial_fit(first_batch.X, first_batch.y, classes=[0, 1])
for batch in streaming_data:
    model.partial_fit(batch.X, batch.y)
```

- ✅ Fast adaptation
- ❌ Can degrade with bad data or delayed labels; hard to audit

### 4. Continuous monitoring with a retraining trigger
Alert when a signal crosses a threshold and trigger retraining (continuous training, CT). Retraining automatically from a single fast signal is risky; prefer using the signal to investigate, and the confirmation (ground truth) to decide.

### 5. Stable features
Prefer variables that change slowly.

```
❌ "Bitcoin price" (changes all the time)
✅ "product category" (stable)
```

Stability is a tie-breaker, not a goal: do not drop a strongly predictive feature just because it moves.

---

## When to retrain?

| Frequency | Use when |
|---|---|
| **Daily** | Very dynamic environment (fraud, pricing) |
| **Weekly** | Moderate change (credit score) |
| **Monthly** | Slow change |
| **On demand** | Drift detected and confirmed |

The right cadence depends on how fast the world changes, how long labels take to arrive, and how much a retraining costs. A fixed schedule is simple and predictable; on-demand retraining avoids waste but depends on good detection, so many teams combine both: a schedule as a floor, plus a confirmed alert as an override.

---

## LLM and embedding systems

The same ideas apply to LLM applications, but the signals are different: the distribution of user prompts and of retrieved documents changes, embeddings drift away from the index, and a provider may update a hosted model version behind the same name. Monitor input topics, embedding distributions and evaluation scores on a fixed test set.

---

## Checklist

- ✅ [[Monitor Accuracy in Production Continuously]]
- ✅ Monitor feature and prediction distributions
- ✅ Monitor model confidence
- ✅ Log predictions to join with the ground truth later
- ✅ Account for seasonality before alerting
- ✅ Alert when the metric drops beyond the threshold (e.g. 5%)
- ✅ Automated retraining with validation before deploy
- ✅ Keep a model history for rollback

---

## Model Drift vs [[Overfitting]]

| Aspect | Model Drift | Overfitting |
|---|---|---|
| **When it happens** | In production, over time | During training |
| **Cause** | The world changed | The model memorized the training data |
| **Signal** | Production metric falls over time | Train >> Test |
| **Solution** | Monitor and retrain | Regularize, simplify |

---

## Summary

| Aspect | Description |
|---|---|
| **Problem** | Performance drops because data or concept changed |
| **Types** | Data drift, target drift, concept drift |
| **Patterns** | Sudden, gradual, incremental, recurring |
| **Fast detection** | Feature/prediction distributions, confidence, [[Population Stability Index (PSI)]] |
| **Confirmation** | Accuracy, F1, Precision, Recall with ground truth |
| **Mitigation** | Retraining, [[champion and challenger]], online learning |

Models are not "set and forget": plan monitoring and retraining from deployment.

[[Evaluating classification model metrics]]
