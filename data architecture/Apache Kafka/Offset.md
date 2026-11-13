---
aliases:
  - offset
  - offsets
  - committed offset
---
## About

An offset is a sequential number (starting at 0) that Kafka assigns to each record when it is appended to a partition. It identifies the position of the record inside that partition's log.

- Offsets are unique **only within a partition**: the same offset number exists in every partition of a topic
- Offsets are immutable and never reused, even after the record is deleted by retention or compaction
- Order is defined by the offset, so a consumer always reads a partition from the lowest to the highest offset

## Consumer Offsets

Records are not removed when they are read, so Kafka keeps the reading position of each consumer group separately from the data. The group coordinator (a broker) stores one committed offset per group, topic and partition in the internal topic `__consumer_offsets`, which allows several groups to read the same data independently.

- **Current position:** the offset of the next record the consumer will fetch
- **Committed offset:** the last position the group has saved as processed, used to resume after a restart or rebalance
- `__consumer_offsets` is a compacted topic replicated like any other (50 partitions by default), keyed by group, topic and partition, so only the latest commit of each key is kept
- Commits survive restarts of the group and of the brokers
- Offsets can also be stored outside Kafka (for example in a database, next to the processed result), and the consumer then uses `seek()` to resume from them

## Resuming Consumption

By convention, the committed offset stored is the offset of the **next record to read** (last processed offset + 1). So if a group has processed up to offset 42, it commits 43 and resumes reading at 43.

If there is no valid committed offset (new group, or the offset was deleted or is out of range), the `auto.offset.reset` config decides where to start:

| Value      | Behavior                                                              |
| ---------- | --------------------------------------------------------------------- |
| `latest`   | Start from the end of the partition, reading only new records (default) |
| `earliest` | Start from the oldest record still retained                           |
| `none`     | Throw an exception to the application                                 |

## Commit Strategies

| Strategy        | Config / API                                  | Risk                                                                   |
| --------------- | --------------------------------------------- | ---------------------------------------------------------------------- |
| Auto commit     | `enable.auto.commit=true` (every `auto.commit.interval.ms`) | A crash after the commit but before processing loses records (at-most-once) |
| Manual sync     | `commitSync()`                                | Blocks until the broker confirms                                       |
| Manual async    | `commitAsync()`                               | Higher throughput, but a failed commit may not be retried in order     |
| Transactional   | `sendOffsetsToTransaction()`                  | Commits offsets atomically with the produced records (exactly-once)    |

- Commit **after** processing for **at-least-once** delivery: a crash causes reprocessing, so processing must be idempotent
- Commit **before** processing for **at-most-once** delivery: a crash causes lost records

## Offset Gaps and Retention

- Log compaction and transaction markers can leave gaps in the offset sequence, so the offset of the next record is not always the previous one plus 1
- If retention deletes records before a slow group reads them, the committed offset becomes out of range and `auto.offset.reset` applies
- Offsets of the same data are **not equal across clusters**: cross-cluster replication needs offset translation or checkpoints when consumers fail over

## Inspecting and Resetting

```bash
# Show current offset, log end offset and lag per partition
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group

# Reset the group to the earliest offset (the group must be inactive)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group \
  --topic my-topic --reset-offsets --to-earliest --execute
```

- **Lag** = log end offset − committed offset; it measures how far a group is behind the producers
