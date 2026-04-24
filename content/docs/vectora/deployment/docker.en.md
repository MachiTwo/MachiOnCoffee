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

Docker is the simplest way to run Vectora in an isolated environment or on servers that do not have the Go runtime installed.

## Official Images

The project maintains two types of Docker images:

1. **`vectora:latest`**: Full version with CLI support and local tools.
2. **`vectora-cloud:latest`**: Lean version optimized for cloud APIs.

## Running with Docker Compose

The recommended way to run locally with all dependencies (such as MongoDB) is via Docker Compose.

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

## Manual Build

You can build the images locally using the `Makefile`:

```bash
make docker-build
```

## External Linking

### Docker & Containers

| Concept                | Resource       | Link                                                                                               |
| :--------------------- | :------------- | :------------------------------------------------------------------------------------------------- |
| **Docker Compose**     | File Reference | [docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/)             |
| **Alpine Linux**       | Base Image     | [alpinelinux.org](https://alpinelinux.org/)                                                        |
| **Multi-stage Builds** | Best Practices | [docs.docker.com/build/building/multi-stage/](https://docs.docker.com/build/building/multi-stage/) |
