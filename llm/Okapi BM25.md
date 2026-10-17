#algorithm #search #python #non-llm 
## BM25 - Best Matching number 25
Is one of the most widely used [[information retrieval]] algorithm in the world for ranking and scoring the relevance of documents to a given text query. It serves as the foundation for modern search engines like [[ElasticSearch]], [[OpenSearch]], and [[Lucene]].

## Limitations

- **Matches words, not meaning**: BM25 is a lexical (sparse) algorithm. It scores documents by the terms that literally appear in the query (term frequency, inverse document frequency and document length).
- **Good for keywords**: excellent for exact terms such as product codes, names, SKUs and technical jargon.
- **Bad for semantics**: it does not understand synonyms or intent. A query like "laptop" will not match a document that only says "notebook", and "cheap" will not match "affordable".
- **Not an embedding model**: it does not generate dense vectors, so it needs no model and runs fully local and cheap.

| | BM25 (sparse) | Embeddings (dense) |
|---|---|---|
| Matches | Exact words | Meaning |
| Synonyms | No | Yes |
| Exact codes / names | Excellent | Weak |
| Needs a model | No | Yes |

A common solution is to combine both in [[Hybrid Search]] (BM25 + vector search), and use [[Embedding Models and Algorithms]] for the semantic side.
