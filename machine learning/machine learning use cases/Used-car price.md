#use-case #regression #pricing
# Used-car price

Predict the **fair price of a used car** from its characteristics: brand and model, age, mileage, engine, condition and history. Marketplaces use it to suggest a listing price, flag overpriced or underpriced ads, and make instant purchase offers.

The target is a positive number on a continuous scale, so this is a **regression** problem. See Continuous Variable. It is close to House price, with three differences that shape the work: prices are **multiplicative** (a car loses a percentage of its value each year, not a fixed amount), there are **many brands and models** (high-cardinality categories), and the **market moves** over time.

## Which algorithm?

| Step | Algorithm | Why |
|---|---|---|
| 1. Baseline | Linear model such as Ridge, **on the log of the price** | Depreciation is a percentage, so it is linear on the log scale. Fast and interpretable. |
| 2. Strong default | Random Forest Regressor | Handles non-linear effects and mixed feature types with little tuning. |
| 3. Usually best on real data | Gradient Boosting (XGBoost, LightGBM, CatBoost, `HistGradientBoostingRegressor`) | Captures interactions (for example age x brand, mileage x fuel) and handles missing values. |

Do not assume the complex model wins: if the price is close to a clean product of effects, a log-linear model is hard to beat. See the example below.

## Features

| Group | Examples |
|---|---|
| Identity | Brand, model, version, body type |
| Age and usage | Age (or registration year), **mileage**, number of owners |
| Technical | Engine power, fuel (petrol, diesel, hybrid, electric), transmission, drivetrain |
| Condition and history | Accidents, service history, damage, number of keys |
| Listing and context | Location, seller type (dealer or private), **listing date**, optional equipment |

- **Age and mileage** carry most of the signal, and they are strongly correlated with each other. Mileage per year (usage intensity) is a useful derived feature.
- **Brand and model** often have hundreds of values. One-hot encoding grows large and sparse, so use a native categorical encoder (CatBoost, LightGBM), target encoding computed **inside the training folds only**, or group rare models into "other". See Categorical columns.
- **The target** is the **asking price** in most datasets, which is higher than the price actually paid. Say so when you report errors.

## Target transformation

Prices are right-skewed, and errors grow with the price. Training on `log(price)` and converting back is often a large gain, especially for linear models.

- A model on `log(price)` minimizes **relative** error, which matches how people think about price ("10% too high").
- Always evaluate **in the original currency**, after converting back.
- Predictions are always positive, which a linear model on the raw price cannot guarantee.
- Averaging in log space slightly underestimates the mean price. Check the bias on validation data.

## Metrics

| Metric | Use |
|---|---|
| MAE - Mean Absolute Error | The typical error in currency units. Easy to explain. |
| RMSE - Root Mean Squared Error | Penalizes large misses, which dominate for expensive cars. |
| MAPE - Mean Absolute Percentage Error | The error as a share of the price. The natural metric here, because a 1,000 error means different things on a cheap and an expensive car. |
| R-squared | Share of the price variance explained. Can look high while the error is still too large to be useful. |

Report MAE and MAPE together, and look at the error **by price segment**. See Evaluating regression model metrics. When luxury cars should not dominate the error, prefer MAE or MAPE over RMSE, or train with a robust loss such as Huber Loss.

## Example (synthetic data)

An illustration with generated listings, **not real data**: 20,000 cars from 10 brands, with age, mileage, engine power, fuel, transmission, accidents, number of owners and the month of the listing. The generated price loses about 11% of its value per year, and there is random noise of about 10%. Prices range from 430 to 138,520 (mean 12,568, median 7,970, skewness 2.3). The split is 75% train and 25% test.

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             mean_absolute_percentage_error, r2_score)

# df: features; price: target. cat = ["brand", "fuel", "transmission"]; num = the numeric columns
ridge = make_pipeline(
    ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), cat),
                       ("n", StandardScaler(), num)]),
    Ridge(alpha=1.0))
hgb = make_pipeline(
    ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat),
                       ("n", "passthrough", num)]),
    HistGradientBoostingRegressor(random_state=0))

def evaluate(model, X_train, y_train, X_test, y_test, log):
    # With log=True the model trains on log(price) and predicts back in the original unit
    est = (TransformedTargetRegressor(regressor=model, func=np.log, inverse_func=np.exp)
           if log else model)
    est.fit(X_train, y_train)
    p = est.predict(X_test)
    return (np.sqrt(mean_squared_error(y_test, p)), mean_absolute_error(y_test, p),
            mean_absolute_percentage_error(y_test, p) * 100, r2_score(y_test, p))
```

**Random split** (RMSE and MAE in currency units):

| Model | RMSE | MAE | MAPE | R-squared |
|---|---|---|---|---|
| Ridge | 6,571 | 4,736 | 102.2% | 0.749 |
| **Ridge, log target** | **1,807** | **1,017** | **8.1%** | **0.981** |
| Hist Gradient Boosting | 1,970 | 1,141 | 9.9% | 0.977 |
| Hist Gradient Boosting, log target | 1,906 | 1,085 | 8.9% | 0.979 |

What the results show:

- **The log target is the biggest gain.** Ridge improves from a MAPE of 102% to 8%. On the raw price a linear model cannot represent a percentage depreciation, so it predicts near-zero or negative prices for cheap old cars.
- **The simple log-linear model matches or beats gradient boosting.** This is partly by construction, because the generated price is a product of effects with no interactions, and a real market has more interactions that boosting would exploit. Always compare, and do not assume the complex model wins.
- **Without the log, boosting is much better than Ridge** (MAE 1,141 versus 4,736), since trees handle the multiplicative structure on their own. The log still helps it a little (MAPE 9.9% to 8.9%).
- **R-squared is high for every model except raw Ridge,** and it hides the difference in relative error. MAPE separates the models far better.

**Error by price segment** (Hist Gradient Boosting, log target, test set):

| Price quartile | MAE | MAPE |
|---|---|---|
| Q1 (cheapest) | 210 | 9.4% |
| Q2 | 517 | 9.0% |
| Q3 | 1,010 | 8.6% |
| Q4 (most expensive) | 2,605 | 8.6% |

The relative error is about the same for all quartiles, but the **absolute error is more than 12 times larger** for the most expensive cars. A single MAE would hide that. Report both.

## Time matters: the market moves

In the example, the market price rises about 15% over the 36 months. A random split mixes old and new listings, so it is optimistic. A **time split** trains on the first 24 months and tests on the last 12, as in production:

| Model | Random split MAE | Time split MAE | Time split MAPE |
|---|---|---|---|
| Ridge, log target | 1,017 | 1,061 | 8.2% |
| Hist Gradient Boosting, log target | 1,085 | 1,191 | 8.9% |

- **Boosting loses about 10% of its accuracy** on the future months, because trees cannot extrapolate beyond the range seen in training. Its predictions are 2.4% **too low on average**.
- **Dropping the listing month makes it worse** (MAE 1,333, MAPE 9.8%, average bias -5.9%): the model has no way to know about the market trend.
- The log-linear model extrapolates a trend more smoothly, which is why it loses very little here.

In practice, retrain often on recent sales, include a market index or the listing date as a feature, and monitor the bias over time. See Model drift.

## Pitfalls

- **Asking price versus sale price:** most public data holds asking prices, which are optimistic and negotiable
- **Random splits:** they leak the future and the same listing repeated across sets. Split by date, and keep duplicates or relists of the same car in the same fold. See K-Fold Cross-Validation and Data Leakage
- **Raw price target with a linear model:** it gives negative or poor predictions. Try the log
- **Ignoring relative error:** report MAPE and the error by price segment, not only RMSE or R-squared
- **High-cardinality categories:** target encoding done on all the data leaks the target. Fit it inside each training fold
- **Rare models and new models:** few examples means noisy predictions. Fall back to the brand level or show a wider uncertainty range
- **Outliers and bad data:** typos (a mileage of 1, a price of 100), exotic and collector cars. Check the residuals and filter or cap carefully
- **Market drift:** a model trained on old sales is biased low in a rising market and high in a falling one. See Model drift
- **Overfitting:** compare the training and test scores. See Overfitting
- **Point price only:** users need a range. Use quantile regression or prediction intervals, not a single number

## Related

- House price
- scikit-learn
- Gradient Boosting
- Random Forest Regressor
- Ridge and Lasso Regression
- Evaluating regression model metrics
- Model Evaluation
