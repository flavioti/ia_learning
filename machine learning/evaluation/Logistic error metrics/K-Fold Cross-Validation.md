---
aliases:
  - K-Fold
  - k-fold CV
  - Cross-Validation
---
#supervised-learning #regression #classification #evaluation #model-selection

## Definition

**K-fold cross-validation** estimates how well a model will perform on new data. It splits the data into **k equal parts (folds)**, and repeats training k times. Each time, one fold is held out for validation and the other k−1 folds are used for training. The final result is the **average of the k scores**.

>[!tip] Every row is used for validation exactly once, and for training k−1 times.

It works for **both regression and classification**, and for any supervised model. Only the splitter and the metric change.

![[k-fold-cross-validation.png]]

## Why use it

| Problem with a single split | How k-fold helps |
|-----------------------------|------------------|
| The score depends on **which rows** landed in the test set | Averages over k different validation sets, so it is more stable |
| A test set wastes data that could train the model | Every row is used for both training and validation |
| You cannot tell whether a score is luck | The spread across folds shows the variability |
| Small datasets give a noisy estimate | Uses the data efficiently |

A single split is described in [[train dataset and test dataset]].

## Math notation

For $k$ folds, with $\text{score}_i$ the metric on the validation fold $i$:

$$
\text{CV score} = \frac{1}{k} \sum_{i=1}^{k} \text{score}_i
$$

$$
\text{Std} = \sqrt{\frac{1}{k-1} \sum_{i=1}^{k} \left( \text{score}_i - \text{CV score} \right)^2}
$$

Report the mean **and** the standard deviation. A small difference between two models that is smaller than the standard deviation is probably noise.

Each fold has about $n / k$ rows, so every iteration trains on a fraction $\frac{k-1}{k}$ of the data. For $k = 5$ that is 80% for training and 20% for validation.

## Procedure

1. **Shuffle** the data (unless the order matters, see time series below).
2. **Split** it into k folds.
3. For each fold $i$: train on the other k−1 folds, validate on fold $i$, and record the score.
4. **Average** the k scores and report the standard deviation.
5. Train the **final model on all the data** (or on all the training data), using the settings you selected. The k models trained during CV are not the final model.

## Choosing k

| k | Training size | Bias of the estimate | Variance | Cost |
|---|---------------|----------------------|----------|------|
| **5** | 80% | Slightly pessimistic | Moderate | Low |
| **10** | 90% | Smaller | Moderate | Medium |
| **n** (leave-one-out, LOOCV) | n − 1 rows | Smallest | High, and the folds are very correlated | Very high |
| **2 to 3** | 50 to 67% | Pessimistic (models see less data) | Moderate | Very low |

**5 or 10** are the usual defaults. They are a good balance between bias, variance and cost. With very small datasets, a larger k (or repeated k-fold) helps.

## Which splitter to use

| Situation | Splitter | Why |
|-----------|----------|-----|
| **Regression** | `KFold` | Plain random folds are fine |
| **Classification** | `StratifiedKFold` | Keeps the class proportions in every fold, which matters for imbalanced data |
| **Rows from the same entity** (several per customer, patient or session) | `GroupKFold` | Keeps a group in a single fold, which avoids [[Data Leakage]] between train and validation |
| **Time series** | `TimeSeriesSplit` | Training always comes **before** validation. Plain k-fold would use the future to predict the past |
| **Small data, more stable estimate** | `RepeatedKFold` / `RepeatedStratifiedKFold` | Repeats k-fold with different shuffles and averages them |
| **Very small data** | `LeaveOneOut` | Maximum training data, but expensive and noisy |

With `cross_val_score(model, X, y, cv=5)` and an integer `cv`, scikit-learn uses `StratifiedKFold` for classifiers and `KFold` for regressors. Note that `KFold` does **not shuffle by default**, so set `shuffle=True` (with a `random_state`) if the rows are ordered by time, class or source.

## Python

### Regression

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeRegressor

X, y = load_diabetes(return_X_y=True)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(
    DecisionTreeRegressor(max_depth=3, random_state=42), X, y,
    cv=kf, scoring="neg_root_mean_squared_error",
)
rmse = -scores                       # scikit-learn negates error metrics
print(rmse.round(1))                 # [59.6 61.  66.5 64.2 61.5]
print(rmse.mean(), rmse.std())       # about 62.6 and 2.5
```

### Classification (imbalanced)

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=1000, weights=[0.9, 0.1], random_state=42)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(
    DecisionTreeClassifier(max_depth=4, random_state=42), X, y,
    cv=skf, scoring="f1",
)
print(scores.round(3))               # [0.703 0.8   0.688 0.81  0.878]
print(scores.mean(), scores.std())   # about 0.776 and 0.071
```

With stratification, each fold in this dataset has 20 or 21 positive rows. With plain shuffled `KFold`, the folds hold between 18 and 24.

### Several metrics and the training score

```python
from sklearn.model_selection import cross_validate

res = cross_validate(
    DecisionTreeClassifier(max_depth=4, random_state=42), X, y, cv=skf,
    scoring=["precision", "recall", "f1"], return_train_score=True,
)
print(res["test_f1"].mean(), res["train_f1"].mean())   # about 0.776 vs 0.878
```

A large gap between the train and validation score signals [[Overfitting]].

### Avoiding leakage with a Pipeline

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
print(cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc").mean())   # about 0.90
```

The pipeline fits the scaler **inside each training fold**. If you scale the full dataset first, the validation fold has influenced the scaler, which is [[Data Leakage]].

## Cross-validation for tuning

`GridSearchCV` and `RandomizedSearchCV` use k-fold internally to compare hyperparameter settings. See the example in [[Decision Tree Regressor]].

>[!warning] The best score found by a search is **optimistic**, because you picked the maximum over many candidates using the same folds. To get an honest estimate, keep a final held-out test set, or use **nested cross-validation** (an inner CV loop for tuning inside an outer CV loop for evaluation).

```python
from sklearn.model_selection import GridSearchCV

inner = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    {"max_depth": [2, 3, 4, 6, 8]},
    cv=StratifiedKFold(3, shuffle=True, random_state=1), scoring="f1",
)
nested = cross_val_score(inner, X, y, cv=skf, scoring="f1")   # outer loop evaluates the whole tuning process
print(nested.mean())
```

## Metrics

Use the metric that matches the task:

| Task | Metrics |
|------|---------|
| Regression | [[RMSE - Root Mean Squared Error]], [[MAE - Mean Absolute Error]], [[R-squared]]. See [[Evaluating regression model metrics]] |
| Classification | [[F1-Score]], [[Precision]], [[Recall]], [[ROC-AUC]]. See [[Evaluating classification model metrics]] |

## Pitfalls

- **Preprocessing outside the folds:** scaling, imputing, encoding, feature selection or resampling (SMOTE) on the full data before splitting leaks information. Put them in a `Pipeline`.
- **Oversampling before the split:** duplicates of a minority row can land in both train and validation. Resample only inside the training folds.
- **Ignoring groups:** rows from the same customer in both train and validation inflate the score. Use `GroupKFold`.
- **Time series:** random folds leak the future. Use `TimeSeriesSplit`.
- **No shuffle on ordered data:** unshuffled folds can have very different distributions.
- **Reading one fold:** a single fold score is noisy. Look at the mean and the standard deviation.
- **Tuning on the final estimate:** do not report the CV score of the best hyperparameters as your performance. Use a held-out set or nested CV.
- **Cost:** the training cost is multiplied by k. For deep learning or very large data, use a single validation split instead.

## When to use it

✅ **Use when:**
- The dataset is small or medium, so a single split would be noisy
- You compare models or tune hyperparameters
- You want a measure of how stable the performance is

❌ **Avoid or adapt when:**
- Training is very expensive (large neural networks, LLMs). Use one validation split.
- The data is a time series (use `TimeSeriesSplit`) or grouped (use `GroupKFold`)
- The data is huge, because a single split is already stable

## Summary

- K-fold CV splits the data into k folds and rotates the validation fold, then **averages the k scores**.
- It applies to **regression and classification**: use `KFold` for regression and `StratifiedKFold` for classification.
- **k = 5 or 10** is the usual choice.
- Always **fit preprocessing inside the folds** with a `Pipeline` to avoid leakage.
- Report the **mean and standard deviation**, and keep a final test set when tuning.

## Related

- [[Model Evaluation]]
- [[train dataset and test dataset]]
- [[Overfitting]]
- [[Underfitting]]
- [[Data Leakage]]
- [[Decision Tree Regressor]]
- [[Decision Tree Classifier]]
- [[Evaluating regression model metrics]]
- [[Evaluating classification model metrics]]
