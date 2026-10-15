System design for AI context refers to the architecture, infrastructure, and engineering strategies used to manage, format, and optimize the data fed into an Artificial Intelligence model (like an LLM or AI agent).
Instead of just modifying prompts, system design for AI context focuses on how knowledge is structured, how tools are exposed, and how memory is managed so that the AI can execute tasks accurately, cost-effectively, and without hallucinations.
## Pillars
- Context selection and retrieval ([[RAG]])
	- [[vector database]]
	- [[Re-ranking]]
	- [[Token compactation]]
- Context Structure & Ontology
	- **Structured Metadata:** Organizing data into standardized formats like JSON or Markdown rather than dumping raw text
	- **Clear Information Architecture:** Creating standardized vocabularies and taxonomies so the AI knows exactly what concepts like "customer" or "order status" mean within your business
- Memory Architecture
	- **[[Short-term Memory]]:** The current working context inside the active session.
	- **[[Long-term Memory]]:** Storing user preferences, historical decisions, and profiles in an external database to be pulled into context only when relevant.
	- **[[Shared Memory]]:** Allowing multiple AI agents to view and update a central dashboard of task progress
## Critical Design Trade-offs
When designing context systems, engineers continuously balance three trade-offs:
1. **[[Relevance]] vs. [[Token Cost]]:** More context results in smarter answers, but significantly increases API costs and processing latency.
2. **[[Hardcoding]] vs. [[Autonomy]]:** Giving the AI rigid structural constraints prevents errors but limits its reasoning capabilities.
3. **[[Freshness]] vs. [[Cacheability]]:** Relying on static, pre-cached context saves money but risks the AI operating on outdated business data
## References

### Components
- [[Design Docs]]

