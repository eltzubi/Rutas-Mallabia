#!/usr/bin/env python3
"""Comprueba data/caminos-zona.json: que este entero, conectado y que de
verdad cubra las rutas publicadas.

    python3 scripts/check_caminos.py
"""
import io
import json
import math
import sys
import os
import glob
import heapq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CERCA_M = 25          # a esta distancia se da por cubierto un punto de ruta
CELDA = 0.0009        # unos 100 m, para la rejilla de busqueda


CLASE_GRABADO = 7
DE_VERDAD_M = 40      # lo mismo que en make_caminos.py
# Pero aqui se mira con 5 m de margen. make_caminos.py mide sobre el trozo
# grabado entero; en el fichero solo queda la forma simplificada a 8 m y
# redondeada a 1,1 m, y un trozo guardado como una recta ha perdido su
# curvatura. Los dos no pueden dar el mismo numero al metro: esto caza las
# copias de verdad, no las que se quedan a un metro del liston.
MARGEN_M = 5


def metros(a, b):
    dy = (b[0] - a[0]) * 111195.0
    dx = (b[1] - a[1]) * 111195.0 * math.cos((a[0] + b[0]) / 2 * math.pi / 180)
    return math.hypot(dx, dy)


def carga():
    d = json.load(io.open(os.path.join(ROOT, 'data', 'caminos-zona.json'),
                          encoding='utf-8'))
    esc = d['escala']
    nodos = []
    x = y = 0
    dif = d['nodos']
    for i in range(0, len(dif), 2):
        x += dif[i]
        y += dif[i + 1]
        nodos.append((x / esc, y / esc))
    tramos = []
    t = d['tramos']
    i = 0
    while i < len(t):
        a, b, cl, largo, k = t[i], t[i + 1], t[i + 2], t[i + 3], t[i + 4]
        i += 5
        forma = []
        ax = int(round(nodos[a][0] * esc))
        ay = int(round(nodos[a][1] * esc))
        for _ in range(k):
            ax += t[i]
            ay += t[i + 1]
            i += 2
            forma.append((ax / esc, ay / esc))
        tramos.append((a, b, cl, largo, forma))
    return d, nodos, tramos


def componentes(n, tramos):
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for a, b, _, _, _ in tramos:
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            padre[ra] = rb
    cuenta = {}
    for i in range(n):
        r = raiz(i)
        cuenta[r] = cuenta.get(r, 0) + 1
    return sorted(cuenta.values(), reverse=True)


def main():
    d, nodos, tramos = carga()
    print('caminos-zona.json: %d cruces, %d tramos, %.0f km'
          % (len(nodos), len(tramos), sum(t[3] for t in tramos) / 1000.))
    comp = componentes(len(nodos), tramos)
    print('trozos sueltos: %d · el mayor tiene %d cruces (%.1f%%)'
          % (len(comp), comp[0], comp[0] * 100.0 / len(nodos)))

    # NINGUN TROZO GRABADO PUEDE SER UNA COPIA DE UN CAMINO QUE YA ESTA.
    # Los trozos de las rutas que OSM no tiene (clase 7) se añaden para que el
    # lapiz pueda ir por donde el autor anda. Pero si uno de ellos no se
    # separa nunca de un camino de OSM, no es un camino que falte: es el
    # mismo camino con el error del GPS, y entonces el lapiz tiene DOS lineas
    # paralelas para un solo camino y puede coger la falsa -la linea sale
    # junto al camino en vez de por el camino-. Llego a haber 96 asi.
    osm = [t for t in tramos if t[2] != CLASE_GRABADO]
    mios = [t for t in tramos if t[2] == CLASE_GRABADO]
    rosm = {}
    for a, b, cl, largo, forma in osm:
        pts = [nodos[a]] + forma + [nodos[b]]
        for k in range(len(pts)):
            q = pts[k]
            rosm.setdefault((math.floor(q[0] / CELDA), math.floor(q[1] / CELDA)),
                            []).append(q)
            if k:
                r = pts[k - 1]
                d2 = metros(r, q)
                for j in range(1, int(d2 // 20) + 1):
                    f = j * 20.0 / d2
                    m = (r[0] + (q[0] - r[0]) * f, r[1] + (q[1] - r[1]) * f)
                    rosm.setdefault((math.floor(m[0] / CELDA),
                                     math.floor(m[1] / CELDA)), []).append(m)

    def lejos_de_osm(q):
        k0, k1 = math.floor(q[0] / CELDA), math.floor(q[1] / CELDA)
        mejor = 1e9
        for u in (-1, 0, 1):
            for v2 in (-1, 0, 1):
                for r in rosm.get((k0 + u, k1 + v2), ()):
                    dd = metros(q, r)
                    if dd < mejor:
                        mejor = dd
        return mejor

    copias = []
    for a, b, cl, largo, forma in mios:
        # El interior, no los extremos: esos estan pegados a la red a
        # proposito y siempre caen cerca de un camino.
        # Sin forma propia -una recta entre dos cruces- se mira su punto
        # de en medio, que es lo que mira tambien make_caminos.py.
        dentro = forma or [((nodos[a][0] + nodos[b][0]) / 2.0,
                            (nodos[a][1] + nodos[b][1]) / 2.0)]
        if max(lejos_de_osm(q) for q in dentro) < DE_VERDAD_M - MARGEN_M:
            copias.append(largo)
    print('trozos tuyos: %d, %.0f km · copias de un camino de OSM: %d'
          % (len(mios), sum(t[3] for t in mios) / 1000., len(copias)))
    if copias:
        print('FALLO: %d trozos de clase %d no se separan nunca %d m de un '
              'camino de OpenStreetMap (%.1f km). Son el mismo camino con el '
              'error del GPS, y el lapiz puede dibujar por la copia.'
              % (len(copias), CLASE_GRABADO, DE_VERDAD_M - MARGEN_M,
                 sum(copias) / 1000.))
        sys.exit(1)

    # Todos los puntos de la red -cruces y formas- en una rejilla.
    rej = {}
    def mete(p):
        rej.setdefault((math.floor(p[0] / CELDA), math.floor(p[1] / CELDA)),
                       []).append(p)
    for p in nodos:
        mete(p)
    for a, b, cl, largo, forma in tramos:
        for p in forma:
            mete(p)
        # Un tramo recto y largo no tiene puntos en medio: se rellena cada
        # 20 m, o un punto de ruta a su lado contaria como no cubierto.
        pts = [nodos[a]] + forma + [nodos[b]]
        for k in range(1, len(pts)):
            p, q = pts[k - 1], pts[k]
            largo_t = metros(p, q)
            pasos = int(largo_t // 20)
            for j in range(1, pasos + 1):
                f = j * 20.0 / largo_t
                mete((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))

    def cerca(p):
        k0 = math.floor(p[0] / CELDA)
        k1 = math.floor(p[1] / CELDA)
        mejor = 1e9
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for q in rej.get((k0 + a, k1 + b), ()):
                    dd = metros(p, q)
                    if dd < mejor:
                        mejor = dd
        return mejor

    total = cubiertos = 0
    peores = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
        n = os.path.basename(f)[:-5]
        if n in ('trailhead', 'alturas', 'rutas', 'cruces-zona', 'caminos-zona'):
            continue
        try:
            dd = json.load(io.open(f, encoding='utf-8'))
        except Exception:
            continue
        tr = (dd.get('tracks') or [None])[0]
        if not tr or len(tr.get('points') or []) < 3:
            continue
        pts = [(p[0], p[1]) for p in tr['points']]
        dentro = sum(1 for p in pts if cerca(p) <= CERCA_M)
        total += len(pts)
        cubiertos += dentro
        peores.append((dentro * 100.0 / len(pts), n, len(pts)))
    peores.sort()
    print('\ncobertura de las rutas publicadas (a %d m de un camino de OSM):'
          % CERCA_M)
    print('  %d de %d puntos, el %.1f%%' % (cubiertos, total,
                                            cubiertos * 100.0 / max(1, total)))
    print('  las cinco peor cubiertas:')
    for pct, n, k in peores[:5]:
        print('    %-26s %5.1f%% de %d puntos' % (n, pct, k))


if __name__ == '__main__':
    main()
