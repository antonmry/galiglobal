#!/usr/bin/env python3
"""
Create a new blog post scaffold.

- Prompts for title and date (default: today).
- Creates the markdown file under blog/YYYY/YYYYMMDD-slug.md.
- Adds an empty Leaflet entry for the new HTML path in leaflet-comments-map.json.
- Adds a link under the correct year in blog-posts.md.

Run (from repo root):
  uv run scripts/create_post.py

No changes are applied until you run the script.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
LEAFLET_MAP = ROOT / "leaflet-comments-map.json"
BLOG_POSTS_MD = ROOT / "blog-posts.md"


@dataclass
class PostInfo:
    title: str
    post_date: date

    @property
    def slug(self) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", self.title.lower())
        slug = re.sub(r"-+", "-", slug).strip("-")
        return slug or "post"

    @property
    def yyyymmdd(self) -> str:
        return self.post_date.strftime("%Y%m%d")

    @property
    def year(self) -> str:
        return str(self.post_date.year)

    @property
    def md_path(self) -> Path:
        return BLOG_DIR / self.year / f"{self.yyyymmdd}-{self.slug}.md"

    @property
    def html_relpath(self) -> str:
        return f"blog/{self.year}/{self.yyyymmdd}-{self.slug}.html"


def prompt(text: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{text}{suffix}: ").strip()
    return val or (default or "")


def ensure_dirs(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_markdown(post: PostInfo) -> None:
    content = f"""# {post.title}

_{post.post_date.strftime('%d %B %Y')}_

---

Write your content here.
"""
    post.md_path.write_text(content, encoding="utf-8")
    print(f"Created {post.md_path}")


def update_leaflet_map(post: PostInfo) -> None:
    data: Dict[str, str] = {}
    if LEAFLET_MAP.exists():
        data = json.loads(LEAFLET_MAP.read_text(encoding="utf-8"))
    data[post.html_relpath] = ""
    LEAFLET_MAP.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated {LEAFLET_MAP} with entry for {post.html_relpath}")


def update_blog_posts(post: PostInfo) -> None:
    if not BLOG_POSTS_MD.exists():
        print(f"{BLOG_POSTS_MD} not found; skipping blog-posts list update.")
        return

    lines: List[str] = BLOG_POSTS_MD.read_text(encoding="utf-8").splitlines()
    year_heading = f"## {post.year}"
    link_line = f"- [{post.title}]({post.html_relpath})"

    if year_heading in lines:
        idx = lines.index(year_heading) + 1
        lines.insert(idx, link_line)
    else:
        # Insert new year section after main title
        insert_at = 1 if lines and lines[0].startswith("#") else 0
        lines[insert_at:insert_at] = ["", year_heading, "", link_line]

    BLOG_POSTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {BLOG_POSTS_MD} with link for {post.title}")


def main() -> int:
    title = prompt("Post title")
    if not title:
        print("Title is required.")
        return 1

    date_str = prompt("Post date (YYYY-MM-DD)", default=date.today().isoformat())
    try:
        year, month, day = map(int, date_str.split("-"))
        post_date = date(year, month, day)
    except Exception:
        print("Invalid date format. Use YYYY-MM-DD.")
        return 1

    post = PostInfo(title=title, post_date=post_date)
    ensure_dirs(post.md_path)
    if post.md_path.exists():
        print(f"File already exists: {post.md_path}")
        return 1

    write_markdown(post)
    update_leaflet_map(post)
    update_blog_posts(post)
    print("Done. Regenerate HTML to include the new post.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
