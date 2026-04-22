import os
import re
import sys

# Mapeamento de regex para tags do Hugo
TAG_KNOWLEDGE_BASE = {
    # Core Tech
    r"\bMCP\b|\bModel Context Protocol\b": "mcp",
    r"\bRAG\b": "rag",
    r"\bHNSW\b|\bVector Search\b": "vector-search",
    r"\bMongoDB\b|\bAtlas\b": "mongodb-atlas",
    r"\bGemini\b": "gemini",
    r"\bVoyage\b": "voyage",
    # Vectora Architecture
    r"\bContext Engine\b": "context-engine",
    r"\bHarness\b": "harness-runtime",
    r"\bReranker\b": "reranker",
    r"\bSub-Agents?\b": "sub-agents",
    r"\bGuardian\b": "guardian",
    r"\bRBAC\b": "rbac",
    r"\bTrust Folder\b": "trust-folder",
    r"\bEmbeddings?\b": "embeddings",
    r"\bAST\b": "ast-parsing",
    # Auth & Security
    r"\bSSO\b|\bOIDC\b": "sso",
    r"\bJWT\b|\bTokens?\b": "auth",
    r"\bSecurity\b|\bSegurança\b": "security",
    r"\bBYOK\b": "byok",
    r"\bPrivacy\b|\bPrivacidade\b": "privacy",
    r"\bGovernance\b|\bGovernança\b": "governance",
    # Integrations
    r"\bChatGPT\b": "chatgpt",
    r"\bOpenAI\b": "openai",
    r"\bPlugins?\b": "plugins",
    r"\bIntegration\b|\bIntegrações\b": "integration",
    # General Concepts
    r"\bPersistence\b|\bPersistência\b": "persistence",
    r"\bState\b|\bEstado\b": "state",
    r"\bArchitecture\b|\bArquitetura\b": "architecture",
    r"\bConcepts?\b|\bConceitos?\b": "concepts",
    r"\bReference\b|\bReferência\b": "reference",
    r"\bSystem\b|\bSistema\b": "system",
    r"\bConfiguração\b|\bConfiguration\b|\bConfig\b": "config",
    r"\bYAML\b": "yaml",
    r"\bErrors?\b|\bErros?\b": "errors",
    r"\bTroubleshooting\b": "troubleshooting",
    r"\bTools?\b|\bFerramentas?\b": "tools",
    r"\bProtocol\b|\bProtocolo\b": "protocol",
}


def generate_tags_from_content(content):
    tags = {"ai", "vectora"}  # Default base tags
    for pattern, tag in TAG_KNOWLEDGE_BASE.items():
        if re.search(pattern, content, re.IGNORECASE):
            tags.add(tag)
    return sorted(list(tags))


def create_frontmatter(filename, content):
    # Extract title from first H1 if exists
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = (
        title_match.group(1).strip()
        if title_match
        else filename.replace(".en.md", "").replace(".md", "").capitalize()
    )

    slug = os.path.basename(filename).replace(".en.md", "").replace(".md", "")
    if slug == "_index":
        slug = os.path.basename(os.path.dirname(filename))
        if slug == "docs":
            slug = "vectora"

    tags = generate_tags_from_content(content)
    tags_yaml = "\n".join([f"  - {t}" for t in tags])

    date_str = "2026-04-18T22:30:00-03:00"  # Static baseline or dynamic

    frontmatter = f"""---
title: {title}
slug: {slug}
date: "{date_str}"
type: docs
sidebar:
  open: true
tags:
{tags_yaml}
---
"""
    return frontmatter


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    body_content = content

    # Check if frontmatter exists
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)

    if frontmatter_match:
        frontmatter_block = frontmatter_match.group(1)
        body_content = content[frontmatter_match.end() :]

        # Extract existing tags
        existing_tags = set()
        tags_match = re.search(r"\ntags:\n((?:  - .*\n?)*)", frontmatter_block)
        if tags_match:
            for line in tags_match.group(1).split("\n"):
                line = line.strip()
                if line.startswith("- "):
                    existing_tags.add(line[2:].strip())

        # Update tags in existing frontmatter
        new_tags = set(generate_tags_from_content(body_content))
        merged_tags = sorted(list(existing_tags.union(new_tags)))
        tags_yaml = "\n".join([f"  - {t}" for t in merged_tags])

        # Replace existing tags block or append if missing
        if "\ntags:" in frontmatter_block:
            # Regex to replace tags array
            new_frontmatter = re.sub(
                r"\ntags:\n(?:  - .*\n?)*", f"\ntags:\n{tags_yaml}\n", frontmatter_block
            )
        else:
            new_frontmatter = frontmatter_block + f"\ntags:\n{tags_yaml}\n"

        content = f"---\n{new_frontmatter}\n---\n{body_content}"
    else:
        # No frontmatter, create one
        frontmatter = create_frontmatter(filepath, content)
        content = frontmatter + "\n" + content

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False


def main():
    modified_any = False
    files_to_check = sys.argv[1:]

    if not files_to_check:
        for root, dirs, files in os.walk("docs"):
            for file in files:
                if file.endswith(".md"):
                    files_to_check.append(os.path.join(root, file))

    for filepath in files_to_check:
        if filepath.endswith(".md"):
            if process_file(filepath):
                print(f"Updated Frontmatter in: {filepath}")
                modified_any = True

    if modified_any:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
