---
description: Basic SQL examples for analytics, starting with a top-N per group query (monthly top 3 sellers) built with a CTE, GROUP BY, a window function and a filter on the rank. Child of SQL Language, used to practise query writing for interviews.
aliases:
  - SQL examples
  - Exemplos básicos de SQL
tags:
  - sql
  - examples
  - interview
---
# Basic SQL Examples

Exemplos curtos de SQL para análise. Ver também [[SQL Language]] e [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]].

## Top 3 vendedores por mês

Para cada mês, lista os três vendedores com maior total de vendas. Usa duas tabelas, `vendas` e `vendedores`.

```sql
WITH raw AS (
    SELECT date_trunc('month', v.data_venda)::date AS cmonth,
           v2.nome,
           SUM(v.valor) AS total
    FROM vendas v
    INNER JOIN vendedores v2 USING (id_vendedor)
    GROUP BY 1, 2
),
ordered AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY cmonth ORDER BY total DESC) AS rn
    FROM raw
)
SELECT *
FROM ordered
WHERE rn BETWEEN 1 AND 3
ORDER BY cmonth DESC;
```

### Passo a passo

1. **`raw`:** agrega as vendas por mês e vendedor.
   - `date_trunc('month', ...)` leva cada data para o primeiro dia do mês. `::date` converte o resultado para `date`. Essa sintaxe é do PostgreSQL.
   - `INNER JOIN ... USING (id_vendedor)` junta as tabelas por uma coluna com o mesmo nome nas duas. Vendas sem vendedor cadastrado ficam de fora.
   - `GROUP BY 1, 2` é o mesmo que agrupar por `cmonth` e `nome`.
2. **`ordered`:** numera os vendedores dentro de cada mês, do maior total para o menor.
   - `ROW_NUMBER() OVER (PARTITION BY cmonth ORDER BY total DESC)` reinicia a contagem a cada mês.
3. **Consulta final:** filtra `rn` entre 1 e 3 e ordena do mês mais recente para o mais antigo.

### Pontos de atenção

- **Empate:** `ROW_NUMBER` atribui posições únicas, então dois vendedores com o mesmo total podem ficar um dentro e outro fora do top 3, de forma arbitrária. Se o empate precisa aparecer, use `RANK()` ou `DENSE_RANK()`. Com `RANK()`, o top 3 pode trazer mais de três linhas.
- **Filtrar depois do window:** o filtro `rn <= 3` precisa ficar fora da CTE que calcula o `ROW_NUMBER`. Window functions não podem aparecer no `WHERE` do mesmo nível.
- **Dialeto:** `date_trunc` e `::` são do PostgreSQL. No BigQuery, use `DATE_TRUNC(data, MONTH)` e `CAST`. No MySQL, `DATE_FORMAT` ou `DATE(...)` cumprem o papel.
- **Desempenho:** sem índice em `data_venda` e em `id_vendedor`, a consulta lê as duas tabelas inteiras. Veja a armadilha de função sobre coluna filtrada em [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]].

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/SQL Pitfalls|SQL Pitfalls]]
