#serving
>[!tip] Inference and serving engine
## What is SGLang?
- **Core Innovation — RadixAttention:** Organizes the KV cache into a radix tree structure that automatically detects and reuses shared context or prefix tokens (such as long system prompts, RAG document headers, or conversation histories) across different requests.
- **Performance Boost:** Skips redundant re-computations for repeated prefixes, yielding significantly higher throughput (up to 29% to 6x faster depending on workload) and lower Time to First Token (TTFT).
- **Structured Output & Control:** Features a front-end language and scheduler-level constrained decoding using compressed finite state machines to reliably and rapidly enforce structured outputs like JSON.
- **Best Used For:** [[multi-step agentic workflows]], [[RAG]], [[multi-turn conversational chatbots]], and [[heavy context reuse]].

[[LLM Infrastructure]]
[[Key-Value caching]]