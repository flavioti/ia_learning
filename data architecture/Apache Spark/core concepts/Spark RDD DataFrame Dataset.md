---
description: Comparison of the three Spark data abstractions (RDD, DataFrame and Dataset), covering schema, type safety, optimizer support, memory format, language support and when to use each one. Child of Apache Spark, used to choose an API and for interview questions.
aliases:
  - RDD vs DataFrame vs Dataset
  - Spark data abstractions
tags:
  - spark
  - rdd
  - dataframe
  - dataset
  - interview
---
# Spark RDD, DataFrame and Dataset

All three are abstractions for distributed data in Spark. They differ by **how much Spark knows about the structure of the data**, which determines how much it can optimize. See [[data architecture/Apache Spark/Apache Spark|Apache Spark]] and [[data architecture/Apache Spark/core concepts/Spark RDD|Spark RDD]].

## Comparison

| Criterion                   | RDD                             | DataFrame                      | Dataset (not available in PySpark)   |
| --------------------------- | ------------------------------- | ------------------------------ | ------------------------------------ |
| Structure                   | Objects with no schema          | Rows with named, typed columns | Typed objects (case class, JavaBean) |
| Type safety                 | Compile time                    | Runtime (`Row`)                | Compile time                         |
| Catalyst optimizer          | No                              | Yes                            | Yes                                  |
| In-memory format (Tungsten) | No, JVM objects                 | Yes, binary format             | Yes, binary format                   |
| Languages                   | Scala, Java, Python, R          | Scala, Java, Python, R         | Scala and Java                       |
| Typical use                 | Custom logic, unstructured data | Most analytics and SQL work    | Typed pipelines in Scala or Java     |

## RDD

A low-level API. You write functions such as `map`, `filter` and `reduceByKey`. Because Spark does not know what is inside the objects, it cannot reorder filters, prune columns or choose a join strategy.

- **Fault tolerance:** Spark recomputes lost partitions from the **lineage**, the chain of transformations.
- **When to use:** full control over execution, data without a structure, or operations that do not fit SQL.

```scala
val rdd = sc.textFile("pedidos.csv")
  .map(_.split(","))
  .filter(_(2).toDouble > 100)
```

## DataFrame

Data organized as a table, with named columns and a schema. Because Spark knows the structure, Catalyst can apply filter pushdown, column pruning and choose joins such as `BroadcastHashJoin`. Tungsten stores the data in a compact binary format.

- **When to use:** almost always. It is the default API and the one with the best performance.
- **In PySpark**, this is the main data model.

```scala
val df = spark.read.option("header", true).csv("pedidos.csv")
  .filter($"valor" > 100)
```

## Dataset

Adds a **compile-time type** to the DataFrame model. A `Dataset[Pedido]` lets the compiler check that `p.valor` exists and has the right type. A DataFrame is a `Dataset[Row]`, so both use the same optimizer.

- **When to use:** Scala or Java pipelines that benefit from type checking.
- **Python has no typed Dataset**, because the language is dynamically typed.

```scala
case class Pedido(id: Long, valor: Double)

val ds = spark.read.option("header", true).csv("pedidos.csv")
  .as[Pedido]
  .filter(_.valor > 100)
```

## Cost of each abstraction

- **RDD:** Spark does not optimize the logic inside the functions, and the data is stored as Java objects, which uses more memory and CPU for serialization.
- **DataFrame:** the optimizer works on the plan, but Python functions (UDFs) break that optimization. Prefer built-in functions. See [[data architecture/Apache Spark/sql and optimization/Spark UDFs|Spark UDFs]].
- **Dataset:** lambda functions (`_.valor > 100`) are black boxes for Catalyst. A filter written as a column expression is optimized, a lambda is not.

## Pitfalls

- **Mixing APIs without need** breaks optimization. A `.rdd` in the middle of a DataFrame pipeline takes the plan away from Catalyst.
- **A Dataset with lambdas** can be slower than a DataFrame using `col()`, even though it is typed.
- **`Row` in a DataFrame** has no type checking. Wrong column names only show up at execution time.

## Interview question

"What is the difference between RDD, DataFrame and Dataset?"

Short answer: an RDD is an object model with no schema, full control and no optimization. A DataFrame has a schema and goes through Catalyst and Tungsten, so it is the default. A Dataset is a DataFrame with a compile-time type, available only in Scala and Java. In Python, use DataFrame.

## Related

- [[data architecture/Apache Spark/core concepts/Spark RDD|Spark RDD]]
- [[data architecture/Apache Spark/sql and optimization/Catalyst|Catalyst]]
- [[data architecture/Apache Spark/sql and optimization/Spark UDFs|Spark UDFs]]
