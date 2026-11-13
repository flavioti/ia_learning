#regression #regularization #supervised-learning
# Ridge and Lasso Regression

**Ridge** and **Lasso** are [[Linear Regression|linear regression]] with a **penalty on the size of the coefficients**. This technique is called **regularization**. It makes the model simpler, so it **overfits less** on new data. See [[Overfitting]].

| | Ridge | Lasso | Elastic Net |
|---|---|---|---|
| Also called | L2 regularization | L1 regularization | L1 + L2 |
| Penalty | Sum of **squared** coefficients | Sum of **absolute** coefficients | A mix of both |
| Effect on coefficients | **Shrinks** them toward 0, rarely to exactly 0 | **Shrinks** them and sets some to **exactly 0** | Both |
| Feature selection | No | **Yes**, built in | Yes |
| scikit-learn | `Ridge` | `Lasso` | `ElasticNet` |

## The idea

Plain linear regression picks the coefficients $w_j$ that minimize the squared error. With few samples, many features, or correlated features, it can use **large coefficients** to chase noise. Regularization adds a cost for large coefficients, so the model has to justify each one.

**Ridge:**

$$
\text{Loss} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \alpha \sum_{j=1}^{p} w_j^2
$$

**Lasso:**

$$
\text{Loss} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 + \alpha \sum_{j=1}^{p} |w_j|
$$

- The first term is the usual squared error, as in [[MSE - Mean Squared Error]].
- The second term is the penalty. $\alpha$ sets its strength.
- $\alpha = 0$ gives plain linear regression. A very large $\alpha$ pushes all coefficients to 0, and the model predicts roughly the mean.
- The intercept is **not** penalized.

>[!note] In scikit-learn the exact scaling of the loss differs between `Ridge` and `Lasso`, so the same $\alpha$ does **not** mean the same strength in both. Choose $\alpha$ separately for each estimator.

### Why Lasso sets coefficients to exactly 0

The L1 penalty has a sharp corner at 0, so the best solution often lands exactly on 0 for the least useful features. The L2 penalty is smooth, so it only gets coefficients close to 0. That is why Lasso doubles as **feature selection**.

### Why Ridge helps with correlated features

When two features carry almost the same information (area and number of rooms), the plain solution is unstable: the coefficients can be huge with opposite signs. Ridge has a closed form that stays well behaved:

$$
w = (X^\top X + \alpha I)^{-1} X^\top y
$$

Adding $\alpha I$ makes the matrix invertible and spreads the weight across correlated features.

## Bias and variance

| $\alpha$ | Coefficients | Model | Risk |
|---|---|---|---|
| Too small | Large, like plain regression | Flexible | **Overfitting** (high variance) |
| Just right | Moderate | Balanced | Best generalization |
| Too large | Close to 0 | Too simple | **Underfitting** (high bias). See [[Underfitting]] |

## Rules of use

- **Scale the features first** (`StandardScaler`). The penalty treats all coefficients equally, so a feature in large units would be penalized unfairly. Use a `Pipeline` so the scaler is fitted on the training data only.
- **Choose $\alpha$ by cross-validation**: `RidgeCV`, `LassoCV` or `GridSearchCV`. See [[K-Fold Cross-Validation]].
- **Use Lasso or Elastic Net** when you suspect only a few features matter. Use **Ridge** when most features contribute a little, or when features are correlated.
- Lasso tends to pick **one** of a group of correlated features and drop the others, which can be unstable. Elastic Net handles groups better.

## Example

Few samples (80), many features (30), of which only 5 carry signal. This setup is easy to overfit. The $\alpha$ values are chosen by cross-validation, and the RMSE is measured on a held-out 40%.

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

X, y = make_regression(n_samples=80, n_features=30, n_informative=5, noise=20.0, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

def rmse(model):
    return mean_squared_error(y_test, model.predict(X_test)) ** 0.5

linear = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
ridge = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 30))).fit(X_train, y_train)
lasso = make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=0)).fit(X_train, y_train)

print(rmse(linear))                                       # 32.11
print(ridge[-1].alpha_, rmse(ridge))                      # 0.36, 30.13
print(lasso[-1].alpha_, rmse(lasso))                      # 1.926, 25.79
print((np.abs(lasso[-1].coef_) > 1e-8).sum())             # 16 coefficients kept out of 30
```

| Model | $\alpha$ (cross-validated) | Test RMSE | Non-zero coefficients |
|---|---|---|---|
| Linear regression | none | 32.11 | 30 of 30 |
| Ridge | 0.36 | 30.13 | 30 of 30 |
| **Lasso** | 1.93 | **25.79** | **16 of 30** |

Both regularized models beat plain regression, and Lasso also removed 14 of the 30 features. This is a single small split, so treat the numbers as an illustration and not as a general ranking.

### Too much regularization

Using Ridge with a fixed $\alpha$ instead of a cross-validated one shows how strength changes the fit (same data, test RMSE):

| $\alpha$ | Sum of squared coefficients | Test RMSE |
|---|---|---|
| 0.01 | 19,599 | 32.04 |
| 1 | 17,611 | 28.85 |
| 10 | 9,885 | 62.14 |
| 100 | 1,635 | 136.80 |
| 10,000 | 0.6 | 175.30 |

The coefficients keep shrinking as $\alpha$ grows. A little regularization (around $\alpha = 1$) helps, but a large $\alpha$ makes the model **underfit** and the error explodes. How large is "too large" depends on the data scale, which is why $\alpha$ should be tuned and not guessed.

## In practice

- In [[House price]], `Ridge` was the linear baseline. Its R-squared of 0.601 trailed the tree models, because the relationship with location is not linear. Regularization limits overfitting but does not add non-linearity.
- Neural networks use the same idea under other names: **weight decay** (L2) and dropout. See [[neural networks]].
- Regularization pairs well with [[Feature Engineering]], especially when you create many features, such as interactions and polynomials.

## Related

- [[Linear Regression]]
- [[Overfitting]]
- [[Underfitting]]
- [[K-Fold Cross-Validation]]
- [[Parsimonious Model]]
- [[scikit-learn]]
- [[House price]]
