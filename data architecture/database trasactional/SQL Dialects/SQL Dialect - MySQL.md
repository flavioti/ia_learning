---
description: MySQL-specific SQL commands (ANALYZE TABLE, EXPLAIN ANALYZE from 8.0.18, LIMIT, ON DUPLICATE KEY UPDATE, backtick quoting) and the missing FULL OUTER JOIN, compared with other engines. Child of SQL Dialects, used when writing or diagnosing queries on MySQL.
aliases:
  - MySQL SQL
tags:
  - sql
  - mysql
  - dialects
---
# SQL Dialect - MySQL

Comandos e sintaxe próprios do MySQL. Ver o hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]] e o produto em [[data architecture/database trasactional/MySQL|MySQL]].

## Estatísticas

```sql
ANALYZE TABLE pedidos;
```

O comando usa a palavra `TABLE`, diferente do `ANALYZE` do PostgreSQL.

## Plano de execução

```sql
EXPLAIN SELECT * FROM pedidos WHERE cliente_id = 10;
EXPLAIN ANALYZE SELECT * FROM pedidos WHERE cliente_id = 10;   -- MySQL 8.0.18+
```

`EXPLAIN ANALYZE` executa a consulta. Confirme a versão antes de usar.

## Limite e paginação

```sql
SELECT * FROM pedidos ORDER BY id LIMIT 10 OFFSET 20;
```

## Upsert

```sql
INSERT INTO clientes (id, nome) VALUES (1, 'Ana')
ON DUPLICATE KEY UPDATE nome = VALUES(nome);
```

No MySQL 8.0.20+, `VALUES()` está marcado como obsoleto. A alternativa é um alias na linha inserida, como `AS novo ON DUPLICATE KEY UPDATE nome = novo.nome`. Confirme na documentação da versão.

## Transações

```sql
START TRANSACTION;
-- consultas
COMMIT;
```

## Identificadores

Use crase: `` `nome` ``. Aspas duplas são strings, não identificadores, por padrão.

## Armadilhas

- **Sem `FULL OUTER JOIN`.** Simule com `LEFT JOIN` + `RIGHT JOIN` + `UNION`:

```sql
SELECT c.nome, p.valor FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id
UNION
SELECT c.nome, p.valor FROM clientes c RIGHT JOIN pedidos p ON p.cliente_id = c.id;
```

- **Sem `SEMI JOIN` ou `ANTI JOIN` como palavras-chave.** Use `EXISTS` e `NOT EXISTS`.
