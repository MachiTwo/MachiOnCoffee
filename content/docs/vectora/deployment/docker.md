---
title: Docker
slug: docker
date: "2026-04-18T22:30:00-03:00"
type: docs
tags:
  - deployment
  - docker
  - container
  - cloud
---

{{< lang-toggle >}}

O Docker é a maneira mais simples de rodar o Vectora em um ambiente isolado ou em servidores que não possuem o runtime Go instalado.

## Imagens Oficiais

O projeto mantém dois tipos de imagens Docker:

1. **`vectora:latest`**: Versão completa com suporte a CLI e ferramentas locais.
2. **`vectora-cloud:latest`**: Versão enxuta otimizada para APIs de nuvem.

## Rodando com Docker Compose

A maneira recomendada para rodar localmente com todas as dependências (como MongoDB) é via Docker Compose.

```yaml
version: "3.8"
services:
  vectora:
    image: vectora-cloud:latest
    ports:
      - "8080:8080"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - VOYAGE_API_KEY=${VOYAGE_API_KEY}
      - VECTORA_DB_URL=mongodb://mongo:27017/vectora
    depends_on:
      - mongo
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
```

## Build Manual

Você pode construir as imagens localmente usando o `Makefile`:

```bash
make docker-build
```

## External Linking

### Docker & Containers

| Conceito               | Recurso               | Link                                                                                               |
| :--------------------- | :-------------------- | :------------------------------------------------------------------------------------------------- |
| **Docker Compose**     | Referência de Arquivo | [docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/)             |
| **Alpine Linux**       | Base Image            | [alpinelinux.org](https://alpinelinux.org/)                                                        |
| **Multi-stage Builds** | Melhores Práticas     | [docs.docker.com/build/building/multi-stage/](https://docs.docker.com/build/building/multi-stage/) |
