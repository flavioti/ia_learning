---
description: PostgreSQL-specific SQL commands (ANALYZE, EXPLAIN ANALYZE, LIMIT, INSERT ON CONFLICT, transactions, date_trunc and casts), compared with other engines. Child of SQL Dialects, used when writing or diagnosing queries on PostgreSQL.
aliases:
  - PostgreSQL SQL
tags:
  - sql
  - postgresql
  - dialects
---
# SQL Dialect - PostgreSQL

Comandos e sintaxe próprios do PostgreSQL. Ver o hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]] e o produto em [[data architecture/database trasactional/Postgres|Postgres]].

## Estatísticas

```sql
ANALYZE pedidos;                       -- também aceito como ANALYSE
ANALYZE VERBOSE pedidos;
ANALYZE pedidos (cliente_id, data_pedido);
```

O autovacuum executa `ANALYZE` automaticamente. Use o manual depois de cargas grandes. Ver [[data architecture/database trasactional/SQL EXPLAIN|SQL EXPLAIN]].

## Plano de execução

```sql
EXPLAIN SELECT * FROM pedidos WHERE cliente_id = 10;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM pedidos WHERE cliente_id = 10;
```

`EXPLAIN (ANALYZE, BUFFERS)` executa a consulta e mostra também os blocos lidos do cache e do disco.

## Limite e paginação

```sql
SELECT * FROM pedidos ORDER BY id LIMIT 10 OFFSET 20;
```

## Upsert

```sql
INSERT INTO clientes (id, nome) VALUES (1, 'Ana')
ON CONFLICT (id) DO UPDATE SET nome = EXCLUDED.nome;
```

`EXCLUDED` é a linha que tentou ser inserida.

## Transações

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
-- consultas
COMMIT;
```

No `psql`, o modo padrão é *autocommit*: cada comando é confirmado sozinho.

## Funções de data e conversão

```sql
SELECT date_trunc('month', data_venda)::date AS mes FROM vendas;
```

`::` é o cast do PostgreSQL. Em SQL padrão, use `CAST(x AS tipo)`.

## Armadilhas

- Identificadores sem aspas são convertidos para minúsculas. `SELECT Nome` busca `nome`. Com aspas duplas, o nome é preservado.
- `ANALYZE` e `VACUUM` são comandos diferentes: o primeiro coleta estatísticas, o segundo recupera espaço.
