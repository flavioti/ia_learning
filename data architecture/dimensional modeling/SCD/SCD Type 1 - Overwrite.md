---
aliases:
  - SCD Type 1
  - Type 1 SCD
  - Overwrite
tags:
  - data-warehouse
  - scd
---
**SCD Type 1 (overwrite)** replaces the old value with the new one in the same row. **No history is kept**: the dimension only shows the latest state.

## How it works

The customer moves from São Paulo to Recife.

Before:

| customer_sk | customer_id | city |
|---|---|---|
| 1 | C-100 | São Paulo |

After:

| customer_sk | customer_id | city |
|---|---|---|
| 1 | C-100 | Recife |

The surrogate key stays the same, so facts loaded earlier now point to a row that says "Recife".

```sql
MERGE INTO dim_customer AS t
USING stg_customer AS s
  ON t.customer_id = s.customer_id
WHEN MATCHED AND t.city <> s.city THEN
  UPDATE SET city = s.city
WHEN NOT MATCHED THEN
  INSERT (customer_id, city) VALUES (s.customer_id, s.city);
```

## When to use it

- **Corrections**: a typo in a name or a wrong value that should never have been there.
- **Attributes where history has no business value**, such as a phone number or an email.
- **Fast-changing, low-importance attributes**, where keeping history would only add rows.

## Pros and cons

| Pros | Cons |
| --- | --- |
| The simplest approach, with the smallest dimension | History is lost for good |
| Facts always join to a single row per business key | Last year's sales by city now show the new city |
| Cheap to load and query | Pre-computed aggregates and materialized views must be rebuilt after a change |

## Design notes

- Rebuild or refresh aggregate tables that depend on the changed attribute.
- Mix with other types per column: Type 1 for corrections, Type 2 for attributes whose history matters.
- If you need the old value later, the source system or a [[data architecture/CDC.md|CDC]] log is the only place left to find it.

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 0 - Retain.md|SCD Type 0 - Retain]]
- [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|SCD Type 2 - Add New Row]]
