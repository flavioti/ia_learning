#framework #llm #open-source

# Hugging Face Transformers

**Transformers** is the open-source Python library from [[Hugging Face]] for using, fine-tuning and sharing pretrained models. It gives one consistent API over thousands of model architectures (text, vision, audio and multimodal) and downloads the weights from the **Hugging Face Hub**. It runs on top of [[PyTorch]], which is its main backend.

>[!tip] Think of it as the standard "model zoo plus toolkit" for open models. You load a model and its tokenizer by name, and the same few lines work for most architectures.

For the models themselves see [[open source models]], [[LLM model]] and [[Embedding model]]. For serving them in production see [[vLLM]] and [[LLM Serving engines]].

## Main building blocks

| Piece | What it does |
|---|---|
| `AutoTokenizer` | Loads the right tokenizer. It turns text into token ids and back |
| `AutoModel...` (for example `AutoModelForCausalLM`) | Loads the right architecture and weights for a task |
| `pipeline` | One-line inference for common tasks (text generation, classification, summarization, embeddings) |
| `generate()` | Text generation with greedy, sampling and beam search, and parameters such as temperature, top-k and top-p |
| `Trainer` and `TrainingArguments` | A training loop with evaluation, checkpoints and mixed precision |
| **Hub** | Hosts the model weights, datasets and model cards. `from_pretrained("name")` downloads and caches them |
| `safetensors` | The safe and fast file format for weights |

## Related libraries in the ecosystem

Each one is a separate library, and worth its own note.

| Library | Purpose |
|---|---|
| **Datasets** | Load and process datasets efficiently |
| **Accelerate** | Run the same code on CPU, one GPU or many GPUs. Also provides `device_map="auto"` to split a large model across devices |
| **PEFT** | Parameter-efficient fine-tuning. See [[PEFT - Parameter-Efficient Fine-Tuning]], [[LoRA - Low-Rank Adaptation]] and [[QLoRA - Quantized Low-Rank Adaptation]] |
| **TRL** | Post-training with supervised fine-tuning, preference optimization and reinforcement learning. See [[RLHF]] and [[Post-training with Reinforcement Learning]] |
| **Sentence Transformers** | Text embedding models. See [[Embedding Models and Algorithms]] |
| **Gradio** | Quick web demos. See [[Hugging face Gradio]] |

## Example

Loading a tokenizer and a model, and generating text. This uses a tiny test model (`sshleifer/tiny-gpt2`, about 100 thousand parameters) so it runs anywhere. Replace the name with any causal language model from the Hub. It was checked with Transformers 5.20 on CPU.

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

name = "sshleifer/tiny-gpt2"          # replace with a real model, for example an instruction-tuned open model

tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name)   # on a GPU: add dtype=torch.bfloat16, device_map="auto"

inputs = tokenizer("Machine learning is", return_tensors="pt")
print(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))
# ['Machine', 'Ġlearning', 'Ġis']   -> 3 tokens (the 'Ġ' marks a leading space)

output = model.generate(**inputs, max_new_tokens=5, do_sample=False,
                        pad_token_id=tokenizer.eos_token_id)
print(tokenizer.decode(output[0], skip_special_tokens=True))

# The same thing in one line with a pipeline
generator = pipeline("text-generation", model=name)
print(generator("Hello", max_new_tokens=5)[0]["generated_text"])
```

Install with `pip install transformers torch`. On Linux this gives the CPU version of PyTorch by default. Use the CUDA build of PyTorch for an NVIDIA GPU, and pick the device with `device_map="auto"` or `model.to("cuda")`.

>[!warning] **Version changes.** In recent major versions, some arguments were renamed. For example, `torch_dtype` became `dtype`. If an example from an older tutorial fails, check the documentation of the installed version.

## Typical workflow

1. **Pick a model** on the Hub. Check the license, the size, the context length and the intended task on its model card.
2. **Load** the tokenizer and the model with `from_pretrained`.
3. **Run inference** with `generate()` or a `pipeline`, to check quality before training anything.
4. If needed, **fine-tune** with `Trainer` or TRL, using PEFT/LoRA to save memory.
5. **Serve** with a dedicated engine such as [[vLLM]] instead of plain `generate()`, which is not built for high throughput.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Huge catalog of models behind one consistent API | Plain `generate()` is slow and uses memory poorly for many concurrent users, so use a serving engine in production |
| Easy fine-tuning, with PEFT and TRL | A large model needs a lot of GPU memory, so quantization or sharding is often needed |
| Large community, documentation and examples | Models on the Hub vary in quality and license. Check the model card |
| Works with [[PyTorch]] and exports to other runtimes | The API changes between major versions |

## Pitfalls

- Loading a model in full precision (float32) when half precision (bfloat16 or float16) is enough, which doubles the memory
- Using the wrong **chat template** for instruction-tuned models, which lowers the quality. Use `tokenizer.apply_chat_template`
- Forgetting the padding token and the `attention_mask` when batching
- Running `generate()` in a loop for a production service instead of using a serving engine
- Downloading models of unknown origin and running custom code from them. Only use `trust_remote_code=True` with sources you trust
- Ignoring the license of the model

## Related

- [[Hugging Face]]
- [[PyTorch]]
- [[open source models]]
- [[LLM inference]]
- [[LLM training]]
- [[vLLM]]
- [[machine learning/frameworks/README|Machine learning frameworks]]
