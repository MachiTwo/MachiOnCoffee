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
- **Required Shortcodes (in every doc page)**:
  - `{{< lang-toggle >}}`: Must be at the top.
  - `{{< section-toggle >}}`: Must follow the lang-toggle.
- **API Documentation**:
  - Uses `{{< godot-api class="ClassName" >}}` to pull data from `data/api/pt/ClassName.json`.

## Naming & Governance Conventions

- **Filenames**: Kebab-case and English-standardized names (e.g., `as-ability.md`).
- **Slugs**: Must match the filename (e.g., `slug: as-ability`).
- **Dates**: Standardized to `2026-04-18T22:30:00-03:00`.
- **Governance**: The "Iron Law" is defined in `api_sources/BUSINESS_RULES.pt.md`. Never violate architectural boundaries.
- **Pre-commit**: Strict `markdownlint` and `prettier` rules. No decorative emojis in technical docs.

## Implementation Workflow

1. Always write/update both PT and EN versions of a file (e.g., `index.md` and `index.en.md`).
2. Maintain alignment between JSON API data and Markdown pages (1:1 mapping for classes).
3. Derive slugs from filenames using the `fix_slugs.py` logic if needed.
