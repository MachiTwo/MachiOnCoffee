import os
import yaml
import sys
from datetime import datetime
from collections import defaultdict

# Configurações de Diretórios
CONTENT_DIR = 'content'
OFF_TOPIC_DIR = os.path.join(CONTENT_DIR, 'off-topic')

# Configurações de Arquivos
INDEX_FILE = os.path.join(CONTENT_DIR, '_index.md')
INDEX_FILE_EN = os.path.join(CONTENT_DIR, '_index.en.md')
OFF_TOPIC_FILE = os.path.join(OFF_TOPIC_DIR, '_index.md')
OFF_TOPIC_FILE_EN = os.path.join(OFF_TOPIC_DIR, '_index.en.md')

MONTHNAMES_PT = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
MONTHNAMES_EN = ["", "January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]

def escape_markdown(text):
    return str(text).replace('[', '\\[').replace(']', '\\]')

def parse_post(path, lang='pt'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.startswith('---'):
            return None

        parts = content.split('---')
        if len(parts) < 3:
            return None

        front = yaml.safe_load(parts[1])
        if not (front and front.get('title') and front.get('date')):
            return None

        # Parse data (handle Z for UTC or ISO strings)
        date_str = str(front['date']).replace('Z', '+00:00')
        date_obj = datetime.fromisoformat(date_str)

        # URL Generation
        base_path = os.path.dirname(path)
        dir_url = base_path.replace(CONTENT_DIR, '').replace('\\', '/').strip('/')

        # Override slug se existir no frontmatter
        if front.get('slug'):
            parts_url = dir_url.split('/')
            parts_url[-1] = str(front['slug'])
            dir_url = '/'.join(parts_url)

        url = f"/{dir_url}/"
        if lang == 'en':
            url = f"/en{url}"

        tags = [str(t) for t in front.get('tags', [])]

        return {
            'title': front['title'],
            'url': url,
            'date': date_obj,
            'tags': tags,
            'lang': lang,
            'path': path
        }
    except Exception as e:
        print(f"Erro processando {path}: {e}")
        return None

def group_by_month(posts):
    posts.sort(key=lambda p: p['date'], reverse=True)
    grouped = defaultdict(list)
    for p in posts:
        grouped[(p['date'].year, p['date'].month)].append(p)
    return grouped

def render_months(grouped, lang='pt'):
    lines = []
    sorted_months = sorted(grouped.keys(), reverse=True)
    month_names = MONTHNAMES_PT if lang == 'pt' else MONTHNAMES_EN

    for year, month in sorted_months:
        lines.append(f"## {year} - {month_names[month]}\n")
        for post in grouped[(year, month)]:
            lines.append(f"- **{post['date'].day:02d}** - [{escape_markdown(post['title'])}]({post['url']})")
        lines.append("")
    return "\n".join(lines)

def write_if_changed(target, content):
    content = content.rstrip() + "\n"
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8') as f:
            if f.read() == content:
                return False

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    return True

def main():
    include_future = '--future' in sys.argv
    now = datetime.now().astimezone() if datetime.now().tzinfo else datetime.now()

    all_posts_pt = []
    all_posts_en = []

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file == 'index.md':
                p = parse_post(os.path.join(root, file), lang='pt')
                if p: all_posts_pt.append(p)
            elif file == 'index.en.md':
                p = parse_post(os.path.join(root, file), lang='en')
                if p: all_posts_en.append(p)

    # Filtros por data (ignora futuros se não houver flag)
    if not include_future:
        all_posts_pt = [p for p in all_posts_pt if p['date'].timestamp() <= now.timestamp()]
        all_posts_en = [p for p in all_posts_en if p['date'].timestamp() <= now.timestamp()]

    # Separação por categorias (Tags)
    def is_off_topic(p): return 'off-topic' in p['tags']

    # Posts regulares (filtramos os off-topic e páginas especiais)
    regular_posts_pt = [p for p in all_posts_pt if not is_off_topic(p)]
    regular_posts_en = [p for p in all_posts_en if not is_off_topic(p)]

    off_topic_pt = [p for p in all_posts_pt if is_off_topic(p)]
    off_topic_en = [p for p in all_posts_en if is_off_topic(p)]

    # 1. Index Principal (PT) - Todos os posts agora ficam aqui
    idx_content = "---\ntitle: MachiOnCoffee\n---\n\n"
    idx_content += render_months(group_by_month(regular_posts_pt), lang='pt')
    if write_if_changed(INDEX_FILE, idx_content):
        print(f"Generated {INDEX_FILE} with {len(regular_posts_pt)} posts.")

    # 2. Off-Topic (PT)
    ot_content = "---\ntitle: Off-Topic\n---\n\n"
    ot_content += "Assuntos fora da programação do dia a dia: café, filosofia e carreira.\n\n"
    ot_content += render_months(group_by_month(off_topic_pt), lang='pt')
    if write_if_changed(OFF_TOPIC_FILE, ot_content):
        print(f"Generated {OFF_TOPIC_FILE} with {len(off_topic_pt)} posts.")

    # 3. Suporte a Inglês (EN) se houver postagens
    if all_posts_en:
        # Index EN
        idx_en_content = "---\ntitle: MachiOnCoffee\n---\n\n"
        idx_en_content += render_months(group_by_month(regular_posts_en), lang='en')
        write_if_changed(INDEX_FILE_EN, idx_en_content)

        # Off-Topic EN
        ot_en_content = "---\ntitle: Off-Topic (EN)\n---\n\n"
        ot_en_content += render_months(group_by_month(off_topic_en), lang='en')
        write_if_changed(OFF_TOPIC_FILE_EN, ot_en_content)

if __name__ == "__main__":
    main()
