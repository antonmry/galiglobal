This is the source for my [blog](https://www.galiglobal.com/).

## Formatting and HTML generation

- Format all markdown files with rumdl:
  - `uv run scripts/format_markdown.py`
- Regenerate all HTML files from their markdown counterparts:
  - `uv run --with markdown scripts/generate_html_from_md.py`
- Scaffold a new blog post (creates md, updates leaflet map and blog list):
  - `uv run scripts/create_post.py`
- Optimize images in-place (resize + recompress):
  - `uv run --with pillow scripts/optimize_images.py`

CI: `.github/workflows/deploy.yml` runs both steps on every push (and can be
dispatched manually). It commits and pushes changes when formatting alters
files.
