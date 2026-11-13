---
aliases:
  - SCD Type 7
  - Type 7 SCD
  - Dual Type 1 and 2
tags:
  - data-warehouse
  - scd
---
**SCD Type 7 (dual Type 1 and Type 2)** serves both views, "as it was" and "as it is now", without repeating the current values on each row. It is a [[data architecture/dimensional modeling/SCD/SCD Type 2 - Add New Row.md|Type 2]] dimension where the fact table also stores a **durable key**, plus a **view** of the dimension that shows only the current rows (Type 1 behavior).

## How it works

| Piece | Role |
| --- | --- |
| `dim_customer` | A Type 2 dimension: one row per version, with the surrogate key `customer_sk` and the validity columns |
| `customer_dk` | **Durable key** (also called supernatural key): a stable key shared by all versions of the entity. It does not change when attributes change |
| `fact_sales` | Stores **both** `customer_sk` (the version at the time of the event) and `customer_dk` |
| `dim_customer_current` | A view over `dim_customer` with only the current rows, joined through `customer_dk` |

`dim_customer`:

| customer_sk | customer_dk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|---|
| 1 | 500 | C-100 | São Paulo | 2024-01-01 | 2026-03-01 | false |
| 2 | 500 | C-100 | Recife | 2026-03-01 | 9999-12-31 | true |

`fact_sales`:

| order_id | customer_sk | customer_dk | amount |
|---|---|---|---|
| 9001 | 1 | 500 | 120.00 |
| 9002 | 2 | 500 | 80.00 |

```sql
CREATE VIEW dim_customer_current AS
SELECT customer_dk, customer_id, city
FROM dim_customer
WHERE is_current;
```

## Queries

```sql
-- As it was: join through the surrogate key
SELECT d.city, SUM(f.amount)
FROM fact_sales f JOIN dim_customer d ON d.customer_sk = f.customer_sk
GROUP BY d.city;

-- As it is now: join through the durable key and the current view
SELECT c.city, SUM(f.amount)
FROM fact_sales f JOIN dim_customer_current c ON c.customer_dk = f.customer_dk
GROUP BY c.city;
```

## When to use it

- Users need both historical and current views, and rewriting `current_*` columns on every row ([[data architecture/dimensional modeling/SCD/SCD Type 6 - Hybrid.md|Type 6]]) is undesirable.
- The attribute set is large, so a current view is easier than extra columns.

## Pros and cons

| Pros | Cons |
| --- | --- |
| Both views from one Type 2 dimension | The fact table carries two keys for the dimension |
| No updates to old dimension rows beyond closing them | Needs a durable key and a current view to maintain |
| A change only closes one row and adds one | Analysts must pick the right join for the question |

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 5 - Mini-Dimension and Type 1 Outrigger.md|SCD Type 5 - Mini-Dimension and Type 1 Outrigger]]
