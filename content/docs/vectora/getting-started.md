---
title: "Como Começar"
weight: 1
type: docs
---

## 🚀 Iniciando com o Vectora

O Vectora foi desenhado para ser plug-and-play mas extremamente customizável.

### Instalação

O runtime do Vectora foi desenvolvido em **TypeScript (Node.js 20+)**, utilizando a **AI SDK da Vercel**.

```bash
npx @kaffyn/vectora init
```

### Configuração Core

- **Context Engine**: Realiza raciocínio multi-hop e análise estrutural via **AST (Tree-sitter)**.
- **Vector DB**: Integração nativa com **Qdrant Cloud** para busca vetorial escalável.
- **Provider Router**: Suporte estável e agnóstico de provedores (OpenRouter, Google, Anthropic, OpenAI).

## 🧪 Validação: Vectora Harness

Como saber se a IA realmente melhorou? Use o **Vectora Harness**:

1. **Medir a Precisão**: Compara output da IA com `vectora:on` vs `vectora:off`.
2. **Eficiência de Tokens**: Otimiza a recuperação para evitar o "overfetch".
3. **Auditabilidade**: Relatórios estruturados sobre o uso das ferramentas.
