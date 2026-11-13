---
aliases:
  - SCD Type 5
  - Type 5 SCD
tags:
  - data-warehouse
  - scd
---
**SCD Type 5** builds on the mini-dimension of [[data architecture/dimensional modeling/SCD/SCD Type 4 - History Table.md|Type 4]] and adds a **Type 1 reference** from the base dimension to the **current** mini-dimension row. The number 5 comes from 4 + 1. It lets a report use the profile "as it was" at the time of the event (through the fact table) or "as it is now" (through the base dimension).

## How it works

Three structures:

| Structure | Content |
| --- | --- |
| `dim_customer` (base dimension) | One row per customer (Type 1) with a column `current_profile_sk` that points to the latest mini-dimension row |
| `dim_customer_profile` (mini-dimension) | One row per combination of banded volatile attributes |
| `fact_sales` | Carries both `customer_sk` and `profile_sk`, where `profile_sk` is the profile **at the time of the sale** |

`dim_customer_profile`:

| profile_sk | age_band | income_band |
|---|---|---|
| 1 | 30-39 | Medium |
| 2 | 30-39 | High |

`dim_customer` (always overwritten, Type 1):

| customer_sk | customer_id | city | current_profile_sk |
|---|---|---|---|
| 1 | C-100 | Recife | 2 |

When the customer's income moves from Medium to High:

1. The ETL finds (or creates) the mini-dimension row for the new combination, here `profile_sk = 2`.
2. It **overwrites** `current_profile_sk` in `dim_customer` with 2.
3. New facts are loaded with `profile_sk = 2`. Old facts keep `profile_sk = 1`.

```sql
-- Update the Type 1 pointer to the current profile
UPDATE dim_customer d
SET current_profile_sk = p.profile_sk
FROM stg_customer s
JOIN dim_customer_profile p
  ON p.age_band = s.age_band AND p.income_band = s.income_band
WHERE d.customer_id = s.customer_id
  AND d.current_profile_sk <> p.profile_sk;
```

(`UPDATE ... FROM` syntax varies by engine.)

## Querying

```sql
-- As it was: profile at the time of the sale
SELECT p.income_band, SUM(f.amount)
FROM fact_sales f
JOIN dim_customer_profile p ON p.profile_sk = f.profile_sk
GROUP BY p.income_band;

-- As it is now: customer's current profile
SELECT p.income_band, SUM(f.amount)
FROM fact_sales f
JOIN dim_customer d ON d.customer_sk = f.customer_sk
JOIN dim_customer_profile p ON p.profile_sk = d.current_profile_sk
GROUP BY p.income_band;
```

## When to use it

- A large dimension with volatile, banded attributes, where users need **both** the historical and the current view.
- You want the base dimension small, with no Type 2 row explosion.

## Pros and cons

| Pros | Cons |
| --- | --- |
| Historical and current views with a small base dimension | Three structures to build and maintain |
| No row explosion in the large dimension | Attributes must be banded |
| Current profile is one join away | Queries are more complex than with a plain Type 2 |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 6 - Hybrid.md|SCD Type 6 - Hybrid]]
- [[data architecture/dimensional modeling/SCD/SCD Type 7 - Dual Type 1 and 2.md|SCD Type 7 - Dual Type 1 and 2]]
