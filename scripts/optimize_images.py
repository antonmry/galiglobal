#!/usr/bin/env python3
"""
# /// script
# dependencies = ["pillow"]
# ///

Optimize images in-place for web use:
  - If a path argument is given, optimize that image only to be <= TARGET_SIZE (default 500KB).
  - Otherwise optimize all repo images larger than TARGET_SIZE.
  - Resize down to a max dimension (default 1920px) while preserving aspect ratio.
  - Convert large PNGs without transparency to JPEG for better compression.
  - Use iterative quality reduction to hit target size.

Run from repo root:
  uv run scripts/optimize_images.py [path/to/image]
"""

from __future__ import annotations

import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MAX_DIM = 1920  # px - reduced for web
TARGET_SIZE = 500 * 1024  # 500 KB
MIN_QUALITY = 60  # Don't go below this quality


@dataclass
class OptimizeResult:
    path: Path
    before: int
    after: int
    resized: bool
    converted: bool
    status: str
    note: str = ""


def find_images(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.suffix.lower() in EXTENSIONS and p.is_file()]


def has_transparency(img: Image.Image) -> bool:
    """Check if image has actual transparency (not just an alpha channel)."""
    if img.mode == "RGBA":
        extrema = img.split()[3].getextrema()
        return extrema[0] < 255  # Has pixels with alpha < 255
    if img.mode == "P":
        return "transparency" in img.info
    return False


def quantize_png(img: Image.Image) -> Image.Image:
    """Reduce PNG colors using quantization for smaller file size."""
    if img.mode == "RGBA":
        # Quantize with transparency support
        return img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGBA")
    elif img.mode == "RGB":
        return img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    return img


def save_with_target_size(img: Image.Image, path: Path, fmt: str, target: int) -> Tuple[int, int]:
    """Save image, iteratively reducing quality if needed to hit target size."""
    quality = 85

    while quality >= MIN_QUALITY:
        buffer = io.BytesIO()
        save_kwargs = build_save_kwargs(fmt, quality)
        img.save(buffer, **save_kwargs)
        size = buffer.tell()

        if size <= target or fmt in {"PNG", "GIF"}:
            # Write to file
            with open(path, "wb") as f:
                f.write(buffer.getvalue())
            return size, quality

        quality -= 5

    # Still over target, save with min quality
    buffer = io.BytesIO()
    save_kwargs = build_save_kwargs(fmt, MIN_QUALITY)
    img.save(buffer, **save_kwargs)
    with open(path, "wb") as f:
        f.write(buffer.getvalue())
    return buffer.tell(), MIN_QUALITY


def optimize_image(path: Path) -> OptimizeResult:
    before_size = path.stat().st_size
    converted = False
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            original_format = (img.format or path.suffix.replace(".", "").upper()).upper()

            # Load image data before closing
            img = img.copy()

            resized = False
            if max(img.size) > MAX_DIM:
                img.thumbnail((MAX_DIM, MAX_DIM), Image.Resampling.LANCZOS)
                resized = True

            fmt = original_format
            output_path = path

            # Convert large PNGs without transparency to JPEG
            if original_format == "PNG" and before_size > TARGET_SIZE:
                if not has_transparency(img):
                    fmt = "JPEG"
                    output_path = path.with_suffix(".jpg")
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    converted = True
                else:
                    # Try quantizing PNG with transparency
                    img = quantize_png(img)

            # Ensure correct mode for JPEG
            if fmt == "JPEG" and img.mode != "RGB":
                img = img.convert("RGB")

            after_size, final_quality = save_with_target_size(img, output_path, fmt, TARGET_SIZE)

            # Remove old file if converted to different format
            if converted and output_path != path and output_path.exists():
                path.unlink()
                path = output_path

    except Exception as e:
        return OptimizeResult(path, before_size, before_size, False, False, "error", str(e))

    status = "ok"
    note = ""
    if after_size > TARGET_SIZE:
        status = "warn"
        note = f"still over {human_kb(TARGET_SIZE)}"
    if converted:
        note = f"converted to JPEG{', ' + note if note else ''}"
    return OptimizeResult(path, before_size, after_size, resized, converted, status, note)


def build_save_kwargs(fmt: str, quality: int = 85) -> dict:
    fmt_upper = fmt.upper()
    if fmt_upper in {"JPG", "JPEG"}:
        return {"format": "JPEG", "quality": quality, "optimize": True, "progressive": True}
    if fmt_upper == "PNG":
        return {"format": "PNG", "optimize": True, "compress_level": 9}
    if fmt_upper == "WEBP":
        return {"format": "WEBP", "quality": quality, "method": 6}
    if fmt_upper == "GIF":
        return {"format": "GIF", "optimize": True, "save_all": True}
    # Fallback to original format
    return {"format": fmt_upper, "optimize": True}


def human_kb(num_bytes: int) -> str:
    return f"{num_bytes/1024:.0f}KB"


def main() -> int:
    args = sys.argv[1:]
    if args:
        targets = [Path(args[0]).resolve()]
    else:
        targets = [p for p in find_images(ROOT) if p.stat().st_size > TARGET_SIZE]

    if not targets:
        print("No images to optimize.")
        return 0

    results: List[OptimizeResult] = []
    for img_path in targets:
        if not img_path.exists():
            print(f"[SKIP] {img_path} (not found)")
            continue
        res = optimize_image(img_path)
        results.append(res)
        delta = res.before - res.after
        actions = []
        if res.resized:
            actions.append("resized")
        if res.converted:
            actions.append("converted")
        actions.append("re-encoded")
        action = "/".join(actions)

        if res.status == "error":
            print(f"[ERROR] {img_path}: {res.note}")
        else:
            savings = f"saved {human_kb(delta)}" if delta >= 0 else f"grew {human_kb(-delta)}"
            print(
                f"[{res.status.upper():4}] {res.path} ({action}) "
                f"{human_kb(res.before)} -> {human_kb(res.after)} ({savings})"
                f"{' ' + res.note if res.note else ''}"
            )

    errors = sum(1 for r in results if r.status == "error")
    converted = sum(1 for r in results if r.converted)
    print(f"\nProcessed {len(results)} images (errors={errors}, converted={converted}).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
