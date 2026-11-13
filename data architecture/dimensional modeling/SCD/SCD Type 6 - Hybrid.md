---
aliases:
  - SCD Type 6
  - Type 6 SCD
  - Hybrid SCD
tags:
  - data-warehouse
  - scd
---
**SCD Type 6 (hybrid)** combines the techniques of Types 1, 2 and 3 (1 + 2 + 3 = 6). It keeps one **row per version** like [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|Type 2]], and adds columns holding the **current** value of the attribute, which are **overwritten on every row** of the entity like Type 1 (with the previous-value idea of Type 3).

The result: from any historical row, you can see both the value that was true then and the value that is true now.

## How it works

Columns for a tracked attribute `city`:

| Column | Meaning |
| --- | --- |
| `city` | The value at the time of this version (historical, never changed) |
| `current_city` | The latest value for the entity, **updated on all its rows** |

Before the change:

| customer_sk | customer_id | city | current_city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | São Paulo | 2024-01-01 | 9999-12-31 | true |

After the customer moves to Recife on 2026-03-01:

| customer_sk | customer_id | city | current_city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | **Recife** | 2024-01-01 | 2026-03-01 | false |
| 2 | C-100 | Recife | Recife | 2026-03-01 | 9999-12-31 | true |

```sql
-- 1. Type 2: close the old version and add the new one (as in Type 2)

-- 2. Type 1: overwrite current_city on every row of the entity
UPDATE dim_customer
SET current_city = 'Recife'
WHERE customer_id = 'C-100';
```

## Queries

```sql
-- Revenue by the city the customer lived in at the time (historical)
SELECT d.city, SUM(f.amount)
FROM fact_sales f JOIN dim_customer d ON d.customer_sk = f.customer_sk
GROUP BY d.city;

-- Revenue regrouped by where the customer lives today (current)
SELECT d.current_city, SUM(f.amount)
FROM fact_sales f JOIN dim_customer d ON d.customer_sk = f.customer_sk
GROUP BY d.current_city;
```

Both reports use the same join, and only the grouping column changes.

## When to use it

- Business users need **as-was and as-is** reporting from the same dimension, for example sales by the old territory and by the new one.
- The attribute changes rarely, so rewriting `current_*` on all versions is cheap.

## Pros and cons

| Pros | Cons |
| --- | --- |
| Historical and current values in one table, one join | Every change touches all rows of the entity |
| No second dimension or view needed | More columns, and extra update logic in the load |
| Easy for analysts to use | Not suited to fast-changing attributes |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 1 - Overwrite.md|SCD Type 1 - Overwrite]]
- [[data architecture/dimensional modeling/SCD/SCD Type 3 - Add New Column.md|SCD Type 3 - Add New Column]]
- [[data architecture/dimensional modeling/SCD/SCD Type 7 - Dual Type 1 and 2.md|SCD Type 7 - Dual Type 1 and 2]]
