#!/usr/bin/env python3
"""Genera los iconos PNG del manifest a partir de favicon.svg.

    python3 scripts/make_icons.py

El manifest necesita un 192 y un 512 en PNG para que el movil pueda poner la
web en la pantalla de inicio; el SVG no vale en todos los navegadores. En vez
de dibujar el icono otra vez aqui (dos sitios que se desincronizan), se lee el
propio favicon.svg: si algun dia cambia, basta con volver a pasar esto.

Solo entiende las primitivas que usa ese icono -- <rect rx>, <path> de lineas
rectas y <circle> -- y avisa si se encuentra cualquier otra cosa, en vez de
dibujar algo distinto en silencio.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SVG = os.path.join(ROOT, "favicon.svg")
TAMANOS = (192, 512)
SUPER = 8          # se dibuja 8x y se reduce: es el antialiasing


def figuras(raiz):
    for el in raiz:
        etiqueta = el.tag.split("}")[-1]
        color = el.get("fill")
        if etiqueta == "rect":
            yield ("rect", (float(el.get("x", 0)), float(el.get("y", 0)),
                            float(el.get("width")), float(el.get("height")),
                            float(el.get("rx", 0))), color)
        elif etiqueta == "circle":
            yield ("circle", (float(el.get("cx")), float(el.get("cy")), float(el.get("r"))), color)
        elif etiqueta == "path":
            d = el.get("d", "").strip()
            if not re.fullmatch(r"[MLZ\d\s.,-]+", d):
                sys.exit(f"favicon.svg: no se dibujar el path {d!r} (solo M/L/Z)")
            puntos = [tuple(map(float, par.split()))
                      for par in re.findall(r"[ML]\s*([\d.-]+\s+[\d.-]+)", d)]
            yield ("poly", puntos, color)
        else:
            sys.exit(f"favicon.svg: elemento <{etiqueta}> que no se dibujar")


def main():
    raiz = ET.parse(SVG).getroot()
    lado_svg = float(raiz.get("viewBox").split()[2])
    for lado in TAMANOS:
        escala = lado * SUPER / lado_svg
        im = Image.new("RGBA", (lado * SUPER, lado * SUPER), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for clase, datos, color in figuras(raiz):
            if clase == "rect":
                x, y, an, al, rx = (v * escala for v in datos)
                d.rounded_rectangle([x, y, x + an, y + al], radius=rx, fill=color)
            elif clase == "circle":
                cx, cy, r = (v * escala for v in datos)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
            else:
                d.polygon([(x * escala, y * escala) for x, y in datos], fill=color)
        im = im.resize((lado, lado), Image.LANCZOS)
        salida = os.path.join(ROOT, f"icon-{lado}.png")
        im.save(salida, "PNG", optimize=True)
        print(f"  icon-{lado}.png  {os.path.getsize(salida)/1024:.1f} KB")


if __name__ == "__main__":
    main()
