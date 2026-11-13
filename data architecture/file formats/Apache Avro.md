---
aliases:
  - Avro
  - Apache Avro
  - Avro file format
tags:
  - data-engineering
  - file-formats
  - avro
  - schema-evolution
  - kafka
description: What Apache Avro is, a row-based binary data format whose schema travels with the data, how an Avro file is built, how schema evolution works, and where it fits in data pipelines, especially with Kafka.
---
**Apache Avro** is a **row-based, binary data serialization format** that always comes with a **schema**. The schema is written in **JSON**, and it describes the fields and types of every record. Avro was created inside the Apache Hadoop project, and it is now widely used for **events, streaming and data exchange**, where producers and consumers change over time.

>[!tip] Avro is built to **move and write data** (one record at a time, schema first). For analytical reads of a few columns, see [[data architecture/file formats/Apache Parquet.md|Apache Parquet]].

## The schema

An Avro schema is a JSON document. A record with a nullable field looks like this:

```json
{
  "type": "record",
  "name": "Order",
  "namespace": "com.example.sales",
  "fields": [
    {"name": "order_id", "type": "long"},
    {"name": "customer_id", "type": "string"},
    {"name": "amount", "type": {"type": "bytes", "logicalType": "decimal", "precision": 12, "scale": 2}},
    {"name": "created_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "coupon", "type": ["null", "string"], "default": null}
  ]
}
```

- **Primitive types:** `null`, `boolean`, `int`, `long`, `float`, `double`, `bytes`, `string`.
- **Complex types:** `record`, `enum`, `array`, `map`, `union`, `fixed`.
- **Union** is how Avro models an optional value: `["null", "string"]`. For a `null` default, `null` must be the first type of the union.
- **Logical types** add meaning to a base type: `decimal`, `date`, `timestamp-millis`, `uuid` and others.

## How an Avro file is built

An Avro **object container file** has:

1. A **header** with a magic marker, the **schema** (JSON), the **compression codec**, and a random **sync marker**.
2. A series of **data blocks**. Each block holds a count of records, the serialized records (compressed with the codec), and the sync marker.

```text
[ header: magic | schema | codec | sync ]
[ block: n records | data | sync ]
[ block: n records | data | sync ]
...
```

- The record data is **compact**: it has no field names or tags, only the values in schema order. So the reader needs the **schema** to decode it, and a file carries it in the header.
- The **sync markers** let a reader find the start of a block, so a big file is **splittable** and processed in parallel.
- **Codecs:** `null` (none), `deflate`, `snappy`, `bzip2`, `xz` and `zstandard`, depending on the library.

## Schema evolution

Avro resolves two schemas when it reads: the **writer schema** (used when the data was written) and the **reader schema** (what the application expects now). Fields are matched **by name**.

| Change | Allowed? | How |
|---|---|---|
| Add a field | Yes | Give it a **default value**, so old data can still be read with the new schema |
| Remove a field | Yes | The reader ignores it. For old readers, the field needs a default |
| Rename a field | Yes | Use **aliases** in the reader schema |
| Change a type | Only some promotions | For example `int` to `long`, `float` or `double`. Others break |
| Reorder fields | Yes | Matching is by name |

With **Kafka**, the schemas live in a **Schema Registry**, and each message carries a small **schema id**, not the whole schema. The registry checks **compatibility** when a producer registers a new version:

| Mode | Guarantee |
|---|---|
| **BACKWARD** | A consumer with the new schema can read old data (the usual default) |
| **FORWARD** | A consumer with the old schema can read new data |
| **FULL** | Both |
| **NONE** | No check |

## Where Avro fits

- **Kafka messages**, with a Schema Registry, so producers and consumers evolve their schemas safely.
- The **landing or raw layer** of a pipeline, where the source schema changes and records arrive in order.
- **Data exchange between services and teams**, as a typed contract.
- **Write-heavy workloads**, because appending a record is cheap.
- Whenever you read **whole records**.

Avro is a **poor fit** for analytics on a few columns of a large table: it has **no column pruning** and **no statistics** to skip data, so a query reads full rows.

## Using Avro

```python
# Python, with the fastavro library
import json
from fastavro import writer, reader, parse_schema

schema = parse_schema(json.load(open("order.avsc")))
records = [{"order_id": 1, "customer_id": "c-10", "amount": 10, "created_at": 0, "coupon": None}]

with open("orders.avro", "wb") as out:
    writer(out, schema, records, codec="snappy")

with open("orders.avro", "rb") as f:
    for record in reader(f):
        print(record)
```

```python
# Spark: needs the spark-avro module, an external package that matches your Spark version
events = spark.read.format("avro").load("s3://bucket/raw/events/")
events.write.format("avro").save("s3://bucket/raw/events_copy/")
```

## Best practices

- Define a **default** for every new field, so the schema stays compatible.
- Use **unions with `null` first** for optional fields.
- Keep schemas in a **Schema Registry** or in version control, and choose a **compatibility mode** on purpose.
- Use **logical types** (decimal, timestamp) instead of strings.
- Compress blocks with **Snappy** or **Zstandard**.
- Convert Avro to a **columnar format** for analytics.

## Common pitfalls

- Adding a field **without a default**, which breaks old readers or old data.
- Using Avro for **analytical queries**, so every query reads full rows.
- Changing a field **type** in an incompatible way.
- Forgetting that the **reader needs the writer schema** to decode data without the file header (for example a bare Kafka payload).
- Mixing `null` as a type and as a default in the wrong order of a union.
- Using strings for dates and decimals.

## Interview questions

- What is Avro, and how is it different from JSON or CSV?
- Why does Avro store the schema with the data?
- What is the difference between the writer schema and the reader schema?
- How do you evolve an Avro schema without breaking consumers?
- What does a Schema Registry do, and what are BACKWARD and FORWARD compatibility?
- Why is Avro a good fit for Kafka and a poor fit for analytics?
- How is an Avro file made splittable?

## Related

- [[data architecture/file formats/Apache Parquet.md|Apache Parquet]]
- [[data architecture/data engineering/Schema Evolution.md|Schema Evolution]]
- [[data architecture/Apache Kafka/Kafka.md|Kafka]]
- [[data architecture/Apache Spark/Apache Spark.md|Apache Spark]]
