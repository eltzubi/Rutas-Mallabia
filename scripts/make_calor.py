#!/usr/bin/env python3
"""data/calor.json: por cuantas rutas pasa cada trozo de camino.

El autor pregunto si se podia poner un mapa de calor «tipo Strava». El de
Strava no se puede -- desde 2018 sus teselas exigen sesion iniciada y sus
condiciones no permiten usarlas fuera de su web --, y ademas dice por donde
pasa la gente, que es un dato que no tenemos. Esto dice otra cosa, con datos
propios: **por cuantas de las 66 rutas de la web pasa cada trozo**. De un
vistazo se ven los caminos que el autor repite una y otra vez frente a los que
ha hecho una sola vez.

No es lo mismo que «por donde se anda mas» y no hay que leerlo asi: un camino
que usan cinco rutas no esta mas pisado que uno que el autor hace cada semana.
Lo que mide es cuanto depende la red de ese camino.

Como se cuenta: cada track se rellena cada RELLENO_M para que no queden huecos,
sus puntos se pegan a una rejilla de CELDA_M y se apunta que esa ruta pasa por
esa celda. Despues, el calor de un punto es **cuantas rutas distintas pasan por
su celda o por alguna de las ocho de alrededor** -- unos 25-35 m de margen, que
es lo que se separan dos grabaciones del mismo camino. Sin ese margen, dos
rutas por la misma pista caen en celdas distintas y el calor sale 1 en las dos.

Sale un nivel por punto, de 1 a 5, y se escribe comprimido por tramos
(«cuatro puntos a nivel 1, nueve a nivel 3...»), que es justo como lo dibuja
el mapa: una linea por tramo, no una por punto.

Los escalones (CORTES) **no son 1, 2, 3, 4+**: con esos, el 58 % de los puntos
caia en el ultimo y el mapa no distinguia nada. Salen del reparto real, que
tiene una cola larguisima -- hay trozos por los que pasan 46 de las 66 rutas --
asi que van en 1 / 2-3 / 4-6 / 7-14 / 15 o mas, que deja entre el 14 y el 25 %
en cada nivel. Si cambia mucho el numero de rutas conviene volver a mirar el
reparto que imprime este script antes de dar los cortes por buenos.

  python3 scripts/make_calor.py

Hay que volver a pasarlo despues de make_map_data.py.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRADA = ROOT / 'data' / 'trailhead.json'
SALIDA = ROOT / 'data' / 'calor.json'

CELDA_M = 25
RELLENO_M = 10
CORTES = (1, 3, 6, 14)  # 1 / 2-3 / 4-6 / 7-14 / 15 o mas
NIVELES = len(CORTES) + 1
LAT0 = 43.2
KX = 111320 * math.cos(math.radians(LAT0))
KY = 110540
PASO_LAT = CELDA_M / KY
PASO_LON = CELDA_M / KX


def celda(lat, lon):
    return (int(math.floor(lat / PASO_LAT)), int(math.floor(lon / PASO_LON)))


def metros(a, b):
    return math.hypot((b[1] - a[1]) * KX, (b[0] - a[0]) * KY)


def celdas_de(puntos):
    """Las celdas por las que pasa un track, rellenando los tramos largos."""
    vistas = set()
    for i in range(len(puntos)):
        vistas.add(celda(*puntos[i]))
        if i == 0:
            continue
        a, b = puntos[i - 1], puntos[i]
        largo = metros(a, b)
        n = int(largo // RELLENO_M)
        for k in range(1, n + 1):
            f = k * RELLENO_M / largo
            vistas.add(celda(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return vistas


def nivel_de(cuantas):
    for i, tope in enumerate(CORTES):
        if cuantas <= tope:
            return i + 1
    return NIVELES


def comprime(niveles):
    """[1,1,3,3,3] -> [[1,2],[3,3]]"""
    tramos = []
    for n in niveles:
        if tramos and tramos[-1][0] == n:
            tramos[-1][1] += 1
        else:
            tramos.append([n, 1])
    return tramos


def main():
    tracks = json.loads(ENTRADA.read_text())['tracks']
    por_celda = {}
    celdas_ruta = []
    for i, t in enumerate(tracks):
        cs = celdas_de(t['points'])
        celdas_ruta.append(cs)
        for c in cs:
            por_celda.setdefault(c, set()).add(i)

    salida = []
    reparto = {n: 0 for n in range(1, NIVELES + 1)}
    for t in tracks:
        niveles = []
        for lat, lon in t['points']:
            cx, cy = celda(lat, lon)
            cerca = set()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cerca |= por_celda.get((cx + dx, cy + dy), set())
            n = nivel_de(max(1, len(cerca)))
            niveles.append(n)
            reparto[n] += 1
        salida.append(comprime(niveles))

    datos = {'niveles': NIVELES, 'cortes': list(CORTES), 'celda': CELDA_M,
             'tramos': salida}
    texto = json.dumps(datos, separators=(',', ':'))
    SALIDA.write_text(texto)
    total = sum(reparto.values())
    print(f'{SALIDA.relative_to(ROOT)}: {len(tracks)} rutas, {total} puntos, '
          f'{len(texto) / 1024:.0f} kB')
    bajo = 1
    for n in range(1, NIVELES + 1):
        if n == NIVELES:
            etq = f'{bajo} o mas'
        elif CORTES[n - 1] == bajo:
            etq = str(bajo)
        else:
            etq = f'{bajo}-{CORTES[n - 1]}'
        print(f'  nivel {n} (por {etq} ruta{"s" if etq != "1" else ""}): '
              f'{reparto[n]:6d} puntos ({100 * reparto[n] / total:4.1f} %)')
        if n < NIVELES:
            bajo = CORTES[n - 1] + 1


if __name__ == '__main__':
    main()
