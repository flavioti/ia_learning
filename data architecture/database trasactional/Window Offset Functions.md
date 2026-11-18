---
description: The offset window functions LAG and LEAD, which read a value from a previous or next row inside a window, with default values, partitions, and common uses such as period-over-period change and gap detection. Child of SQL Language, used for analytics queries and interview questions.
aliases:
  - LAG LEAD
  - Funções de deslocamento em janela
tags:
  - sql
  - window-functions
  - interview
---
# Window Offset Functions

`LAG` e `LEAD` leem o valor de uma linha **anterior** (`LAG`) ou **seguinte** (`LEAD`) dentro da janela, sem fazer join. Ver também [[SQL Language]] e [[data architecture/database trasactional/Window Aggregate Functions|Window Aggregate Functions]].

![[lag and lead.excalidraw|1024]]

## Sintaxe

```sql
LAG(coluna, deslocamento, valor_padrao) OVER (PARTITION BY ... ORDER BY ...)
LEAD(coluna, deslocamento, valor_padrao) OVER (PARTITION BY ... ORDER BY ...)
```

- **`coluna`:** o valor a ser lido.
- **`deslocamento`:** quantas linhas voltar ou avançar. O padrão é 1.
- **`valor_padrao`:** o que retornar quando não existe linha anterior ou seguinte. O padrão é NULL.
- **`ORDER BY`** define a sequência. Sem ele, "anterior" e "seguinte" não têm sentido.

## Dados de exemplo

Tabela `vendas_mensais`, com o total de cada mês:

| mes | total |
|---|---|
| 2026-01 | 100 |
| 2026-02 | 150 |
| 2026-03 | 120 |
| 2026-04 | 180 |

## LAG: valor do mês anterior

```sql
SELECT mes, total,
       LAG(total) OVER (ORDER BY mes) AS total_anterior,
       total - LAG(total) OVER (ORDER BY mes) AS variacao
FROM vendas_mensais;
```

| mes | total | total_anterior | variacao |
|---|---|---|---|
| 2026-01 | 100 | NULL | NULL |
| 2026-02 | 150 | 100 | 50 |
| 2026-03 | 120 | 150 | -30 |
| 2026-04 | 180 | 120 | 60 |

A primeira linha não tem anterior, então retorna NULL e a variação também fica NULL.

Para variação percentual, divida pela linha anterior:

```sql
SELECT mes, total,
       ROUND((total - LAG(total) OVER (ORDER BY mes)) * 100.0
             / NULLIF(LAG(total) OVER (ORDER BY mes), 0), 1) AS var_pct
FROM vendas_mensais;
```

`NULLIF` evita divisão por zero quando o mês anterior tem total zero.

## LEAD: valor do mês seguinte

```sql
SELECT mes, total,
       LEAD(total) OVER (ORDER BY mes) AS proximo_total
FROM vendas_mensais;
```

| mes | total | proximo_total |
|---|---|---|
| 2026-01 | 100 | 150 |
| 2026-02 | 150 | 120 |
| 2026-03 | 120 | 180 |
| 2026-04 | 180 | NULL |

Use `LEAD` quando a linha precisa olhar o futuro, por exemplo para saber quando um evento terminou.

## Valor padrão e deslocamento

```sql
-- Retorna 0 em vez de NULL na primeira linha, e olha duas linhas atrás
SELECT mes, total,
       LAG(total, 2, 0) OVER (ORDER BY mes) AS total_dois_meses_antes
FROM vendas_mensais;
```

## PARTITION BY: reiniciar por grupo

Com `PARTITION BY`, a sequência reinicia em cada grupo. Assim, o mês anterior de janeiro de 2026 não vem de dezembro de 2025 de outro cliente:

```sql
SELECT cliente_id, mes, total,
       LAG(total) OVER (PARTITION BY cliente_id ORDER BY mes) AS total_anterior
FROM vendas_cliente_mensal;
```

## Usos comuns

- **Variação entre períodos:** LAG, para comparar com o mês ou dia anterior.
- **Detecção de intervalo:** LAG da data, para encontrar lacunas entre eventos. Por exemplo, uma sessão que começou depois de mais de 30 minutos do fim da anterior.
- **Sessionização:** LAG do timestamp, marcando um novo grupo quando a diferença passa de um limite.
- **Fim de evento:** LEAD da data de início, para calcular a duração até o próximo evento.
- **Mudança de estado:** comparar o status atual com o anterior e registrar só as transições.

```sql
-- Detecta quando o status de um cliente muda
SELECT cliente_id, data_evento, status
FROM (
    SELECT cliente_id, data_evento, status,
           LAG(status) OVER (PARTITION BY cliente_id ORDER BY data_evento) AS status_anterior
    FROM eventos_cliente
) t
WHERE status <> status_anterior OR status_anterior IS NULL;
```
## Exemplos com dados inline

Os exemplos abaixo usam uma CTE com `UNION`, para rodar sem tabela. Os resultados já estão calculados.

### LAG: evento anterior

```sql
with t1 as (
	select cast('2026-11-18' as date) as dt, 'climb' as eventx
	union select cast('2026-11-17' as date), 'run'
	union select cast('2026-11-16' as date), 'swin'
)
select *, lag(eventx) over (order by dt desc) as previous_event
from t1
```

| dt | eventx | previous_event |
|---|---|---|
| 2026-11-18 | climb | NULL |
| 2026-11-17 | run | climb |
| 2026-11-16 | swin | run |

A ordenação é `dt desc`, então "anterior" significa o dia mais recente antes da linha. Na primeira linha não há anterior, e o resultado é NULL.

### LEAD: evento seguinte

```sql
with t1 as (
	select cast('2026-11-18' as date) as dt, 'climb' as eventx
	union select cast('2026-11-17' as date), 'run'
	union select cast('2026-11-16' as date), 'swin'
)
select *, lead(eventx) over (order by dt desc) as next_event
from t1
```

| dt | eventx | next_event |
|---|---|---|
| 2026-11-18 | climb | run |
| 2026-11-17 | run | swin |
| 2026-11-16 | swin | NULL |

Com a mesma ordenação, `LEAD` olha para o dia anterior no calendário, porque a sequência é decrescente. Se quiser o evento do dia seguinte no calendário, use `order by dt asc`.

### LAG com deslocamento e valor padrão

```sql
with t1 as (
	select cast('2026-11-18' as date) as dt, 'climb' as eventx
	union select cast('2026-11-17' as date), 'run'
	union select cast('2026-11-16' as date), 'swin'
)
select *, lag(eventx, 2, 'sem evento') over (order by dt desc) as evento_2_dias_antes
from t1
```

| dt | eventx | evento_2_dias_antes |
|---|---|---|
| 2026-11-18 | climb | sem evento |
| 2026-11-17 | run | sem evento |
| 2026-11-16 | swin | climb |

O deslocamento 2 olha duas linhas para trás. As duas primeiras linhas não têm esse anterior, então recebem o valor padrão.

### Duração entre eventos

Calcula quantos dias se passaram desde o evento anterior, com `LAG` da data:

```sql
with t1 as (
	select cast('2026-11-18' as date) as dt, 'climb' as eventx
	union select cast('2026-11-17' as date), 'run'
	union select cast('2026-11-16' as date), 'swin'
)
select dt, eventx,
       dt - lag(dt) over (order by dt) as dias_desde_o_anterior
from t1
order by dt
```

| dt | eventx | dias_desde_o_anterior |
|---|---|---|
| 2026-11-16 | swin | NULL |
| 2026-11-17 | run | 1 |
| 2026-11-18 | climb | 1 |

Esse padrão serve para detectar lacunas: um valor maior que o esperado indica que houve um período sem eventos.

Obs.: a subtração de datas que devolve número de dias é específica de alguns dialetos. No PostgreSQL, `dt - lag(dt)` retorna inteiro. Em outros bancos, use `DATEDIFF` ou `date_diff`.

## Armadilhas

- **Sem `ORDER BY` a sequência é indefinida.** O resultado pode mudar entre execuções.
- **NULL na coluna:** se o valor anterior for NULL, `LAG` retorna NULL, e comparações com `<>` também dão NULL. O filtro acima trata isso com `IS NULL`.
- **Ordem com empates:** se duas linhas têm o mesmo `ORDER BY`, a ordem entre elas não é garantida. Use uma coluna de desempate.
- **`LAG` e `LEAD` não filtram:** eles só olham a sequência ordenada. Se você filtrar linhas no `WHERE` antes da janela, a sequência muda.

## Pergunta de entrevista

"Como você calcula a variação em relação ao mês anterior?"

Resposta curta: `LAG` sobre a coluna de total, ordenado pelo mês, dentro do mesmo cliente se houver partição. Depois, subtrai ou divide pelo valor retornado, com `NULLIF` para evitar divisão por zero.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/Window Aggregate Functions|Window Aggregate Functions]]
- [[data architecture/database trasactional/Window Ranking Functions|Window Ranking Functions]]
