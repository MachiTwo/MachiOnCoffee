import os
import re
import sys

# Ensure stdout can handle UTF-8 if possible, or fallback to ignoring errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# A comprehensive list of literal emojis to remove, plus a broad range for others.
# Using literal characters as the user requested.
EMOJI_LIST = "🎯🔍🧩📦🛡️💰🔄🧭💡📂🟢🔵🟣⚫🚀🧠🔑✅❌🛡️💎🔥✨⚡⭐🌟☁️🌈🌊🌋🌲🌳🌴🌵🌾🌿🍀🍁🍂🍃🍄🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷🍸🍹🍺🍻🍼🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻🎼🎽🎾🎿🏀🏁🏂🏃🏄🏆🏈🏊🏐🏏🏒🏓🏔️🏕️🏖️🏜️🏝️🏞️🏟️🏠🏡🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏮🏯🏰"

# Pattern to match literal emojis and the common symbol ranges
# This includes the specific ones the user pointed out: 🔑 🚀 🧠 🎯 🔍
EMOJI_PATTERN = re.compile(
    r"["
    + EMOJI_LIST
    + r"\U00010000-\U0010ffff\u2600-\u27bf\u2b50\u2b55\u231a\u231b\u23e9-\u23f3\u23f8-\u23fa]",
    flags=re.UNICODE,
)


def clean_text(text):
    """
    Remove emojis and clean up resulting whitespace only if emojis were found.
    """
    if not EMOJI_PATTERN.search(text):
        return text

    # Remove emojis
    text = EMOJI_PATTERN.sub("", text)

    # Process line by line to handle double spaces and preserve indentation
    # but only for lines that were potentially changed or have odd spacing.
    # Actually, to be safe and consistent with previous behavior but less destructive:
    lines = []
    original_lines = text.splitlines(keepends=True)

    for line in original_lines:
        # Preserve indentation
        match = re.match(r"^(\s*)", line)
        indent = match.group(1) if match else ""

        # Get the content without indentation AND without the trailing newline
        content_with_newline = line[len(indent) :]
        newline_match = re.search(r"[\r\n]+$", content_with_newline)
        newline = newline_match.group(0) if newline_match else ""
        content = content_with_newline[: len(content_with_newline) - len(newline)]

        # Remove multiple spaces inside content (e.g., "Word1  Word2" -> "Word1 Word2")
        # and strip trailing spaces (not the newline itself)
        content = re.sub(r" +", " ", content).rstrip()

        lines.append(indent + content + newline)

    return "".join(lines)


def run():
    # If arguments are provided (e.g. from pre-commit), use them.
    # Otherwise, fallback to 'content' directory.
    if len(sys.argv) > 1:
        md_files = []
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                for root, _, files in os.walk(arg):
                    for file in files:
                        if file.endswith(".md"):
                            md_files.append(os.path.join(root, file))
            elif os.path.isfile(arg) and arg.endswith(".md"):
                md_files.append(arg)

        if not md_files:
            return

        target_dir = (
            os.path.commonpath([os.path.abspath(f) for f in md_files])
            if len(md_files) > 1
            else os.path.dirname(os.path.abspath(md_files[0]))
        )
        print(f"Limpando emojis em {len(md_files)} arquivos...")
    else:
        target_dir = "content"
        if not os.path.exists(target_dir):
            # Allow running from scripts/ folder
            target_dir = os.path.join("..", "content")

        if not os.path.exists(target_dir):
            print("Erro: Diretorio 'content' nao encontrado.")
            return

        print(f"Iniciando limpeza de emojis em: {os.path.abspath(target_dir)}")

        md_files = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

    count = 0
    for path in sorted(md_files):
        try:
            # Use 'newline=""' to preserve original line endings
            with open(path, "r", encoding="utf-8", newline="") as f:
                original = f.read()

            cleaned = clean_text(original)

            if original != cleaned:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(cleaned)

                # Print relative path for clarity
                try:
                    rel_path = os.path.relpath(path, os.getcwd())
                except Exception:
                    rel_path = os.path.basename(path)
                print(f"MODIFICADO: {rel_path}")
                count += 1
        except Exception as e:
            print(f"ERRO ao processar {path}: {str(e)}")

    if count > 0 or len(sys.argv) == 1:
        print(f"\nSucesso! {count} arquivos foram limpos.")


if __name__ == "__main__":
    run()
