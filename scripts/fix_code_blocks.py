#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def fix_code_blocks(file_path):
    """
    Add 'text' language specifier only to odd-numbered ``` (opening blocks).
    Ignores even-numbered ``` (closing blocks).
    """
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    # Find all ``` positions
    backtick_pattern = re.compile(r"^```", re.MULTILINE)
    matches = list(backtick_pattern.finditer(content))

    if not matches:
        return False

    # Process from end to start to avoid offset issues
    modified = False
    new_content = content
    for idx in range(len(matches) - 1, -1, -1):
        match = matches[idx]
        position = match.start()

        # Check if this is an odd-numbered match (1st, 3rd, 5th = indices 0, 2, 4)
        if idx % 2 == 0:  # Opening block (0-indexed: 0, 2, 4 = 1st, 3rd, 5th)
            # Check what comes after the ```
            end_pos = position + 3
            if end_pos < len(content) and content[end_pos] not in [
                "\n",
                "\r",
                " ",
                "\t",
            ]:
                # Already has a language specifier, skip
                continue

            # Replace ``` with ```text
            new_content = (
                new_content[:position] + "```text" + new_content[position + 3 :]
            )
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        print(f"  [OK] {file_path}: Fixed code blocks")
        return True
    else:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_code_blocks.py <file1> <file2> ... or <directory>")
        sys.exit(1)

    modified_count = 0
    targets = sys.argv[1:]

    for target_str in targets:
        target = Path(target_str)
        if target.is_file():
            if fix_code_blocks(target):
                modified_count += 1
        elif target.is_dir():
            md_files = list(target.rglob("*.md"))
            for md_file in sorted(md_files):
                if fix_code_blocks(md_file):
                    modified_count += 1
        else:
            print(f"Error: {target} is not a file or directory")

    if len(targets) > 1 or Path(targets[0]).is_dir():
        print(f"\n[OK] Fixed {modified_count} files")


if __name__ == "__main__":
    main()
