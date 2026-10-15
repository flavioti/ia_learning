#serving
>[!tip] Inference and serving engine
## What is vLLM?
- **Core Innovation — PagedAttention:** Manages the [[Key-Value caching]] (memory used to store past tokens in attention layers) by dividing it into fixed-size blocks, much like an operating system manages virtual memory pages.
- **Memory Efficiency:** Eliminates internal memory fragmentation, raising GPU memory utilization from around 30% to over 90% and allowing more concurrent requests.
- **Ecosystem & Support:** Launched in June 2023, it is the industry-standard default with the broadest hardware support (NVIDIA, AMD ROCm, Google TPU, Intel Gaudi, and CPU fallback) and compatibility with 400+ model architectures.
- **Best Used For:** General-purpose, [[high-throughput serving]], [[single-turn generation tasks]], and teams looking for an easy, out-of-the-box production setup with an OpenAI-compatible API.

[[LLM Infrastructure]]
[[Key-Value caching]]