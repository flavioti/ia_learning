Model quality during **development**: how to measure, validate and diagnose a model before it goes to production. For what happens after deployment, see the production notes in [[#Related]].

## Workflow

1. Prepare the data: [[Data Cleaning]]
2. Split and validate: [[Model Evaluation]], [[K-Fold Cross-Validation]], and [[Backtest]] for time-ordered data
3. Measure with the right metrics (see below)
4. Diagnose the fit: [[Overfitting]] and [[Underfitting]], and with a [[Learning Curve - Linear regression|learning curve]] to see whether more data would help

## Classification metrics

All of them derive from the [[Confusion Matrix]] (TP, FP, FN, TN).

| Note | Question it answers | Penalizes |
|---|---|---|
| [[Accuracy]] | How many predictions were correct overall? | All errors (misleading when imbalanced) |
| [[Precision]] | Of what was predicted positive, how much was right? | False positives |
| [[Recall]] | Of what was actually positive, how much was found? | False negatives |
| [[F1-Score]] | Is the balance between precision and recall good? | Weakness in either |
| [[ROC-AUC]] | How well are positives ranked above negatives, at any threshold? | Poor ranking |

Which one to pick:

- Balanced classes, equal error cost: [[Accuracy]]
- False positives are costly (spam filter, fraud block): [[Precision]]
- False negatives are costly (medical screening, intrusion): [[Recall]]
- Imbalanced classes, need a single number: [[F1-Score]]
- Compare models independent of a threshold: [[ROC-AUC]]; with severe imbalance prefer [[PR-AUC]]

More in [[Evaluation classification model metrics]] and [[Evaluating regression model metrics]].

## Model validation and fit

- [[Model Evaluation]]: the evaluation workflow and what makes a model good
- [[K-Fold Cross-Validation]]: robust estimate of generalization performance
- [[Model Evaluation - Interview Cheat Sheet]]: direct summary of metrics, validation and diagnostics for interviews
- [[Overfitting]] (high variance): great on training data, poor on new data
- [[Underfitting]] (high bias): poor on both

## Decision tree split criteria

- [[Entropy]] (stub)
- [[Gini]] (stub)

## Folders

- `classification models/`: model-specific notes for classification (empty for now)
- `regression models/`: model-specific notes for regression (empty for now)

## Files in this folder

- `roc_auc_generator.py` generates `roc_curve.png`, used in [[ROC-AUC]]
- `k-fold-cross-validation.png`, used in [[K-Fold Cross-Validation]]

## To do

- Expand the stubs: [[Entropy]], [[Gini]]
- Translate the remaining Portuguese notes to English: [[Accuracy]], [[Overfitting]], [[Underfitting]]

## Related

- [[evaluation]]
- [[Evaluation classification model metrics]]
- [[Evaluating regression model metrics]]
- Production quality: [[Model drift]], [[concept drift]], [[model performance monitoring]], [[champion and challenger]]
- [[Machine Learning|Machine Learning]]
