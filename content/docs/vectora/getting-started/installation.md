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
Vectora é distribuído como um binário nativo de alta performance para Windows, macOS e Linux. No Windows, a instalação é padronizada via **Winget** e reside em seu diretório de programas local, sem necessidade de Node.js ou privilégios de administrador.

> [!IMPORTANT] > **BYOK (Bring Your Own Key)**: No plano Free, o Vectora exige chaves de API do Gemini e Voyage. Nos planos **Pro** e **Team (Plus)**, você pode optar pelo modo **Managed**, onde os créditos de IA já estão inclusos.

---

## Pré-requisitos

## Sistema Operacional

- **macOS** 12.0+
- **Linux** (Ubuntu 20.04+, Fedora 35+, Debian 11+)
- **Windows 11** (WSL2 recomendado)

## Software

- **Sistemas 64-bit** (x64 ou ARM64)
- **Conexão com Internet** para ativação de chaves

## Verificar Versão do Winget (Windows)

```powershell
winget --version # Deve retornar v1.4 ou superior
```

---

## Passo 1: Instalar Vectora

## Windows (Recomendado)

Abra o terminal (PowerShell ou CMD) e execute:

```powershell
winget install kaffyn.vectora
```

O binário será instalado em `%LOCALAPPDATA%\Programs\Vectora` e adicionado automaticamente ao seu PATH.

## macOS / Linux

Use nosso script de instalação rápida:

```bash
curl -sSf https://vectora.sh/install.sh | sh
```

## Download Manual

Você também pode baixar o binário diretamente da nossa [página de Releases no GitHub](https://github.com/kaffyn/vectora/releases).

---

## Passo 2: Obter Chaves de API Gratuitas

## Gemini API (Google)

1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Clique em **"Create API Key"**
3. Copie a chave gerada

**Limite gratuito**: 60 requisições por minuto, 1.5M tokens/mês

## Voyage API (VoyageAI)

1. Acesse [Voyage AI Dashboard](https://dash.voyageai.com/api-keys)
2. Clique em **"Create API Key"**
3. Copie a chave gerada

**Limite gratuito**: 50 requisições por minuto, 100M tokens/mês

---

## Passo 3: Configurar via Systray

Após a instalação, procure pelo ícone do Vectora na sua bandeja do sistema (perto do relógio).

1. Clique no ícone e selecione **"Login"**.
2. Isso abrirá seu navegador para autenticação SSO.
3. Once authenticated, o Vectora configurará suas chaves automaticamente.

---

## Passo 4: Verificar Configuração (CLI)

Se preferir o terminal, verifique o status:

```bash
vectora auth status
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

## Para Usuários de Claude Desktop

Vá para [Claude Code Integration](../integrations/claude-code.md) e configure o MCP.

## Para Usuários de Cursor

Vá para [Cursor Integration](../integrations/cursor.md).

## Para Usuários de VS Code

Vá para [VS Code Extension](../integrations/vscode.md).

## Para Aprender a Configurar

Vá para [Configuration](./configuration.md).

---

## Troubleshooting

### Erro: `command not found: vectora`

**Causa**: O binário não está no PATH.

**Solução**: Verifique se a instalação foi concluída e reinicie seu terminal.

### Erro: `Error: API key not found`

**Causa**: Variáveis de ambiente não configuradas ou falha no login.

**Solução**: Verifique o status com `vectora auth status`.

### Erro: `403 Quota Exceeded` (Gemini)

**Causa**: Limite de requisições excedido (60/min no tier gratuito).

**Solução**: Aguarde ou faça upgrade para o [plano Pro](../plans/pro.md).

### Erro: `EACCES: permission denied`

npm install -g @kaffyn/vectora

```text

---

## FAQ

**P: Preciso de internet para usar Vectora?**
R: Sim, você precisa de conexão para APIs do Gemini e Voyage. Para modo local (experimental), você pode usar modelos locais via Ollama, mas isso requer configuração adicional.

**P: Minhas chaves de API são seguras?**
R: Sim. As chaves são armazenadas localmente em `~/.vectora/credentials.enc` (criptografadas) ou em seu `.env`. Kaffyn nunca acessa suas chaves.

**P: Posso usar múltiplos projetos com uma única instalação?**
R: Sim. Use `vectora init` para cada projeto em diretórios diferentes.

**P: Como atualizar o Vectora?**
R: No Windows, use `winget upgrade kaffyn.vectora`. Em outros sistemas, rode o script de instalação novamente ou use `vectora update`.

---

> **Próximo**: Você está configurado! Agora configure seu IDE em [Configuration](./configuration.md).

---

_Parte do ecossistema Vectora_ · Open Source (MIT)
```
