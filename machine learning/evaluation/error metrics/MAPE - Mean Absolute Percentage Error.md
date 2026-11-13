---
aliases:
  - MAPE
---
#metrics #regression #forecasting #evaluation #regression-metric

## Definition
Is the average error expressed as a percentage of the actual value. It answers the question: "On average, by what percent are my predictions off?"

>[!tip] It is scale-free, so it can be compared across series with different units.

## Math notation
$$
\text{MAPE} = \frac{100\%}{n} \sum_{i=1}^{n} \left| \frac{y_i - \hat{y}_i}{y_i} \right|
$$

Where $y_i$ is the actual value, $\hat{y}_i$ is the predicted value, and $n$ is the number of samples.

## Key Characteristics
Scale-free and easy to explain, but undefined when an actual value is 0 and biased towards under-prediction.

**Best Used When**: All actual values are clearly positive and far from zero (e.g., sales volume, demand or prices), and you need to report error as a percentage to non-technical stakeholders or compare series with different scales.

## Example

Reusing the forecast from [[MAE - Mean Absolute Error]]:

| Month | Actual | Forecast | Absolute error | % error |
|-------|--------|----------|----------------|---------|
| Jan | 100 | 98 | 2 | 2.00% |
| Feb | 110 | 115 | 5 | 4.55% |
| Mar | 120 | 117 | 3 | 2.50% |
| Apr | 130 | 126 | 4 | 3.08% |

$$
\text{MAPE} = \frac{2.00 + 4.55 + 2.50 + 3.08}{4} \approx 3.03\%
$$

The forecast is off by about 3% on average.

## Python

```python
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

actual   = np.array([100, 110, 120, 130])
forecast = np.array([98, 115, 117, 126])

print(np.mean(np.abs((actual - forecast) / actual)) * 100)     # 3.03 (percent)
print(mean_absolute_percentage_error(actual, forecast))        # 0.0303 (a fraction, not a percent)
```

>[!warning] scikit-learn returns MAPE as a **fraction** (0.0303). Multiply by 100 to get a percentage.

## Key properties

| Property | Meaning |
|----------|---------|
| **Scale-free** | Comparable across series with different units, unlike [[MAE - Mean Absolute Error]] or [[RMSE - Root Mean Squared Error]] |
| **Easy to interpret** | "The forecast is off by 3%" |
| **Lower is better** | 0% means perfect predictions |
| **Not bounded above** | Over-predictions can produce errors above 100% |
| **Needs actuals that are not zero** | Division by the actual value |

## Weaknesses

| Problem | Why |
|---------|-----|
| **Undefined at 0** | An actual value of 0 is a division by zero. Plain NumPy gives `inf`. scikit-learn replaces 0 with a tiny epsilon, so it returns an absurdly large number instead of failing |
| **Unstable with small actuals** | A tiny actual inflates the percentage, and a few such points can dominate the average |
| **Asymmetric** | The percentage error depends on which value is the denominator. See below |
| **Penalizes over-prediction more** | Over-predictions are unbounded, while under-predictions are capped at 100% (for non-negative values). Models tuned for MAPE tend to under-predict |
| **Not meaningful on interval scales** | Temperature in °C, for example, since zero is arbitrary |

### Asymmetry example

The same absolute error of 50 gives different percentages:

| Actual | Forecast | Error | % error |
|--------|----------|-------|---------|
| 100 | 150 | over-prediction | 50% |
| 150 | 100 | under-prediction | 33.3% |

## MAPE vs. alternatives

| Metric | Formula idea | Notes |
|--------|--------------|-------|
| **MAPE** | Mean of \|error\| / \|actual\| | Easy to read, breaks near 0 |
| **sMAPE** | Mean of \|error\| / ((\|actual\| + \|forecast\|) / 2) | Less extreme for small actuals, but still has quirks (it is not truly symmetric about under/over-prediction) |
| **WAPE** | Σ\|error\| / Σ\|actual\| | Stable when some actuals are small. Also called weighted MAPE |
| **MASE** | MAE ÷ MAE of a naive forecast | Scale-free and works with zeros. Good for comparing across series |
| [[MAE - Mean Absolute Error]] | Mean of \|error\| | In the units of the target, robust to zeros |
| [[RMSE - Root Mean Squared Error]] | √MSE | In the units of the target, sensitive to outliers |

For the example above, WAPE = 14 / 460 ≈ 3.04% and sMAPE ≈ 3.03%. They are close to MAPE (3.03%) because the actuals are all of similar size.

## When to use it

✅ **Use when:**
- Actual values are always positive and not close to zero
- You need a percentage error that non-technical stakeholders understand
- You compare accuracy across series with different scales (with care)

❌ **Do not use when:**
- The target contains zeros or near-zero values (intermittent demand, counts, returns). Use WAPE, MASE or [[MAE - Mean Absolute Error]].
- You want an unbiased view of over- vs. under-prediction
- The target is on an interval scale (temperature)

## Related

- [[MAE - Mean Absolute Error]]
- [[MSE - Mean Squared Error]]
- [[RMSE - Root Mean Squared Error]]
- [[R-squared]]
- [[Evaluating regression model metrics]]
- [[Evaluating classification model metrics]]
