#llm #infrastructure #serving #llmops
# LLM Infrastructure

Layers and components required to serve an LLM in production: from the client request down to the GPU, plus the observability around it.

## Architecture

![[LLM Stack Layers.png|629]]

## Layers and components

| Layer | Component | Role |
|-------|-----------|------|
| **Client** | Applications | Chat UI, [[AI Agent]], [[RAG]] pipelines calling the model |
| **Gateway** | API Gateway | Authentication, rate limiting, routing, quotas and cost control |
| | Load Balancer | Spreads requests across serving replicas |
| **Serving** | [[vLLM]] API | OpenAI-compatible endpoint with streaming (SSE) |
| | Tokenizer | Converts text to token ids and back |
| | Scheduler | Continuous batching: adds and removes requests from the batch at each step |
| | KV Cache | [[Key-Value caching]] managed by PagedAttention, in fixed-size blocks |
| **Model** | Weights | The [[Transformer]] parameters, often quantized (FP16, FP8, INT4) |
| | Inference engine | Runs **prefill** (process the prompt) and **decode** (generate token by token) |
| **Hardware** | CUDA / ROCm | Kernels and libraries such as FlashAttention ([[NVIDIA CUDA]]) |
| | GPU | HBM memory holds weights and KV cache. Large models use tensor / pipeline parallelism |
| **Operations** | Kubernetes | Deployment, GPU scheduling and autoscaling ([[kubernetes]]) |
| | Observability | [[Prometheus]] and [[Grafana]] for latency, throughput and GPU usage |
| | Model registry / storage | Where weights are stored and loaded from |

## Request flow

1. The application sends a request to the **gateway**, which authenticates and routes it.
2. The **load balancer** picks a vLLM replica.
3. vLLM **tokenizes** the prompt and the **scheduler** puts it in the running batch.
4. **Prefill**: the engine processes the whole prompt in one pass and fills the **KV cache**.
5. **Decode**: one token per step, reusing the KV cache, streamed back to the client.
6. When the request ends, its KV cache blocks are freed for other requests.

## Why vLLM

- **PagedAttention** removes KV cache fragmentation, raising GPU memory utilization and allowing more concurrent requests.
- **Continuous batching** keeps the GPU busy, increasing throughput.
- **OpenAI-compatible API** makes it a drop-in replacement for hosted APIs.

## Key metrics

| Metric | Meaning |
|--------|---------|
| **TTFT** (time to first token) | Latency until the first token arrives, driven by prefill |
| **TPOT / ITL** | Time per output token, driven by decode |
| **Throughput** | Tokens per second across all requests |
| **GPU memory / KV cache usage** | Limits how many concurrent requests fit |

## Links

[[LLM architecture]]
[[Transformer]]
[[vLLM]]
[[LLM Serving engines]]
[[Key-Value caching]]
