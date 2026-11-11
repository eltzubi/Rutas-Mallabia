#!/usr/bin/env python3
"""Comprueba data/caminos-zona.json: que este entero, conectado y que de
verdad cubra las rutas publicadas.

    python3 scripts/check_caminos.py
"""
import io
import json
import math
import os
import glob
import heapq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CERCA_M = 25          # a esta distancia se da por cubierto un punto de ruta
CELDA = 0.0009        # unos 100 m, para la rejilla de busqueda


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
