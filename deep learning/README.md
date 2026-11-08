# Deep learning

Index of deep learning topics. This folder holds the notes about neural networks trained with deep learning frameworks. For classical ML libraries see [[machine learning/frameworks/README|Machine learning frameworks]].

## Frameworks

| Framework | Notes |
| --- | --- |
| [[PyTorch]] | The dominant choice in research and, increasingly, in production. Most new models and papers ship in PyTorch first. It is also the base for Hugging Face Transformers |
| [[Keras and TensorFlow\|TensorFlow / Keras]] | Still common in existing production systems and in mobile or edge deployment (TF Lite). Keras 3 runs on multiple backends |
| **JAX** | High-performance research and large-scale training, often through Flax. Popular at Google and in some labs |

## Rule of thumb

- **Deep learning or LLMs:** PyTorch, usually with [[Hugging Face Transformers]]. See [[llm - plataform & framework|LLM platforms and frameworks]].
- **Existing production systems, mobile or edge:** TensorFlow / Keras.
- **Large-scale research:** JAX.

## Related

- [[Deep Learning]]
- [[neural networks]]
- [[machine learning/frameworks/README|Machine learning frameworks]]
