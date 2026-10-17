#machine-learning #forecasting #time-series

The ability of a [[time series forecasting]] model to use **extra variables (covariates)** alongside the series it predicts, instead of looking only at the target's own history.

>[!tip] A **covariate** is any additional, [[time-aligned variable]] that may explain or influence the target.

## Why it matters

Take sales forecasting:

- **Without covariates**, the model sees only past sales and extrapolates trend and seasonality.
- **With covariates**, it also knows "next month has a holiday and a 20% discount", so it can forecast the jump instead of missing it.

## Types of covariates

| Type | Known when? | Examples | In [[Google TimesFM 3.0]] |
|------|-------------|----------|---------------------------|
| **Past-only** (dynamic, unknown future) | Only up to "now" | Observed temperature, competitor price, web traffic | `past_only_covariates` |
| **Past + future** (dynamic, known future) | Past *and* planned/future values | Holidays, planned promotions, ad spend, weather forecast | `past_future_covariates` |
| **Static** | Constant over time | Store ID, region, product category | not covered in the example |

Expected input shapes in TimesFM 3.0:

| Input | Shape |
|-------|-------|
| Past-only covariates | `(channels, context_length)` |
| Past + future covariates | `(channels, context_length + horizon)` |

## Covariate support vs. [[Multivariate Forecasting]]

They overlap but are **not the same thing**.

|                         | Covariates                             | Multivariate targets                      |
| ----------------------- | -------------------------------------- | ----------------------------------------- |
| Role of extra variables | Inputs only, not predicted             | Are themselves predicted                  |
| Example                 | Predict sales using price and holidays | Predict sales, demand and returns jointly |
| Output                  | One target (or several)                | Several targets together                  |

- Covariates are **one way** to make a forecast multivariate (the loose meaning of the term).
- Multivariate forecasting can exist **without** covariates (all variables are targets).
- Covariates can exist **without** multiple targets (one target plus a holiday flag).

## Practical points

- **Future values are required** for past+future covariates. If you don't know them at prediction time, use past-only covariates or forecast them first (which adds error).
- Covariates must be **aligned in time** with the target: same frequency, no gaps.
- Useless covariates add noise; they help only when they carry real signal.
- A foundation model with covariate support can use them [[Zero-Shot]], without training on your dataset.

## Classic equivalents

| Approach | Covariate mechanism |
|----------|---------------------|
| ARIMAX / SARIMAX | Exogenous regressors |
| Prophet | Extra regressors |
| Gradient boosting (XGBoost, LightGBM) | Lag features plus extra feature columns |
| Temporal Fusion Transformer | Static, past and known-future inputs |
| [[Google TimesFM 3.0]] | `past_only_covariates`, `past_future_covariates` |

## Example

See the Python example in [[Google TimesFM 3.0]].

```python
outputs = list(
    forecaster.predict_batch(
        contexts=[target],                          # (num_variates, context_length)
        horizon=24,
        past_only_covariates=[past_only_cov],       # (channels, context_length)
        past_future_covariates=[past_future_cov],   # (channels, context_length + horizon)
        return_quantiles=True,
        use_symmetric_averaging=False,
    )
)
```
