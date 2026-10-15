#open-source #microservices #portability

Platform designed to make running [[ML - Machine Learning]] workflows on [[kubernetes]] simple, portable, and scalable.

A bridge between [[Data Science]] and [[DevOps Engineer]] (often called [[MLOps Engineer]]). Instead of managing servers, networks, and storage manually, Kubeflow lets you build, deploy, and manage your [[ML model]] using containers.

## Core components

- Notebooks: Web-based development environment ([[Jupyter Notebook]], RStudio, [[VSCode]]).
- Pipelines (KFP): end-to-end ML workflows, preprocessing, [[model training]], and [[ML model evaluation]]
- Katib: automated tool for [[ML hyperparameter tuning]]
- Training operators: distributed training jobs for popular frameworks like [[TensorFlow]], [[PyTorch]], and [[MXNet]]
- KServe (KFServing): tool for deploying trained models at scale, [[ML model serving]], [[auto-scaling]] (down to zero when not in use), and [[ML monitoring]].

