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

# Nueve fichas llevan los kilometros de sus puntos numerados sobre la base
# antigua, anterior al commit e4967121, y el autor decidio dejarlos asi. Aqui
# se respetan: se rehace el perfil y la distancia, pero no sus marcadores.
# Ver «Content rules» en CLAUDE.md.
BASE_ANTIGUA = ('sancristobal', 'trabakua', 'urregarai', 'zengotitagane',
                'egoarbitza', 'kalamua', 'urko', 'arteta', 'zenarruza')

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


def en_km(ps, acum, punto, pista=None):
    """Kilometro y altura del track en el punto mas cercano a 'punto'.

    Una ruta puede pasar dos veces por el mismo sitio, y entonces "el mas
    cercano" no basta: trabakuamallabia pasa por Zengotita en el km 3,67 (a
    2 m) y en el 14,71 (a 1 m), y coger el minimo movia el punto numerado
    once kilometros. Si se sabe en que kilometro lo puso el autor, se elige
    el paso que le corresponde.
    """
    d = [haversine(q, punto) for q in ps]
    j = min(range(len(ps)), key=lambda i: d[i])
    if pista is not None:
        # todos los pasos que se acercan tanto como el mejor, con margen
        tope = max(d[j] + 15.0, d[j] * 3)
        pasos = []
        for i in range(len(ps)):
            if d[i] <= tope and all(abs(acum[i] - acum[k]) > 500 for k in pasos):
                pasos.append(i)
        if pasos:
            j = min(pasos, key=lambda i: abs(acum[i] / 1000 - pista))
    return acum[j] / 1000, ps[j][2]


_KM_TITULO = re.compile(
    r'<title>[^<]*?(?:&middot;|\u00b7) (\d+)(?:,(\d+))? km'
    r'( (?:&middot;|\u00b7) [\d.]+ m)?</title>')


def _forma_original(slug, actual):
    """Como escribia cada punto su kilometro: decimales y si lleva altura.

    Se mira la version de git y no la del disco, porque si esta ficha ya se
    ha reescrito una vez el dato de origen se habria perdido. Importa porque
    no todas las fichas lo escriben igual: unas con un decimal y otras con
    dos, y sancristobalgaraiandikoa sin altura. Cambiarlo seria tocar algo
    que nadie ha pedido -- y ademas rompe las claves de src/i18n/eu.py.
    """
    import subprocess
    r = subprocess.run(["git", "show", "HEAD:src/%s_tail.html" % slug],
                       capture_output=True, text=True, cwd=ROOT)
    fuente = r.stdout or actual
    return [(len(m.group(2) or ''), bool(m.group(3)),
             float(m.group(1) + "." + (m.group(2) or "0")))
            for m in _KM_TITULO.finditer(fuente)]


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
    forma = _forma_original(slug, t)

    largos = re.findall(r'<path d="(M[^"]{200,})"', t)
    if len(largos) != 2:
        raise SystemExit(f"{slug}: esperaba 2 trazados largos, encuentro {len(largos)}")
    # No todas las fichas dibujan el perfil igual: trabakuamallabia lleva 201
    # muestras repartidas por puntos del track y separadas por espacios, y
    # zengotitagane 160. Redibujarlas con esta convencion no las corrige,
    # las cambia de estilo sin que nadie lo haya pedido. Mejor pararse.
    xs = re.findall(r'[ML]([\d.]+)[, ]', largos[1])
    paso = [float(xs[i + 1]) - float(xs[i]) for i in range(len(xs) - 1)]
    if len(xs) != N or max(paso) - min(paso) > 0.1 or "," not in largos[1]:
        raise SystemExit(
            "%s: el perfil no esta dibujado con esta convencion (%d muestras, "
            "separador %r). Redibujarlo lo cambiaria de estilo: miralo a mano."
            % (slug, len(xs), "," if "," in largos[1] else " "))
    t = t.replace(largos[0], relleno, 1).replace(largos[1], linea, 1)

    def nuevo_marcador(m, i):
        km, ele = en_km(ps, acum, tuple(wps[i]),
                        forma[i][2] if i < len(forma) else None)
        x = km / (acum[-1] / 1000) * 1000
        y = 285 - (ele - mn) / (mx - mn) * 270
        # Unas fichas escriben el separador como &middot; y otras como el
        # caracter · tal cual: se respeta el que ya tuviera.
        cab = re.search(r"<title>(.*?) (&middot;|·) ", m.group(0))
        if cab is None:
            raise SystemExit("%s: no entiendo el titulo %r" % (slug, m.group(0)[:90]))
        nombre, sep = cab.group(1), cab.group(2)
        # Cada ficha escribe el kilometro con uno o con dos decimales, y a
        # veces mezcla las dos cosas. Se conserva el que ya tenia ese punto:
        # cambiarlo seria tocar algo que nadie ha pedido.
        dec, con_altura = forma[i][:2] if i < len(forma) else (1, True)
        cuerpo = ('<title>%s {s} %s km {s} %s m</title>' if con_altura
                  else '<title>%s {s} %s km</title>')
        plantilla = (
            '<g class="elev-marker">' + cuerpo +
            '<circle cx="%.1f" cy="%.1f" r="9" fill="var(--teal)" stroke="var(--ground)" stroke-width="2.5"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" '
            'font-family="IBM Plex Mono, monospace" font-size="10" font-weight="700" '
            'fill="var(--ground)">%d</text></g>').replace("{s}", sep)
        datos = [nombre, ("%.*f" % (dec, km)).replace(".", ",")]
        if con_altura:
            # Mil y pico metros se escribe «1.020 m» en todas las fichas.
            datos.append("{:,.0f}".format(ele).replace(",", "."))
        return plantilla % tuple(datos + [x, y, x, y, i + 1])

    n = [0]
    def reemplaza(m):
        i = n[0]; n[0] += 1
        return m.group(0) if slug in BASE_ANTIGUA else nuevo_marcador(m, i)
    t = re.sub(r'<g class="elev-marker">.*?</g>', reemplaza, t, flags=re.S)
    if n[0] != len(wps):
        raise SystemExit(f"{slug}: {n[0]} marcadores y {len(wps)} waypoints")

    # La leyenda de debajo del perfil. Casi todas las fichas ponen ahi solo
    # el nombre, pero sancristobalgaraiandikoa le pone tambien el kilometro, y
    # si no se toca se queda contando otra cosa que el punto numerado.
    kms = re.findall(r'<title>[^<]*?(?:&middot;|\u00b7) ([\d,]+) km', t)
    leyenda = [0]

    def pon_leyenda(m):
        i = leyenda[0]; leyenda[0] += 1
        return (m.group(1) + kms[i] + m.group(3)) if i < len(kms) else m.group(0)

    t = re.sub(r'(<span class="elev-legend-item"><span class="num">\d+</span>'
               r'[^<]*? (?:&middot;|\u00b7) )([\d,]+)( km</span>)', pon_leyenda, t)

    # la distancia de la ficha
    km_tot = ("%.2f" % (acum[-1] / 1000)).replace(".", ",")
    t = re.sub(r'(<div class="fact"><span class="v">)[\d.,]+( km</span>)',
               lambda m: m.group(1) + km_tot + m.group(2), t, count=1)
    open(ruta, "w", encoding="utf-8").write(t)
    print("%s: %s km, %d puntos numerados%s, perfil entre %.0f y %.0f m"
          % (slug, km_tot, len(wps),
             " (intactos: base antigua)" if slug in BASE_ANTIGUA else "", mn, mx))
    return km_tot


if __name__ == "__main__":
    for s in sys.argv[1:]:
        rehaz(s)
