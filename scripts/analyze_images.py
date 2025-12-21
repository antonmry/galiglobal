#!/usr/bin/env python3
"""
Analyze image assets for web suitability (size and dimensions).

Reports:
  - file size thresholds (warn > 1.5MB, fail > 3MB)
  - max dimension thresholds (warn > 2560px, fail > 4000px)

Run from repo root:
  uv run --with pillow scripts/analyze_images.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

WARN_SIZE = 1.5 * 1024 * 1024  # 1.5MB
FAIL_SIZE = 3 * 1024 * 1024    # 3MB
WARN_DIM = 2560
FAIL_DIM = 4000


@dataclass
class ImageReport:
    path: Path
    size_bytes: int
    dimensions: Tuple[int, int]
    status: str
    notes: List[str]


def classify(img_path: Path) -> ImageReport:
    size_bytes = img_path.stat().st_size
    width = height = 0
    notes: List[str] = []
    status = "ok"

    try:
        with Image.open(img_path) as img:
            width, height = img.size
    except Exception as e:
        return ImageReport(img_path, size_bytes, (0, 0), "error", [f"cannot open: {e}"])

    max_dim = max(width, height)

    if size_bytes > FAIL_SIZE or max_dim > FAIL_DIM:
        status = "fail"
    elif size_bytes > WARN_SIZE or max_dim > WARN_DIM:
        status = "warn"

    if size_bytes > WARN_SIZE:
        notes.append(f"large file: {size_bytes/1024/1024:.2f}MB")
    if max_dim > WARN_DIM:
        notes.append(f"large dimension: {width}x{height}px")

    return ImageReport(img_path, size_bytes, (width, height), status, notes)


def find_images(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.suffix.lower() in EXTENSIONS and p.is_file()]


def main() -> int:
    images = find_images(ROOT)
    if not images:
        print("No images found.")
        return 0

    reports = [classify(p) for p in images]
    totals = {"ok": 0, "warn": 0, "fail": 0, "error": 0}
    for r in reports:
        totals[r.status] = totals.get(r.status, 0) + 1

    for r in reports:
        if r.status in {"warn", "fail", "error"}:
            dim_str = f"{r.dimensions[0]}x{r.dimensions[1]}" if r.dimensions != (0, 0) else "unknown"
            notes = "; ".join(r.notes) if r.notes else ""
            print(f"[{r.status.upper():5}] {r.path} ({dim_str}, {r.size_bytes/1024/1024:.2f}MB) {notes}")

    total = len(reports)
    print(f"\nImages checked: {total} (ok={totals['ok']}, warn={totals['warn']}, fail={totals['fail']}, error={totals['error']})")

    return 1 if totals["fail"] or totals["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
