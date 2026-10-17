#framework #deep-learning #machine-learning
# PyTorch

>[!tip] An open-source **[[Deep Learning]] framework** for building, training and running [[neural networks]] in Python. 

Think of it as NumPy that runs on GPUs and can compute gradients automatically.
It is the most widely used framework for research and for modern LLMs, and most models on [[Hugging Face]] ship PyTorch weights (for example [[Google TimesFM 3.0]]).

## Core building blocks

| Concept | What it is |
|---------|------------|
| **Tensor** | N-dimensional array (like NumPy), can live on CPU or GPU |
| **Autograd** | Automatic differentiation: records operations and computes gradients for [[Backpropagation]] |
| **`nn.Module`** | Base class for layers and models |
| **Optimizer** (`torch.optim`) | Updates weights from gradients (SGD, Adam, AdamW) |
| **Loss function** | Measures prediction error (`MSELoss`, `CrossEntropyLoss`) |
| **`Dataset` / `DataLoader`** | Loading, batching and shuffling data |
| **Device** | Where tensors run: `cpu`, `cuda` (NVIDIA), `mps` (Apple silicon) |
## Key characteristics

- **Eager execution (define-by-run)**: the graph is built as the code runs, so you can debug with normal Python tools (`print`, breakpoints).
- **Pythonic**: models are plain classes and functions.
- **GPU acceleration**: `tensor.to("cuda")` moves computation to the GPU.
- **`torch.compile`**: optional compilation (PyTorch 2.x) for faster training and inference.
- **Large ecosystem**: `torchvision`, `torchaudio`, Hugging Face Transformers, PyTorch Lightning.

## Minimal example

```python
import torch
from torch import nn

# 1. Data: y = 3x + 2 with noise
x = torch.linspace(0, 1, 100).unsqueeze(1)
y = 3 * x + 2 + 0.1 * torch.randn_like(x)

# 2. Model, loss, optimizer
model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# 3. Training loop
for epoch in range(200):
    optimizer.zero_grad()          # reset gradients
    loss = loss_fn(model(x), y)    # forward pass
    loss.backward()                # autograd computes gradients
    optimizer.step()               # update weights

print(model.weight.item(), model.bias.item())  # approx 3 and 2
```

## Device selection

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
x = x.to(device)
```

## Installing

| Environment                                    | Install                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------- |
| Default (Linux, pulls CUDA wheels, several GB) | `pip install torch`                                                  |
| CPU only (no NVIDIA GPU, much smaller)         | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| Apple silicon                                  | `pip install torch` (uses `mps`)                                     |

## PyTorch vs. other frameworks

| | PyTorch | TensorFlow / Keras | JAX |
|---|---------|--------------------|-----|
| Style | Eager, imperative | Graph + eager, high-level Keras API | Functional, JIT-compiled |
| Strength | Research, LLMs, ecosystem | Production tooling, mobile/edge | Performance, TPU, math-heavy research |
| Debugging | Easy (plain Python) | Easier since 2.x | Harder (functional transforms) |

## Common uses

- Training and fine-tuning [[Deep Learning]] models
- [[LLM training]] and [[LLM inference]]
- Computer vision, speech and time series forecasting
- Running pretrained models from [[Hugging Face]]

## Related

- [[Deep Learning]]
- [[Backpropagation]]
- [[Hugging Face]]
- [[Google TimesFM 3.0]]: PyTorch checkpoint used in the notebook example
