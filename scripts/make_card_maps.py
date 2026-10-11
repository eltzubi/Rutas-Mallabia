#!/usr/bin/env python3
"""Dibuja la miniatura de mapa de cada ruta para las tarjetas de la portada.

    python3 scripts/make_card_maps.py           # las que falten
    python3 scripts/make_card_maps.py --force   # todas otra vez

La silueta del track sola no dice gran cosa; sobre un mapa, si: se ve por
donde cae la ruta, que pueblos toca y si es un circuito o una travesia.

El mapa NO se pide al visitante. Se dibuja aqui, una sola vez, y lo que se
publica es una imagen nuestra en img/. Eso importa por dos razones:

  - Las teselas del IGN y de OpenStreetMap no se pueden guardar en bloque: lo
    prohiben sus condiciones de uso, que es justo lo que hay que respetar en
    una web que sirve 118 paginas.
  - OpenFreeMap si lo permite -- es gratis, sin clave, sin limites, uso
    comercial incluido, y reparte el planeta entero para descargar -- asi que
    el mapa sale de ahi (datos de OpenStreetMap via OpenMapTiles). La
    atribucion va en el pie de la portada.

Se dibuja con MapLibre dentro del Chromium que ya usa el driver, y la imagen
se guarda en WebP. Hay que volver a pasarlo cuando entre una ruta nueva.
"""
import argparse
import glob
import json
import math
import os
import sys
import tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "img")
TRAILHEAD = os.path.join(ROOT, "data", "trailhead.json")

ANCHO, ALTO = 320, 200      # el doble de lo que mide en pantalla
CALIDAD = 72
ESTILO = "https://tiles.openfreemap.org/styles/liberty"
COLOR = {"bici": "#0f7d8c", "senderismo": "#3f6b14"}   # sobre mapa claro
RELLENO = 16

PLANTILLA = """<!doctype html><html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/4.7.1/maplibre-gl.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/4.7.1/maplibre-gl.min.css" rel="stylesheet">
<style>html,body{margin:0}#m{width:%(ancho)dpx;height:%(alto)dpx}
.maplibregl-ctrl-attrib{display:none}</style></head>
<body><div id="m"></div><script>
window.listo = false;
const puntos = %(puntos)s;
const mapa = new maplibregl.Map({container:'m', style:'%(estilo)s',
  attributionControl:false, interactive:false, fadeDuration:0});
mapa.on('load', () => {
  mapa.addSource('track', {type:'geojson', data:{type:'Feature',
    geometry:{type:'LineString', coordinates:puntos}}});
  mapa.addLayer({id:'track-halo', type:'line', source:'track',
    paint:{'line-color':'#ffffff','line-width':6,'line-opacity':.85},
    layout:{'line-cap':'round','line-join':'round'}});
  mapa.addLayer({id:'track', type:'line', source:'track',
    paint:{'line-color':'%(color)s','line-width':3},
    layout:{'line-cap':'round','line-join':'round'}});
  const caja = puntos.reduce((b,c) => b.extend(c),
    new maplibregl.LngLatBounds(puntos[0], puntos[0]));
  mapa.fitBounds(caja, {padding:%(relleno)d, duration:0});
  mapa.once('idle', () => { window.listo = true; });
});
</script></body></html>
"""


def navegador():
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                "/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"):
        hit = sorted(glob.glob(pat))
        if hit:
            return hit[-1]
    sys.exit("sin chromium")


def actividad_de(slug):
    """Bici o senderismo, leido de la tarjeta de la portada."""
    html = open(os.path.join(ROOT, "src", "mallabia_tail.html"), encoding="utf-8").read()
    import re
    m = re.search(r'href="%s\.html" data-activity="([^"]*)"' % re.escape(slug), html)
    act = (m.group(1) if m else "bici").split(",")[0]
    return act if act in COLOR else "bici"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--solo", nargs="*", help="solo estos slugs")
    a = ap.parse_args()

    tracks = json.load(open(TRAILHEAD))["tracks"]
    pendientes = []
    for t in tracks:
        slug = (t.get("href") or "").replace(".html", "")
        if not slug or not t.get("points"):
            continue
        if a.solo and slug not in a.solo:
            continue
        destino = os.path.join(IMG, f"mapa-{slug}.webp")
        if os.path.exists(destino) and not a.force:
            continue
        pendientes.append((slug, t["points"], destino))

    if not pendientes:
        print("nada que dibujar")
        return
    print(f"{len(pendientes)} mapas por dibujar")

    prox = os.environ.get("HTTPS_PROXY")
    hechos = peso = 0
    with sync_playwright() as p:
        nav = p.chromium.launch(
            executable_path=navegador(),
            args=["--no-sandbox", "--ignore-certificate-errors",
                  "--use-gl=swiftshader", "--enable-unsafe-swiftshader"],
            proxy={"server": prox} if prox else None)
        pg = nav.new_page(viewport={"width": ANCHO, "height": ALTO},
                          device_scale_factor=1)
        for slug, puntos, destino in pendientes:
            # MapLibre quiere lon,lat; el track viene en lat,lon.
            coords = [[round(q[1], 5), round(q[0], 5)] for q in puntos]
            html = PLANTILLA % {"ancho": ANCHO, "alto": ALTO, "estilo": ESTILO,
                                "puntos": json.dumps(coords),
                                "color": COLOR[actividad_de(slug)],
                                "relleno": RELLENO}
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                             encoding="utf-8") as f:
                f.write(html)
                ruta = f.name
            try:
                pg.goto("file://" + ruta)
                for _ in range(60):
                    if pg.evaluate("window.listo"):
                        break
                    pg.wait_for_timeout(500)
                pg.wait_for_timeout(600)
                crudo = pg.screenshot(type="png")
            finally:
                os.unlink(ruta)
            with tempfile.NamedTemporaryFile("wb", suffix=".png", delete=False) as f:
                f.write(crudo)
                tmp = f.name
            Image.open(tmp).convert("RGB").save(destino, "WEBP",
                                                quality=CALIDAD, method=6)
            os.unlink(tmp)
            hechos += 1
            peso += os.path.getsize(destino)
            print(f"  {slug:28} {os.path.getsize(destino)//1024:3} kB")
        nav.close()
    print(f"\n{hechos} mapas, {peso/1024:.0f} kB en total "
          f"({peso/hechos/1024:.0f} kB de media)")


if __name__ == "__main__":
    main()
