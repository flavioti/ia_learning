#llm #parameter #retrieval
# Top-K

A limit that keeps only the **K best items** of a ranked list. In LLM systems it appears in two places: **text generation** (sampling) and **retrieval** ([[RAG]]).

## 1. Top-k sampling (text generation)

Decoding parameter. At each step the model keeps only the **K most probable next tokens** and samples among them.

| Value | Effect |
|-------|--------|
| `top_k = 1` | Always the most likely token (greedy, deterministic) |
| `top_k = 50` | More variety and creativity |

- Configures the window of probabilities of the next words.
- Usually combined with [[temperature]] and [[top-p]] (an improved version that uses a probability threshold instead of a fixed count).

## 2. Top-k in retrieval (RAG)

Number of results returned by a similarity search. The query is embedded, compared against stored vectors, and only the **K most similar** items are passed to the LLM as context.

Example: `top-k = 5` returns the 5 products most similar to "lightweight laptop for travel".

| K | Effect |
|---|--------|
| Too small | May miss the right item (low recall) |
| Too large | Adds noise, increases prompt tokens, cost and latency |

- Typical values: 3 to 10.
- Common pattern: retrieve a larger set (e.g. top-50), then **rerank** down to the best 5.

## Comparison

| | Sampling top-k | Retrieval top-k |
|---|---|---|
| Applies to | Next-token candidates | Vector search results |
| Where | LLM decoding | Retriever / vector DB |
| Controls | How random the output is | How much context is retrieved |

## SQL examples

### Classic top-k (by a column)

```sql
SELECT id, name, price
FROM products
ORDER BY price DESC
LIMIT 5;
```

SQL Server uses `TOP 5`; Oracle uses `FETCH FIRST 5 ROWS ONLY`.

### Top-k per group

```sql
SELECT id, name, category, price
FROM (
    SELECT id, name, category, price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
) ranked
WHERE rn <= 3;
```

### Top-k by vector similarity (pgvector)

See [[PGVector (Postgres)]].

```sql
SELECT id, name, price,
       1 - (embedding <=> :query_vector) AS similarity
FROM products
ORDER BY embedding <=> :query_vector   -- cosine distance (smaller = closer)
LIMIT 5;                               -- top-k
```

#### What is `:query_vector`?

The **embedding of the user's question**: a list of numbers (e.g. 1536 floats) that represents the meaning of the search text. The `:` marks a query **parameter**, filled in by the application, not by the database.

```python
query_text = "ultralight laptop for travel"
query_vector = embedding_model.embed_query(query_text)   # [0.012, -0.087, ..., 0.056]

cur.execute(
    "SELECT id, name FROM products ORDER BY embedding <=> %(qv)s LIMIT 5",
    {"qv": query_vector},
)
```

- `embedding` is the vector of each product, computed ahead of time when the data was inserted.
- `<=>` computes the distance between each product vector and `query_vector`.
- `ORDER BY ... LIMIT 5` returns the 5 products closest in meaning to the question (the top-k).

> [!warning] Use the same embedding model for insert and query
> The model (or algorithm) used to generate the vectors **inserted** into pgvector must be exactly the same one used to generate `query_vector` at **query time**.
> - Each model has its own vector space: vectors from different models are not comparable, and the distance becomes meaningless (the top-k returns wrong results, with no error).
> - The **dimension** must match the column (`vector(1536)` requires a 1536-dim `query_vector`), otherwise the query fails.
> - Same model **version** and same text preprocessing too. If the model changes, **re-embed and re-index all data**.
>
> ```python
> EMBEDDING_MODEL = "text-embedding-3-small"   # single source of truth, used by both flows
> doc_vector   = embed(EMBEDDING_MODEL, product_description)  # at insert time
> query_vector = embed(EMBEDDING_MODEL, user_question)        # at query time
> ```

See [[embeddings]] and [[Embedding model]].

#todo 

| Operator | Distance |
|----------|----------|
| `<=>` | Cosine |
| `<->` | Euclidean (L2) |
| `<#>` | Negative inner product |

### Top-k with metadata filters (hybrid)

```sql
SELECT id, name, price,
       1 - (embedding <=> :query_vector) AS similarity
FROM products
WHERE category = 'laptop'
  AND price BETWEEN 3000 AND 8000
  AND in_stock = true
ORDER BY embedding <=> :query_vector
LIMIT 5;
```

### Speeding it up with an index

Without an index, pgvector scans every row. An HNSW index makes top-k approximate and much faster:

```sql
CREATE INDEX ON products
USING hnsw (embedding vector_cosine_ops);
```

With a restrictive `WHERE`, an approximate index may return fewer than `k` rows. In pgvector 0.8+, `SET hnsw.iterative_scan = relaxed_order;` helps.

## Links

[[top-p]]
[[temperature]]
[[RAG]]
[[PGVector (Postgres)]]
