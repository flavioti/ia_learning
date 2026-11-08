---
aliases:
  - ML Algorithms
---
# Machine Learning Algorithms

Index of the algorithms covered in the vault, grouped by family. Each algorithm has its own note. Where an algorithm is explained inside a use case, it is listed under "Used in".

## Linear models

| Algorithm | Task | Notes | Used in |
|---|---|---|---|
| [[Linear Regression (regression problems)\|Linear regression]] | Regression | The simplest baseline: a weighted sum of the features | [[House price]] |
| [[Ridge and Lasso Regression]] | Regression | Linear regression with a penalty on the coefficients. Ridge (`Ridge`), Lasso (`Lasso`), Elastic Net (`ElasticNet`) | [[House price]], [[Used-car price]] |
| [[Logistic regression (Classification problems)\|Logistic regression]] | Classification | Predicts a probability. Explainable, well calibrated and a strong baseline | [[Credit approval]], [[Credit Risk]], [[Churn]] |

## Tree-based models

| Algorithm | Task | Notes | Used in |
|---|---|---|---|
| [[Decision Tree]] | Both | The shared concepts: splits, pruning, feature importance | |
| [[Decision Tree Classifier]] | Classification | Readable rules, but unstable on its own | [[Credit approval]] |
| [[Decision Tree Regressor]] (`DecisionTreeRegressor`) | Regression | Piecewise-constant predictions | [[House price]] |
| [[Random Forest]] | Both | Many trees averaged, so it is more stable than one tree | |
| [[Random Forest Regressor]] (`RandomForestRegressor`) | Regression | A strong default with little tuning | [[House price]] |
| [[Gradient Boosting]] | Both | Trees built one after another, each correcting the previous errors. Often the most accurate on tabular data | [[House price]], [[Churn]] |
| [[XGBoost]] | Both | An optimized, regularized gradient boosting library with native missing values and early stopping | [[House price]], [[Used-car price]], [[Fraud detection]] |

## Time series

| Algorithm              | Task        | Notes                                                                                                         |
| ---------------------- | ----------- | ------------------------------------------------------------------------------------------------------------- |
| [[ARIMA]]              | Forecasting | A classic statistical model that uses the series' own past values and errors. See [[Time series forecasting]] |
| [[Google TimesFM 3.0]] | Forecasting |                                                                                                               |

## Applied models

| Note                     | What it covers                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| [[Business ML models]]   | Business problems solved with ML: [[Churn]], [[Credit Risk]], [[fraud detection]], [[anomaly detection]] and [[collection]] |
| [[classification model]] | The classification task in general                                                                                          |

## How to choose

| Situation | Start with | Then try |
|---|---|---|
| Regression on tabular data | Linear regression or Ridge (on the log of a skewed target) as the baseline | [[Random Forest Regressor]], then [[Gradient Boosting]] or [[XGBoost]] |
| Classification on tabular data | [[Logistic regression (Classification problems)\|Logistic regression]] as the baseline | [[Gradient Boosting]] as the challenger |
| The model must be explained to customers or regulators | Logistic regression or a small [[Decision Tree]] | Boosting, explained with [[SHAP]] |
| Few rows or noisy data | A regularized linear model ([[Ridge and Lasso Regression]]) | A shallow tree model |
| Strong interactions and non-linear effects | [[Gradient Boosting]] or [[XGBoost]] | Tune with early stopping |
| Data ordered in time | [[ARIMA]] or a simple seasonal baseline | Boosting with lag features, validated with a [[Backtest]] |
| Rare positive class | Any of the above, with [[Imbalanced classes]] handled by metrics and thresholds | Class weights, only if the ranking is poor |

A simple model often matches a complex one when the signal is mostly linear or noisy. In the use cases of this vault, logistic regression matched or beat boosting in several of them. Always compare against a [[baseline]]. See [[machine learning use cases/README|Machine learning use cases]].

![[Pasted image 20261027092022.png]]

## Related

- [[Supervised Learning]]
- [[Model Evaluation]]
- [[Overfitting]]
- [[SHAP]]
- [[machine learning/frameworks/README|Machine learning frameworks]]
- [[machine learning use cases/README|Machine learning use cases]]
