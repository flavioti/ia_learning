---
description: Aggregate functions used as window functions (SUM, MAX and MIN with OVER), showing how each row keeps its detail while receiving a total, running value, or group maximum and minimum from a PARTITION BY and ORDER BY window. Child of SQL Language, used for analytics queries and interview questions.
aliases:
  - SUM OVER MAX OVER MIN OVER
  - Funções de agregação em janela
tags:
  - sql
  - window-functions
  - interview
---
# Window Aggregate Functions

`SUM`, `MAX` e `MIN` com `OVER` calculam um valor sobre uma janela de linhas, **sem agrupar**. Cada linha continua no resultado e recebe o valor agregado ao lado. Ver também [[SQL Language]] e [[data architecture/database trasactional/Window Ranking Functions|Window Ranking Functions]].

A diferença para o `GROUP BY`: com `GROUP BY`, as linhas somem e sobra uma por grupo. Com `OVER`, todas permanecem.

## Dados de exemplo

Tabela `vendas`:

| data_venda | mes | valor |
|---|---|---|
| 2026-01-01 | jan | 10 |
| 2026-01-02 | jan | 30 |
| 2026-01-03 | jan | 20 |
| 2026-02-01 | fev | 50 |

## Sintaxe e exemplos

```sql
SELECT data_venda, mes, valor,
       SUM(valor) OVER ()                                AS total_geral,
       SUM(valor) OVER (ORDER BY data_venda)             AS acumulado,
       SUM(valor) OVER (PARTITION BY mes)                AS total_mes,
       MAX(valor) OVER (PARTITION BY mes)                AS max_mes,
       MIN(valor) OVER (PARTITION BY mes)                AS min_mes
FROM vendas
ORDER BY data_venda;
```

| data_venda | mes | valor | total_geral | acumulado | total_mes | max_mes | min_mes |
|---|---|---|---|---|---|---|---|
| 2026-01-01 | jan | 10 | 110 | 10 | 60 | 30 | 10 |
| 2026-01-02 | jan | 30 | 110 | 40 | 60 | 30 | 10 |
| 2026-01-03 | jan | 20 | 110 | 60 | 60 | 30 | 10 |
| 2026-02-01 | fev | 50 | 110 | 110 | 50 | 50 | 50 |

## Como ler cada janela

- **`OVER ()`:** a janela é a tabela inteira. `total_geral` é 110 em todas as linhas.
- **`OVER (ORDER BY data_venda)`:** soma acumulada, do início até a linha atual. É a base de saldo acumulado e de receita acumulada.
- **`OVER (PARTITION BY mes)`:** a janela é só o grupo do mês. `total_mes` é 60 para janeiro e 50 para fevereiro, mas as linhas continuam individuais.
- **`MAX` e `MIN` com `PARTITION BY`:** o maior e o menor valor do grupo, repetidos em cada linha. Útil para comparar cada linha com o extremo do grupo.

## Porcentagem do total

Um uso frequente em análise é dividir a linha pelo total da janela:

```sql
SELECT data_venda, valor,
       valor * 100.0 / SUM(valor) OVER () AS pct_do_total
FROM vendas;
```

Para janeiro, 10 representa 9,1% do total de 110.

## Armadilha: o frame padrão com ORDER BY

Quando há `ORDER BY` e nenhum frame explícito, o padrão é `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Linhas com a **mesma data** são tratadas como "pares" e recebem o mesmo acumulado.

Se houver duas vendas em 2026-01-02, por exemplo, as duas recebem a soma das duas juntas. Para uma soma linha a linha, use o frame explícito (detalhes em [[data architecture/database trasactional/Window Frame Clause|Window Frame Clause]]):

```sql
SELECT data_venda, valor,
       SUM(valor) OVER (ORDER BY data_venda
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado
FROM vendas;
```

Para uma média móvel de 3 linhas, troque o frame por `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.

## Quando usar

| Necessidade | Expressão |
|---|---|
| Total geral em cada linha | `SUM(x) OVER ()` |
| Saldo ou receita acumulada | `SUM(x) OVER (ORDER BY data)` |
| Total por grupo sem perder as linhas | `SUM(x) OVER (PARTITION BY grupo)` |
| Comparar a linha com o máximo ou mínimo do grupo | `MAX(x) OVER (PARTITION BY grupo)` |
| Diferença para o máximo do grupo | `x - MAX(x) OVER (PARTITION BY grupo)` |

## Pergunta de entrevista

"Qual a diferença entre `GROUP BY` e `SUM() OVER (PARTITION BY ...)`?"

Resposta curta: o `GROUP BY` reduz as linhas a uma por grupo. O `OVER` calcula o mesmo agregado, mas mantém todas as linhas, o que permite comparar cada detalhe com o total do seu grupo.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/Window Ranking Functions|Window Ranking Functions]]
- [[data architecture/database trasactional/Basic SQL Examples|Basic SQL Examples]]
