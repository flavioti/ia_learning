---
aliases:
  - Install Debezium
  - Debezium setup
tags:
  - cdc
---
How to install and configure Debezium as a **source connector on Kafka Connect**, using PostgreSQL as the example. The steps are the same for other databases, only the database setup and a few connector properties change.

## Prerequisites

- A running Kafka cluster that the Connect workers can reach.
- A Kafka Connect cluster in **distributed mode** (see `connect-distributed.sh`), with a Java runtime that matches the Debezium version. Check the compatibility matrix on the Debezium site before choosing versions.
- A source database with access to its transaction log, and an account for the connector.
- Network access from the workers to both the brokers and the database.

## Step 1: Prepare the database (PostgreSQL)

Set these in `postgresql.conf` and restart the server:

```properties
wal_level = logical
max_wal_senders = 10
max_replication_slots = 10
```

Create a dedicated user for the connector and give it the minimum it needs:

```sql
CREATE ROLE debezium WITH LOGIN REPLICATION PASSWORD '<password>';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
GRANT CREATE ON DATABASE shop TO debezium;  -- lets the connector create its publication
```

Optional, but recommended for tables where you need the full `before` row:

```sql
ALTER TABLE public.orders REPLICA IDENTITY FULL;
```

The `pg_hba.conf` file must also allow the `debezium` user to open a replication connection from the worker hosts.

### Other databases

| Database | What to enable |
| --- | --- |
| MySQL, MariaDB | `binlog_format=ROW`, `binlog_row_image=FULL`, a unique `server-id`. The user needs `SELECT`, `RELOAD`, `SHOW DATABASES`, `REPLICATION SLAVE`, `REPLICATION CLIENT`. The connector also needs `schema.history.internal.kafka.*` properties, because it stores DDL history in a Kafka topic |
| SQL Server | Enable CDC on the database and on each captured table (`sys.sp_cdc_enable_db`, `sys.sp_cdc_enable_table`) |
| MongoDB | A replica set or sharded cluster, since it reads change streams |
| Oracle | Archive log mode and supplemental logging, with LogMiner or XStream |

## Step 2: Install the connector plugin

The connector is a `.tar.gz` of JARs that must be in each worker's `plugin.path`.

### Option A: Manual install on the workers

```bash
VERSION=<debezium-version>
curl -O https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/$VERSION/debezium-connector-postgres-$VERSION-plugin.tar.gz

sudo mkdir -p /opt/kafka/plugins
sudo tar -xzf debezium-connector-postgres-$VERSION-plugin.tar.gz -C /opt/kafka/plugins
```

In `connect-distributed.properties`:

```properties
plugin.path=/opt/kafka/plugins
```

Do this on **every** worker, then restart them. Verify the plugin is loaded:

```bash
curl -s http://localhost:8083/connector-plugins | grep -i debezium
```

### Option B: Debezium container image

The `quay.io/debezium/connect` image already includes the Debezium connectors. Docker Compose, assuming a Kafka broker reachable as `kafka:9092`:

```yaml
services:
  postgres:
    image: quay.io/debezium/postgres:16   # wal_level=logical already set
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: shop

  connect:
    image: quay.io/debezium/connect:<debezium-version>
    ports:
      - "8083:8083"
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: connect-cluster
      CONFIG_STORAGE_TOPIC: connect_configs
      OFFSET_STORAGE_TOPIC: connect_offsets
      STATUS_STORAGE_TOPIC: connect_statuses
```

All workers with the same `GROUP_ID` form one Connect cluster.

### Option C: Kubernetes with Strimzi

Strimzi builds an image with the plugin for you:

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: debezium-connect
  annotations:
    strimzi.io/use-connector-resources: "true"
spec:
  replicas: 2
  bootstrapServers: my-cluster-kafka-bootstrap:9092
  build:
    output:
      type: docker
      image: registry.example.com/debezium-connect:latest
    plugins:
      - name: debezium-postgres
        artifacts:
          - type: tgz
            url: https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/<debezium-version>/debezium-connector-postgres-<debezium-version>-plugin.tar.gz
```

With the annotation, you create connectors as `KafkaConnector` resources instead of calling the REST API.

## Step 3: Keep secrets out of the config

Enable a config provider on the workers (`connect-distributed.properties`):

```properties
config.providers=file
config.providers.file.class=org.apache.kafka.common.config.provider.FileConfigProvider
```

Then reference the value in the connector config as `${file:/secrets/db.properties:password}`. The file lives only on the workers and never appears in the REST API output.

## Step 4: Create the connector

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @orders-cdc.json
```

`orders-cdc.json`:

```json
{
  "name": "orders-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",

    "database.hostname": "db.internal",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${file:/secrets/db.properties:password}",
    "database.dbname": "shop",

    "topic.prefix": "dbserver",
    "table.include.list": "public.orders,public.customers",

    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "publication.name": "dbz_orders_pub",
    "publication.autocreate.mode": "filtered",

    "snapshot.mode": "initial",
    "heartbeat.interval.ms": "10000",

    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "value.converter.schemas.enable": "false"
  }
}
```

### Main properties

| Property | Purpose |
| --- | --- |
| `connector.class` | The Debezium connector for your database |
| `tasks.max` | Keep at `1` for PostgreSQL and MySQL. A single log has to be read in order, so more tasks do nothing |
| `topic.prefix` | Prefix for every topic name: `<prefix>.<schema>.<table>`. Treat it as the logical name of the server and do not change it later |
| `table.include.list` | Tables to capture, as `schema.table`. Without it, all non-system tables are captured |
| `plugin.name` | Logical decoding plugin. `pgoutput` is built in to PostgreSQL 10+ |
| `slot.name` | Replication slot. Use a unique name per connector |
| `publication.autocreate.mode` | `filtered` creates a publication only for the included tables |
| `snapshot.mode` | `initial` (default) snapshots first, then streams. Others include `no_data` (no existing rows), `initial_only` (snapshot and stop), `when_needed`, `always` |
| `heartbeat.interval.ms` | Emits heartbeat events so the slot position advances even when the captured tables are idle, which keeps WAL from piling up |
| `key.converter`, `value.converter` | How messages are serialized. Use Avro or Protobuf with a schema registry in production, and JSON with schemas disabled for local tests |

### Optional: flatten the event

By default each message carries the full envelope (`before`, `after`, `op`, `source`). To get only the new row state, which suits sink connectors, add the unwrap transform:

```json
"transforms": "unwrap",
"transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
"transforms.unwrap.delete.handling.mode": "rewrite",
"transforms.unwrap.drop.tombstones": "false"
```

With `rewrite`, deletes appear as records with a `__deleted` field set to `true`.

## Step 5: Verify

```bash
# connector and task state should be RUNNING
curl -s http://localhost:8083/connectors/orders-cdc/status

# topics created by the snapshot
kafka-topics.sh --bootstrap-server kafka:9092 --list | grep dbserver

# read the events
kafka-console-consumer.sh --bootstrap-server kafka:9092 \
  --topic dbserver.public.orders --from-beginning
```

Then change a row in the database and confirm a new event arrives. On PostgreSQL, check the slot:

```sql
SELECT slot_name, active, restart_lsn FROM pg_replication_slots;
```

## Step 6: Operate the connector

```bash
# pause and resume
curl -X PUT  http://localhost:8083/connectors/orders-cdc/pause
curl -X PUT  http://localhost:8083/connectors/orders-cdc/resume

# restart the connector and its tasks after a failure
curl -X POST "http://localhost:8083/connectors/orders-cdc/restart?includeTasks=true"

# update the configuration
curl -X PUT http://localhost:8083/connectors/orders-cdc/config \
  -H "Content-Type: application/json" -d @orders-cdc-config-only.json

# delete the connector
curl -X DELETE http://localhost:8083/connectors/orders-cdc
```

Deleting a connector does **not** drop its PostgreSQL replication slot. Drop it yourself, or the database keeps accumulating WAL:

```sql
SELECT pg_drop_replication_slot('debezium_orders');
```

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Connector class not found | The plugin is not in `plugin.path` on every worker, or the workers were not restarted |
| `must be superuser or replication role` | The database user lacks the `REPLICATION` attribute or the `pg_hba.conf` rule |
| Task fails with a slot error | Another connector or process is using the same `slot.name`. Use a unique slot per connector |
| No events after the snapshot | The table is missing from `table.include.list`, or the publication does not cover it |
| `before` has only the key columns | The table does not have `REPLICA IDENTITY FULL` |
| Disk usage on the database keeps growing | The connector is stopped or lagging and the slot holds WAL. Fix the connector, set heartbeats, or drop an unused slot |
| Message too large | Increase `max.request.size` on the producer side of Connect and `message.max.bytes` on the topic |

## Production checklist

- Pin the Debezium version and install the same one on every worker.
- Create the Connect internal topics with replication factor 3 (`config.storage.replication.factor`, `offset.storage.replication.factor`, `status.storage.replication.factor`).
- Run at least two workers so tasks can fail over.
- Use a dedicated database user with minimal privileges and a config provider for secrets.
- Set heartbeats and alert on replication slot lag, connector status and the Debezium JMX metrics.
- Use Avro or Protobuf with a schema registry, so schema changes are tracked.
- Plan the initial snapshot of large tables for a low-traffic window.

## Related

- [[data architecture/CDC.md|CDC]]
- [[data architecture/Apache Kafka/Topics.md|Topics]]
