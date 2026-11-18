---
description: The ANALYZE (ANALYSE) command, which collects table and column statistics for the query planner, with PostgreSQL syntax, how to check the stored statistics, when to run it manually, and the equivalent commands in other engines. Child of SQL Language, used to explain bad execution plans and for interview questions.
aliases:
  - ANALYSE
  - Coletar estatísticas SQL
  - Estatísticas do otimizador
tags:
  - sql
  - performance
  - statistics
  - interview
---
# SQL ANALYZE

`ANALYZE` (escrito `ANALYSE` também, no PostgreSQL) coleta **estatísticas** sobre uma tabela. O planejador usa essas estatísticas para estimar quantas linhas cada filtro, join e agregação vai retornar, e assim escolher o plano. Estatísticas desatualizadas levam a planos ruins, mesmo com os índices certos. Ver também [[SQL Language]] e [[data architecture/database trasactional/SQL EXPLAIN|SQL EXPLAIN]].

`ANALYZE` não é o `EXPLAIN ANALYZE`. O primeiro coleta estatísticas. O segundo executa a consulta e mostra o plano com tempos reais.

## Sintaxe (PostgreSQL)

```sql
ANALYZE pedidos;                          -- tabela inteira
ANALYZE pedidos (cliente_id, data_pedido); -- só algumas colunas, mais rápido
ANALYZE VERBOSE pedidos;                  -- mostra o progresso
ANALYZE;                                  -- todas as tabelas do banco
```

## O que é coletado

Para cada coluna, o banco guarda:

- **`null_frac`:** fração de valores NULL.
- **`n_distinct`:** número estimado de valores distintos.
- **`most_common_vals` e `most_common_freqs`:** os valores mais frequentes e suas frações.
- **Histograma:** a distribuição dos demais valores, usado para estimar faixas de filtro.
- **Tamanho médio** dos valores e número de páginas da tabela.

Com essas informações, o planejador estima quantas linhas um filtro como `WHERE cliente_id = 10` vai retornar. A estimativa define se vale usar um índice ou um `Seq Scan`, e qual join usar.

## Como verificar

```sql
-- Estatísticas por coluna
SELECT attname, n_distinct, null_frac, most_common_vals
FROM pg_stats
WHERE tablename = 'pedidos';

-- Quando a tabela foi analisada
SELECT relname, last_analyze, last_autoanalyze
FROM pg_stat_user_tables
WHERE relname = 'pedidos';
```

## Autovacuum

O autovacuum executa `ANALYZE` automaticamente quando a tabela muda o suficiente. Ele é o caminho normal. O comando manual é para situações pontuais.

## Quando rodar manualmente

- **Depois de uma carga grande**, como um `INSERT` de milhões de linhas ou um `COPY`, antes que o autovacuum reanalise.
- **Quando o `EXPLAIN ANALYZE` mostra estimativas muito diferentes do real.** Rode `ANALYZE` e compare o plano de novo.
- **Quando a distribuição mudou muito**, por exemplo um valor passou a dominar a coluna.

## Sinal de estatística ruim no plano

```text
Seq Scan on pedidos  (cost=... rows=10) (actual ... rows=500000)
```

Estimativa de 10 linhas para uma leitura de 500 mil indica estatística desatualizada. Essa é a situação em que o `ANALYZE` resolve.

## Equivalentes em outros bancos

| Banco | Comando |
|---|---|
| PostgreSQL | `ANALYZE pedidos;` |
| MySQL | `ANALYZE TABLE pedidos;` |
| SQL Server | `UPDATE STATISTICS pedidos;` |
| Oracle | `DBMS_STATS.GATHER_TABLE_STATS(...)` |
| Spark SQL | `ANALYZE TABLE pedidos COMPUTE STATISTICS;` |

Detalhes de cada um estão no hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]].

## Armadilhas

- **`ANALYZE` não é `VACUUM`.** `ANALYZE` atualiza estatísticas. `VACUUM` recupera espaço de linhas removidas.
- **Amostragem:** o `ANALYZE` lê uma amostra da tabela, então as estatísticas são aproximadas em tabelas grandes.
- **Permissão:** só o dono da tabela, ou um superusuário, pode executar `ANALYZE`.
- **Não substitui índice:** estatística boa ajuda o planejador a escolher, mas não cria índice.

## Pergunta de entrevista

"Quando você rodaria `ANALYZE` manualmente?"

Resposta curta: depois de cargas grandes ou mudanças fortes na distribuição, ou quando o `EXPLAIN ANALYZE` mostra estimativas muito diferentes do real. Em produção, o autovacuum cuida da maior parte.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/SQL EXPLAIN|SQL EXPLAIN]]
- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - PostgreSQL|SQL Dialect - PostgreSQL]]
