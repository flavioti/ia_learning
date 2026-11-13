---
aliases:
  - Connect distributed mode
  - connect-distributed
tags:
  - kafka-connect
---
How to configure Kafka Connect in **distributed mode**, where several workers form one Connect cluster, share the connector tasks and keep their state in Kafka. This note ends with the simplest working example: two workers and a file source connector.

## What distributed mode needs

- A running Kafka cluster (the workers are ordinary Kafka clients).
- One properties file, **the same on every worker**, started with `bin/connect-distributed.sh`.
- Three internal topics where the cluster keeps its state:

| Topic | Stores |
| --- | --- |
| `config.storage.topic` | Connector and task configuration. Must have **1 partition** and be compacted |
| `offset.storage.topic` | Offsets of source connectors (positions in the source system) |
| `status.storage.topic` | Status of connectors and tasks |

No state is kept on the worker's local disk, so a worker can be replaced at any time.

## Worker configuration

`config/connect-distributed.properties` (Apache Kafka ships a ready-made file with these keys):

```properties
# Kafka cluster the workers connect to
bootstrap.servers=localhost:9092

# Workers with the same group.id form one Connect cluster
group.id=connect-cluster

# How records are serialized in Kafka
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# Internal topics (replication factor 1 only for a single-broker dev setup)
config.storage.topic=connect-configs
config.storage.replication.factor=1
offset.storage.topic=connect-offsets
offset.storage.replication.factor=1
status.storage.topic=connect-status
status.storage.replication.factor=1

# REST API of this worker
listeners=http://:8083

# Where the connector plugins live
plugin.path=/opt/kafka/plugins
```

### Key settings

| Setting | Purpose |
| --- | --- |
| `bootstrap.servers` | Brokers to connect to |
| `group.id` | Name of the Connect cluster. **Must be unique per cluster and identical on all its workers**, and must not clash with a consumer group |
| `*.converter` | Default converters for keys and values. A connector can override them |
| `*.storage.topic` and `*.replication.factor` | Names of the internal topics, and their durability. Use 3 in production |
| `listeners` | Address where the worker serves the REST API (default port 8083) |
| `plugin.path` | Directories or JARs scanned for connectors, converters and transforms |
| `offset.flush.interval.ms` | How often source offsets are committed (default 60 s) |

The internal topics are created automatically if they don't exist, using the replication factors above. In production, create them beforehand with the settings you want.

## What must be the same on every worker

- `group.id` and the three storage topic names.
- The same connector plugins in `plugin.path`, with the same versions. A task fails if it lands on a worker that lacks the plugin.
- Compatible converter settings.

What differs per worker: the REST `listeners` address (only when two workers share one machine) and local paths.

## Start the workers

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

Run the same command on each machine. Starting another worker with the same `group.id` is all it takes to **scale out**. Stopping one makes the others take over its tasks.

## Simplest example: two workers and a file source

This runs everything on one machine, with a Kafka broker on `localhost:9092`. It uses the demo `FileStreamSource` connector, which ships with Apache Kafka but is not on the default plugin path.

### 1. Make the file connector available

In `config/connect-distributed.properties`, point `plugin.path` at the connector JAR (the version matches your Kafka):

```properties
plugin.path=/opt/kafka/libs/connect-file-<kafka-version>.jar
```

### 2. Start the first worker

```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

Check that the REST API answers, and that the plugin is loaded:

```bash
curl -s http://localhost:8083/
curl -s http://localhost:8083/connector-plugins | grep FileStream
```

### 3. Start a second worker

Copy the file and change **only** the port:

```bash
cp config/connect-distributed.properties config/connect-distributed-2.properties
sed -i 's|listeners=http://:8083|listeners=http://:8084|' config/connect-distributed-2.properties

bin/connect-distributed.sh config/connect-distributed-2.properties
```

Both workers share the same `group.id` and topics, so they now form one cluster of two workers.

### 4. Create the connector

Send it to either worker:

```bash
mkdir -p /tmp/connect-demo && touch /tmp/connect-demo/input.txt

curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "file-source",
    "config": {
      "connector.class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
      "tasks.max": "1",
      "file": "/tmp/connect-demo/input.txt",
      "topic": "connect-demo"
    }
  }'
```

### 5. Test it

```bash
echo "hello connect" >> /tmp/connect-demo/input.txt
echo "second line"   >> /tmp/connect-demo/input.txt

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic connect-demo --from-beginning
```

Each line of the file appears as a message in the `connect-demo` topic.

### 6. See which worker runs the task

```bash
curl -s http://localhost:8083/connectors/file-source/status
```

The response lists a `worker_id` for the connector and for each task. Stop the worker that runs the task: after a few seconds the other worker takes it over, and new lines still reach the topic.

> The file connector reads a local file, so the file must exist on whichever worker runs the task. That works here because both workers share one machine. In real deployments, use connectors that read from a network system (a database, object storage, a queue).

## Useful REST calls

| Call | Does |
| --- | --- |
| `GET /connectors` | Lists connectors |
| `GET /connectors/<name>/status` | State of the connector and its tasks, with the worker of each |
| `GET /connectors/<name>/config` | Current configuration |
| `PUT /connectors/<name>/config` | Creates or updates a connector |
| `PUT /connectors/<name>/pause` and `/resume` | Pauses and resumes it |
| `POST /connectors/<name>/restart?includeTasks=true` | Restarts the connector and its tasks |
| `DELETE /connectors/<name>` | Deletes it |
| `GET /connector-plugins` | Lists the installed plugins |

You can call any worker. A request that needs the cluster leader is forwarded for you.

## Common problems

| Symptom | Likely cause |
| --- | --- |
| Workers don't see each other | Different `group.id` or different storage topic names |
| Connector class not found | The plugin is missing from `plugin.path` on that worker, or the worker was not restarted |
| Task stays `UNASSIGNED` or fails after a rebalance | The task moved to a worker that lacks the plugin or the file or network access it needs |
| Startup fails on the internal topics | Replication factor higher than the number of brokers, or the config topic has more than one partition |
| `Address already in use` | Two workers on one machine use the same REST port |

## Related

- [[Consumer|Consumer group]]
- [[data architecture/Apache Kafka/Debezium Installation and Configuration.md|Debezium Installation and Configuration]]
