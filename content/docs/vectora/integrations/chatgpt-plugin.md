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

**APP PRÓPRIO**: Vectora funciona como um **Custom GPT Plugin** que estende ChatGPT com busca de contexto de codebase. Arquitetura dedicada com OpenAPI schema, ngrok/endpoint público, e publicação na OpenAI plugin store.

> [!IMPORTANT]
> ChatGPT Custom GPT Plugin (app próprio) vs MCP Protocol (genérico). Escolha conforme sua IDE/plataforma preferida.

## Instalação

## Pré-requisitos

- ChatGPT Plus (com acesso a Custom GPTs)
- Servidor Vectora rodando (`vectora mcp` ou `vectora server`)
- Endpoint público ou ngrok tunnel

## Passo 1: Configurar Servidor Vectora Público

Por padrão, Vectora roda em `localhost:9090`. Para ChatGPT alcançar, você precisa expor:

#### Opção A: ngrok (Teste)

```bash
# Instale ngrok
# https://ngrok.com

# Exponha porta 9090
ngrok http 9090

# Output:
# Forwarding: https://xxxx-xx-xxx-xx-x.ngrok.io -> http://localhost:9090

# Copie o URL
```

#### Opção B: VPS com IP público (Produção)

```bash
# Em seu servidor
vectora server --host 0.0.0.0 --port 9090

# Expose via firewall
# iptables -A INPUT -p tcp --dport 9090 -j ACCEPT
```

#### Opção C: Managed Vectora (Cloud)

```bash
# Registre em https://console.vectora.app
# Obtenha endpoint automático
# https://api.vectora.app/v1/your-project-id
```

## Passo 2: Criar Custom GPT no ChatGPT

1. Vá para [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor)
2. Clique em **"Create a new GPT"**
3. Nome: "Vectora Codebase Assistant"
4. Descrição: "Assistente inteligente para análise de codebase com Vectora"

## Passo 3: Configurar Schema OpenAPI

Na aba **"Configure"** → **"Actions"**, adicione seu endpoint Vectora:

```yaml
openapi: 3.0.0
info:
  title: Vectora API
  version: 1.0.0
servers:
  - url: https://xxxx-xx-xxx-xx-x.ngrok.io # Seu endpoint
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

---

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

---

## Autenticação & Segurança

## Token-based Auth

Se seu servidor requer autenticação:

```yaml
# Schema OpenAPI
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

Configure no GPT:

```text
Vá para "Configure" → "Authentication"
Selecione "API Key"
Cole seu token
```

## Rate Limiting

Proteja seu servidor:

```bash
# Em vectora config
server:
  rate_limit_per_hour: 1000
  max_concurrent: 5
```

---

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

---

## Troubleshooting

## "Plugin not responding"

**Causa**: Servidor Vectora offline.

**Solução**:

```bash
# Verificar se está rodando
curl https://seu-endpoint/health

# Se retorna 404, inicie
vectora mcp
```

## "Unauthorized"

**Causa**: Token inválido ou expirado.

**Solução**:

```bash
# Gerar novo token
vectora auth create-token --name "ChatGPT Plugin" --ttl 365d

# Atualizar no Custom GPT settings
```

## "Timeout"

**Causa**: Busca muito lenta.

**Solução**:

```bash
# Reduzir top_k
# Na instrução do GPT, modifique para:
"Use top_k=5 ao invés de 10"

# Ou aumentar timeout
curl -X POST https://seu-endpoint/search \
  -H "Timeout: 10000" \
  -d "{...}"
```

---

## Performance & Limits

| Recurso              | Limite | Upgrade         |
| -------------------- | ------ | --------------- |
| Busca/dia            | 10,000 | Plano Pro       |
| Latência             | <2s    | SSD + mais CPU  |
| Tamanho resposta     | 5MB    | Compaction      |
| Usuários simultâneos | 10     | Managed Vectora |

---

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

---

## Monitoramento

Via console Vectora:

```bash
vectora logs --service chatgpt_plugin --level info

# Exemplo output:
# [2026-04-19 10:30:45] POST /search - 200 - 234ms
# [2026-04-19 10:31:12] POST /analyze-dependencies - 200 - 156ms
# [2026-04-19 10:32:00] POST /file-summary - 200 - 89ms
```

---

> **Próximo**: [Gemini API](./gemini-api.md)

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
