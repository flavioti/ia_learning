#marketing #use-case #classification #churn
# Churn

Predict which customers are **about to leave** (cancel a subscription, stop buying, close an account), so the business can act **before** they go, for example with a retention offer.

It is usually a **binary classification** problem: for each customer, predict the probability of churning in the next period (for example 30 or 90 days). The model output is a **ranking of customers by risk**, and the business decides how many to contact. Similar framing to Credit approval, with a different cost structure.

## Problem framing

| Question | Typical answer |
|---|---|
| Target | `churn` = 1 if the customer left (or became inactive) within the **prediction window**, otherwise 0 |
| Model output | A churn probability used to **rank** customers, not only a yes/no |
| Decision | Contact the top N% of customers with an offer. N comes from budget and economics |
| Class balance | **Imbalanced**: churners are usually a small share of customers (about 11% in the example below) |
| Churn type | **Contractual** (a cancellation event exists, as in subscriptions) or **non-contractual** (the customer just stops buying, so churn must be defined by inactivity) |

See problem framing and Discrete Classes.

>[!warning] **Define churn carefully.** For non-contractual businesses, "no purchase in 90 days" is a choice. A window that is too short flags customers who are only between purchases. A window that is too long produces labels too late to act on.

## Data and features

All features must be computed **as of the prediction date** (the snapshot), using only data known at that moment. The label comes from the window **after** the snapshot.

| Group | Examples |
|---|---|
| Customer profile | Tenure, plan, contract type, acquisition channel |
| Billing | Monthly charge, price changes, late or failed payments |
| Usage and engagement | Logins, purchases, feature use, and especially the **trend** (usage dropping versus previous months) |
| Support | Number of tickets, complaints, unresolved issues |
| Context | Competitor offers, season, region |

- **Trends and changes** (a usage drop, a new complaint) are often more predictive than static attributes.
- Encode categories properly. See Categorical columns and feature engineering.

>[!warning] **Leakage and time:** features such as "cancellation requested" or "days since last activity" measured after the snapshot leak the answer. Build features at the snapshot date and split train and test **by date** (train on older snapshots, test on newer ones). See Data Leakage and train dataset and test dataset.

## Which algorithm?

| Algorithm | Strength | Weakness |
|---|---|---|
| **Logistic regression** | Fast, well calibrated, easy to explain which factors raise risk. A strong baseline | Misses non-linear effects and interactions unless engineered |
| Decision Tree Classifier | Readable rules for the business | Unstable and weaker on its own |
| Gradient Boosting (XGBoost, LightGBM, `HistGradientBoostingClassifier`) | Usually the most accurate on tabular data, captures interactions | Harder to explain, probabilities need checking |
| Survival models | Predict **when** a customer will leave, not just whether. Useful when timing drives the action | More complex to build and explain |

Start with logistic regression as the baseline and use gradient boosting as the challenger. Keep the one that wins on the business metric, not on accuracy.

### Class imbalance

With few churners, a model that predicts "nobody leaves" is 89% accurate and useless.

- Prefer **ranking metrics** (below) and a threshold or a top N% chosen by business cost.
- `class_weight="balanced"` or resampling can help some models find the rare class, but they **distort the probabilities**. See the example below.
- If you need real probabilities (for lifetime value or budget planning), do not rebalance, or recalibrate afterwards.

## Metrics

Accuracy is a poor choice. Churn teams care about how well the model **puts churners at the top of the list**.

| Metric | What it tells you |
|---|---|
| ROC-AUC | How well the score ranks churners above non-churners |
| PR-AUC | Precision and recall trade-off for the rare churn class. Compare with the base rate (the PR-AUC of a random model equals the churn rate) |
| Precision at top N% | Of the customers contacted, how many were really about to leave |
| Recall at top N% | Of all churners, how many the campaign reached |
| **Lift** at top N% | Precision at top N% divided by the base churn rate. A lift of 3.5 means the top group has 3.5 times more churners than a random group |
| Confusion Matrix at a threshold | Missed churners versus wasted offers |
| Calibration, Brier score | Whether a predicted 30% really means 30% of such customers leave |

See Evaluation classification model metrics.

### Choosing how many customers to contact

Contacting a customer costs money (an offer, a discount, agent time). A retention offer only pays when the customer was **truly going to leave** and the offer **works**.

- **Contacting a customer who would have stayed** (false positive): you pay the offer cost, and may give a discount for nothing.
- **Not contacting a churner** (false negative): you lose the customer's future value.

Pick the share of customers to contact that **maximizes expected profit** on validation data, and confirm it on a test set.

## Example (synthetic data)

An illustration with generated customers, **not real data**: 20,000 customers, about 11% churn, six features (tenure, monthly charge, contract type, support tickets, usage change, late payments). The data is split 60/20/20 into train, validation and test sets with stratified sampling.

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

# X_train, X_val, X_test, y_train, y_val, y_test: customers split by stratified sampling
models = {
    "Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Logistic regression, balanced": make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
    "Gradient boosting": HistGradientBoostingClassifier(random_state=0),
}

def top_k(y_true, score, k=0.10):
    n = int(len(y_true) * k)
    top = np.argsort(-score)[:n]                       # the k% riskiest customers
    precision = y_true[top].mean()
    return precision, precision / y_true.mean(), y_true[top].sum() / y_true.sum()  # precision, lift, recall

for name, model in models.items():
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1]              # churn probability
    print(name, roc_auc_score(y_test, p), average_precision_score(y_test, p),
          brier_score_loss(y_test, p), top_k(y_test, p))

# Campaign economics: retained customer is worth 600, an offer costs 50, an offer saves 30% of churners
VALUE, COST, SAVE = 600, 50, 0.30

def profit(y_true, score, share):
    n = int(len(y_true) * share)
    top = np.argsort(-score)[:n]
    return y_true[top].sum() * SAVE * VALUE - n * COST

gb = models["Gradient boosting"]
p_val, p_test = gb.predict_proba(X_val)[:, 1], gb.predict_proba(X_test)[:, 1]
shares = np.linspace(0.01, 1, 100)
best = shares[np.argmax([profit(y_val, p_val, s) for s in shares])]   # chosen on validation
```

| Model | AUC | PR-AUC | Brier | Precision @10% | Lift @10% | Recall @10% |
|---|---|---|---|---|---|---|
| Logistic regression | 0.823 | 0.393 | 0.083 | 0.412 | 3.66 | 0.366 |
| Logistic regression, balanced | 0.823 | 0.391 | 0.184 | 0.420 | 3.73 | 0.373 |
| Gradient boosting | 0.801 | 0.359 | 0.086 | 0.398 | 3.53 | 0.353 |

The base churn rate is 11.3%, so a random model would have a PR-AUC of about 0.11 and a lift of 1.

What the results show:

- **The simple logistic regression matches or beats gradient boosting.** This is partly by construction, because the generated risk is mostly linear, but it is also common when the signal is noisy. Do not assume the more complex model wins.
- **Balancing the classes does not improve the ranking** (same AUC) but **ruins the probabilities**: the Brier score more than doubles (0.083 to 0.184). Use it only if you do not need real probabilities.
- Reaching the top 10% of customers by risk finds about **a third of all churners** with 3.5 to 3.7 times the base rate.

The number of customers to contact changes the business result far more than the algorithm (gradient boosting scores on the test set, with the made-up values above):

| Customers contacted | Profit |
|---|---|
| None | 0 |
| Top 7% (best on validation) | 8,369 |
| Top 10% | 8,619 |
| Everyone | -118,820 |

Contacting everyone loses a lot of money, because most offers go to customers who would have stayed. A targeted campaign makes a profit. The best share on validation (7%) is close to, but not exactly, the best on the test set, which is normal: choose the share on validation and expect some noise. The values here are invented for illustration. Real ones come from the customer lifetime value, the offer cost and the real success rate of the offer.

## Beyond prediction: who to treat

A churn score tells you **who is likely to leave**, not **who will be saved by an offer**. Some likely churners will leave anyway, and some will stay even without an offer (and may be annoyed or get an unnecessary discount). **Uplift modeling** estimates the effect of the offer itself. Validate a retention program with a **control group** that receives no offer, to measure the real gain.

## Monitoring in production

The churn outcome appears only after the prediction window, so monitoring starts **without ground truth** and is confirmed **with ground truth** later. See Ground Truth and Steps to model monitoring.

| Stage | What to watch |
|---|---|
| **Right away** (Open loop monitoring) | Do today's customers look like the training population? Population Stability Index (PSI) on the score and key features, score distribution, share flagged as high risk |
| **After the window** (Closed loop monitoring) | AUC, PR-AUC, lift and calibration on matured cohorts |
| **Behavior changes** | concept drift: a new competitor, a price change or a new product can change why customers leave. See Model drift |
| **Feedback loop** | The retention campaign changes the outcome you want to predict: customers who received an offer and stayed look like non-churners. Keep a **holdout group** and take the campaign into account when you retrain |
| **Retraining** | Retrain on recent snapshots and compare against the current model before replacing it |

## Common pitfalls

- Using accuracy on imbalanced data
- Features built with data from after the snapshot date (leakage), or random splits instead of splits by date
- A vague churn definition, or a window too short or too long to act on
- Rebalancing the classes and then using the probabilities as if they were real
- Judging the model by AUC alone, without checking lift at the contacted share and the campaign profit
- Contacting everyone, or using a fixed 0.5 threshold, instead of a cost-based share
- Predicting who will leave without checking who can be saved
- Ignoring the feedback loop created by the retention campaign

## Related

- Credit approval
- Logistic regression (Classification problems)
- Gradient Boosting
- Decision Tree Classifier
- Discrete Classes
- Evaluation classification model metrics
- Steps to model monitoring
- Data Leakage
- Business ML models
