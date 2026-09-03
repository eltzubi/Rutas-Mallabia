#!/usr/bin/env python3
"""Resizes and recompresses img/*.jpg in place, and writes a .webp next to each.

Run after adding new photos to img/:

    python3 scripts/optimize_images.py

Photos come straight off a phone/camera at native resolution (often
3000-4000 px on the long side) and get displayed in a card a fraction of
that size -- nothing in the site ever needs more than MAX_SIDE pixels on
the long edge. Downscales in place (never upscales an already-smaller
photo), strips EXIF, and recompresses as progressive JPEG. Also writes a
sibling img/<name>.webp (used by <picture> in the *_tail.html templates)
at the same resolution.
"""
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(ROOT, "img")

MAX_SIDE = 1600
JPEG_QUALITY = 80
WEBP_QUALITY = 75


def process(path):
    name = os.path.basename(path)
    before = os.path.getsize(path)

    im = Image.open(path)
    # exif_transpose PRIMERO: convert("RGB") tira la etiqueta de orientacion pero
    # no gira los pixeles, asi que una foto hecha en vertical con el movil (EXIF
    # orientation 6) acababa tumbada en la web. Aqui se aplica de verdad y luego
    # ya se puede tirar la etiqueta.
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")  # drops any stray alpha
    w, h = im.size
    scale = MAX_SIDE / max(w, h)
    resized = scale < 1
    if resized:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)

    im.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    after = os.path.getsize(path)

    webp_path = os.path.splitext(path)[0] + ".webp"
    im.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=6)
    webp_size = os.path.getsize(webp_path)

    tag = "resized" if resized else "recompressed"
    print(
        f"{name}: {before/1024:7.1f} KB -> {after/1024:7.1f} KB jpg "
        f"({tag}{'' if not resized else f', {w}x{h} -> {im.size[0]}x{im.size[1]}'}), "
        f"{webp_size/1024:7.1f} KB webp"
    )
    return before, after, webp_size


def main():
    total_before = total_after = total_webp = 0
    names = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(".jpg"))
    for name in names:
        b, a, w = process(os.path.join(IMG_DIR, name))
        total_before += b
        total_after += a
        total_webp += w
    print(f"\n{len(names)} images")
    print(f"jpg total:  {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB")
    print(f"webp total: {total_webp/1024/1024:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
