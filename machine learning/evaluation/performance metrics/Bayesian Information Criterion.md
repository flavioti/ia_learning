---
aliases:
  - BIC
  - Schwarz Information Criterion
---
#metrics #model-selection #evaluation #regression

## Definition

The **Bayesian Information Criterion (BIC)**, also called the Schwarz criterion, scores a model by how well it fits the data **minus a penalty for complexity that grows with the sample size**. It works like [[Akaike Information Criterion|AIC]] but penalizes extra parameters more heavily, so it favors **simpler models**.

>[!tip] Is the extra complexity justified by the amount of data I have?

Like AIC, it is a relative score for comparing models fit on **the same data**.

## Math notation

$$
\text{BIC} = k \ln(n) - 2\ln(\hat{L})
$$

Where:
- $k$ is the number of estimated parameters
- $n$ is the number of samples
- $\hat{L}$ is the maximum value of the likelihood function of the model
- $k \ln(n)$ is the **complexity penalty**
- $-2\ln(\hat{L})$ is the **lack of fit**

For linear regression with Gaussian errors, up to a constant shared by all models fit on the same data:

$$
\text{BIC} = n \ln\left(\frac{SS_{res}}{n}\right) + k \ln(n)
$$

Where $SS_{res}$ is the residual sum of squares.

## How to read it

- **Lower is better.** Pick the model with the lowest BIC.
- Compare through $\Delta_i = \text{BIC}_i - \text{BIC}_{\min}$:

| $\Delta$ | Evidence against model $i$ |
|----------|---------------------------|
| 0 to 2 | Not worth mentioning |
| 2 to 6 | Positive |
| 6 to 10 | Strong |
| > 10 | Very strong |

- The approximation comes from Bayesian model comparison: $\text{BIC}$ approximates $-2\ln$ of the marginal likelihood of the model. A difference of 10 corresponds to a Bayes factor of roughly $e^5 \approx 150$.
- Like AIC, BIC can be negative, and only differences matter.

## Example

The same three models and $n = 100$ as in the [[Akaike Information Criterion|AIC]] note, using $\ln(100) \approx 4.605$:

| Model | $k$ | $SS_{res}$ | AIC | BIC |
|-------|-----|------------|-----|-----|
| 1: few features | 3 | 200 | 75.31 | **83.13** (best) |
| 2: medium | 6 | 185 | **73.52** (best) | 89.15 |
| 3: many features | 11 | 180 | 80.78 | 109.44 |

The criteria disagree. AIC charges 2 per parameter and prefers model 2. BIC charges $\ln(100) \approx 4.6$ per parameter and prefers the simpler model 1.

## Python

```python
import numpy as np

rng = np.random.default_rng(42)
n = 100
x = rng.uniform(-3, 3, n)
y = 1.0 + 2.0 * x - 0.5 * x**2 + rng.normal(0, 1.0, n)   # true model: degree 2

def bic(y, y_pred, k):
    """Gaussian linear regression. k = number of fitted coefficients."""
    n = len(y)
    rss = np.sum((y - y_pred) ** 2)
    return n * np.log(rss / n) + k * np.log(n)

for degree in range(1, 7):
    coefs = np.polyfit(x, y, degree)
    y_pred = np.polyval(coefs, x)
    print(f"degree={degree}  BIC={bic(y, y_pred, k=degree + 1):7.2f}")
```

Sample output (BIC picks degree 2, the true model, with a clear margin):

```
degree=1  BIC= 104.24
degree=2  BIC=   9.10
degree=3  BIC=  10.11
degree=4  BIC=  14.68
...
```

In the same run, AIC gave degree 2 = 1.28 and degree 3 = -0.31, so AIC leaned towards the slightly larger model.

Libraries expose it directly: `statsmodels` results have `.bic`, and scikit-learn's `GaussianMixture` has `.bic(X)`, commonly used to choose the number of clusters. `LassoLarsIC(criterion="bic")` picks the regularization strength by BIC.

## Key properties

| Property | Meaning |
|----------|---------|
| **Penalty $k \ln(n)$** | Grows with data size, so for $n \geq 8$ it is stricter than AIC's $2k$ |
| **Consistent** | If the true model is among the candidates, BIC selects it with probability approaching 1 as $n \to \infty$ |
| **Favors parsimony** | Prefers smaller models than AIC |
| **Bayesian roots** | Approximates the log marginal likelihood under a vague prior |
| **Likelihood-based** | Needs a probabilistic model |
| **Relative** | Only comparable across models on identical data |

## When to use it

✅ **Use when:**
- You want the **simplest adequate model**, or want to **explain** the data
- The dataset is large and you want to avoid selecting spuriously complex models
- You are choosing the number of clusters or mixture components, or time series orders

❌ **Do not use when:**
- The goal is the **best predictions** and the sample is not large. BIC can underfit. Consider [[Akaike Information Criterion|AIC]] or cross-validation.
- The "true model" is not among the candidates. The consistency guarantee then does not apply.
- Models are fit on different data.
- High-dimensional settings with $p \gg n$. Standard BIC tends to select too many variables there, and extended versions (EBIC) exist.

## AIC vs. BIC

| | [[Akaike Information Criterion\|AIC]] | BIC |
|---|---|---|
| Formula | $2k - 2\ln(\hat{L})$ | $k\ln(n) - 2\ln(\hat{L})$ |
| Penalty per parameter | $2$ | $\ln(n)$ |
| Goal | Best predictions | Identify the true model |
| Consistent | ❌ No | ✅ Yes |
| Efficient (best predictions as $n \to \infty$) | ✅ Yes | ❌ No |
| Model size | Larger | Smaller |

>[!note] Rule of thumb
>Use **AIC** when predictive performance is the goal. Use **BIC** when you want a simple, interpretable model. When both agree, you can be more confident. When they disagree, validate on held-out data.

## Pitfalls

- **Same data, same target:** never compare the scores of models fit on different datasets or with a transformed target.
- **Counting $k$:** include every estimated parameter, and count them the same way for all models.
- **Absolute meaning:** a low BIC says the model is the best of those compared, not that it is a good model. Check residuals and a held-out metric.
- **Misusing the Bayes factor reading:** the thresholds above are rough guides, not tests.

## Related

- [[Akaike Information Criterion]]
- [[Adjusted R-squared]]
- [[R-squared]]
- [[MSE - Mean Squared Error]]
- [[Evaluating regression model metrics]]
