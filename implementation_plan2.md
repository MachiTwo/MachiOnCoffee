# Plano de Implementação: Documentação Data-Driven (XML → JSON → Hugo)

Este plano descreve a transição para um sistema de documentação automatizado onde o **XML do Godot** é a fonte única de verdade (SSOT). O conteúdo técnico será renderizado dinamicamente via Shortcodes, preservando a limpeza dos arquivos Markdown.

## Review do Usuário Necessário

> [!IMPORTANT] > **Abordagem Data-Driven**:
>
> - Não haverá atualização direta de texto nos arquivos `.md`.
> - O script Python converterá os XMLs para **arquivos JSON** na pasta `data/api/`.
> - Os Markdowns usarão o shortcode `{{< godot-api class="NomeDaClasse" >}}`.

> [!IMPORTANT] > **Padrão de Frontmatter**: Todos os Markdowns de referência de classe seguirão o padrão:
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
>
> <!-- Teoria/Prática Manual -->
>
> {{< godot-api class="<ClassName>" >}}
> ```

## Mudanças Propostas

### Scripts

#### [NOVO] [xml_to_json.py](file:///c:/Users/bruno/Desktop/MachiOnCoffee/scripts/xml_to_json.py)

Script Python para processar a SSOT:

- **Input**: `temp/ability_system/doc_classes/*.xml`.
- **Output**: `data/api/en/*.json` e `data/api/pt/*.json` (cópias iniciais).
- **Dados**: Extrair de forma estruturada: `brief_description`, `description`, `properties`, `methods`, `signals`, `constants`.

### Hugo Layouts

#### [NOVO] [godot-api.html](file:///c:/Users/bruno/Desktop/MachiOnCoffee/layouts/_shortcodes/godot-api.html)

Shortcode para renderizar a API:

- **Lógica**: Detectar idioma da página (.Lang) e buscar o JSON correspondente em `.Site.Data.api`.
- **Template**: Renderizar tabelas GFM-style para Propriedades e Métodos, e seções detalhadas para descrições.

### Documentação

#### [MODIFICAR] [asability.md](file:///c:/Users/bruno/Desktop/MachiOnCoffee/content/docs/ability-system/resources/asability)

Remover tabelas manuais e substituir pelo shortcode.

## Plano de Verificação

### Testes Automatizados

- Executar `python scripts/xml_to_json.py`.
- Verificar se os arquivos JSON foram gerados corretamente em `data/api/`.

### Verificação Manual

- Validar se o shortcode renderiza corretamente no Hugo (`npm run dev`).
- Confirmar se a alternância de idioma (lang-toggle) funciona e aponta para os dados corretos.
