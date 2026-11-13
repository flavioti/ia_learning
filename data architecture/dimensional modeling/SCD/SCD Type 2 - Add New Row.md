---
aliases:
  - SCD Type 2
  - Type 2 SCD
  - Add new row
tags:
  - data-warehouse
  - scd
---
**SCD Type 2 (add new row)** keeps the **full history**: when a tracked attribute changes, the current row is closed and a new row is inserted. It is the default choice for most analytical dimensions.

## How it works

Each version of a business entity has its own row, identified by a **surrogate key**. The **business key** (natural key) is the same across all versions of the entity. Validity columns say when each version was true.

| Column | Role |
| --- | --- |
| `customer_sk` | Surrogate key, unique per version. Facts point to it |
| `customer_id` | Business key, shared by all versions |
| `valid_from` | When this version became true |
| `valid_to` | When it stopped being true. `9999-12-31` for the current row |
| `is_current` | Flag for the latest version |
| `row_hash` (optional) | Hash of the tracked columns, for fast change detection |

Before the change:

| customer_sk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | 2024-01-01 | 9999-12-31 | true |

After the customer moves to Recife on 2026-03-01:

| customer_sk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | 2024-01-01 | 2026-03-01 | false |
| 2 | C-100 | Recife | 2026-03-01 | 9999-12-31 | true |

Facts loaded before the move keep pointing to `customer_sk = 1`, and new facts point to `customer_sk = 2`.

## Load pattern

```sql
-- 1. Close current rows whose tracked attributes changed
MERGE INTO dim_customer AS t
USING stg_customer AS s
  ON t.customer_id = s.customer_id AND t.is_current
WHEN MATCHED AND t.row_hash <> s.row_hash THEN
  UPDATE SET valid_to = CURRENT_DATE, is_current = FALSE;

-- 2. Insert a new current row for changed and new customers
INSERT INTO dim_customer (customer_id, city, row_hash, valid_from, valid_to, is_current)
SELECT s.customer_id, s.city, s.row_hash, CURRENT_DATE, DATE '9999-12-31', TRUE
FROM stg_customer s
LEFT JOIN dim_customer t
  ON t.customer_id = s.customer_id AND t.is_current
WHERE t.customer_id IS NULL;
```

Step 1 closes the changed rows, so step 2 finds no current row for them and inserts the new version. The order of the two steps matters.

### With dbt snapshots

dbt implements Type 2 for you:

```sql
{% snapshot dim_customer_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='check',
    check_cols=['city', 'segment']
  )
}}
select customer_id, city, segment from {{ source('crm', 'customers') }}
{% endsnapshot %}
```

dbt adds `dbt_valid_from` and `dbt_valid_to`. The current row has `dbt_valid_to` set to `NULL`, not `9999-12-31`. The `timestamp` strategy uses an `updated_at` column, and `check` compares column values.

## Joining facts to the right version

Two common ways:

1. **Store the version key in the fact at load time.** The fact table gets `customer_sk` of the version that was current on the event date. Queries are simple equi-joins.
2. **Join on the business key and the event date**, a point-in-time join:

```sql
SELECT d.city, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_customer d
  ON d.customer_id = f.customer_id
 AND f.order_date >= d.valid_from
 AND f.order_date <  d.valid_to
GROUP BY d.city;
```

## Pros and cons

| Pros | Cons |
| --- | --- |
| Complete and accurate history | The dimension grows with every change |
| Past facts stay tied to the values that were true then | More complex loads and joins |
| Works for audit and point-in-time reporting | Late-arriving changes require reopening and re-splitting versions |

## Design notes

- **Track only the attributes that matter.** Versioning every column makes row counts explode. Mix types per column.
- **Use a hash** of the tracked columns for change detection. Handle `NULL` values explicitly in the hash, or two different rows can look equal.
- **Half-open ranges** (`>= valid_from AND < valid_to`) avoid a fact matching two versions on the boundary date.
- **Late-arriving changes** (a change discovered after newer facts were loaded) need a backfill that fixes the validity ranges and the fact keys.
- **Use CDC** ([[data architecture/CDC.md|CDC]]) to receive changes as they happen, instead of diffing full snapshots.

## Related

- [[data architecture/dimensional modeling/SCD/SCD Type 1 - Overwrite.md|SCD Type 1 - Overwrite]]
- [[data architecture/dimensional modeling/SCD/SCD Type 6 - Hybrid.md|SCD Type 6 - Hybrid]]
- [[data architecture/dimensional modeling/SCD/SCD Type 7 - Dual Type 1 and 2.md|SCD Type 7 - Dual Type 1 and 2]]
