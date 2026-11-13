---
aliases:
  - SCD Type 0
  - Type 0 SCD
  - Retain original
tags:
  - data-warehouse
  - scd
---
**SCD Type 0 (retain original)** means the attribute **never changes** after the row is first loaded. Updates that arrive from the source are ignored, so the dimension always keeps the original value.

## How it works

The load inserts a row the first time it sees a business key, and never updates the tracked attributes afterwards.

| customer_id | signup_channel | birth_date |
|---|---|---|
| C-100 | Paid search | 1990-05-12 |

If the source later says the signup channel is "Email", the dimension still shows "Paid search".

```sql
-- Insert only new customers; never update the retained columns
INSERT INTO dim_customer (customer_id, signup_channel, birth_date)
SELECT s.customer_id, s.signup_channel, s.birth_date
FROM stg_customer s
LEFT JOIN dim_customer d ON d.customer_id = s.customer_id
WHERE d.customer_id IS NULL;
```

## When to use it

- **Attributes that are true by definition and do not change**: birth date, the original signup channel or campaign, the date of the first purchase, a durable identifier.
- **Reporting that must always group by the original value**, for example "revenue by acquisition channel".
- It is common to mix it with other types: one dimension can have some attributes at Type 0, others at Type 1 or Type 2.

## Pros and cons

| Pros | Cons |
| --- | --- |
| The simplest to load and reason about | A wrong value stays wrong unless you correct it with a separate process |
| The value is stable, so reports never shift | It does not fit anything that really changes |
| No extra rows or columns | The current state of a changed attribute is not available |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 1 - Overwrite.md|SCD Type 1 - Overwrite]]
- [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|SCD Type 2 - Add New Row]]
