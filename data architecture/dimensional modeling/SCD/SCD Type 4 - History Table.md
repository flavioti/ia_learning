---
aliases:
  - SCD Type 4
  - Type 4 SCD
  - Mini-dimension
  - History table
tags:
  - data-warehouse
  - scd
---
**SCD Type 4** keeps the **current** values in the main dimension and moves the **changing attributes or the history** elsewhere. The name is used for two related techniques, and sources do not agree on which one is "the" Type 4:

| Variant | Idea | Used by |
| --- | --- | --- |
| **History table** | The dimension holds only the current row. Every previous version goes to a separate history table | Many textbooks and tutorials |
| **Mini-dimension** | Attributes that change often are split into a small separate dimension, and the fact table points to both | Kimball's dimensional modeling |

## Variant 1: history table

`dim_customer` always has one row per customer, as in [[data architecture/dimensional modeling/SCD/SCD Type 1 - Overwrite.md|Type 1]]. A second table, `dim_customer_history`, stores the old versions with their validity range.

`dim_customer` (current only):

| customer_sk | customer_id | city | valid_from |
|---|---|---|---|
| 1 | C-100 | Recife | 2026-03-01 |

`dim_customer_history`:

| customer_sk | customer_id | city | valid_from | valid_to |
|---|---|---|---|---|
| 1 | C-100 | São Paulo | 2024-01-01 | 2026-03-01 |
| 1 | C-100 | Recife | 2026-03-01 | 9999-12-31 |

```sql
-- On a change: archive the old row, then overwrite the current one
INSERT INTO dim_customer_history (customer_sk, customer_id, city, valid_from, valid_to)
SELECT d.customer_sk, d.customer_id, d.city, d.valid_from, CURRENT_DATE
FROM dim_customer d
JOIN stg_customer s ON s.customer_id = d.customer_id
WHERE d.city <> s.city;

UPDATE dim_customer d
SET city = s.city, valid_from = CURRENT_DATE
FROM stg_customer s
WHERE s.customer_id = d.customer_id
  AND s.city <> d.city;
```

(`UPDATE ... FROM` syntax varies by engine.)

Queries that only need the current state stay fast and small. Reports that need history query the history table. Some databases do this automatically with **temporal tables**.

## Variant 2: mini-dimension

Some attributes change too often and are too numerous to version in a big dimension with [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|Type 2]], for example the age band, income band and credit-score band of a customer with millions of rows. Those attributes go into a **mini-dimension**, with one row per combination of values. The values are grouped into **bands** (ranges), so the mini-dimension stays small.

`dim_customer_profile` (mini-dimension):

| profile_sk | age_band | income_band | credit_band |
|---|---|---|---|
| 1 | 30-39 | Medium | Good |
| 2 | 30-39 | High | Good |

The fact table then carries two keys, and the profile that was true at the time of the event is captured with no extra rows in `dim_customer`:

```
fact_sales (customer_sk, profile_sk, date_sk, amount)
```

## When to use it

- **History table**: you mostly query the current state and rarely need history, or the database supports temporal tables.
- **Mini-dimension**: a large dimension with a group of volatile attributes whose history matters.

## Pros and cons

| Pros | Cons |
| --- | --- |
| The main dimension stays small and fast | Two structures to load and query |
| Volatile attributes are isolated from stable ones | Mini-dimension attributes must be banded, which loses precision |
| Full history is still available | Queries for history need an extra join or union |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|SCD Type 2 - Add New Row]]
- [[data architecture/dimensional modeling/SCD/SCD Type 5 - Mini-Dimension and Type 1 Outrigger.md|SCD Type 5 - Mini-Dimension and Type 1 Outrigger]]
