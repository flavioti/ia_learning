---
aliases:
  - Consumer group
  - consumer group
---

## About

A consumer is a client application that reads records from Kafka topics. It uses a **pull** model: the consumer calls `poll()` and fetches batches of records from the brokers at its own pace, so a slow consumer never overloads the brokers or affects other consumers.

Reading a record does not remove it. Records stay in the log until retention or compaction deletes them, so the same data can be read many times and by many applications.

## Consumer Group

A consumer group is a set of consumers that share the same `group.id` and work together to read a topic.

- Each [[data architecture/Apache Kafka/Partition.md|Partition]] of the topic is assigned to **exactly one** consumer of the group, while one consumer can read several partitions
- Records are split between the members, so each record is processed by only one consumer of the group
- Different groups are independent: each group receives every record of the topic and keeps its own [[data architecture/Apache Kafka/Offset.md|Offset]]
- Adding consumers scales the processing, up to the number of partitions. Extra consumers stay idle

| Scenario                          | Result                                               |
| --------------------------------- | ---------------------------------------------------- |
| 1 group, consumers < partitions   | Some consumers read more than one partition          |
| 1 group, consumers = partitions   | One partition per consumer (maximum parallelism)     |
| 1 group, consumers > partitions   | The extra consumers are idle (standby)               |
| Several groups on the same topic  | Each group reads all records (publish/subscribe)     |

## Resuming Where It Stopped

The group stores its progress as committed [[data architecture/Apache Kafka/Offset.md|offsets]] in the internal topic `__consumer_offsets`. After a restart or rebalance, each partition is read again from its last committed offset.

## Group Coordinator and Rebalance

One broker acts as the **group coordinator** of each group. It tracks the members and the committed offsets.

A **rebalance** redistributes the partitions among the members. It is triggered when:

- A consumer joins the group
- A consumer leaves or crashes
- The topic gets new partitions or the subscription changes
- A consumer is considered dead (see the timeouts below)

During a classic rebalance the group may pause consumption, so frequent rebalances hurt throughput.

| Config                 | Description                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| session.timeout.ms     | Max time without heartbeats before the consumer is removed from the group. Heartbeats are sent by a background thread |
| heartbeat.interval.ms  | How often heartbeats are sent. Should be a third of `session.timeout.ms` or less                     |
| max.poll.interval.ms   | Max time between two `poll()` calls. If processing a batch takes longer, the consumer leaves the group and a rebalance follows |
| max.poll.records       | Max number of records returned by one `poll()`. Lower it when each batch takes too long to process   |
| group.instance.id      | Enables **static membership**: a restarted consumer keeps its partitions without triggering a rebalance |

Slow processing is a common cause of rebalances: the consumer keeps sending heartbeats but exceeds `max.poll.interval.ms`. The fix is to reduce the work per poll (`max.poll.records`) or tune the interval to the measured processing time.

## Delivery Semantics

The semantics depend on when the offset is committed relative to the processing:

| Semantics     | How                                                                 | Failure effect                |
| ------------- | ------------------------------------------------------------------- | ----------------------------- |
| At-most-once  | Commit before processing                                            | A crash loses records         |
| At-least-once | Commit after processing (default choice)                            | A crash causes duplicates     |
| Exactly-once  | Kafka transactions, with consumers using `isolation.level=read_committed` | Aborted writes are never visible |

- Rebalances can make two consumers process the same record at the same time, so side effects on external systems (payments, emails) need an **idempotency key** in the target service
- `isolation.level=read_committed` makes the consumer skip records from aborted or still open transactions. The default is `read_uncommitted`

## Main Configs

| Config               | Description                                                                          | Default          |
| -------------------- | ------------------------------------------------------------------------------------ | ---------------- |
| group.id             | Identifies the consumer group                                                        |                  |
| enable.auto.commit   | Commits offsets automatically in the background                                      | `true`           |
| auto.offset.reset    | Where to start without a valid committed offset: `latest`, `earliest` or `none`      | `latest`         |
| fetch.min.bytes      | Min data the broker returns per fetch. Higher values favor throughput over latency   | 1                |
| fetch.max.wait.ms    | Max time the broker waits to reach `fetch.min.bytes`                                 | 500              |
| isolation.level      | `read_uncommitted` or `read_committed`                                               | `read_uncommitted` |

## Basic Example

```python
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "orders-service",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})
consumer.subscribe(["orders"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise RuntimeError(msg.error())

        process(msg.value())          # must be idempotent
        consumer.commit(message=msg)  # commit after processing: at-least-once
finally:
    consumer.close()
```

## Troubleshooting

- **Authenticated but cannot read a topic:** the authentication worked, so check the authorization: the principal needs `Read` permission (ACL) on the topic and on the consumer group
- **Constant rebalances:** check `max.poll.interval.ms` against the batch processing time and consider static membership
- **Growing lag:** add consumers (up to the partition count), speed up the processing or increase the partitions

## Links

- [[data architecture/Apache Kafka/Offset.md|Offset]]

## Related

- [[data architecture/Apache Kafka/Partition.md|Partition]]
