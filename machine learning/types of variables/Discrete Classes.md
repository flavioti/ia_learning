#classification #types-of-variables
# Discrete Classes

**Discrete classes** are the **separate, named outcomes** that a [[classification model]] chooses between: spam or not spam, cat or dog or bird, fraud or legit. Each example belongs to one class (or, in multilabel problems, to several).

Classes are the **categories of a target column**. They are not the same as a [[Discrete Variable]] (a numeric count): a class is a **label**, and its number, if it has one, is only an ID.

Related: [[Categorical columns]] · [[Discrete Variable]] · [[Continuous Variable]] · [[classification model]]

---

## Discrete classes vs. related terms

| Term | What it is | Example |
|---|---|---|
| **Discrete classes** | The possible values of a **classification target** | `spam`, `not spam` |
| **[[Categorical columns]]** | Any column that holds labels, as a feature **or** as a target | `country`, `membership tier` |
| **[[Discrete Variable]]** | A numeric **count** with gaps, where arithmetic is meaningful | `num_purchases = 4` |
| **[[Continuous Variable]]** | A numeric measurement that can take any value in a range (regression target) | `price = 19.99` |

When a categorical column is the thing you predict, its categories are the discrete classes. "Discrete" here only says that the output is one of a fixed set of options, in contrast to a continuous output.

---

## Types of class problems

| Type | Classes per example | Example | Output layer | Loss |
|---|---|---|---|---|
| **Binary** | 1 of 2 | Churn / no churn | Sigmoid | Binary crossentropy |
| **Multiclass** | 1 of N (N > 2) | Digit 0 to 9, iris species | Softmax | Categorical or sparse categorical crossentropy |
| **Multilabel** | Any subset of N | Tags on a photo (`beach`, `dog`) | One sigmoid per class | Binary crossentropy per class |
| **Ordinal** | 1 of N, with an **order** | Rating 1 to 5, low / medium / high | Depends: classification or ordinal regression | Crossentropy or an ordinal loss |

See [[Crossentropy]] for how the loss variants differ.

---

## Key characteristics

- A **finite set** of values, fixed before training
- **No arithmetic**: the mean of class IDs has no meaning
- **No order**, unless the classes are ordinal
- The model outputs **one probability per class**, and the probabilities sum to 1 (multiclass)
- The predicted class is usually the one with the highest probability, or the one above a decision threshold in the binary case

---

## How classes are encoded

Models cannot use text labels directly, so the classes are encoded as numbers. The encoding is a naming scheme, not a measurement.

| Format | Example for `[setosa, versicolor, virginica]` | Used with |
|---|---|---|
| **Text label** | `"versicolor"` | The raw data |
| **Integer (label encoding)** | `1` | Sparse categorical crossentropy, scikit-learn classifiers |
| **One-hot** | `[0, 1, 0]` | Categorical crossentropy |

Integer and one-hot encodings of the **same labels** give the **same loss**. Only the storage differs, and the integer form is smaller when there are many classes.

---

## Code example

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

iris = load_iris()
names = np.array(iris.target_names)[iris.target]   # 'setosa', 'versicolor', 'virginica'
print(np.unique(names, return_counts=True))        # 50 examples per class

# Encode the classes: integer ids and one-hot
le = LabelEncoder().fit(names)
y_int = le.transform(names)                        # 0, 1, 2
y_onehot = OneHotEncoder().fit_transform(y_int.reshape(-1, 1)).toarray()
print(le.classes_)                                 # ['setosa' 'versicolor' 'virginica']
print(y_onehot[0], y_onehot[-1])                   # [1. 0. 0.] [0. 0. 1.]

# A classifier returns one probability per class
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, names, test_size=0.3, stratify=names, random_state=0
)
clf = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print(clf.classes_)                                # the class order used by predict_proba
proba = clf.predict_proba(X_test[:2])
print(proba.sum(axis=1))                           # [1. 1.]
print(clf.predict(X_test[:2]))                     # the class with the highest probability
```

---

## Common pitfalls

### 1. Treating class IDs as numbers

If `bird = 2` and `dog = 1`, a regression model or a distance-based model reads "bird is twice dog", which is meaningless. Use a classifier, or one-hot encode the class when it is a **feature**. See [[Categorical columns]].

### 2. Class imbalance

When one class is rare (fraud at 5%), a model can score high accuracy by always predicting the majority class. Check [[Recall]], [[Precision]] and [[F1-Score]] instead of [[Accuracy]]. Options:

- **Stratified splits** (`stratify=y`) to keep the class ratio in train and test
- **Class weights** (`class_weight="balanced"`), so rare-class mistakes cost more
- **Resampling**, or a different decision threshold

With a 5% positive class, `LogisticRegression` reached a recall of about 0.64 on the rare class by default and about 0.93 with `class_weight="balanced"`. Higher recall usually costs some precision, so check both.

### 3. Treating ordinal classes as nominal

Ratings and sizes have an order. One-hot encoding throws it away. Ordinal encoding keeps it, but it assumes the gaps are equal, which is not always true.

### 4. Too many classes

A target with thousands of classes (a user ID, a product SKU) is hard to learn. Consider embeddings, hierarchical classes, or a ranking formulation instead.

### 5. Class order mismatch

`predict_proba` columns follow `clf.classes_`, not the order in your data. Always map probabilities to class names through `classes_`.

---

## Evaluation

Classes are evaluated with the metrics derived from the [[Confusion Matrix]]. See [[Evaluating classification model metrics]]. For multiclass problems, per-class metrics are combined with a `macro`, `micro` or `weighted` average.

---

## Summary

- Discrete classes are the **named outcomes** of a classification target.
- They are **labels**, not quantities: no arithmetic, and no order unless ordinal.
- They are the categories of a categorical column that you predict.
- The numbers used to encode them are IDs. Integer and one-hot encodings carry the same information.
- Watch for **class imbalance**, and evaluate with precision, recall and F1.
