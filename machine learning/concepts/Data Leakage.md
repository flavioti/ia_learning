# Data Leakage

**Data leakage** happens when information the model would not have at prediction time gets into training. The model looks great in evaluation but fails in production, because it learned from information that does not exist there.

---

## Common Causes

| Cause | Description | Example |
|---|---|---|
| **Preprocessing before the split** | Statistics computed on the whole dataset influence training | Fitting a scaler or imputer on all rows, then splitting |
| **Target leakage** | A feature is derived from the label or is only known after the outcome | `collections_status` used to predict loan default |
| **Temporal leakage** | The model trains on the future to predict the past | Random split of a time series |
| **Duplicates across splits** | The same record or entity appears in train and test | Same user in both sets |

---

## Example

```python
# Leaky: the scaler sees test rows before the split
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
X_train, X_test = train_test_split(X_scaled)
```

The test rows already shaped the mean and variance, so the test score is slightly optimistic.

```python
# Correct: split first, fit on training data only
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)
```

---

## How to Detect

- Suspiciously high scores (for example, near-perfect AUC).
- One feature dominating importance.
- A large drop in performance between evaluation and production.
- Features that would not be available at prediction time.

---

## How to Prevent

- Split first, then fit all transformers (scaling, imputation, encoding, selection) on the training set only.
- Use a `Pipeline` so cross-validation refits transformers in every fold.
- Use time-based splits for temporal data.
- Deduplicate and group by entity (for example, `GroupKFold`).
- Review each feature: "Would I know this at prediction time?"

---

## Related

- [[feature engineering]]
- [[train dataset and test dataset]]
- [[Overfitting]]
- [[Training-Serving Skew]]
