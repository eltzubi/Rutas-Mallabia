#!/usr/bin/env python3
"""Rehace data/<ruta>.json y data/trailhead.json desde los GPX de verdad.

    python3 scripts/make_map_data.py

El mapa de cada ficha se dibuja con data/<ruta>.json. Esos ficheros se venian
haciendo cogiendo un punto de cada N del GPX, y eso recorta las curvas: con
417 puntos de los 10.382 de karabieta, las revueltas salian como lineas rectas
y el trazado parecia dibujado a mano alzada. En total el sitio pintaba 16.556
puntos de los 427.501 de los GPX: el 4%.

Aqui se usa Douglas-Peucker, que es otra cosa: en vez de contar puntos, mira
cuanto se desvia el dibujo. Conserva todos los que hagan falta en una curva y
tira los de una recta larga, que no aportan nada. Con TOLERANCIA metros de
error maximo el trazado es indistinguible del GPX a cualquier zoom al que se
pueda mirar.

No toca el marcador ni los waypoints de cada fichero: solo los puntos del
track. Es seguro volver a pasarlo.
"""
import glob
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TOLERANCIA = 1.0      # metros, para el mapa de cada ficha
TOLERANCIA_PORTADA = 10.0  # el mapa general lleva las 57 rutas a la vez y se ve muy alejado
DECIMALES = 6


def puntos_gpx(ruta):
    """(lat, lon, altura). La altura va en el tercer sitio porque Leaflet ya
    la admite ahi y porque es lo que necesita el mapa para pintar el track por
    pendiente. Si a algun punto le falta la altura, la ruta se queda sin
    alturas entera: media pendiente inventada es peor que ninguna."""
    puntos = []
    completo = True
    for e in ET.parse(ruta).getroot().iter():
        if not e.tag.endswith('trkpt'):
            continue
        ele = e.find('{*}ele')
        if ele is None or not (ele.text or '').strip():
            completo = False
        puntos.append((float(e.get('lat')), float(e.get('lon')),
                       float(ele.text) if ele is not None and (ele.text or '').strip() else 0.0))
    if not completo:
        puntos = [(a, b, None) for a, b, _ in puntos]
    return puntos


def simplifica(pts, tol):
    """Douglas-Peucker. Devuelve los puntos cuya ausencia moveria la linea
    mas de tol metros."""
    if len(pts) < 3:
        return list(pts)
    lat0 = pts[0][0]
    kx = 111320 * math.cos(math.radians(lat0))
    ky = 111320.0
    guarda = [False] * len(pts)
    guarda[0] = guarda[-1] = True
    pila = [(0, len(pts) - 1)]
    while pila:
        i, j = pila.pop()
        if j <= i + 1:
            continue
        ax, ay = kx * (pts[j][1] - pts[i][1]), ky * (pts[j][0] - pts[i][0])
        largo = math.hypot(ax, ay)
        peor = -1.0
        idx = -1
        for k in range(i + 1, j):
            bx, by = kx * (pts[k][1] - pts[i][1]), ky * (pts[k][0] - pts[i][0])
            d = abs(ax * by - ay * bx) / largo if largo else math.hypot(bx, by)
            if d > peor:
                peor, idx = d, k
        if peor > tol:
            guarda[idx] = True
            pila.append((i, idx))
            pila.append((idx, j))
    return [p for p, g in zip(pts, guarda) if g]


def redondea(pts, con_altura):
    if con_altura:
        return [[round(p[0], DECIMALES), round(p[1], DECIMALES), round(p[2])] for p in pts]
    return [[round(p[0], DECIMALES), round(p[1], DECIMALES)] for p in pts]


def main():
    fichas = 0
    antes = despues = 0
    for destino in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
        slug = os.path.basename(destino)[:-5]
        if slug == 'trailhead':
            continue
        gpx = os.path.join(ROOT, 'src', f'{slug}.gpx')
        if not os.path.exists(gpx):
            print(f'  {slug}: sin GPX, lo dejo como esta')
            continue
        datos = json.load(open(destino))
        if len(datos.get('tracks', [])) != 1:
            print(f'  {slug}: tiene {len(datos.get("tracks", []))} tracks, lo dejo como esta')
            continue
        crudo = puntos_gpx(gpx)
        # La altura solo en el mapa de cada ficha, que es donde se puede
        # pintar la pendiente. En el de la portada son 57 tracks a la vez y
        # nadie mira la pendiente de una ruta desde tan lejos.
        con_altura = all(p[2] is not None for p in crudo)
        nuevos = redondea(simplifica(crudo, TOLERANCIA), con_altura)
        if not con_altura:
            print(f'  {slug}: el GPX no trae todas las alturas, va sin ellas')
        antes += len(datos['tracks'][0]['points'])
        despues += len(nuevos)
        datos['tracks'][0]['points'] = nuevos
        with open(destino, 'w') as f:
            json.dump(datos, f, separators=(', ', ': '))
        fichas += 1
    print(f'{fichas} fichas: {antes} -> {despues} puntos')

    portada = os.path.join(ROOT, 'data', 'trailhead.json')
    datos = json.load(open(portada))
    antes = despues = 0
    for track in datos['tracks']:
        slug = track.get('href', '').replace('.html', '')
        gpx = os.path.join(ROOT, 'src', f'{slug}.gpx')
        if not os.path.exists(gpx):
            continue
        nuevos = redondea(simplifica(puntos_gpx(gpx), TOLERANCIA_PORTADA), False)
        antes += len(track['points'])
        despues += len(nuevos)
        track['points'] = nuevos
    with open(portada, 'w') as f:
        json.dump(datos, f, separators=(', ', ': '))
    print(f'portada: {antes} -> {despues} puntos')


if __name__ == '__main__':
    sys.exit(main())
