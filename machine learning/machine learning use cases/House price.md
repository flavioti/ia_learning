#use-case #regression #linear-regression
# House price

Predict the **sale price of a house** from its characteristics: size, rooms, age, condition and, above all, **location**.

The target is a number on a continuous scale, so this is a **regression** problem. See Continuous Variable.

## Which algorithm?

There is no single best algorithm, but on tabular data like this one the usual winner is **gradient boosting**.

| Step                    | Algorithm                                                                  | Why                                                                                         |
| ----------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1. Baseline             | Linear regression, Ridge, Lasso            | Fast and interpretable. A floor to beat.                                                    |
| 2. Strong default       | Random Forest Regressor                                                | Handles non-linear effects and mixed feature types with little tuning.                      |
| 3. Usually best         | Gradient Boosting (XGBoost, LightGBM, `HistGradientBoostingRegressor`) | Captures feature interactions (for example area x neighborhood) and handles missing values. |
| To understand the rules | Decision Tree Regressor                                                | Easy to read, but weaker than the ensembles on its own.                                     |

## Features

- **Location** is usually the strongest signal: neighborhood, coordinates, distance to the center or to transport
- **Size:** area, number of rooms and bathrooms
- **Age and condition**
- **Context:** local income level, crime rate, schools

Encode categorical columns properly (neighborhood, property type). See Categorical columns and feature engineering.

## Metrics

| Metric | Use |
|---|---|
| RMSE - Root Mean Squared Error | The standard choice. Penalizes large misses, in the price's own unit. |
| MAE - Mean Absolute Error | The typical error, less affected by luxury outliers. |
| MAPE - Mean Absolute Percentage Error | The error as a percentage of the price, which is easy to explain. |
| R-squared | Share of the price variance the model explains. |

See Evaluating regression model metrics. When a few expensive houses should not dominate the error, prefer MAE or MAPE over RMSE, or train with a robust loss such as Huber Loss.

## Example: California housing

The public California housing dataset has 20,640 districts and 8 features. The target is the **median house value** in units of $100,000 (mean 2.07, standard deviation 1.15, capped at 5.0).

```python
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.compose import TransformedTargetRegressor

X, y = fetch_california_housing(return_X_y=True)   # target in units of $100,000
cv = KFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Ridge":               make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "Random Forest":       RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42),
    "Hist Gradient Boost": HistGradientBoostingRegressor(random_state=42),
}

scoring = {"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error", "r2": "r2"}
for name, model in models.items():
    for log in (False, True):
        # With log=True the model is trained on log(1 + price) and predicts back in the original unit
        est = (TransformedTargetRegressor(regressor=model, func=np.log1p, inverse_func=np.expm1)
               if log else model)
        res = cross_validate(est, X, y, cv=cv, scoring=scoring)
        print(name, "(log target)" if log else "",
              round(-res["test_rmse"].mean(), 3),
              round(-res["test_mae"].mean(), 3),
              round(res["test_r2"].mean(), 3))
```

Results with 5-fold cross-validation (RMSE and MAE in units of $100,000, so 0.466 is about $46,600):

| Model                              | RMSE      | MAE       | R-squared |
| ---------------------------------- | --------- | --------- | --------- |
| Ridge                              | 0.728     | 0.532     | 0.601     |
| Ridge, log target                  | 0.830     | 0.528     | 0.477     |
| Random Forest                      | 0.503     | 0.328     | 0.810     |
| Random Forest, log target          | 0.505     | 0.320     | 0.809     |
| **Hist Gradient Boosting**         | **0.466** | 0.312     | **0.836** |
| Hist Gradient Boosting, log target | 0.472     | **0.307** | 0.833     |

What the results show:

- **Gradient boosting wins**, followed by the random forest. Ridge is clearly behind: the relationship with location is not linear.
- **A log target is not always a gain.** It is a common trick for right-skewed prices, but here it barely changed the tree models (slightly lower MAE, slightly higher RMSE) and made Ridge worse on RMSE. This target is capped at 5.0 and not very skewed. Always compare with and without it, in the original unit.
- **Features were used as they come.** No feature engineering and no tuning were done, so all three models can improve.

## Pitfalls

- **Spatial and time leakage:** houses in the same neighborhood are similar, so a random split lets the model "see" neighbors of the test houses. Randomly shuffled folds, as in the example, give an optimistic score. For a realistic estimate, split by area or by date. See K-Fold Cross-Validation.
- **Price drift:** the market changes over time, so a model trained on old sales degrades. See Model drift.
- **Capped or outlier targets:** a cap (the 5.0 above) and luxury properties distort the error. Check the residuals, not only the average.
- **Unit of the error:** report RMSE and MAE in currency units, and not only R-squared, because a high R-squared can still mean an error too big to be useful.
- **Overfitting:** compare the training and test scores. See Overfitting.

## Related

- scikit-learn
- Gradient Boosting
- Random Forest Regressor
- Decision Tree Regressor
- Evaluating regression model metrics
- Model Evaluation
