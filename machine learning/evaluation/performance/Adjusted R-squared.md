#regression-metric #metrics #regression #evaluation

## Definition

**Adjusted R-squared** ($\bar{R}^2$) is a version of [[R-squared]] that **penalizes the number of features** in the model. Plain $R^2$ never decreases when you add a feature, even a useless one. Adjusted $R^2$ only increases if the new feature improves the model **more than would be expected by chance**.

>[!tip] Is this extra feature actually helping, or am I just inflating R-squared?

## Math notation

$$
\bar{R}^2 = 1 - \left( 1 - R^2 \right) \frac{n - 1}{n - p - 1}
$$

Where:
- $R^2$ is the regular [[R-squared]]
- $n$ is the number of samples
- $p$ is the number of predictors (features), not counting the intercept

Equivalent form, which shows it compares **unbiased variance estimates** instead of raw sums:

$$
\bar{R}^2 = 1 - \frac{SS_{res} / (n - p - 1)}{SS_{tot} / (n - 1)}
$$

## How the penalty works

The factor $\frac{n - 1}{n - p - 1}$ grows as $p$ grows, which shrinks $\bar{R}^2$. A new feature must raise $R^2$ enough to offset that growth, otherwise adjusted $R^2$ goes down.

## Example

Dataset with $n = 50$ samples:

| Model | Features $p$ | $R^2$ | $\bar{R}^2$ |
|-------|--------------|-------|-------------|
| A: meaningful features | 3 | 0.800 | $1 - 0.2 \cdot \frac{49}{46} \approx$ **0.787** |
| B: A plus 7 noise features | 10 | 0.810 | $1 - 0.19 \cdot \frac{49}{39} \approx$ **0.761** |

Plain $R^2$ rose from 0.800 to 0.810, which suggests that model B is better. Adjusted $R^2$ fell from 0.787 to 0.761, which correctly shows that the 7 extra features added complexity without real value.

## Python

scikit-learn has no built-in adjusted $R^2$, so compute it from `r2_score`:

```python
import numpy as np
from sklearn.metrics import r2_score

def adjusted_r2(y_true, y_pred, n_features):
    n = len(y_true)
    r2 = r2_score(y_true, y_pred)
    return 1 - (1 - r2) * (n - 1) / (n - n_features - 1)

# Formula check with the numbers from the example
n = 50
for p, r2 in [(3, 0.80), (10, 0.81)]:
    print(p, 1 - (1 - r2) * (n - 1) / (n - p - 1))   # 0.787, 0.761
```

## Key properties

| Property | Meaning |
|----------|---------|
| **Always $\le R^2$** | The penalty can only lower the value |
| **Can decrease** | When a feature adds less than chance would, the metric drops |
| **Can be negative** | If the model is very poor and $p$ is large relative to $n$ |
| **Converges to $R^2$** | When $n \gg p$, the penalty factor approaches 1 |
| **Needs $n > p + 1$** | Otherwise the denominator is zero or negative |
| **Unitless** | Comparable across targets, like $R^2$ |

## R-squared vs. Adjusted R-squared

| | [[R-squared]] | Adjusted R-squared |
|---|---|---|
| Adding a useless feature | Stays the same or goes up | Goes down |
| Accounts for number of features | ❌ No | ✅ Yes |
| Good for comparing models with different $p$ | ❌ No | ✅ Yes |
| Interpretation | Share of variance explained | Share of variance explained, corrected for model size |
| Upper bound | 1 | 1 |

## When to use it

✅ **Use when:**
- Comparing linear regression models with **different numbers of features**
- Doing feature selection (stepwise selection, checking whether a new feature earns its place)
- Reporting in-sample fit for a regression where $p$ is not tiny compared to $n$

❌ **Do not rely on it when:**
- You have a held-out test set. Compute plain $R^2$, [[RMSE - Root Mean Squared Error]] or [[MAE - Mean Absolute Error]] there instead, since out-of-sample evaluation is the more direct check against overfitting.
- The model is highly non-linear or regularized. The "number of parameters" is not simply $p$, so the penalty is not meaningful. Use cross-validation.
- You need to compare models for predictive accuracy. Adjusted $R^2$ is an in-sample, linear-model tool, not a replacement for validation.

## Pitfalls

- **It is only a rough correction:** it penalizes the feature count but does not detect leakage or a badly specified model.
- **Alternatives for model selection:** [[Akaike Information Criterion|AIC]], [[Bayesian Information Criterion|BIC]] and cross-validated error penalize complexity more rigorously.
- **Do not confuse $p$ and $n$:** $p$ counts predictors only, not the intercept and not the samples.

## Related

- [[R-squared]]
- [[Akaike Information Criterion]]
- [[Bayesian Information Criterion]]
- [[MSE - Mean Squared Error]]
- [[RMSE - Root Mean Squared Error]]
- [[MAE - Mean Absolute Error]]
- [[Evaluating regression model metrics]]
- [[ML metrics]]
