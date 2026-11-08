#regression 
# Cosine similarity

**Cosine similarity** is a mathematical metric that measures how similar two vectors are by their **direction**, regardless of their size (magnitude). In AI and [[vector database|vector databases]], it tells how close two pieces of data (words, sentences, images) are in **[[meaning]]**, once they are converted into [[embeddings]].

Instead of measuring the straight-line distance between two points, it measures the **angle between two arrows** that start at the same origin. The smaller the angle, the more similar the vectors.

## Formula

$$
\cos(\theta) = \frac{A \cdot B}{\lVert A \rVert \, \lVert B \rVert} = \frac{\sum_{i=1}^{n} a_i b_i}{\sqrt{\sum_{i=1}^{n} a_i^2} \; \sqrt{\sum_{i=1}^{n} b_i^2}}
$$

- $A \cdot B$ is the **dot product**: the [[statistics/symbols/Sum|sum]] of the products of matching components.
- $\lVert A \rVert$ and $\lVert B \rVert$ are the **lengths** (norms) of the vectors. Dividing by them removes the effect of magnitude.

The result is the **cosine of the angle**, not the angle itself.

## How to read the value

| Value | Angle | Meaning |
|---|---|---|
| **1** | 0° | Same direction: very similar |
| **0** | 90° | Orthogonal: unrelated |
| **-1** | 180° | Opposite direction |

For text embeddings from most models, scores usually fall between 0 and 1.

## Cosine distance

Many databases return a **distance** instead of a similarity, so that smaller means closer:

$$
\text{cosine distance} = 1 - \cos(\theta)
$$

This is what the `<=>` operator in pgvector returns (see [[top-k]]).

## Example

With $A = [1, 2, 3]$ and $B = [4, 5, 6]$:

$$
A \cdot B = 1 \cdot 4 + 2 \cdot 5 + 3 \cdot 6 = 32
$$

$$
\lVert A \rVert = \sqrt{14} \approx 3.742 \qquad \lVert B \rVert = \sqrt{77} \approx 8.775
$$

$$
\cos(\theta) = \frac{32}{3.742 \times 8.775} \approx 0.975
$$

The vectors point in almost the same direction.

## Cosine vs Euclidean distance

Cosine ignores magnitude, Euclidean distance does not. Take $A = [1, 2]$:

| Vector $B$ | Description | Cosine similarity | Euclidean distance |
|---|---|---|---|
| $[10, 20]$ | Same direction, 10x longer (e.g. a long document on the same topic) | **1.00** | 20.1 |
| $[2, 1]$ | Similar direction | 0.80 | 1.4 |
| $[2, -1]$ | Perpendicular | 0.00 | 3.2 |
| $[-1, -2]$ | Opposite direction | -1.00 | 4.5 |

A short and a long text about the same topic are **far apart** by Euclidean distance but **identical** by cosine. That is why cosine is the usual choice for text, where length varies a lot.

## Relation to the dot product

If the vectors are **normalized** (length 1), the denominator is 1 and:

$$
\cos(\theta) = A \cdot B
$$

So cosine similarity equals the dot product (inner product). Many embedding models return normalized vectors, and databases can then use the faster inner product operator and get the same ranking. See [[Embedding Models and Algorithms]].

## Python

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# From the definition
cos = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
print(cos)                                    # 0.9746

# With scikit-learn (expects 2D arrays)
print(cosine_similarity([a], [b])[0][0])      # 0.9746

# With normalized vectors, the dot product is enough
a_n = a / np.linalg.norm(a)
b_n = b / np.linalg.norm(b)
print(a_n @ b_n)                              # 0.9746
```

## Limitations

- **Ignores magnitude:** when length carries information (for example, how strongly something is expressed), cosine throws it away.
- **Zero vector:** the norm is 0, so the result is undefined. Check for it before dividing.
- **High dimensions:** with hundreds or thousands of dimensions, scores tend to cluster in a narrow range, so small differences can matter. Compare with a threshold calibrated on your own data.
- **Not a distance metric:** it does not satisfy the triangle inequality, although $1 - \cos(\theta)$ is fine for ranking.

## Where it is used

- **Similarity search** in a [[vector database]]: find the closest vectors to a query.
- **[[RAG]] retrieval:** rank document chunks by similarity to the question.
- **Semantic chunking:** split text where the similarity between consecutive sentences drops. See [[Semantic distance]].
- **Recommendation and deduplication:** find similar items or near-duplicate texts.

## Related

- [[embeddings]]
- [[vector database]]
- [[Semantic distance]]
- [[Embedding Models and Algorithms]]
- [[top-k]]
- [[RAG]]
