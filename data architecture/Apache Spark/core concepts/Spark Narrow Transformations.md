---
aliases:
  - Narrow transformation
  - Narrow transformations
  - Spark Narrow Transformation
  - Narrow dependency
tags:
  - data-engineering
  - spark
  - transformations
  - performance
description: What a narrow transformation is in Apache Spark (an operation where each output partition depends on at most one input partition, so it needs no shuffle), which operations are narrow, how Spark pipelines them in one stage, and their limits.
---
A **narrow transformation** is an operation where each output partition depends on **at most one input partition**, or on a small fixed group of partitions. The task works on its own partition, inside its own executor, so **no data moves across the network** and there is **no shuffle**. Spark chains consecutive narrow transformations into the **same stage** and runs them together in one pass over the data.

>[!tip] If `df.explain()` shows no `Exchange` between two steps, they are narrow and run in the same stage.

## Narrow vs wide

| | Narrow | Wide |
|---|---|---|
| Input needed per output partition | One input partition | Many input partitions |
| Data movement | None | Shuffle across the network |
| Stage | Same stage (pipelined) | New stage after the shuffle |
| Cost | Cheap | Disk, network and serialization |
| Failure recovery | Recompute one partition | May recompute many partitions |

See [[data architecture/Apache Spark/core concepts/Spark Wide Transformations.md|Spark Wide Transformations]] for the other side.

## Common narrow operations

| Operation | Notes |
|---|---|
| `select`, `selectExpr`, `withColumn`, `drop`, `withColumnRenamed` | Work row by row |
| `filter`, `where` | Drop rows inside each partition |
| `map`, `flatMap`, `mapPartitions` (RDD) | Transform each record, or each whole partition |
| `explode` | One row can become many, but the rows stay in the same partition |
| `cast`, built-in column functions | Row-level expressions |
| `union` | Concatenates the partitions of both DataFrames, without a shuffle |
| `coalesce(n)` | Merges neighbor partitions without a full shuffle. See [[data architecture/Apache Spark/core concepts/Spark Repartition.md|Spark Repartition]] |
| `sample` | Samples inside each partition |
| **Broadcast join** (the big side) | The big side is not shuffled. Each partition joins the broadcast copy locally |

A join between two datasets that are **already partitioned the same way** by the join key (for example bucketed tables) can also avoid the shuffle.

## Pipelining: one stage, one pass

Spark does not run `filter`, then `select`, then `withColumn` as three separate passes. It **pipelines** them: each row goes through the whole chain before the next row is read. With **whole-stage code generation**, Spark compiles the chain into one tight loop.

```python
result = (
    orders
    .filter(F.col("status") == "paid")                       # narrow
    .select("customer_id", "amount", "created_at")           # narrow
    .withColumn("order_date", F.to_date("created_at"))       # narrow
)
result.explain()
# == Physical Plan ==
# *(1) Project [...]
# +- *(1) Filter (status = paid)
#    +- *(1) FileScan parquet [...]      <- one stage, no Exchange
```

The `*(1)` marks operators in the same whole-stage code generation block, and there is **no `Exchange`**.

## Why it is cheap

- **No network and no shuffle files.** Data stays in the executor.
- **Streaming of rows.** Narrow operations do not need to keep many rows in memory, so they rarely [[data architecture/Apache Spark/memory and performance/Spark Spills.md|spill]].
- **Cheap recovery.** If a task fails, Spark recomputes **only that partition** from its parent partition.
- **Parallelism is simple:** one task per partition, all independent.

## What narrow does not mean

Narrow means **no shuffle**. It does not always mean **cheap**:

- **Python UDFs** are narrow, but they move rows between the JVM and Python, and they block optimizations.
- **`explode`** or a `flatMap` that multiplies rows can create very large partitions.
- **`mapPartitions`** can hold a whole partition in memory if you build a list from the iterator, which can cause an out of memory error. See [[data architecture/Apache Spark/common errors/Spark OutOfMemoryError.md|Spark OutOfMemoryError]].
- **Wide rows** (many columns, big strings) make every narrow step heavier.
- **Few partitions** limit the parallelism, no matter how cheap each step is.
- **`coalesce(1)` before a write** pushes the narrow merge up and can run the whole stage with one task.

## Using narrow transformations well

- **Filter and select early.** Catalyst pushes filters and column pruning down by itself, but write the query clearly.
- **Prefer built-in functions** to Python UDFs, so Catalyst can still optimize.
- **Use `mapPartitions`** when each partition needs a one-time setup (for example a client), and process the iterator lazily.
- **Keep the plan narrow as long as you can,** and put the wide operation after the data has been reduced.
- **Check the plan:** an unexpected `Exchange` means a narrow step became wide (for example a changed partitioning).

## Pitfalls

- Believing narrow transformations are always fast.
- Using `coalesce` to increase partitions. It can only decrease them.
- Building a Python list inside `mapPartitions` for a big partition.
- Using a UDF for something a built-in function does.
- Calling `collect()` after narrow steps, which brings everything to the driver.

## Interview questions

- What is a narrow transformation, and how does it differ from a wide one?
- Why are narrow transformations pipelined into one stage?
- Which operations are narrow, and is `union` narrow or wide?
- Why is recovery from a failure cheaper for narrow dependencies?
- Is a broadcast join narrow or wide, and why?
- Why is a Python UDF narrow but still expensive?
- How can you check in `explain()` that two steps are in the same stage?

## Related

- [[data architecture/Apache Spark/core concepts/Spark Wide Transformations.md|Spark Wide Transformations]]
