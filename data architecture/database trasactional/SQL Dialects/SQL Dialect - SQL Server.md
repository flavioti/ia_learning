---
description: Microsoft SQL Server commands (UPDATE STATISTICS, execution plans with SET SHOWPLAN and STATISTICS IO, TOP and OFFSET FETCH, MERGE, bracket quoting) compared with other engines. Child of SQL Dialects, used when writing or diagnosing queries on SQL Server.
aliases:
  - T-SQL
  - MS SQL Server
tags:
  - sql
  - sql-server
  - dialects
---
# SQL Dialect - SQL Server

Comandos e sintaxe próprios do SQL Server (T-SQL). Ver o hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]].

## Estatísticas

```sql
UPDATE STATISTICS pedidos;
```

Não existe um comando `ANALYZE` no SQL Server.

## Plano de execução

```sql
SET SHOWPLAN_ALL ON;      -- plano estimado, sem executar
GO
SELECT * FROM pedidos WHERE cliente_id = 10;
GO
SET SHOWPLAN_ALL OFF;
```

Para o plano real, use o botão *Include Actual Execution Plan* do SQL Server Management Studio, ou `SET STATISTICS PROFILE ON`. Para contar leituras de página, use `SET STATISTICS IO ON`.

## Limite e paginação

```sql
SELECT TOP 10 * FROM pedidos ORDER BY id;

SELECT * FROM pedidos
ORDER BY id
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

`LIMIT` não existe no T-SQL. `OFFSET ... FETCH` exige `ORDER BY`.

## Upsert

```sql
MERGE clientes AS alvo
USING (VALUES (1, 'Ana')) AS origem (id, nome)
ON alvo.id = origem.id
WHEN MATCHED THEN UPDATE SET nome = origem.nome
WHEN NOT MATCHED THEN INSERT (id, nome) VALUES (origem.id, origem.nome);
```

## Transações

```sql
BEGIN TRANSACTION;
-- consultas
COMMIT TRANSACTION;
```

## Identificadores

Use colchetes: `[nome]`. Aspas duplas funcionam se `QUOTED_IDENTIFIER` estiver ligado, que é o padrão.

## Armadilhas

- `TOP` sem `ORDER BY` retorna linhas arbitrárias.
- `MERGE` tem fama de ter bugs de concorrência em algumas versões. Confirme antes de usar em produção de alto volume.
