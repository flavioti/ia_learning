---
aliases:
  - DecisionTreeRegressor
  - Regression Tree
---
#ml-model #supervised-learning #regression #tree-based

## Definition

A **regression tree** is a [[Decision Tree]] that predicts a **continuous numeric target**. It splits the data into regions with similar target values, and each leaf predicts the **mean of the target** of its training samples. In scikit-learn it is `DecisionTreeRegressor`.

>[!tip] Think of it as cutting the feature space into boxes and predicting the average of each box.

Shared concepts (anatomy, greedy splitting, pruning, feature importance, strengths and weaknesses) are in [[Decision Tree]]. This note covers what is specific to regression. For the target type, see [[Continuous Variable]] (and [[Discrete Variable]] for count targets).

![[decision-tree-regressor.png|961]]

## Leaf prediction

The prediction for a new sample is the **mean of the training targets in the leaf** it falls into. So the model outputs only as many distinct values as it has leaves, which makes the prediction curve a **staircase**.

## Math notation

The split criterion is the impurity of the **target values** in a node. With $\bar{y}$ the mean target in the node and $N$ the number of samples in it:

$$
H(Q) = \text{MSE} = \frac{1}{N} \sum_{i=1}^{N} \left( y_i - \bar{y} \right)^2
$$

The algorithm picks the split that minimizes the weighted impurity of the two children:

$$
J(\text{feature}, t) = \frac{N_L}{N}\, H(Q_L) + \frac{N_R}{N}\, H(Q_R)
$$

Minimizing the MSE of the children is the same as maximizing the **variance reduction**. See [[MSE - Mean Squared Error]].

### Criteria

| `criterion` | Impurity | Leaf prediction | Use when |
|-------------|----------|-----------------|----------|
| `"squared_error"` (default) | MSE | Mean | Standard choice |
| `"friedman_mse"` | MSE with Friedman's improvement score | Mean | Often used inside gradient boosting |
| `"absolute_error"` | MAE | **Median** | Outliers in the target. Slower to train |
| `"poisson"` | Poisson deviance | Mean | Non-negative **count** targets or rates (target must be ≥ 0) |

## Worked example (MSE)

Target values: `[10, 12, 11, 30, 32, 31]`. The mean is 21, so the parent's variance (MSE around the mean) is about **100.7**.

A split between 12 and 30 gives two children:

| Child | Values | Mean (the leaf's prediction) | MSE |
|-------|--------|------------------------------|-----|
| Left | 10, 12, 11 | 11 | 0.67 |
| Right | 30, 32, 31 | 31 | 0.67 |

The weighted MSE falls from 100.7 to 0.67, a huge reduction, so this is an excellent split.

## Limitations specific to regression

| Limitation | What happens | What to do |
|------------|--------------|------------|
| **Staircase predictions** | A smooth relationship is approximated by steps, and needs many leaves | Use [[Linear Regression\|Linear regression]], a GAM, or boosting |
| **No extrapolation** | Outside the training range, the prediction stays at the value of the nearest leaf | Use a linear model or add a trend component |
| **Sensitive to target outliers** | The leaf mean is pulled by extreme targets | `criterion="absolute_error"`, or winsorize the target |
| **Skewed target** | Large values dominate the MSE | Predict `log1p(y)` and transform back |
| **High variance** | A small data change gives a different tree | Prune, or use [[Random Forest]] / [[Gradient Boosting]] |

Example of the extrapolation limit: a tree trained on `y = 2x` for `x` between 0 and 10 predicts about 19.5 for `x = 9.9`, and **the same value** for `x = 20` or `x = 100`.

## Hyperparameters

Complexity controls are shared with every tree, see [[Decision Tree]]. For regression, the most useful ones are:

| Hyperparameter | Effect for regression |
|----------------|-----------------------|
| `max_depth` | Fewer, coarser steps when small |
| `min_samples_leaf` | Each leaf averages more samples, which gives smoother predictions and less noise |
| `ccp_alpha` | Prunes branches that do not reduce the error enough |
| `criterion` | See the table above |

## Python

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import root_mean_squared_error, r2_score

rng = np.random.default_rng(42)
X = rng.uniform(0, 10, (300, 1))
y = np.sin(X[:, 0]) * 10 + rng.normal(0, 2, 300)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Unconstrained tree: perfect on train, worse on test
deep = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)
print("train R2:", deep.score(X_train, y_train))   # 1.0
print("test  R2:", deep.score(X_test, y_test))     # ~0.82

# Tune the complexity with cross-validation
grid = GridSearchCV(
    DecisionTreeRegressor(random_state=42),
    param_grid={"max_depth": [2, 3, 4, 5, 6, 8, None], "min_samples_leaf": [1, 5, 10, 20]},
    scoring="neg_root_mean_squared_error",
    cv=5,
).fit(X_train, y_train)

print(grid.best_params_)          # {'max_depth': 6, 'min_samples_leaf': 5}
best = grid.best_estimator_
pred = best.predict(X_test)
print("RMSE:", root_mean_squared_error(y_test, pred))
print("R2:  ", r2_score(y_test, pred))
```

### Median leaves with `absolute_error`

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

X = np.zeros((4, 1))
y = np.array([1, 2, 3, 100.0])                                    # one outlier

print(DecisionTreeRegressor().fit(X, y).predict([[0]]))                          # [26.5]  (mean)
print(DecisionTreeRegressor(criterion="absolute_error").fit(X, y).predict([[0]]))  # [2.5]   (median)
```

## Evaluating a regression tree

Always evaluate on **held-out data** (or with cross-validation), since training scores are misleading for trees. Compare the training and test score: a big gap signals overfitting.

| Metric | Use |
|--------|-----|
| [[RMSE - Root Mean Squared Error]] | Error in the target units, penalizes large errors |
| [[MAE - Mean Absolute Error]] | Error in the target units, robust to outliers |
| [[MAPE - Mean Absolute Percentage Error]] | Percentage error, when the target is always far from 0 |
| [[R-squared]] | Share of variance explained, a quick gut check |

See [[Evaluating regression model metrics]] for the full comparison, and [[Linear Regression]] for the problem type.

## Use cases

| Use case | Why a regression tree fits |
|----------|----------------------------|
| House price estimation | Non-linear effects and interactions (size, location) |
| Insurance claim or loss estimation | Threshold-driven behavior, explainable |
| Delivery time (ETA) | Distinct regimes (rush hour vs. night) |
| Demand forecasting from tabular features | Promotions and holidays cause abrupt changes |
| Dynamic pricing tiers | The output is piecewise constant, as prices often are |
| Energy or sensor regression | Behavior changes at thresholds (temperature, occupancy) |
| Count targets (claims, visits) | `criterion="poisson"` |

## When to use it

✅ **Use when:**
- The target is numeric and the relationship is non-linear or full of interactions
- You need readable rules or a quick baseline
- The target is step-like (tiers, thresholds)

❌ **Do not use alone when:**
- You need the best accuracy (use [[Random Forest]] or [[Gradient Boosting]])
- The relationship is smooth or linear, or you must **extrapolate** beyond the training range
- The dataset is small and noisy

## Related

- [[Decision Tree]]
- [[Decision Tree Classifier]]
- [[Random Forest]]
- [[Gradient Boosting]]
- [[Linear Regression|Linear regression]]
- [[Continuous Variable]]
- [[Evaluating regression model metrics]]
