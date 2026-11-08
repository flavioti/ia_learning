#QA #interview-question #model-evaluation #regression

## Question

You built a regression model that predicts the **expected sale price of a used car** from its attributes (make, model, year, mileage, condition, region, and so on). The price is used to set **starting prices and purchase offers** in an online used-car marketplace. On the test set it reaches an **[[MAE - Mean Absolute Error|MAE]] of €1,200** with an average price of about €15,000 (≈ 8%) and an **[[R-squared|R²]] of 0.93**. After launch, the business team says that some cars sell far below the prediction, others stay unsold, and the margin did not improve.

1. Why can a low MAE and a high R² coexist with a bad business result?
2. Which metrics and slices would you report instead?
3. How would you account for the fact that overpricing and underpricing do not cost the same?
4. Which evaluation mistakes (split, leakage, selection bias, time) would you rule out first?
5. How do you keep evaluating the model after it is live?

---

## What a strong answer covers

- **A single average error hides where the model fails.** Error usually grows with price, and rare or high-mileage cars are much harder. Report errors **by segment**, not only globally. See [[Evaluating regression model metrics]].
- **Pick the metric that matches the decision.** [[MAE - Mean Absolute Error|MAE]] is in euros, [[MAPE - Mean Absolute Percentage Error|MAPE]] is relative (a €1,200 error is not the same on a €5k and a €50k car), [[RMSE - Root Mean Squared Error|RMSE]] punishes large misses.
- **Errors are asymmetric.** Overestimating means buying too high or not selling; underestimating means losing deals or margin. Look at **bias** (signed error), not only absolute error.
- **A point estimate is not enough.** Prediction **intervals** (quantiles) tell the business how much to trust each price.
- **The split must imitate production:** time-based, and grouped by vehicle. See [[Backtest]] and [[K-Fold Cross-Validation]].
- **Rule out [[Data Leakage]] and selection bias:** only sold cars have a price.
- **The market moves.** See [[Distribution shift]], [[Model drift]] and [[concept drift]].

---

## Model answer

### 1. Why the offline numbers look good and the business does not

- **Averages hide the tails.** An [[MAE - Mean Absolute Error|MAE]] of €1,200 can be €500 on cheap cars and €3,500 on premium or rare ones. The expensive cars are exactly where one mistake costs the most.
- **[[R-squared]] rewards the easy part.** Price varies a lot across makes and years, so almost any model explains most of that variance. R² of 0.93 says little about whether the model beats a simple baseline within a segment.
- **Symmetric metrics for an asymmetric problem.** MAE counts +€1,200 and −€1,200 the same, but the business does not.
- **[[Selection bias]]:** the training data only has cars that **were sold**. Cars that stayed unsold (often the overpriced ones) have no label, so the model never learns from its worst mistakes.
- **[[Data Leakage|Leakage]]:** a feature available only after the sale (final number of bids, days to sell, final price of a similar lot) inflates every offline metric.
- **[[Distribution shift|Time shift]]:** prices follow season, interest rates, supply and new-model launches. A model validated on a random split of past data does not see this.

Illustrative breakdown (same model, same test set):

| Segment | Share of cars | MAE | MAPE | Bias (mean signed error) |
|---|---:|---:|---:|---:|
| Up to €8k | 30% | €500 | 9% | +€60 |
| €8k to €20k | 50% | €950 | 7% | +€100 |
| Above €20k | 15% | €2,600 | 9% | +€900 |
| Rare models / very high mileage | 5% | €3,500 | 18% | +€1,400 |
| **Overall** | **100%** | **≈ €1,200** | **≈ 8%** | **≈ +€270** |

The model is consistently **optimistic** (positive bias), and more so exactly in the segments that hurt the most.

### 2. Metrics and slices to report

| What | Why it is useful here |
|---|---|
| [[MAE - Mean Absolute Error\|MAE]] and [[RMSE - Root Mean Squared Error\|RMSE]] | Typical and worst-case error in euros; a large RMSE/MAE ratio signals heavy tails |
| [[MAPE - Mean Absolute Percentage Error\|MAPE]] (or median APE) | Comparable across cheap and expensive cars; median APE is robust to outliers |
| **Bias** (mean and median signed error) | Shows systematic over- or underpricing |
| **% of cars within ±5% / ±10% of the real price** | Easy for the business to read and to set targets on |
| Metrics **by slice**: price band, make, age, mileage, region, channel | Finds the segments where the model should not be trusted |
| **Interval coverage:** does the 80% interval contain the price 80% of the time? | Checks if the uncertainty is honest |
| **Baseline comparison** | Against a median-price lookup by make, model, year and mileage band, and against the current pricing rule or human appraisers |
| **Business impact:** margin, days to sell, unsold rate | What really matters in the end |

Always plot **predicted vs. actual** and the **residuals by price band**, instead of relying on a single number.

### 3. Handling asymmetric costs

1. Quantify both errors: cost of overpricing (unsold car, holding cost, price cuts, bought above market) versus cost of underpricing (lost margin, lost deal).
2. If they differ, train or evaluate with an **asymmetric loss**: **quantile (pinball) loss** for a chosen quantile, or a weighted absolute error. The decision then uses a **conservative quantile** (for example the 40th percentile for a purchase offer) instead of the mean.
3. Output **prediction intervals** (quantile regression or conformal prediction) and use the width as a confidence signal: a wide interval can route the car to a human appraiser.
4. Measure the final decision with an **expected-cost** function on the validation set, not only with MAE.

For outlier-heavy prices, a robust loss such as [[Huber Loss]] can also be considered.

### 4. Evaluation mistakes to rule out

- **Random split on time-ordered data:** train on the past and validate on the future (time-based split or rolling [[Backtest]]), because the market changes.
- **Same car in train and test:** a vehicle re-listed several times, or near-duplicate listings, makes the test set too easy. **Group the split by vehicle id (VIN) or by seller.**
- **[[Data Leakage|Leakage]]:** features known only after the sale or derived from the target; encodings or aggregates (for example average price per model) computed on the full dataset before the split.
- **Selection bias (survivorship):** unsold cars have no sale price. Evaluate on the population the model will actually see, and consider modeling the **probability of sale** together with the price.
- **Tuning on the test set:** keep a final hold-out that is used once.
- **One global number:** report **confidence intervals** (bootstrap) and slice metrics, because small segments have noisy errors.
- **Ignoring outliers or data errors:** typos in mileage or price (for example 1,000,000 km) distort MAE/RMSE; clean them in a documented way ([[Data Cleaning]]).

### 5. After deployment

- **Labels arrive with delay:** the real price is only known when the car is sold, possibly weeks later. Track meanwhile the input drift ([[Population Stability Index (PSI)|PSI]] on mileage, year, make mix) and the prediction distribution.
- **Compare with the current process** using [[champion and challenger]]: shadow mode first (predict but do not act), then an A/B test on margin and days to sell.
- **Monitor error by slice and bias over time**, not only the global MAE. Seasonal and macro changes show up as growing bias before they show up in the MAE.
- **Retrain on a schedule or on a trigger** (bias above a threshold, coverage of the intervals below target). See [[Monitor Accuracy in Production Continuously]] and [[Model drift]].
- **Feedback loop:** if the model sets the starting price, it also influences the final price. Keep a small share of cars priced by the old process (or randomized) to keep an unbiased signal.

---

## Common pitfalls (follow-up questions)

- "Why not just optimize R²?" It rewards explaining the easy variance, ignores asymmetric cost and does not tell if the model beats a simple baseline.
- "MAE improved but the margin did not. What happened?" The improvement may be in cheap cars, where it matters little, while the bias stayed in the expensive ones. Weight the error by the business value of each car.
- "How do you evaluate a model when 40% of the cars never sell?" Not with the sold subset only: model the sale probability, or evaluate on a population that includes unsold cars and compare against the asking price and the final outcome.
- "A new make appears with no history. What do you do?" Fall back to a baseline or a wide interval, and send it to human review (cold-start).

## Related

- [[Evaluating regression model metrics]]
- [[Model Evaluation]]
- [[quality/development/README|Model quality in development]]
- [[Your Model Scores 95% Offline but Fails in Production. How Do You Evaluate It Properly?]] (classification counterpart)
