#metric #monitoring

# Population Stability Index (PSI)

## What is it?

**PSI** measures how much the distribution of a variable changed between a **reference** sample (usually the training data) and a **current** sample (production). It needs no ground truth, so it is used to detect [[data drift]] quickly.

The variable is split into ranges (bins) and, for each bin, the share of records in the reference (`p`) is compared with the share in the current sample (`q`):

$$
\text{PSI} = \sum_{i=1}^{B} (q_i - p_i)\,\ln\frac{q_i}{p_i}
$$

The larger the PSI, the larger the change in the distribution. It works for continuous variables (after binning) and for categorical ones. PSI is 0 when the two distributions are identical and is never negative. It is the symmetric version of the KL divergence.

## Interpretation

By convention (originally from credit scoring):

| PSI | Interpretation |
|---|---|
| < 0.1 | Stable |
| 0.1 to 0.25 | Moderate change |
| > 0.25 | Significant change |

These thresholds are rules of thumb, not statistical tests. Tune them per feature and per use case, and treat a high PSI as a reason to investigate, not as an automatic retrain trigger.

## Worked example

Three bins of a feature:

| Bin | Reference `p` | Current `q` | $(q-p)\ln(q/p)$ |
|---|---|---|---|
| A | 0.50 | 0.30 | 0.102 |
| B | 0.30 | 0.30 | 0.000 |
| C | 0.20 | 0.40 | 0.139 |
| **Total** | | | **0.241** |

PSI ≈ 0.24: moderate, close to the significant threshold.

## Python

```python
import numpy as np

def psi(reference, current, bins=10, eps=1e-6):
    # Bin edges come from the reference, so both samples use the same bins
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf

    p = np.histogram(reference, edges)[0] / len(reference)
    q = np.histogram(current, edges)[0] / len(current)

    # Avoid log(0) and division by zero in empty bins
    p, q = np.clip(p, eps, None), np.clip(q, eps, None)
    return float(np.sum((q - p) * np.log(q / p)))
```

Example with a normal reference and a shifted production sample: no shift gives about 0.00, a shift of 0.3 standard deviations about 0.09, and a shift of 0.8 about 0.57.

## Practical notes

- **Binning matters:** about 10 quantile bins from the reference is a common default. Changing the number of bins changes the value.
- **Empty bins:** a bin with zero records makes the formula undefined (log of zero). Add a small epsilon, as above, or merge bins.
- **Sample size:** very small samples give noisy PSI. Use enough records per bin.
- **Univariate only:** it looks at one feature at a time and misses changes in feature interactions.
- **Blind to concept drift:** PSI watches the inputs. If only the input-to-target relationship changes, PSI stays low; see [[concept drift]].
- **Many features:** with many features, some will cross the threshold by chance. Prioritize the most important ones.
- **Also useful for scores:** apply it to the model's predicted scores to detect changes in the prediction distribution.

## PSI vs KS-test

| | PSI | KS-test |
|---|---|---|
| Output | A magnitude with rule-of-thumb thresholds | A statistic and a p-value |
| Variable types | Continuous (binned) and categorical | Continuous |
| Large samples | Stays interpretable | The p-value becomes tiny for irrelevant differences |

They complement each other: KS for significance, PSI for size of the change.

## Related

- [[Model drift]]
- [[data drift]]
- [[concept drift]]
- [[machine learning/concepts/Ground Truth|Ground Truth]]
