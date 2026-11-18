---
description: Hub that compares the SQL commands which change between database engines (statistics, execution plans, row limits, upsert, transactions, identifier quoting), linking to one note per engine. Child of SQL Language, used to avoid mixing dialect syntax in queries and interviews.
aliases:
  - SQL dialects
  - Dialetos SQL
tags:
  - sql
  - dialects
  - interview
---
# SQL Dialects

O SQL padrão é parecido entre bancos, mas os **comandos de manutenção, diagnóstico e algumas funções** mudam. Esta nota compara os mais usados. Detalhes de cada banco estão nas notas filhas. Ver também [[SQL Language]].

## Comparação

| Tarefa | PostgreSQL | MySQL | SQL Server | Oracle | Spark SQL |
|---|---|---|---|---|---|
| Coletar estatísticas | `ANALYZE t` | `ANALYZE TABLE t` | `UPDATE STATISTICS t` | `DBMS_STATS.GATHER_TABLE_STATS` | `ANALYZE TABLE t COMPUTE STATISTICS` |
| Plano estimado | `EXPLAIN` | `EXPLAIN` | plano estimado do cliente ou `SET SHOWPLAN_ALL ON` | `EXPLAIN PLAN FOR` + `DBMS_XPLAN` | `EXPLAIN` |
| Plano com execução real | `EXPLAIN ANALYZE` | `EXPLAIN ANALYZE` (8.0.18+) | plano real do cliente | não há equivalente direto no mesmo comando | não há; usar a Spark UI |
| Limitar linhas | `LIMIT n` | `LIMIT n` | `TOP n` ou `OFFSET ... FETCH` | `FETCH FIRST n ROWS ONLY` (12c+) | `LIMIT n` |
| Upsert | `INSERT ... ON CONFLICT` | `INSERT ... ON DUPLICATE KEY UPDATE` | `MERGE` | `MERGE` | `MERGE INTO` (Delta) |
| Iniciar transação | `BEGIN` | `START TRANSACTION` | `BEGIN TRANSACTION` | implícita; `COMMIT` e `ROLLBACK` | não se aplica no Spark puro; Delta tem ACID |
| Quotar identificador | `"nome"` | `` `nome` `` | `[nome]` ou `"nome"` | `"NOME"` | `` `nome` `` |
| `FULL OUTER JOIN` | sim | não nativo | sim | sim | sim |

## Pontos que mais causam erro

- **`LIMIT` não existe no SQL Server nem no Oracle antigo.** Use `TOP` ou `FETCH`.
- **`FULL OUTER JOIN` não existe nativamente no MySQL.** Para simular, combine `LEFT JOIN` e `RIGHT JOIN` com `UNION`.
- **`ANALYZE` não é universal.** Veja a linha de estatísticas acima.
- **`MERGE` tem sintaxe diferente** em SQL Server, Oracle e Spark. Não copie um bloco de um banco para outro.
- **Aspas em identificadores** mudam, e isso quebra consultas copiadas entre bancos.

## Notas por banco

- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - PostgreSQL|PostgreSQL]]
- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - MySQL|MySQL]]
- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - SQL Server|SQL Server]]
- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - Oracle|Oracle]]
- [[data architecture/database trasactional/SQL Dialects/SQL Dialect - Spark SQL|Spark SQL]]

## Pergunta de entrevista

"O SQL é padrão? O que muda entre bancos?"

Resposta curta: a linguagem de consulta é parecida, mas comandos de manutenção, planos de execução, limite de linhas, upsert e transações têm sintaxe própria. Por isso, ao trocar de banco, eu confiro essas partes antes de rodar a consulta.
