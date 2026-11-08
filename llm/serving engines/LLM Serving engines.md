#serving 
## Quick Comparison

| Feature                      | [[vLLM]]                                                  | [[SGLang]]                                              |
| ---------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| **Primary Memory Technique** | PagedAttention                                            | RadixAttention                                          |
| **Best Workload Fit**        | General high-concurrency, single-turn, or diverse prompts | Multi-turn chat, RAG, agents, heavy prefix reuse        |
| **Model / Hardware Breadth** | 400+ architectures; wide hardware support                 | Strong on popular open models (e.g., DeepSeek, Llama)   |
| **Structured Output**        | Supported                                                 | Native scheduler-level constrained decoding (fast JSON) |

## Other engines

- [[TensorRT-LLM]]: NVIDIA's engine, tuned for the best performance on NVIDIA GPUs
- [[llama.cpp]]: lightweight inference on CPU and consumer hardware
