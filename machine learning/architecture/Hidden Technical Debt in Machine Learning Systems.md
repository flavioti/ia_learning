#machinelearning #mlops #architecture

The **core components** of a production ML system. The model code (ML) is only a small part of it: most of the system is the surrounding infrastructure for data, configuration, resources, serving and monitoring.

```mermaid
treemap-beta
"ML System":::root
    "Configuration": 10:::infra
    "Data Collection": 14:::data
    "Feature Extraction": 20:::data
    "Data Verification": 10:::data
    "ML": 2:::model
    "Machine Resource Management": 11:::infra
    "Analysis Tools": 9:::ops
    "Process Management Tools": 9:::infra
    "Serving Infrastructure": 12:::ops
    "Monitoring": 8:::ops

    classDef root fill:#1e293b,stroke:#0f172a,color:#f8fafc,stroke-width:2px
    classDef data fill:#3b82f6,stroke:#1d4ed8,color:#ffffff,stroke-width:2px
    classDef infra fill:#8b5cf6,stroke:#5b21b6,color:#ffffff,stroke-width:2px
    classDef model fill:#f97316,stroke:#c2410c,color:#ffffff,stroke-width:3px
    classDef ops fill:#14b8a6,stroke:#0f766e,color:#ffffff,stroke-width:2px
```

**Color legend:** 🔵 data (collection, features, verification) · 🟣 infrastructure (configuration, resources, process management) · 🟠 model (ML) · 🟢 operations (analysis, serving, monitoring).

> The values are illustrative, only to show that the ML code is a small block compared to the rest of the system. They are not measurements.

## Components

| Component                       | Role                                                                                     |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| **Configuration**               | Parameters, hyperparameters and environment settings, versioned and reproducible         |
| **Data Collection**             | Ingestion of raw data from sources such as databases, logs, APIs and streams             |
| **Feature Extraction**          | Transforms raw data into features for training and inference                             |
| **Data Verification**           | Validates schema, distribution and quality before the data is used                       |
| **ML**                          | The model code: training, evaluation and the algorithm itself                            |
| **Machine Resource Management** | Allocation of CPU, GPU, memory and storage for training and serving                      |
| **Analysis Tools**              | Inspection of data and model results, such as metrics, explainability and error analysis |
| **Process Management Tools**    | Orchestration of pipelines, scheduling, experiment tracking and versioning               |
| **Serving Infrastructure**      | Delivers predictions in batch or online through APIs                                     |
| **Monitoring**                  | Tracks system health, data drift, model performance and alerts                           |
