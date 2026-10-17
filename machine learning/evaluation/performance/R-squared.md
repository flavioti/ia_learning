---
aliases:
  - Coefficient of Determination
---
#regression-metric #metrics #regression #evaluation

## Definition

**R-squared** ($R^2$, coefficient of determination) measures the **proportion of the variance in the target that the model explains**. It compares the model against the laziest possible baseline: always predicting the mean of the target.

>[!tip] How much better is my model than just guessing the average?

- $R^2 = 0$: the model is no better than predicting the mean. It is useless.
- $R^2 = 1$: the model predicts every data point perfectly, with zero error.
- $R^2 < 0$: the model is **worse** than predicting the mean. This is possible on test data, or with a model fit without an intercept.

## Math notation

$$
R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2}{\sum_{i=1}^{n} \left( y_i - \bar{y} \right)^2}
$$

Where:
- $y_i$ is the actual value
- $\hat{y}_i$ is the predicted value
- $\bar{y}$ is the mean of the actual values
- $n$ is the number of samples
- $SS_{res}$ is the residual sum of squares (the model's error)
- $SS_{tot}$ is the total sum of squares (the error of the mean baseline)

Equivalent form using [[MSE - Mean Squared Error]]:

$$
R^2 = 1 - \frac{\text{MSE}(\text{model})}{\text{Var}(y)}
$$

## Example

Reusing the forecast from [[MAE - Mean Absolute Error]]:

| Month | Actual $y_i$ | Forecast $\hat{y}_i$ | $(y_i - \hat{y}_i)^2$ | $(y_i - \bar{y})^2$ |
|-------|-------------|----------------------|------------------------|----------------------|
| Jan | 100 | 98 | 4 | 225 |
| Feb | 110 | 115 | 25 | 25 |
| Mar | 120 | 117 | 9 | 25 |
| Apr | 130 | 126 | 16 | 225 |
| **Sum** | | | **54** ($SS_{res}$) | **500** ($SS_{tot}$) |

With $\bar{y} = 115$:

$$
R^2 = 1 - \frac{54}{500} = 0.892
$$

The model explains about **89.2%** of the variance in the target.

## Python

```python
import numpy as np
from sklearn.metrics import r2_score

actual   = np.array([100, 110, 120, 130])
forecast = np.array([98, 115, 117, 126])

ss_res = np.sum((actual - forecast) ** 2)
ss_tot = np.sum((actual - actual.mean()) ** 2)

print(1 - ss_res / ss_tot)          # 0.892
print(r2_score(actual, forecast))   # 0.892
```

## Key properties

| Property | Meaning |
|----------|---------|
| **Unitless** | Easy to compare across targets with different units, unlike [[MAE - Mean Absolute Error]] or [[RMSE - Root Mean Squared Error]] |
| **Higher is better** | 1 is perfect, 0 is the mean baseline |
| **Never decreases when you add features** | On the training set, adding any feature (even random noise) leaves $R^2$ the same or higher for ordinary least squares. This is why [[Adjusted R-squared]] exists |
| **Sensitive to outliers** | It is built on squared errors, like MSE |
| **Depends on the target's variance** | The same absolute error gives a higher $R^2$ on a high-variance target than on a low-variance one |
| **Says nothing about bias or fit quality** | A high $R^2$ does not prove the model is correct. Check residual plots |

## Pitfalls

- **Overfitting:** a high training $R^2$ with a low test $R^2$ signals overfitting. Always report $R^2$ on held-out data.
- **Adding features inflates it:** do not use plain $R^2$ to compare models with a different number of features. Use [[Adjusted R-squared]] or cross-validation.
- **Non-linear models:** the usual interpretation as "explained variance" is cleanest for linear regression. For other models, treat it as a skill score against the mean baseline.
- **Time series:** a trending series gives a high $R^2$ even for poor forecasts. Compare against a naive forecast instead.
- **Not a measure of error size:** a model can have a high $R^2$ and still be off by too many units to be useful. Pair it with MAE or RMSE.

## Related

- [[Adjusted R-squared]]
- [[Akaike Information Criterion]]
- [[Bayesian Information Criterion]]
- [[MSE - Mean Squared Error]]
- [[RMSE - Root Mean Squared Error]]
- [[MAE - Mean Absolute Error]]
- [[Evaluating regression model metrics]]
- [[ML metrics]]
