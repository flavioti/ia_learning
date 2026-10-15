# Receiver Operating Characteristic – Area Under the Curve
**ROC-AUC** (Receiver Operating Characteristic – Area Under the Curve) is a evaluation metric for binary classification models that measures a model's ability to rank positive instances higher than negative instances across all possible decision thresholds.
## 1. How the ROC Curve Is Constructed
The ROC curve plots two key parameters as the decision threshold moves from $1.0$ down to $0.0$:
- **True Positive Rate (TPR / Recall / Sensitivity)** on the **y-axis**:
    
    $$\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
    
- **False Positive Rate (FPR / 1 - Specificity)** on the **x-axis**:
    
    $$\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}$$
    

As you lower the classification probability threshold, the model classifies more samples as positive, which increases both True Positives and False Positives. The ROC curve traces this tradeoff across all thresholds.

## 2. Interpreting the AUC Value

The Area Under the Curve (AUC) aggregates the curve's performance into a single metric between $0.0$ and $1.0$:

- **$\text{AUC} = 1.0$:** Perfect classifier. Every positive sample is ranked higher than every negative sample with no overlap between classes.
- **$\text{AUC} = 0.5$:** Random guessing. The curve follows the diagonal line ($y = x$).
- **$\text{AUC} < 0.5$:** Predicts worse than random chance (often indicates inverted labels).
### Probabilistic Interpretation

Mathematically, the AUC value equals the probability that a randomly chosen positive sample will be assigned a higher predicted score than a randomly chosen negative sample:

$$P(\hat{y}_{\text{pos}} > \hat{y}_{\text{neg}})$$

## 3. Key Properties & Strengths

- **Threshold-Invariant:** Evaluates the overall ranking capability of the model without locking into a specific decision boundary (e.g., $0.5$).
- **Scale-Invariant:** Measures how well predictions are ordered rather than their exact calibrated probabilities. Monotonic transformations of predictions (like multiplying probabilities by a constant) do not change the AUC score.
## 4. Limitation: Imbalanced Datasets

ROC-AUC can give a misleadingly optimistic impression when evaluated on **severely imbalanced datasets** where the negative class dominates ($N_{\text{neg}} \gg N_{\text{pos}}$, such as fraud detection or rare disease screening).

Because the denominator of the False Positive Rate includes all true negatives ($\text{TN} + \text{FP}$), a massive number of True Negatives keeps the FPR near zero even if the model produces a large number of False Positives relative to the small positive class.

> **Rule of Thumb:** Use **[[PR-AUC]]** (Precision-Recall Area Under the Curve) instead of ROC-AUC whenever there is severe class imbalance, as Precision ($\frac{\text{TP}}{\text{TP} + \text{FP}}$) directly reflects false positive errors against the minority positive class.