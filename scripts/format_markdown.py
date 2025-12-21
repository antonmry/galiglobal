#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys


def format_markdown_file(path: Path) -> int:
    """Run rumdl fmt on a single markdown file."""
    result = subprocess.run(
        ["uv", "tool", "run", "--from", "rumdl", "rumdl", "fmt", str(path)],
        check=False,
    )
    if result.returncode != 0:
        print(f"Warning: rumdl reported issues after formatting {path} (exit {result.returncode})")
    return result.returncode


def main() -> int:
    files = sorted(Path(".").rglob("*.md"))
    if not files:
        print("No markdown files found.")
        return 0

    exit_code = 0
    for file_path in files:
        print(f"Formatting {file_path}")
        rc = format_markdown_file(file_path)
        if rc != 0:
            exit_code = rc

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
