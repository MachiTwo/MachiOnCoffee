import os
import re
import sys

# Ensure stdout can handle UTF-8 if possible, or fallback to ignoring errors
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# A comprehensive list of literal emojis to remove, plus a broad range for others.
# Using literal characters as the user requested.
EMOJI_LIST = "🎯🔍🧩📦🛡️💰🔄🧭💡📂🟢🔵🟣⚫🚀🧠🔑✅❌🛡️💎🔥✨⚡⭐🌟☁️🌈🌊🌋🌲🌳🌴🌵🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏆🏈🏊🏐🏏🏒🏓🏔️🏕️🏖️🏜️🏝️🏞️🏟️🏠🏡🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏮🏯🏰"

# Pattern to match literal emojis and the common symbol ranges
# This includes the specific ones the user pointed out: 🔑 🚀 🧠 🎯 🔍
EMOJI_PATTERN = re.compile(
    r'[' + EMOJI_LIST + r'\U00010000-\U0010ffff\u2600-\u27bf\u2b50\u2b55\u231a\u231b\u23e9-\u23f3\u23f8-\u23fa]',
    flags=re.UNICODE
)

def clean_text(text):
    """
    Remove emojis and clean up resulting whitespace.
    """
    # Remove emojis
    text = EMOJI_PATTERN.sub('', text)

    # Process line by line to handle double spaces and preserve indentation
    lines = []
    for line in text.splitlines():
        # Preserve indentation
        match = re.match(r'^(\s*)', line)
        indent = match.group(1) if match else ""
        content = line[len(indent):]
        # Remove multiple spaces inside content (e.g., "Word1  Word2" -> "Word1 Word2")
        content = re.sub(r' +', ' ', content).strip()
        lines.append(indent + content)

    return '\n'.join(lines)

def run():
    # Target directory is 'content'
    target_dir = 'content'
    if not os.path.exists(target_dir):
        # Allow running from scripts/ folder
        target_dir = os.path.join('..', 'content')

    if not os.path.exists(target_dir):
        print("Erro: Diretorio 'content' nao encontrado.")
        return

    print(f"Iniciando limpeza de emojis em: {os.path.abspath(target_dir)}")

    count = 0
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        original = f.read()

                    cleaned = clean_text(original)

                    if original != cleaned:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(cleaned)
                        # Avoid printing the path if it contains emojis (unlikely for filenames but safe)
                        # and use ASCII-safe status
                        print(f"MODIFICADO: {file}")
                        count += 1
                except Exception as e:
                    print(f"ERRO ao processar {file}: {str(e)}")

    print(f"\nSucesso! {count} arquivos foram limpos.")

if __name__ == "__main__":
    run()
