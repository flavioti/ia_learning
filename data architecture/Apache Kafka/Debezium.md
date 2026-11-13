---
aliases:
  - Debezium
  - debezium
tags:
  - cdc
---
Debezium is an open-source **change data capture (CDC)** platform. It reads the **transaction log** of a database and turns every committed row change (insert, update, delete) into an event, usually published to Kafka. Because it reads the log and not the tables, it adds little load to the source database and does not miss deletes.

It is not part of Apache Kafka. It is a separate project that provides **source connectors** for [[data architecture/Apache Kafka/Connect.md|Kafka Connect]].

![[Debezium.excalidraw|1000]]

## How it works

1. The application writes to the database as usual.
2. The database appends every change to its transaction log.
3. The Debezium connector runs inside a Connect worker. On the first start it takes a **snapshot** of the existing rows (`op = r`), then **streams** the log changes from that point.
4. Each change becomes an event, passes through the optional SMTs and the converter, and is produced to a Kafka topic. There is **one topic per table**, named `<topic.prefix>.<schema>.<table>`, and the key is the row's primary key.
5. The connector saves its position in the log (for example the Postgres LSN) in `connect-offsets`, so it resumes where it stopped after a restart.

## Change event

| Field | Meaning |
| --- | --- |
| `before` | Row state before the change (`null` for inserts) |
| `after` | Row state after the change (`null` for deletes) |
| `op` | `c` create, `u` update, `d` delete, `r` snapshot read |
| `source` | Where it came from: database, table, log position, transaction id |
| `ts_ms` | When the connector processed the event |

A delete produces an event with `op = d`, followed by a **tombstone** (same key, `null` value) so compacted topics can drop the key.

## Supported sources

| Database | Log it reads |
| --- | --- |
| PostgreSQL | WAL, through logical decoding (`pgoutput`) and a replication slot |
| MySQL, MariaDB | Binlog |
| SQL Server | CDC tables |
| Oracle | LogMiner or XStream |
| MongoDB | Change streams |

## Installing and running

- **Plugin on Kafka Connect:** the most common way. The connector is a set of JARs placed in the workers' `plugin.path`, or you use the `quay.io/debezium/connect` image that already includes them.
- **Debezium Server:** a standalone process that sends events to Kafka, Pulsar, Kinesis, Google Pub/Sub and others, without Kafka Connect.
- **Embedded engine:** a Java library that runs inside your own application.

## Example connector (PostgreSQL)

Created through the Connect REST API (`POST /connectors`):

```json
{
  "name": "orders-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "db.internal",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${file:/secrets/db.properties:password}",
    "database.dbname": "shop",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "topic.prefix": "dbserver",
    "table.include.list": "public.orders,public.customers"
  }
}
```

The password comes from a config provider, not from the JSON itself.

## Pitfalls

- **Replication slot growth (Postgres):** if the connector is stopped or stuck, the database keeps the WAL the slot still needs, and the disk can fill up. Monitor the slot lag and drop slots you no longer use.
- **Before values (Postgres):** `before` is only complete with `REPLICA IDENTITY FULL` on the table. The default sends just the key columns on updates and deletes.
- **Initial snapshot:** on large tables it takes time and adds read load. Plan it, or use incremental snapshots.
- **Schema changes:** an `ALTER TABLE` changes the event schema. Use a schema registry and compatible changes so consumers keep working.
- **Delivery:** at-least-once. After a crash an event can be delivered twice, so consumers and sinks should be idempotent (upsert by key).
- **Ordering:** guaranteed per key, within a partition, not across tables or partitions.

## Links

- [[data architecture/Apache Kafka/Debezium Installation and Configuration.md|Debezium Installation and Configuration]]

## Related

- [[data architecture/CDC.md|CDC]]
