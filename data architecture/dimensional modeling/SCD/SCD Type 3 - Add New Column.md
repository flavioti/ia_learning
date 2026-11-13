---
aliases:
  - SCD Type 3
  - Type 3 SCD
  - Add new column
tags:
  - data-warehouse
  - scd
---
**SCD Type 3 (add new column)** keeps a **limited history** in the same row: one column for the current value and another for the previous one. When the attribute changes, the old value moves to the "previous" column and the new value takes its place.

## How it works

| customer_id | city | previous_city |
|---|---|---|
| C-100 | São Paulo | *(null)* |

After the customer moves to Recife:

| customer_id | city | previous_city |
|---|---|---|
| C-100 | Recife | São Paulo |

A second move to Salvador gives `city = Salvador` and `previous_city = Recife`. **São Paulo is lost.** Only one level of history survives.

```sql
MERGE INTO dim_customer AS t
USING stg_customer AS s
  ON t.customer_id = s.customer_id
WHEN MATCHED AND t.city <> s.city THEN
  UPDATE SET previous_city = t.city,
             city          = s.city;
```

In a SQL `UPDATE`, the right-hand sides read the row's values from before the update, so `previous_city = city` takes the old value. Check how your engine evaluates `SET` expressions.

## Variants

- **Effective date column**: add `city_changed_on` so you know when the change happened.
- **Original and current**: keep `original_city` (never changed, like Type 0) next to `current_city`.
- **Several previous values**: columns `city_1`, `city_2`, `city_3`. This grows quickly and is rarely worth it.

## When to use it

- **A single, known change**, such as a sales territory realignment, where users want to report with the old and the new assignment side by side.
- **A limited transition period**, when both values are needed for comparison.
- **Small dimensions** where one extra column is enough and you don't want more rows.

## Pros and cons

| Pros | Cons |
| --- | --- |
| Simple, with no extra rows | Only the last value (or a few) is kept |
| Easy to compare old and new in one row | Not suited to attributes that change often |
| Facts keep a single surrogate key | You can't tell the value at an arbitrary past date |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 1 - Overwrite.md|SCD Type 1 - Overwrite]]
- [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|SCD Type 2 - Add New Row]]
- [[data architecture/dimensional modeling/SCD/SCD Type 6 - Hybrid.md|SCD Type 6 - Hybrid]]
