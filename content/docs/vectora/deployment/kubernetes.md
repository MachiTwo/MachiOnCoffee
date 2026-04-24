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

A implantação em Kubernetes é o método recomendado para ambientes de produção que exigem alta disponibilidade e escalabilidade.

O Vectora fornece manifestos padrão que cobrem segredos, configuração, deployment e escalonamento automático (HPA).

## Estrutura dos Manifestos

Os manifestos estão localizados na pasta `k8s/` da raiz do projeto:

- `secret.yaml`: Armazena chaves de API sensíveis e tokens JWT.
- `configmap.yaml`: Configurações não sensíveis (URLs, portas, etc.).
- `deployment.yaml`: Define o estado desejado do container `vectora-cloud`.
- `service.yaml`: Expõe o Vectora internamente ou via LoadBalancer.
- `hpa.yaml`: Configura o Horizontal Pod Autoscaler baseado em CPU/Memória.

## Passos para Implantação

1. **Configurar Segredos**: Atualize o `k8s/secret.yaml` com suas chaves codificadas em base64 ou use uma ferramenta de gerenciamento de segredos.
2. **Aplicar Manifestos**: Use o comando `make k8s-deploy` ou aplique diretamente com `kubectl`.
3. **Verificar**: Monitore os pods para garantir que o Vectora iniciou corretamente.

```bash
kubectl get pods -l app=vectora
```

## External Linking

### Kubernetes & Cloud

| Conceito    | Recurso         | Link                                                                                                                                             |
| :---------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **kubectl** | Cheat Sheet     | [kubernetes.io/docs/reference/kubectl/cheatsheet/](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)                                     |
| **HPA**     | Pod Autoscaling | [kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) |
| **Helm**    | Package Manager | [helm.sh](https://helm.sh/)                                                                                                                      |
