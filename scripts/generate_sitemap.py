import os
import yaml
from datetime import datetime

BASE_URL = "https://cafegame.dev"
CONTENT_DIR = "content"
SITEMAP_PATH = "static/sitemap.xml"

def get_lastmod(front):
    if front.get('lastmod'):
        return str(front['lastmod'])
    if front.get('date'):
        return str(front['date'])
    return datetime.now().isoformat()

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

        url_path = "/".join(path_parts)
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
        priority = front.get('priority', '0.7' if is_index else '0.5')
        changefreq = front.get('changefreq', 'weekly')

        return {
            'loc': url,
            'lastmod': get_lastmod(front),
            'changefreq': changefreq,
            'priority': priority
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_sitemap():
    urls = []
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                res = parse_md_file(file_path)
                if res:
                    urls.append(res)

    # Sort for consistency
    urls.sort(key=lambda x: x['loc'])

    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{url["loc"]}</loc>')
        xml_content.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_content.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_content.append(f'    <priority>{url["priority"]}</priority>')
        xml_content.append('  </url>')

    xml_content.append('</urlset>')

    content = "\n".join(xml_content)

    # Save to static folder so Hugo copies it to public
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Sitemap generated at {SITEMAP_PATH} with {len(urls)} entries.")

if __name__ == "__main__":
    generate_sitemap()
