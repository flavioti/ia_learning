---
description: The EXPLAIN and EXPLAIN ANALYZE commands in SQL, which show the execution plan a database chooses for a query, with examples of how to read scans, joins, estimates and sorts in PostgreSQL, and the Spark equivalent. Child of SQL Language, used to diagnose slow queries and for interview questions.
aliases:
  - EXPLAIN ANALYZE
  - Plano de execução SQL
tags:
  - sql
  - performance
  - interview
---
# SQL EXPLAIN

`EXPLAIN` mostra o **plano de execução** que o otimizador escolheu para uma consulta: como as tabelas serão lidas, em que ordem os joins acontecem, se há índice e qual o custo estimado de cada etapa. Ver também [[SQL Language]] e [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]].

- **`EXPLAIN`:** mostra o plano, sem executar a consulta.
- **`EXPLAIN ANALYZE`:** executa a consulta e mostra o tempo e o número de linhas **reais** de cada etapa.

O exemplo a seguir usa PostgreSQL. A sintaxe muda entre bancos, mas a ideia é a mesma.


![[SQL explain.excalidraw]]

## Exemplo 1: plano estimado

```sql
EXPLAIN
SELECT c.nome, SUM(p.valor) AS total
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome;
```

Saída ilustrativa. Os números variam conforme o banco, as estatísticas e o volume de dados:

```text
HashAggregate  (cost=...)
  Group Key: c.nome
  ->  Hash Join  (cost=...)
        Hash Cond: (p.cliente_id = c.id)
        ->  Seq Scan on pedidos p  (cost=...)
        ->  Hash  (cost=...)
              ->  Seq Scan on clientes c  (cost=...)
```

Leitura de baixo para cima: primeiro as tabelas são lidas, depois o join, depois a agregação.

## Exemplo 2: filtro com índice

```sql
CREATE INDEX idx_pedidos_data ON pedidos (data_pedido);

EXPLAIN
SELECT * FROM pedidos
WHERE data_pedido >= '2026-01-01' AND data_pedido < '2026-02-01';
```

Se o filtro for seletivo, a saída costuma mostrar um `Index Scan` ou `Bitmap Index Scan` no índice. Sem o índice, aparece um `Seq Scan`, que lê a tabela inteira.

Agora compare com a versão que aplica função na coluna:

```sql
EXPLAIN
SELECT * FROM pedidos
WHERE EXTRACT(YEAR FROM data_pedido) = 2026;
```

Na maioria dos casos o índice em `data_pedido` não é usado, e o plano mostra `Seq Scan`. Essa é a armadilha de função sobre coluna filtrada.

## Exemplo 3: EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT c.nome, SUM(p.valor) AS total
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome;
```

A saída inclui `actual time` e `rows` reais, além das estimativas. Compare os dois:

```text
Seq Scan on pedidos p  (cost=...) (actual time=... rows=...)
```

Se `rows` estimado e `rows` real forem muito diferentes, as estatísticas da tabela estão desatualizadas. Rode `ANALYZE pedidos;` e compare o plano de novo.

**Cuidado:** `EXPLAIN ANALYZE` executa a consulta de verdade. Em `INSERT`, `UPDATE` e `DELETE`, isso altera os dados. Para testar essas operações com segurança, use uma transação e um `ROLLBACK`:

```sql
BEGIN;
EXPLAIN ANALYZE DELETE FROM pedidos WHERE valor < 0;
ROLLBACK;
```

## O que procurar no plano

| Sinal                                           | O que significa                    | O que fazer                                        |
| ----------------------------------------------- | ---------------------------------- | -------------------------------------------------- |
| `Seq Scan` em tabela grande                     | Leitura da tabela inteira          | Verificar índice e se o filtro usa função          |
| `Index Scan` ou `Bitmap Index Scan`             | Leitura pelo índice                | Normal para filtros seletivos                      |
| `Hash Join`                                     | Join com tabela de hash na memória | Bom para tabelas de tamanho médio                  |
| `Nested Loop` com muitas linhas do lado externo | Uma busca por linha                | Pode ser lento; conferir estatísticas              |
| Estimativa muito diferente do real              | Estatísticas desatualizadas        | `ANALYZE` na tabela                                |
| `Sort` ou `Hash` com "Disk"                     | Memória insuficiente, usando disco | Reduzir dados antes do sort, ou revisar `work_mem` |

## Spark

No Spark, o equivalente é `explain`, que mostra os planos lógico e físico:

```python
df.explain()        # plano físico
df.explain(True)    # planos lógico (analisado, otimizado) e físico
```

O plano físico mostra as operações como `Exchange` (shuffle), `BroadcastHashJoin` e `FileScan` com os filtros empurrados (`PushedFilters`). A Spark UI mostra as mesmas informações de forma visual, por etapa e por tarefa.

## Pergunta de entrevista

"O que o `EXPLAIN` faz e como você o usaria para diagnosticar uma consulta lenta?"

Resposta curta: o `EXPLAIN` mostra o plano escolhido pelo otimizador, sem executar. Com `EXPLAIN ANALYZE`, comparo o tempo e as linhas reais com as estimativas. Procuro `Seq Scan` em tabela grande, joins caros, estimativas erradas e operações que vazam para o disco.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]]
- [[data architecture/database trasactional/Basic SQL Examples|Basic SQL Examples]]
