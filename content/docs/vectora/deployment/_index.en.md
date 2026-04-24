---
title: Deployment
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

Vectora is designed to be deployed flexibly, from local machines to cloud-based Kubernetes clusters.

The `vectora-cloud` binary is optimized for container environments, removing GUI dependencies and focusing on API and search engine performance.

## Deployment Options

Vectora offers three main paths for deployment:

1. **Docker**: Ideal for isolated environments and quick testing.
2. **Kubernetes**: Recommended for large-scale production, with support for secrets and auto-scaling.
3. **Native Binary**: For local use or dedicated servers where containerization overhead is not desired.

## Infrastructure Requirements

For a stable deployment, ensure you have:

- **MongoDB Atlas**: Recommended for vector and metadata persistence.
- **API Keys**: `GOOGLE_API_KEY` (Gemini) and `VOYAGE_API_KEY` (Voyage AI).
- **Resources**: Minimum 512MB RAM and 0.5 CPU per instance.

## External Linking

### Infrastructure & Orchestration

| Concept           | Resource               | Link                                                                         |
| :---------------- | :--------------------- | :--------------------------------------------------------------------------- |
| **Kubernetes**    | Official Documentation | [kubernetes.io](https://kubernetes.io/docs/home/)                            |
| **Docker**        | Docker Docs            | [docs.docker.com](https://docs.docker.com/)                                  |
| **MongoDB Atlas** | Vector Search          | [mongodb.com](https://www.mongodb.com/products/platform/atlas-vector-search) |
| **Voyage AI**     | API Reference          | [docs.voyageai.com](https://docs.voyageai.com/reference/embeddings-api)      |
