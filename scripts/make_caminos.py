#!/usr/bin/env python3
"""data/caminos.json: la red de caminos de OpenStreetMap de la zona.

La herramienta de dibujar trazados pega los toques del visitante a caminos de
verdad. Hasta ahora los unicos caminos que conocia eran los de las 66 rutas de
la web; con esto puede usar ademas cualquier sendero, pista o calle registrada
en OpenStreetMap alrededor de Mallabia, que es lo que pidio el autor: «que
pueda crear una ruta suya» aprovechando los senderos que hay.

Entra el volcado crudo de Overpass (la consulta esta en scripts/osm/LEEME.txt)
y sale un fichero pequeño: las geometrias simplificadas a SIMPLIFICA_M y
escritas como diferencias entre puntos consecutivos, en centimillonesimas de
grado. 24 MB en bruto se quedan en unos 345 kB comprimidos, que es lo que pesa
hoy data/trailhead.json -- y esto no lo paga quien solo mira el mapa: se baja
al entrar en el modo de dibujar.

  python3 scripts/make_caminos.py <volcado.json>

Datos (c) colaboradores de OpenStreetMap, licencia ODbL.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT / 'data' / 'caminos.json'
ESCALA = 100000          # centimillonesimas de grado: 1,1 m de lado
SIMPLIFICA_M = 4         # el grafo pega a una rejilla de 15 m: mas detalle sobra

# A pie se puede ir por todo lo que hay aqui. En bici no: los escalones no, y
# las aceras solo si alguien ha dicho que si. Las etiquetas de OSM no dan para
# mas -- de las 19.098 vias de la zona solo 512 dicen algo de la bici y 590 del
# pie --, asi que el filtro va por tipo de camino y las etiquetas mandan solo
# cuando existen. No se inventa dificultad: saber si un sendero esta pedregoso
# o embarrado no lo dice ningun dato, y por eso la herramienta tampoco lo dice.
PIE = 1
BICI = 2

NO_BICI = {'steps', 'footway', 'pedestrian'}
SIN_ESCALONES = {'steps'}


def modo(tags):
    h = tags.get('highway')
    acceso = tags.get('access')
    if acceso in ('private', 'no'):
        return 0                      # el camino de la casa de alguien
    m = 0
    if tags.get('foot') != 'no':
        m |= PIE
    bici = tags.get('bicycle')
    if bici in ('yes', 'designated', 'permissive'):
        m |= BICI
    elif bici != 'no' and h not in NO_BICI and h not in SIN_ESCALONES:
        # sac_scale habla de trepar, no de pedalear
        if tags.get('sac_scale') in (None, 'hiking', 'mountain_hiking'):
            m |= BICI
    return m


def simplifica(pts, tol):
    """Douglas-Peucker en metros. Mantiene los extremos, que son los empalmes."""
    if len(pts) < 3:
        return pts
    kx = 111320 * math.cos(math.radians(pts[0][0]))
    ky = 110540

    def lejos(p, a, b):
        ax, ay = (a[1] - p[1]) * kx, (a[0] - p[0]) * ky
        bx, by = (b[1] - p[1]) * kx, (b[0] - p[0]) * ky
        dx, dy = bx - ax, by - ay
        largo = math.hypot(dx, dy)
        if largo < 1e-9:
            return math.hypot(ax, ay)
        return abs(ax * dy - ay * dx) / largo

    guarda = {0, len(pts) - 1}
    pila = [(0, len(pts) - 1)]
    while pila:
        i, j = pila.pop()
        if j - i < 2:
            continue
        corte, peor = -1, tol
        for k in range(i + 1, j):
            d = lejos(pts[k], pts[i], pts[j])
            if d > peor:
                peor, corte = d, k
        if corte > 0:
            guarda.add(corte)
            pila += [(i, corte), (corte, j)]
    return [pts[k] for k in sorted(guarda)]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    crudo = json.loads(Path(sys.argv[1]).read_text())
    vias = []
    fuera = 0
    for w in crudo['elements']:
        tags = w.get('tags', {})
        m = modo(tags)
        if not m:
            fuera += 1
            continue
        g = [(p['lat'], p['lon']) for p in w.get('geometry', [])]
        g = simplifica(g, SIMPLIFICA_M)
        if len(g) < 2:
            continue
        q = [(round(a * ESCALA), round(b * ESCALA)) for a, b in g]
        enc = [m, q[0][0], q[0][1]]
        for k in range(1, len(q)):
            enc.append(q[k][0] - q[k - 1][0])
            enc.append(q[k][1] - q[k - 1][1])
        vias.append(enc)

    datos = {'formato': 1, 'escala': ESCALA, 'vias': vias}
    texto = json.dumps(datos, separators=(',', ':'))
    SALIDA.write_text(texto)
    puntos = sum((len(v) - 1) // 2 for v in vias)
    solopie = sum(1 for v in vias if v[0] == PIE)
    solobici = sum(1 for v in vias if v[0] == BICI)
    print(f'{SALIDA.relative_to(ROOT)}: {len(vias)} vias, {puntos} puntos, '
          f'{len(texto) / 1024:.0f} kB')
    print(f'  descartadas por acceso privado: {fuera}')
    print(f'  solo a pie: {solopie} | solo en bici: {solobici} | las dos: '
          f'{len(vias) - solopie - solobici}')


if __name__ == '__main__':
    main()
