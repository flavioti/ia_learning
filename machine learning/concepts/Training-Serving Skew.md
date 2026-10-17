# Training-Serving Skew

**Training-serving skew** is a mismatch between how features are computed during training and during inference. The model receives inputs in production that look different from what it was trained on, even though the underlying data is the same.

The result is that production performance is worse than evaluation performance, often without any error being raised.

---

## Common Causes

| Cause | Description | Example |
|---|---|---|
| **Different code paths** | Training and serving implement the transformations separately | Pandas in a notebook vs. reimplemented logic in Java or SQL |
| **Different data sources** | Different freshness or definitions between batch and live data | Warehouse table for training, live API for serving |
| **Missing transformations** | A step is skipped at inference time | Scaler or encoder not applied |
| **Inconsistent null handling** | Missing values are treated differently | Median imputation in training, `0` in production |
| **Time-travel errors** | Training features use data updated after the event | Aggregates that include future records |

---

## Example

In training, a missing `age` is imputed with the median (for example, 35). In production, the service passes `0`. The model sees values it never learned from and predicts poorly.

---

## How to Detect

- Compare feature distributions between training data and live traffic.
- Log serving features and recompute them offline to compare.
- Monitor drift metrics (see [[Population Stability Index (PSI)]]).
- Watch for a gap between offline metrics and online metrics.

---

## How to Prevent

- Use one shared transformation code path, such as a saved scikit-learn `Pipeline` loaded at serving time.
- Use a feature store that serves the same feature definitions offline and online (see [[Offline Feature Store]] and [[Online Feature Store]]).
- Use point-in-time correct joins when building training data.
- Add input validation and schema checks at inference time.

---

## Related

- [[feature engineering]]
- [[Data Leakage]]
- [[Population Stability Index (PSI)]]
