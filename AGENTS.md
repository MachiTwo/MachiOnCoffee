# AGENTS.md - MachiOnCoffee Guidelines

This file provides guidance for AI agents working in this repository.

## Project Overview

**MachiOnCoffee** is the official documentation site for the **Ability System** and **Vectora** projects. It is built with **Hugo** using the **Hextra** theme.

## Essential Commands

```powershell
# API Data Generation (XML -> JSON)
python scripts/xml_to_json.py

# Validation
pre-commit run --all-files

# Local Build (Development)
python build_local.py
```

## Content Structure

- **Ability System**: `content/docs/ability-system/`
- **Vectora**: `content/docs/vectora/`
- **API Sources**: `api_sources/` (XML files from C++ source)
- **JSON Data**: `data/api/` (Output from `xml_to_json.py`)

## Architecture & Shortcodes

- **Theme**: Hextra v0.11.1
- **Multi-language**: Portuguese (canonical) and English (translations).
- **Required Shortcodes**:
  - `{{< lang-toggle >}}`: Must be at the top of EVERY documentation page.
  - `{{< section-toggle >}}`: ONLY on Home and main Docs index (`content/docs/_index.md`). Prohibited on internal documentation pages.
- **API Documentation**:
  - Uses `{{< godot-api class="ClassName" >}}` to pull data from `data/api/pt/ClassName.json`.

## Naming & Governance Conventions

- **Filenames**: Kebab-case and English-standardized names (e.g., `as-ability.md`).
- **Slugs**: Must match the filename (e.g., `slug: as-ability`).
- **Dates**: Standardized to `2026-04-18T22:30:00-03:00`.
- **Text Structure & Flow**:
  - **No Title Stacking**: NEVER place a header (H2, H3) immediately after another header or the page title (H1 from frontmatter). There must ALWAYS be a descriptive paragraph between them.
  - **Redundant "Visão Geral"**: Remove "## Visão Geral" or "## Overview" headers if they appear right after the shortcodes. Let the content flow dynamically from the top.
  - **Hierarchy**: Do not jump from H1 directly to H3. Follow a logical H1 -> Paragraph -> H2 -> Paragraph -> H3 flow.
- **Reference Headers**: Reference pages like `godot-api` should also follow the paragraph rule before listing methods or properties.
- **Governance**: The "Iron Law" is defined in `api_sources/BUSINESS_RULES.pt.md`. Never violate architectural boundaries.
- **Pre-commit**: Strict `markdownlint` and `prettier` rules. No decorative emojis in technical docs.

## SEO & Metadata

- **Frontmatter Tags**: Every documentation page MUST include a `tags` list in the frontmatter for SEO.

  ```yaml
  tags:
    - ai
    - context-engine
    - mcp
    - vectora
  ```

- **Sitemap**: Generated via `python scripts/generate_sitemap.py`. This is enforced by `pre-commit`.
- **Robots.txt**: Located at `static/robots.txt`.
- **Description**: Ensure `hugo.toml` has a concise site description.

## Implementation Workflow

1. Always write/update both PT and EN versions of a file (e.g., `index.md` and `index.en.md`).
2. Maintain alignment between JSON API data and Markdown pages (1:1 mapping for classes).
3. Derive slugs from filenames using the `fix_slugs.py` logic if needed.
