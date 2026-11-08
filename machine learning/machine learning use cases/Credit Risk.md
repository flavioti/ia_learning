---
aliases:
  - Scorecard
  - Credit Score
---
#logistic-regression #credit-risk #use-case
# Credit risk

**Credit risk** is the risk of **losing money** because a borrower does not repay a loan, card balance or other credit on time. A credit risk model estimates that risk for each customer, so the lender can decide **who to lend to, how much, and at what price**.

The classic machine learning form of this model is the **scorecard** (also called a **credit score**): a transparent logistic regression that turns applicant data into a number, where a higher score means lower risk.

Related use case: Credit approval (the approve or reject decision built on top of these models).

## The three components of risk

Credit loss is usually split into three parts, each with its own model:

| Component | Name | Question | Typical model |
|---|---|---|---|
| **PD** | Probability of Default | How likely is the borrower to default in a given period (for example 12 months)? | Classification: scorecard, Gradient Boosting |
| **LGD** | Loss Given Default | If they default, what share of the amount is lost after recoveries? | Regression (a share between 0 and 1) |
| **EAD** | Exposure at Default | How much will be owed at the moment of default? | Regression |

$$
\text{Expected Loss} = \text{PD} \times \text{LGD} \times \text{EAD}
$$

**Example:** a loan of 10,000 where PD = 5%, LGD = 40% and EAD = 10,000 has an expected loss of $0.05 \times 0.40 \times 10{,}000 = 200$. The lender must price the loan and hold reserves to cover this loss. Banking regulation (such as the Basel framework and IFRS 9 provisioning) is built on these same three quantities.

Most ML material focuses on **PD**, because it is a classification problem with a clear target. This note does too.

## Types of scorecard

| Scorecard | Used when | Information available |
|---|---|---|
| **Application score** | A new customer applies | Application form, bureau data |
| **Behavior score** | An existing customer, to manage limits and offers | Payment and usage history |
| **Collection score** | An account is late, to decide how to approach recovery | Delinquency stage, past contact results. See collection |
| **Fraud score** | Detect fake or stolen identities | Different problem. See Business ML models |

## Why logistic regression?

The scorecard stays popular even though more accurate models exist, because it is:

- **Explainable:** each feature adds or removes a known number of points, so a rejection can be justified
- **Stable and auditable:** regulators and risk teams can review every rule
- **Well calibrated:** its probabilities usually match the real default rates
- **A strong baseline:** hard to beat by much when the signal is noisy. See baseline

Gradient boosting is often used as a **challenger** to find extra signal, with explainability tools on top. See Logistic regression (Classification problems).

## How a scorecard is built

1. **Define the target:** what a "bad" customer is (for example 90 days late within 12 months) and the observation window. Labels arrive late. See Ground Truth.
2. **Split by date,** not randomly, to avoid leaking the future. See Data Leakage.
3. **Bin each feature** into ranges. See Discretization.
4. **Replace each bin with its WoE** (Weight of Evidence) and measure each feature with its **IV** (Information Value).
5. **Fit a logistic regression** on the WoE values.
6. **Scale the output to points** (the score), so that a fixed number of points doubles the odds.
7. **Validate:** ranking power (Gini, KS), calibration, stability. Then group scores into **risk bands**.

### Weight of Evidence (WoE)

For each bin, WoE compares the share of good customers with the share of bad customers:

$$
\text{WoE}_i = \ln\left(\frac{\%\text{ of good in bin } i}{\%\text{ of bad in bin } i}\right)
$$

- Positive WoE: the bin has more good customers than average (lower risk)
- Negative WoE: the bin has more bad customers than average (higher risk)
- It puts every feature on the **log-odds scale**, handles missing values and outliers as just another bin, and makes the relationship with risk **monotonic**

### Information Value (IV)

IV summarizes how well a whole feature separates good from bad:

$$
\text{IV} = \sum_{i} \left(\%\text{good}_i - \%\text{bad}_i\right) \times \text{WoE}_i
$$

| IV | Predictive power (rule of thumb) |
|---|---|
| Below 0.02 | Not useful |
| 0.02 to 0.1 | Weak |
| 0.1 to 0.3 | Medium |
| 0.3 to 0.5 | Strong |
| Above 0.5 | Suspiciously strong: check for leakage |

### Score scaling

The model predicts the probability of being bad. The score converts the **odds** (good to bad) into points, using three choices:

- **Base score:** the score at some reference odds (for example 600 points at 50 to 1)
- **PDO** (points to double the odds): how many points double the odds (for example 20)

$$
\text{Factor} = \frac{\text{PDO}}{\ln 2} \qquad \text{Offset} = \text{Base score} - \text{Factor} \times \ln(\text{Base odds})
$$

$$
\text{Score} = \text{Offset} + \text{Factor} \times \ln(\text{odds of good})
$$

## Example (synthetic data)

An illustration with generated applicants, **not real data**: 20,000 applicants, about 10% bad, five features (income, debt ratio, credit utilization, history length, past delinquencies). Train and test are split 70/30.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

features = ["income", "debt_ratio", "utilization", "history_years", "delinquencies"]
# train / test: DataFrames with the features and a `bad` column (1 = default)

# 1. Bin each feature into 5 quantile bins (delinquencies is already a small count)
edges = {}
def bin_feature(s, name, fit=False):
    if name == "delinquencies":
        return s.astype(int)
    if fit:
        edges[name] = np.unique(np.quantile(s, np.linspace(0, 1, 6)))
        edges[name][0], edges[name][-1] = -np.inf, np.inf
    return pd.cut(s, edges[name], labels=False)

for f in features:
    train[f + "_bin"] = bin_feature(train[f], f, fit=True)
    test[f + "_bin"] = bin_feature(test[f], f)

# 2. WoE and IV, computed on the training data only
total_good, total_bad = (train.bad == 0).sum(), (train.bad == 1).sum()
woe_maps, iv = {}, {}
for f in features:
    g = train.groupby(f + "_bin").bad.agg(bad="sum", n="count")
    g["good"] = g.n - g.bad
    pct_good = (g.good + 0.5) / total_good          # +0.5 avoids log(0)
    pct_bad = (g.bad + 0.5) / total_bad
    g["woe"] = np.log(pct_good / pct_bad)
    woe_maps[f] = g["woe"]
    iv[f] = ((pct_good - pct_bad) * g["woe"]).sum()

def woe_frame(d):
    return pd.DataFrame({f: d[f + "_bin"].map(woe_maps[f]) for f in features}).fillna(0)

# 3. Logistic regression on the WoE values
lr = LogisticRegression(max_iter=1000).fit(woe_frame(train), train.bad)
p_bad = lr.predict_proba(woe_frame(test))[:, 1]
auc = roc_auc_score(test.bad, p_bad)                # 0.689, Gini = 2 * AUC - 1 = 0.379

# 4. Scale to points: 600 at 50:1 odds, +20 points double the odds
factor = 20 / np.log(2)
offset = 600 - factor * np.log(50)
test["score"] = offset + factor * (-lr.decision_function(woe_frame(test)))   # decision_function = ln(bad/good)
```

**Information Value** (training data):

| Feature | IV | Power |
|---|---|---|
| debt_ratio | 0.128 | Medium |
| history_years | 0.102 | Medium |
| delinquencies | 0.093 | Weak |
| income | 0.084 | Weak |
| utilization | 0.083 | Weak |

**WoE by bin:** for `utilization` (from the lowest to the highest bin) the WoE is `0.37, 0.26, 0.08, -0.13, -0.43`. It falls steadily, so higher utilization means higher risk, which is exactly the monotonic pattern a scorecard wants.

**Test results:** AUC 0.689, Gini 0.379. Because the inputs are WoE values on the log-odds scale, the fitted coefficients all come out close to -1 (the minus sign appears because the model predicts the probability of being *bad*).

**Risk bands** (test set, scores grouped into five equal-sized bands):

| Band | Applicants | Bad rate | Score range |
|---|---|---|---|
| E (riskiest) | 1,202 | 19.0% | 463 to 538 |
| D | 1,199 | 13.5% | 538 to 551 |
| C | 1,200 | 8.4% | 551 to 563 |
| B | 1,201 | 5.6% | 563 to 575 |
| A (safest) | 1,198 | 2.8% | 575 to 614 |

The bad rate falls steadily from the riskiest band to the safest one. The bands let the business act on score ranges, for example: approve A and B, review C, reject D and E, or charge a higher rate for riskier bands. This is a single synthetic split, so treat the numbers as an illustration.

## Evaluation

| Question | Metric |
|---|---|
| Does the score rank risky customers above safe ones? | ROC-AUC, Gini (2 x AUC - 1), KS statistic |
| Are the probabilities correct? | Calibration, Brier score, log loss. See Crossentropy |
| Is the score stable over time? | Population Stability Index (PSI) on the score and on each feature |
| What is the business result? | Approval rate, bad rate in the approved population, expected loss |

See Evaluation classification model metrics. Accuracy is a poor choice because defaults are rare.

## Monitoring

Scorecards run for years, so they must be watched. Monitoring starts before the outcome is known (Open loop monitoring: PSI, score distribution) and is confirmed when labels mature (Closed loop monitoring: Gini, KS, calibration). An economic shock can change the default rate for the same profile (concept drift). See Steps to model monitoring.

## Pitfalls

- **Selection bias:** only approved customers have outcomes, so the training data is a filtered population (reject inference tries to correct this)
- **Leakage:** a feature that is only known after the loan was granted. A suspiciously high IV (above 0.5) is a warning sign
- **Fixed bins:** the bins and the WoE are learned on training data. Reuse them unchanged in production
- **Protected attributes:** do not use them or close proxies for them, and check fairness
- **Regulation:** requirements differ by country and change over time, so involve risk and compliance teams

## Related

- Credit approval
- Logistic regression (Classification problems)
- Gradient Boosting
- Decision Tree Classifier
- Discretization
- collection
- Business ML models
