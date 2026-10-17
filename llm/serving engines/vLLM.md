#serving #acceleration-layer

>[!tip] Inference and serving engine
## What is vLLM?
- **Paged Attention:** Manages the [[Key-Value caching]] (memory used to store past tokens in attention layers) by dividing it into fixed-size blocks, much like an operating system manages virtual memory pages.
- **Memory Efficiency:** Eliminates internal memory fragmentation, raising GPU memory utilization from around 30% to over 90% and allowing more concurrent requests.
- **Ecosystem & Support:** Launched in June 2023, it is the industry-standard default with the broadest hardware support (NVIDIA, AMD ROCm, Google TPU, Intel Gaudi, and CPU fallback) and compatibility with 400+ model architectures.
- **Best Used For:** General-purpose, [[high-throughput serving]], [[single-turn generation tasks]], and teams looking for an easy, out-of-the-box production setup with an OpenAI-compatible API.

## vLLM on Kubernetes

A vLLM replica is typically one **pod** (usually in a `Deployment`) running `vllm serve <model>`. You scale by adding pods. See [[kubernetes]].

| Piece | In Kubernetes |
|-------|---------------|
| **Replica** | A pod exposing the OpenAI-compatible API on one port |
| **GPUs** | `resources.limits: nvidia.com/gpu: N`, provided by the NVIDIA device plugin / GPU Operator |
| **Model weights** | PVC, object store (S3/GCS) via init container, or a shared Hugging Face cache volume |
| **Traffic** | `Service` + Ingress/Gateway in front of the replicas |
| **Autoscaling** | HPA or KEDA driven by vLLM metrics (queue length, running requests, KV cache usage), not CPU |
| **Observability** | `/metrics` endpoint scraped by [[Prometheus]] and shown in [[Grafana]] |

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm
spec:
  replicas: 2
  selector:
    matchLabels: { app: vllm }
  template:
    metadata:
      labels: { app: vllm }
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args: ["--model", "Qwen/Qwen3-8B", "--tensor-parallel-size", "1"]
          ports: [{ containerPort: 8000 }]
          resources:
            limits: { nvidia.com/gpu: 1 }
          readinessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 120   # model load takes time
          volumeMounts:
            - { name: shm, mountPath: /dev/shm }
      volumes:
        - name: shm
          emptyDir: { medium: Memory }   # needed for multi-GPU / tensor parallel
```

**Things to watch**
- **Slow startup:** loading weights can take minutes, so use a generous readiness probe and avoid aggressive scale-to-zero.
- **GPU is not shareable by default:** each replica occupies whole GPUs, so scaling is coarse and costly.
- **Large models:** span several GPUs in one pod (tensor parallel) or several nodes (pipeline parallel, e.g. Ray or LeaderWorkerSet).
- **Routing matters:** replicas have independent [[Key-Value caching]], so cache/prefix-aware routing improves hit rate over round-robin.
- **Autoscale on the right metric:** queue depth or KV cache usage, not CPU.

**Ready-made options**
- **vLLM production-stack:** official Helm chart with router, autoscaling and monitoring.
- **KServe:** model serving platform with a vLLM runtime.
- **llm-d:** Kubernetes-native distributed inference built on vLLM.

[[LLM Inference Infrastructure]]