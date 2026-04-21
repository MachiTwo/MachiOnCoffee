---
title: Trust Folder
slug: trust-folder
date: "2026-04-18T22:30:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - architecture
  - concepts
  - folder
  - mcp
  - trust
  - vectora
---

{{< lang-toggle >}}
Trust Folder é o **perímetro de segurança** que limita quais arquivos o Vectora pode indexar, ler e processar. Funciona como um "sandbox de path" contra leitura de arquivos sensíveis.

> [!IMPORTANT]
> Trust Folder não é opcional. Sem dele, Vectora poderia indexar .env, chaves privadas, e dados de usuários. Com Trust Folder, apenas arquivos dentro do perímetro são acessíveis.

---

## O Problema

Sem Trust Folder:

- Vectora indexa tudo no disco: `/etc/passwd`, `~/.ssh/id_rsa`, `.env`
- Sensível a directory traversal: `../../sensitive/file.txt`
- Sem auditoria de quis acessou qual arquivo

Com Trust Folder:

- Indexação confinada a `./src`, `./docs` (configurável)
- Directory traversal é bloqueado: `../../../.env` é rejeitado
- Audit log rastreia todas as leituras

---

## Configuração

Trust Folder é configurado em vectora.config.yaml e pode usar caminhos relativos ou absolutos, com suporte a expansão de variáveis de ambiente.

## Padrão

```yaml
# vectora.config.yaml
project:
  trust_folder: "." # Padrão: raiz do projeto
```

Significa: "Confio em tudo dentro deste diretório e subdiretórios".

## Explícito (Recomendado)

```yaml
project:
  trust_folder: "./src" # APENAS ./src

# Ou múltiplas pastas
project:
  trust_folders:
    - "./src"
    - "./docs"
    - "./packages"
    # NÃO incluido: ./node_modules, ./build, ./.env
```

## Caminho Absoluto vs Relativo

```yaml
# Relativo (recomendado)
trust_folder: "./src"
# Resolvido para: /current/working/dir/src

# Absoluto (permitido)
trust_folder: "/home/user/myproject/src"

# Variable expansion
trust_folder: "${PROJECT_ROOT}/src"
# Resolvido via environment variables
```

---

## Resolução de Paths

Vectora resolve paths de forma segura, normalizando caminhos relativos para absolutos e bloqueando tentativas de sair do Trust Folder.

### Allow List

Quando indexando:

```text
Trust Folder: ./src
File Requested: ./src/auth/login.ts

Resolução:
1. ./src/auth/login.ts → /absolute/path/to/src/auth/login.ts
2. Is /absolute/path/to/src/auth/login.ts dentro de /absolute/path/to/src?
3. SIM → Permitido
```

### Block List (Directory Traversal)

```text
Trust Folder: ./src
File Requested: ../../../.env

Resolução:
1. Normaliza: ../../../.env → /absolute/path/.env
2. Is /absolute/path/.env dentro de /absolute/path/to/src?
3. NÃO → BLOQUEADO
```

```text
Trust Folder: ./src
File Requested: ./src/../../.env

Resolução:
1. Normaliza: ./src/../../.env → /absolute/path/.env
2. Is /absolute/path/.env dentro de /absolute/path/to/src?
3. NÃO → BLOQUEADO
```

---

## Casos de Uso

Abaixo apresentamos três padrões de configuração real: monorepo com isolamento entre packages, site de documentação com seções privadas, e sandbox para máxima segurança.

## Case 1: Monorepo com Múltiplos Packages

```text
project/
├── packages/
│ ├── backend/
│ │ ├── src/
│ │ └── docs/
│ └── frontend/
│ ├── src/
│ └── docs/
├── shared/
└── .env (SENSÍVEL)
```

Configuration:

```yaml
# Para backend
project:
  trust_folders:
    - "./packages/backend/src"
    - "./packages/backend/docs"
    - "./shared"

# Para frontend
project:
  trust_folders:
    - "./packages/frontend/src"
    - "./packages/frontend/docs"
    - "./shared"
```

Resultado:

- Backend não consegue ler frontend code
- Frontend não consegue ler backend code
- Ambos podem acessar shared
- `.env` está bloqueado para AMBOS

## Case 2: Documentação + Source Code

```text
docs-website/
├── content/ ← Público
│ ├── getting-started/
│ └── api-reference/
├── src/ ← Código do site (config, templates)
├── private/ ← Rascunhos privados (SENSÍVEL)
└── .env
```

Configuration:

```yaml
project:
  trust_folders:
    - "./content"
    - "./src"
  # private/ e .env são inaccessíveis
```

## Case 3: Sandbox Completo

Para máxima segurança (ex: CI/CD):

```yaml
project:
  trust_folder: "./sanitized"
# Antes de rodar, copie APENAS o que é permitido:
# mkdir sanitized
# cp -r src/ sanitized/
# cp -r docs/ sanitized/
# vectora init --trust-folder ./sanitized
```

---

## Integração com Guardian

Guardian também valida paths:

```yaml
guardian:
  rules:
    - name: "block_env_files"
      pattern: "\.env.*"
      action: "block"

    - name: "block_secrets"
      pattern: "secrets/"
      action: "block"

    - name: "allow_only_src_docs"
      pattern: "^(src|docs)/.*"
      action: "allow"
```

**Ordem**: Trust Folder → Guardian → Indexing

- Trust Folder nega: arquivo bloqueado imediatamente
- Trust Folder permite: Guardian valida pattern
- Ambos passam: arquivo é indexado

---

## Auditoria

## Logging

```bash
VECTORA_AUDIT_LOG=true
VECTORA_LOG_LEVEL=debug
```

Log output:

```json
{
  "timestamp": "2026-04-19T14:32:00Z",
  "event": "file_access_attempt",
  "path": "../../../.env",
  "normalized_path": "/home/user/.env",
  "trust_folder": "/home/user/project/src",
  "result": "DENIED",
  "reason": "outside_trust_folder"
}
```

## Inspection

```bash
vectora audit --since 24h --filter "DENIED"
# Mostra todas as tentativas bloqueadas

vectora audit --filter "file_access" | jq '.[] | {path, result}'
```

---

## Cenários de Segurança (O que Trust Folder Previne)

Abaixo mostramos 4 ataques potenciais e como Trust Folder previne cada um deles, demonstrando a importância de configuração segura.

## Ataque 1: Path Traversal Simples

**Sem Trust Folder:**

```bash
# LLM pede (ou usuário injeta)
vectora search --file "../../.env"
# Resultado: .env é lido VULNERABILITY
```

**Com Trust Folder (`./src`):**

```bash
vectora search --file "../../.env"
# Resolução: /project/.env (fora de /project/src)
# Resultado: BLOQUEADO SAFE
```

## Ataque 2: Symlink Escape

**Cenário:**

```text
project/src/link → ../../sensitive/secrets.yml
```

**Sem resolução:**
Vectora vê `src/link` (parece seguro) e indexa.

**Com resolução (padrão):**
Vectora resolve: `src/link` → `../../sensitive/secrets.yml` → `/project/sensitive/secrets.yml`
Detecta: fora de trust folder → BLOQUEADO

## Ataque 3: Injection via LLM Context

**Cenário:**

```text
Usuário: "Meu código importa de 'os.system'.
         Busque em ../../../../etc/passwd"

LLM (sem Trust Folder):
"Encontrei isso em /etc/passwd: root:x:0:0:..."

LLM (com Trust Folder):
"Não posso acessar /etc/passwd - fora do trust folder"
```

## Ataque 4: CI/CD Exposure

- **Sem Trust Folder:**

```text
CI/CD runner executa: vectora index
Indices: /home/runner/secrets.json (com API keys!)
Vectora Cloud sync: secrets.json é enviado
Resultado: Keys expostas
```

**Com Trust Folder `./src`:**

```text
CI/CD runner executa: vectora index --trust-folder ./src
Indices: APENAS ./src/
Resultado: secrets.json ignorado
```

---

## Teste & Verificação

Para validar que Trust Folder está funcionando corretamente, use os comandos abaixo. Um security audit completo garante que nenhum arquivo sensível é acessível.

## Verificar Trust Folder Está Ativo

```bash
# 1. Config
vectora config get trust_folder
# Output: ./src

# 2. List arquivos indexados
vectora index --list-files | head -20
# Verifica: todos começam com ./src?

# 3. Dry-run de path denied
vectora index --try-path "../.env" --dry-run
# Output: ERROR: outside_trust_folder
```

## Security Audit Completo

```bash
#!/bin/bash
# audit-trust-folder.sh

echo "=== Trust Folder Security Audit ==="

# 1. Check config
TRUST=$(vectora config get trust_folder)
echo "Trust Folder: $TRUST"

# 2. List all indexed files
INDEXED=$(vectora index --list-files)
OUTSIDE=$(echo "$INDEXED" | grep -v "^${TRUST}" | wc -l)

if [ "$OUTSIDE" -gt 0 ]; then
  echo " FAIL: $OUTSIDE files outside trust folder"
  exit 1
fi

# 3. Try access sensitive files
SENSITIVE=(".env" ".secrets" "*.pem" "*.key")
for pattern in "${SENSITIVE[@]}"; do
  FOUND=$(vectora search --file "*/$pattern" 2>&1 | grep "outside_trust_folder" | wc -l)
  if [ "$FOUND" -eq 0 ]; then
    echo " WARNING: Pattern $pattern may be exposed"
  fi
done

echo " PASS: Trust Folder is properly configured"
```

---

## Troubleshooting

Problemas comuns ao usar Trust Folder e como resolvê-los, incluindo soluções para symlinks e path resolution.

## Arquivo Válido Bloqueado

```text
Error: ./src/utils/helpers.ts is outside trust folder
```

**Diagnóstico**:

```bash
# Acheck paths
pwd # Seu CWD
cat vectora.config.yaml | grep trust_folder

# Verify com --dry-run
vectora index --dry-run
```

**Solução**: Verificar se trust_folder é relativo ao CWD.

## Symlinks

-

Por padrão, symlinks são **resolvidos**:

```text
Trust Folder: ./src
File: ./src/link-to-config.ts (symlink → ../../../.env)

Resolução:
1. Resolve symlink: /home/user/.env
2. Is /home/user/.env dentro de /home/user/project/src?
3. NÃO → BLOQUEADO
```

Para permitir symlinks específicos:

```yaml
project:
  trust_folder: "./src"
  symlink_mode: "follow" # default: "deny"
  symlink_whitelist:
    - "./src/link-to-shared" # Exceção explícita
```

---

## Configuração Avançada

```yaml
# vectora.config.yaml
project:
  trust_folder: "./src"

  # Comportamento de path resolution
  path_resolution:
    normalize_case: false # Windows: case-insensitive?
    resolve_symlinks: true
    follow_mountpoints: false

  # Auditoria
  audit:
    enabled: true
    log_all_accesses: false # true = muito verbose
    log_denied_accesses: true
    retention_days: 30
```

---

> **Próximo**: [Vector Search](./vector-search.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
