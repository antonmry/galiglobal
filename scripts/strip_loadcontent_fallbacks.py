#!/usr/bin/env python3
"""
Remove embedded navbar/footer fallback code from generated HTML files.

The fallback injected raw HTML into JS template literals, which could break
scripts when the HTML contained closing tags. This script rewrites the
loadContent function to a minimal version (fetch + inject + execute
data-execute scripts) across all .html files.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent

LOAD_CONTENT_RE = re.compile(
    r"async function loadContent\(url, elementId\) \{.*?\n\s*\}\n\n\s*document.addEventListener\('DOMContentLoaded'",
    re.DOTALL,
)

NEW_LOAD_CONTENT = """async function loadContent(url, elementId) {
        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          const html = await response.text();
          const target = document.getElementById(elementId);
          if (!target) return;
          target.innerHTML = html;

          const scripts = target.querySelectorAll('script[data-execute="true"]');
          scripts.forEach((oldScript) => {
            const newScript = document.createElement('script');
            [...oldScript.attributes].forEach((attr) => newScript.setAttribute(attr.name, attr.value));
            newScript.textContent = oldScript.textContent;
            target.appendChild(newScript);
          });
        } catch (error) {
          console.error(`Error loading ${url}:`, error);
        }
      }

      document.addEventListener('DOMContentLoaded'"""


def rewrite_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, count = LOAD_CONTENT_RE.subn(NEW_LOAD_CONTENT, text, count=1)
    if count:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    html_files = sorted(ROOT.rglob("*.html"))
    changed = 0
    for html in html_files:
        if rewrite_file(html):
            changed += 1
            print(f"Updated loadContent in {html}")
    print(f"Done. Updated {changed} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
