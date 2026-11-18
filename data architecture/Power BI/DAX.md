---
description: DAX (Data Analysis Expressions), the formula language of Power BI, Analysis Services Tabular and Power Pivot, used to write measures, calculated columns and row-level security over a loaded data model. Covers filter and row context, CALCULATE, time intelligence and common mistakes.
aliases:
  - Data Analysis Expressions
  - DAX Power BI
tags:
  - dax
  - bi
  - power-bi
---
# DAX

**DAX** (Data Analysis Expressions) is the formula language of Power BI, also used in Analysis Services (Tabular) and Power Pivot for Excel. It calculates over a model that is already loaded: measures, calculated columns, calculated tables and RLS filters.

The key idea is **context**. A measure is not computed once. Power BI evaluates it for each cell of a visual, using the filters of that cell. The same `[Receita]` measure shows the company total in a card and the value per product in a table.

Compared with SQL, you do not write the `WHERE` or the `GROUP BY`. You write `Receita = SUM ( Vendas[Valor] )`, and the filters and grouping come from the visual, the slicers and the page filters.

## Measure vs calculated column

| Aspect | Calculated column | Measure |
|---|---|---|
| When it is computed | At refresh, row by row | At query time, in each visual cell |
| Storage | Stored in the model, uses memory | Not stored |
| Reacts to filters | No, each row has a fixed value | Yes, changes with slicers and visuals |
| Typical use | Classify or group rows, such as a price band | Aggregations and KPIs: revenue, margin, % |

Use a measure for aggregations.

## Filter context and row context

- **Filter context:** the filters active when the measure is evaluated. They flow through relationships from dimensions to the fact table, which is why DAX works best on a [[data architecture/dimensional modeling/Star schema|star schema]].
- **Row context:** the "current row" while a table is iterated. It exists in calculated columns and in iterator functions (the ones ending in X). By itself it filters nothing.

`SUM` adds a column. `SUMX` walks a table, evaluates an expression on each row and adds the results:

```dax
Receita = SUMX ( Vendas, Vendas[Quantidade] * Vendas[Preço] )
```

## CALCULATE

The most important DAX function. It evaluates an expression with modified filters, like changing the `WHERE` clause:

```dax
Receita Brasil = CALCULATE ( [Receita], Cliente[País] = "Brasil" )
% do Total = DIVIDE ( [Receita], CALCULATE ( [Receita], ALL ( Produto ) ) )
```

In the second example, `ALL ( Produto )` removes the product filter, so the denominator is the revenue of all products.

**Context transition:** when `CALCULATE` runs inside a row context, the current row becomes a filter. In a calculated column on the Cliente table:
- `SUM ( Vendas[Valor] )` returns the grand total on every row.
- `CALCULATE ( SUM ( Vendas[Valor] ) )` returns the sales of each customer.

## Variables

`VAR` stores an intermediate result. It makes long formulas readable and avoids computing the same expression twice:

```dax
Margem % =
VAR Lucro = [Receita] - [Custo]
RETURN DIVIDE ( Lucro, [Receita] )
```

## Time intelligence

Functions such as `TOTALYTD`, `SAMEPERIODLASTYEAR` and `DATEADD` need a **date table** with continuous dates, marked as a date table in the model.

```dax
Receita AA = CALCULATE ( [Receita], SAMEPERIODLASTYEAR ( 'Calendário'[Data] ) )
Var % AA = DIVIDE ( [Receita] - [Receita AA], [Receita AA] )
Receita YTD = TOTALYTD ( [Receita], 'Calendário'[Data] )
```

"AA" means previous year.

## Examples for FP&A

```dax
Margem = [Receita] - [Custo]
Margem % = DIVIDE ( [Margem], [Receita] )
Desvio vs Orçado = [Realizado] - [Orçado]
```

## Row-level security

A role with a DAX filter restricts the rows a user sees. A static role uses a fixed value. A dynamic role uses the signed-in user, for example `USERPRINCIPALNAME()` compared with a table of user permissions. 

## Common mistakes

- **Total does not match the sum of the rows:** the total of a table is the same measure evaluated with fewer filters. This shows up with averages, distinct counts and percentages. To sum the rows, use `SUMX ( VALUES ( Produto[Nome] ), [Medida] )`.
- Using `/` instead of `DIVIDE`. `DIVIDE` handles division by zero.
- Writing a calculated column where a measure is needed.
- Using bidirectional relationships without need, which causes ambiguity and slows the model.

## Performance

- Store intermediate results with `VAR`.
- Keep the model a star schema, and move transformations to the warehouse or Power Query.
- Avoid `FILTER` over a whole fact table when a simple filter argument to `CALCULATE` does the job.
- Measure with Performance Analyzer in Power BI Desktop and with DAX Studio.

## DAX and Power Query (M)

Power Query prepares data before the load: it cleans, joins and types the tables. DAX calculates afterwards, over the loaded model. Do the transformations as early as possible, in the warehouse or in Power Query, and leave for DAX only what depends on the user's filters.

## Related

- [[data architecture/dimensional modeling/Star schema|Star schema]]
- [[data architecture/dimensional modeling/dimensional modeling|Dimensional modeling]]
