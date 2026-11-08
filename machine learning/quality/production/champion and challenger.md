#mlops #deployment

**Champion and challenger** is a safe way to replace a model in production: the model currently serving (the *champion*) is compared against a new candidate (the *challenger*), and the challenger is promoted only if it surpasses the champion's metrics.

- **Champion:** the model in production now
- **Challenger:** a new candidate, e.g. retrained on recent data, with a different algorithm, or different features or hyperparameters

It is the standard way to act on [[Model drift]]: retraining produces a challenger, and this process decides whether it deserves to replace the champion.

## How it works

1. Train a challenger (on a schedule, or when drift is confirmed)
2. Validate it through the rollout stages below, from cheapest to riskiest
3. Apply the promotion rule at each stage
4. If the challenger wins, deploy it and keep the old champion available for rollback
5. If it loses at any stage, keep the champion and record the result

## Rollout stages

The evaluation modes are usually **stages in a sequence**, not alternatives. A better offline metric shows the challenger is good on a held-out set; it does not show it will behave well in production. Each stage adds confidence and exposes more risk.

| Stage                                                     | How                                                                   | What it catches                                                                                                                           | What it does not catch                                                |
| --------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **1. Offline**                                            | Both models score the same recent labeled held-out set                | A quality gain over the champion, cheaply                                                                                                 | Training-serving skew, live traffic differences, latency              |
| **2. [[shadow deployment\|Shadow]]**                      | The challenger receives live traffic, but its output is **not used**  | Pipeline and feature bugs, latency and memory, crashes on real inputs, unusual disagreement with the champion; quality once labels arrive | Real impact on users and downstream systems; effects on future labels |
| **3. [[canary deployment]] / [[A-B testing]]** (optional) | A small share of live traffic (e.g. 5%) is answered by the challenger | Real business impact, with limited exposure                                                                                               | Slower, and users are exposed to a possibly worse model               |
| **4. Full promotion**                                     | The challenger becomes the champion; the old one is kept for rollback |                                                                                                                                           |                                                                       |

**How long to stay in shadow:** long enough to cover a representative period (a full weekly or monthly cycle if traffic is seasonal) and to collect enough labels for a meaningful comparison. If labels take weeks, shadow takes weeks too.

**When to skip or shorten stages:**
- Low-risk use cases, where a bad prediction is cheap
- Rollback is instant and easy
- A routine refresh: same architecture and feature pipeline as the champion, only new training data

> **Not to be confused with a baseline model.** A challenger is a candidate for promotion and is judged on labeled data. A baseline model that runs next to the main model purely as a drift signal is never promoted; see "Disagreement with a baseline model" in [[Monitor Accuracy in Production Continuously]].

## Promotion rule

Do not promote on any tiny improvement: noise would swap models back and forth.

- Require a **minimum margin** (e.g. +1 point of the chosen metric), or a significance test
- Use the metric that matches the business cost: [[Precision]], [[Recall]], [[F1-Score]] or [[ROC-AUC]] rather than [[Accuracy]] alone when classes are imbalanced
- Also compare latency, cost and stability, not only the quality metric
- Evaluate on the same data for both models

```python
MARGIN = 0.01  # minimum gain required to promote

champion_score = evaluate(champion, X_recent_test, y_recent_test)
challenger_score = evaluate(challenger, X_recent_test, y_recent_test)

if challenger_score > champion_score + MARGIN:
    promote(challenger)  # keep the champion for rollback
```

(`evaluate` and `promote` are placeholders for your own pipeline.)

## Pitfalls

- **Stale evaluation set:** an old test set favors a model that matches the old world. Use recent labeled data.
- **Label delay:** the comparison can only be as fresh as the labels.
- **Selection noise:** many challengers compared on the same set raises the chance that one wins by luck. Use a fresh set for the final check.
- **Shadow shows no real impact:** its output is never used, so you cannot see how users react, and if the model's decisions influence future labels, shadow mode cannot show that effect.
- **Cost:** retraining and, in shadow mode, double serving.

## Related

- [[Model drift]]
- [[concept drift]]
- [[model performance monitoring]]
- [[Monitor Accuracy in Production Continuously]]
