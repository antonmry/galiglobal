#!/usr/bin/env python3
"""
# /// script
# dependencies = ["pillow"]
# ///

Optimize images in-place for web use:
  - Resize down to a max dimension (default 2560px) while preserving aspect ratio.
  - Re-encode with sensible compression per format.
  - PNGs are converted to WebP by default to shrink large assets.
  - Prints savings per file.

Run from repo root:
  uv run scripts/optimize_images.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MAX_DIM = 2560  # px
CONVERT_PNG_TO_WEBP = False


@dataclass
class OptimizeResult:
    path: Path
    before: int
    after: int
    resized: bool
    status: str
    note: str = ""


def find_images(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.suffix.lower() in EXTENSIONS and p.is_file()]


def optimize_image(path: Path) -> OptimizeResult:
    before_size = path.stat().st_size
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            resized = False
            if max(img.size) > MAX_DIM:
                img.thumbnail((MAX_DIM, MAX_DIM))
                resized = True

            fmt = (img.format or path.suffix.replace(".", "").upper()).upper()
            target_path = path

            # Convert PNGs to WebP when enabled
            if fmt == "PNG" and CONVERT_PNG_TO_WEBP:
                target_path = path.with_suffix(".webp")
                fmt = "WEBP"
                # remove the original later if conversion succeeds
                remove_original = True
            else:
                remove_original = False

            save_kwargs = build_save_kwargs(fmt)
            img.save(target_path, **save_kwargs)

            if remove_original and target_path != path:
                path.unlink()
                path = target_path
    except Exception as e:
        return OptimizeResult(path, before_size, before_size, False, "error", str(e))

    after_size = path.stat().st_size
    status = "ok"
    note = ""
    if after_size > before_size:
        status = "warn"
        note = "grew after re-encode"
    return OptimizeResult(path, before_size, after_size, resized, status, note)


def build_save_kwargs(fmt: str) -> dict:
    fmt_upper = fmt.upper()
    if fmt_upper in {"JPG", "JPEG"}:
        return {"format": "JPEG", "quality": 85, "optimize": True, "progressive": True}
    if fmt_upper == "PNG":
        return {"format": "PNG", "optimize": True, "compress_level": 9}
    if fmt_upper == "WEBP":
        return {"format": "WEBP", "quality": 80, "method": 6}
    if fmt_upper == "GIF":
        return {"format": "GIF", "optimize": True, "save_all": True}
    # Fallback to original format
    return {"format": fmt_upper, "optimize": True}


def human_mb(num_bytes: int) -> str:
    return f"{num_bytes/1024/1024:.2f}MB"


def main() -> int:
    images = find_images(ROOT)
    if not images:
        print("No images found.")
        return 0

    results: List[OptimizeResult] = []
    for img in images:
        res = optimize_image(img)
        results.append(res)
        delta = res.before - res.after
        action = "resized" if res.resized else "re-encoded"
        if res.status == "error":
            print(f"[ERROR] {img}: {res.note}")
        else:
            print(
                f"[{res.status.upper():4}] {img} ({action}) "
                f"{human_mb(res.before)} -> {human_mb(res.after)} "
                f"({'saved ' + human_mb(delta) if delta >=0 else 'grew ' + human_mb(-delta)}) {res.note}"
            )

    errors = sum(1 for r in results if r.status == "error")
    warns = sum(1 for r in results if r.status == "warn")
    print(f"\nProcessed {len(results)} images (errors={errors}, warnings={warns}).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
