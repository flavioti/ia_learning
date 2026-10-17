# Discrete Variable

A **discrete variable** is a numeric variable that takes only **specific, separate values**, usually whole numbers obtained by **counting**. There are gaps between possible values: a user can make 2 or 3 purchases, never 2.5.

Related: [[Continuous Variable]] · [[Categorical columns]] · [[feature engineering]]

---

## Key Characteristics

- Values are **countable** (finite, or countably infinite like 0, 1, 2, …)
- Obtained by **counting**, not measuring
- Numeric, so arithmetic is meaningful (mean, sum, difference)
- Often **non-negative** (counts cannot be below 0)
- Often **skewed** with many small values and a long right tail
- Described by discrete distributions: Bernoulli, Binomial, Poisson, Negative Binomial, Geometric

---

## Examples in ML

| Variable | Context | Possible values |
|---|---|---|
| Number of purchases | Churn / recommendation | 0, 1, 2, … |
| Number of failed logins | Fraud / security | 0, 1, 2, … |
| Number of tokens in a prompt | LLM | 1, 2, … |
| Number of layers / heads | Neural network hyperparameter | 1, 2, 4, 8, … |
| Number of children | Credit scoring | 0, 1, 2, … |
| Clicks per session | CTR models | 0, 1, 2, … |
| Class label (0 to 9) | Digit classification | integers only, but see warning below |

---

## Discrete vs. Categorical (Common Confusion)

A number stored as an integer is **not necessarily** a discrete variable in the ML sense.

| | Discrete variable | Categorical variable |
|---|---|---|
| Meaning of the number | A real **count** | A **label** (ID) |
| Arithmetic makes sense? | ✅ Yes (4 is twice 2) | ❌ No |
| Example | `num_purchases = 4` | `zip_code = 90210`, `class_id = 7` |
| Treatment | Numeric feature | Encode (one-hot, target, embeddings). See [[Categorical columns]] |

Rule of thumb: if averaging the values would be meaningless, it is categorical, not discrete.

An **ordinal** variable (rating 1 to 5) sits in between. It is ordered but gaps are not necessarily equal, so it can be treated as numeric or as categorical depending on the model.

---

## How It Affects ML

### Modeling

| Aspect | Guidance |
|---|---|
| **Regression target (counts)** | Plain linear regression can predict negatives and fractions. Prefer **Poisson** or **Negative Binomial** regression (overdispersed counts) |
| **Zero-heavy counts** | Use **zero-inflated** or **hurdle** models |
| **Binary target** | Logistic regression / classifiers (Bernoulli) |
| **Loss functions** | Poisson deviance (`PoissonRegressor`, XGBoost `count:poisson`, LightGBM `poisson`), instead of MSE |
| **Tree-based models** | Handle discrete features natively by splitting on thresholds |
| **Linear / distance / NN models** | Usually need scaling, especially when ranges differ a lot |

### Feature engineering

| Technique | When to use | Note |
|---|---|---|
| **Log transform** (`log1p`) | Right-skewed counts with a long tail | `log1p` handles zeros |
| **Scaling** (standardization / min-max) | Linear models, KNN, SVM, neural networks | Not needed for trees |
| **Capping / winsorizing** | Extreme outliers (a bot with 10,000 clicks) | Keeps the model stable |
| **Binning** | Non-linear effects, or when exact counts are noisy | See [[Discretization]] |
| **Treat as categorical** | Very few distinct values (e.g. 1, 2, 4, 8 heads) | One-hot or ordinal encoding |
| **Ratios / rates** | Counts depend on exposure | `clicks / impressions`, not raw `clicks` |

### Pitfall: counts without exposure

Raw counts are not comparable if the observation windows differ. 10 purchases in 1 week is not the same as 10 in 1 year. Use a rate, or an **offset** in Poisson regression.

---

## Code Example

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split

# Count target: number of support tickets per customer
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "tenure_months": rng.integers(1, 60, 1000),
    "num_products": rng.integers(1, 6, 1000),     # discrete feature
})
df["tickets"] = rng.poisson(lam=0.5 + 0.05 * df["num_products"])  # discrete target

# Feature engineering for a skewed discrete feature
df["log_tenure"] = np.log1p(df["tenure_months"])

X = df[["log_tenure", "num_products"]]
y = df["tickets"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Poisson regression respects the nature of count data (non-negative predictions)
model = PoissonRegressor(alpha=1e-4)
model.fit(X_train, y_train)
print(model.predict(X_test)[:5])
```

---

## Summary

- Discrete = **countable** numeric values with gaps.
- Not the same as categorical: discrete numbers carry **magnitude**.
- For count targets, use Poisson-family models, not plain linear regression.
- For skewed counts, use `log1p`, capping and rates.
