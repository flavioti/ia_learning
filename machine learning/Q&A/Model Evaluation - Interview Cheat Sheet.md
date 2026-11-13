---
tags:
  - interview
  - review
aliases:
  - ML Evaluation Interview Cheat Sheet
---
Quick, direct summary of how to evaluate machine learning models, for interview preparation. For the full workflow see [[Model Evaluation]].

## 1. Classification metrics

All derive from the [[Confusion Matrix]] (TP, FP, FN, TN).

| Metric | Meaning | Use when |
|---|---|---|
| [[Accuracy]] | correct / total | Balanced classes only |
| [[Precision]] | TP / (TP + FP) | A false positive is costly (spam filter, fraud alerts) |
| [[Recall]] | TP / (TP + FN) | A false negative is costly (cancer, fraud detection) |
| [[F1-Score]] | Harmonic mean of precision and recall | Imbalanced data, one number balancing both |
| [[ROC-AUC]] | P(random positive is ranked above random negative) | Threshold-independent ranking, moderate imbalance |
| [[PR-AUC]] | Area under the precision-recall curve | **Heavy imbalance** (prefer over ROC-AUC) |
| Log loss ([[Crossentropy]]) | Penalizes confident wrong predictions | You need calibrated probabilities |

- The **decision threshold** is a business choice, not a model property.
- See also [[Imbalanced classes]] and [[Evaluating classification model metrics]].

## 2. Regression metrics

- [[MAE - Mean Absolute Error]]: robust to outliers, in the target's units.
- [[MSE - Mean Squared Error]] / [[RMSE - Root Mean Squared Error]]: penalize large errors more; use when big misses are costly.
- [[R-squared]]: share of variance explained; [[Adjusted R-squared]] corrects for the number of features.
- [[MAPE - Mean Absolute Percentage Error]]: percentage error, breaks when the true value is near zero.
- [[Huber Loss]]: a compromise between MAE and MSE.
- See also [[Evaluating regression model metrics]].

## 3. Validation strategy

- **Train / validation / test split**: the test set is used **once**, at the end.
- [[K-Fold Cross-Validation]]: the standard approach; stratified folds for classification.
- **Time-series split** ([[Backtest]]): train on the past, test on the future. Random splits leak information.
- **Group K-fold**: keeps the same user or patient out of both train and test.
- [[Data Leakage]]: the most common failure. Examples: fitting a scaler before the split, target leakage, duplicates across splits.

## 4. Diagnosing model behavior

- [[Overfitting]] (high variance): train score far better than validation. Fix with regularization, more data, simpler model, early stopping.
- [[Underfitting]] (high bias): both scores poor. Fix with a more complex model or better features.
- **Learning curves** show which of the two you have and whether more data helps.
- **Calibration**: do predicted probabilities match observed frequencies? Check with a reliability diagram or Brier score; fix with Platt scaling or isotonic regression.

## 5. Other task types

- **Ranking / recommendation**: NDCG, MAP, MRR, Precision@K.
- **Clustering**: silhouette score, Davies-Bouldin.
- **LLMs / generative**: perplexity, BLEU/ROUGE (weak), LLM-as-judge, human evals, task benchmarks, RAG metrics (faithfulness, context recall).

## 6. Beyond the metric (senior-level answers)

- **Baseline first**: compare with a dummy model or a simple heuristic.
- **Business alignment**: translate the metric into cost or revenue (cost of a FP vs. a FN).
- **Slice analysis**: performance per segment, for fairness and hidden failures.
- **Statistical significance**: confidence intervals, bootstrap, [[A-B testing]].
- **Offline vs. online**: offline metrics do not always predict online impact; validate with an A/B test.
- **Drift monitoring** in production: [[Model drift]], [[concept drift]], [[Population Stability Index (PSI)]].
- **Interpretability**: [[SHAP]] and permutation importance as a sanity check.

## Common interview questions

1. **Why not accuracy on imbalanced data?** A model predicting the majority class gets 99% accuracy and is useless.
2. **ROC-AUC vs. PR-AUC?** ROC-AUC is inflated by the many true negatives; PR-AUC is more honest when positives are rare.
3. **Precision vs. recall trade-off?** Moving the threshold raises one and lowers the other; choose by error cost.
4. **How do you detect leakage?** Suspiciously high scores, one feature dominating importance, a big drop in production.
5. **Great offline, poor in production. Why?** Train/serve skew, drift, leakage, or a metric that does not match the business goal.

## Related

- [[Model Evaluation]]
- [[Your Model Scores 95% Offline but Fails in Production. How Do You Evaluate It Properly? (PT-BR)]]
- [[Your Used-Car Price Model Has a Low MAE, but the Business Still Loses Money. How Do You Evaluate It?]]
- [[Mock Senior ML Interview]]
- [[machine learning/quality/development/README|Quality: development]]
