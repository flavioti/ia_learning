---
aliases:
  - DecisionTreeClassifier
  - Classification Tree
---
#ml-model #supervised-learning #classification #tree-based

## Definition

A **classification tree** is a [[Decision Tree]] that predicts a **class label**. It splits the data into groups that are as **pure** as possible (mostly one class), and each leaf predicts the **majority class** of its training samples. In scikit-learn it is `DecisionTreeClassifier`.

>[!tip] Think of it as a flowchart of yes/no questions that ends in a class.

Shared concepts (anatomy, greedy splitting, pruning, feature importance, strengths and weaknesses) are in [[Decision Tree]]. This note covers what is specific to classification. See also the [[classification model]] note and the problem type [[Logistic regression (Classification problems)]].

## Leaf prediction

| Output | How |
|--------|-----|
| `predict` | The **majority class** in the leaf |
| `predict_proba` | The **class proportions** in the leaf, e.g. 8 of 10 samples are class A, so P(A) = 0.8 |

## Math notation

The split criterion is the **impurity** of the class distribution in a node. With $p_k$ the proportion of class $k$ in the node:

$$
\text{Gini} = 1 - \sum_{k} p_k^2
\qquad\qquad
\text{Entropy} = -\sum_{k} p_k \log_2 p_k
$$

Both are 0 for a pure node and largest when the classes are evenly mixed. The algorithm picks the split with the highest **information gain**:

$$
\text{Gain} = H(Q) - \left( \frac{N_L}{N}\, H(Q_L) + \frac{N_R}{N}\, H(Q_R) \right)
$$

Where $H$ is Gini or entropy, $N$ is the number of samples in the node, and $N_L$, $N_R$ are the samples in the left and right children.

### Criteria

| `criterion` | Impurity | Notes |
|-------------|----------|-------|
| `"gini"` (default) | Gini impurity | Fast, a good default |
| `"entropy"` | Shannon entropy | Slightly slower, usually gives very similar trees |
| `"log_loss"` | Log loss (equivalent to entropy here) | Same splits as `"entropy"` |

## Worked example (Gini)

Loan default data: 10 customers, 6 repaid and 4 defaulted.

$$
\text{Gini}_{\text{parent}} = 1 - 0.6^2 - 0.4^2 = 0.48
$$

Candidate split `income < 50k`:

| Child | Repaid | Defaulted | Gini |
|-------|--------|-----------|------|
| Left (income < 50k), 5 samples | 1 | 4 | $1 - 0.2^2 - 0.8^2 = 0.32$ |
| Right (income ≥ 50k), 5 samples | 5 | 0 | $0$ (pure) |

$$
\text{Weighted Gini} = \tfrac{5}{10}(0.32) + \tfrac{5}{10}(0) = 0.16
\qquad
\text{Gain} = 0.48 - 0.16 = 0.32
$$

The algorithm compares this gain against every other feature and threshold and keeps the best one.

### The same split with entropy

$$
H_{\text{parent}} = 0.971
\qquad
H_{\text{left}} = 0.722
\qquad
H_{\text{right}} = 0
\qquad
\text{Gain} = 0.971 - \tfrac{5}{10}(0.722) = 0.610
$$

The numbers differ from Gini, but both criteria rank this split the same way.

## Classification-specific issues

| Issue | What happens | What to do |
|-------|--------------|------------|
| **Class imbalance** | A rare class barely affects the impurity, so the tree ignores it | `class_weight="balanced"`, resampling, and metrics beyond accuracy |
| **Poor probabilities** | A fully grown tree has pure leaves, so `predict_proba` returns only 0 and 1. Shallow trees give coarse probabilities | Limit depth, use `min_samples_leaf`, or calibrate (isotonic or Platt) |
| **Axis-aligned boundaries** | A diagonal class boundary needs many splits | Add combined features, or use another model |
| **Threshold choice** | `predict` uses an implicit 0.5 probability cutoff | Tune the threshold on `predict_proba` for your cost of FP vs. FN |
| **Multiclass** | Handled natively, with no one-vs-rest needed | Use macro-averaged metrics if rare classes matter |

### Class imbalance example

Synthetic data with about 8% positives, a tree with `max_depth=4`:

| `class_weight` | Recall on the positive class |
|----------------|------------------------------|
| `None` | 0.46 |
| `"balanced"` | 0.85 |

Balancing trades some precision for a much higher recall. Re-check both on held-out data.

## Hyperparameters

Complexity controls are shared with every tree, see [[Decision Tree]]. For classification, these also matter:

| Hyperparameter | Effect for classification |
|----------------|---------------------------|
| `class_weight` | Weights classes in the impurity, which helps with imbalance |
| `criterion` | Gini, entropy or log loss, see above |
| `min_samples_leaf` | Larger leaves give smoother, more reliable probabilities |
| `max_depth` | Shallower trees give simpler rules and coarser probabilities |

## Python

### Fitting and reading the rules

```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, random_state=42, stratify=iris.target
)

clf = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)
print("accuracy:", clf.score(X_test, y_test))

# The learned rules as text
print(export_text(clf, feature_names=list(iris.feature_names)))
print(dict(zip(iris.feature_names, clf.feature_importances_.round(3))))
```

Sample output: the first rule splits on `petal length <= 2.45` (separating class 0 from the others), and `petal length` carries about 95% of the importance.

### Probabilities

```python
print(clf.predict_proba(X_test[:3]))      # class proportions in the leaf of each sample
```

On this depth-3 tree, the first three test samples all land in pure leaves, so the probabilities come out as exactly 1.0 and 0.0. A fully grown tree returns only 0 and 1 for every test sample. To get useful probabilities, tune `min_samples_leaf`, or calibrate the model.

### Class weights

```python
clf = DecisionTreeClassifier(
    max_depth=4, min_samples_leaf=10, class_weight="balanced", random_state=0
)
```

## Evaluating a classification tree

Evaluate on **held-out data**, and watch the gap between the training and test score.

| Metric | Use |
|--------|-----|
| [[machine learning/quality/development/Accuracy\|Accuracy]] | Balanced classes only |
| [[Precision]] | When false alarms are costly |
| [[Recall]] | When misses are costly |
| [[F1-Score]] | A balance of precision and recall on imbalanced data |
| [[ROC-AUC]] and [[PR-AUC]] | Ranking quality, from `predict_proba` |
| [[Confusion Matrix]] | The full breakdown of errors |

See [[Evaluation classification model metrics]] for the full comparison.

## Use cases

| Use case | Why a classification tree fits |
|----------|--------------------------------|
| Credit scoring and loan approval | Auditable rules for regulators |
| Customer churn | Interpretable segments |
| Medical triage and diagnosis support | Transparent step-by-step logic |
| Fraud screening rules | Readable thresholds that analysts can review |
| Customer segmentation by behavior | Rules map directly to business actions |
| Quality control (pass or fail) | Simple criteria on measurements |

## When to use it

✅ **Use when:**
- You need decisions that can be read and justified
- The data is tabular, with non-linear effects or interactions
- You want a quick baseline with little preprocessing

❌ **Do not use alone when:**
- You need the best accuracy (use [[Random Forest]] or [[Gradient Boosting]])
- You need well-calibrated probabilities
- The classes are heavily imbalanced and you do not adjust for it
- The dataset is small and noisy, because the tree will be unstable

## Related

- [[Decision Tree]]
- [[Decision Tree Regressor]]
- [[Random Forest]]
- [[Gradient Boosting]]
- [[classification model]]
- [[Logistic regression (Classification problems)]]
- [[Evaluation classification model metrics]]
- [[Categorical columns]]
