#!/usr/bin/env python3
"""Rellena data-places de cada tarjeta de la portada con los lugares por los que pasa su track.

    python3 scripts/make_places.py

El buscador de la portada (src/js/filters.js) busca en el nombre, la descripcion
y data-places de cada tarjeta. data-places no se ve en pantalla: solo sirve para
que una ruta aparezca al buscar un pueblo, barrio, cima o ermita por el que pasa
aunque no salga en su titulo.

Fuentes, todas verificadas contra el track real de la ruta (data/<ruta>.json):
- los lugares que ya estaban puestos a mano en data-places (se conservan, primero);
- los puntos numerados de la propia ficha (su .elev-legend);
- OpenStreetMap: una copia fija en scripts/osm/ (places.json: pueblos, barrios y
  parajes; pois.json: cimas, collados, iglesias y ermitas, cascadas), bajada de
  Overpass. Un lugar entra si el track pasa a menos de MAX_M metros de el.
  Datos (c) colaboradores de OpenStreetMap, licencia ODbL.

No hace falta conexion: para refrescar los datos de OSM, vuelve a bajar esos dos
ficheros con la consulta que se describe en scripts/osm/LEEME.txt.

Hay que volver a pasarlo cuando entre una ruta nueva a la portada.
"""
import html
import json
import math
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOME = os.path.join(ROOT, 'src', 'mallabia_tail.html')

# Distancia maxima del track, por tipo de lugar. Un pueblo es un punto en su
# centro, asi que se le da mas margen; un paraje (locality) o una cima solo
# cuentan si el track pasa practicamente por encima.
MAX_M = {
    'town': 450, 'village': 350, 'suburb': 250, 'hamlet': 200, 'neighbourhood': 200,
    'locality': 70, 'peak': 60, 'saddle': 80, 'pass': 80,
    'place_of_worship': 70, 'waterfall': 150,
}


# Parajes que en OSM se llaman solo con un nombre comun ("Presa", "Fuente"):
# harian saltar rutas al buscar esa palabra sin que tengan nada de especial.
GENERICOS = {'presa', 'fuente', 'iturri', 'iturria', 'borda', 'errota', 'ermita', 'eliza',
             'iglesia', 'mirador', 'puente', 'zubia', 'cueva', 'kobea', 'cantera', 'harrobia',
             'larrea', 'basoa', 'mendia', 'gaina', 'etxea', 'caserio', 'baserria', 'molino',
             'lavadero', 'garbitokia', 'plaza', 'enparantza', 'campa', 'zelaia'}


def fold(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower().strip()


def kind(tags):
    if tags.get('place'):
        return tags['place']
    if tags.get('natural') in ('peak', 'saddle'):
        return tags['natural']
    if tags.get('mountain_pass') == 'yes':
        return 'pass'
    if tags.get('amenity') == 'place_of_worship':
        return 'place_of_worship'
    if tags.get('waterway') == 'waterfall':
        return 'waterfall'
    return None


def names(tags):
    out = []
    for k in ('name', 'name:es', 'name:eu', 'alt_name'):
        for n in (tags.get(k) or '').split(';'):
            n = n.strip()
            if n and fold(n) not in GENERICOS and fold(n) not in [fold(x) for x in out]:
                out.append(n)
    return out


def load_osm():
    feats = []
    for f in ('places.json', 'pois.json'):
        for e in json.load(open(os.path.join(HERE, 'osm', f), encoding='utf-8'))['elements']:
            k = kind(e.get('tags', {}))
            lat = e.get('lat', (e.get('center') or {}).get('lat'))
            lon = e.get('lon', (e.get('center') or {}).get('lon'))
            if k in MAX_M and lat is not None and names(e['tags']):
                feats.append((lat, lon, MAX_M[k], names(e['tags'])))
    return feats


def dist_to_track(lat, lon, pts):
    """Distancia minima en metros de un punto a la polilinea (proyeccion local)."""
    ky = 111320.0
    kx = 111320.0 * math.cos(math.radians(lat))
    best = float('inf')
    px, py = 0.0, 0.0
    prev = None
    for a, b in pts:
        x, y = (b - lon) * kx, (a - lat) * ky
        if prev is None:
            best = min(best, math.hypot(x, y))
        else:
            dx, dy = x - prev[0], y - prev[1]
            L = dx * dx + dy * dy
            t = 0 if L == 0 else max(0, min(1, -(prev[0] * dx + prev[1] * dy) / L))
            best = min(best, math.hypot(prev[0] + t * dx - px, prev[1] + t * dy - py))
        prev = (x, y)
    return best


def legend_names(slug):
    p = os.path.join(ROOT, 'src', f'{slug}_tail.html')
    if not os.path.exists(p):
        return []
    s = open(p, encoding='utf-8').read()
    return [html.unescape(n).strip() for n in
            re.findall(r'<span class="num">\d+</span>([^<]+)</span>', s)]


def main():
    feats = load_osm()
    s = open(HOME, encoding='utf-8').read()
    total = 0

    def fix(m):
        nonlocal total
        tag = m.group(0)
        slug = m.group(1).split('.')[0]
        data = os.path.join(ROOT, 'data', f'{slug}.json')
        if not os.path.exists(data):
            return tag
        pts = [p for t in json.load(open(data, encoding='utf-8'))['tracks'] for p in t['points']]
        lats = [p[0] for p in pts]; lons = [p[1] for p in pts]
        old = re.search(r' data-places="([^"]*)"', tag)
        found = [html.unescape(x).strip() for x in (old.group(1).split(',') if old else []) if x.strip()]
        found += legend_names(slug)
        for lat, lon, maxm, ns in feats:
            if not (min(lats) - 0.01 < lat < max(lats) + 0.01 and min(lons) - 0.01 < lon < max(lons) + 0.01):
                continue
            if dist_to_track(lat, lon, pts) <= maxm:
                found += ns
        out, seen = [], set()
        for n in found:
            if fold(n) not in seen:
                seen.add(fold(n)); out.append(n)
        total += len(out)
        attr = ' data-places="' + html.escape(', '.join(out), quote=True) + '"'
        tag = re.sub(r' data-places="[^"]*"', '', tag)
        return tag[:-1] + attr + '>'

    s2 = re.sub(r'<a class="route-card" href="([^"]+)"[^>]*>', fix, s)
    open(HOME, 'w', encoding='utf-8').write(s2)
    print(f'{total} lugares en {s2.count(chr(32) + "data-places=")} tarjetas')


if __name__ == '__main__':
    main()
