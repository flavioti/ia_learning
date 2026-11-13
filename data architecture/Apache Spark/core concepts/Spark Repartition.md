---
aliases:
  - Repartition
  - repartition
  - Spark Repartition
  - repartitionByRange
tags:
  - data-engineering
  - spark
  - partitioning
  - performance
description: What repartition does in Apache Spark (a full shuffle that redistributes a DataFrame into a chosen number of partitions), its variants, how it differs from coalesce, and when to use it.
---
**`repartition`** changes how a DataFrame is split into **partitions**. It does a **full shuffle**: every row can move to a different partition, so the result is a new set of partitions of balanced size, by a number you choose, by one or more columns, or both. Because one task processes one partition, the number and size of partitions decide the **parallelism** of the next stages.

>[!tip] `repartition` is a **wide** transformation. It costs a shuffle, so use it only when the partitions are wrong (too few, too many, too big, uneven) and the gain is worth that cost.

## Variants

| Call | Strategy | Number of partitions |
|---|---|---|
| `df.repartition(n)` | **Round-robin**: rows are spread evenly | `n` |
| `df.repartition(n, "col")` | **Hash** of the column(s): same key, same partition | `n` |
| `df.repartition("col")` | **Hash** of the column(s) | `spark.sql.shuffle.partitions` (AQE may coalesce it) |
| `df.repartitionByRange(n, "col")` | **Range**: sorted ranges of the column, found by sampling | `n` |

```python
df = spark.read.parquet("s3://bucket/raw/orders/")
print(df.rdd.getNumPartitions())          # see the current number

by_count = df.repartition(200)            # even sizes, no key
by_key   = df.repartition(200, "customer_id")   # same customer, same partition
by_range = df.repartitionByRange(200, "order_date")  # ordered ranges
```

In SQL, use hints: `/*+ REPARTITION(200) */`, `/*+ REPARTITION(200, customer_id) */`, `/*+ REPARTITION_BY_RANGE(200, order_date) */` and, with AQE, `/*+ REBALANCE */`.

## Repartition vs coalesce

| | `repartition(n)` | `coalesce(n)` |
|---|---|---|
| Shuffle | **Full shuffle** | No full shuffle (merges neighbor partitions) |
| Direction | Increase or decrease | **Only decrease** |
| Balance | Even sizes | Can leave uneven sizes |
| Cost | Higher | Lower |

Trap: `coalesce(1)` before a write reduces the parallelism of the **whole stage** before it, because the narrow merge is pushed up. `repartition(1)` keeps the upstream work parallel and shuffles only at the end.

## When to use it

- **Too few partitions:** a big file read in a few tasks, or a join that left few partitions. Increase them to use all cores.
- **Too many small partitions:** after a heavy filter, compact them before the next stage.
- **Uneven partitions:** rebalance them after a skewed step, with `repartition(n)` (round-robin).
- **Before a wide operation by key:** `repartition("key")` co-locates the rows of the same key for a later `groupBy` or `join` on that key.
- **Before a write:** control the **number and size of the output files**, to avoid the small files problem.

```python
# One group of files per date, a few files each, instead of thousands of tiny files
(
    df.repartition("order_date")
      .write.partitionBy("order_date")
      .mode("overwrite")
      .parquet("s3://bucket/gold/orders/")
)
```

`partitionBy` on the writer defines the **folders** on disk. `repartition` defines how the rows are grouped in memory **before** they are written. They solve different problems and often work together.

## How many partitions?

- A common target is **about 100 to 200 MB per partition**, which gives tasks of seconds to a few minutes.
- A starting point is **2 to 4 times the total cores** of the cluster, then adjust.
- With **AQE** on (`spark.sql.adaptive.enabled=true`), Spark can coalesce small shuffle partitions by itself, so avoid a hard-coded number that fits only one data size.

## Pitfalls

- Repartitioning by a **skewed column**: a hot key still lands in one partition. Use round-robin `repartition(n)` or **salt** the key.
- Repartitioning **early and often** for no reason: each call is a full shuffle.
- Using `repartition(n)` to **reduce** partitions when `coalesce(n)` is enough and the sizes are already balanced.
- Hard-coding `n` for data that grows, so partitions become too big and the job [[data architecture/Apache Spark/memory and performance/Spark Spills.md|spills]].
- Expecting a repartition to **sort** the data. Only `repartitionByRange` creates ordered ranges, and the rows inside a partition are still unsorted.
- Calling `repartition` on a very small DataFrame, where the shuffle costs more than it saves.

## Interview questions

- What does `repartition` do, and why is it a wide transformation?
- What is the difference between `repartition` and `coalesce`?
- What is the difference between `repartition("col")`, `repartition(n, "col")` and `repartitionByRange`?
- How do you choose the number of partitions?
- How do you avoid the small files problem when writing partitioned data?
- Why can `coalesce(1)` slow down the whole stage before it?
- How does `repartition` relate to data skew?

## Related

- [[data architecture/Apache Spark/memory and performance/Spark Spills.md|Spark Spills]]
- [[data architecture/Apache Spark/sql and optimization/Spark Joins.md|Spark Joins]]
