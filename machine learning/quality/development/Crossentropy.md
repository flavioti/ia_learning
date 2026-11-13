# Crossentropy

**Definition**: Measures how well a predicted probability distribution $q$ matches the true distribution $p$. It is the average number of bits (or nats) needed to encode events from $p$ using a code optimized for $q$.

It is **not a true distance**: it is not symmetric ($H(p, q) \neq H(q, p)$) and it is not zero when $p = q$.

## Formula

$$
H(p, q) = -\sum_{x} p(x) \log q(x)
$$

It uses the [[statistics/symbols/Sum|Sum operator]] over all classes $x$.

It decomposes into the [[Entropy]] of $p$ plus the KL divergence, which is the extra cost of using $q$ instead of $p$:

$$
H(p, q) = H(p) + D_{KL}(p \parallel q)
$$

The true labels are fixed, so $H(p)$ is constant, and **minimizing cross-entropy is the same as minimizing the KL divergence**. It is also equivalent to **maximizing the likelihood** of the data.

## Use in machine learning

Cross-entropy is the standard **loss function for classification**. It punishes confident wrong predictions heavily: the loss goes to infinity as the probability given to the correct class goes to 0.

## Variants

| Variant                                 | Task                                     | Label format              | Output activation |
| --------------------------------------- | ---------------------------------------- | ------------------------- | ----------------- |
| **[[Binary Crossentropy]]**             | Two classes (or independent multi-label) | 0 or 1                    | Sigmoid           |
| **[[Categorical Crossentropy]]**        | Multi-class (one correct class)          | One-hot, e.g. `[0, 1, 0]` | Softmax           |
| **[[Sparse Categorical Crossentropy]]** | Multi-class (one correct class)          | Integer, e.g. `1`         | Softmax           |

Categorical and sparse categorical compute the **same loss**. Only the label encoding differs, and the sparse version saves memory when there are many classes.

Binary crossentropy, with $y \in \{0, 1\}$ and predicted probability $\hat{y}$:

$$
L = -\left[ y \log \hat{y} + (1 - y) \log (1 - \hat{y}) \right]
$$

## Example

True label `[1, 0, 0]` (class 0) and prediction `[0.7, 0.2, 0.1]`. Only the correct class contributes, because the other terms are multiplied by 0:

$$
H(p, q) = -\left(1 \cdot \ln 0.7 + 0 \cdot \ln 0.2 + 0 \cdot \ln 0.1\right) = -\ln 0.7 \approx 0.357
$$

If the model had given only 0.1 to the correct class, the loss would be $-\ln 0.1 \approx 2.303$.

## Practical notes

- **Logits vs probabilities:** PyTorch's `CrossEntropyLoss` expects **raw logits** and applies log-softmax internally. Applying softmax before it is a common mistake. See [[machine learning/frameworks/PyTorch|PyTorch]].
- **Numerical stability:** frameworks clip probabilities or use log-softmax to avoid $\log(0)$.
- **Evaluation:** as a metric it is usually called **log loss**. It evaluates the quality of the predicted probabilities, not only the final class. See [[Evaluating classification model metrics|Evaluating classification model metrics]].

## Related

- [[Entropy]]
- [[Huber Loss]] (a loss for regression)
