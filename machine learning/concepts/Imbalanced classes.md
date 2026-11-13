---
aliases:
  - Imbalance
  - Class imbalance
  - Imbalanced data
  - imbalanced
---
#concept #classification #evaluation #imbalanced-data

# Imbalanced classes

A classification dataset is **imbalanced** when one class has far fewer examples than the others. The rare class (the **minority class**) is usually the one you care about, and the common one is the **majority class**.

| Problem | Rare class | Typical share |
|---|---|---|
| [[Churn]] | Customer leaves | about 11% in the example |
| [[Credit approval]] | Applicant defaults | about 11.5% in the example |
| Fraud detection | Fraudulent transaction | often under 1% |
| Medical screening | Disease present | often a few percent |
| Defect detection | Faulty item | often under 1% |

The **imbalance ratio** is majority count divided by minority count. A 95/5 split has a ratio of 19 to 1. Imbalance is common in real problems, and it is not a bug in the data: it reflects how rare the event is.

>[!tip] The first thing to do on any classification dataset is to look at the class balance: `y.value_counts(normalize=True)`.

## Why it is a problem

**1. Accuracy lies.** A model that always predicts the majority class looks excellent. With 5% positives, "always negative" is **95% accurate** and finds **no positives at all**. See [[Accuracy]].

**2. The model has little to learn from.** The loss is dominated by the majority class, so the model can lower its error by mostly ignoring the rare class. The default decision boundary ends up in the wrong place for it.

**3. The default threshold of 0.5 is wrong.** Probabilities of the rare class are naturally low, so few cases ever cross 0.5.

**4. Small test sets are unreliable.** With few positives, one or two extra cases change recall a lot. Precision and recall for the rare class have a lot of noise.

## Recommended order of work

1. **Measure the balance** and decide what the rare class is worth.
2. **Use the right metrics** (below), not accuracy.
3. **Split with stratification**, and by date if time matters.
4. **Train a [[baseline]] without any rebalancing** and get a probability for every case.
5. **Tune the threshold** by business cost.
6. Only if the **ranking** is still poor, try class weights or resampling, and check the calibration afterwards.

## 1. Use the right metrics

| Metric | Why it helps or hurts |
|---|---|
| [[Accuracy]] | Misleading. Avoid it as the main metric |
| [[Precision]] | Of the cases flagged, how many are really positive |
| [[Recall]] | Of all the positives, how many were found |
| [[F1-Score]] | One number for precision and recall at one threshold |
| [[PR-AUC]] | Precision and recall over all thresholds. The baseline of a random model equals the positive rate, so compare against it |
| [[ROC-AUC]] | Ranking quality over all thresholds. Can look good even when precision is poor, because false positives are divided by the many negatives |
| [[Confusion Matrix]] | Shows exactly which errors you make |
| Lift or recall at top N% | How concentrated the positives are at the top of the ranking |
| Calibration, Brier score | Whether a predicted 20% really means 20% (matters when the probability is used) |

See [[Evaluating classification model metrics]].

## 2. Split with stratification

A **stratified** split keeps the same share of the rare class in the train, validation and test sets. Without it, a small split can have very few positives, or none.

In the example below, a 40-row test split taken from data with 5% positives (two expected) gave 1, 2, 1, 1 and 3 positives with random splits over five seeds, and exactly 2 every time with stratification. Use `stratify=y` in `train_test_split` and `StratifiedKFold` for cross-validation. See [[train dataset and test dataset]] and [[K-Fold Cross-Validation]].

If the data has a time order, split by date instead, and keep the test set with the **natural** class balance, because that is what production looks like. Never rebalance the validation or test set.

## 3. Choose the threshold by cost

Most models output a probability, and the **threshold** turns it into a decision. The two mistakes rarely cost the same:

- **False negative** (missing a positive): a missed fraud, defaulter or churner.
- **False positive** (a false alarm): a wasted check, offer or call.

Pick the threshold that minimizes the total expected cost, or that reaches the recall you need, on **validation data**. Then confirm it on the test set. This often helps more than any resampling technique, and it does not change the probabilities.

## 4. Rebalance the training data (optional)

| Technique | What it does | Notes |
|---|---|---|
| **Class weights** (`class_weight="balanced"`) | Errors on the minority class count more in the loss | Simple. No data is changed |
| **Random oversampling** | Repeats minority rows until the classes are equal | Can overfit to the repeated rows |
| **SMOTE** and variants | Creates synthetic minority rows between real neighbors | Do it on the **training set only**. It can create unrealistic points |
| **Random undersampling** | Removes majority rows | Fast, but throws away information |
| **Better algorithms or losses** | Boosting with `scale_pos_weight`, focal loss, balanced bagging | Often equivalent to class weights |
| **Collect more minority data** | More real rare examples | The strongest fix when possible |

>[!warning] **Resample only the training data,** and only **after** the split (inside each cross-validation fold). Resampling before the split puts copies of the same rows in train and test, which is [[Data Leakage]] and gives a falsely high score.

### The catch: rebalancing distorts probabilities

These techniques make the model act as if the classes were balanced, so its probabilities are **too high** for the minority class. The ranking does not improve, but the probabilities no longer match reality. If the probability feeds pricing, budgets or provisioning, do not rebalance, or recalibrate the output afterwards.

## Example (synthetic data)

An illustration with generated data, **not real data**: 40,000 rows, 12 features, 5.4% positives. It is split 60/20/20 into train, validation and test sets with stratification (the test set has 8,000 rows and 433 positives). The model is a logistic regression with scaled features.

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample

def lr(**kw):
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, **kw))

# X_train, X_val, X_test, y_train, y_val, y_test: stratified split, test set keeps the natural balance
default  = lr().fit(X_train, y_train)
weighted = lr(class_weight="balanced").fit(X_train, y_train)

# Random oversampling of the minority class, on the training set only
pos, neg = X_train[y_train == 1], X_train[y_train == 0]
pos_up = resample(pos, replace=True, n_samples=len(neg), random_state=0)
X_over = np.vstack([neg, pos_up])
y_over = np.r_[np.zeros(len(neg)), np.ones(len(neg))]
oversampled = lr().fit(X_over, y_over)

# Cost-based threshold, chosen on validation data: a missed positive costs 10x a false alarm
C_FN, C_FP = 10, 1
def cost(y_true, p, t):
    return C_FN * ((p < t) & (y_true == 1)).sum() + C_FP * ((p >= t) & (y_true == 0)).sum()

p_val = default.predict_proba(X_val)[:, 1]
grid = np.linspace(0.01, 0.9, 90)
threshold = grid[np.argmin([cost(y_val, p_val, t) for t in grid])]
```

A model that always predicts the majority class gets **94.6% accuracy and a recall of 0**. Results on the test set:

| Approach                                    | Threshold | Accuracy | PR-AUC | Brier     | Precision | Recall |
| ------------------------------------------- | --------- | -------- | ------ | --------- | --------- | ------ |
| Default logistic regression                 | 0.5       | 0.948    | 0.282  | **0.046** | 1.000     | 0.032  |
| Class weights                               | 0.5       | 0.696    | 0.252  | 0.202     | 0.110     | 0.654  |
| Random oversampling                         | 0.5       | 0.692    | 0.251  | 0.203     | 0.109     | 0.656  |
| Random undersampling                        | 0.5       | 0.681    | 0.225  | 0.205     | 0.106     | 0.654  |
| Default, threshold by best F1 on validation | 0.174     | 0.935    | 0.282  | 0.046     | 0.369     | 0.286  |
| Default, threshold by cost on validation    | 0.130     | 0.908    | 0.282  | 0.046     | 0.262     | 0.381  |

The ROC-AUC is 0.742 for every model except undersampling (0.737). The PR-AUC of a random model would be the positive rate, about 0.054.

What the results show:

- **The default model is useless at 0.5 despite 94.8% accuracy.** It finds only 3% of the positives. It is correct when it flags a case (precision 1.0), but it almost never does, so it is no better than the model that always predicts "negative".
- **Resampling and class weights do not improve the ranking.** The ROC-AUC is the same (0.742) and the PR-AUC is slightly **lower**. What changes is that, at 0.5, the models now flag many more cases (recall 0.65), at the price of low precision.
- **They damage the probabilities.** The Brier score is about four times worse (0.046 to 0.20), and accuracy drops from 0.948 to about 0.69.
- **Moving the threshold gets a similar trade-off without damaging the probabilities.** The Brier score stays at 0.046. The threshold is the lever that changes the business result.

The cost of errors on the test set, with the made-up costs above (a missed positive costs 10 and a false alarm costs 1):

| Decision | Total cost |
|---|---|
| Predict "negative" for everyone | 4,330 |
| Default model, threshold 0.5 | 4,190 |
| Default model, cost-based threshold (0.13) | **3,144** |

The cost-based threshold lowers the cost by about 25%, with no resampling at all. The costs here are invented. In practice they come from the loss per missed case and the cost of a check.

## Imbalance is not always the problem

- A low ranking power (a ROC-AUC of 0.74 here) is a **signal** problem, not an imbalance problem. Rebalancing cannot add information that the features do not contain. Better features help more.
- Strong models such as [[Gradient Boosting]] often work well on imbalanced data without any resampling. Compare against the simple baseline first.
- With **extreme imbalance** (for example 1 in 10,000), classification can become **anomaly detection**, where the model learns what normal looks like and flags the exceptions.

## Common pitfalls

- Reporting accuracy
- Resampling before the split, or rebalancing the validation and test sets
- Using the default 0.5 threshold
- Using rebalanced probabilities as if they were real probabilities
- Trusting metrics from a test set with very few positives. Report uncertainty, and prefer cross-validation
- Using random splits when the data has a time order
- Tuning the threshold on the test set instead of on validation data
- Reaching for SMOTE before checking the baseline and the threshold

## Related

- [[Churn]]
- [[Credit approval]]
- [[Logistic regression]]
- [[Gradient Boosting]]
- [[Evaluating classification model metrics]]
- [[Confusion Matrix]]
- [[PR-AUC]]
- [[ROC-AUC]]
