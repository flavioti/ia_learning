---
description: Index of the file format notes for data pipelines and data lakes, with Apache Avro (row-based, schema first) and Apache Parquet (columnar).
tags:
  - data-engineering
  - file-formats
  - index
---
# File formats

Notes about the file formats used to store and move data. Each format has its own note.

| Format | Layout | Best for |
|---|---|---|
| [[data architecture/file formats/Apache Avro.md\|Apache Avro]] | Row-based, schema stored with the data | Events, streaming (Kafka), ingestion, schema evolution |
| [[data architecture/file formats/Apache Parquet.md\|Apache Parquet]] | Columnar | Analytics on a lake or lakehouse, queries on a few columns |

## Links

- [[data architecture/file formats/Apache Avro.md|Apache Avro]]
- [[data architecture/file formats/Apache Parquet.md|Apache Parquet]]
