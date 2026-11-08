---
aliases:
  - SCD
  - Slowly Changing Dimensions
tags:
  - data-warehouse
---

**Slowly Changing Dimensions (SCD)** are dimension attributes that change rarely and unpredictably over time, such as a customer's city, a product's category or an employee's department. Because a data warehouse is used to analyze history, each SCD type is a strategy that answers one question: when an attribute changes, do we **overwrite** the old value or **keep the history**?

Without a strategy, a change silently rewrites the past. If a customer moves from São Paulo to Recife, a report of last year's sales by city would wrongly assign those sales to Recife.

## SCD types

| Type  | Strategy                                             | History kept                          | Typical use                                                 |
| ----- | ---------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------- |
| **0** | Retain: the value never changes after the first load | Original only                         | Immutable attributes (birth date, original signup channel)  |
| **1** | Overwrite the old value                              | None                                  | Corrections and attributes where history is irrelevant      |
| **2** | Add a new row per change                             | Full                                  | Most analytical dimensions (the default choice)             |
| **3** | Add a column for the previous value                  | Last value only                       | A single known change, such as a reorganization             |
| **4** | Move history to a separate history table             | Full, in another table                | Frequently changing attributes with a small "current" table |
| **6** | Hybrid of types 1 + 2 + 3                            | Full, plus current value on every row | Reports needing both historical and current values          |

### Type 1: overwrite

The row is updated in place. Simple and cheap, but history is lost and previously loaded facts now appear under the new value.

### Type 2: new row per change

Each change closes the current row and inserts a new one. A **surrogate key** identifies each version, while the **business key** (natural key) stays the same across versions.

Before the change:

| customer_sk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | 2024-01-01 | 9999-12-31 | true |

After the customer moves to Recife on 2026-03-01:

| customer_sk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 1 | C-100 | São Paulo | 2024-01-01 | 2026-03-01 | false |
| 2 | C-100 | Recife | 2026-03-01 | 9999-12-31 | true |

Facts loaded before the move keep pointing to `customer_sk = 1`, and new facts point to `customer_sk = 2`. This is how the report above stays correct. An open-ended `valid_to` such as `9999-12-31` (instead of `NULL`) makes range joins simpler.

### Type 3: previous-value column

| customer_id | city | previous_city |
|---|---|---|
| C-100 | Recife | São Paulo |

Only one level of history is kept, so a second move loses the oldest value.

## Implementing type 2

A type 2 load compares the incoming data with the current rows, closes the changed ones and inserts the new versions. In SQL this is usually done with `MERGE` (or an `UPDATE` followed by an `INSERT`):

```sql
-- 1. Close current rows whose tracked attribute changed
MERGE INTO dim_customer AS t
USING stg_customer AS s
  ON t.customer_id = s.customer_id AND t.is_current
WHEN MATCHED AND t.city <> s.city THEN
  UPDATE SET valid_to = CURRENT_DATE, is_current = FALSE;

-- 2. Insert a new current row for changed and new customers
INSERT INTO dim_customer (customer_id, city, valid_from, valid_to, is_current)
SELECT s.customer_id, s.city, CURRENT_DATE, DATE '9999-12-31', TRUE
FROM stg_customer s
LEFT JOIN dim_customer t
  ON t.customer_id = s.customer_id AND t.is_current
WHERE t.customer_id IS NULL;
```

Tools often provide this out of the box: dbt **snapshots** implement type 2 (with `strategy='timestamp'` or `'check'`), and Delta Lake, Apache Iceberg and Snowflake support `MERGE` for the pattern.

## Design notes

- **Track only the attributes that matter.** Versioning every column explodes row counts. Mix types per attribute: type 1 for typo fixes, type 2 for business-relevant changes.
- **Detect changes reliably.** Compare column values or a hash of the tracked columns, or use [[data architecture/CDC.md|CDC]] to receive changes as they happen from the source instead of diffing full snapshots.
- **Join facts on the right version.** Either store the surrogate key in the fact at load time, or join on the business key and the event date falling inside `valid_from`/`valid_to`.
- **Late-arriving changes** (a change that is discovered after newer facts were loaded) require reopening and re-splitting versions, so plan for backfills.
- **Wide, denormalized models** such as [[OBT - One Big Table|OBT]] make SCDs hard: a changed value must be rewritten on many rows, or the history must be baked into the table at build time.

## Related

- [[data architecture/CDC.md|CDC]]
- [[data architecture/dimensional modeling/Star schema.md|Star schema]]
- [[OBT - One Big Table|OBT - One Big Table]]
