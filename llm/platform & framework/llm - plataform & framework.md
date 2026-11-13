# LLM platforms and frameworks

Index of the frameworks and libraries used to build, fine-tune, serve and orchestrate LLM applications. For classical machine learning libraries see [[machine learning/frameworks/README|Machine learning frameworks]], and for deep learning frameworks see [[deep learning/README|Deep learning]].

## Models and fine-tuning

| Framework | Notes |
|---|---|
| [[Hugging Face Transformers]] | The standard library to load, run and fine-tune open models from the [[Hugging Face]] Hub. Works with PEFT and TRL for efficient fine-tuning |
| [[PEFT - Parameter-Efficient Fine-Tuning]] | Fine-tune a small number of parameters. See [[LoRA - Low-Rank Adaptation]] and [[QLoRA - Quantized Low-Rank Adaptation]] |

## Inference and serving engines

Engines that run a trained model efficiently. They live in `llm/serving engines/`, see [[LLM Serving engines]] for a comparison.

| Engine | Notes |
|---|---|
| [[vLLM]] | The general-purpose default, with PagedAttention and the broadest hardware support |
| [[SGLang]] | Strong for multi-turn chat, RAG and agents with heavy prefix reuse |
| [[TensorRT-LLM]] | NVIDIA's engine, tuned for the best performance on NVIDIA GPUs |
| [[llama.cpp]] | Lightweight inference on CPU and consumer hardware |

## Orchestration and application frameworks

| Framework | Notes |
|---|---|
| [[LangChain SDK]] | Building blocks for LLM applications and agents. See also [[LangChain 's ecosystem]] |
| [[LangGraph SDK]] | Stateful, graph-based agent workflows |
| [[LangFlow]] | Visual builder for LLM flows |
| [[LlamaIndex]] | Document parsing and retrieval for RAG and agent workflows |
| [[platform/N8N.md\|n8n]] | Visual workflow automation with AI agent nodes, to connect apps and APIs. Fair-code license and self-hostable |
| [[llm/platform & framework/Google ADK.md\|Google ADK]] | Code-first framework to build, evaluate and deploy single and multi-agent systems, optimized for Gemini and Google Cloud |

## Observability and evaluation

| Tool | Notes |
|---|---|
| [[LangSmith platform]] | Tracing, datasets, experiments and monitoring for LangChain applications |
| [[DeepEval]] | Evaluation of LLM outputs |

## Demos and interfaces

| Tool | Notes |
|---|---|
| [[Hugging face Gradio]] | Quick web demos for models |

## Rule of thumb

- **Use an open model:** Hugging Face Transformers, fine-tuned with PEFT if needed.
- **Serve it in production:** vLLM by default, TensorRT-LLM when the hardware is NVIDIA and performance is critical, llama.cpp on a laptop or CPU.
- **Build an application or an agent:** LangChain and LangGraph, or LlamaIndex when documents and retrieval are the core. On Google Cloud, Google ADK is the native option for agents.

## Related

- [[LLM Serving engines]]
- [[open source models]]
- [[LLM inference]]
- [[LLM training]]
- [[machine learning/frameworks/README|Machine learning frameworks]]
