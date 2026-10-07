#!/usr/bin/env python3
"""Resizes and recompresses the master JPEGs in place (img/ and img/orig/),
and writes a .webp for each one in img/, que es lo que se publica.

Run after adding new photos to img/:

    python3 scripts/optimize_images.py

Photos come straight off a phone/camera at native resolution (often
3000-4000 px on the long side) and get displayed in a card a fraction of
that size -- nothing in the site ever needs more than MAX_SIDE pixels on
the long edge. Downscales in place (never upscales an already-smaller
photo), strips EXIF, and recompresses as progressive JPEG. Also writes a
sibling img/<name>.webp (used by <picture> in the *_tail.html templates)
at the same resolution.

Solo toca lo que hace falta. Recomprimir un JPEG que ya paso por aqui no lo
mejora: da bytes distintos cada vez (1.026 ficheros nuevos en git por pasada,
que es de donde salen los cientos de MB de historia) y ademas lo degrada un
poco mas cada vez, porque vuelve a cuantizar una imagen ya cuantizada. Por eso
se apunta en img/.optimized.json lo que se escribio, y en la siguiente pasada
se saltan las fotos que siguen igual. Con --force se reprocesa todo.

Tampoco entra en las salidas de los otros dos scripts (ver EXCLUIR).
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(ROOT, "img")
# Los originales de 1600 px que no se publican (ver _config.yml). Los 57 que
# siguen en img/ son los que cada ficha declara como og:image, y esos tienen
# que seguir siendo descargables para que la vista previa al compartir salga
# en condiciones.
ORIG_DIR = os.path.join(IMG_DIR, "orig")

MAX_SIDE = 1600
JPEG_QUALITY = 80
WEBP_QUALITY = 75
REGISTRO = os.path.join(IMG_DIR, ".optimized.json")
# Salidas de otros scripts, que tienen su propia calidad afinada. Sin esto,
# pasar por aqui detras de make_card_thumbs.py le sobrescribia el <name>-card.webp
# con uno de peor calidad y mas pesado (114 -> 118 KB en la miniatura medida).
# make_wide_variants.py excluye estos mismos sufijos por el mismo motivo.
EXCLUIR = ("-card", "-800")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def lee_registro():
    try:
        with open(REGISTRO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def ya_pasada(path, webp_path):
    """Sin registro, adopta lo que ya esta hecho en vez de rehacerlo.

    Las fotos del repositorio son justo la salida de este script, asi que la
    primera pasada no tiene que reescribir nada: le basta con reconocerlas.
    Una foto recien anadida no cumple esto (viene mas grande, o sin su webp) y
    se procesa normal.
    """
    if not os.path.exists(webp_path):
        return False
    with Image.open(path) as im:
        return max(im.size) <= MAX_SIDE


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
    forzar = "--force" in sys.argv
    registro = {} if forzar else lee_registro()
    total_before = total_after = total_webp = 0
    hechas = saltadas = 0
    originales = []
    for carpeta in (IMG_DIR, ORIG_DIR):
        if not os.path.isdir(carpeta):
            continue
        originales += [(f, os.path.join(carpeta, f)) for f in os.listdir(carpeta)
                       if f.lower().endswith(".jpg")
                       and not any(x in f for x in EXCLUIR)]
    for name, path in sorted(originales):
        # El .webp siempre en img/, se mire donde se mire el original: es el
        # que de verdad reciben los navegadores.
        webp_path = os.path.join(IMG_DIR, os.path.splitext(name)[0] + ".webp")
        apunte = registro.get(name)
        if not forzar:
            if apunte and os.path.exists(webp_path) \
                    and apunte.get("jpg") == sha(path) \
                    and apunte.get("webp") == sha(webp_path):
                saltadas += 1
                continue
            if apunte is None and ya_pasada(path, webp_path):
                registro[name] = {"jpg": sha(path), "webp": sha(webp_path)}
                saltadas += 1
                continue
        b, a, w = process(path)
        registro[name] = {"jpg": sha(path), "webp": sha(webp_path)}
        hechas += 1
        total_before += b
        total_after += a
        total_webp += w
    with open(REGISTRO, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(registro.items())), f, indent=0, sort_keys=True)
        f.write("\n")
    print(f"\n{len(names)} imagenes: {hechas} procesadas, {saltadas} ya estaban")
    if hechas:
        print(f"jpg total:  {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB")
        print(f"webp total: {total_webp/1024/1024:.2f} MB")


if __name__ == "__main__":
    sys.exit(main())
