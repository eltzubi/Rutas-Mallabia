#!/usr/bin/env python3
"""Hace data/caminos-zona.json: la RED DE CAMINOS de la zona, para el lapiz.

    python3 scripts/make_caminos.py <respuestas-de-overpass.json ...>

Sin argumentos solo dice la consulta que hay que bajar y se para.

POR QUE EXISTE. El lapiz de la web calcula el camino entre dos toques sobre
una red hecha con los tracks de las rutas publicadas. Eso tiene un techo
medido: las rutas abarcan un recuadro de 24 x 22,7 km y solo el 26% de el
esta a menos de 120 m de un camino grabado, asi que 74 de cada 100 toques no
enganchan nada. No es un fallo del codigo; es que la red solo tiene lo que
esta grabado. Con los caminos de OpenStreetMap, el lapiz va por cualquier
pista y cualquier sendero.

QUE SE BAJA. Los `highway` de la caja, menos autopistas y cosas que no son
para andar (proposed, construction, raceway, plataformas de bus). Con sus
ETIQUETAS: sin ellas no se distingue un sendero de una nacional, y una ruta a
pie no puede ir por cualquier sitio.

QUE SE GUARDA, Y POR QUE NO TODOS LOS PUNTOS. Un grafo CONTRAIDO: los nodos
son solo los cruces y los extremos, y entre dos de ellos va un tramo con su
longitud, su clase y la forma del camino. Guardar punto a punto serian unos
350.000 nodos, y en un movil eso no cabe como objetos de JavaScript -cada
nodo y cada vecino es un array-. Contraido son unas decenas de miles de
tramos: el calculo del camino va sobre los cruces y la forma solo se usa para
dibujar.

FORMATO. Todo en centesimas de milesima de grado (1,1 m) y en diferencias:

  nodos   lat,lon de cada cruce, en diferencias sobre el anterior
  tramos  una lista plana de enteros; por cada tramo:
            a, b, clase, largo_m, k, y luego 2k diferencias con la forma
          (a y b son indices de `nodos`; la forma va de a hacia b y no
           incluye ni a ni b)
  clases  0 sendero  1 pista  2 calle o servicio  3 carretera  4 bidegorri
          5 nacional o similar  6 privado o restringido

Las clases las usa el buscador de caminos para no mandar a nadie por una
nacional cuando hay un sendero al lado.
"""
import glob
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BBOX = [43.10, -2.72, 43.42, -2.34]
ESCALA = 100000          # 1,1 m
SIMPLIFICA_M = 8.0    # Douglas-Peucker sobre la forma de cada tramo
EXCLUIR = ('motorway', 'motorway_link', 'proposed', 'construction',
           'raceway', 'bus_guideway', 'platform')

CONSULTA = ('[out:json][timeout:600];way["highway"]'
            '["highway"!~"^(%s)$"](%.2f,%.2f,%.2f,%.2f);out body;>;out skel;'
            % ('|'.join(EXCLUIR), BBOX[0], BBOX[1], BBOX[2], BBOX[3]))

CLASES = {
    'footway': 0, 'path': 0, 'steps': 0, 'bridleway': 0, 'pedestrian': 0,
    'track': 1,
    'service': 2, 'residential': 2, 'unclassified': 2, 'living_street': 2,
    'road': 2, 'busway': 2,
    'tertiary': 3, 'tertiary_link': 3, 'secondary': 3, 'secondary_link': 3,
    'primary': 3, 'primary_link': 3,
    'cycleway': 4,
    'trunk': 5, 'trunk_link': 5,
}
CLASE_POR_DEFECTO = 2
CLASE_PRIVADO = 6
# Los trozos de las rutas publicadas que OpenStreetMap no tiene. Medido: el
# 93,4% de los puntos de las 72 rutas esta a menos de CUBIERTO_M de un camino
# de OSM, pero el 6,6% que falta es real -gerea el 49%, 7pago el 64%- y son
# sitios por los que el autor anda. Si la red fuera solo OSM, el lapiz
# perderia justo eso, que hoy si puede dibujar. Asi que esos trozos se suman.
CLASE_GRABADO = 7
CUBIERTO_M = 25      # a esta distancia un punto de ruta ya tiene camino OSM
PEGA_M = 30          # a esta, el extremo de un trozo se engancha a la red
CELDA_BUSCA = 0.0009  # unos 100 m


def metros(a, b):
    dy = (b[0] - a[0]) * 111195.0
    dx = (b[1] - a[1]) * 111195.0 * math.cos((a[0] + b[0]) / 2 * math.pi / 180)
    return math.hypot(dx, dy)


def simplifica(pts, tol):
    """Douglas-Peucker, en metros."""
    if len(pts) < 3:
        return pts[:]
    guarda = [False] * len(pts)
    guarda[0] = guarda[-1] = True
    pila = [(0, len(pts) - 1)]
    while pila:
        i, j = pila.pop()
        if j <= i + 1:
            continue
        a, b = pts[i], pts[j]
        kx = math.cos(a[0] * math.pi / 180)
        ax, ay = a[1] * kx, a[0]
        bx, by = b[1] * kx, b[0]
        dx, dy = bx - ax, by - ay
        norma = dx * dx + dy * dy
        peor, donde = -1.0, -1
        for k in range(i + 1, j):
            px, py = pts[k][1] * kx, pts[k][0]
            if norma:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / norma))
            else:
                t = 0.0
            d = math.hypot(px - (ax + t * dx), py - (ay + t * dy)) * 111195.0
            if d > peor:
                peor, donde = d, k
        if peor > tol and donde > 0:
            guarda[donde] = True
            pila.append((i, donde))
            pila.append((donde, j))
    return [p for p, g in zip(pts, guarda) if g]


def lee(ficheros):
    nodos = {}
    vias = {}
    for f in ficheros:
        d = json.load(io.open(f, encoding='utf-8'))
        for e in d['elements']:
            if e['type'] == 'node':
                nodos[e['id']] = (e['lat'], e['lon'])
            elif e['type'] == 'way':
                vias[e['id']] = (e.get('nodes', []), e.get('tags', {}) or {})
        print('%s: %d caminos, %d nodos acumulados'
              % (os.path.basename(f), len(d['elements']), len(nodos)))
    return nodos, vias


def clase_de(tags):
    if tags.get('access') in ('private', 'no') or tags.get('foot') == 'no':
        return CLASE_PRIVADO
    return CLASES.get(tags.get('highway'), CLASE_POR_DEFECTO)


def construye(nodos, vias):
    """Grafo contraido: nodos = cruces y extremos; tramos = lo de en medio."""
    # Cuantas veces aparece cada nodo: si esta en dos caminos, o es extremo,
    # es un nodo del grafo. Lo de en medio es solo forma.
    veces = {}
    for ns, _ in vias.values():
        for i, n in enumerate(ns):
            veces[n] = veces.get(n, 0) + (2 if 0 < i < len(ns) - 1 else 1)
    corta = set()
    for ns, _ in vias.values():
        if not ns:
            continue
        corta.add(ns[0])
        corta.add(ns[-1])
        for n in ns[1:-1]:
            if veces.get(n, 0) > 2:
                corta.add(n)

    indice = {}
    puntos = []

    def idx(n):
        i = indice.get(n)
        if i is None:
            i = len(puntos)
            indice[n] = i
            puntos.append(nodos[n])
        return i

    tramos = []
    for ns, tags in vias.values():
        ns = [n for n in ns if n in nodos]
        if len(ns) < 2:
            continue
        cl = clase_de(tags)
        trozo = [ns[0]]
        for n in ns[1:]:
            trozo.append(n)
            if n in corta:
                if len(trozo) >= 2 and trozo[0] != trozo[-1]:
                    forma = [nodos[x] for x in trozo]
                    largo = sum(metros(forma[k - 1], forma[k])
                                for k in range(1, len(forma)))
                    medio = simplifica(forma, SIMPLIFICA_M)[1:-1]
                    tramos.append((idx(trozo[0]), idx(trozo[-1]), cl,
                                   int(round(largo)), medio))
                trozo = [n]
    return puntos, tramos


def rejilla_de(puntos, tramos):
    """Todos los puntos de la red en una rejilla de 100 m, con los tramos
    largos rellenados: un tramo recto sin puntos en medio dejaria fuera a lo
    que pase justo a su lado."""
    rej = {}

    def mete(p):
        rej.setdefault((math.floor(p[0] / CELDA_BUSCA),
                        math.floor(p[1] / CELDA_BUSCA)), []).append(p)

    for p in puntos:
        mete(p)
    for a, b, _cl, _largo, forma in tramos:
        pts = [puntos[a]] + forma + [puntos[b]]
        for k in range(1, len(pts)):
            p, q = pts[k - 1], pts[k]
            mete(q)
            d = metros(p, q)
            for j in range(1, int(d // 20) + 1):
                f = j * 20.0 / d
                mete((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
    return rej


def cerca_de(rej, p):
    k0 = math.floor(p[0] / CELDA_BUSCA)
    k1 = math.floor(p[1] / CELDA_BUSCA)
    mejor = 1e9
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for q in rej.get((k0 + a, k1 + b), ()):
                d = metros(p, q)
                if d < mejor:
                    mejor = d
    return mejor


def suma_lo_grabado(puntos, tramos):
    """Añade los trozos de las rutas publicadas que OSM no tiene."""
    rej = rejilla_de(puntos, tramos)
    # Para enganchar un extremo a un cruce que ya exista, y para que dos
    # rutas que comparten un trozo no cubierto compartan tambien sus nodos.
    cruces = {}
    for i, p in enumerate(puntos):
        cruces.setdefault((math.floor(p[0] / CELDA_BUSCA),
                           math.floor(p[1] / CELDA_BUSCA)), []).append(i)

    def nodo_para(p):
        k0 = math.floor(p[0] / CELDA_BUSCA)
        k1 = math.floor(p[1] / CELDA_BUSCA)
        mejor, suya = -1, PEGA_M
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for i in cruces.get((k0 + a, k1 + b), ()):
                    d = metros(p, puntos[i])
                    if d < suya:
                        suya, mejor = d, i
        if mejor >= 0:
            return mejor
        i = len(puntos)
        puntos.append(p)
        cruces.setdefault((k0, k1), []).append(i)
        return i

    metidos = km = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
        nombre = os.path.basename(f)[:-5]
        if nombre in ('trailhead', 'alturas', 'rutas', 'cruces-zona',
                      'caminos-zona'):
            continue
        try:
            d = json.load(io.open(f, encoding='utf-8'))
        except Exception:
            continue
        tr = (d.get('tracks') or [None])[0]
        pts = [(p[0], p[1]) for p in (tr or {}).get('points', [])]
        if len(pts) < 3:
            continue
        fuera = [cerca_de(rej, p) > CUBIERTO_M for p in pts]
        i = 0
        while i < len(pts):
            if not fuera[i]:
                i += 1
                continue
            j = i
            while j + 1 < len(pts) and fuera[j + 1]:
                j += 1
            # Un punto mas a cada lado, para que el trozo toque la red.
            a, b = max(0, i - 1), min(len(pts) - 1, j + 1)
            trozo = pts[a:b + 1]
            largo = sum(metros(trozo[k - 1], trozo[k])
                        for k in range(1, len(trozo)))
            # Un solo punto suelto es ruido del GPS, no un camino que falte.
            if largo >= 30:
                na, nb = nodo_para(trozo[0]), nodo_para(trozo[-1])
                if na != nb:
                    medio = simplifica(trozo, SIMPLIFICA_M)[1:-1]
                    tramos.append((na, nb, CLASE_GRABADO,
                                   int(round(largo)), medio))
                    metidos += 1
                    km += largo / 1000.
            i = j + 1
    print('trozos de tus rutas que OSM no tiene: %d, %.0f km' % (metidos, km))
    return puntos, tramos


def escribe(puntos, tramos, fecha):
    dif = []
    px = py = 0
    for lat, lon in puntos:
        ex, ey = int(round(lat * ESCALA)), int(round(lon * ESCALA))
        dif.append(ex - px)
        dif.append(ey - py)
        px, py = ex, ey
    planos = []
    for a, b, cl, largo, medio in tramos:
        planos.extend((a, b, cl, largo, len(medio)))
        ax = int(round(puntos[a][0] * ESCALA))
        ay = int(round(puntos[a][1] * ESCALA))
        for lat, lon in medio:
            ex, ey = int(round(lat * ESCALA)), int(round(lon * ESCALA))
            planos.append(ex - ax)
            planos.append(ey - ay)
            ax, ay = ex, ey
    salida = os.path.join(ROOT, 'data', 'caminos-zona.json')
    doc = {'bbox': BBOX, 'fecha_osm': fecha, 'escala': ESCALA,
           'nodos': dif, 'tramos': planos}
    with io.open(salida, 'w', encoding='utf-8') as f:
        json.dump(doc, f, separators=(',', ':'))
    print('escrito data/caminos-zona.json: %d cruces, %d tramos, %.0f km, %.0f KB'
          % (len(puntos), len(tramos),
             sum(t[3] for t in tramos) / 1000.,
             os.path.getsize(salida) / 1024.))


def main():
    if len(sys.argv) < 2:
        print('Falta la respuesta de Overpass. Bajala por franjas de 0,02 de')
        print('latitud -la caja entera devuelve 504- con esta consulta:\n')
        print('  ' + CONSULTA + '\n')
        sys.exit(1)
    nodos, vias = lee([x for x in sys.argv[1:] if not x.startswith('--')])
    puntos, tramos = construye(nodos, vias)
    if not tramos:
        sys.exit('No ha salido ningun tramo: revisa la respuesta de Overpass.')
    print('de OpenStreetMap: %d cruces, %d tramos' % (len(puntos), len(tramos)))
    puntos, tramos = suma_lo_grabado(puntos, tramos)
    escribe(puntos, tramos, '')


if __name__ == '__main__':
    main()
