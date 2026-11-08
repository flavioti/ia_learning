---
aliases:
  - Point-in-time correctness
  - Point-in-time join
  - As-of join
---
#concept #feature-store #data-leakage

Classical machine learning: as the model must be trained with historical facts, an [[Offline Feature Store]] must ensure that the data is correctly stored and that each training example sees only what was known **at that moment**.

## Point-in-time

**Point-in-time correctness** means that, for every training example, each feature has the value it had **at the time of the prediction** (the label's timestamp), and never a value from after it.

The tool is the **point-in-time join** (also called an **as-of join**): for each row of the label table, it picks the **most recent feature value that is not later than the row's timestamp**.

>[!tip] Ask for every feature: "What would the system have known at that exact moment?" A feature value that is not available at that moment must not appear in the training row.

## What problems point-in-time solves?

| Problem | What happens without point-in-time |
|---|---|
| **Future data in training** | A join takes the latest value of a feature (for example today's balance) for a label from months ago, so the model trains with information from the future |
| **Training-serving mismatch** | The model sees "perfect" features in training and only the real, older ones in production, so the live performance is worse than the offline one. See [[Training-Serving Skew]] |
| **Irreproducible training sets** | Rebuilding the dataset next week gives different numbers, because the feature tables changed. A point-in-time dataset can be rebuilt exactly |
| **Late-arriving data** | A value for yesterday that was only stored today looks available in the past. The join must use when the value was **available**, not only when the event happened |
| **Wrong offline evaluation** | The metrics look excellent because of leakage, and the model disappoints after deployment |

## Data Leakage

Without point-in-time correctness the result is **temporal leakage**, one of the main causes of [[Data Leakage]]: the model trains on the future to predict the past. It is dangerous because the model looks great in evaluation and fails in production.

A naive join on the entity key alone is the typical mistake. A random train and test split does not fix it, because the leaked feature values are already inside every training row. Point-in-time correctness also does not replace a time-based split of the data: use both. See [[train dataset and test dataset]].

## Example

One user, two labels (an outcome observed at a given date) and a feature table that changes over time. The feature is an account balance.

| Label table | | |
|---|---|---|
| user | label time | label |
| 1 | 2024-03-10 | 1 |
| 1 | 2024-03-20 | 0 |

| Feature table (user 1) | |
|---|---|
| feature time | balance |
| 2024-03-01 | 100 |
| 2024-03-15 | 250 |
| 2024-03-25 | 400 |

| Label time | Naive join (latest value) | Point-in-time join |
|---|---|---|
| 2024-03-10 | 400 (from 2024-03-25, **the future**) | **100** (from 2024-03-01) |
| 2024-03-20 | 400 (from 2024-03-25, **the future**) | **250** (from 2024-03-15) |

With pandas, `merge_asof` does the point-in-time join. Both tables must be sorted by time:

```python
import pandas as pd

labels = pd.DataFrame({
    "user": [1, 1],
    "label_time": pd.to_datetime(["2024-03-10", "2024-03-20"]),
    "label": [1, 0],
}).sort_values("label_time")

features = pd.DataFrame({
    "user": [1, 1, 1],
    "feature_time": pd.to_datetime(["2024-03-01", "2024-03-15", "2024-03-25"]),
    "balance": [100, 250, 400],
}).sort_values("feature_time")

training = pd.merge_asof(
    labels, features,
    left_on="label_time", right_on="feature_time",
    by="user",                    # match the same entity
    direction="backward",         # latest value at or before the label time
)
# balance: 100 for the first label, 250 for the second
```

The result is the **Point-in-time join** column of the table above. This example was run with pandas, and the SQL version (a window function on the same data) gives the same result. See the SQL in [[Offline Feature Store]].

## Two clocks: event time and availability time

A correct join often needs two timestamps per feature value:

| Timestamp | Meaning |
|---|---|
| **Event time** | When the fact happened or was valid (for example the transaction date) |
| **Created or ingestion time** | When the value became available in the system (for example when the batch loaded it) |

Use the **availability time** when the data arrives with a delay (for example a nightly batch, or a payment that is settled days later). Joining on event time alone includes values that the production system did not have yet. Many feature stores let you set a time-to-live, so that a value that is too old is treated as missing.

## Where it is implemented

- **[[Offline Feature Store]]:** stores the full history of every feature and serves training sets through point-in-time joins (for example `get_historical_features` in Feast, or the training set functions of managed feature stores). The online store serves only the latest values at prediction time, so the two stores together keep training and serving consistent.
- **Data lakes and warehouses:** table formats with time travel (for example Delta Lake, Apache Iceberg and warehouse "as of" queries) can read a table as it was at a past time. `ASOF JOIN` exists in several SQL engines.
- **Your own pipeline:** `merge_asof` in pandas, or a window query that takes the latest row per entity not later than the label time.

## Checklist

- Every training row has a **label time** (the moment of the prediction)
- Every feature is joined **as of that time**, never with the latest value
- Late-arriving data is handled with an availability timestamp
- Aggregations (for example "purchases in the last 30 days") only use events **before** the label time
- The split between train and test is by time (older labels for training, newer ones for testing)
- The training set can be rebuilt exactly later, because the feature history is kept (no overwritten rows)
- Compare the offline metric with the live one after deployment. A large gap is a warning sign

## Pitfalls

- Joining on the entity key only, which takes the latest feature value
- Overwriting feature tables in place, which destroys the history needed for point-in-time joins
- Timestamps in different time zones or with different precision between tables
- Windowed aggregations that include the label event itself or later events
- Using the event time when the data arrives late
- Assuming that a random split is enough to prevent temporal leakage

## Related

- [[Offline Feature Store]]
- [[Data Leakage]]
- [[Training-Serving Skew]]
- [[Feature Engineering]]
- [[train dataset and test dataset]]
- [[Ground Truth]]
