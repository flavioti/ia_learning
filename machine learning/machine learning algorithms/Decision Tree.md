---
aliases:
  - Decision Trees
  - CART
cover: decision-tree-regressor.png
---
#ml-model #supervised-learning #classification #regression #tree-based

## Definition

A **decision tree** is a [[Supervised Learning]] that predicts a target by learning a hierarchy of **if/else questions** on the features. It splits the data into smaller and smaller groups, and each final group (a **leaf**) outputs a prediction.

There are two flavors, which share the same algorithm but differ in the target, the impurity measure and the leaf prediction:

|                    | [[Decision Tree Classifier]]                         | [[Decision Tree Regressor]]                                                                 |
| ------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| scikit-learn class | `DecisionTreeClassifier`                             | `DecisionTreeRegressor`                                                                     |
| Target             | A class                                              | A number                                                                                    |
| Leaf prediction    | Majority class (or class proportions)                | **Mean of the target** (or median with `absolute_error`)                                    |
| Impurity           | [[Gini]], [[Entropy]]                                | [[MSE - Mean Squared Error\|MSE]], [[MAE - Mean Absolute Error\|Absolute Error]], Poisson   |
| Metrics            | [[Precision]], [[Recall]], [[F1-Score]], [[ROC-AUC]] | [[RMSE - Root Mean Squared Error\|RMSE]], [[MAE - Mean Absolute Error\|MAE]], [[R-squared]] |
| Typical use        | [[Credit approval]], [[Churn]], diagnosis            | [[House price]], ETA, demand                                                                |

>[!tip] Think of it as a flowchart that the algorithm writes for you from the data.

The most common training algorithm is **CART** (Classification And Regression Trees), which scikit-learn implements. It builds **binary** trees using greedy, recursive splitting.

## Anatomy

![[decision-tree-regressor.png|961]]

| Part | Meaning |
|------|---------|
| **Root node** | The first split, using all the training data |
| **Internal node** | A question on one feature, e.g. `area_m2 <= 121` |
| **Branch** | The outcome of the question (True / False) |
| **Leaf (terminal node)** | A final group that holds the prediction |
| **Depth** | Number of splits from the root to the deepest leaf |

## How it learns

At every node, CART:

1. Tries **every feature** and **every candidate threshold** (midpoints between sorted unique values).
2. Scores each split by how much it reduces **impurity** in the child nodes.
3. Picks the best split, divides the data, and **repeats recursively** on each child.
4. Stops when a stopping rule triggers: max depth, too few samples, no further gain, or a pure node.

This is **greedy**: each split is the best *locally*. There is no guarantee that the whole tree is globally optimal.

## Math notation

### Choosing a split

For a node with $N$ samples split into a left child ($N_L$ samples) and a right child ($N_R$ samples), the algorithm minimizes the weighted impurity of the children:

$$
J(\text{feature}, t) = \frac{N_L}{N}\, H(Q_L) + \frac{N_R}{N}\, H(Q_R)
$$

Where $H$ is the impurity measure and $t$ is the threshold. The **information gain** of a split is:

$$
\text{Gain} = H(Q) - \left( \frac{N_L}{N}\, H(Q_L) + \frac{N_R}{N}\, H(Q_R) \right)
$$

### Impurity measures

| Task | Impurity $H$ | Details and worked example |
|------|--------------|----------------------------|
| Classification | Gini $= 1 - \sum_k p_k^2$, Entropy $= -\sum_k p_k \log_2 p_k$ | [[Decision Tree Classifier]] |
| Regression | MSE $= \frac{1}{N} \sum_i (y_i - \bar{y})^2$ | [[Decision Tree Regressor]] |

A node is "pure" when impurity is 0 (every sample has the same class, or the same target value).

## Hyperparameters

The tree grows until it is told to stop. An unconstrained tree memorizes the training set (**overfitting**, see [[Overfitting]]), so these controls matter most:

| Hyperparameter | What it does | Effect of increasing it |
|----------------|--------------|--------------------------|
| `max_depth` | Maximum depth of the tree | More complex, higher variance |
| `min_samples_split` | Minimum samples needed to split a node | Simpler tree |
| `min_samples_leaf` | Minimum samples required in a leaf | Simpler, smoother predictions |
| `max_leaf_nodes` | Maximum number of leaves | Simpler tree |
| `max_features` | Number of features considered per split | More randomness, less variance when ensembled |
| `ccp_alpha` | Cost-complexity pruning strength | Simpler tree (prunes weak branches) |
| `criterion` | Impurity measure | Classification: `"gini"`, `"entropy"`, `"log_loss"`. Regression: `"squared_error"`, `"absolute_error"`, `"friedman_mse"`, `"poisson"` |
| `class_weight` | Reweights classes (classifier only) | Helps with imbalanced data |

## Pre-pruning vs. post-pruning

| | Pre-pruning (early stopping) | Post-pruning |
|---|---|---|
| Idea | Stop growing early | Grow a full tree, then remove weak branches |
| Controls | `max_depth`, `min_samples_leaf`, `max_leaf_nodes` | `ccp_alpha` (cost-complexity pruning) |
| Pros | Fast, simple | Often more accurate, since it can keep a late useful split |
| Cons | May stop before a useful split appears | Slower |

### Cost-complexity pruning in code

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, random_state=42, stratify=iris.target
)

full = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
path = full.cost_complexity_pruning_path(X_train, y_train)   # candidate alphas

for alpha in path.ccp_alphas:
    tree = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha).fit(X_train, y_train)
    print(f"alpha={alpha:.4f}  leaves={tree.get_n_leaves()}  test acc={tree.score(X_test, y_test):.3f}")
```

Sample output: `alpha=0.0000` gives 9 leaves, and `alpha=0.0227` gives 3 leaves with a similar test accuracy (about 0.92). A larger alpha prunes the tree down to a single node (accuracy 0.32). Choose alpha with **cross-validation**, since this test set is tiny (38 samples).

## Feature importance

A fitted tree exposes `feature_importances_`: the total impurity reduction contributed by each feature, normalized to sum to 1. It tells you which features the tree used most.

>[!warning] Impurity-based importance is biased towards high-cardinality and continuous features. For a more reliable view, use permutation importance on held-out data.

## Strengths and weaknesses

| ✅ Strengths | ❌ Weaknesses |
|-------------|---------------|
| Easy to explain and visualize | **Overfits** easily when deep |
| Handles non-linear relationships | **High variance**: small data changes can produce a very different tree |
| Captures feature interactions automatically | Predictions are piecewise **constant** (staircase), not smooth |
| No feature scaling needed | **Cannot extrapolate** beyond the training range |
| Works with numeric and categorical (encoded) features | Greedy splitting is not globally optimal |
| Fast to train and predict | Splits are axis-aligned, so diagonal boundaries need many splits |
| Robust to outliers in the features | Biased towards features with many split points |

## Preprocessing

| Topic                    | Guidance                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Scaling**              | Not needed. Splits depend on order, not scale                                                                                                                                                    |
| **Skewed features**      | Monotonic transforms (log) do not change the tree                                                                                                                                                |
| **Categorical features** | scikit-learn needs numeric input. Use ordinal or one-hot encoding. See [[Categorical columns]]. Recent versions can handle categorical features natively in some tree estimators. Check the docs |
| **Missing values**       | Supported natively in recent scikit-learn versions for the standard tree estimators. Check your version                                                                                          |
| **Class imbalance**      | Classifier only: use `class_weight="balanced"` and metrics beyond accuracy. See [[Decision Tree Classifier]]                                                                                     |
| **Skewed target**        | Regressor only: consider predicting `log1p(y)`. See [[Decision Tree Regressor]]                                                                                                                  |
| **Leakage**              | Fit any encoders or imputers on the training set only. See [[Data Leakage]]                                                                                                                      |

## Evaluating a tree

Always evaluate on **held-out data** (or with cross-validation), since training scores are misleading for trees.

| Task                                              | Metrics                                                                                                           |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [[Linear Regression]]       | [[RMSE - Root Mean Squared Error]], [[MAE - Mean Absolute Error]], [[R-squared]]                                  |
| [[Logistic regression]] | [[machine learning/quality/development/Accuracy\|Accuracy]], [[Precision]], [[Recall]], [[F1-Score]], [[ROC-AUC]] |

Compare the training and test score. A big gap signals overfitting, so reduce `max_depth` or raise `min_samples_leaf`. More detail: [[Evaluating regression model metrics]] and [[Evaluating classification model metrics]].

## Use cases

| Use case | Type | Why a tree fits |
|----------|------|-----------------|
| Credit scoring and loan approval | Classification | Auditable rules for regulators |
| Customer churn | Classification | Interpretable segments |
| Medical triage and diagnosis support | Classification | Transparent step-by-step logic |
| House price estimation | Regression | Non-linear effects and interactions (size, location) |
| Delivery time (ETA) and demand forecasting | Regression | Distinct regimes and abrupt changes |
| Exploratory analysis | Both | A shallow tree reveals key features and cutoffs |
| Building block for ensembles | Both | Base learner of Random Forest and Gradient Boosting |

More use cases per task: [[Decision Tree Classifier]] and [[Decision Tree Regressor]].

## Decision tree vs. other models

| Model                                     | Compared with a single tree                                                                                                                              |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [[Linear Regression\|Linear regression]]                     | Linear models extrapolate and are smooth, but need non-linear terms and interactions added by hand. Trees find them automatically but cannot extrapolate |
| [[Random Forest]]                         | Averages many trees trained on random subsets. Much lower variance and usually more accurate, but less interpretable                                     |
| [[Gradient Boosting]] (XGBoost, LightGBM) | Builds trees sequentially, each correcting the previous errors. Often the best on tabular data, but needs more tuning                                    |
| Neural networks                           | Better on images, text and audio. Trees usually win or tie on small to medium tabular data                                                               |

## When to use it

✅ **Use when:**
- You need a model whose decisions can be read and justified
- The data is tabular with non-linear effects or interactions
- You want a quick baseline with minimal preprocessing
- You want to explore which features and thresholds matter

❌ **Do not use alone when:**
- Predictive accuracy is the priority (use Random Forest or Gradient Boosting)
- The relationship is smooth or linear
- You must extrapolate beyond the training range
- The dataset is small and noisy, because the tree structure will be unstable

## Summary

- A tree predicts with a **learned hierarchy of if/else rules**; leaves hold a class or the mean of the target.
- Splits are chosen **greedily** to minimize impurity (Gini or entropy for classification, MSE for regression).
- Left unconstrained, it **overfits**. Control it with `max_depth`, `min_samples_leaf` and `ccp_alpha`.
- Its main values are **interpretability** and **zero scaling**. Its main weakness is **high variance**, which ensembles fix.

## Related

- [[Decision Tree Classifier]]
- [[Decision Tree Regressor]]
- [[Random Forest]]
- [[Gradient Boosting]]
- [[Overfitting]]
- [[Linear Regression|Linear regression]]
- [[Categorical columns]]
- [[Feature Engineering]]
- [[Data Leakage]]
