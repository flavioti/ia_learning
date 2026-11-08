#serving #acceleration-layer #nvidia

>[!tip] Inference and serving engine for NVIDIA GPUs

# TensorRT-LLM

**TensorRT-LLM** is NVIDIA's open-source library for running large language models with the lowest latency and the highest throughput on **NVIDIA GPUs**. It is built on NVIDIA's inference stack and tuned for each GPU generation, so it is usually the fastest option when the hardware is NVIDIA, at the price of being tied to it.

For the general idea of an inference engine and a comparison of the others, see [[LLM Serving engines]], [[vLLM]] and [[SGLang]]. For running on a laptop or CPU, see [[llama.cpp]]. GPU basics are in [[NVIDIA CUDA]].

## What it provides

| Feature | What it does |
|---|---|
| **In-flight (continuous) batching** | Adds new requests to a running batch instead of waiting for the whole batch to finish, so the GPU stays busy |
| **Paged KV cache** | Manages the memory of the [[Key-Value caching]] in blocks, like [[vLLM]]'s PagedAttention, so more requests fit in memory |
| **Optimized attention kernels** | Custom GPU kernels for the attention operation |
| **Quantization** | Lower precision weights and activations (for example FP8, INT8, INT4 with AWQ or GPTQ, and FP4 on the newest GPUs) to cut memory and raise speed |
| **Speculative decoding** | A small draft model proposes tokens that the large model checks together, which lowers latency |
| **Parallelism** | Tensor, pipeline and expert parallelism to split a model across several GPUs and nodes |
| **OpenAI-compatible server** | A serving command that exposes the model through an API compatible with the OpenAI API |

The exact feature set and supported GPUs change quickly between releases. Check the release notes of the version you use.

## When to choose it

| Choose TensorRT-LLM when | Prefer another engine when |
|---|---|
| The hardware is NVIDIA and the lowest cost per token matters | You need AMD, TPU, Intel or CPU support ([[vLLM]], [[llama.cpp]]) |
| The workload is stable and high volume, so tuning pays off | The model or traffic changes often and you want a simple setup |
| You run in the NVIDIA ecosystem (for example with NVIDIA's serving and orchestration tools) | You want the broadest model support with the least setup |
| You can invest in quantization and per-GPU tuning | Heavy prefix reuse in multi-turn or agent workloads is the main case ([[SGLang]]) |

## How it fits in a deployment

1. Take a trained model (for example from [[Hugging Face Transformers]]).
2. Optionally **quantize** it, and check that the quality is still good on your evaluation set.
3. Load it in the engine, which applies its optimizations for the target GPU.
4. Serve it behind an API, scale replicas on [[kubernetes]], and monitor latency, throughput and GPU memory.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Often the best performance on NVIDIA GPUs | **NVIDIA only** |
| Strong quantization and multi-GPU support | More setup and tuning than simpler engines |
| Integrates with NVIDIA's serving tools | New models can take longer to be supported than in the community engines |
| Production focus: batching, KV cache, parallelism | Fast-moving, and the API and features change between versions |

## Pitfalls

- Benchmarking with unrealistic prompts. Measure with your real prompt and output lengths, and your concurrency
- Quantizing without checking the quality loss on a task-specific evaluation
- Comparing engines with different settings (batch size, precision, context length)
- Forgetting that GPU memory is shared between the weights and the KV cache
- Depending on one vendor without a fallback plan

## Related

- [[LLM Serving engines]]
- [[vLLM]]
- [[SGLang]]
- [[llama.cpp]]
- [[Key-Value caching]]
- [[NVIDIA CUDA]]
- [[LLM inference]]
