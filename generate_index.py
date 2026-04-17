import os
import yaml
from datetime import datetime
from collections import defaultdict

def escape_markdown(text):
    return str(text).replace('[', '\\[').replace(']', '\\]')

entries = []

for root, _, files in os.walk('content'):
    for file in files:
        if file != 'index.md':
            continue

        path = os.path.join(root, file)

        # Ignorar o index principal e o _index.md
        if path.replace('\\', '/') in ['content/index.md', 'content/_index.md']:
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if not lines or lines[0].strip() != '---':
                continue

            fm_lines = []
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                fm_lines.append(lines[i])
                i += 1

            if i < len(lines) and lines[i].strip() == '---':
                front = yaml.safe_load(''.join(fm_lines))
                if front and front.get('title') and front.get('date'):
                    try:
                        # Hugo usa formato RFC 3339, usando fromisoformat do python
                        # Algumas vezes pode ter Z ao inves de +00:00
                        date_str = str(front['date']).replace('Z', '+00:00')
                        date_obj = datetime.fromisoformat(date_str)

                        url = path.replace('\\', '/').replace('content/', '').replace('/index.md', '/')
                        entries.append({
                            'title': front['title'],
                            'url': url,
                            'date': date_obj
                        })
                    except ValueError:
                        pass
        except Exception as err:
            print(f"Erro processando {path}: {err}")

# Ordenar mais recentes primeiro
entries.sort(key=lambda e: e['date'], reverse=True)

# Agrupar por ano e mes
grouped = defaultdict(list)
for e in entries:
    grouped[(e['date'].year, e['date'].month)].append(e)

# Meses em pt-br para ficar mais legal (ou ingles como no original)
MONTHNAMES = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

sorted_keys = sorted(grouped.keys(), reverse=True)

new_content = "---\ntitle: MachiOnCoffee\n---\n\n"

for year, month in sorted_keys:
    month_name = MONTHNAMES[month]
    new_content += f"## {year} - {month_name}\n\n"

    for post in grouped[(year, month)]:
        new_content += f"- [{escape_markdown(post['title'])}]({post['url']})\n"

    new_content += "\n"

# Remove todos os \n sobrando do fim e garante que o arquivo acabe só com 1 \n
# Isso previne que o end-of-file-fixer do pre-commit fique brigando com o nosso script o tempo todo!
new_content = new_content.rstrip() + "\n"

target_file = 'content/_index.md'
write_file = True

if os.path.exists(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    if existing_content == new_content:
        write_file = False

if write_file:
    with open(target_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    print("Generated content/_index.md with posts grouped by year & month.")
else:
    print("content/_index.md is already up to date.")
