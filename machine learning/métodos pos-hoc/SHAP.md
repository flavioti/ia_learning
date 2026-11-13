---
aliases:
  - SHapley Additive exPlanations
  - Shapley values
  - SHAP values
---
#explainability #post-hoc #interpretability #model-explanation

# SHAP

**SHAP** (SHapley Additive exPlanations) is a [[post hoc method]] that measures the **exact contribution of each feature** to a prediction. It explains a trained model without changing it, for one prediction (**local**) or for the whole dataset (**global**).

>[!tip] SHAP splits a prediction into a **base value** (the average prediction) plus one **contribution per feature**. Positive contributions push the prediction up, and negative ones push it down.

It is based on **Shapley values** from cooperative game theory: the prediction is the "payout", the features are the "players", and each feature gets a fair share of the payout according to how much it adds when it joins every possible group of features.

## The idea

For a prediction $f(x)$ and a baseline $E[f(X)]$ (the average prediction), SHAP finds a value $\phi_i$ for each feature $i$ so that:

$$
f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i, \qquad \phi_0 = E[f(X)]
$$

The value of a feature is its **average marginal contribution** over all the possible orders in which the features could be added to the model:

$$
\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!\,(M-|S|-1)!}{M!}\Big[f_{S \cup \{i\}}(x) - f_S(x)\Big]
$$

Computing this exactly means looking at every subset of features, which grows exponentially. The SHAP library uses **fast algorithms for specific models** (trees, linear models) and **approximations** for the rest.

### Properties

Shapley values are the only attribution method that satisfies all of these:

| Property | Meaning |
|---|---|
| **Local accuracy (additivity)** | The base value plus all the contributions equals the model's prediction |
| **Missingness** | A feature that is absent contributes zero |
| **Consistency** | If a model changes so that a feature matters more, its SHAP value does not decrease |

## Reading a SHAP value

- **Base value:** the average model output. For a regression it is the mean prediction, and for a classifier like XGBoost it is usually in **log-odds**, not in probability.
- **SHAP value of a feature (for one row):** how much that feature moved the prediction away from the base value, in the **same unit as the model output**.
- **Sign:** positive raises the prediction, negative lowers it.
- **Size:** the larger the absolute value, the stronger the effect for that row.
- **Global importance:** the **mean of the absolute SHAP values** of a feature across many rows.

## Explainers

| Explainer | For | Notes |
|---|---|---|
| `TreeExplainer` | Tree models: [[XGBoost]], LightGBM, CatBoost, [[Random Forest]], scikit-learn trees and [[Gradient Boosting]] | **Fast and exact** for trees. The usual choice |
| `LinearExplainer` | Linear and logistic models ([[Logistic regression]]) | Exact. For independent features the value is the coefficient times the feature's distance from its mean |
| `DeepExplainer`, `GradientExplainer` | Neural networks | Faster approximations that use the network's gradients |
| `KernelExplainer` | **Any** model, treated as a black box | Model-agnostic but **slow**, because it samples many perturbed inputs. Use on a small sample |
| `PermutationExplainer`, `ExactExplainer` | Any model, small number of features | Sampling-based or exact |
| `shap.Explainer(model, data)` | Chooses an explainer automatically | The simplest entry point |

## Plots

| Plot | Scope | What it shows |
|---|---|---|
| **Waterfall** (`shap.plots.waterfall`) | One prediction | From the base value to the prediction, one bar per feature |
| **Force** (`shap.plots.force`) | One prediction | The same idea as a single stacked bar |
| **Bar** (`shap.plots.bar`) | Global | Mean absolute SHAP value per feature (importance) |
| **Beeswarm** (`shap.plots.beeswarm`) | Global | Every row as a dot: position is the SHAP value, color is the feature value. Shows importance **and** direction |
| **Scatter / dependence** (`shap.plots.scatter`) | One feature | SHAP value against the feature value, which reveals non-linear effects and interactions |

## Example

[[XGBoost]] regressor on the California housing data (the one used in [[House price]]): 20,640 districts, 8 features, target in units of $100,000. Trained on 80% of the data and explained on the other 20% (4,128 rows). Checked with `shap` 0.54 and `xgboost` 3.4 on CPU.

```python
import shap
import xgboost
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

X, y = fetch_california_housing(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = xgboost.XGBRegressor(n_estimators=600, learning_rate=0.05, max_depth=6,
                             subsample=0.8, colsample_bytree=0.8,
                             random_state=42, n_jobs=-1).fit(X_train, y_train)

explainer = shap.TreeExplainer(model)
sv = explainer(X_test)                      # an Explanation: .values, .base_values, .data

# Local accuracy: base value + sum of the contributions = the prediction
pred = model.predict(X_test)
assert abs((sv.base_values + sv.values.sum(axis=1)) - pred).max() < 1e-4

shap.plots.waterfall(sv[0])                 # one prediction
shap.plots.beeswarm(sv)                     # global view, with direction
shap.plots.bar(sv)                          # global importance
shap.plots.scatter(sv[:, "MedInc"])         # effect of one feature
```

Install with `pip install shap`. TreeSHAP on these 4,128 rows took about 1.4 seconds on CPU.

### One prediction (local)

The base value is **2.07** (the average prediction, about $207,000). For the first test district the model predicts **1.37**:

| Feature | Value | SHAP value |
|---|---|---|
| Longitude | -117.05 | **-0.974** |
| Latitude | 32.58 | **+0.632** |
| AveOccup | 4.18 | -0.381 |
| MedInc | 4.15 | +0.034 |
| HouseAge | 22 | -0.033 |
| AveRooms | 5.66 | +0.017 |
| AveBedrms | 1.08 | +0.003 |
| Population | 1551 | -0.002 |

Sum of the contributions: **-0.705**, and 2.07 - 0.705 = **1.37**, the prediction. The additivity check passed (the largest error over all rows was about $7 \times 10^{-6}$).

Here the location (longitude and latitude, which together describe where the district is) and a high occupancy per household explain almost all of the difference from the average, and income has almost no effect. Notice that longitude pushes the price **down** and latitude pushes it **up**: the two features describe the same thing (location), and the model splits the effect between them.

### The whole dataset (global)

Mean absolute SHAP value compared with XGBoost's built-in importance (the share of gain):

| Feature | Mean \|SHAP\| | Built-in importance |
|---|---|---|
| Latitude | **0.490** | 0.123 |
| Longitude | 0.406 | 0.148 |
| MedInc | 0.347 | **0.380** |
| AveOccup | 0.192 | 0.125 |
| AveRooms | 0.150 | 0.090 |
| HouseAge | 0.054 | 0.066 |
| AveBedrms | 0.026 | 0.043 |
| Population | 0.024 | 0.026 |

The two rankings **disagree**. The built-in importance says income is by far the most important feature. SHAP says that **latitude and longitude** are the strongest features, ahead of income. The reason is that location is encoded in two correlated features (their correlation here is -0.92), so the built-in gain is split between them, and each one looks smaller. SHAP measures the actual effect of each feature on the predictions, and shows that location, taken together, matters most. Never rely on a single importance number.

### Dependence on one feature

Average SHAP value of `MedInc` by income quintile:

| MedInc quintile | Average SHAP value |
|---|---|
| Lowest | -0.467 |
| 2 | -0.300 |
| 3 | -0.112 |
| 4 | +0.096 |
| Highest | +0.745 |

Higher income raises the predicted price, and the effect is stronger at the high end. This is the kind of non-linear shape that a linear model's single coefficient would miss, and that `shap.plots.scatter` shows directly.

## SHAP and other explanation methods

| Method | Scope | Notes |
|---|---|---|
| **SHAP** | Local and global | Consistent and additive, with strong theory. Can be slow for non-tree models |
| Built-in tree importance (gain, split count) | Global | Quick, but biased toward some features and unreliable with correlated ones (see the example) |
| Permutation importance | Global | Measures the drop in the score when a feature is shuffled. Model-agnostic and needs ground truth |
| **LIME** | Local | Fits a simple model around one prediction. Fast, but less stable and not additive |
| Partial dependence (PDP) and ICE | Global / local | Average and per-row effect of a feature on the prediction |
| Coefficients | Global | Only for linear models. SHAP gives the same idea for any model |

## Use cases

- **Explain individual decisions:** the main reasons behind a rejection in [[Credit approval]] or a high churn score in [[Churn]]. In regulated areas, the reasons must be clear and consistent.
- **Debug and validate a model:** find features with a suspicious effect, which often reveals [[Data Leakage]] (one feature dominating with a near-perfect score).
- **Feature selection and engineering:** find features with a near-zero SHAP value, or non-linear shapes that can be simplified.
- **Fairness checks:** see whether a sensitive feature, or a proxy for it, drives the predictions.
- **Monitoring:** compare the SHAP values or importances on live data with those in training, to detect [[Model drift]] and changes in what the model relies on.
- **Communicating with the business:** the waterfall plot is easy to explain.

## Limits and pitfalls

- **It explains the model, not the world.** A SHAP value shows what the model uses, not what **causes** the outcome. Do not read it as a causal effect.
- **Correlated features** share the credit in a way that can look odd (as with longitude and latitude above). Check how features relate, and consider reading grouped features together.
- **The reference (background) data matters.** The base value and the values depend on the baseline distribution. Choose it deliberately.
- **Units:** for classifiers the SHAP values are often in **log-odds**, not probability. Convert when explaining to the business.
- **Cost:** `KernelExplainer` and large datasets are slow. Use `TreeExplainer` when possible, and explain a sample.
- **Tree explainers have two modes:** by default they follow the tree paths, while the "interventional" mode uses a background dataset and breaks the dependence between features. They can give different values with correlated features.
- **Instability:** for small models or small samples the global ranking can change between runs and datasets.
- **A good explanation is not a good model.** An accurate explanation of a model that overfits still explains an overfitted model. See [[Overfitting]].
- **Do not use it with leaky features as proof of quality.** SHAP faithfully explains a leaking feature.
- **Privacy and security:** explanations can reveal information about the model and the data.

## Related

- [[post hoc method]]
- [[XGBoost]]
- [[Gradient Boosting]]
- [[Random Forest]]
- [[Logistic regression]]
- [[House price]]
- [[Credit approval]]
- [[Churn]]
- [[Data Leakage]]
- [[Model drift]]
