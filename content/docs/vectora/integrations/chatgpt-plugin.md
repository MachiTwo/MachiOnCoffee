---
title: ChatGPT Plugin
slug: chatgpt-plugin
date: "2026-04-19T09:50:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - ai
  - chatgpt
  - integration
  - plugins
  - openai
  - vectora
---

{{< lang-toggle >}}
{{< section-toggle >}}

**INTEGRAÇÃO COM VECTORA CLOUD**: Vectora funciona como um **Custom GPT Plugin** que estende ChatGPT com busca de contexto de codebase. O plugin conecta diretamente ao **Vectora Cloud**, que executa o Vectora Core gerenciado internamente, sem necessidade de configurar servidores locais.

> [!IMPORTANT] ChatGPT Custom GPT Plugin (via Vectora Cloud) vs MCP Protocol (IDE local). Escolha conforme sua preferência: Cloud para ChatGPT, MCP para Claude Code/Cursor.

## Instalação

## Pré-requisitos

- ChatGPT Plus (com acesso a Custom GPTs)
- Conta em [Vectora Cloud](https://console.vectora.app) (Pro, Team ou Enterprise)
- Projeto com indexação completa

## Passo 1: Obter Credenciais do Vectora Cloud

1. Acesse [console.vectora.app](https://console.vectora.app)
2. Selecione seu projeto
3. Vá para **Settings → API Keys**
4. Clique em **"New API Key"**
5. Configure:
   - **Name**: "ChatGPT Plugin"
   - **Scope**: `search` (leitura apenas)
   - **Expires**: 1 ano
6. Copie o token gerado: `vca_live_xxxxxxxxxxxxxxxxxxxxxxxx`

## Passo 2: Criar Custom GPT no ChatGPT

1. Vá para [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor)
2. Clique em **"Create a new GPT"**
3. Nome: "Vectora Codebase Assistant"
4. Descrição: "Assistente inteligente para análise de codebase com Vectora Cloud"

## Passo 3: Configurar Schema OpenAPI

Na aba **"Configure"** → **"Actions"**, adicione o endpoint do Vectora Cloud:

```yaml
openapi: 3.0.0
info:
  title: Vectora Cloud API
  version: 1.0.0
servers:
  - url: https://api.vectora.app/v1/plugins # Endpoint gerenciado Vectora Cloud
paths:
  /search:
    post:
      summary: Search codebase context
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: "Search query (semantic)"
                namespace:
                  type: string
                  description: "Project namespace"
                top_k:
                  type: integer
                  default: 10
      responses:
        "200":
          description: Search results
          content:
            application/json:
              schema:
                type: object
                properties:
                  chunks:
                    type: array
                  precision:
                    type: number
  /analyze-dependencies:
    post:
      summary: Find all usages of a function
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                function_name:
                  type: string
                namespace:
                  type: string
      responses:
        "200":
          description: Dependency analysis
  /file-summary:
    post:
      summary: Get file structure and summary
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                file_path:
                  type: string
                namespace:
                  type: string
      responses:
        "200":
          description: File summary
```

## Passo 4: Adicionar Instrução de Sistema

Na aba **"Instructions"**, copie:

```text
Você é um assistente especializado em análise de código usando Vectora.

Quando o usuário pergunta sobre código:
1. Use a ação "search" para buscar contexto relevante
2. Use "analyze-dependencies" para encontrar relacionados
3. Use "file-summary" para entender estrutura

Sempre cite o arquivo e linha quando referencia código.
Priorize precisão sobre velocidade.

Exemplo bom:
"Encontrei isso em src/auth/jwt.ts:45:
function validateToken(token) { ... }"

Exemplo ruim:
"Acho que a função está em algum lugar"
```

## Passo 5: Publicar

Clique em **"Publish to Store"** e compartilhe com seu time.

## Workflows Detalhados

Os workflows abaixo demonstram casos de uso reais do Vectora integrado ao ChatGPT, mostrando conversas práticas e resultados concretos.

## Workflow 1: Entender Feature Complexa (Onboarding)

**Cenário**: Novo dev no time quer entender como funciona autenticação JWT.

```text
Você: "Como funciona o sistema de autenticação JWT aqui?"

ChatGPT (com Vectora):
Encontrei a implementação em 3 arquivos principais:

1. **src/auth/jwt.ts** (definição)
   function validateToken(token: string) {
     const decoded = jwt.verify(token, SECRET_KEY);
     return decoded.payload;
   }

2. **src/guards/auth.guard.ts** (aplicação em rotas)
   @UseGuards(AuthGuard)
   async getProfile(@Req() req) {
     // Já está autenticado aqui
   }

3. **src/tests/auth.test.ts** (exemplos)
   it('should reject expired token', () => {
     // Teste mostra comportamento esperado
   })

**Fluxo**:
request → AuthGuard.canActivate() → validateToken() → req.user = payload

**Próximos passos**: Adicione sua rota assim...
```

Clique em qualquer arquivo → abre em editor/navegador.

## Workflow 2: Debugging Estratégico

**Cenário**: Você tem um erro e precisa entender causa raiz.

```text
Você: "Teste 'should create user' está falhando com
      'Cannot read property id of undefined'.
      Onde é o problema?"

ChatGPT (com Vectora):
Procurando o teste e código relacionado...

**Achei o problema!**

Arquivo: src/__tests__/user.service.test.ts:145
  it('should create user', () => {
    const user = userService.create({ name: 'John' });
    expect(user.id).toBeDefined(); // ← Falha aqui
  })

Analisando userService.create():

  // src/services/user.service.ts:23
  create(data: CreateUserInput) {
    // Problema: não retorna o user criado
    db.insert(users).values(data);
    // Deveria ser:
    return db.insert(users).values(data).returning();
  }

**3 usuários desse padrão no código:**
  • src/services/order.service.ts:34
  • src/services/product.service.ts:12
  • src/services/invoice.service.ts:88

**Sugestão**: Aplicar mesmo fix nos 3 lugares.
```

## Workflow 3: Code Review Assistido (PR Complexa)

**Cenário**: Revisando uma PR que toca múltiplos arquivos de auth.

```text
Você: "Revise essa PR que refactora auth middleware.
       [cola 50 linhas de código]"

ChatGPT (com Vectora):
Analisando mudanças...

**Impacto Estimado**: 12 arquivos afetados
- 8 arquivos de rotas (GET /profile, etc)
- 2 testes de auth
- 2 guards

**Problemas detectados**:

1. Comportamento mudou em linha 23
   ANTES: guard.canActivate() retorna boolean
   AGORA: retorna Promise<boolean>

   Isso quebra em 4 lugares:
   - src/routes/admin.ts:45
   - src/routes/api.ts:78
   - src/middleware/verify.ts:12
   - src/guards/optional.ts:3

2. Positivo: Novo método isTokenValid() é reutilizado bem
   (encontrei 6 usos)

3. Segurança: GuardBlacklist está sendo respeitado
   (verifica todos os 4 patterns)

**Testes relacionados que DEVEM passar**:
□ auth.guard.test.ts
□ jwt.validation.test.ts
□ permission.test.ts
□ integration/auth-flow.test.ts

**Conclusão**: Aprove com condições:
1. Corrigir os 4 arquivos (async/await)
2. Rodar full test suite
3. Check: nenhum SECRET_KEY exposto
```

## Autenticação & Segurança

## Token-based Auth

Se seu servidor requer autenticação:

```yaml
# Schema OpenAPI
components:
  securitySchemes:
    apiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - apiKeyAuth: []
```

Configure no GPT:

```text
Vá para "Configure" → "Authentication"
Selecione "API Key"
Cole sua API Key do Vectora Cloud
Header name: X-API-Key
```

## Rate Limiting

Proteja seu servidor:

```bash
# Em vectora config
server:
  rate_limit_per_hour: 1000
  max_concurrent: 5
```

## Privacidade & Compliance

## O que é Enviado para OpenAI

- Sua pergunta (texto)
- Parâmetros de busca (namespace, top_k)
- **Chunks NÃO são salvos** na OpenAI

## O que Permanece Local

- Índices vetoriais (Qdrant)
- Embeddings brutos
- Credenciais de API

## Dados Criptografados

```bash
# Habilitar criptografia ponta-a-ponta
vectora config set --key "ENCRYPT_TRANSIT" --value "true"

# Certificado SSL/TLS
openssl req -x509 -newkey rsa:4096 -out cert.pem -keyout key.pem

# Usar com HTTPS
vectora server --cert cert.pem --key key.pem
```

## Troubleshooting

## "Plugin not responding"

**Causa**: Índice não está pronto ou instância Cloud offline.

**Solução**:

```bash
# Verificar status da indexação em https://console.vectora.app
# Settings → Indexing → View Progress

# Se ainda indexando, aguarde conclusão
# Geralmente leva minutos a horas dependendo do tamanho
```

## "Unauthorized"

**Causa**: API Key inválida, expirada ou sem escopo `search`.

**Solução**:

```bash
# Gerar nova API Key em console.vectora.app
# Settings → API Keys → New API Key
# Scope: "search"
# Ttl: 1 year

# Atualizar no Custom GPT:
# Configure → Authentication → Cole a chave nova
```

## "Timeout (>30s)"

**Causa**: Busca muito complexa ou muitos documentos.

**Solução**:

```bash
# Reduzir top_k na instrução do GPT para:
"Use sempre top_k=5 (máximo 10) para respostas rápidas"

# Ou verificar em console.vectora.app:
# Analytics → Query Performance
# Se latência > 2s, considere upgrade Pro → Team
```

## Performance & Quotas (Vectora Cloud)

| Recurso            | Free  | Pro    | Team    | Enterprise |
| ------------------ | ----- | ------ | ------- | ---------- |
| Buscas/dia         | 100   | 10,000 | 100,000 | Ilimitado  |
| Latência P95       | <3s   | <2s    | <500ms  | <250ms     |
| Concurrent queries | 1     | 5      | 20      | Ilimitado  |
| Storage            | 512MB | 5GB    | 50GB    | Custom     |
| **ChatGPT Plugin** |       |        |         |            |

## Exemplos Avançados

## Custom GPT para Design Review

```text
Instrução:
"Você é um Design Reviewer baseado em Vectora.
Quando o usuário mostra código:
1. Procure por padrões similares no projeto
2. Avalie consistência
3. Sugira melhorias baseado em style guides existentes
4. Cite exemplos do codebase"
```

## Custom GPT para Onboarding

```text
Instrução:
"Você é um Onboarding Assistant.
Novos engenheiros perguntam como o código funciona.
Use Vectora para:
1. Buscar documentação
2. Encontrar exemplos
3. Listar dependências
4. Sugerir arquivos para ler primeiro"
```

## Monitoramento & Analytics

Via [console.vectora.app](https://console.vectora.app):

1. **Analytics → ChatGPT Plugin**

   - Queries totais por dia
   - Latência média/P95
   - Taxa de erro
   - Top queries

2. **Logs → Integration**
   - Últimas 100 chamadas
   - Status, latência, tokens usados
   - Erros detalhados

Exemplo:

```text
[2026-04-19 10:30:45] ChatGPT Plugin /search - 200 OK - 234ms - 5 chunks
[2026-04-19 10:31:12] ChatGPT Plugin /analyze - 200 OK - 156ms - 3 files
[2026-04-19 10:32:00] ChatGPT Plugin /file-summary - 200 OK - 89ms
```

---

> **Próximo**: [Gemini API](./gemini-api.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
