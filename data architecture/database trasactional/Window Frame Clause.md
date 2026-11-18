---
description: The frame clause of SQL window functions (ROWS or RANGE BETWEEN ... AND ...), which defines the rows each window function sees for every row, with the default frame, the difference between ROWS and RANGE for ties, and common frames such as running totals and moving averages. Child of SQL Language, used with the window aggregate and offset notes.
aliases:
  - Window frame
  - ROWS BETWEEN
  - Cláusula de frame em janela
tags:
  - sql
  - window-functions
  - interview
---
# Window Frame Clause

A **frame clause** define quais linhas da partição entram no cálculo de cada linha. Ela vale para funções de agregação em janela (`SUM`, `MAX`, `MIN`, `AVG`) e para algumas funções de valor, como `FIRST_VALUE` e `LAST_VALUE`. `ROW_NUMBER`, `RANK` e `LAG`/`LEAD` não usam frame. Ver também [[data architecture/database trasactional/Window Aggregate Functions|Window Aggregate Functions]] e [[SQL Language]].

## Sintaxe

```sql
função(...) OVER (
    PARTITION BY ...
    ORDER BY ...
    ROWS | RANGE BETWEEN início AND fim
)
```

- **`ROWS`:** conta **linhas físicas**. Cada linha é uma posição, mesmo que tenha o mesmo `ORDER BY` que outra.
- **`RANGE`:** conta **valores** de `ORDER BY`. Linhas empatadas, os "pares", entram juntas.
- **`início`:** `UNBOUNDED PRECEDING` (primeira linha da partição), `N PRECEDING` (N linhas antes) ou `CURRENT ROW`.
- **`fim`:** `CURRENT ROW`, `N FOLLOWING` ou `UNBOUNDED FOLLOWING` (última linha da partição).

## Exemplo: ROWS x RANGE com empate

```sql
with t1 as (
	select cast('2026-11-16' as date) as dt, 10 as valor
	union select cast('2026-11-17' as date), 20
	union select cast('2026-11-17' as date), 30
)
select dt, valor,
       sum(valor) over (order by dt) as range_default,
       sum(valor) over (order by dt rows between unbounded preceding and current row) as rows_explicito
from t1
```

| dt | valor | range_default | rows_explicito |
|---|---|---|---|
| 2026-11-16 | 10 | 10 | 10 |
| 2026-11-17 | 20 | 60 | 30 |
| 2026-11-17 | 30 | 60 | 60 |

- Com `RANGE`, as duas linhas de 17/11 são pares e recebem o mesmo total, 60.
- Com `ROWS`, cada linha soma até ela mesma: 30, depois 60.

## O frame padrão

O frame padrão depende do `ORDER BY`:

| Situação | Frame padrão |
|---|---|
| Com `ORDER BY` | `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| Sem `ORDER BY` | `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (partição inteira) |

Por isso `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` **não** é o padrão. É um frame explícito. O padrão é `RANGE`.

## Frames comuns

### Acumulado linha a linha

```sql
SUM(valor) OVER (ORDER BY dt
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

Cada linha recebe a soma de todas as linhas anteriores e dela mesma.

### Média móvel de 3 linhas

```sql
AVG(valor) OVER (ORDER BY dt
                 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
```

A linha atual e as duas anteriores. As primeiras linhas usam menos de três valores.

### Janela centrada

```sql
AVG(valor) OVER (ORDER BY dt
                 ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

A linha anterior, a atual e a seguinte.

### Total da partição inteira

```sql
SUM(valor) OVER (PARTITION BY grupo
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

Equivale a `SUM(valor) OVER (PARTITION BY grupo)`, sem `ORDER BY`.

## Quando usar cada um

| Necessidade | Frame |
|---|---|
| Acumulado linha a linha | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| Acumulado por data, com empates somados juntos | padrão (`RANGE`) |
| Média dos últimos N registros | `ROWS BETWEEN N-1 PRECEDING AND CURRENT ROW` |
| Total da partição | sem `ORDER BY`, ou `UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` |

## Armadilhas

- **Esquecer o frame com `ORDER BY`:** o `RANGE` padrão soma as linhas empatadas juntas, e o resultado pode parecer errado.
- **`LAST_VALUE` com frame padrão:** o frame padrão termina na linha atual, então `LAST_VALUE` devolve a própria linha. Para o último valor da partição, use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
- **Frame em `ROWS` depende da ordem:** se a ordenação não for determinística, as linhas do frame mudam entre execuções. Use um desempate.

## Pergunta de entrevista

"O que faz `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, e qual é o padrão?"

Resposta curta: a expressão define um acumulado que começa na primeira linha e termina na linha atual, contando linhas físicas. O padrão com `ORDER BY` é `RANGE`, que trata empates como pares.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/Window Aggregate Functions|Window Aggregate Functions]]
- [[data architecture/database trasactional/Window Ranking Functions|Window Ranking Functions]]
- [[data architecture/database trasactional/Window Offset Functions|Window Offset Functions]]
