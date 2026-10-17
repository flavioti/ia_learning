#outliers #regression-metric 
## Definition: 
Measures the average of the squared errors (L₂ loss). Punish big mistakes.
## Math notation
$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2
$$

Where $y_i$ is the actual value, $\hat{y}_i$ is the predicted value, and $n$ is the number of samples.

**Key Characteristics**: Heavily penalizes large errors; smooth gradients, easy to solve mathematically.
**Best Used When**: Outliers are highly undesirable or represent critical errors you want to avoid at all costs.

[[ML - Machine Learning]]
