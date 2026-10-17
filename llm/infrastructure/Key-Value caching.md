#inference #memory

## Paged Attention (The Game Changer)

Paged Attention is a novel memory management technique that borrows heavily from how operating systems manage virtual memory.
*   **How it works:** Instead of forcing the entire KV cache for a sequence to occupy one contiguous block of GPU memory (which wastes space), ==Paged Attention== breaks the ==KV cache== into discrete, non-contiguous blocks called "==pages==."
*   **The Benefit:** This allows vLLM to share memory efficiently and manage requests of different lengths simultaneously without fragmentation. It dramatically increases the amount of memory that can be utilized, meaning you can fit many more users and sequences onto the same GPU.
* It is provided by [[vLLM]] and similar serving engines.