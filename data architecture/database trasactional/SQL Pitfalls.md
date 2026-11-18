---
description: Common SQL mistakes that return wrong results or run slowly without raising an error (cartesian join, unnecessary subqueries and functions on filtered columns), with the fix for each and the same idea in Spark and BigQuery. Child of SQL Language, used for query review and technical interviews.
aliases:
  - Armadilhas em SQL
  - SQL anti-patterns
tags:
  - sql
  - performance
  - interview
---
# SQL Pitfalls

Erros de SQL que quase nunca dão erro de sintaxe. A consulta roda, mas devolve linhas a mais, a menos, ou fica lenta. Ver também [[SQL Language]].

## 1. Join cartesiano

Um join sem condição de igualdade combina cada linha de uma tabela com todas as linhas da outra. Com `N` linhas em uma tabela e `M` na outra, o resultado tem `N × M` linhas.

```sql
-- Ruim: sem ON. 1000 clientes × 500 pedidos = 500 000 linhas
SELECT c.nome, p.valor
FROM clientes c, pedidos p;

-- Bom: a condição limita as combinações
SELECT c.nome, p.valor
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id;
```

- **Quando é intencional:** gerar uma grade, por exemplo datas × produtos. Deve ser explícito e comentado.
- **Sinal de alerta:** multiplicação inesperada na contagem de linhas, ou memória e tempo que explodem.
- **Cuidado com chave não única:** mesmo com `ON`, se a chave de um dos lados se repete, o join multiplica linhas. Confira a cardinalidade antes.

## 2. Subconsultas desnecessárias

Uma subconsulta correlacionada no `SELECT` roda uma vez por linha. Um `JOIN` com `GROUP BY` costuma ser mais claro e mais rápido.

```sql
-- Ruim: subconsulta executada para cada cliente
SELECT c.nome,
       (SELECT SUM(p.valor) FROM pedidos p WHERE p.cliente_id = c.id) AS total
FROM clientes c;

-- Bom: uma passagem com join e agregação
SELECT c.nome, SUM(p.valor) AS total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome;
```

- **Subconsulta com `EXISTS` ou `IN` não é o problema** quando a pergunta é de existência, como no semi join ou no anti join.
- **Otimizadores nem sempre reescrevem sozinhos.** Não conte com isso.
- **Legibilidade conta:** CTEs (`WITH`) deixam a lógica em etapas nomeadas.

## 3. Função sobre coluna filtrada

Aplicar uma função na coluna do `WHERE` ou do `JOIN` impede o uso de índice, e no Big Data impede o descarte de partições. O banco precisa calcular a função em cada linha antes de filtrar.

```sql
-- Ruim: a função sobre a coluna impede o uso de índice
SELECT * FROM pedidos WHERE YEAR(data_pedido) = 2026;

-- Bom: a coluna fica intacta e o intervalo é explícito
SELECT * FROM pedidos
WHERE data_pedido >= '2026-01-01' AND data_pedido < '2027-01-01';
```

- **Mesmo problema em joins:** `ON UPPER(a.email) = UPPER(b.email)` impede o uso de índice. Normalize o dado antes, se for uma operação frequente.
- **No Spark e no BigQuery:** a mesma regra vale para o **partition pruning**. Filtrar a coluna de partição com uma função impede que o engine descarte partições inteiras.

## Como responder em entrevista

1. Diga o problema e por que ele passa despercebido (não dá erro).
2. Mostre a versão ruim e a corrigida.
3. Diga o efeito: linhas multiplicadas, consulta repetida por linha ou leitura de dados desnecessária.
4. Se a pergunta for sobre Spark ou BigQuery, cite o pruning.

## Related

- [[SQL Language]]
