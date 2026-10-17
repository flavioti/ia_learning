**Feature engineering** is the process of turning ==raw data== into ==input variables== (features) that help a machine learning model learn better. It combines domain knowledge, statistics and transformations to expose the patterns that matter.

>[!tip] Model quality often depends more on the features than on the choice of algorithm.

---

## Main Activities

| Activity | What it does | Example |
|---|---|---|
| **Cleaning / imputation** | Handles missing values and outliers | Fill missing age with the median |
| **Encoding categoricals** | Converts categories to numbers | One-hot, ordinal, target encoding (see [[Categorical columns]]) |
| **Scaling / normalization** | Puts numeric features on comparable ranges | Standardization (z-score), min-max |
| **Transformation** | Reshapes skewed distributions | Log, square root, Box-Cox |
| **Binning / discretization** | Groups continuous values into intervals (see [[Discretization]]) | Age → age brackets |
| **Feature creation** | Derives new variables from existing ones | `price / area`, ratios, interactions, polynomial terms |
| **Temporal features** | Extracts structure from timestamps | Day of week, hour, lags, rolling averages |
| **Text / image features** | Converts unstructured data to vectors | TF-IDF, [[embeddings]] |
| **Feature selection** | Removes irrelevant or redundant features | Correlation filters, mutual information, L1 regularization, tree importance |
| **Dimensionality reduction** | Compresses features while keeping information | PCA |

---

## Why It Matters

- Makes patterns easier for the model to find (a ratio can be more predictive than its two raw parts).
- Lets models consume data types they cannot read directly, such as text and categories.
- Reduces [[Overfitting]] and training cost by dropping noise.
- Many algorithms are sensitive to feature scale (linear models, SVM, k-NN, neural nets), while tree-based models mostly are not.

---

## Pitfalls

- **[[Data Leakage]]:** Do not compute statistics (mean for scaling or imputation, target encodings) on the full dataset. Fit them on the training split only, then apply them to validation and test data. See [[train dataset and test dataset]].
- **[[Training-Serving Skew]]:** The exact same transformations must run at training and inference time. This is why pipelines and feature stores are used (see [[Offline Feature Store]] and [[Online Feature Store]]).
- **Over-engineering:** Too many derived features add noise and complexity.
- **Distribution drift:** Feature distributions change over time; monitor them (see [[Population Stability Index (PSI)]]).

---

## Example (scikit-learn)

A pipeline keeps transformations fitted on training data only, which avoids [[Data Leakage|leakage]] and [[Training-Serving Skew|skew]].

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("data.csv")

# Feature creation
df["price_per_m2"] = df["price"] / df["area"]
df["day_of_week"] = pd.to_datetime(df["created_at"]).dt.dayofweek

numeric = ["price", "area", "price_per_m2"]
categorical = ["city", "day_of_week"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), categorical),
])

model = Pipeline([
    ("features", preprocess),
    ("clf", RandomForestClassifier(random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(
    df.drop(columns="target"), df["target"], test_size=0.2, random_state=42
)

model.fit(X_train, y_train)   # transformers are fitted on training data only
print(model.score(X_test, y_test))
```

---

## Relation to Deep Learning

Deep learning performs much of this automatically through *representation learning*, so manual feature engineering matters less for images, text and audio. For tabular data, it is still very important.
