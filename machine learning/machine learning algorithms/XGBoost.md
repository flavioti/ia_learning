---
aliases:
  - Extreme Gradient Boosting
  - xgboost
---
#ml-model #supervised-learning #classification #regression #tree-based #ensemble

# XGBoost

**XGBoost** (eXtreme Gradient Boosting) is an optimized, open-source library that implements [[Gradient Boosting]] with decision trees. It builds trees **one after another**, and each new tree corrects the errors of the ones before it. It adds explicit regularization, a second-order approximation of the loss, native handling of missing values and an efficient, parallel implementation.

It became the default winner for **tabular data** (rows and columns) in competitions and in industry, and it supports regression, classification, ranking and custom objectives. It does not fit raw images, audio or text, where neural networks are the usual choice.

>[!tip] Think of a team of weak decision trees where each member only studies the mistakes left by the previous ones. XGBoost makes each step precise, regularized and fast.

For the shared tree concepts see [[Decision Tree]], [[Decision Tree Regressor]] and [[Decision Tree Classifier]]. The parallel idea of averaging independent trees is [[Random Forest]].

## How it works

1. Start with a constant prediction (for example the mean of the target).
2. Compute, for each row, how wrong the current prediction is: the **gradient** (first derivative of the loss) and the **hessian** (second derivative, the curvature).
3. Fit a new small tree to those gradients and hessians.
4. Add the tree to the model, scaled by the **learning rate** (`eta`), so each tree makes only a small correction.
5. Repeat for `n_estimators` rounds, or until the validation score stops improving.

The final prediction is the sum of all trees (passed through a sigmoid or softmax for classification).

### The regularized objective

XGBoost minimizes the loss **plus a penalty on tree complexity**:

$$
\text{Obj} = \sum_i L(y_i, \hat y_i) + \sum_k \Omega(f_k), \qquad \Omega(f) = \gamma T + \tfrac{1}{2}\lambda \sum_j w_j^2
$$

- $T$ is the number of leaves and $w_j$ the leaf values (the predictions).
- $\gamma$ charges for every extra leaf, and $\lambda$ shrinks the leaf values (an L2 penalty). There is also an optional L1 penalty, `alpha`.

Using both the gradient $g$ and the hessian $h$, the best value of a leaf and the **gain** of a split have closed forms:

$$
w^* = -\frac{G}{H + \lambda}, \qquad \text{Gain} = \tfrac12\left[\frac{G_L^2}{H_L+\lambda} + \frac{G_R^2}{H_R+\lambda} - \frac{(G_L+G_R)^2}{H_L+H_R+\lambda}\right] - \gamma
$$

where $G$ and $H$ are the sums of gradients and hessians in a leaf. A split is made only if its gain is positive, so $\gamma$ and $\lambda$ **prune** the tree as it grows.

## What makes it distinctive

| Feature | What it does |
|---|---|
| **Regularization** (`reg_lambda`, `reg_alpha`, `gamma`) | Controls complexity directly and fights [[Overfitting]] |
| **Second-order optimization** | Uses the hessian, so steps are better and training converges in fewer rounds |
| **Native missing values** | Learns a **default direction** for missing values at each split, so no imputation is needed |
| **Histogram-based splits** (`tree_method="hist"`, the default) | Bins values to find split points quickly, with low memory |
| **Sampling** (`subsample`, `colsample_bytree`) | Uses a random share of the rows and columns for each tree, like in a random forest, to reduce variance |
| **Early stopping** | Stops adding trees when the validation score stops improving |
| **Built-in cross-validation, custom objectives and metrics** | Flexible training and evaluation |
| **Monotonic and interaction constraints** | Force a feature to only increase (or decrease) the prediction, useful in credit and pricing |
| **GPU training** (`device="cuda"`) | Large speedups on NVIDIA GPUs for big datasets |
| **Distributed training** | Dask and Spark integrations |
| **Categorical support** (`enable_categorical=True`) | Native handling of categories as pandas `category` columns |

## Main hyperparameters

| Parameter | Effect | Typical starting point |
|---|---|---|
| `n_estimators` | Number of trees | Large (500 to 5000) together with early stopping |
| `learning_rate` (`eta`) | Size of each correction. Smaller is better but needs more trees | 0.03 to 0.1 |
| `max_depth` | Depth of each tree. Deeper trees capture more interactions and overfit more | 3 to 8 |
| `min_child_weight` | Minimum hessian sum in a leaf. Higher means more conservative | 1 to 10 |
| `subsample` | Share of rows for each tree | 0.6 to 1.0 |
| `colsample_bytree` | Share of columns for each tree | 0.6 to 1.0 |
| `reg_lambda` / `reg_alpha` | L2 / L1 penalty on leaf values | 1 / 0 |
| `gamma` | Minimum gain required to split | 0 to 5 |
| `scale_pos_weight` | Weight of the positive class, for [[Imbalanced classes]] | negatives / positives |

Practical recipe: fix a small `learning_rate` (for example 0.05), set a large `n_estimators` with **early stopping on a validation set**, then tune `max_depth`, `min_child_weight` and the sampling parameters. The number of trees and the learning rate trade off against each other.

## Example: California housing

The same public dataset as in [[House price]]: 20,640 districts, 8 features, target in units of $100,000. 5-fold cross-validation with shuffled folds, the same folds as in that note.

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from xgboost import XGBRegressor

X, y = fetch_california_housing(return_X_y=True)
cv = KFold(5, shuffle=True, random_state=42)
scoring = {"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error", "r2": "r2"}

models = {
    "HistGradientBoosting": HistGradientBoostingRegressor(random_state=42),
    "XGBoost (defaults)":   XGBRegressor(random_state=42, n_jobs=-1),
    "XGBoost (tuned)":      XGBRegressor(n_estimators=600, learning_rate=0.05, max_depth=6,
                                         subsample=0.8, colsample_bytree=0.8,
                                         random_state=42, n_jobs=-1),
}
for name, model in models.items():
    r = cross_validate(model, X, y, cv=cv, scoring=scoring)
    print(name, -r["test_rmse"].mean(), -r["test_mae"].mean(), r["test_r2"].mean())

# Early stopping: add trees until the validation score stops improving
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)
X_fit, X_val, y_fit, y_val = train_test_split(X_tr, y_tr, test_size=0.2, random_state=0)
model = XGBRegressor(n_estimators=5000, learning_rate=0.05, max_depth=6,
                     subsample=0.8, colsample_bytree=0.8,
                     early_stopping_rounds=50, random_state=42, n_jobs=-1)
model.fit(X_fit, y_fit, eval_set=[(X_val, y_val)], verbose=False)
print(model.best_iteration)
```

Install with `pip install xgboost`. On Linux this gives the CPU version, and the GPU is used with `device="cuda"` when an NVIDIA GPU is available.

| Model | RMSE | MAE | R-squared |
|---|---|---|---|
| HistGradientBoosting | 0.466 | 0.312 | 0.836 |
| XGBoost (defaults) | 0.464 | 0.307 | 0.838 |
| **XGBoost (tuned)** | **0.441** | **0.287** | **0.854** |

RMSE and MAE are in units of $100,000, so 0.441 is about $44,100.

What the results show:

- **With defaults, XGBoost and the histogram-based boosting in scikit-learn are practically tied** (RMSE 0.464 versus 0.466). They are close relatives.
- **A little tuning helps:** a lower learning rate with more trees and row and column sampling lowered the RMSE by about 5% (0.464 to 0.441).
- **Early stopping found the number of trees for you:** with a learning rate of 0.05 it stopped at **891 trees** on a separate validation set, and reached a test RMSE of 0.436.
- **Tree depth is a trade-off.** Test RMSE with 100 trees was 0.491 (depth 3), 0.457 (depth 6) and 0.484 (depth 10). The training RMSE falls from 0.457 to 0.276 to 0.051 as depth grows: depth 10 almost memorizes the training set.
- **Missing values need no imputation:** after deleting a random 10% of all the values, XGBoost still reached an RMSE of 0.539 (R-squared 0.781) with no imputation step. The loss is real, but the model runs unchanged.
- **Most important feature:** median income (`MedInc`, 48% of the gain importance), followed by average occupancy, longitude and latitude (location).
- **Speed:** on this CPU, one cross-validation run took about 7 seconds for the scikit-learn model and 30 to 40 seconds for XGBoost. Timings vary with the machine and the settings, so measure on your own data.

The data was used as it comes (no feature engineering) and the folds are shuffled, so the scores are optimistic for geographic data. See the pitfalls in [[House price]].

## Interpreting an XGBoost model

- **Feature importance** (`gain`, `weight`, `cover`) is quick, but the built-in numbers can mislead when features are correlated, and they say nothing about direction.
- **SHAP values** explain each prediction and the global effect of each feature. XGBoost has a fast built-in tree SHAP (`pred_contribs=True`). See [[SHAP]].
- **Monotonic constraints** make the model respect known business rules.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Often the most accurate on tabular data | Many hyperparameters, and results depend on tuning |
| Handles missing values, mixed scales and non-linear effects | Harder to interpret than a linear model or a single tree |
| No scaling needed (trees ignore feature scale) | Can [[Overfitting\|overfit]] on small or noisy data without regularization and early stopping |
| Regularization, early stopping and sampling built in | Cannot **extrapolate** beyond the range of the training targets |
| Fast, with GPU and distributed options | Sequential by nature, so slower to train than a random forest on one core |
| Custom losses and metrics, monotonic constraints | Probabilities need checking ([[Imbalanced classes]] and `scale_pos_weight` distort them) |

## XGBoost, LightGBM, CatBoost and scikit-learn

| Library | Notes |
|---|---|
| **XGBoost** | Mature and widely supported, level-wise growth by default, good defaults, rich ecosystem |
| **LightGBM** | Leaf-wise growth and a very fast histogram method, often faster on large data, can overfit small data |
| **CatBoost** | Best native handling of categorical features and strong defaults with little tuning |
| **`HistGradientBoosting`** (scikit-learn) | No extra dependency, close to LightGBM in design, a good first choice inside scikit-learn pipelines |

In practice the accuracy of the four is usually close, and the quality of the features and the validation matter more than the library. Try one, tune it, and compare against a simple [[baseline]].

## Pitfalls

- Using **no early stopping** and a fixed large number of trees, which overfits. Use a validation set
- Tuning on the test set, or letting early stopping see the test set. Use a separate validation set
- A learning rate that is too high with deep trees
- Random splits when the data has a time order or a spatial structure, which gives optimistic scores. See [[Data Leakage]]
- Expecting it to **extrapolate**: it never predicts outside the range of the training targets, so a rising market or a trend is underpredicted
- Using `scale_pos_weight` or resampling and then trusting the probabilities. See [[Imbalanced classes]]
- Reading built-in feature importances as causal effects
- Target encoding or other preprocessing fitted on all the data instead of inside the training folds
- Assuming it always beats a simple model: in several [[machine learning use cases/README|use cases]], logistic regression matched or beat boosting on mostly linear signals

## Used in

- [[House price]]
- [[Used-car price]]
- [[Churn]]
- [[Credit approval]]
- [[Fraud detection]]

## Related

- [[Gradient Boosting]]
- [[Random Forest]]
- [[Decision Tree]]
- [[Logistic regression]]
- [[SHAP]]
- [[scikit-learn]]
- [[MLFlow]]
