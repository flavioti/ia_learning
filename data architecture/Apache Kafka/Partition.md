---
aliases:
  - partition leader
  - partition replica
---

## About

A partition is the unit of storage and parallelism of a Kafka topic. Each topic is split into one or more partitions, and each partition is an ordered, append-only log of records. Every record in a partition gets a sequential number called the [[data architecture/Apache Kafka/Offset.md|offset]], which is unique only within that partition.

## Parallelism

- Partitions are spread across the [[data architecture/Apache Kafka/Brokers.md|Brokers]] of the cluster, so reads and writes scale horizontally
- Within a consumer group, each partition is assigned to **at most one** consumer, so the number of partitions is the upper limit of useful consumers in the group
- Different consumer groups read the same partition independently, each one tracking its own offsets

## Ordering

- Kafka guarantees order **only inside a single partition**, never across the partitions of a topic
- The producer chooses the partition of each record:
  - **With a key:** the default partitioner hashes the key, so all records with the same key go to the same partition
  - **Without a key:** records are distributed across partitions (sticky/round-robin)
- To keep the order of the events of one entity (for example, one customer), use its ID as the record key

## Partition Count

- The count is defined when the topic is created and can be **increased** later, but never decreased
- Increasing it changes the hash-to-partition mapping, so new records for an existing key may land in a different partition and break per-key ordering
- More partitions means more parallelism, but also more open files, more replication traffic and longer leader election and recovery times

## Replication

Each partition is replicated on several brokers, according to the topic **replication factor**.

- **Leader:** the single replica that handles all reads and writes of the partition
- **Followers:** replicas that only fetch records from the leader to stay up to date
- **ISR (in-sync replicas):** the leader plus the followers that are fully caught up with it. Only ISR members are eligible to become leader
- Replicas of the same partition live on different brokers, so a single broker failure does not lose the partition
- A replication factor of 3 is the common choice: the partition survives the loss of up to 2 brokers

### Durability settings

| Config              | Where    | Effect                                                                                          |
| ------------------- | -------- | ----------------------------------------------------------------------------------------------- |
| replication.factor  | Topic    | How many copies of each partition exist (leader included)                                       |
| min.insync.replicas | Topic    | Minimum ISR size (leader included) required to accept a write when the producer uses `acks=all` |
| acks=all            | Producer | The leader acknowledges a write only after all ISR members have it                              |

With `replication.factor=3`, `min.insync.replicas=2` and `acks=all`, writes keep working with one replica down. If only the leader remains in the ISR, new writes are rejected (`NotEnoughReplicasException`) instead of being acknowledged with a risk of data loss.

## Leader Election

1. The broker that hosts a partition leader fails
2. The [[data architecture/Apache Kafka/Controllers.md|cluster controller]] (a [[data architecture/Apache Kafka/KRaft.md|KRaft]] controller in current versions) detects the broker failure
3. The controller elects one eligible replica from the ISR as the new leader
4. Producers and consumers discover the new leader through metadata updates, and the partition resumes reads and writes

Because the new leader comes from the ISR, it already has every record that was acknowledged with `acks=all`, so no committed data is lost.

## Related

- [[data architecture/Apache Kafka/Producer.md|Producer]]
- [[Consumer|Consumer group]]
- [[data architecture/Apache Kafka/Cluster.md|Cluster]]

## Links

- [[data architecture/Apache Kafka/Offset.md|Offset]]
- [[data architecture/Apache Kafka/Kafka Topic Partition Replica.md|Kafka Topic Partition Replica]]
