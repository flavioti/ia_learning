---
aliases:
  - Learning Curve
  - Learning curves
  - Learning curve linear regression
---
#evaluation #diagnostics #linear-regression #bias-variance

# Learning Curve - Linear regression

A **learning curve** plots a model's error on the **training data** and on **validation data** as the **size of the training set grows**. Its shape shows whether the model is limited by **bias** (too simple) or by **variance** (too sensitive to the training sample), and it answers a practical question: **would more data help?**

>[!tip] Read it as two lines that move toward each other. The **gap** between them is the variance, and the **height** where they meet is the bias plus the noise.

This note shows how it looks for [[Linear Regression|linear regression]]. For the same idea in classification see [[Logistic regression]], and for the diagnosis in words see [[Underfitting]] and [[Overfitting]].

## How to build one

1. Choose several **training set sizes** (for example 30, 50, 100, 200 up to all the data).
2. For each size, train the model on that many rows and measure the error on the **training rows** and on a **fixed validation set** that the model never saw.
3. Repeat with several random splits and plot the **mean and the spread**.
4. Plot error (for example [[RMSE - Root Mean Squared Error]]) against the training size.

```python
import numpy as np
from sklearn.model_selection import learning_curve, ShuffleSplit
from sklearn.linear_model import LinearRegression

cv = ShuffleSplit(n_splits=20, test_size=0.25, random_state=0)
sizes, train_scores, val_scores = learning_curve(
    LinearRegression(), X, y,
    train_sizes=[30, 50, 80, 120, 200, 350, 600, 1000, 1500],   # rows (or fractions)
    cv=cv, scoring="neg_root_mean_squared_error", n_jobs=-1)

train_rmse = -train_scores.mean(axis=1)     # scikit-learn scores are negative errors
val_rmse = -val_scores.mean(axis=1)
```

scikit-learn's `learning_curve` does steps 2 and 3. Put the preprocessing (for example scaling) inside a scikit-learn `Pipeline`, so that it is fitted only on the training rows. See [[K-Fold Cross-Validation]] and [[Data Leakage]].
## What linear regression looks like

Linear regression has very few parameters (one per feature), so its behavior is easy to predict:

| Training size  | Training error                                                                                                         | Validation error                                                       |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Very small** | Very **low**: with few rows the line can fit almost every point (even exactly, when there are more features than rows) | Very **high**: the line learned from a tiny sample does not generalize |
| **Growing**    | **Rises**: a single line cannot pass through more and more points                                                      | **Falls**: the estimate of the coefficients improves                   |
| **Large**      | Settles at a plateau                                                                                                   | Settles at a plateau, close to the training error                      |

The final level of both lines is set by the **noise floor** (the irreducible error that no model can remove) plus the **bias** (what a straight line cannot capture).

## Three typical cases

Generated data, **not real data**, with a known noise level, so the best possible error is known (the dashed line). RMSE, mean of 20 random splits.

![[learning-curve-linear-regression-cases.png]]

### A. Good fit

The true relationship is linear (5 features, noise of 1.0). Training and validation error **meet at the noise floor**, about 1.0.

| Training rows | Training RMSE | Validation RMSE |
|---|---|---|
| 30 | 0.93 | 1.09 |
| 80 | 0.96 | 1.01 |
| 200 | 0.96 | 0.99 |
| 600 | 0.98 | 0.98 |
| 1,500 | 0.98 | 0.98 |

The gap closes after about 200 to 300 rows, and **more data adds nothing**. The model is as good as it can be: the remaining error is noise.

### B. High bias (underfitting)

The true relationship is a wave (a sine curve plus a trend, noise of 0.3), and the model is a straight line. Both curves **flatten at 1.40, far above the noise floor of 0.3**.

| Training rows | Training RMSE | Validation RMSE |
|---|---|---|
| 30 | 1.37 | 1.43 |
| 200 | 1.40 | 1.40 |
| 1,500 | 1.40 | 1.39 |

- **High error on both lines, with a tiny gap.** The model is too simple.
- **More data does not help:** the lines have already converged, at the wrong level.
- **What helps:** a richer model or better features: polynomial or interaction terms, binning, or a non-linear model. See [[Underfitting]].

### C. High variance (overfitting)

The true relationship is linear, but there are **40 features** and only 4 of them matter (noise of 2.0). With few rows the line fits the training sample, noise included.

| Training rows | Training RMSE | Validation RMSE |
|---|---|---|
| 30 | **0.00** | **4.71** |
| 80 | 1.45 | 2.94 |
| 200 | 1.83 | 2.27 |
| 600 | 1.95 | 2.09 |
| 1,500 | 1.99 | 2.05 |

- **A large gap at small sizes:** with 30 rows and 41 parameters, the line passes through every point (training error 0), and the validation error is huge.
- **The gap closes as data grows,** and both lines reach the noise floor of 2.0. Here **more data helps**.
- **What helps with little data:** fewer features, or **regularization**. See [[Ridge and Lasso Regression]] and [[Overfitting]].

With a penalty chosen by cross-validation (`RidgeCV`), the validation error at the smallest sizes improves:

| Training rows | Linear regression | Ridge (penalty chosen by cross-validation) |
|---|---|---|
| 30 | 4.71 | **3.84** |
| 50 | 5.00 | **3.25** |
| 80 | 2.94 | **2.73** |
| 350 and more | 2.15 and below | same |

At 350 rows and above the two are identical, because there is enough data to estimate the coefficients without help. A **fixed, untuned penalty can hurt**: with `alpha=100` the same case got a *worse* validation error than plain linear regression at 80, 200 and 600 rows (3.33, 2.61 and 2.17), because the penalty was too strong. Choose the penalty by cross-validation.

## Diagnosis guide

| What you see | Diagnosis | What to do |
|---|---|---|
| Both lines **high** and **close together**, flat | **High bias** (underfitting) | A more expressive model, new features, less regularization. More data will not help |
| **Big gap**, training low and validation high | **High variance** (overfitting) | More data, fewer features, regularization, a simpler model |
| Lines **converge** and still decreasing at the right edge | The model still **benefits from more data** | Collect more data, if it is affordable |
| Lines converge and are **flat**, at an acceptable level | **Good fit** | Stop. Any remaining error is mostly noise |
| Validation error **unstable**, with a wide band | Outliers or too small a validation set | Check the data. Use more splits |

>[!warning] Compare the plateau to something. Without a **noise floor, a [[baseline]] or a business target**, a flat curve at 1.4 does not tell you whether that is good. In real data the noise floor is unknown, so use a stronger model (for example boosting) as a reference.

## A real dataset: California housing

The same data used in [[House price]]: 20,640 districts, 8 features, target in units of $100,000. Linear regression with scaled features, RMSE as a function of the training size. Left: the raw features. Middle: the same model after clipping the features to their 0.5 and 99.5 percentiles. Right: gradient boosting, for comparison.

![[learning-curve-california-housing.png]]

| Training rows | Raw: train / validation | Clipped: train / validation | Gradient boosting: train / validation |
|---|---|---|---|
| 50 | 0.61 / **4.28** | 0.60 / 0.80 | 0.71 / 0.97 |
| 200 | 0.68 / 3.86 | 0.66 / 0.68 | 0.28 / 0.71 |
| 800 | 0.70 / 2.82 | 0.67 / 0.67 | 0.20 / 0.59 |
| 3,200 | 0.71 / 1.94 | 0.66 / 0.67 | 0.30 / 0.51 |
| 12,800 | 0.72 / 0.73 | 0.67 / 0.66 | 0.39 / 0.48 |

What the curves show:

- **Raw features: the validation error is enormous at small sizes** (4.28, when the typical error is about 0.7) and the band is very wide. The reason is **outliers**: the average occupancy per household reaches 1,243, while the median is 2.8. A line trained on a few hundred rows gives such an extreme coefficient to these values that some validation rows get absurd predictions. The curve does not tell you "you need 12,000 rows". It tells you "the data has outliers".
- **After clipping, the curve is clean:** both lines meet at about **0.66 with only 400 rows**, much earlier and lower than with the raw data (0.73). (Here the limits were computed on all the data to keep the example short. In a real project, fit them on the training rows only.)
- **A flat, converged curve at 0.66 is a high-bias signature.** More data will not improve a linear model. It is limited by the shape of the model, not by the amount of data.
- **Gradient boosting reaches 0.48 and is still falling** at 12,800 rows, with a visible gap, so it uses more data well. The reduction from 0.66 to 0.48 is the **bias that the linear model could not remove**. See [[Gradient Boosting]]. The training error of boosting rises with more data because the model has a fixed number of trees (100), so it can memorize 800 rows but not 12,800.

## What a learning curve does **not** tell you

- **Why** the error is high (noise, outliers, missing features, wrong form). It points to the **kind** of problem only.
- **Whether the data is representative.** The curve uses a random validation set from the same data. For data with a time order, use a [[Backtest]] instead of random splits.
- **Whether the metric is the business metric.**

## Learning curve vs similar tools

| Tool | X axis | Question it answers |
|---|---|---|
| **Learning curve** | **Training set size** | Would more data help? Is it bias or variance? |
| Validation curve | A **hyperparameter** (for example the penalty `alpha`, the polynomial degree) | Which model complexity is best? |
| Training history | **Epochs or boosting rounds** | When to stop training? See [[XGBoost]] early stopping |
| [[K-Fold Cross-Validation]] | None | How well will the model do on new data? |

## Common pitfalls

- Reading the curve without a **reference level** (noise floor, baseline or target)
- Using **one split**: the curve will be noisy. Average several splits and show the spread
- Computing the **scaling or clipping on all the data** instead of only on the training rows ([[Data Leakage]])
- A **tiny validation set**, which makes the validation line jump around
- Starting with sizes too small for the number of features: a linear model with more features than rows fits the training data exactly, and its numbers mean little
- Concluding "I need more data" when the curves have already converged (high bias), or "I need a bigger model" when there is a big gap (high variance)
- Ignoring **outliers**: they can look like a data-size problem (see the California housing example)
- Using random splits for time-ordered data

## Related

- [[Linear Regression|Linear Regression]]
- [[Ridge and Lasso Regression]]
- [[Underfitting]]
- [[Overfitting]]
- [[K-Fold Cross-Validation]]
- [[Model Evaluation]]
- [[baseline]]
- [[House price]]
- [[Backtest]]
- [[Evaluating regression model metrics]]
