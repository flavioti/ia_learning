---
aliases:
  - Fraud
  - Transaction fraud
  - Payment fraud
---
#use-case #classification #fraud #xgboost #imbalanced-data

# Fraud detection

Decide, for each transaction (a card payment, a transfer, an account login), **how likely it is to be fraud**, so the business can **block it, ask for extra verification, or send it to a human reviewer** before the money is lost.

It is a **binary classification** problem with **extreme class imbalance**: fraud is often well under 1% of the transactions. The model outputs a **fraud score**, and a business rule turns the score into an action. It is the use case where **XGBoost** is the usual first choice: tabular data, strong feature interactions, a rare positive class, and a need for fast scoring.

## Problem framing

| Question | Typical answer |
|---|---|
| Target | `fraud` = 1 if the transaction was later confirmed as fraud (for example a chargeback or a customer report), otherwise 0 |
| Model output | A probability or score, not only a yes/no |
| Decision | Approve, **step-up** (extra verification), **review** or **block**, by score ranges |
| Class balance | **Extremely imbalanced**: about 0.9% in the example below |
| Latency | Often milliseconds, because the decision happens while the customer waits |
| Capacity | Human reviewers can check only a limited number of alerts per day |

See problem framing, Imbalanced classes and Business ML models. A related decision problem is Credit approval.

## Why XGBoost fits

| Need | How XGBoost helps |
|---|---|
| Tabular features of many types | Trees need no scaling and handle mixed features |
| Interactions are the signal (a night purchase **and** a new device **and** a high amount) | Trees learn interactions on their own, where logistic regression needs them built by hand |
| Rare positive class | Handles imbalance with `scale_pos_weight`, sample weights and PR-AUC as the early stopping metric |
| Missing values (a new customer with no history) | Native handling of missing values, no imputation needed |
| Low latency | Fast prediction, with small trees |
| Business rules and regulation | Monotonic constraints, and SHAP values for reason codes |
| Training on millions of rows | Fast histogram training, GPU and distributed options |

A simple logistic regression stays useful as a **baseline** and as a comparison. See baseline.

## Data and features

| Group | Examples |
|---|---|
| Transaction | Amount, time and hour of day, merchant category, channel, currency |
| Customer and card | Card age, account age, usual spending level |
| Device and session | New or known device, IP address, country mismatch |
| Geography | Distance from home or from the previous transaction, foreign country |
| **Behavior and velocity** | Number of transactions in the last hour, day or week, amount compared with the customer's average, number of distinct merchants |
| Network | Links between cards, devices and merchants that have been involved in fraud |

- **Velocity and behavior features** are usually the strongest. They are aggregations over a **time window**, and they must be computed with only the data **before** the transaction. See point-in-time and Offline Feature Store.
- At scoring time the same features come from an Online Feature Store, computed with the **same definitions**, otherwise Training-Serving Skew appears.

>[!warning] **Leakage and time:** never use information that arrives after the transaction, such as a later chargeback flag, "account blocked" or a feature computed over a window that includes later events. Split train and test **by date**. See Data Leakage and Backtest.

## Labels arrive late

A fraud is confirmed days or weeks later (a customer complaint, a chargeback). That brings three problems:

- **Delayed Ground Truth:** recent transactions are not labeled yet, and the latest period looks cleaner than it is. Leave a **maturity period** before using data for evaluation.
- **Incomplete labels:** a fraud that nobody noticed is labeled as normal.
- **Feedback loop:** transactions that the model **blocked** never reveal whether they were really fraud, and the fraudsters change their behavior in response. A random sample of approved transactions, or a small exploration group, helps to keep learning.

## Metrics

Accuracy is useless: a model that approves everything is 99% accurate.

| Metric | What it tells you |
|---|---|
| PR-AUC | Precision and recall trade-off for the rare class. The main ranking metric. A random model scores about the fraud rate |
| ROC-AUC | Ranking quality, but it looks good even when precision is poor, because the negatives are so many |
| Precision at the alert budget | Of the alerts raised, how many are real fraud. Measures wasted reviews |
| Recall at the alert budget | Of all the frauds, how many were caught |
| **Value or cost** | Fraud amount prevented minus the cost of reviews and of annoying good customers |
| Calibration, Brier score | Whether a score of 5% means 5%. Matters if the score feeds rules and pricing |

See Evaluation classification model metrics.

### Choosing the threshold by value and capacity

The decision is not "score above 0.5". It comes from two limits:

- **Cost:** a missed fraud loses the transaction amount, while a review costs time and a false block annoys a good customer. Fraud amounts differ, so large transactions deserve a lower threshold.
- **Capacity:** reviewers can handle only a fixed number of alerts, so a common rule is "review the top N% by score".

Choose the threshold on validation data to maximize the net value, and confirm it on a later test period.

## Example (synthetic data)

An illustration with generated transactions, **not real data**: 250,000 transactions in time order with 2,230 frauds (0.89%). Eight features: amount, hour, distance from home, transactions in the last hour, new device, card age, merchant risk and foreign country. Fraud depends on the features and on three interactions (night and a high amount, a new device with high velocity, a foreign transaction far from home). The split is **by time**: the first 70% for training (1,586 frauds), the next 15% for validation (304) and the last 15% for testing (340).

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from xgboost import XGBClassifier

# X_train, X_val, X_test, y_train, y_val, y_test: split by time (older to newer)
lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
hgb = HistGradientBoostingClassifier(random_state=0)

xgb = XGBClassifier(
    n_estimators=3000, learning_rate=0.05, max_depth=4,
    subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
    eval_metric="aucpr",              # PR-AUC is the right metric for a rare class
    early_stopping_rounds=50,         # stop when the validation PR-AUC stops improving
    random_state=42, n_jobs=-1)
xgb.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

score = xgb.predict_proba(X_test)[:, 1]

# Value-based threshold, chosen on validation data:
# fraud amount prevented minus 5 per reviewed alert
REVIEW_COST = 5.0
def net_value(y_true, score, amount, threshold):
    flagged = score >= threshold
    return (y_true * amount * flagged).sum() - REVIEW_COST * flagged.sum()
```

Test results (the top 1% of transactions by score is the alert budget):

| Model | ROC-AUC | PR-AUC | Brier | Precision @ top 1% | Recall @ top 1% |
|---|---|---|---|---|---|
| Logistic regression | 0.846 | 0.097 | 0.00861 | 0.173 | 0.191 |
| HistGradientBoosting | 0.877 | 0.148 | 0.00888 | 0.221 | 0.244 |
| **XGBoost (early stopping)** | 0.878 | **0.180** | **0.00822** | **0.243** | **0.268** |
| XGBoost + `scale_pos_weight` | **0.891** | 0.181 | 0.12021 | 0.237 | 0.262 |

The PR-AUC of a random model would be about 0.009 (the fraud rate).

What the results show:

- **XGBoost beats logistic regression clearly** (PR-AUC 0.180 versus 0.097), because the fraud signal contains interactions that a linear model cannot represent. This is the opposite of Credit approval and Churn, where the simple model matched boosting. It is partly by construction (the generated fraud has interactions), but real fraud also depends on interactions.
- **The advantage over scikit-learn's histogram boosting is smaller** (0.180 versus 0.148). With only 340 frauds in the test set, differences like this are noisy. Do not read them as a fixed ranking.
- **`scale_pos_weight` does not improve the ranking but ruins the probabilities.** The PR-AUC is the same (0.181 versus 0.180), and the mean predicted fraud probability jumps from 0.009 to **0.274**, so the Brier score becomes 15 times worse (0.00822 to 0.12021). The ROC-AUC rose slightly (0.878 to 0.891), which shows why it is a poor guide here. Use the weight only if you need to rank, and recalibrate if you need probabilities. See Imbalanced classes.
- **The model without weights is already well calibrated** (mean score 0.0090 versus actual rate 0.0091).
- **Early stopping on PR-AUC stopped early** (31 trees without weights, 88 with weights), which is a sign that there is little data for the rare class, and that a validation set with more frauds would give a more stable choice.

**Business value** with made-up amounts (fraud amounts are the transaction amounts, and a review costs 5):

| Decision on the test period | Result |
|---|---|
| Flag nothing | 0 prevented, all fraud losses of 61,283 stay |
| Threshold 0.5 | Flags 1 transaction, net value **148** |
| **Threshold 0.0238 (chosen on validation)** | Flags 2,235 transactions (6.0%), catches **193 of 340 frauds** (recall 0.57, precision 0.09), net value **33,631** |

The default threshold of 0.5 almost never raises an alert, because even a high-risk transaction has a low probability when the base rate is under 1%. The value-based threshold flags more transactions, and only about 9% of the alerts are real fraud, but it prevents more than half of the fraud and the net value is much higher. Precision is low on purpose: a missed fraud is more expensive than a review. The amounts and costs are invented. Real ones come from the loss per fraud, the review cost and the customer friction.

**Most important features** (XGBoost built-in importance): new device (0.35), amount (0.19), transactions in the last hour (0.16), hour (0.11) and merchant risk (0.07). For a reliable view, and for reasons per decision, use SHAP. Built-in importances can mislead with correlated features.

## Explaining decisions

- **Reason codes:** SHAP values give the top features behind a single score, for example "new device" and "five transactions in the last hour". Reviewers use them to decide faster, and customers can be told why a step-up was requested.
- **Monotonic constraints:** force known relationships (a higher velocity never lowers the risk), which makes the model more stable and easier to audit.
- **Regulation and fairness:** do not use protected attributes or their proxies, and check error rates across groups.

## Monitoring in production

Fraud is **adversarial**: criminals adapt, so the data changes faster than in most use cases. Monitoring starts without ground truth, because labels are late. See Steps to model monitoring.

| Stage | What to watch |
|---|---|
| **Right away** (Open loop monitoring) | Score distribution, share of transactions flagged, Population Stability Index (PSI) on the score and key features, volume per alert type |
| **Operations** | Alert volume against reviewer capacity, review outcomes, false block complaints |
| **After labels mature** (Closed loop monitoring) | PR-AUC, recall at the alert budget and value on matured cohorts |
| **Changing attacks** | concept drift: new fraud patterns appear, and the old ones disappear. See Model drift |
| **Retraining** | Retrain often on recent data. Compare a new model with the current one on the same period before replacing it (champion and challenger) |

## Common pitfalls

- Using accuracy, or the default 0.5 threshold
- Random splits instead of splits by time, and velocity features that include later events (leakage)
- Evaluating on recent data whose fraud labels have not matured
- Using `scale_pos_weight` or resampling and then trusting the probabilities
- Ignoring the transaction amount: a missed large fraud costs far more than a missed small one
- Ignoring reviewer capacity, so the alerts overwhelm the team
- Training only on transactions that were approved, because blocked ones have no labels
- Features computed differently offline and online (Training-Serving Skew)
- Never retraining, while the fraud patterns change
- Trusting small differences between models when there are only a few hundred frauds in the test set

## Related

- XGBoost
- SHAP
- Gradient Boosting
- Imbalanced classes
- Credit approval
- Churn
- Business ML models
- Offline Feature Store
- Online Feature Store
- point-in-time
- Backtest
- Data Leakage
- Model drift
