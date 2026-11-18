---
description: Spark SQL commands (ANALYZE TABLE COMPUTE STATISTICS, EXPLAIN EXTENDED or FORMATTED, LIMIT, MERGE INTO with Delta, backtick quoting, LEFT SEMI and LEFT ANTI joins) compared with other engines. Child of SQL Dialects, used when writing or diagnosing queries on Spark or Databricks.
aliases:
  - Spark SQL
tags:
  - sql
  - spark
  - dialects
---
# SQL Dialect - Spark SQL

Comandos e sintaxe próprios do Spark SQL, usados também no Databricks. Ver o hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]] e [[data architecture/Apache Spark/Apache Spark|Apache Spark]].

## Estatísticas

```sql
ANALYZE TABLE pedidos COMPUTE STATISTICS;
ANALYZE TABLE pedidos COMPUTE STATISTICS FOR COLUMNS cliente_id, data_pedido;
```

As estatísticas alimentam o otimizador, por exemplo para escolher `BroadcastHashJoin`.

## Plano de execução

```sql
EXPLAIN SELECT * FROM pedidos WHERE cliente_id = 10;
EXPLAIN EXTENDED SELECT * FROM pedidos WHERE cliente_id = 10;   -- planos lógico e físico
EXPLAIN FORMATTED SELECT * FROM pedidos WHERE cliente_id = 10;  -- formato mais legível
```

## Limite

```sql
SELECT * FROM pedidos ORDER BY id LIMIT 10;
```

Não há `OFFSET` no Spark SQL, use uma window function ou `row_number()` para paginar.

## Upsert

Com Delta Lake:

```sql
MERGE INTO clientes alvo
USING novos origem
ON alvo.id = origem.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Tabelas Parquet simples não têm `MERGE`.

## Transações

O Spark não tem `BEGIN` e `COMMIT` como um banco transacional. O Delta Lake oferece transações ACID por tabela. Veja [[data architecture/Data Lakehouse/Data Lakehouse|Data Lakehouse]].

## Identificadores

Use crase: `` `nome` ``.

## Joins semi e anti

```sql
SELECT * FROM clientes c LEFT SEMI JOIN pedidos p ON p.cliente_id = c.id;
SELECT * FROM clientes c LEFT ANTI JOIN pedidos p ON p.cliente_id = c.id;
```

Ao contrário do PostgreSQL e do MySQL, o Spark SQL aceita essas palavras-chave diretamente.

## Armadilhas

- `ANALYZE TABLE` não é executado sozinho em todas as tabelas. Rode após cargas grandes.
- `EXPLAIN` no Spark mostra o plano sem executar. Para o tempo real, use a Spark UI.
