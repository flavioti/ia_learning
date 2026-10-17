#provider #gpu #nvidia
# NVIDIA CUDA

**CUDA** (Compute Unified Device Architecture) is NVIDIA's platform and programming model for running general-purpose computation on its GPUs.

> It lets frameworks such as [[PyTorch]] send heavy numerical work (matrix multiplications, convolutions) to the GPU instead of the CPU.

## Why it matters for AI

Neural networks are mostly large matrix operations that can run in parallel. A GPU has thousands of small cores built for this, so training and inference are often 10-100x faster than on a CPU.

| | CPU | GPU (with CUDA) |
|---|---|---|
| Cores | Few, powerful | Thousands, simple |
| Best at | Sequential, branching logic | Massively parallel math |
| Typical AI role | Data loading, orchestration | Training and inference |

## What CUDA includes

| Component | Role |
|-----------|------|
| **CUDA driver** | Lets the OS talk to the NVIDIA GPU |
| **CUDA toolkit** | Compiler (`nvcc`), libraries, debugging and profiling tools |
| **cuBLAS** | Fast linear algebra (matrix math) |
| **cuDNN** | Optimized deep learning primitives (convolutions, attention, normalization) |
| **NCCL** | Communication between multiple GPUs |
| **TensorRT** | Inference optimizer built on CUDA |

## Programming model

| Concept | Meaning |
|---------|---------|
| **Kernel** | A function that runs on the GPU, executed by many threads in parallel |
| **Thread** | Smallest unit of execution |
| **Block** | Group of threads that share fast memory |
| **Grid** | All blocks launched for one kernel |
| **Host / Device** | Host = CPU and its RAM, device = GPU and its VRAM |

Typical flow: copy data from host to device, launch a kernel, copy results back.

## Usage in PyTorch

```python
import torch

torch.cuda.is_available()          # True if an NVIDIA GPU + driver is usable
device = "cuda" if torch.cuda.is_available() else "cpu"

model = model.to(device)           # move the model to the GPU
x = x.to(device)                   # move the data too
```

If this prints `False`, check that an NVIDIA GPU exists (`nvidia-smi`) and that you did not install the CPU-only PyTorch build.

## Installation notes

| Situation | What to do |
|-----------|------------|
| NVIDIA GPU available | `pip install torch` (default Linux build bundles the CUDA libraries, several GB) |
| No NVIDIA GPU | `pip install torch --index-url https://download.pytorch.org/whl/cpu` (much smaller) |
| Check the setup | `nvidia-smi` shows the driver version and the highest CUDA version it supports |

Compatibility matters: the **driver**, **CUDA version** and **PyTorch build** must match. A newer driver generally runs older CUDA builds, not the other way around.

## Key points

- **NVIDIA only**: CUDA does not run on AMD or Intel GPUs. AMD's equivalent is **ROCm**.
- **Without CUDA** the code still runs on CPU, only slower.
- Frameworks and inference engines such as [[PyTorch]] and [[vLLM]] default to CUDA, which is a large part of NVIDIA's dominance in AI hardware.
- Libraries such as FlashAttention are written as custom CUDA kernels to speed up attention (see [[LLM Inference Infrastructure]]).

## Related

- [[PyTorch]]
- [[Deep Learning]]
- [[vLLM]]
- [[LLM Inference Infrastructure]]
