---
aliases:
  - KRaft
  - Kraft
  - Kafka Raft
  - KRaft mode
tags:
  - kafka
---
KRaft (**K**afka **Raft**) is the way Kafka manages its own cluster metadata, using the **Raft** consensus protocol inside Kafka itself. It replaced Zookeeper: it became production ready in Kafka 3.3, and Zookeeper mode was removed in Kafka 4.0.

A small group of nodes, the **controller quorum**, keeps the metadata in a replicated log. One of them is the active controller, and the others are ready to take over.

## What the controller manages

- **Topics and partitions:** creation, deletion, partition count and replica placement.
- **Leader election:** choosing the partition leader and keeping the in-sync replica (ISR) list.
- **Brokers:** registration, heartbeats, and fencing a broker that stops responding.
- **Configuration and security:** dynamic configs, ACLs and quotas.
- **Feature levels:** the cluster-wide `metadata.version`.

It does **not** manage consumers. That is the job of the group coordinator, which runs on a broker.

## How it works

1. The controllers form a Raft quorum. They elect one **active controller** (the Raft leader). The others are **followers**.
2. Every metadata change, such as "topic X created" or "broker 3 fenced", is a record appended to the `__cluster_metadata` log. This is a single-partition internal topic, replicated across the quorum.
3. A change is committed once a **majority** of controllers has stored it.
4. Brokers **fetch** that log from the active controller and keep the metadata in memory. Previously the controller pushed updates to brokers by RPC.
5. Controllers periodically write **snapshots** of the metadata, so a node that restarts or falls behind catches up from the snapshot plus the log tail, without replaying everything.
6. If the active controller fails, the followers elect a new leader within moments. They already hold the full log, so there is no slow state reload.

## Roles

A node is configured with `process.roles`:

| Role | `process.roles` | Use |
| --- | --- | --- |
| Broker only | `broker` | Serves clients and stores partitions |
| Controller only | `controller` | Dedicated quorum member. Recommended in production |
| Combined | `broker,controller` | One process does both. Fine for development and small clusters |

## Quorum size

The quorum needs a **majority** alive to make progress, so use an odd number:

| Controllers | Failures tolerated |
| --- | --- |
| 1 | 0 (development only) |
| 3 | 1 |
| 5 | 2 |

More than 5 rarely helps, because every commit has to reach a majority.

## Configuration

### Single node (development)

```properties
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
advertised.listeners=PLAINTEXT://localhost:9092
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
log.dirs=/tmp/kraft-combined-logs
```

### Production: 3 dedicated controllers and separate brokers

Controller nodes (one file per node, with its own `node.id`):

```properties
process.roles=controller
node.id=1
controller.quorum.voters=1@ctrl1:9093,2@ctrl2:9093,3@ctrl3:9093
listeners=CONTROLLER://:9093
controller.listener.names=CONTROLLER
log.dirs=/var/lib/kafka/metadata
```

Broker nodes:

```properties
process.roles=broker
node.id=101
controller.quorum.voters=1@ctrl1:9093,2@ctrl2:9093,3@ctrl3:9093
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://broker1:9092
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
log.dirs=/var/lib/kafka/data
```

### Main settings

| Setting | Purpose |
| --- | --- |
| `process.roles` | Whether the node is a broker, a controller, or both |
| `node.id` | Unique id of the node across the whole cluster, brokers and controllers |
| `controller.quorum.voters` | The fixed list of controllers, as `id@host:port`. Newer versions can use `controller.quorum.bootstrap.servers` with a dynamic quorum, so controllers can be added or removed at runtime |
| `controller.listener.names` | Name of the listener used for controller traffic |
| `listeners` | Addresses the node listens on. Controllers need the controller listener, brokers the client one |
| `log.dirs` | Where partitions are stored. On controllers, where the metadata log is stored |

## Format the storage and start

Every node needs a storage directory formatted with the **same cluster id** before its first start:

```bash
# once, for the whole cluster
CLUSTER_ID=$(bin/kafka-storage.sh random-uuid)

# on every node, with that node's own properties file
bin/kafka-storage.sh format -t $CLUSTER_ID -c config/server.properties

# start
bin/kafka-server-start.sh config/server.properties
```

## Inspect the quorum

```bash
bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --status
bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 describe --replication
```

The first shows the cluster id, the current leader and the voters. The second shows each controller's lag behind the leader. `kafka-metadata-shell.sh` lets you browse the metadata log directly.

## Compared with Zookeeper

| | Zookeeper mode | KRaft mode |
| --- | --- | --- |
| Systems to run | Kafka plus a separate Zookeeper cluster | Kafka only |
| Metadata stored in | Zookeeper | `__cluster_metadata` log inside Kafka |
| Update propagation | Controller pushes by RPC | Brokers fetch the log |
| Controller failover | Slow, reloads all state from Zookeeper | Fast, followers already have the log |
| Partition limit | Hundreds of thousands | Millions |

## Migration

Clusters on Zookeeper can be migrated online to KRaft in the 3.x line. Kafka 4.0 cannot run with Zookeeper, so move to KRaft before upgrading to 4.x.

## Related

- [[data architecture/Apache Kafka/Zookeeper (deprecated).md|Zookeeper (deprecated)]]
