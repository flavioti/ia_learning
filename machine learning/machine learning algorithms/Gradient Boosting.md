---
aliases:
  - Gradient Boosted Trees
  - GBM
  - GBDT
  - Gradient Boosting Machine
---
#ml-model #supervised-learning #classification #regression #tree-based #ensemble

# Gradient Boosting

**Gradient boosting** builds a strong model by adding many **small decision trees one after another**, where each new tree is trained to **correct the errors of the model built so far**. It is often the most accurate algorithm for **tabular data** (rows and columns), for both regression and classification.

>[!tip] Think of a team of weak models where each member only studies the mistakes left by the previous ones. Added together, with small steps, they make a strong model.

The trees are small ([[Decision Tree]] with a depth of about 3 to 8), so each one alone is a **weak learner**. The shared tree concepts are in [[Decision Tree]], [[Decision Tree Regressor]] and [[Decision Tree Classifier]]. The idea of averaging **independent** trees is [[Random Forest]]. Boosting is different: the trees are **dependent and sequential**.

## How it works

1. Start with a constant prediction (for example the mean of the target).
2. Measure how wrong the current model is on every row: the **residuals** (the "pseudo-residuals" for other losses).
3. Fit a small tree to predict those residuals.
4. Add the tree to the model, **scaled by a small learning rate**.
5. Repeat for a number of rounds, or until the validation error stops improving.

$$
F_0(x) = \bar y, \qquad F_m(x) = F_{m-1}(x) + \eta \, h_m(x)
$$

where $h_m$ is the tree fitted to the errors of $F_{m-1}$ and $\eta$ is the learning rate. The prediction is the **sum of all the trees**.

### Why "gradient"

The residual is the **negative gradient of the loss** with respect to the current prediction. Boosting is gradient descent in the space of functions: each tree is a step in the direction that lowers the loss the most.

| Task | Loss | What each tree fits (negative gradient) |
|---|---|---|
| Regression | Squared error | The plain residual $y - \hat y$ |
| Regression | Absolute error or Huber ([[Huber Loss]]) | The sign of the residual (clipped for large errors), which is robust to outliers |
| Binary classification | Log loss ([[Crossentropy]]) | $y - p$, where $p$ is the current predicted probability |
| Ranking, Poisson, survival and others | The corresponding loss | Its gradient |

Because only the **gradient** is needed, any differentiable loss can be used. For classification the sum of the trees is on the **log-odds** scale, and a sigmoid turns it into a probability (the same output scale as in [[Logistic regression|logistic regression]]).

## A small example by hand

40 points of a noisy curve, trees of depth 2, learning rate 0.5, three rounds. The loop below is the whole algorithm, and its predictions are **identical** to scikit-learn's `GradientBoostingRegressor` with the same settings (maximum difference 0.0).

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor

rng = np.random.default_rng(0)
x = np.sort(rng.uniform(0, 6, 40))
y = np.sin(x) + 0.2 * x + rng.normal(0, 0.15, 40)
X = x.reshape(-1, 1)

eta, rounds = 0.5, 3
pred = np.full(len(y), y.mean())              # F0: a constant
for m in range(rounds):
    residual = y - pred                        # negative gradient of the squared error
    tree = DecisionTreeRegressor(max_depth=2, random_state=0).fit(X, residual)
    pred = pred + eta * tree.predict(X)        # a small step
    print(m + 1, np.sqrt(np.mean((y - pred) ** 2)))

sk = GradientBoostingRegressor(n_estimators=rounds, learning_rate=eta, max_depth=2,
                               random_state=0).fit(X, y)
print(np.abs(pred - sk.predict(X)).max())      # 0.0: the same model
```

| Round | Training RMSE |
|---|---|
| 0 (constant mean) | 0.511 |
| 1 | 0.331 |
| 2 | 0.238 |
| 3 | 0.185 |

Each tree removes a part of the remaining error, and the learning rate decides how big a part.

## Main hyperparameters

| Parameter | Effect | Typical range |
|---|---|---|
| `n_estimators` | Number of trees (rounds) | 100 to several thousand, with early stopping |
| `learning_rate` ($\eta$, shrinkage) | Size of each step. Smaller needs more trees but generalizes better | 0.01 to 0.2 |
| `max_depth` | Depth of each tree, which sets the **interaction order** the model can learn | 3 to 8 |
| `subsample` | Share of rows used for each tree (stochastic gradient boosting). Less than 1 reduces variance | 0.5 to 1.0 |
| `max_features` / `colsample` | Share of features per tree or split | 0.5 to 1.0 |
| `min_samples_leaf` / `min_child_weight` | Minimum size of a leaf. Larger is more conservative | 1 to 50 |
| Regularization (`reg_lambda`, `gamma` in [[XGBoost]]) | Penalizes complex trees | Library-specific |
| `n_iter_no_change` / early stopping | Stops when the validation score stops improving | 10 to 50 rounds |

### The learning rate and the number of trees go together

A small learning rate needs many more trees. A large one converges fast but overfits sooner. The chart shows the validation error of three runs (trees of depth 3) on California housing (the data of [[House price]]):

![[gradient-boosting-learning-rate.png]]

| Learning rate | Best validation RMSE | At how many trees | Training RMSE at 1,000 trees |
|---|---|---|---|
| 0.5 | 0.500 | 355 | 0.180 |
| 0.1 | **0.482** | 943 | 0.352 |
| 0.02 | 0.517 | 1,000 (still improving) | 0.464 |

- **Learning rate 0.5 learns fast** (it is the best curve at the start) but **flattens and rises** after about 350 trees, and the training error (0.18) is far below the validation error: it overfits.
- **Learning rate 0.1** is slower and ends **lower**. This is the usual lesson: a smaller step plus more trees generalizes better.
- **Learning rate 0.02 is too slow for 1,000 trees:** it is still improving, and would need many more trees.
- **Practical rule:** fix a small learning rate (0.05 to 0.1), set a large `n_estimators`, and let **early stopping** pick the number of trees. The scikit-learn version has it built in (`n_iter_no_change`, `validation_fraction`). In the same data, with a rate of 0.05 and depth 4 it stopped at **686 trees** (test RMSE 0.469).

## Depth controls the interactions

A tree of depth $d$ can capture interactions among up to $d$ features. California housing, 300 trees, learning rate 0.1, test RMSE:

| `max_depth` | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| RMSE | 0.622 | 0.524 | 0.493 | 0.455 | 0.450 |

Depth 1 (stumps) makes an **additive model**, with no interactions, and is clearly worse. The gain flattens after about depth 5. Deeper trees fit the data more closely and overfit more easily, so check them on validation data.

## Comparison with other tree models

California housing, same split, RMSE on the test set (in units of $100,000, lower is better):

| Model | Test RMSE |
|---|---|
| Single decision tree (depth 6) | 0.706 |
| [[Random Forest Regressor]] (200 trees) | 0.512 |
| Gradient boosting, default (100 trees, depth 3, rate 0.1) | 0.539 |
| **Gradient boosting, tuned** (500 trees, depth 4, rate 0.05, subsample 0.8) | **0.470** |
| `HistGradientBoostingRegressor` (defaults) | **0.461** |

- **A single tree is clearly worse** than any ensemble.
- **Untuned boosting (0.539) is worse than the random forest (0.512).** Boosting needs a sensible learning rate, number of trees and depth. A random forest is more forgiving.
- **Tuned boosting beats the forest** (0.470 versus 0.512). This is the usual result on tabular data.
- **The histogram version is the best here and much faster** (the fit took about 0.3 seconds, against about 2 seconds for the default classic version and about 12 seconds for the tuned one, on one CPU run). It bins the features, so it scales to large data. See below.

| | Random forest | Gradient boosting |
|---|---|---|
| How trees are built | Independently, in parallel | Sequentially, each corrects the previous |
| What it reduces | Mainly **variance** (averages deep, overfit trees) | Mainly **bias** (adds shallow trees that fix errors) |
| Tree depth | Deep | Shallow |
| Tuning sensitivity | Low | **High** |
| Overfitting risk | Low | Higher, controlled by the learning rate, depth and early stopping |
| Typical accuracy | Strong | Usually the highest on tabular data |

## Implementations

| Library | Notes |
|---|---|
| scikit-learn `GradientBoostingRegressor` / `Classifier` | The classic, exact version. Clear and complete, but slow on large data |
| scikit-learn `HistGradientBoostingRegressor` / `Classifier` | Histogram-based, fast, native missing values and categories, early stopping. A good default inside scikit-learn |
| [[XGBoost]] | Regularized objective, second-order gradients, native missing values, GPU and distributed training |
| LightGBM | Very fast histogram method with leaf-wise growth. Can overfit small data |
| CatBoost | Strong native handling of categorical features and good defaults |

The accuracy of the modern libraries is usually close. The quality of the features and the validation matter more than the choice of library.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Often the most accurate on tabular data | Many hyperparameters, and **needs tuning** |
| Captures non-linear effects and interactions automatically | Sequential: harder to parallelize than a random forest (the modern libraries do it well within each tree) |
| Handles mixed feature types, no scaling needed | Can **overfit** on small or noisy data |
| Works with many losses (regression, classification, ranking, robust losses) | **Cannot extrapolate** beyond the range of the training targets |
| Modern versions handle missing values | Less interpretable than a linear model or a single tree |
| Feature importance and [[SHAP]] explanations | Probabilities may need calibration, and weights for rare classes distort them |

### It cannot extrapolate

Trees predict averages of training targets, so the model **never goes outside the range it saw**. In a test with a straight line $y = 2x$ trained on $x$ between 0 and 5, the model predicted **10.2 at $x = 10$**, when the true value is 20. It also gives 10.2 at $x = 5$, and stays flat beyond that. For trends, add lag or trend features, model the **change** instead of the level, or combine it with a linear model. See [[Backtest]] and [[Used-car price]].

## Interpreting the model

- **Feature importance** (split gain or count) is quick, but it can mislead with correlated features.
- **[[SHAP]] values** give exact, per-prediction contributions and a reliable global ranking.
- **Monotonic constraints** force a feature to only raise (or only lower) the prediction, which is useful in credit, pricing and regulated areas.

## When to use it

- **Tabular data** with enough rows and a mix of numeric and categorical features.
- When **accuracy** matters more than a fully transparent model.
- Always as a **challenger** against a simple [[baseline]]: in several use cases of this vault, logistic regression matched or beat boosting when the signal was mostly linear or noisy.

Other tools fit better for raw images, audio and text (neural networks), for strong trends and extrapolation (linear or time series models such as [[ARIMA]]), and for very small data (a regularized linear model such as [[Ridge and Lasso Regression]]).

## Common pitfalls

- Using the **default** settings and concluding that boosting is worse than a random forest
- A **high learning rate** with deep trees and no early stopping
- Tuning and early stopping on the **test set**: keep a separate validation set
- Random splits when the data has a time order or a spatial structure, which gives optimistic scores. See [[Data Leakage]]
- Expecting it to **extrapolate** trends
- Using class weights or resampling for rare classes and then trusting the probabilities. See [[Imbalanced classes]]
- Reading the built-in feature importance as the truth about causes
- Fitting preprocessing (encoding, target encoding) on all the data instead of inside the training folds

## Used in

- [[House price]]
- [[Used-car price]]
- [[Churn]]
- [[Credit approval]]
- [[Fraud detection]]

## Related

- [[XGBoost]]
- [[Decision Tree]]
- [[Random Forest]]
- [[Logistic regression]]
- [[SHAP]]
- [[Overfitting]]
- [[scikit-learn]]
- [[Machine Learning Algorithms|Machine learning algorithms]]
