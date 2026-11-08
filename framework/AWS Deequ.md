#data-quality #spark #aws #framework

An AWS open-source framework for [[data quality]]: "unit tests for data".
Ideal for [[Apache Spark]] and [[AWS S3]]

## What it is

Deequ is a library built on top of [[Apache Spark]] (written in Scala) that lets you define data quality constraints declaratively and verify them on large datasets. Because it runs as Spark jobs, checks scale to billions of rows. **PyDeequ** is the Python wrapper.

## Main components

| Component | Purpose |
| --- | --- |
| **Analyzers** | Compute data metrics (size, completeness, uniqueness, mean, etc.) |
| **Checks / Verification Suite** | Declare constraints and verify them against the data |
| **Constraint Suggestion** | Automatically propose constraints by profiling the data |
| **Metrics Repository** | Store metrics per run to compare over time |
| **Anomaly Detection** | Detect unusual changes in metrics between runs (e.g. row count drops) |

## Typical checks

| Dimension | Example constraint |
| --- | --- |
| Completeness | `isComplete("id")` or `hasCompleteness("email", _ >= 0.95)` |
| Uniqueness | `isUnique("id")` |
| Validity | `isContainedIn("status", Array("A", "B"))` |
| Range | `isNonNegative("amount")` |
| Volume | `hasSize(_ >= 1000)` |

## Example (PyDeequ)

```bash
pip install pydeequ
export SPARK_VERSION=3.5   # must match the installed Spark version
```

```python
from pyspark.sql import SparkSession
import pydeequ
from pydeequ.checks import Check, CheckLevel
from pydeequ.verification import VerificationSuite, VerificationResult

spark = (
    SparkSession.builder
    .config("spark.jars.packages", pydeequ.deequ_maven_coord)
    .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
    .getOrCreate()
)

df = spark.read.parquet("s3a://my-bucket/orders/")

check = Check(spark, CheckLevel.Error, "integrity checks")

result = (
    VerificationSuite(spark)
    .onData(df)
    .addCheck(
        check.hasSize(lambda x: x >= 1)
        .isComplete("order_id")
        .isUnique("order_id")
        .isContainedIn("status", ["NEW", "PAID", "CANCELLED"])
        .isNonNegative("amount")
    )
    .run()
)

VerificationResult.checkResultsAsDataFrame(spark, result).show()
```

`CheckLevel.Error` fails the verification when a constraint is violated; `CheckLevel.Warning` only reports it.

## Where it fits

- Runs in the ingestion/transformation stage, owned by the **Data Engineer** (see [[ML Lifecycle]]).
- Acts as a gate in pipelines: fail or quarantine a batch before it reaches feature engineering or training.
- Metrics repository + anomaly detection support monitoring of data drift over time.

## Pros and cons

| Pros | Cons |
| --- | --- |
| Scales with Spark | Requires a Spark cluster/runtime |
| Declarative, readable constraints | Scala-first; PyDeequ lags behind in features |
| Metrics history and anomaly detection | Version coupling between PyDeequ and Spark |

## Alternatives

[[Great expectations]]
