#machine-learning #statistics #forecasting
# Quantiles

A **quantile** is a cut point that splits ordered data (or a probability distribution) into parts with a given share of values on each side.

>[!tip] The **q-quantile** is the value below which a fraction *q* of the data falls.

## Example

For the values `10, 20, 30, 40, 50, 60, 70, 80, 90, 100`:

| Quantile | Meaning | Approx. value |
|----------|---------|---------------|
| 0.1 (10th percentile) | 10% of values are below it | ~19 |
| 0.5 (**median**) | Half are below, half above | 55 |
| 0.9 (90th percentile) | 90% of values are below it | ~91 |

## Named quantiles

| Name                | Cuts the data into | Cut points        |
| ------------------- | ------------------ | ----------------- |
| **Median**          | 2 equal parts      | 0.5               |
| **Quartiles**       | 4 parts            | 0.25, 0.5, 0.75   |
| **[[Deciles]]**     | 10 parts           | 0.1, 0.2, ... 0.9 |
| **[[Percentiles]]** | 100 parts          | 0.01, ... 0.99    |

Percentile is the same idea on a 0-100 scale: quantile 0.9 = 90th percentile.

## Quantiles vs. mean

The mean is sensitive to outliers; quantiles (especially the median) are robust.

With incomes of `30, 35, 40, 45, 1000`:

| Statistic | Value |
|-----------|-------|
| Mean | 230 |
| Median | 40 |

The median represents a typical value better here.

## Quantiles in forecasting

A point forecast gives one number ("sales will be 130"). **Quantile forecasts** describe the *uncertainty* around it.

| Quantile | Reading |
|----------|---------|
| 0.1 | Pessimistic: only a 10% chance the value falls below this |
| 0.5 | Median forecast, the most typical outcome |
| 0.9 | Optimistic: only a 10% chance the value goes above this |

The range between 0.1 and 0.9 is an **80% prediction interval**: the actual value is expected to fall inside it 80% of the time.

[[Google TimesFM 3.0]] returns a point forecast plus 9 quantiles (0.1 to 0.9). A `quantiles.shape` of `(12, 9)` means 12 time steps by 9 quantiles. See [[time series forecasting]].

## Quantile loss (pinball loss)

To train a model to predict a specific quantile *q*, use the pinball loss:

```
L_q(y, ŷ) = q · (y − ŷ)       if y ≥ ŷ
          = (1 − q) · (ŷ − y)  if y < ŷ
```

| Quantile q | Behavior |
|------------|----------|
| 0.9 | Under-predicting is penalized 9x more than over-predicting, so the model learns a high estimate |
| 0.5 | Symmetric: equals half the absolute error (predicts the median) |
| 0.1 | Over-predicting is penalized 9x more, so the model learns a low estimate |

## Python example

```python
import numpy as np

values = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

print(np.quantile(values, 0.5))                 # 55.0 (median)
print(np.quantile(values, [0.1, 0.5, 0.9]))     # [19. 55. 91.]
print(np.percentile(values, 90))                # 91.0 (same as quantile 0.9)


def pinball_loss(y_true, y_pred, q):
    diff = y_true - y_pred
    return np.mean(np.maximum(q * diff, (q - 1) * diff))
```

## Practical uses

| Use | Example |
|-----|---------|
| **Inventory planning** | Stock to the 0.9 quantile to avoid stock-outs, not the average |
| **Risk and capacity planning** | Plan for the bad case, not just the typical one |
| **Anomaly detection** | Values outside the 0.05-0.95 range may be unusual |
| **Latency monitoring** | p50, p95, p99 response times (SRE) |
| **Prediction intervals** | Report a range instead of a single number |

## Related

- [[time series forecasting]]
- [[Google TimesFM 3.0]]
- [[Covariate Support]]
