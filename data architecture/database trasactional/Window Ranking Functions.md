---
description: The three ranking window functions ROW_NUMBER, RANK and DENSE_RANK, how each one treats ties, with the same example data for all three. Child of SQL Language, used for top-N queries, deduplication and interview questions.
aliases:
  - ROW_NUMBER RANK DENSE_RANK
  - Funções de ranking em SQL
tags:
  - sql
  - window-functions
  - interview
---
# Window Ranking Functions

As três funções numeram linhas dentro de uma janela (`OVER`). Elas diferem só no tratamento de **empates**. Ver também [[SQL Language]].

## Dados de exemplo

Tabela `vendedores_total`, com o total de vendas de cada vendedor no mês. Ana e Bruno empatam.

| nome | total |
|---|---|
| Ana | 100 |
| Bruno | 100 |
| Carla | 80 |
| Diego | 70 |

```sql
SELECT nome, total,
       ROW_NUMBER() OVER (ORDER BY total DESC) AS row_number,
       RANK()       OVER (ORDER BY total DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY total DESC) AS dense_rank
FROM vendedores_total;
```

| nome | total | row_number | rank | dense_rank |
|---|---|---|---|---|
| Ana | 100 | 1 | 1 | 1 |
| Bruno | 100 | 2 | 1 | 1 |
| Carla | 80 | 3 | 3 | 2 |
| Diego | 70 | 4 | 4 | 3 |

## ROW_NUMBER

Dá um número **único e sequencial** a cada linha. Em caso de empate, a ordem entre as linhas empatadas é arbitrária, então o resultado pode mudar entre execuções se não houver um critério de desempate.

- **Uso típico:** deduplicação (manter uma linha por chave) e paginação.
- **Desempate explícito:** `ORDER BY total DESC, nome` deixa a ordem determinística.

```sql
-- Mantém o registro mais recente de cada cliente
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY atualizado_em DESC) AS rn
    FROM clientes_historico
) t
WHERE rn = 1;
```

## RANK

Empatados recebem o **mesmo número**, e o próximo número é pulado. Com dois empatados em 1, o próximo é 3.

- **Uso típico:** ranking em que a posição real importa, como classificação de competição.
- **Atenção:** um top 3 com `RANK` pode trazer mais de três linhas, se houver empate na terceira posição.

```sql
-- Top 3 com empates: pode retornar mais de 3 linhas
SELECT *
FROM (
    SELECT nome, total, RANK() OVER (ORDER BY total DESC) AS rk
    FROM vendedores_total
) t
WHERE rk <= 3;
```

## DENSE_RANK

Empatados recebem o **mesmo número**, e o próximo número **não** é pulado. Com dois empatados em 1, o próximo é 2.

- **Uso típico:** "segundo maior valor distinto", ou ranking em que os níveis são contínuos.

```sql
-- Segundo maior total distinto (com empates, pega o próximo nível, não a segunda linha)
SELECT DISTINCT total
FROM (
    SELECT total, DENSE_RANK() OVER (ORDER BY total DESC) AS dr
    FROM vendedores_total
) t
WHERE dr = 2;
```

## Por grupo (PARTITION BY)

As três funções aceitam `PARTITION BY`, que reinicia a contagem em cada grupo. É o que se usa para top N por categoria:

```sql
SELECT mes, nome, total,
       DENSE_RANK() OVER (PARTITION BY mes ORDER BY total DESC) AS dr
FROM vendas_mensais;
```

## Resumo

| Função | Empate | Próximo número após dois empatados em 1 | Uso típico |
|---|---|---|---|
| `ROW_NUMBER` | Desempate arbitrário, números únicos | 2 | Deduplicação, paginação |
| `RANK` | Mesmo número | 3 (pula o 2) | Classificação com posição real |
| `DENSE_RANK` | Mesmo número | 2 (sem pular) | Níveis contínuos, segundo maior distinto |

## Pergunta de entrevista

"Qual a diferença entre `RANK` e `DENSE_RANK`?"

Resposta curta: os dois dão o mesmo número a empatados. `RANK` pula posições depois do empate, e `DENSE_RANK` não pula. Para `ROW_NUMBER`, a diferença é que ele nunca repete número, então o empate é quebrado de forma arbitrária.

## Related

- [[SQL Language]]
- [[data architecture/database trasactional/Basic SQL Examples|Basic SQL Examples]]
