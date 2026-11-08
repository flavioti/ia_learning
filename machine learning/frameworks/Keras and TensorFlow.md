#framework #deep-learning #machine-learning
# Keras and TensorFlow

>[!tip] **TensorFlow** is a [[Deep Learning]] framework from Google. **Keras** is a high-level API for building and training [[neural networks]] with very little code.

They are closely related but they are **not the same thing**:

| | TensorFlow | Keras |
|---|------------|-------|
| What it is | The engine: tensors, automatic differentiation, GPU execution, serving tools | The interface: layers, models, `compile()` and `fit()` |
| Level | Low to mid | High |
| Relation | Includes Keras as `tf.keras` | Since **Keras 3** it also runs on **PyTorch** or **JAX**, so it no longer depends on TensorFlow |
| Typical use | Large models, production serving, mobile and edge | Quickly building and training a network |

Think of Keras as the steering wheel and TensorFlow (or PyTorch, or JAX) as the engine.

## TensorFlow building blocks

| Concept | What it is |
|---------|------------|
| **Tensor** (`tf.Tensor`) | N-dimensional array, like [[Numpy]], can live on CPU or GPU |
| **`tf.Variable`** | A tensor whose value changes during training, such as model weights |
| **`tf.GradientTape`** | Records operations and computes gradients for [[Backpropagation]] |
| **`tf.function`** | Compiles Python code into a graph for speed and for deployment |
| **`tf.data`** | Input pipeline for loading, shuffling and batching data |
| **TensorFlow Serving** | Serves trained models behind an API in production |
| **TensorFlow Lite** | Runs models on mobile and edge devices |

```python
import tensorflow as tf

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2
print(tape.gradient(y, x))   # 6.0, the derivative of x^2 at x = 3
```

## Keras building blocks

| Concept | What it is |
|---------|------------|
| **Layer** (`layers.Dense`, `layers.Conv2D`, ...) | A building block with weights and an operation |
| **Model** (`keras.Sequential`, `keras.Model`) | Layers connected into a network |
| **`compile()`** | Sets the optimizer, the loss and the metrics |
| **`fit()`** | Runs the training loop for you |
| **`evaluate()` / `predict()`** | Measures the model and makes predictions |
| **Callbacks** | Hooks during training, such as early stopping and checkpoints |

## Minimal example

Binary classification with a small network:

```python
import numpy as np
import keras
from keras import layers

# 1. Data: 1,000 samples with 20 features, label = 1 when the sum is large
rng = np.random.default_rng(0)
x = rng.random((1000, 20)).astype("float32")
y = (x.sum(axis=1) > 10).astype("float32")

# 2. Model
model = keras.Sequential([
    keras.Input(shape=(20,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(1, activation="sigmoid"),   # probability of class 1
])

# 3. Compile: optimizer, loss and metric
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 4. Train and evaluate
model.fit(x, y, epochs=5, batch_size=32, validation_split=0.2)
loss, accuracy = model.evaluate(x, y)
```

Compare with [[PyTorch]], where you write the training loop (`zero_grad`, `backward`, `step`) yourself. In Keras, `fit()` does it.

## Loss functions and crossentropy

The three [[Crossentropy]] variants come from Keras. Pick the loss from the task and from the label format:

| Keras loss | Task | Labels | Last layer |
|------------|------|--------|------------|
| `BinaryCrossentropy` | Two classes (or multi-label) | 0 or 1 | `sigmoid` |
| `CategoricalCrossentropy` | Multi-class | One-hot, e.g. `[0, 1, 0]` | `softmax` |
| `SparseCategoricalCrossentropy` | Multi-class | Integer, e.g. `1` | `softmax` |
| `MeanSquaredError` | Regression | A number | none (linear) |

Categorical and sparse categorical give the **same loss**. Only the label encoding differs.

## Installing

| Environment | Install |
|-------------|---------|
| Keras with TensorFlow, CPU | `pip install tensorflow` |
| Keras with TensorFlow, NVIDIA GPU (Linux) | `pip install "tensorflow[and-cuda]"` |
| Keras only (choose a backend) | `pip install keras`, plus `tensorflow`, `torch` or `jax` |

Keras picks its backend from the `KERAS_BACKEND` environment variable (`tensorflow`, `torch` or `jax`). Check which Python versions your TensorFlow release supports before installing.

```python
import tensorflow as tf
print(tf.config.list_physical_devices("GPU"))   # [] on a CPU-only machine
```

## Keras / TensorFlow vs. other frameworks

| | Keras / TensorFlow | PyTorch | scikit-learn |
|---|--------------------|---------|--------------|
| Focus | Deep learning | Deep learning | Classical ML |
| Style | High-level `fit()`, optional graph compilation | Eager, you write the training loop | `fit()` / `predict()` |
| Strength | Fast prototyping, serving, mobile and edge | Research, LLMs, ecosystem | Tabular data, baselines, metrics |
| GPU | Yes (CUDA) | Yes (CUDA) | No |

For tabular data, start with [[scikit-learn]]. Move to a deep learning framework when you need [[neural networks]] for images, text, audio or very large data.

## Related

- [[Deep Learning]]
- [[neural networks]]
- [[Backpropagation]]
- [[PyTorch]]
- [[scikit-learn]]
- [[Crossentropy]]
- [[Overfitting]]
