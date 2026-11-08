#framework #machine-learning
# scikit-learn

>[!tip] An open-source Python library for **classical machine learning**: classification, regression, clustering, dimensionality reduction, preprocessing and model evaluation.

It is built on [[Numpy]] and works best on **tabular data** that fits in memory. It is the standard tool for baselines and for computing the metrics in this vault. It is **not** a deep learning library: for [[neural networks]] use [[PyTorch]] or [[Keras and TensorFlow]].

## Core API

Every object follows the same small interface, so models are easy to swap.

| Concept | Methods | What it is |
|---------|---------|------------|
| **Estimator** | `fit(X, y)` | Anything that learns from data (a model or a transformer) |
| **Predictor** | `predict(X)`, `predict_proba(X)`, `score(X, y)` | An estimator that makes predictions, such as `RandomForestClassifier` |
| **Transformer** | `fit(X)`, `transform(X)`, `fit_transform(X)` | Changes the data, such as `StandardScaler` or `OneHotEncoder` |
| **Pipeline** | `make_pipeline(...)` | Chains transformers and a final model into one estimator |
| **Model selection** | `train_test_split`, `cross_val_score`, `GridSearchCV` | Splitting data, cross-validation and hyperparameter search |
| **Metrics** | `sklearn.metrics` | Scores that compare predictions with the truth |

>[!warning] Fit transformers on the **training data only**. Fitting a scaler on the full dataset leaks information from the test set. A `Pipeline` avoids this mistake, because it fits each step on the training fold only, including inside cross-validation.

## Minimal example

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

# 1. Data: imbalanced binary classification (about 10% positives)
X, y = make_classification(n_samples=2000, n_features=10, weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 2. Pipeline: preprocessing + model, fitted together
model = make_pipeline(StandardScaler(), RandomForestClassifier(random_state=42))
model.fit(X_train, y_train)

# 3. Predict and evaluate on held-out data
y_pred = model.predict(X_test)
print(accuracy_score(y_test, y_pred))   # 0.945
print(f1_score(y_test, y_pred))         # 0.703
print(classification_report(y_test, y_pred))

# 4. Cross-validation on the training set
scores = cross_val_score(model, X_train, y_train, cv=5, scoring="f1")
print(scores.mean(), scores.std())      # about 0.74 +/- 0.03
```

Accuracy is 94.5%, but the F1-Score on the rare class is only 0.70, which shows why [[Accuracy]] alone misleads on imbalanced data. See [[Evaluation classification model metrics]].

## Metrics in `sklearn.metrics`

| Task | Function | Note |
|------|----------|------|
| Classification | `accuracy_score` | [[Accuracy]] |
| | `precision_score`, `recall_score` | [[Precision]], [[Recall]] |
| | `f1_score` | [[F1-Score]] |
| | `confusion_matrix` | [[Confusion Matrix]] |
| | `roc_auc_score` | [[ROC-AUC]], needs probabilities |
| | `average_precision_score` | Estimate of [[PR-AUC]] |
| | `log_loss` | [[Crossentropy]] on predicted probabilities |
| Regression | `mean_absolute_error` | [[MAE - Mean Absolute Error]] |
| | `mean_squared_error` | [[MSE - Mean Squared Error]] |
| | `r2_score` | [[R-squared]] |
| Similarity | `cosine_similarity` (in `sklearn.metrics.pairwise`) | [[Cosine similarity]] |

See also [[Evaluating regression model metrics]].

## Common algorithms

| Family | Examples |
|--------|----------|
| Linear models | `LinearRegression`, `LogisticRegression`, `Ridge`, `Lasso` |
| Trees and ensembles | [[Decision Tree Classifier]], [[Random Forest]], [[Gradient Boosting]] (`GradientBoostingClassifier`, `HistGradientBoostingClassifier`) |
| Other supervised | `SVC`, `KNeighborsClassifier`, `GaussianNB` |
| Clustering | `KMeans`, `DBSCAN` |
| Dimensionality reduction | `PCA`, `TruncatedSVD` |
| Preprocessing | `StandardScaler`, `OneHotEncoder`, `SimpleImputer` (see [[Feature Engineering]]) |

## Installing

```bash
pip install scikit-learn
```

It runs on **CPU only** and has no GPU requirement. Install it in a virtual environment (for example `.venv`).

## scikit-learn vs. deep learning frameworks

| | scikit-learn | PyTorch | Keras / TensorFlow |
|---|--------------|---------|--------------------|
| Focus | Classical ML | Deep learning | Deep learning |
| Data | Tabular, fits in memory | Any (images, text, audio) | Any (images, text, audio) |
| GPU | No | Yes (CUDA) | Yes (CUDA) |
| Training | `fit()` | Write the training loop | `compile()` + `fit()` |
| Best for | Baselines, tabular data, evaluation | Research, LLMs | Fast prototyping, production serving |

## Related

- [[Numpy]]
- [[Model Evaluation]]
- [[K-Fold Cross-Validation]]
- [[Overfitting]]
- [[PyTorch]]
- [[Keras and TensorFlow]]
- [[MLFlow]]
