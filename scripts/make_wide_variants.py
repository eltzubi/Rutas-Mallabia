#!/usr/bin/env python3
"""Crea la version de 800 px de cada foto, para que el movil no se baje la de 1600.

Una foto de galeria se ve a 130-165 px en un movil (260-495 px reales contando
la densidad de pantalla) y hasta ahora el navegador se descargaba la de 1600 px
igual: una ficha de ruta pesaba 2,6 MB en un telefono. Con las dos versiones
declaradas en el srcset, el navegador coge la que le vale y en el movil eso son
tres cuartas partes menos de bytes, sin que cambie nada en escritorio ni al
ampliar una foto (el visor abre siempre la grande, por data-lightbox-src).

A diferencia de optimize_images.py, este script NO toca los originales: solo
anade ficheros -800.webp que no existan. Es seguro volver a lanzarlo, y lanzarlo
despues de anadir fotos nuevas es justo lo que hay que hacer.

Uso:
    python3 scripts/make_wide_variants.py          # crea las que falten
    python3 scripts/make_wide_variants.py --force  # rehace tambien las que ya estan
"""
import os
import sys
import glob

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "img")

ANCHO = 800
CALIDAD = 75  # la misma que usa optimize_images.py para el webp de 1600

# Las miniaturas de las tarjetas de la portada ya salen a 1100 px de
# make_card_thumbs.py y se ven a 356 px como mucho, asi que no entran aqui.
EXCLUIR = ("-card", "-800")


def candidatas():
    for ruta in sorted(glob.glob(os.path.join(IMG, "*.jpg"))):
        nombre = os.path.basename(ruta)
        if any(x in nombre for x in EXCLUIR):
            continue
        yield ruta


def main():
    forzar = "--force" in sys.argv
    hechas = saltadas = 0
    bytes_originales = bytes_nuevos = 0

    for origen in candidatas():
        destino = origen[: -len(".jpg")] + "-800.webp"
        grande = origen[: -len(".jpg")] + ".webp"

        if os.path.exists(destino) and not forzar:
            saltadas += 1
            continue

        with Image.open(origen) as im:
            im = im.convert("RGB")
            w, h = im.size
            if max(w, h) <= ANCHO:
                # Ya es pequena: no tiene sentido una variante, el srcset se
                # queda con una sola fuente para esta foto.
                saltadas += 1
                continue
            escala = ANCHO / max(w, h)
            im = im.resize((round(w * escala), round(h * escala)), Image.LANCZOS)
            im.save(destino, "WEBP", quality=CALIDAD, method=6)

        if os.path.exists(grande):
            bytes_originales += os.path.getsize(grande)
        bytes_nuevos += os.path.getsize(destino)
        hechas += 1
        print(f"  {os.path.basename(destino)} ({os.path.getsize(destino)//1024} KB)")

    print(f"\n{hechas} creadas, {saltadas} sin tocar")
    if bytes_originales:
        print(f"peso de esas mismas fotos a 1600: {bytes_originales/1048576:.0f} MB")
        print(f"peso de las nuevas de 800:        {bytes_nuevos/1048576:.0f} MB "
              f"({100 - bytes_nuevos/bytes_originales*100:.0f}% menos)")


if __name__ == "__main__":
    main()
