#!/usr/bin/env python3
"""Escribe una version pequena de cada foto de tarjeta de la portada.

    python3 scripts/make_card_thumbs.py

Las fotos de img/ estan a 1600 px de lado (scripts/optimize_images.py), que es
lo que necesita la foto grande de una ficha o el visor a pantalla completa. La
tarjeta de la portada, en cambio, mide unos 342 px en un movil y unos 350 en
una pantalla grande: servirle la de 1600 px son medio mega por tarjeta, y hay
28 tarjetas.

Este script escribe, junto a cada foto de tarjeta, un img/<nombre>-card.jpg y un
img/<nombre>-card.webp de CARD_WIDTH px de ancho, que es lo que consume el
<picture> de src/mallabia_tail.html. Nunca amplia una foto que ya sea menor, y
no toca ningun otro fichero de img/ (a diferencia de optimize_images.py, que
reescribe el directorio entero).

CARD_WIDTH sale de medir el hueco: 340 px en un movil de 390, pero 517 px en
una ventana de 1440. A 1100 px la foto cubre el doble de ese hueco, que es lo
que necesita una pantalla Retina grande; con 800 se quedaba corta justo ahi.

Ademas iguala el tono de las 28, que es lo que hace que el listado se lea como
una serie y no como 28 fotos sueltas: estan hechas a lo largo de anos, con movil
y con dron, y su luminancia mediana iba de 20 a 202 sobre 255.

Hay que volver a pasarlo cuando entre una ruta nueva a la portada.
"""
import os
import re
import sys

from PIL import Image, ImageEnhance, ImageOps, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(ROOT, "img")
HOME_TAIL = os.path.join(ROOT, "src", "mallabia_tail.html")

CARD_WIDTH = 1100         # 2x del hueco mas grande de la tarjeta (517 px a 1440)
CARD_RATIO = 16 / 10      # el mismo aspect-ratio que .route-card-photo
JPEG_QUALITY = 78
WEBP_QUALITY = 68         # bajado desde 72: al nivelar el tono aflora algo de
                          # ruido en las fotos oscuras y eso engorda el fichero;
                          # a 350 px de tarjeta la diferencia no se ve
SUFFIX = "-card"

# --- igualado de tono ---------------------------------------------------
# El contraste y la saturacion los hacia antes el navegador, con un
# filter:contrast(1.1) saturate(1.25) sobre .route-card-photo img. Ahora van
# grabados aqui para que la foto ya salga bien del fichero y para poder
# ajustarla foto a foto, que un filtro de CSS no puede.
CONTRASTE = 1.10
SATURACION = 1.25

# Y esto es lo nuevo: acercar la luminancia de cada foto a la del conjunto.
# OBJETIVO es la mediana de las 28 en el momento de escribir esto; si algun dia
# el listado cambia mucho, se recalcula midiendo la mediana de todas otra vez.
# No se llega hasta el objetivo (FUERZA) ni se pasa del TOPE, para nivelar sin
# aplanar: una foto con su intencion tiene que conservarla.
OBJETIVO = 112

# La correccion es asimetrica a proposito. Subir una foto oscura la mejora casi
# siempre: estaba subexpuesta. Bajar una clara le quita fuerza, y las claras son
# justo las verdes y azules que tiran del listado -- con la misma fuerza en los
# dos sentidos perdian hasta un 12% de contraste y el conjunto se veia soso.
# Asi que las oscuras suben como antes y las claras apenas se mueven.
FUERZA_SUBIR = 0.45
FUERZA_BAJAR = 0.20
TOPE = (0.92, 1.35)

# Por debajo de esta luminancia la foto es de noche o a contraluz. Ahi no se
# toca el brillo: el primer intento le metia azul al amanecer de la ermita y la
# dejaba con pinta de retocada. Una foto de noche debe seguir siendo de noche.
NOCHE = 70


def card_photos():
    """Las fotos de origen de las tarjetas, en orden de aparicion.

    El marcado ya apunta a la version pequena (img/<nombre>-card.jpg), asi que
    hay que quitarle el sufijo para volver a la foto grande: si no, la segunda
    vez que se pasa el script no encuentra nada que hacer.
    """
    html = open(HOME_TAIL, encoding="utf-8").read()
    names = []
    for block in re.findall(r'<div class="route-card-photo">.*?</div>', html, re.S):
        for m in re.finditer(r'img/([A-Za-z0-9._-]+)\.jpg', block):
            name = m.group(1)
            if name.endswith(SUFFIX):
                name = name[:-len(SUFFIX)]
            if name not in names:
                names.append(name)
    return names


def luminancia(im):
    """Mediana del canal de luz, 0-255. La mediana y no la media: una foto con
    un cielo enorme y quemado enganaria a la media."""
    return ImageStat.Stat(im.convert("L")).median[0]


def igualar_tono(im):
    """Deja la foto en el mismo registro que el resto del listado."""
    if luminancia(im) < NOCHE:
        # Solo un nivelado minimo, y ni brillo ni ajuste hacia el objetivo.
        im = Image.blend(im, ImageOps.autocontrast(im, cutoff=2, preserve_tone=True), 0.25)
    else:
        im = Image.blend(im, ImageOps.autocontrast(im, cutoff=1, preserve_tone=True), 0.5)
        actual = max(luminancia(im), 1)
        fuerza = FUERZA_SUBIR if actual < OBJETIVO else FUERZA_BAJAR
        deseada = actual + (OBJETIVO - actual) * fuerza
        factor = min(max(deseada / actual, TOPE[0]), TOPE[1])
        im = ImageEnhance.Brightness(im).enhance(factor)
    im = ImageEnhance.Color(im).enhance(SATURACION)
    return ImageEnhance.Contrast(im).enhance(CONTRASTE)


def make(name):
    src = os.path.join(IMG_DIR, name + ".jpg")
    if not os.path.exists(src):
        print("  falta %s.jpg" % name)
        return 0
    im = Image.open(src).convert("RGB")
    w, h = im.size

    # La tarjeta ya recorta la foto por el centro (object-fit:cover sobre un
    # aspect-ratio 16/10). Recortarla aqui igual no cambia nada de lo que se ve
    # y quita de en medio todo lo que el navegador iba a tirar de todos modos:
    # es lo que hace pequenas las fotos verticales, que son las mas pesadas.
    if w / h > CARD_RATIO:
        nw = round(h * CARD_RATIO)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / CARD_RATIO)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))

    w, h = im.size
    if w > CARD_WIDTH:                       # nunca se amplia una foto pequena
        im = im.resize((CARD_WIDTH, round(h * CARD_WIDTH / w)), Image.LANCZOS)

    im = igualar_tono(im)

    jpg = os.path.join(IMG_DIR, name + SUFFIX + ".jpg")
    webp = os.path.join(IMG_DIR, name + SUFFIX + ".webp")
    im.save(jpg, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    im.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
    saved = os.path.getsize(src) - os.path.getsize(webp)
    print("  %-22s %5.0f KB -> %4.0f KB webp / %4.0f KB jpg" % (
        name, os.path.getsize(src) / 1024,
        os.path.getsize(webp) / 1024, os.path.getsize(jpg) / 1024))
    return saved


def main():
    names = card_photos()
    if not names:
        sys.exit("No he encontrado ninguna foto de tarjeta en mallabia_tail.html")
    print("%d fotos de tarjeta:" % len(names))
    saved = sum(make(n) for n in names)
    print("\nla portada se ahorra %.1f MB al recorrerla entera" % (saved / 1e6))


if __name__ == "__main__":
    main()
