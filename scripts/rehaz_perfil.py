#!/usr/bin/env python3
"""Rehace el perfil de altura y los puntos numerados de una ficha, desde su GPX.

    python3 scripts/rehaz_perfil.py <ruta> [<ruta>...]

Hace falta cada vez que cambia un track: el perfil, el kilometro de cada
punto numerado y la distancia de la ficha salen del GPX, y si el track se
recorta o se empalma (ver scripts/aleja_de_casa.py) dejan de cuadrar.

La forma del dibujo es la que ya tenian las fichas, deducida de ellas y
comprobada contra el fichero antes de tocar nada: 161 muestras repartidas por
distancia recorrida, x = k*1000/160, y = 285 - (ele-min)/(max-min)*270 sobre
un viewBox de 0 0 1000 300. Dos trazados, el relleno y la linea.

NO toca el desnivel acumulado. Esa cifra no sale del GPX -- sumar las subidas
del track en bruto se va hasta un 43% -- sino de la fuente de cada ruta, y la
propia ficha lo dice. Un recorte de medio kilometro de carretera no la mueve.
"""
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NS = "{http://www.topografix.com/GPX/1/1}"
N = 161


def haversine(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0]); dl = math.radians(b[1] - a[1])
    return 2 * r * math.asin(math.sqrt(
        math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))


def track(slug):
    ps = []
    for p in ET.parse(os.path.join(ROOT, "src", slug + ".gpx")).getroot().iter(NS + "trkpt"):
        e = p.find(NS + "ele")
        ps.append((float(p.get("lat")), float(p.get("lon")),
                   float(e.text) if e is not None else 0.0))
    acum = [0.0]
    for i in range(1, len(ps)):
        acum.append(acum[-1] + haversine(ps[i - 1], ps[i]))
    return ps, acum


def muestras(ps, acum):
    tot = acum[-1]
    out = []
    for k in range(N):
        meta = tot * k / (N - 1)
        j = min(range(len(acum)), key=lambda i: abs(acum[i] - meta))
        out.append(ps[j][2])
    return out


def en_km(ps, acum, punto):
    """Kilometro y altura del track en el punto mas cercano a 'punto'."""
    j = min(range(len(ps)), key=lambda i: haversine(ps[i], punto))
    return acum[j] / 1000, ps[j][2]


def rehaz(slug):
    ps, acum = track(slug)
    alt = muestras(ps, acum)
    mn, mx = min(alt), max(alt)
    xy = ["%.1f,%.1f" % (k * 1000 / 160, 285 - (alt[k] - mn) / (mx - mn) * 270)
          for k in range(N)]
    linea = "M" + " L".join(xy)
    relleno = linea + " L1000,300 L0,300 Z"

    import json
    with open(os.path.join(ROOT, "data", slug + ".json"), encoding="utf-8") as f:
        wps = json.load(f).get("waypoints", [])

    ruta = os.path.join(ROOT, "src", slug + "_tail.html")
    t = open(ruta, encoding="utf-8").read()

    largos = re.findall(r'<path d="(M[^"]{200,})"', t)
    if len(largos) != 2:
        raise SystemExit(f"{slug}: esperaba 2 trazados largos, encuentro {len(largos)}")
    t = t.replace(largos[0], relleno, 1).replace(largos[1], linea, 1)

    def nuevo_marcador(m, i):
        km, ele = en_km(ps, acum, tuple(wps[i]))
        x = km * 1000 / (acum[-1] / 1000) / 1000 * 1000
        x = km / (acum[-1] / 1000) * 1000
        y = 285 - (ele - mn) / (mx - mn) * 270
        nombre = re.search(r"<title>(.*?) &middot;", m.group(0)).group(1)
        return ('<g class="elev-marker"><title>%s &middot; %s km &middot; %s m</title>'
                '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--teal)" stroke="var(--ground)" stroke-width="2.5"/>'
                '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" '
                'font-family="IBM Plex Mono, monospace" font-size="10" font-weight="700" '
                'fill="var(--ground)">%d</text></g>'
                % (nombre, ("%.1f" % km).replace(".", ","), "%.0f" % ele, x, y, x, y, i + 1))

    n = [0]
    def reemplaza(m):
        i = n[0]; n[0] += 1
        return nuevo_marcador(m, i)
    t = re.sub(r'<g class="elev-marker">.*?</g>', reemplaza, t, flags=re.S)
    if n[0] != len(wps):
        raise SystemExit(f"{slug}: {n[0]} marcadores y {len(wps)} waypoints")

    # la distancia de la ficha
    km_tot = ("%.2f" % (acum[-1] / 1000)).replace(".", ",")
    t = re.sub(r'(<div class="fact"><span class="v">)[\d.,]+( km</span>)',
               lambda m: m.group(1) + km_tot + m.group(2), t, count=1)
    open(ruta, "w", encoding="utf-8").write(t)
    print("%s: %s km, %d puntos numerados, perfil entre %.0f y %.0f m"
          % (slug, km_tot, len(wps), mn, mx))
    return km_tot


if __name__ == "__main__":
    for s in sys.argv[1:]:
        rehaz(s)
