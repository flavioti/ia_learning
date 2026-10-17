## Continuous Variable

A continuous variable is a numeric variable that can take **any value within a range**, including decimals. It is obtained by **measuring**. (Age, House price, Income)
## Key Characteristics

- Infinite possible values within an interval
- Obtained by **measuring** (time, weight, money, probability)
- Arithmetic is meaningful (mean, variance, differences, ratios)
- Described by continuous distributions: Normal (Gaussian), Log-normal, Exponential, Gamma, Uniform, Beta
- Plotted with histograms, density plots (KDE) and box plots

Related: [[Discrete Variable]] · [[Categorical columns]] · [[feature engineering]]

Examples in ML

| Variable                   | Context                 | Typical range             |
| -------------------------- | ----------------------- | ------------------------- |
| Age (as a measurement)     | Credit scoring          | 0 to 120                  |
| Income                     | Credit / risk           | ≥ 0, heavily right-skewed |
| Latency (ms)               | Model serving           | ≥ 0                       |
| House price                | Regression target       | ≥ 0                       |
| Temperature                | Sensor / IoT            | any real value            |
| Predicted probability      | Classifier output       | 0 to 1                    |
| Learning rate              | Hyperparameter          | e.g. 1e-5 to 1e-1         |
| Embedding dimension values | Neural network          | any real value            |
| Temperature / top-p        | LLM sampling parameters | 0 to 2 / 0 to 1           |

---

## Discrete vs. Continuous

| | Discrete | Continuous |
|---|---|---|
| Values | Countable, with gaps | Any value in a range |
| Obtained by | Counting | Measuring |
| Example | Number of clicks | Time on page (s) |
| Distributions | Binomial, Poisson | Normal, Exponential |
| Chart | Bar chart | Histogram / density |
| Regression target | Poisson / Negative Binomial | Linear regression, gradient boosting (MSE / MAE) |

**Gray zone:** a continuous quantity is always *recorded* discretely (age in whole years, price in cents). If there are many distinct values and the order and distance matter, treat it as continuous.

---

## How It Affects ML

### Modeling

| Aspect | Guidance |
|---|---|
| **Regression target** | Linear regression, Ridge/Lasso, gradient boosting, neural networks. Loss: MSE, MAE, Huber |
| **Skewed target** | Predict `log(y)` and convert back, or use Gamma / log-normal assumptions |
| **Tree-based models** | Split on thresholds. Invariant to monotonic transforms and scaling |
| **Linear, KNN, SVM, neural networks** | Sensitive to scale. **Scaling is required** |
| **Distance-based models** | A feature with a large range (income) dominates a small one (age) without scaling |

### Feature engineering

| Technique | Purpose | Notes |
|---|---|---|
| **Standardization** (z-score) | Mean 0, std 1 | Good default for linear models, NN, SVM |
| **Min-max scaling** | Rescale to [0, 1] | Sensitive to outliers |
| **Robust scaling** | Uses median and IQR | Good with outliers |
| **Log / Box-Cox / Yeo-Johnson** | Reduce right skew, stabilize variance | Log needs positive values |
| **Clipping / winsorizing** | Limit outliers | Choose limits on train data only |
| **Binning** (discretization) | Capture non-linear effects, handle noise | See [[Discretization]] |
| **Polynomial / interaction features** | Let linear models fit non-linear patterns | Scale afterwards |
| **Missing value imputation** | Mean, median, model-based | Add a "was missing" flag |

### Pitfall: data leakage in scaling

Fit scalers on the **training set only**, then apply them to validation and test sets. Fitting on the full dataset leaks test information. See [[Data Leakage]]. Use a `Pipeline` to enforce this.

---

## Code Example

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, StandardScaler

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "income": rng.lognormal(mean=10, sigma=0.8, size=1000),   # skewed, continuous
    "age": rng.normal(40, 12, 1000).clip(18, 90),             # continuous
})
df["price"] = 0.002 * df["income"] + 50 * df["age"] + rng.normal(0, 500, 1000)

X, y = df[["income", "age"]], df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Skewed feature: Yeo-Johnson. Symmetric feature: standard scaling.
# Scalers are fit on train only because they live inside the pipeline.
preprocess = ColumnTransformer([
    ("skewed", PowerTransformer(method="yeo-johnson"), ["income"]),
    ("scaled", StandardScaler(), ["age"]),
])

linear = Pipeline([("prep", preprocess), ("model", Ridge(alpha=1.0))])
linear.fit(X_train, y_train)
print("Ridge R2:", linear.score(X_test, y_test))

# Trees do not need scaling
trees = GradientBoostingRegressor(random_state=42).fit(X_train, y_train)
print("GBM R2:", trees.score(X_test, y_test))
```

---

## Summary

- Continuous = **measured** values in a range, with infinite precision in theory.
- **Scale** features for linear, distance-based and neural models. Trees do not need it.
- Fix **skew** with log / Yeo-Johnson, and tame outliers with clipping or robust scaling.
- Always fit transformations on the **training set only** to avoid [[Data Leakage]].
- Binning turns a continuous variable into a categorical one. See [[Discretization]].
