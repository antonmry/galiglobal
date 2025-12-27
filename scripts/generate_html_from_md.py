#!/usr/bin/env python3
# /// script
# dependencies = ["markdown"]
# ///
"""
Generate HTML files from Markdown, preserving existing HTML filenames.

- For every *.md file, writes/overwrites the sibling *.html file.
- Renders markdown with sensible extensions (fenced code, tables, etc).
- Keeps the navbar/footer loading pattern and optionally preserves the
  Leaflet comments container if the existing HTML had one.

Run with: uv run scripts/generate_html_from_md.py
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

import markdown

ROOT = Path(__file__).resolve().parent.parent
NAVBAR_HTML = (ROOT / "navbar.html").read_text(encoding="utf-8") if (ROOT / "navbar.html").exists() else ""
FOOTER_HTML = (ROOT / "footer.html").read_text(encoding="utf-8") if (ROOT / "footer.html").exists() else ""


def extract_title(md_text: str) -> str:
    """Grab the first ATX or Setext heading as the page title."""
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ").strip()
        if line.endswith("=" * len(line.strip())) and len(line.strip()) > 0:
            return line.strip("= ").strip()
    return "GaliGlobal"


def render_markdown(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "sane_lists",
            "toc",
        ],
        output_format="html5",
    )


def had_leaflet_comments(existing_html: Path) -> bool:
    if not existing_html.exists():
        return False
    try:
        return "leaflet-comments" in existing_html.read_text(encoding="utf-8")
    except Exception:
        return False


def build_html(title: str, body_content: str, include_comments: bool) -> str:
    comments_block = '<div id="leaflet-comments" class="mt-4"></div>' if include_comments else ""
    # Escape for JS template literal
    navbar_js = sanitize_for_js_literal(NAVBAR_HTML)
    footer_js = sanitize_for_js_literal(FOOTER_HTML)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="antonmry">
    <meta name="keywords" content="">
    <meta name="generator" content="generated-from-markdown">

    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="/css/asciidoctor.css" rel="stylesheet">
    <link href="/css/base.css" rel="stylesheet">
    <link href="/css/prettify.css" rel="stylesheet">
  </head>
  <body>
    <div id="wrap">
      <div id="navbar-container"></div>
      <div class="container">
        <div id="content">
{body_content}
        </div>
        {comments_block}
      </div>
      <div id="push"></div>
    </div>

    <div id="footer-container"></div>

    <script src="/js/jquery-1.11.1.min.js"></script>
    <script src="/js/bootstrap.min.js" defer></script>
    <script src="/js/prettify.js" defer></script>

    <script>
      async function loadContent(url, elementId) {{
        try {{
          const response = await fetch(url);
          if (!response.ok) throw new Error(`HTTP error! status: ${{response.status}}`);
          const html = await response.text();
          const target = document.getElementById(elementId);
          if (!target) return;
          target.innerHTML = html;

          const scripts = target.querySelectorAll('script[data-execute="true"]');
          scripts.forEach((oldScript) => {{
            const newScript = document.createElement('script');
            [...oldScript.attributes].forEach((attr) => newScript.setAttribute(attr.name, attr.value));
            newScript.textContent = oldScript.textContent;
            target.appendChild(newScript);
          }});
        }} catch (error) {{
          console.error(`Error loading ${{url}}:`, error);
        }}
      }}

      document.addEventListener('DOMContentLoaded', async () => {{
        await loadContent('/navbar.html', 'navbar-container');
        await loadContent('/footer.html', 'footer-container');

        if (typeof prettyPrint === 'function') {{
          prettyPrint();
        }}
      }});
    </script>
  </body>
    </html>
"""


def load_leaflet_map() -> dict[str, str]:
    map_path = ROOT / "leaflet-comments-map.json"
    if not map_path.exists():
        return {}
    try:
        return json.loads(map_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def has_leaflet_map_entry(html_file: Path, leaflet_map: dict[str, str]) -> bool:
    try:
        relpath = html_file.relative_to(ROOT).as_posix()
    except ValueError:
        return False
    return relpath in leaflet_map or f"/{relpath}" in leaflet_map


def process_markdown(md_file: Path, leaflet_map: dict[str, str]) -> None:
    html_file = md_file.with_suffix(".html")
    md_text = md_file.read_text(encoding="utf-8")
    title = extract_title(md_text)
    html_body = render_markdown(md_text)
    comments_flag = had_leaflet_comments(html_file) or has_leaflet_map_entry(html_file, leaflet_map)

    html_output = build_html(title=title, body_content=indent_html(html_body, 8), include_comments=comments_flag)
    html_file.write_text(html_output, encoding="utf-8")
    print(f"Rendered {md_file} -> {html_file}")


def indent_html(html: str, spaces: int) -> str:
    indent = " " * spaces
    # Ensure each line is indented for readable output
    return "\n".join(f"{indent}{line}" if line.strip() else "" for line in html.splitlines())


def sanitize_for_js_literal(html: str) -> str:
    """Escape content so it can live safely inside a JS template literal."""
    return (
        html.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("</script", "<\\/script")
    )


def main() -> int:
    md_files = sorted(ROOT.rglob("*.md"))
    if not md_files:
        print("No markdown files found.")
        return 0

    leaflet_map = load_leaflet_map()
    for md in md_files:
        process_markdown(md, leaflet_map)

    return 0


if __name__ == "__main__":
    sys.exit(main())
