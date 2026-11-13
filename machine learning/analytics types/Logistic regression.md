---
aliases:
  - LogisticRegression
  - Classification-problems
  - classic-ml
tags:
  - classic-ml
---
#ml-model #supervised-learning #classification #linear-model

[[Evaluating classification model metrics]]
## Logistic regression

It predicts a probability for a ==🟠category== (e.g. spam / not spam, churn / no churn) by passing a linear combination of features through a sigmoid function, so the output falls between ==🟡0 and 1==.

Despite the name, it is a **classification** model, not a regression one. It is the standard [[baseline]] for classification on tabular data: fast, stable, well calibrated and easy to explain. In scikit-learn it is `LogisticRegression`.

>[!tip] Think of it as a linear regression whose output is squeezed into a probability. The straight line works on the **log-odds** scale, and the sigmoid converts it back to a probability.

| Algorithm                                                              | Task           | Notes                                                                      | Used in                             |
| ---------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------- | ----------------------------------- |
| [[Logistic regression\|Logistic regression]] | Classification | Predicts a probability. Explainable, well calibrated and a strong baseline | Credit approval, Credit Risk, Churn |
|                                                                        |                |                                                                            |                                     |
## How it works

1. Compute a linear score from the features: $z = b_0 + b_1 x_1 + \dots + b_n x_n$
2. Turn it into a probability with the **sigmoid** (logistic) function:

$$
P(y=1 \mid x) = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

3. Turn the probability into a class with a **threshold** (0.5 by default): predict 1 if $P \ge$ threshold.

The sigmoid maps any number to (0, 1): a large positive $z$ gives a probability near 1, a large negative $z$ near 0, and $z = 0$ gives exactly 0.5.

### Odds and log-odds

The model is linear in the **log-odds** (also called the *logit*):

$$
\ln\frac{P}{1-P} = b_0 + b_1 x_1 + \dots + b_n x_n
$$

| Term | Meaning | Example (P = 0.8) |
|---|---|---|
| Probability | Chance of the positive class | 0.8 |
| Odds | $P / (1-P)$ | 4 (4 to 1) |
| Log-odds | $\ln(\text{odds})$ | 1.39 |

### Reading the coefficients

- The sign of $b_i$ shows the direction: positive raises the probability of class 1, negative lowers it.
- $e^{b_i}$ is the **odds ratio**: how much the odds are multiplied when $x_i$ rises by one unit, holding the others fixed. For example, $b = 0.65$ gives $e^{0.65} \approx 1.9$, so the odds almost double.
- The effect on the **probability** is not constant: the same change in $x_i$ moves the probability more near 0.5 than near 0 or 1.
- To compare coefficients between features, **standardize** the features first, so each coefficient is "per one standard deviation".

## Training

The coefficients are found by minimizing the **log loss** (binary cross-entropy), which is the negative log-likelihood of the data. See [[Crossentropy]].

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\Big[y_i \ln p_i + (1-y_i)\ln(1-p_i)\Big]
$$

- There is **no closed-form solution** as in linear regression, so an iterative solver is used (`lbfgs` by default in scikit-learn).
- The loss is **convex**, so there is one global minimum and no bad local minima.
- A confident wrong prediction is punished heavily, which pushes the model to produce honest probabilities.

## Regularization

scikit-learn applies an **L2** penalty by default. The parameter `C` is the **inverse** of the regularization strength: a **smaller C means a stronger penalty**.

| Penalty | Effect |
|---|---|
| **L2** (Ridge, default) | Shrinks all coefficients. Keeps every feature. Helps with correlated features |
| **L1** (Lasso) | Sets some coefficients to exactly zero, so it also selects features |
| **Elastic net** | A mix of L1 and L2 |

See [[Ridge and Lasso Regression]] for the same idea in linear regression. Regularization fights [[Overfitting]], which matters when there are many features or few rows.

>[!warning] **scikit-learn 1.8 deprecated the `penalty` parameter.** Leave it at the default for L2, and use `l1_ratio` instead: `l1_ratio=1` for L1 (needs `solver="saga"`), a value between 0 and 1 for elastic net. `penalty` will be removed in version 1.10.

## Feature preparation

- **Scale the features** (for example `StandardScaler`). The solver converges much faster and the L1/L2 penalty treats all features fairly. Without scaling, features with large units dominate the penalty.
- **Encode categories** (one-hot). See [[Categorical columns]].
- **Add non-linear terms by hand** (squares, interactions, bins) if the relationship is not linear. The model itself only draws a **linear boundary**. See [[Discretization]] for binning, as in a credit scorecard.
- **Correlated features** make the coefficients unstable and hard to interpret, although predictions stay fine. Regularization helps.
- Fit the scaler on the training data only, and apply it unchanged to new data. See [[Data Leakage]].

## Example

Binary classification on the public breast cancer dataset from scikit-learn: 569 samples, 30 numeric features, and the class `1` = benign (63%) versus `0` = malignant (37%). Metrics from 5-fold stratified cross-validation on a 70% training split.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
cv = StratifiedKFold(5, shuffle=True, random_state=42)

models = {
    "No scaling":       LogisticRegression(max_iter=5000),
    "Scaled, C=1":      make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Scaled, C=0.01":   make_pipeline(StandardScaler(), LogisticRegression(C=0.01, max_iter=1000)),
    "Scaled, C=100":    make_pipeline(StandardScaler(), LogisticRegression(C=100, max_iter=1000)),
    "Scaled, L1":       make_pipeline(StandardScaler(),
                                      LogisticRegression(l1_ratio=1, solver="saga", C=0.1, max_iter=5000)),
}
for name, model in models.items():
    res = cross_validate(model, X_train, y_train, cv=cv,
                         scoring=["roc_auc", "accuracy", "neg_log_loss"])
    print(name, res["test_roc_auc"].mean(), res["test_accuracy"].mean(), -res["test_neg_log_loss"].mean())
```

| Model | ROC-AUC | Accuracy | Log loss | Non-zero coefficients |
|---|---|---|---|---|
| No scaling | 0.991 | 0.952 | 0.125 | 30 (2,021 solver iterations) |
| **Scaled, C=1 (default)** | 0.993 | **0.982** | **0.079** | 30 (19 iterations) |
| Scaled, C=0.01 (too strong) | 0.993 | 0.955 | 0.194 | 30 |
| Scaled, C=100 (too weak) | 0.987 | 0.967 | 0.191 | 30 |
| Scaled, L1 (C=0.1) | 0.994 | 0.962 | 0.140 | **6** |

What the results show:

- **Scaling matters:** the same model needs about 2,000 solver iterations without it and 19 with it, and it scores better.
- **The middle value of `C` wins.** Too strong a penalty underfits (accuracy drops to 0.955), too weak a penalty overfits (log loss rises to 0.191). Tune `C` by cross-validation, for example with `LogisticRegressionCV`.
- **L1 keeps almost the same ranking (AUC 0.994) with only 6 of 30 features**, which gives a much simpler model, at the cost of some accuracy and log loss here.
- The default model reaches an AUC of 0.998 on the held-out test set. This is an easy dataset, so do not expect such numbers on noisy business data.

### Odds ratios of the scaled model

Each value is the factor applied to the odds of *benign* when the feature rises by **one standard deviation**:

| Feature | Coefficient | Odds ratio | Reading |
|---|---|---|---|
| worst texture | -1.23 | 0.29 | Strongest push toward malignant |
| worst concave points | -1.00 | 0.37 | Pushes toward malignant |
| worst area | -0.95 | 0.38 | Pushes toward malignant |
| mean compactness | 0.65 | 1.92 | Pushes toward benign, although it is correlated with the features above |

The positive sign of *mean compactness* looks odd, because the other size and shape features push the other way. This is a typical effect of **correlated features**: the coefficient of one feature is only meaningful given the others. Do not read single coefficients as isolated causes when features are correlated.

### Threshold changes the error type

The default threshold of 0.5 is not sacred. The test set has 171 samples (107 benign, 64 malignant), and the positive class is *benign*. Raising the threshold makes the model call fewer cases benign:

| Threshold | Malignant missed (predicted benign) | Benign flagged as malignant | Precision (benign) | Recall (benign) |
|---|---|---|---|---|
| 0.5 | 1 | 1 | 0.991 | 0.991 |
| 0.9 | 0 | 16 | 1.000 | 0.850 |
| 0.1 | 9 | 0 | 0.922 | 1.000 |

A **high** threshold (0.9) never calls a malignant case benign, but sends 16 benign cases to further checks. A **low** threshold (0.1) does the opposite: no benign case is flagged, but 9 malignant cases are missed. In a medical setting a **missed malignant case** is the costly mistake, so you would choose the high threshold and accept more false alarms. In credit or churn, choose the threshold from the **business cost**, not 0.5. See [[Confusion Matrix]], [[Precision]] and [[Recall]].

## Multiclass

For more than two classes, scikit-learn fits a **multinomial** (softmax) logistic regression by default: one score per class, converted to probabilities that sum to 1. The alternative is **one-vs-rest**, with one binary model per class.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Fast to train and predict, works on large data | Linear decision boundary: misses non-linear effects and interactions unless engineered |
| **Interpretable** coefficients and odds ratios | Coefficients are unstable with correlated features |
| Outputs **well-calibrated probabilities** (without class rebalancing) | Sensitive to outliers and to unscaled features |
| Convex loss: one stable solution | Usually less accurate than [[Gradient Boosting]] when there are strong interactions |
| Few hyperparameters, little tuning | Struggles with images, text embeddings and other raw unstructured inputs |
| Strong, regulator-friendly [[baseline]] | Perfectly separable classes make the coefficients grow without limit unless regularized |

## Class imbalance

When one class is rare, accuracy is misleading. Use [[ROC-AUC]], [[PR-AUC]] and a cost-based threshold. `class_weight="balanced"` can raise recall of the rare class, but it **distorts the probabilities**: in the [[Churn]] example it left the ranking unchanged and more than doubled the Brier score. Use it only if you do not need real probabilities, or recalibrate afterwards.

## Evaluation

Accuracy, [[Precision]], [[Recall]], [[F1-Score]], [[ROC-AUC]] and the [[Confusion Matrix]], plus calibration and log loss when the probabilities are used. See [[Evaluating classification model metrics]].

## Used in

- [[Credit Risk]]: the **scorecard**, a logistic regression on WoE-binned features
- [[Credit approval]]: baseline versus [[Gradient Boosting]]
- [[Churn]]: baseline that matches or beats boosting on a mostly linear signal

## Pitfalls

- Forgetting to **scale** the features, which slows the solver and makes the penalty unfair
- Reading a coefficient as a probability change: it is a **log-odds** change
- Interpreting coefficients of **correlated** features one by one
- Using the default 0.5 threshold when the costs of the two errors differ
- Using `class_weight="balanced"` and then trusting the probabilities
- Assuming a linear boundary is enough, without checking interactions or comparing against a tree ensemble
- Fitting the scaler or the bins on all the data instead of the training data only (leakage)
- Using the deprecated `penalty` parameter in new scikit-learn versions

# Models
[[Decision Tree Classifier|DecisionTreeClassifier]]
[[Evaluating classification model metrics]]
