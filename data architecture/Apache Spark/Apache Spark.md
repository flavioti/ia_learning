## Read Less
- partition pruning = query partitions directly
- Predicate push down - apply filters earlier
- Column pruning = choose columns, not `select *`
- Fix small files
## Shuffle less
- Broadcast join
- Bucketing
- Aggregate earlier
- Handle Skew - skewjoin.enabled=true
## Compute smarter
- Turn on AOE
- Cache what you reuse
- re partition vs coalesce
- Avoid python UDFs
