#!/usr/bin/env python3
"""Crea las versiones de 800 px de cada foto: la .webp y el .jpg de respaldo.

Una foto de galeria se ve a 130-165 px en un movil (260-495 px reales contando
la densidad de pantalla) y hasta ahora el navegador se descargaba la de 1600 px
igual: una ficha de ruta pesaba 2,6 MB en un telefono. Con las dos versiones
declaradas en el srcset, el navegador coge la que le vale y en el movil eso son
tres cuartas partes menos de bytes, sin que cambie nada en escritorio ni al
ampliar una foto (el visor abre siempre la grande, por data-lightbox-src, que ahora
apunta al .webp de 1600).

Tambien escribe el -800.jpg, que es lo unico que ve un navegador sin WebP: el
original de 1600 px vive en img/orig/, que no se publica (ver _config.yml). Eso
quito 211 MB del sitio publicado -- los JPEG de 1600 que no se bajaba nadie,
porque las fotos se sirven en WebP y hasta el visor pide el WebP primero.

A diferencia de optimize_images.py, este script NO toca los originales: solo
anade ficheros -800.webp y -800.jpg que no existan. Es seguro volver a lanzarlo,
y lanzarlo despues de anadir fotos nuevas es justo lo que hay que hacer.

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
# Los originales de 1600 px viven aparte y fuera del sitio publicado.
ORIG = os.path.join(IMG, "orig")

ANCHO = 800
CALIDAD = 75       # la misma que usa optimize_images.py para el webp de 1600
CALIDAD_JPG = 80   # el respaldo: lo ve menos del 1% de las visitas

# Las miniaturas de las tarjetas de la portada ya salen a 1100 px de
# make_card_thumbs.py y se ven a 356 px como mucho, asi que no entran aqui.
EXCLUIR = ("-card", "-800")


def candidatas():
    # Los originales estan repartidos: los 57 de og:image siguen publicados en
    # img/ y el resto en img/orig/ (ver _config.yml).
    rutas = glob.glob(os.path.join(IMG, "*.jpg")) + glob.glob(os.path.join(ORIG, "*.jpg"))
    for ruta in sorted(rutas, key=os.path.basename):
        nombre = os.path.basename(ruta)
        if any(x in nombre for x in EXCLUIR):
            continue
        yield ruta


def main():
    forzar = "--force" in sys.argv
    hechas = saltadas = 0
    rotas = []
    bytes_originales = bytes_nuevos = 0

    for origen in candidatas():
        base = os.path.join(IMG, os.path.basename(origen)[: -len(".jpg")])
        destino = base + "-800.webp"
        respaldo = base + "-800.jpg"

        if os.path.exists(destino) and os.path.exists(respaldo) and not forzar:
            saltadas += 1
            continue

        try:
            with Image.open(origen) as im:
                im = im.convert("RGB")
                w, h = im.size
                grande_de_verdad = max(w, h) > ANCHO
                if grande_de_verdad:
                    escala = ANCHO / max(w, h)
                    im = im.resize((round(w * escala), round(h * escala)), Image.LANCZOS)
                # Una foto que ya nace pequena no necesita variante en el
                # srcset -- la del tamano completo ya es esta -- pero si
                # necesita su respaldo .jpg, que es lo unico que puede ver un
                # navegador sin WebP ahora que el original no se publica.
                if grande_de_verdad:
                    im.save(destino, "WEBP", quality=CALIDAD, method=6)
                im.save(respaldo, "JPEG", quality=CALIDAD_JPG,
                        optimize=True, progressive=True)
        except OSError as e:
            # Un fichero truncado o corrupto no puede parar a los otros
            # quinientos: se avisa y se sigue.
            print(f"  !! {os.path.basename(origen)}: ilegible ({e})")
            rotas.append(os.path.basename(origen))
            continue

        bytes_originales += os.path.getsize(origen)
        bytes_nuevos += os.path.getsize(respaldo)
        if os.path.exists(destino):
            bytes_nuevos += os.path.getsize(destino)
        hechas += 1
        print(f"  {os.path.basename(respaldo)} ({os.path.getsize(respaldo)//1024} KB)")

    print(f"\n{hechas} creadas, {saltadas} sin tocar")
    if rotas:
        print(f"{len(rotas)} ilegibles: {', '.join(rotas)}")
    if bytes_originales:
        print(f"originales de esas fotos: {bytes_originales/1048576:.0f} MB")
        print(f"lo publicado a 800:       {bytes_nuevos/1048576:.0f} MB "
              f"({100 - bytes_nuevos/bytes_originales*100:.0f}% menos)")


if __name__ == "__main__":
    main()
