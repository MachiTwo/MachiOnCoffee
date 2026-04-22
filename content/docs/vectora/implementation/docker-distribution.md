---
title: Plano de Implementação - Distribuição via Docker
slug: docker-distribution
date: "2026-04-21T14:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - cloud
  - concepts
  - config
  - containers
  - docker
  - engineering
  - errors
  - gemini
  - goreleaser
  - guardian
  - kubernetes
  - mcp
  - mongodb-atlas
  - protocol
  - security
  - state
  - sub-agents
  - system
  - tools
  - troubleshooting
  - vector-search
  - vectora
  - voyage
  - yaml
---

{{< lang-toggle >}}
{{< section-toggle >}}

O Vectora é distribuído via **Docker** para facilitar deployment em qualquer ambiente: máquinas locais, servidores, Kubernetes (para Managed Instances na Cloud), e ambientes de desenvolvimento. Este documento descreve como criar, testar e publicar imagens Docker.

## Visão Geral da Arquitetura

```mermaid
graph LR
    A[Push/Tag v*] --> B[GitHub Actions - CI/CD]
    B --> C[Build Multi-Arch Dockerfile]
    C -->|amd64| D["vectora:2.1.0-amd64"]
    C -->|arm64| E["vectora:2.1.0-arm64"]
    D --> F["Docker Hub Registry"]
    E --> F
    F -->|multi-arch| G["docker pull vectora:latest"]
    G -->|Local Dev| H["dev.docker-compose.yml"]
    G -->|Kubernetes| I["Managed Instance"]
    G -->|Standalone| J["Systray + Core"]
```

## Fases de Implementação

### **Fase 1: Criar Dockerfile Multi-Stage (Core)**

**Duração**: 1 semana

**Deliverables**:

- [ ] Dockerfile otimizado com multi-stage build
- [ ] Suporte para amd64 e arm64
- [ ] Imagem base Go 1.21
- [ ] Tamanho <150MB
- [ ] Healthcheck integrado

**Código de Exemplo - Dockerfile (Root)**:

```dockerfile
# Dockerfile - Vectora Core
# Multi-stage build: compile + runtime

FROM golang:1.21-alpine AS builder

WORKDIR /build

# Instalar dependências de build
RUN apk add --no-cache git ca-certificates tzdata

# Copiar go.mod e go.sum
COPY go.mod go.sum ./

# Download de dependências (cached layer)
RUN go mod download

# Copiar código-fonte
COPY . .

# Build do binário unificado (daemon + CLI + Systray)
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w -X main.Version=${BUILD_VERSION:-dev}" \
    -o /build/dist/vectora ./cmd/vectora

# Stage 2: Runtime (minimal)
FROM alpine:3.19

# Instalar runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    curl \
    git

# Criar user não-root para segurança
RUN addgroup -g 1000 vectora && adduser -D -u 1000 -G vectora vectora

# Copiar binário unificado do builder
COPY --from=builder --chown=vectora:vectora /build/dist/vectora /usr/local/bin/

# Criar diretórios necessários
RUN mkdir -p /home/vectora/.config/vectora && \
    chown -R vectora:vectora /home/vectora

USER vectora

WORKDIR /home/vectora

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD vectora health || exit 1

# Default command
ENTRYPOINT ["vectora"]
CMD ["--help"]

# Labels (metadados)
LABEL org.opencontainers.image.title="Vectora Core"
LABEL org.opencontainers.image.description="AI Sub-Agent for Code Context (MCP)"
LABEL org.opencontainers.image.url="https://github.com/kaffyn/vectora"
LABEL org.opencontainers.image.source="https://github.com/kaffyn/vectora"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.vendor="Kaffyn"
```

**Dockerfile para Desenvolvimento (com mais ferramentas)**:

```dockerfile
# Dockerfile.dev - Development image com debug tools
FROM golang:1.21-alpine AS dev

WORKDIR /workspace

# Instalar ferramentas de debug
RUN apk add --no-cache \
    git \
    ca-certificates \
    curl \
    vim \
    bash \
    delve \
    make

# Copiar código
COPY . .

# Download de deps
RUN go mod download

# Expor porta para debug
EXPOSE 2345

# Modo debug com Delve
CMD ["dlv", "debug", "-l", "0.0.0.0:2345", "--headless", "--api-version=2", "./cmd/vectora"]
```

### **Fase 2: Dockerfile para Managed Instances (Cloud)**

**Duração**: 1 semana

**Deliverables**:

- [ ] Imagem completa (Core + MCP Server + Guardian)
- [ ] Suporte para injeção de configuração via variáveis de ambiente
- [ ] Suporte para MongoDB connection string
- [ ] Provisioning automático de API keys
- [ ] Logging estruturado para Kubernetes

**Código de Exemplo - Dockerfile.managed**:

```dockerfile
# Dockerfile.managed - Para Managed Instances (Kubernetes)

FROM golang:1.21-alpine AS builder

WORKDIR /build
RUN apk add --no-cache git ca-certificates tzdata

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build com todas as features
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w \
    -X main.Version=${BUILD_VERSION:-dev} \
    -X main.Environment=production \
    -X main.ManagedMode=true" \
    -o /build/dist/vectora-core ./cmd/vectora

# Stage 2: Runtime (Kubernetes-ready)
FROM alpine:3.19

RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    curl \
    dumb-init

# User não-root
RUN addgroup -g 1000 vectora && adduser -D -u 1000 -G vectora vectora

COPY --from=builder --chown=vectora:vectora /build/dist/vectora-core /usr/local/bin/vectora

# Diretórios para volume mounts
RUN mkdir -p \
    /home/vectora/.config/vectora \
    /home/vectora/.cache/vectora \
    /var/log/vectora && \
    chown -R vectora:vectora /home/vectora /var/log/vectora

USER vectora
WORKDIR /home/vectora

# Variáveis de ambiente padrão
ENV VECTORA_MODE=managed
ENV VECTORA_LOG_LEVEL=info
ENV VECTORA_LOG_FORMAT=json

# Healthcheck (Kubernetes liveness)
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD vectora health --mongodb ${MONGODB_URI:-mongodb://localhost:27017}

# dumb-init para signal handling correto
ENTRYPOINT ["/sbin/dumb-init", "--"]
CMD ["vectora", "server", "--managed-mode"]

LABEL org.opencontainers.image.title="Vectora Managed"
LABEL org.opencontainers.image.description="Vectora Core for Kubernetes Managed Instances"
```

### **Fase 3: docker-compose.yml (Desenvolvimento Local)**

**Duração**: 3 dias

**Deliverables**:

- [ ] Docker Compose para stack completo (local)
- [ ] MongoDB local + Redis
- [ ] Vectora Core
- [ ] Volumes para código
- [ ] Network isolada

**Código de Exemplo - docker-compose.yml**:

```yaml
version: "3.9"

services:
  # MongoDB para vector storage
  mongodb:
    image: mongo:7.0
    container_name: vectora-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: vectora
      MONGO_INITDB_ROOT_PASSWORD: dev-password-only
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
    networks:
      - vectora-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 3

  # Redis para cache (opcional)
  redis:
    image: redis:7-alpine
    container_name: vectora-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - vectora-network
    healthcheck:
      test: redis-cli ping
      interval: 10s
      timeout: 5s
      retries: 3

  # Vectora Core
  vectora:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        BUILD_VERSION: "dev-local"
    container_name: vectora-core
    ports:
      - "8080:8080" # HTTP gateway
    environment:
      # MongoDB
      MONGODB_URI: "mongodb://vectora:dev-password-only@mongodb:27017/vectora?authSource=admin"

      # Providers
      GEMINI_API_KEY: ${GEMINI_API_KEY:-}
      VOYAGE_API_KEY: ${VOYAGE_API_KEY:-}

      # Logging
      LOG_LEVEL: "debug"
      LOG_FORMAT: "json"

      # Mode
      VECTORA_MODE: "development"
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      # Code mounting para hot reload (se suportado)
      - .:/workspace
      # Cache
      - vectora_cache:/home/vectora/.cache/vectora
      # Config
      - ./config/local.yaml:/home/vectora/.config/vectora/config.yaml:ro
    networks:
      - vectora-network
    command: vectora server --config /home/vectora/.config/vectora/config.yaml

volumes:
  mongodb_data:
  mongodb_config:
  redis_data:
  vectora_cache:

networks:
  vectora-network:
    driver: bridge
```

**Código de Exemplo - docker-compose.prod.yml** (Production-like):

```yaml
version: "3.9"

services:
  mongodb:
    image: mongo:7.0
    container_name: vectora-mongodb-prod
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGODB_USER:-vectora}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PASSWORD}
    volumes:
      - mongodb_prod_data:/data/db
    networks:
      - vectora-network-prod
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  vectora:
    image: kaffyn/vectora:${VECTORA_VERSION:-latest}
    container_name: vectora-core-prod
    ports:
      - "8080:8080"
    environment:
      MONGODB_URI: "mongodb://${MONGODB_USER:-vectora}:${MONGODB_PASSWORD}@mongodb:27017/vectora?authSource=admin"
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      VOYAGE_API_KEY: ${VOYAGE_API_KEY}
      LOG_LEVEL: "info"
      VECTORA_MODE: "production"
    depends_on:
      - mongodb
    networks:
      - vectora-network-prod
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

volumes:
  mongodb_prod_data:

networks:
  vectora-network-prod:
    driver: bridge
```

**Arquivo .env (Template)**:

```bash
# .env.example - Copiar para .env e preencher

# MongoDB
MONGODB_USER=vectora
MONGODB_PASSWORD=change-me-in-production

# API Keys (obter em console.vectora.app)
GEMINI_API_KEY=your-gemini-key-here
VOYAGE_API_KEY=your-voyage-key-here

# Versão do Vectora
VECTORA_VERSION=latest

# Logging
LOG_LEVEL=debug
```

### **Fase 4: Integração com GitHub Actions & GoReleaser**

**Duração**: 1 semana

**Deliverables**:

- [ ] Build de imagem Docker no GoReleaser
- [ ] Push automático para Docker Hub
- [ ] Tagging multi-arch
- [ ] Verificação de integridade
- [ ] SBOM (Software Bill of Materials)

**Atualizar .goreleaser.yml**:

```yaml
# .goreleaser.yml - adicionar docker config

dockers:
  - image_templates:
      - "docker.io/kaffyn/vectora:{{ .Version }}-amd64"
      - "docker.io/kaffyn/vectora:latest-amd64"
    dockerfile: Dockerfile
    use: buildx
    build_flag_templates:
      - "--platform=linux/amd64"
      - "--label=org.opencontainers.image.title={{.ProjectName}}"
      - "--label=org.opencontainers.image.description=AI Sub-Agent for Code Context"
      - "--label=org.opencontainers.image.url=https://github.com/kaffyn/vectora"
      - "--label=org.opencontainers.image.version={{.Version}}"
      - "--label=org.opencontainers.image.revision={{.FullCommit}}"
      - "--label=org.opencontainers.image.created={{.Date}}"

  - image_templates:
      - "docker.io/kaffyn/vectora:{{ .Version }}-arm64"
      - "docker.io/kaffyn/vectora:latest-arm64"
    dockerfile: Dockerfile
    use: buildx
    build_flag_templates:
      - "--platform=linux/arm64"
      - "--label=org.opencontainers.image.version={{.Version}}"

docker_manifests:
  - name_template: "docker.io/kaffyn/vectora:{{ .Version }}"
    image_templates:
      - "docker.io/kaffyn/vectora:{{ .Version }}-amd64"
      - "docker.io/kaffyn/vectora:{{ .Version }}-arm64"

  - name_template: "docker.io/kaffyn/vectora:latest"
    image_templates:
      - "docker.io/kaffyn/vectora:latest-amd64"
      - "docker.io/kaffyn/vectora:latest-arm64"
```

**Workflow GitHub Actions - .github/workflows/docker-release.yml**:

```yaml
name: Docker Release

on:
  push:
    tags:
      - "v*"

env:
  REGISTRY: docker.io
  IMAGE_NAME: kaffyn/vectora

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Generate SBOM
        run: |
          # Gerar SBOM via syft (instalar se necessário)
          curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
          syft ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }} -o cyclonedx-json > sbom.cyclonedx.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.cyclonedx.json

      - name: Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload: |
            {
              "text": "Docker Release ${{ github.ref_name }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Status: ${{ job.status }}\nImage: `docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}`\n[Docker Hub](https://hub.docker.com/r/${{ env.IMAGE_NAME }})"
                  }
                }
              ]
            }
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### **Fase 5: Kubernetes Deployment (Managed Instances)**

**Duração**: 2 semanas

**Deliverables**:

- [ ] Helm chart para Vectora
- [ ] StatefulSet com persistent volumes
- [ ] Service + Ingress
- [ ] ConfigMap + Secrets
- [ ] HPA (Horizontal Pod Autoscaler)

**Código de Exemplo - k8s/deployment.yaml**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vectora-core
  namespace: vectora-system
  labels:
    app: vectora-core
    version: v2.1.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: vectora-core
  template:
    metadata:
      labels:
        app: vectora-core
        version: v2.1.0
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      containers:
        - name: vectora
          image: kaffyn/vectora:latest
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
            - name: mcp
              containerPort: 9090
              protocol: TCP

          env:
            - name: VECTORA_MODE
              value: "managed"

            - name: MONGODB_URI
              valueFrom:
                secretKeyRef:
                  name: vectora-secrets
                  key: mongodb-uri

            - name: GEMINI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: vectora-secrets
                  key: gemini-api-key

            - name: VOYAGE_API_KEY
              valueFrom:
                secretKeyRef:
                  name: vectora-secrets
                  key: voyage-api-key

            - name: LOG_LEVEL
              value: "info"

            - name: LOG_FORMAT
              value: "json"

          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"

          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2

          volumeMounts:
            - name: config
              mountPath: /home/vectora/.config/vectora
              readOnly: true
            - name: cache
              mountPath: /home/vectora/.cache/vectora

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

      volumes:
        - name: config
          configMap:
            name: vectora-config
        - name: cache
          emptyDir: {}

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - vectora-core
                topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: Service
metadata:
  name: vectora-core
  namespace: vectora-system
spec:
  type: ClusterIP
  selector:
    app: vectora-core
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
    - name: mcp
      port: 9090
      targetPort: 9090
      protocol: TCP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vectora-core-hpa
  namespace: vectora-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vectora-core
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### **Fase 6: Testes & Validação**

**Duração**: 1 semana

**Deliverables**:

- [ ] Testes de imagem Docker
- [ ] Verificação de segurança (Trivy)
- [ ] Performance benchmarks
- [ ] Teste em Kubernetes local (kind)

**Script de Teste - .github/scripts/test-docker.sh**:

```bash
#!/bin/bash
set -e

echo " Testing Docker image..."

VERSION=${1:-latest}
IMAGE="kaffyn/vectora:${VERSION}"

# 1. Build local
echo " Building image..."
docker build -t "${IMAGE}" .

# 2. Verificar tamanho
SIZE=$(docker image inspect "${IMAGE}" --format='{{.Size}}' | numfmt --to=iec)
echo " Image size: ${SIZE}"

# 3. Scan com Trivy (se disponível)
if command -v trivy &> /dev/null; then
    echo " Running security scan with Trivy..."
    trivy image "${IMAGE}" || echo " Trivy scan found issues (check manually)"
fi

# 4. Test run básico
echo " Testing container execution..."
docker run --rm "${IMAGE}" --version

# 5. Test health endpoint
echo " Testing health check..."
docker run --rm -d --name vectora-test "${IMAGE}" || true
sleep 2
if docker inspect --format='{{.State.Running}}' vectora-test 2>/dev/null | grep -q true; then
    echo " Container running"
    docker stop vectora-test || true
else
    echo " Container failed to start"
    docker logs vectora-test || true
    exit 1
fi

echo " All Docker tests passed!"
```

### **Fase 7: Documentação & Best Practices**

**Duração**: 3 dias

**Deliverables**:

- [ ] Guia de instalação Docker
- [ ] Exemplos docker-compose
- [ ] Troubleshooting
- [ ] Security best practices
- [ ] Performance tuning

## Checklist de Release

Antes de publicar Docker images:

- [ ] Testes unitários passam (`make test`)
- [ ] Linting passa (`make lint`)
- [ ] Dockerfile constrói sem erros
- [ ] Imagem funciona localmente (`docker run ...`)
- [ ] Scan de segurança (Trivy) limpo
- [ ] SBOM gerado e verificado
- [ ] Docker Hub credentials configurados
- [ ] Tag Git criada (`git tag v2.1.0`)
- [ ] Push para GitHub (`git push origin v2.1.0`)
- [ ] CI/CD completa com sucesso
- [ ] Imagem disponível em Docker Hub
- [ ] Documentação atualizada

## Métricas de Sucesso

| Métrica                       | Alvo          |
| :---------------------------- | :------------ |
| Tempo de build (Docker)       | <5 minutos    |
| Tamanho final da imagem       | <150MB        |
| Suporte multi-arch            | amd64/arm64   |
| Tempo de startup              | <5 segundos   |
| Taxa de sucesso em Kubernetes | >99%          |
| Security score (Trivy)        | CRITICAL: 0   |
| Pull/pull rate limit (Docker) | <50% capacity |
| Uptime em produção            | >99.9%        |

---

## External Linking

| Concept            | Resource                                       | Link                                                                                                       |
| ------------------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Docker**         | Docker Documentation                           | [docs.docker.com/](https://docs.docker.com/)                                                               |
| **MongoDB Atlas**  | Atlas Vector Search Documentation              | [www.mongodb.com/docs/atlas/atlas-vector-search/](https://www.mongodb.com/docs/atlas/atlas-vector-search/) |
| **Kubernetes**     | Kubernetes Official Documentation              | [kubernetes.io/docs/](https://kubernetes.io/docs/)                                                         |
| **MCP**            | Model Context Protocol Specification           | [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)                     |
| **MCP Go SDK**     | Go SDK for MCP (mark3labs)                     | [github.com/mark3labs/mcp-go](https://github.com/mark3labs/mcp-go)                                         |
| **GitHub Actions** | Automate your workflow from idea to production | [docs.github.com/en/actions](https://docs.github.com/en/actions)                                           |

---

_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)
