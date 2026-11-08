#use-case #classification #credit-risk
# Credit approval

Decide whether to **approve or reject a credit application** (loan, credit card, financing) by estimating how likely the applicant is to **default**, which means failing to repay.

It is a **binary classification** problem. The model usually outputs a **probability of default (PD)**, and a business rule turns that probability into a decision. The classic form of this model is the **scorecard**, built with logistic regression. See Credit Risk.

## Problem framing

| Question | Typical answer |
|---|---|
| Target | `default` = 1 if the applicant did not repay within a fixed window (for example 12 months), otherwise 0 |
| Model output | A probability of default, not only a yes/no |
| Decision | Approve if the PD is below a threshold. The threshold comes from business cost, not from 0.5 |
| Extra decisions | Credit limit, interest rate and manual review for borderline cases |
| Class balance | **Imbalanced**: defaults are usually a small share of the applicants |

See problem framing and Discrete Classes.

## Data and target

- **Applicant data:** income, debt-to-income ratio, credit utilization, length of credit history, past late payments, employment, requested amount
- **Behavior and bureau data**, when available
- **Define the target carefully:** what counts as a default (for example 90 days late) and over which **observation window** changes the model and its results
- **Labels arrive late.** The real outcome appears months after the decision, so Ground Truth is delayed. This shapes how you validate and monitor the model.

>[!warning] **Leakage and time:** never use information that was not known at the time of the application, such as a later payment status. Split train and test **by date** (train on older applications, test on newer ones), not randomly. See Data Leakage and train dataset and test dataset.

### Selection bias (reject inference)

You only know the outcome of **approved** applicants. Rejected applicants never got a loan, so their label is unknown. A model trained only on approved applicants learns from a filtered population and can be biased for the borderline cases it is meant to decide. Techniques called **reject inference** try to correct this. At the least, be aware that the training data is not the full applicant population.

## Which algorithm?

| Algorithm | Strength | Weakness |
|---|---|---|
| **Logistic regression** (scorecard) | Simple, stable, well calibrated, **easy to explain** to customers and regulators | Misses non-linear effects and interactions unless you engineer them |
| Decision Tree Classifier | Auditable rules | Unstable and weaker on its own |
| Gradient Boosting | Often the most accurate, captures interactions | Harder to explain, needs calibration, can overfit on small data |

In credit, **explainability often outweighs a small accuracy gain**: a rejection must be justified with clear reasons. A common approach is a logistic regression scorecard as the baseline, with gradient boosting as a challenger, explained with feature-importance tools such as SHAP and with monotonic constraints (for example, a higher debt ratio can never lower the risk). See baseline.

### Features

- Continuous variables are often **binned** into ranges, so the model is stable and the scorecard is readable. See Discretization and the credit score example there.
- Encode categories properly. See Categorical columns.
- **Do not use protected attributes** (such as gender, race or religion), or close proxies for them. See the fairness section.

## Metrics

Accuracy is a poor choice because the classes are imbalanced. Credit teams look at how well the model **ranks** risky applicants above safe ones, and at how good the **probabilities** are.

| Metric | What it tells you |
|---|---|
| ROC-AUC | How well the score ranks defaulters above non-defaulters |
| **Gini** = 2 x AUC - 1 | The same information on a 0 to 1 scale. This is the credit-scoring Gini coefficient, not the Gini impurity used in decision trees. See Gini |
| **KS statistic** | The maximum gap between the score distributions of defaulters and non-defaulters, which equals max(TPR - FPR) |
| PR-AUC | Precision and recall trade-off for the rare default class |
| Calibration, Brier score, log loss | Whether a predicted PD of 10% really means 10% of such applicants default. Critical when the PD feeds pricing or provisioning. See Crossentropy |
| Confusion Matrix at a threshold | How many defaulters are approved and how many good applicants are rejected |

See Evaluation classification model metrics.

### Choosing the threshold by cost

The two mistakes have different costs:

- **Approving a defaulter** (false negative): you lose the money lent.
- **Rejecting a good applicant** (false positive): you lose the interest you would have earned.

The first is usually much more expensive. Pick the threshold that **minimizes the total expected cost** on validation data, and confirm it on a test set. The default 0.5 is almost always wrong for imbalanced data.

## Example (synthetic data)

An illustration with generated applicants, **not real data**: 20,000 applicants, about 11.5% defaults, five features (income, debt ratio, credit utilization, history length, past delinquencies). The data is split into train, validation and test sets.

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix

# X_train, X_val, X_test, y_train, y_val, y_test: applicants split by stratified sampling
models = {
    "Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Gradient boosting":   HistGradientBoostingClassifier(random_state=0),
}

def ks(y_true, score):
    fpr, tpr, _ = roc_curve(y_true, score)
    return (tpr - fpr).max()

for name, model in models.items():
    model.fit(X_train, y_train)
    pd_test = model.predict_proba(X_test)[:, 1]          # probability of default
    auc = roc_auc_score(y_test, pd_test)
    print(name, auc, 2 * auc - 1, ks(y_test, pd_test))   # AUC, Gini, KS

# Threshold by cost: approving a defaulter costs 5x more than rejecting a good applicant
COST_FN, COST_FP = 5, 1

def cost(y_true, score, threshold):
    reject = score >= threshold
    fn = ((~reject) & (y_true == 1)).sum()               # approved, then defaulted
    fp = (reject & (y_true == 0)).sum()                  # rejected, would have paid
    return COST_FN * fn + COST_FP * fp

pd_val = models["Gradient boosting"].predict_proba(X_val)[:, 1]
grid = np.linspace(0.01, 0.6, 120)
threshold = grid[np.argmin([cost(y_val, pd_val, t) for t in grid])]   # chosen on validation
```

| Model | AUC | Gini | KS | PR-AUC | Brier |
|---|---|---|---|---|---|
| Logistic regression | 0.710 | 0.420 | 0.315 | 0.250 | 0.095 |
| Gradient boosting | 0.700 | 0.400 | 0.303 | 0.232 | 0.097 |

On this data the **simple logistic regression matches or slightly beats gradient boosting**. This is partly by construction, because the generated risk is mostly linear, but it is also common in credit, where the signal is noisy and a stable, explainable model is hard to beat. Do not assume the more complex model wins.

The threshold changes the business result far more than the algorithm (gradient boosting scores on the test set, with the made-up costs above):

| Threshold | Approval rate | Defaulters approved | Good applicants rejected | Total cost |
|---|---|---|---|---|
| 0.5 (default) | 99.3% | 450 of 460 | 19 | 2,269 |
| 0.179 (cost-based) | 82.5% | 282 of 460 | 522 | **1,932** |

With 0.5 the model approves almost everyone and catches only 10 of the 460 defaulters. The cost-based threshold rejects many more good applicants, but the total cost is lower, because each missed defaulter is the expensive mistake. The costs here are invented for illustration. Real costs come from the loss given default and the margin on a good loan.

## Explainability and fairness

- **Explain every decision.** Rejected applicants should receive the main reasons (for example, high utilization and recent late payments). Simple models and tools such as SHAP make this possible.
- **Fairness:** check that approval and error rates do not differ unjustifiably between groups, even when protected attributes are excluded, because other features can act as proxies.
- **Regulation:** credit decisions are heavily regulated, and rules differ by country. Treat auditability, documentation and human review of borderline cases as part of the requirements, not as extras.

## Monitoring in production

The outcome takes months to appear, so monitoring starts **without ground truth** and is confirmed **with ground truth** later. See Steps to model monitoring.

| Stage | What to watch |
|---|---|
| **Right away** (Open loop monitoring) | Do today's applicants look like the training population? Population Stability Index (PSI) on the score and on key features, approval rate, score distribution |
| **After the outcome** (Closed loop monitoring) | Gini, KS and calibration on matured cohorts. A drop means the model is losing power |
| **Economic changes** | concept drift: after a shock, the same income and debt profile can carry a much higher default rate, even if the applicants look the same. See Model drift |
| **Retraining** | Retrain on recent data and compare the new model against the current one before replacing it |

Remember the selection bias: once the model rejects a group, you stop seeing what would have happened to them, so a drop in applicants' quality can hide inside the approved population.

## Common pitfalls

- Using accuracy on imbalanced data (a model that approves everyone looks 88% accurate in the example above)
- Random splits instead of splits by date, which leak the future into training
- Using the default 0.5 threshold
- Ignoring that only approved applicants have labels
- Uncalibrated probabilities feeding pricing or provisioning
- Using protected attributes or their proxies
- Optimizing accuracy while the business needs explainability

## Related

- Credit Risk
- Logistic regression (Classification problems)
- Gradient Boosting
- Decision Tree Classifier
- Discrete Classes
- Evaluation classification model metrics
- Steps to model monitoring
- Ground Truth
- Churn
