---
aliases:
  - AIC
---
#metrics #model-selection #evaluation #regression

## Definition

The **Akaike Information Criterion (AIC)** scores a model by how well it fits the training data **minus a penalty for the number of parameters**. It estimates how much information is lost when the model approximates the true process, and it is used to **compare models fit on the same data**.

>[!tip] Which model gives the best trade-off between fit and simplicity?

It is a relative score: only differences between models matter. The absolute value of AIC means nothing on its own.

## Math notation

$$
\text{AIC} = 2k - 2\ln(\hat{L})
$$

Where:
- $k$ is the number of estimated parameters in the model
- $\hat{L}$ is the maximum value of the likelihood function of the model
- $2k$ is the **complexity penalty**
- $-2\ln(\hat{L})$ is the **lack of fit** (lower means a better fit)

For linear regression with Gaussian errors, up to a constant shared by all models fit on the same data:

$$
\text{AIC} = n \ln\left(\frac{SS_{res}}{n}\right) + 2k
$$

Where $n$ is the number of samples and $SS_{res}$ is the residual sum of squares.

For small samples, use the corrected version, which is stricter:

$$
\text{AIC}_c = \text{AIC} + \frac{2k(k + 1)}{n - k - 1}
$$

A common rule of thumb is to use $\text{AIC}_c$ when $n / k < 40$. It converges to AIC as $n$ grows.

## How to read it

- **Lower is better.** Pick the model with the lowest AIC.
- Compare through the difference $\Delta_i = \text{AIC}_i - \text{AIC}_{\min}$:

| $\Delta$ | Support for model $i$ |
|----------|----------------------|
| 0 to 2 | Essentially as good as the best model |
| 4 to 7 | Considerably less support |
| > 10 | Essentially no support |

- AIC can be negative. That is fine, because only the ordering matters.
- Models must be fit on **the same data and the same target** (and for linear regression, the same transformation of $y$).

## Example

Three regression models fit on the same $n = 100$ samples, using $\text{AIC} = n \ln(SS_{res}/n) + 2k$:

| Model | Parameters $k$ | $SS_{res}$ | AIC |
|-------|---------------|------------|-----|
| 1: few features | 3 | 200 | **75.31** |
| 2: medium | 6 | 185 | **73.52** (best) |
| 3: many features | 11 | 180 | **80.78** |

Model 3 has the smallest error, but its extra 5 parameters over model 2 do not pay for themselves, so its AIC is worse. Model 2 wins.

## Python

```python
import numpy as np

rng = np.random.default_rng(42)
n = 100
x = rng.uniform(-3, 3, n)
y = 1.0 + 2.0 * x - 0.5 * x**2 + rng.normal(0, 1.0, n)   # true model: degree 2

def aic(y, y_pred, k):
    """Gaussian linear regression. k = number of fitted coefficients."""
    n = len(y)
    rss = np.sum((y - y_pred) ** 2)
    return n * np.log(rss / n) + 2 * k

for degree in range(1, 7):
    coefs = np.polyfit(x, y, degree)
    y_pred = np.polyval(coefs, x)
    print(f"degree={degree}  AIC={aic(y, y_pred, k=degree + 1):7.2f}")
```

Sample output (degrees 2 and 3 are very close, which shows AIC can lean towards a slightly more complex model than the true one):

```
degree=1  AIC=  99.03
degree=2  AIC=   1.28
degree=3  AIC=  -0.31
degree=4  AIC=   1.66
...
```

Libraries expose it directly: `statsmodels` results have `.aic`, and scikit-learn models such as `GaussianMixture` have `.aic(X)`. For linear models, `LassoLarsIC(criterion="aic")` picks the regularization strength by AIC.

## Key properties

| Property | Meaning |
|----------|---------|
| **Penalty $2k$** | Each extra parameter must reduce $-2\ln(\hat{L})$ by more than 2 to be worth it |
| **Optimizes prediction** | It aims at the model that predicts new data best, not at the "true" model |
| **Asymptotically equivalent to leave-one-out cross-validation** | For many model families |
| **Not consistent** | As $n \to \infty$ it does not always settle on the true model. It can keep favoring a slightly bigger one |
| **Likelihood-based** | Needs a probabilistic model (or a likelihood). It does not apply to arbitrary scoring rules |
| **Relative** | Meaningful only when comparing models on identical data |

## When to use it

✅ **Use when:**
- Comparing models of different complexity: number of features, polynomial degree, ARIMA orders, number of mixture components
- The goal is **prediction**
- You want a cheap alternative to cross-validation

❌ **Do not use when:**
- Models are fit on different datasets or targets
- You need a measure of absolute quality. AIC does not say whether *any* of the models is good.
- The goal is to identify the true underlying structure and $n$ is large. Consider [[Bayesian Information Criterion]].
- You can afford proper validation. Held-out error or cross-validation is more direct.

## AIC vs. BIC

| | AIC | [[Bayesian Information Criterion\|BIC]] |
|---|---|---|
| Penalty per parameter | $2$ | $\ln(n)$ |
| Preference | Predictive accuracy | Simpler, "true" model |
| Penalty gets stronger with $n$ | ❌ No | ✅ Yes (for $n \geq 8$, BIC's penalty is larger) |
| Tends to | Select slightly larger models | Select smaller models |

## Pitfalls

- **Counting $k$:** include every estimated parameter (intercept, coefficients, and the error variance for Gaussian models). Be consistent across models, because only the differences matter.
- **Small samples:** use $\text{AIC}_c$.
- **Overlooking misspecification:** the best of a bad set of models is still bad. Check residuals and an out-of-sample metric too.
- **Data-driven search:** testing many models and picking the best AIC still risks overfitting the selection.

## Related

- [[Bayesian Information Criterion]]
- [[Adjusted R-squared]]
- [[R-squared]]
- [[MSE - Mean Squared Error]]
- [[Evaluating regression model metrics]]
