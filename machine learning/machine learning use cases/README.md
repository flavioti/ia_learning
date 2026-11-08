# Machine learning use cases

Index of end-to-end use cases. Each note frames the problem, compares algorithms, picks metrics and lists the pitfalls. Most notes include a runnable example on synthetic or public data.

## Regression

| Use case           | Best algorithms                                                                                                                                                                       | Key metrics                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| House price    | Gradient Boosting (XGBoost, LightGBM, `HistGradientBoostingRegressor`), with Random Forest Regressor as a strong default and Ridge/Lasso as the baseline                      | RMSE - Root Mean Squared Error, MAE - Mean Absolute Error, R-squared                 |
| Used-car price | Ridge on the **log of the price** as the baseline, Gradient Boosting (LightGBM, CatBoost) for interactions. A log-linear model can match boosting when effects are multiplicative | MAE - Mean Absolute Error, MAPE - Mean Absolute Percentage Error, error by price segment |

## Classification

| Use case            | Problem type                                         | Best algorithms                                                                                                                                                                                 | Key metrics                                                                                         |
| ------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Credit approval | Binary classification (imbalanced)                   | Logistic regression scorecard as the baseline, Gradient Boosting as the challenger. Explainability often outweighs a small accuracy gain | ROC-AUC, Gini, KS, calibration, cost-based threshold                                            |
| Credit Risk     | Classification (PD), plus regression for LGD and EAD | Logistic regression scorecard (WoE + IV, points scaling), Gradient Boosting as a challenger                                              | Gini, KS, calibration, Population Stability Index (PSI)                                         |
| Churn           | Binary classification (imbalanced)                   | Logistic regression as the baseline, Gradient Boosting as the challenger, survival models when timing matters                            | ROC-AUC, PR-AUC, lift and precision at top N%, campaign profit                              |
| Fraud detection | Binary classification (extremely imbalanced)         | XGBoost (early stopping on PR-AUC), with logistic regression as the baseline. Trees learn the feature interactions that fraud depends on | PR-AUC, precision and recall at the alert budget, net value (fraud prevented minus review cost) |

## Takeaways

- **Tabular data:** Gradient Boosting is usually the most accurate choice, but always compare against a simple baseline (House price).
- **Boosting wins on interactions:** in Fraud detection, XGBoost clearly beat logistic regression (PR-AUC 0.18 versus 0.10), because the fraud signal depends on feature interactions that a linear model cannot represent.
- **A simple model can win:** logistic regression matched or beat gradient boosting in Credit approval, Credit Risk and Churn, and a log-linear model did the same in Used-car price. This is partly because the synthetic signal is mostly linear, so do not assume the complex model wins.
- **Regulated, high-stakes decisions:** start with an explainable model such as logistic regression as the baseline (Credit approval, Credit Risk).
- **Skewed, multiplicative targets:** prices lose a percentage of value, not a fixed amount. Train on the log of the target and evaluate back in the original unit (Used-car price).
- **Relative vs absolute error:** report MAE and MAPE together, and look at the error by price segment. R-squared alone hides the differences.
- **Imbalanced classes:** do not use accuracy. Rank with AUC/Gini/KS or PR-AUC, check calibration, and choose the threshold or the contacted share by business cost, not 0.5.
- **Class weights:** `class_weight="balanced"` and XGBoost's `scale_pos_weight` do not improve the ranking and distort the probabilities (Churn, Fraud detection).
- **Splits:** split by date (credit, churn, used cars) or by area/date (house price) to avoid leaking the future or neighbors into training.
- **Labels can arrive late:** monitor first without ground truth, then confirm with matured outcomes (credit, fraud).
- **The market moves:** retrain on recent data and monitor the bias over time, since trees cannot extrapolate beyond the training range (Used-car price). See Model drift.

## Related

- Gradient Boosting
- XGBoost
- Logistic regression (Classification problems)
- Imbalanced classes
- Evaluation classification model metrics
- Evaluating regression model metrics
- Steps to model monitoring
