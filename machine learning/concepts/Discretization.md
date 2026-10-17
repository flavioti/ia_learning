---
aliases:
  - Binning
  - Bucketing
---
# Discretization (Binning/Bucketing)

## What is it?

**Discretization** is converting a **continuous variable into a categorical one** by splitting it into **intervals (bins/buckets)**. Basically, creating ranges. It is a very common practice in credit, risk and recommendation models!

---

## Before vs After

```
BEFORE (Continuous):
Age: 5, 15, 25, 35, 45, 55, 65, 75

AFTER (Discretized):
Age Group: "0-18", "19-35", "36-60", "60+"
```

---

## Examples

| Original Variable | Discretization |
|------------------|---------------|
| Temperature: -10 to 50°C | "Cold" (-10 to 0), "Warm" (0 to 25), "Hot" (25 to 50) |
| Income: $0 to $200k | "Low" (0-50k), "Medium" (50-100k), "High" (100-200k) |
| Score: 0 to 100 | "Bad" (0-40), "Good" (40-70), "Excellent" (70-100) |

---

## Why Use It?

| Reason | Benefit |
|--------|----------|
| **Interpretation** | "Good" is more intuitive than "723.45" |
| **Stakeholders** | Executives understand ranges, not numbers |
| **Decisions** | "If score ≥ Good, approve" is actionable |
| **Reduces noise** | 723 vs 725 are practically the same |
| **Communication** | "Customer is in the Excellent range" is clear |

---

## Types of Discretization

| Type | Method | Example |
|------|--------|---------|
| **Equal Width** | Splits into equal-sized intervals | Score 0-1000: [0-250], [250-500], [500-750], [750-1000] |
| **Equal Frequency** | Splits so each bin has the same amount of data | Each bin has ~25% of the customers |
| **Manual** | Defined using domain knowledge | Score 0-100: "Low" (0-30), "Medium" (30-70), "High" (70-100) |

---

## Real Cases: Discretized Scores

### Risk Score (0-100)
```
0-30   → "Low"
30-70  → "Medium"
70-100 → "High"
```

### Quality Score (0-1000)
```
0-300    → "Poor"
300-600  → "Acceptable"
600-850  → "Good"
850-1000 → "Excellent"
```

### Propensity Score (0-1)
```
0-0.3   → "Unlikely"
0.3-0.6 → "Possible"
0.6-1.0 → "Likely"
```

### Practical Example: Credit Score (0-1000)
```
Customer A: 350  →  "Fair"
Customer B: 720  →  "Good"
Customer C: 950  →  "Excellent"
```

---

## ⚠️ Trade-off: Clarity vs Precision

| Advantage | Disadvantage |
|----------|------------|
| Simple to understand | Loses specific information |
| Reduces noise | Less granularity |
| Stakeholders understand it | Less potential precision |
| Clearer decisions | Loss of nuance |

---

## When to Use It?

✅ **USE when:**
- Interpretation is important
- You want to communicate with stakeholders
- Data is very noisy
- Decisions are binary/categorical

❌ **DO NOT use when:**
- You need maximum precision
- The model already captures the relationship well
- The score is the final continuous metric
