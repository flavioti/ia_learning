#embeddings #llm #retrieval
# Embeddings models and frameworks

Options to generate embeddings. An embedding model does **not** need to be a generative LLM: most are smaller **encoder** models that can run locally.

## Options

| Option                           | Examples                                                            | Runs local?      | Notes                                                                                       |
| -------------------------------- | ------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------- |
| **Open-source embedding models** | `bge-m3`, `multilingual-e5`, `all-MiniLM-L6-v2`, `nomic-embed-text` | Yes (CPU or GPU) | Best cost-benefit, real semantics                                                           |
| **Provider API**                 | OpenAI `text-embedding-3-*`, Cohere, Voyage                         | No               | High quality, no infrastructure, but has cost and data leaves your environment ([[OpenAI]]) |
| **Via Ollama / vLLM**            | `nomic-embed-text`, `mxbai-embed-large`                             | Yes              | Same open-source models behind a local API ([[providers/Ollama]], [[vLLM]])                           |
| **Classic (sparse)**             | TF-IDF, [[Okapi BM25\|BM25]]                                        | Yes              | Match words only, not meaning. Good for keywords, bad for semantics                         |
| **Old word embeddings**          | word2vec, fastText                                                  | Yes              | Weak for sentences, no context. Rarely used today                                           |

## Local example with `sentence-transformers`

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")   # runs local, no API

# At insert time
doc_vectors = model.encode(product_descriptions, normalize_embeddings=True)

# At query time (SAME model)
query_vector = model.encode("lightweight laptop for travel", normalize_embeddings=True)
```

## How to choose

| Criteria | Recommendation |
|----------|----------------|
| **Language** | If the catalog is not in English, use a **multilingual** model (`bge-m3`, `multilingual-e5`) |
| **Privacy / compliance (LGPD/GDPR)** | A local model keeps data inside the environment |
| **Volume and cost** | Local has fixed infrastructure cost, API charges per token |
| **Latency** | A small local model answers in milliseconds on CPU |
| **Quality** | Large APIs usually win by a small margin, modern open-source models come close |

## Attention points

- **Same model for insert and query**: vectors from different models are not comparable (see [[top-k]]). This applies to local and API models.
- **Column dimension**: `vector(N)` must match the model output (e.g. `bge-m3` = 1024, `all-MiniLM-L6-v2` = 384).
- **Required prefixes**: some models (E5 family) expect `query:` and `passage:` before the text.
- **Changing the model** means re-embedding the whole dataset.

## Links

[[embeddings]]
[[Embedding model]]
[[Hybrid Search]]
[[PGVector (Postgres)]]
[[top-k]]
