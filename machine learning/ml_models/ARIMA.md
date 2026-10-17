#machine-learning #forecasting #time-series #statistics
# ARIMA

**ARIMA (AutoRegressive Integrated Moving Average)** is a classic statistical model for [[time series forecasting]]. It predicts future values from the series' own past values and past forecast errors.

>[!tip] Make the series stable, then model each value as a combination of its recent past values and recent errors.

## The three parts: ARIMA(p, d, q)

| Letter | Component | What it does | Parameter |
|--------|-----------|--------------|-----------|
| **AR** | AutoRegressive | Predicts from the previous *p* values | `p` = number of lags |
| **I** | Integrated | Differences the series *d* times to remove trend | `d` = degree of differencing |
| **MA** | Moving Average | Predicts from the previous *q* forecast errors | `q` = number of error lags |

## Differencing

**Differencing** replaces each value with the change from the previous one, which removes a trend.

| Month | Sales | After differencing (d=1) |
|-------|-------|--------------------------|
| Jan | 100 | n/a |
| Feb | 110 | +10 |
| Mar | 120 | +10 |
| Apr | 130 | +10 |

The original series trends upward, but the differenced series is constant, so it is stable.

## Intuition

For ARIMA(1, 1, 1), the model works on the differenced series and predicts each step from:

1. the previous change in the series (AR),
2. the previous forecast error (MA).

Then it adds the predicted change back to the last value to get the forecast (I).

## Stationarity

ARIMA needs a **stationary** series after differencing: constant mean and variance over time, and no trend.

| Check | Meaning |
|-------|---------|
| **ADF test** (Augmented Dickey-Fuller) | p-value below 0.05 suggests the series is stationary |
| **Plot** | No visible trend, roughly constant spread |
| If not stationary | Increase `d` (usually 1 or 2 is enough) |

## Python example

```python
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# Synthetic monthly series: trend + noise
rng = np.random.default_rng(42)
y = 100 + 2 * np.arange(60) + rng.normal(0, 3, 60)

model = ARIMA(y, order=(1, 1, 1))     # (p, d, q)
fitted = model.fit()

forecast = fitted.get_forecast(steps=12)
print(forecast.predicted_mean)        # point forecast
print(forecast.conf_int(alpha=0.2))   # 80% prediction interval
```

Install with `pip install statsmodels`.

## Choosing p, d, q

| Method | Idea |
|--------|------|
| **ACF / PACF plots** | Autocorrelation patterns suggest `q` (ACF) and `p` (PACF) |
| **Grid search with AIC/BIC** | Try combinations and keep the lowest score |
| **`auto_arima`** (`pmdarima`) | Automates the search |

## Variants

| Model | Adds |
|-------|------|
| **ARMA** | ARIMA without differencing (data already stationary) |
| **SARIMA** | Seasonal terms (p,d,q)(P,D,Q)m for repeating patterns |
| **ARIMAX / SARIMAX** | External regressors, similar to [[Covariate Support]] |
| **VAR** | Several interacting series, see [[Multivariate Forecasting]] |

## Pros and cons

| Pros | Cons |
|------|------|
| Interpretable, well understood | Assumes linear relationships |
| Works well on small datasets | Needs stationarity and manual tuning |
| Gives prediction intervals | Plain ARIMA ignores seasonality |
| Fast to fit | One model per series, weak at long horizons |

## ARIMA vs. foundation models

| | ARIMA | [[Google TimesFM 3.0]] |
|---|-------|------------------------|
| Training | Fitted separately to each series | [[Zero-Shot]], no fitting |
| Data needed | Works with short series | Needs enough context history |
| Interpretability | High | Low |
| Covariates | Via ARIMAX | Via [[Covariate Support]] |
| Output | Point forecast + intervals | Point forecast + 9 [[Quantiles]] |

ARIMA is still a good **baseline**: compare a modern model's [[MAE - Mean Absolute Error|MAE]] against it.

## Related

- [[time series forecasting]]
- [[Covariate Support]]
- [[Multivariate Forecasting]]
- [[Quantiles]]
- [[MAE - Mean Absolute Error]]
- [[Google TimesFM 3.0]]
