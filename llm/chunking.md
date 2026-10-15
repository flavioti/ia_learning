Created by ==🟡LLM specialist== ou a ==🟣non-llm way (algorithms)==
## Chunking strategies

Choose based on document structure, task type and retrieve goals

| Strategy              | Requires LLM? | Ingestion speed | Compute cost | How it works                                                                                                                                  | Best for                 |
| --------------------- | ------------- | --------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Fixed size            | No            | Fast            | Near zero    | Cuts text every N tokens with a small overl                                                                                                   | Simple docs              |
| Recursive             |               |                 |              | Split by paragraphs, then lines, then words, then characters if n                                                                             | General purpose docs     |
| Document-based        |               |                 |              | Split at headings, chapter, or HTML / Markdown                                                                                                | Structured documents     |
| [[Semantic distance]] | No            | Moderate        | Low          | New chunk starts when sentence similarity                                                                                                     | Long-form content        |
| LLM-based             | Yes           | Slow            | High         | LLM rewrites text into standalone propos                                                                                                      | High-stakes Q&A          |
| Agentic               |               |                 |              | AI Agent picks the chunking method per d                                                                                                      | Mixed-format collections |
| Late chunking         |               |                 |              | Embbeds the full first, then applies split boundaries and pools token vectors into chunk em                                                   | Full-context tasks       |
| Hierach               |               |                 |              | Breaks the content into multiple levels (document -> section -> subsection -> paragraph -> sentence) and indexes them with parent-child links | Large structured docs    |

### References
[[embeddings]]
[[RAG]]
