# Precision-Recall Area Under the Curve

Is a single-number metric used to evaluate binary classification models by measuring the trade-off between precision and recall across different decision threholds.

**The curve & area**: A Precision-Recall curve plots precision on the Y-axis against recall on the X-axis for every possible threhold. PR-AUC calculates the total area undeneath this curve, where a score of 1.0 represents a flawless.

[[Precision]]
[[Recall]]
### Why PR-AUC matters
**Imbalanced Data**: It is the preferred metric when with heavly imbalanced datasets, where the positive class is rare (such as a fraud detection, rare disease screening, or anomaly detection).
**Ignoring True Negatives**: Unlike [[ROC-AUC]], PR-AUC completely ignores true negatives. Because imbalanced datasets feature an overwhelming majority of negative cases, including true negatives in ROC-AUC can inflate performance scores and create a false sense of security. PR-AUC zeroes in strictly on performance regarding the minority positive class.

[[ML metrics]]