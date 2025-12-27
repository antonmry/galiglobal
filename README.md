This is the source for my [blog](https://www.galiglobal.com/).
 
## Formatting and HTML generation

- Format all markdown files with rumdl:
  - `uv run scripts/format_markdown.py`
- Regenerate all HTML files from their markdown counterparts:
  - `uv run scripts/generate_html_from_md.py`
- Scaffold a new blog post (creates md, updates leaflet map and blog list):
  - `uv run scripts/create_post.py`
- Optimize images in-place (resize + recompress):
  - `uv run scripts/optimize_images.py`

## Publish with GitHub Pages

- Manually trigger the Pages workflow:
  - `gh workflow run publish-pages.yml`
- Check recent runs for that workflow:
  - `gh run list --workflow="publish-pages.yml"`

CI: `.github/workflows/deploy.yml` runs all steps on every push (and can be
dispatched manually). It commits and pushes changes when formatting alters
files.

