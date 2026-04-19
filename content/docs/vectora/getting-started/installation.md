---
title: Instalação
slug: installation
date: "2026-04-19T08:00:00-03:00"
type: docs
sidebar:
  open: true
tags:
  - getting-started
  - installation
  - setup
  - npm
  - vectora
  - byok
  - api-keys
---

{{< lang-toggle >}}

## Visão Geral

Vectora é instalado globalmente via npm como um agent MCP (Model Context Protocol). A instalação leva menos de 5 minutos e requer apenas Node.js 18+ e chaves de API gratuitas.

> [!IMPORTANT] > **BYOK (Bring Your Own Key)**: No plano Free, o Vectora exige chaves de API do Gemini e Voyage. Nos planos **Pro** e **Team (Plus)**, você pode optar pelo modo **Managed**, onde os créditos de IA já estão inclusos.

---

## Pré-requisitos

### Sistema Operacional

- **macOS** 12.0+
- **Linux** (Ubuntu 20.04+, Fedora 35+, Debian 11+)
- **Windows 11** (WSL2 recomendado)

### Software

- **Node.js** 18.0.0 ou superior ([download](https://nodejs.org))
- **npm** 9.0.0+ (incluído com Node.js)
- **git** 2.30+ (opcional, para clonar repositórios)

### Verificar Pré-requisitos

```bash
node --version # Deve retornar v18.0.0 ou superior
npm --version # Deve retornar 9.0.0 ou superior
```

---

## Passo 1: Instalar Vectora Globalmente

```bash
npm install -g @kaffyn/vectora
```

**Tempo esperado**: 2-3 minutos (primeira instalação)

### Verificar Instalação

```bash
vectora --version
# Output esperado: vectora/1.x.x
```

Se o comando não for encontrado, você pode precisar atualizar seu `PATH`:

```bash
# macOS / Linux
export PATH="$PATH:$(npm config get prefix)/bin"

# Adicione a linha acima ao seu ~/.bashrc ou ~/.zshrc para persistência
```

---

## Passo 2: Obter Chaves de API Gratuitas

### Gemini API (Google)

1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Clique em **"Create API Key"**
3. Copie a chave gerada

**Limite gratuito**: 60 requisições por minuto, 1.5M tokens/mês

### Voyage API (VoyageAI)

1. Acesse [Voyage AI Dashboard](https://dash.voyageai.com/api-keys)
2. Clique em **"Create API Key"**
3. Copie a chave gerada

**Limite gratuito**: 50 requisições por minuto, 100M tokens/mês

---

## Passo 3: Configurar Variáveis de Ambiente

### Opção A: Arquivo `.env` Local (Recomendado)

Crie um arquivo `.env` na raiz do seu projeto:

```bash
cat > .env << 'EOF'
GEMINI_API_KEY=your_gemini_key_here
VOYAGE_API_KEY=your_voyage_key_here
VECTORA_NAMESPACE=my-project
VECTORA_TRUST_FOLDER=.
EOF
```

Substitua `your_gemini_key_here` e `your_voyage_key_here` pelas suas chaves.

### Opção B: Variáveis de Ambiente do Sistema

```bash
# macOS / Linux
export GEMINI_API_KEY="seu_gemini_api_key"
export VOYAGE_API_KEY="seu_voyage_api_key"

# Windows (PowerShell)
$env:GEMINI_API_KEY = "seu_gemini_api_key"
$env:VOYAGE_API_KEY = "seu_voyage_api_key"
```

### Opção C: Usar `vectora config` (Interactive)

```bash
vectora config set --key GEMINI_API_KEY
# Será solicitada a entrada interativa
# Depois:
vectora config set --key VOYAGE_API_KEY
```

---

## Passo 4: Verificar Configuração

```bash
vectora config list
# Deve mostrar:
# GEMINI_API_KEY: ••••••••••
# VOYAGE_API_KEY: ••••••••••
# VECTORA_NAMESPACE: my-project
```

---

## Passo 5: Inicializar um Projeto

```bash
# Crie um diretório para seu primeiro projeto
mkdir meu-projeto-vectora
cd meu-projeto-vectora

# Inicialize o Vectora
vectora init --name "Meu Projeto" --type codebase
```

Isso cria:

- `vectora.config.yaml` — Configuração do projeto
- `.vectora/` — Diretório interno (cache, índices locais)
- `AGENTS.md` — Arquivo de memória do agente

---

## Próximos Passos

### Para Usuários de Claude Desktop

Vá para [Claude Code Integration](../integrations/claude-code.md) e configure o MCP.

### Para Usuários de Cursor

Vá para [Cursor Integration](../integrations/cursor.md).

### Para Usuários de VS Code

Vá para [VS Code Extension](../integrations/vscode.md).

### Para Aprender a Configurar

Vá para [Configuration](./configuration.md).

---

## Troubleshooting

### Erro: `command not found: vectora`

**Causa**: Node.js não está no PATH.

**Solução**:

```bash
# Reinstale Node.js: https://nodejs.org
node --version # Deve funcionar primeiro
npm install -g @kaffyn/vectora # Reinstale
```

### Erro: `Error: API key not found`

**Causa**: Variáveis de ambiente não configuradas.

**Solução**: Verifique se `GEMINI_API_KEY` e `VOYAGE_API_KEY` estão definidas:

```bash
echo $GEMINI_API_KEY
echo $VOYAGE_API_KEY
```

### Erro: `403 Quota Exceeded` (Gemini)

**Causa**: Limite de requisições excedido (60/min no tier gratuito).

**Solução**: Aguarde ou faça upgrade para o [plano Pro](../plans/pro.md).

### Erro: `EACCES: permission denied`

**Causa**: Permissão insuficiente para instalar globalmente.

**Solução**:

```bash
# Opção 1: Use sudo (não recomendado)
sudo npm install -g @kaffyn/vectora

# Opção 2: Configure npm para instalação local (recomendado)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g @kaffyn/vectora
```

---

## FAQ

**P: Preciso de internet para usar Vectora?**
R: Sim, você precisa de conexão para APIs do Gemini e Voyage. Para modo local (experimental), você pode usar modelos locais via Ollama, mas isso requer configuração adicional.

**P: Minhas chaves de API são seguras?**
R: Sim. As chaves são armazenadas localmente em `~/.vectora/credentials.enc` (criptografadas) ou em seu `.env`. Kaffyn nunca acessa suas chaves.

**P: Posso usar múltiplos projetos com uma única instalação?**
R: Sim. Use `vectora init` para cada projeto em diretórios diferentes.

**P: Como atualizar Vectora?**
R: Use `npm update -g @kaffyn/vectora` ou instale uma versão específica: `npm install -g @kaffyn/vectora@latest`.

---

> **Próximo**: Você está configurado! Agora configure seu IDE em [Configuration](./configuration.md).

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
