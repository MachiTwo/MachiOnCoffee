# Plano de Implementação: Sincronização de Documentação (`make_markdown.py`)

Este plano descreve a criação de um script Python para converter arquivos de referência de classe RST (gerados do Godot) em Markdown e atualizar os arquivos existentes no site sem perder explicações teóricas manuais.

## Review do Usuário Necessário

> [!IMPORTANT] > **Marcadores de Sincronização**: O script usará `<!-- AUTO-GENERATED-API-START -->` e `<!-- AUTO-GENERATED-API-END -->`.
>
> - O conteúdo entre eles será substituído pela API atualizada.
> - O conteúdo fora (teoria, exemplos práticos manuais) será preservado.

> [!IMPORTANT] > **Padrão de Frontmatter**: Arquivos novos ou atualizados sem frontmatter seguirão rigorosamente:
>
> ```markdown
> ---
> title: <Title>
> type: docs
> sidebar:
>   open: false
> breadcrumbs: false
> ---
>
> {{< lang-toggle >}}
>
> {{< section-toggle >}}
> ```

## Mudanças Propostas

### Scripts

#### [ATUALIZAR] [make_markdown.py](file:///c:/Users/bruno/Desktop/MachiOnCoffee/scripts/make_markdown.py)

Reescrever o script com a seguinte lógica:

- **Input**: Pasta `temp/ability_system/classes/`.
- **Mapeamento**: Localizar recursivamente o arquivo `.md` correspondente em `content/docs/ability-system/`.
- **Dualidade de Idioma**: Para cada classe `X`, atualizar `X.en.md` (Inglês) e `X.md` (Português). Inicialmente, o conteúdo da API no `.md` será uma cópia do Inglês.
- **Parsing RST**:
  - Extrair Propriedades, Métodos, Sinais e Enums.
  - Converter tabelas RST para Markdown GFM.
  - Converter links `:ref:` para links Markdown internos.
- **Merge Inteligente**: Injetar a API formatada nos marcadores específicos.

### Documentação (Exemplo de Validação)

#### [MODIFICAR] [asability.md](file:///c:/Users/bruno/Desktop/MachiOnCoffee/content/docs/ability-system/resources/asability)

Adicionar os marcadores para testar a primeira execução do script.

## Perguntas Abertas

1. **Mapeamento de Novos Arquivos**: Se o script encontrar uma classe (ex: `ASStateSnapshot`) que ainda não tem um `.md`, ele deve criar o arquivo seguindo a hierarquia (ex: `refcounted/asstatesnapshot.md`) ou apenas ignorar?
2. **Título**: O `<Title>` no frontmatter deve ser apenas o nome da classe (ex: `ASAbility`) ou algo mais descritivo?

## Plano de Verificação

### Testes Automatizados

- Executar `python scripts/make_markdown.py`.
- Verificar se `asability.md` foi atualizado corretamente entre os marcadores.
- Confirmar se o frontmatter foi mantido/criado conforme a exigência.

### Verificação Manual

- Validar se as tabelas de métodos e propriedades estão legíveis no navegador (via `npm run dev`).
