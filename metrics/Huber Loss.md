#outliers

**Definition**: Combines MSE for small errors and MAE for large errors using a threshold (δ).
**Key Characteristics**: Offers the best of both worlds: differentiable at zero and robust to extreme outliers.
**Best Used When**: You want a **balanced, robust model** but need smooth gradients for stable optimization.