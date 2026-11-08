---
aliases:
  - data mining
---
#data-science #data-mining

**Data mining** is the process of discovering useful, previously unknown **patterns, relationships and anomalies** in large datasets, using methods from statistics, machine learning and databases. The goal is to turn raw data into knowledge that supports decisions, such as "customers who buy X tend to churn within 30 days" or "these transactions look anomalous".

>[!debug] The name is misleading: you are not extracting data, you are extracting *patterns* from data you already have.

## Main tasks

| Task                            | Goal                               | Typical techniques                                  | Example                       |
| ------------------------------- | ---------------------------------- | --------------------------------------------------- | ----------------------------- |
| **Classification**              | Predict a category                 | Decision trees, logistic regression, random forests | Fraud or not fraud            |
| **Regression**                  | Predict a number                   | Linear regression, gradient boosting                | House price, demand           |
| **Clustering**                  | Group similar items without labels | k-means, hierarchical, DBSCAN                       | Customer segments             |
| **Association rules**           | Find items that occur together     | Apriori, FP-Growth                                  | Market-basket analysis        |
| **Anomaly detection**           | Find unusual records               | Isolation forest, statistical tests                 | Faulty sensors, intrusions    |
| **Sequence and trend analysis** | Find patterns over time            | Time-series models, sequential patterns             | Usage trends, event sequences |

Classification and regression are **[[Predictive model]]** (supervised, see [[Supervised Learning]]); clustering and association are **[[Descriptive model]]** (unsupervised, see [[Unsupervised learning]]).

## Example: association rules

In 1,000 transactions, 200 contain bread, 150 contain butter and 100 contain both. For the rule *bread → butter*:

$$
\text{support} = \frac{100}{1000} = 0.10 \qquad
\text{confidence} = \frac{100}{200} = 0.50 \qquad
\text{lift} = \frac{0.50}{150/1000} \approx 3.3
$$

- **Support:** how often the items appear together
- **Confidence:** how often butter appears when bread does
- **Lift:** how much more likely butter is with bread than at random. Above 1 means a positive association

## The process (KDD)

Data mining is the core step of the broader [[Knowledge Discovery in Databases (KDD)|Knowledge Discovery in Databases (KDD)]] process:

1. **Selection:** choose the relevant data
2. **Preprocessing:** [[Data Cleaning]], handle missing values and noise
3. **Transformation:** build features ([[Feature Engineering]]), scale, reduce dimensions
4. **Data mining:** apply the algorithms to find patterns
5. **Interpretation and evaluation:** validate the patterns and turn them into knowledge ([[Model Evaluation]])

[[CRISP-DM]] is the industry process model for running a whole data mining project, from business understanding to deployment.

## Data mining vs related terms

| Term | Relationship |
|---|---|
| **[[Knowledge Discovery in Databases (KDD)\|KDD]]** | The full process of getting knowledge from data. Data mining is its central step |
| **Machine learning** | The toolbox of algorithms often used. Data mining is the *goal* (discover patterns), machine learning is how models learn from data |
| **Data science** | Broader: includes data mining plus data engineering, statistics, communication and deployment ([[data science/README\|Data Science]]) |
| **Statistics** | Provides many of the methods. Data mining usually works on larger, messier data and emphasizes prediction and discovery |
| **BI / reporting** | Describes what happened. Data mining looks for hidden patterns and predictions |

In the 1990s "data mining" was the common name for what is now called data science or machine learning projects, which is why [[CRISP-DM]] is named *for Data Mining*.

## Pitfalls

- **Spurious patterns (data dredging):** with enough variables, something looks significant by chance. Validate on new data and correct for multiple comparisons
- **Correlation is not causation:** a pattern says what goes together, not why
- **[[Overfitting]]:** a model that memorizes noise finds patterns that do not generalize
- **[[Data Leakage]]:** information from the future or the target leaks into the features and inflates results
- **Bad data quality:** garbage in, garbage out
- **Bias:** historical data may encode unfair patterns that the model reproduces
- **Privacy and ethics:** mining personal data requires consent, anonymization and compliance with regulations
- **Actionability:** a pattern that is true but obvious or not usable has no value

## Related

- [[CRISP-DM]]
- [[data science/README|Data Science]]
- [[Supervised Learning]]
- [[Unsupervised learning]]
- [[classification model]]
- [[Model Evaluation]]
