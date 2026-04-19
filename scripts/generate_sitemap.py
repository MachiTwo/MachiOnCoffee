import os
import yaml
from datetime import datetime
from collections import defaultdict

BASE_URL = "https://cafegame.dev"
CONTENT_DIR = "content"
SITEMAP_PATH = "static/sitemap.xml"

# Default fallback date if none found (to avoid constant changes in sitemap)
DEFAULT_DATE = "2026-04-18T22:30:00-03:00"

def get_lastmod(front):
    if front.get('lastmod'):
        return str(front['lastmod'])
    if front.get('date'):
        return str(front['date'])
    return DEFAULT_DATE

def parse_md_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---')
        if len(parts) < 3:
            return None

        front = yaml.safe_load(parts[1])
        if not front:
            return None

        # SEO: Ignore drafts
        if front.get('draft') is True:
            return None

        # Determine language independently
        lang = 'pt'
        if file_path.endswith('.en.md'):
            lang = 'en'

        # Determine URL based on file path and slugs
        rel_path = os.path.relpath(file_path, CONTENT_DIR)
        rel_path = rel_path.replace('\\', '/')

        filename = os.path.basename(rel_path)
        parent_dir = os.path.dirname(rel_path)

        # Strip extension correctly for each language
        if filename.endswith('.en.md'):
            base_filename = filename[:-6]
        else:
            base_filename = filename[:-3]

        is_index = base_filename in ['index', '_index']

        path_parts = parent_dir.split('/') if parent_dir else []

        # SEO: Use slug if present, otherwise use filename
        # This is handled separately per file (.md vs .en.md)
        if not is_index:
            if front.get('slug'):
                path_parts.append(str(front['slug']))
            else:
                path_parts.append(base_filename)
        else:
            # For index files, the slug can override the section name
            if front.get('slug') and path_parts:
                path_parts[-1] = str(front['slug'])

        # filter out empty parts
        path_parts = [p for p in path_parts if p and p != '.']

        canonical_id = "/".join(path_parts)

        url_path = canonical_id
        if lang == 'en':
            url = f"{BASE_URL}/en/{url_path}/"
        else:
            url = f"{BASE_URL}/{url_path}/"

        # Root URL fixes
        if not url_path:
            if lang == 'en':
                url = f"{BASE_URL}/en/"
            else:
                url = f"{BASE_URL}/"

        # Normalize URL
        url = url.replace('//', '/').replace(':/', '://')
        if not url.endswith('/'):
            url += '/'

        # SEO: Priority and Changefreq from frontmatter or defaults
        priority = str(front.get('priority', '0.7' if is_index else '0.5'))
        changefreq = str(front.get('changefreq', 'weekly'))

        return {
            'canonical_id': canonical_id,
            'lang': lang,
            'loc': url,
            'lastmod': get_lastmod(front),
            'changefreq': changefreq,
            'priority': priority,
            'tags': front.get('tags', []), # Store tags for possible metadata inclusion
            'title': front.get('title', '')
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_sitemap():
    # Group results by canonical_id to handle hreflang
    grouped_pages = defaultdict(dict)

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                res = parse_md_file(file_path)
                if res:
                    grouped_pages[res['canonical_id']][res['lang']] = res

    # Flatten and sort for consistency
    all_urls = []
    for cid in grouped_pages:
        for lang in grouped_pages[cid]:
            page = grouped_pages[cid][lang]
            # Add alternates
            alternates = []
            for other_lang in grouped_pages[cid]:
                alternates.append({
                    'lang': 'en' if other_lang == 'en' else 'pt-br', # Adjust to site language codes
                    'href': grouped_pages[cid][other_lang]['loc']
                })
            page['alternates'] = alternates
            all_urls.append(page)

    all_urls.sort(key=lambda x: x['loc'])

    xml_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    for url in all_urls:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{url["loc"]}</loc>')
        xml_content.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_content.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_content.append(f'    <priority>{url["priority"]}</priority>')

        # Add hreflang alternates (Complete SEO)
        for alt in url['alternates']:
            xml_content.append(f'    <xhtml:link rel="alternate" hreflang="{alt["lang"]}" href="{alt["href"]}"/>')

        # Optional: Add custom tags as comments or specific tags if requested
        # Since standard XML sitemap doesn't support <tags>, we can keep them in comments for audit
        if url['tags']:
            tags_str = ", ".join(url['tags'])
            xml_content.append(f'    <!-- Tags: {tags_str} -->')

        xml_content.append('  </url>')

    xml_content.append('</urlset>')

    content = "\n".join(xml_content)

    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Sitemap generated at {SITEMAP_PATH} with {len(all_urls)} entries.")

if __name__ == "__main__":
    generate_sitemap()
