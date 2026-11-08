# Machine learning frameworks

Index of the most used ML frameworks and libraries, grouped by purpose. Deep learning frameworks live in [[deep learning/README|Deep learning]], and LLM frameworks in [[llm - plataform & framework|LLM platforms and frameworks]]. The ranking is approximate and comes from general knowledge, not from live usage statistics.
## Classical ML on tabular data

| Framework                               | Notes                                                                                                                            |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [[scikit-learn]]                        | The standard for classical ML: pipelines, preprocessing, metrics and cross-validation. Almost everything else plugs into its API |
| [[XGBoost]], **LightGBM**, **CatBoost** | The usual picks for [[Gradient Boosting]] on tabular data                                                                        |
| **statsmodels**                         | Statistical modeling with inference, p-values and time series                                                                    |
## MLOps and the rest of the lifecycle

| Framework               | Notes                                                        |
| ----------------------- | ------------------------------------------------------------ |
| [[MLFlow]]              | Experiment tracking and [[model registry]]                   |
| **Spark MLlib**         | ML on big data in distributed clusters. See [[Apache Spark]] |
| **ONNX / ONNX Runtime** | Portable model format and fast inference across frameworks   |
| **Ray**                 | Distributed training, tuning and serving                     |
## Data and visualization

Supporting libraries used in almost every ML project.

| Library     | Notes                                                           |
| ----------- | --------------------------------------------------------------- |
| [[Numpy]]   | Arrays and numerical computing. The base of the Python ML stack |
| [[Seaborn]] | Statistical plots on top of Matplotlib                          |
## Rule of thumb

- **Tabular data:** scikit-learn plus a boosting library.
- **Deep learning:** see [[deep learning/README|Deep learning]] (PyTorch, TensorFlow / Keras, JAX).
- **LLMs and generative AI:** see [[llm - plataform & framework|LLM platforms and frameworks]] (Hugging Face Transformers, serving engines, orchestration).
- **Production:** MLflow for tracking, ONNX or a serving engine for deployment.

## Related

- [[Machine Learning|Machine learning]]
- [[machine learning use cases/README|Machine learning use cases]]
- [[Gradient Boosting]]
- [[deep learning/README|Deep learning]]
- [[llm - plataform & framework|LLM platforms and frameworks]]
