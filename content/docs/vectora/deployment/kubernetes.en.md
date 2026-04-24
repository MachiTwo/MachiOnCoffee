---
title: Kubernetes
slug: kubernetes
date: "2026-04-18T22:30:00-03:00"
type: docs
tags:
  - deployment
  - kubernetes
  - orchestration
  - cloud
---

{{< lang-toggle >}}

Kubernetes deployment is the recommended method for production environments requiring high availability and scalability.

Vectora provides standard manifests covering secrets, configuration, deployment, and auto-scaling (HPA).

## Manifest Structure

The manifests are located in the `k8s/` folder at the project root:

- `secret.yaml`: Stores sensitive API keys and JWT tokens.
- `configmap.yaml`: Non-sensitive configurations (URLs, ports, etc.).
- `deployment.yaml`: Defines the desired state of the `vectora-cloud` container.
- `service.yaml`: Exposes Vectora internally or via LoadBalancer.
- `hpa.yaml`: Configures Horizontal Pod Autoscaler based on CPU/Memory.

## Deployment Steps

1. **Configure Secrets**: Update `k8s/secret.yaml` with your base64-encoded keys or use a secret management tool.
2. **Apply Manifests**: Use the `make k8s-deploy` command or apply directly with `kubectl`.
3. **Verify**: Monitor the pods to ensure Vectora started correctly.

```bash
kubectl get pods -l app=vectora
```

## External Linking

### Kubernetes & Cloud

| Concept     | Resource        | Link                                                                                                                                             |
| :---------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **kubectl** | Cheat Sheet     | [kubernetes.io/docs/reference/kubectl/cheatsheet/](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)                                     |
| **HPA**     | Pod Autoscaling | [kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) |
| **Helm**    | Package Manager | [helm.sh](https://helm.sh/)                                                                                                                      |
