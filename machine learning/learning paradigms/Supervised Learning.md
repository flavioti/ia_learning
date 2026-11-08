#supervised-learning #predictive 

Labeled, so there is a target to predict.

| Task                                    | Predicts                       | Example                                                 | Frameworks             |
| --------------------------------------- | ------------------------------ | ------------------------------------------------------- | ---------------------- |
| **Ranking / learning to rank**          | An ordering of items           | Search results, recommendations                         |                        |
| **[[Time series forecasting]]**         | Future values of a sequence    | Sales next month (see [ARIMA](app://obsidian.md/ARIMA)) | [[Google TimesFM 3.0]] |
| **Structured prediction**               | Sequences or structures        | Translation, named entity recognition                   |                        |
| **Object detection / segmentation**     | Boxes or pixel masks in images | Self-driving, medical imaging                           |                        |
| **Multi-label classification**          | Several labels at once         | Tags on an article                                      |                        |
| **Survival analysis**                   | Time until an event            | Time until churn or failure                             |                        |
| **Probabilistic / quantile regression** | A distribution or interval     | Forecast range                                          |                        |

## Most used algorithms

Regression predicts a number, classification predicts a class. Tree-based algorithms cover both tasks.

```mermaid
flowchart LR
    SL([Supervised Learning])

    SL --> REG[Regression<br/>predicts a number]
    SL --> CLF[Classification<br/>predicts a class]

    REG --> RLIN[Linear models]
    REG --> RTREE[Tree-based]

    RLIN --> LR[Linear Regression]
    RLIN --> RL[Ridge / Lasso / Elastic Net]

    RTREE --> RDT[Decision Tree Regressor]
    RTREE --> RRF[Random Forest Regressor]
    RTREE --> RGB[Gradient Boosting]
    RGB --> RXGB[XGBoost / LightGBM / CatBoost]

    CLF --> CLIN[Linear and probabilistic]
    CLF --> CTREE[Tree-based]

    CLIN --> LOG[Logistic Regression]
    CLIN --> NB[Naive Bayes]

    CTREE --> CDT[Decision Tree Classifier]
    CTREE --> CRF[Random Forest]
    CTREE --> CGB[Gradient Boosting]
    CGB --> CXGB[XGBoost / LightGBM / CatBoost]

    classDef root fill:#37474f,color:#fff,stroke:#37474f
    classDef regTask fill:#1565c0,color:#fff,stroke:#0d47a1
    classDef regFamily fill:#bbdefb,color:#000,stroke:#1565c0
    classDef regAlgo fill:#e3f2fd,color:#000,stroke:#1565c0
    classDef clfTask fill:#e65100,color:#fff,stroke:#bf360c
    classDef clfFamily fill:#ffcc80,color:#000,stroke:#e65100
    classDef clfAlgo fill:#fff3e0,color:#000,stroke:#e65100
    class SL root
    class REG regTask
    class RLIN,RTREE regFamily
    class LR,RL,RDT,RRF,RGB,RXGB regAlgo
    class CLF clfTask
    class CLIN,CTREE clfFamily
    class LOG,NB,CDT,CRF,CGB,CXGB clfAlgo
```

How to read it:

- **Blue**: regression branch (predicts a number).
- **Orange**: classification branch (predicts a class).
- Darker shade = task, medium = algorithm family, lighter = algorithm.
- Tree-based: Random Forest reduces variance (bagging); Gradient Boosting and XGBoost reduce bias (boosting) and are usually the best on tabular data.
- Levels: paradigm → task → algorithm family → algorithm. Algorithms that serve both tasks (trees, boosting) appear under each task, using the regressor or classifier variant.
- Logistic regression is, despite its name, a classifier: a linear model passed through a sigmoid.

Details per algorithm in [[Machine Learning Algorithms|Machine Learning Algorithms]].

## References

[[Evaluation classification model metrics]]
