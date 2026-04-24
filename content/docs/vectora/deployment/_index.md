---
title: Implantação
slug: deployment
date: "2026-04-18T22:30:00-03:00"
type: docs
tags:
  - deployment
  - docker
  - kubernetes
  - cloud
---

{{< lang-toggle >}}

O Vectora foi projetado para ser implantado de forma flexível, desde máquinas locais até clusters Kubernetes em nuvem.

O binário `vectora-cloud` é otimizado para ambientes de container, removendo dependências de interface gráfica e focando na performance da API e do motor de busca.

## Opções de Implantação

O Vectora oferece três caminhos principais para implantação:

1. **Docker**: Ideal para ambientes isolados e testes rápidos.
2. **Kubernetes**: Recomendado para produção em larga escala, com suporte a segredos e auto-scaling.
3. **Binário Nativo**: Para uso local ou em servidores dedicados onde o overhead de containerização não é desejado.

## Requisitos de Infraestrutura

Para uma implantação estável, certifique-se de ter:

- **MongoDB Atlas**: Recomendado para persistência de vetores e metadados.
- **Chaves de API**: `GOOGLE_API_KEY` (Gemini) e `VOYAGE_API_KEY` (Voyage AI).
- **Recursos**: Mínimo de 512MB RAM e 0.5 CPU por instância.

## External Linking

### Infraestrutura & Orquestração

| Conceito          | Recurso              | Link                                                                         |
| :---------------- | :------------------- | :--------------------------------------------------------------------------- |
| **Kubernetes**    | Documentação Oficial | [kubernetes.io](https://kubernetes.io/docs/home/)                            |
| **Docker**        | Docker Docs          | [docs.docker.com](https://docs.docker.com/)                                  |
| **MongoDB Atlas** | Vector Search        | [mongodb.com](https://www.mongodb.com/products/platform/atlas-vector-search) |
| **Voyage AI**     | API Reference        | [docs.voyageai.com](https://docs.voyageai.com/reference/embeddings-api)      |
