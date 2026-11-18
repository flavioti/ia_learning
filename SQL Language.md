---
description: SQL as a language, with a reference drawing of the join types (inner, left, right, full, semi and anti) and what each one returns from two tables, used for query design and technical interviews.
aliases:
  - SQL
  - sql
---
# SQL Language

## Joins

Cada desenho mostra as regiões que o join retorna. Verde = incluída no resultado, sem cor = fora.
T1 é a tabela da esquerda e T2 a da direita.

![[SQL Joins.excalidraw|1024]]

## Exemplos

Tabelas de exemplo: `clientes` (T1) e `pedidos` (T2), ligadas por `clientes.id = pedidos.cliente_id`.

```sql
-- INNER JOIN: só clientes com pedido
SELECT c.nome, p.valor
FROM clientes c
INNER JOIN pedidos p ON p.cliente_id = c.id;

-- LEFT JOIN: todos os clientes; valor fica NULL para quem não comprou
SELECT c.nome, p.valor
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id;

-- RIGHT JOIN: todos os pedidos; nome fica NULL se o cliente não existe na tabela
SELECT c.nome, p.valor
FROM clientes c
RIGHT JOIN pedidos p ON p.cliente_id = c.id;

-- FULL JOIN: todos os clientes e todos os pedidos
SELECT c.nome, p.valor
FROM clientes c
FULL JOIN pedidos p ON p.cliente_id = c.id;

-- LEFT SEMI (em SQL, com EXISTS): clientes que têm pedido; sem colunas de pedidos
SELECT c.nome
FROM clientes c
WHERE EXISTS (SELECT 1 FROM pedidos p WHERE p.cliente_id = c.id);

-- LEFT ANTI (em SQL, com NOT EXISTS): clientes sem pedido
SELECT c.nome
FROM clientes c
WHERE NOT EXISTS (SELECT 1 FROM pedidos p WHERE p.cliente_id = c.id);
```

No Spark, o mesmo semi e anti join aparece como `left_semi` e `left_anti`:

```python
clientes.join(pedidos, clientes.id == pedidos.cliente_id, "left_semi")
clientes.join(pedidos, clientes.id == pedidos.cliente_id, "left_anti")
```

## Frame de janela

A cláusula `ROWS` ou `RANGE BETWEEN ... AND ...`, com o frame padrão e as diferenças para empates: [[data architecture/database trasactional/Window Frame Clause|Window Frame Clause]].

## Funções de deslocamento em janela

`LAG` e `LEAD`, para ler a linha anterior ou seguinte, com variação entre períodos e detecção de mudança de estado: [[data architecture/database trasactional/Window Offset Functions|Window Offset Functions]].

## Funções de agregação em janela

`SUM`, `MAX` e `MIN` com `OVER`, com exemplos de total geral, acumulado e por grupo: [[data architecture/database trasactional/Window Aggregate Functions|Window Aggregate Functions]].

## Funções de ranking

`ROW_NUMBER`, `RANK` e `DENSE_RANK`, com exemplos e tratamento de empates: [[data architecture/database trasactional/Window Ranking Functions|Window Ranking Functions]].

## Exemplos básicos

Top 3 vendedores por mês, com CTE, `ROW_NUMBER` e filtro no rank: [[data architecture/database trasactional/Basic SQL Examples|Basic SQL Examples]].

## EXPLAIN

Como ler o plano de execução e diagnosticar uma consulta lenta: [[data architecture/database trasactional/SQL EXPLAIN|SQL EXPLAIN]].

## Estatísticas

O comando `ANALYZE`, que alimenta o planejador: [[data architecture/database trasactional/SQL ANALYZE|SQL ANALYZE]].

## Dialetos

Comandos que mudam entre bancos (estatísticas, plano, limite, upsert, transações): [[data architecture/database trasactional/SQL Dialects/SQL Dialects|SQL Dialects]].

## Armadilhas

Join cartesiano, subconsultas desnecessárias e funções sobre colunas filtradas: [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]].

## Notas

- **Semi e anti não são palavras-chave padrão do SQL.** Em SQL, use `EXISTS` (semi) e `NOT EXISTS` ou `LEFT JOIN ... WHERE b.chave IS NULL` (anti). No Spark, existem como `left_semi` e `left_anti`.
- **Armadilha do `LEFT JOIN`:** filtrar a tabela da direita no `WHERE` transforma o join em inner. O filtro deve ir na cláusula `ON`.
- **Cartesiano:** um join sem condição de igualdade multiplica as linhas.
