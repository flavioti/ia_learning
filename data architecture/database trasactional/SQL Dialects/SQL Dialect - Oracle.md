---
description: Oracle Database commands (DBMS_STATS, EXPLAIN PLAN with DBMS_XPLAN, FETCH FIRST and ROWNUM, MERGE, implicit transactions, uppercase identifiers) compared with other engines. Child of SQL Dialects, used when writing or diagnosing queries on Oracle.
aliases:
  - Oracle SQL
  - PL/SQL
tags:
  - sql
  - oracle
  - dialects
---
# SQL Dialect - Oracle

Comandos e sintaxe próprios do Oracle. Ver o hub [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]].

## Estatísticas

```sql
BEGIN
  DBMS_STATS.GATHER_TABLE_STATS(ownname => 'VENDAS', tabname => 'PEDIDOS');
END;
/
```

É uma chamada de pacote PL/SQL, não um comando SQL. Em geral o Oracle coleta estatísticas pelo job automático.

## Plano de execução

```sql
EXPLAIN PLAN FOR
SELECT * FROM pedidos WHERE cliente_id = 10;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

Para o plano com estatísticas de execução real, use `DBMS_XPLAN.DISPLAY_CURSOR` com `'ALLSTATS LAST'` depois de rodar a consulta com `/*+ gather_plan_statistics */`.

## Limite e paginação

```sql
SELECT * FROM pedidos ORDER BY id FETCH FIRST 10 ROWS ONLY;   -- 12c ou superior
```

Em versões antigas, use `ROWNUM` em uma subconsulta, mas atenção: `ROWNUM` é aplicado antes do `ORDER BY` do nível externo.

## Upsert

```sql
MERGE INTO clientes alvo
USING (SELECT 1 AS id, 'Ana' AS nome FROM dual) origem
ON (alvo.id = origem.id)
WHEN MATCHED THEN UPDATE SET alvo.nome = origem.nome
WHEN NOT MATCHED THEN INSERT (id, nome) VALUES (origem.id, origem.nome);
```

`DUAL` é a tabela de uma linha usada em `SELECT` sem tabela, em versões que exigem `FROM`.

## Transações

Não há `BEGIN` explícito. A transação começa com o primeiro comando de escrita ou leitura e termina com `COMMIT` ou `ROLLBACK`.

## Identificadores

Nomes sem aspas viram maiúsculas. `"Nome"` com aspas preserva a capitalização.

## Armadilhas

- `SELECT` sem `FROM` exige `FROM DUAL` nas versões antigas.
- Diferença de maiúsculas e minúsculas em identificadores entre sessões é uma causa comum de erro ao migrar código.
