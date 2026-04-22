import os
import re
import sys


def get_footer(is_english):
    if is_english:
        return "\n\n---\n\n_Part of the Vectora ecosystem_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contributors](https://github.com/Kaffyn/Vectora/graphs/contributors)\n"
    else:
        return "\n\n---\n\n_Parte do ecossistema Vectora_ · [Open Source (MIT)](https://github.com/Kaffyn/Vectora) · [Contribuidores](https://github.com/Kaffyn/Vectora/graphs/contributors)\n"


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine language based on filename extension
    is_english = filepath.endswith(".en.md")

    expected_footer = get_footer(is_english).strip()

    # regex to match existing footers to remove them and standardize
    # Matches `---` followed by `Part of`, `Parte do`, etc. at the end of the file
    footer_regex = (
        r"\n*---\n+(?:_?Part of.*?|_?Parte do.*?(?:ecossistema)?.*?)(?:\n|\Z)*$"
    )

    # Strip any existing matching footer
    new_content = re.sub(footer_regex, "", content, flags=re.DOTALL).rstrip()

    # Append the new standard footer
    new_content = new_content + "\n\n" + expected_footer + "\n"

    # Only write if it actually changed to avoid prettier loops
    if content != new_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
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
                print(f"Standardized Footer in: {filepath}")
                modified_any = True

    if modified_any:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
