#metrics #regression #forecasting #evaluation #regression-metric 
## Definition: 
Measures the average magnitude of absolute errors (L₁ loss).
## Math notation
$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} \left| y_i - \hat{y}_i \right|
$$

Where $y_i$ is the actual value, $\hat{y}_i$ is the predicted value, and $n$ is the number of samples.

## Key Characteristics: 
Robust to outliers; stable gradients, but the gradient is discontinuous at zero.
**Best Used When**: Outliers are present and should not heavily distort the model (e.g., financial forecasting where anomalies happen but shouldn't break the system).

>[!tip] On average, how far off are my predictions, in the same units as the target?

## Formula

```
MAE = (1/n) · Σ |yᵢ − ŷᵢ|
```

- `yᵢ` = actual value
- `ŷᵢ` = predicted value
- `n` = number of predictions

## Example

| Month | Actual | Forecast | Error | Absolute error |
|-------|--------|----------|-------|----------------|
| Jan | 100 | 98 | +2 | 2 |
| Feb | 110 | 115 | −5 | 5 |
| Mar | 120 | 117 | +3 | 3 |
| Apr | 130 | 126 | +4 | 4 |

==🟢MAE = (2 + 5 + 3 + 4) / 4 = **3.5**==

The forecast is off by 3.5 units on average. If the target is sales in units, that means 3.5 units.

## Python

```python
import numpy as np
from sklearn.metrics import mean_absolute_error

actual   = np.array([100, 110, 120, 130])
forecast = np.array([98, 115, 117, 126])

print(np.mean(np.abs(actual - forecast)))        # 3.5
print(mean_absolute_error(actual, forecast))     # 3.5
```

## Key properties

| Property | Meaning |
|----------|---------|
| **Same units as the target** | Easy to explain ("off by 3.5 units") |
| **Robust to outliers** | Each error counts linearly, so one huge miss doesn't dominate |
| **Lower is better** | 0 means perfect predictions |
| **Scale-dependent** | Can't compare MAE across series with different scales |
| **No direction** | Doesn't show whether the model over- or under-predicts (that is *bias*) |

## Outliers: MAE vs. MSE

Errors of `1, 1, 1, 1, 20`:

| Metric | Value | Reading |
|--------|-------|---------|
| MAE | 4.8 | The big miss counts linearly |
| MSE | 80.8 | The big miss dominates because it is squared |
| RMSE | ≈ 8.99 | Pulled up by the outlier |

If RMSE is much larger than MAE, a few large errors are driving the result.

## MAE vs. related metrics

| Metric | Formula idea | Notes |
|--------|--------------|-------|
| **MAE** | Mean of \|error\| | Easy to read, robust to outliers |
| [[MSE - Mean Squared Error]] | Mean of error² | Penalizes large errors heavily |
| **RMSE** | √MSE | Same units as target, more sensitive to outliers than MAE |
| **MAPE** | Mean of \|error\| / \|actual\| | Percentage, but breaks when actual values are near 0 |
| **sMAPE** | Symmetric percentage error | Less sensitive to small actuals than MAPE |
| **MASE** | MAE ÷ MAE of a naive forecast | Scale-free, good for comparing across series |
| [[Huber Loss]] | Quadratic for small errors, linear for large | Compromise between MAE and MSE |

## As a loss function

| Aspect | MAE (L₁) | MSE (L₂) |
|--------|----------|----------|
| Gradient | Constant magnitude, discontinuous at 0 | Proportional to the error, smooth |
| Predicts | The **median** | The **mean** |
| Outliers | Robust | Sensitive |

## Connection to quantiles

MAE is minimized by predicting the **median**, which is the 0.5 quantile. The pinball loss at q = 0.5 equals half the absolute error, so training for MAE is the same as training for the median forecast. See [[Quantiles]].

## Typical use

MAE is a standard metric for evaluating [[time series forecasting]] models, including comparing [[Google TimesFM 3.0]] against a baseline such as a moving average or ARIMA.

## Related

- [[ML metrics]]
- [[MSE - Mean Squared Error]]
- [[Huber Loss]]
- [[Quantiles]]
- [[ML - Machine Learning]]
