#!/usr/bin/env python3
"""Hace data/cruces-zona.json: los CRUCES de la zona, para el navegador GPS.

    python3 scripts/make_cruces.py <respuesta-de-overpass.json> [mas.json ...]
    python3 scripts/make_cruces.py --fusiona <franja.json>

Sin argumento solo dice la consulta que hay que bajar y se para.

Con --fusiona NO se rehace el fichero entero: se le SUMAN los cruces de las
descargas que se pasen, conservando los que ya estaban. Sirve para ampliar la
caja sin volver a bajarla toda, que son 27 MB y el servidor de Overpass
responde 504 la mitad de las veces. Asi se amplio por el norte hasta 43,42 el
8 de noviembre de 2026, para que la ruta de Lekeitio tuviera cruces: 5,08 km
de sus 32,38 -el 16%, justo la bajada al pueblo- se quedaban fuera.

Por que existe esto. El navegador GPS (trabakutik-gps-pruebas/nuevo.html)
avisaba de los giros deduciendolos del angulo del propio track: si la linea
del GPX se doblaba mas de tantos grados, aviso. Eso no sabe lo que es un
cruce. Medido sobre seis rutas y 105 km con los cruces de OSM delante: de 86
avisos, 29 caian en un cruce real -el 66% eran curvas del camino- y de los 117
cruces de verdad que hay en esas rutas avisaba de 31, se callaba en el 74%. El
autor lo dijo tal cual: "en realidad solo queria que me indicaran los cruces
no las curvas".

Un cruce no se puede deducir de la forma del track. Komoot los canta porque no
sigue un GPX: calcula la ruta sobre los caminos de OpenStreetMap y por tanto
tiene la lista de cruces. Wikiloc no los canta -su ayuda oficial dice que la
app no da indicaciones de voz, y sus avisos son solo salirse de la ruta,
volver, saltarse un tramo, acercarse a un waypoint y llegar al final-. Aqui se
hace lo de Komoot.

Que es un cruce. Un nodo de camino con TRES RAMAS O MAS. Los de dos ramas no
valen: en OSM un camino se parte en dos cada vez que cambia el firme o el
nombre, y esos dos trozos comparten un nodo sin que haya bifurcacion ninguna.
En esta caja hay 245.402 nodos de dos ramas y 17.515 cruces de verdad.

Por que la zona entera y no los cruces de cada ruta. Porque asi vale para
cualquier track, no solo para los 70: si subes un GPX de Wikiloc a la app,
tiene los mismos cruces que una ruta de la web. Ademas los ficheros de ruta no
engordan, que los baja tambien la web y alli los cruces no se usan.

Como se usa. El navegador baja este fichero una vez, lo guarda y se queda con
los cruces que estan pegados al track que lleves cargado. El que avisa o no
es el navegador: avisa del cruce si la ruta gira ahi lo suficiente y se calla
en los que se pasan de largo en recto. Esos umbrales se tocan en nuevo.html
sin volver a pasar este script.

Formato. Las coordenadas van en cienmilesimas de grado (1,1 m) y en
DIFERENCIAS sobre el cruce anterior, ordenados. En pares de grados sueltos el
fichero pesa 338 KB; asi pesa 127 KB, y 49 KB por el cable.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# La misma caja que scripts/osm/LEEME.txt, con sitio de sobra alrededor de las
# rutas. Si alguna ruta se sale, ampliala ahi y aqui y vuelve a bajarlo.
BBOX = [43.10, -2.72, 43.42, -2.34]
RAMAS_MIN = 3
ESCALA = 100000  # cienmilesimas de grado, 1,1 m

CONSULTA = ('[out:json][timeout:600];way["highway"](%.2f,%.2f,%.2f,%.2f);'
            'out skel;>;out skel;' % tuple(BBOX))


def cruces_de(osm):
    """Los nodos de camino con RAMAS_MIN ramas o mas, redondeados."""
    nodos = {}
    vecinos = {}
    for e in osm["elements"]:
        if e["type"] == "node":
            nodos[e["id"]] = (e["lat"], e["lon"])
        elif e["type"] == "way":
            ns = e.get("nodes", [])
            for i, n in enumerate(ns):
                s = vecinos.setdefault(n, set())
                if i > 0:
                    s.add(ns[i - 1])
                if i < len(ns) - 1:
                    s.add(ns[i + 1])
    dos = sum(1 for s in vecinos.values() if len(s) == 2)
    cr = set((round(nodos[n][0], 5), round(nodos[n][1], 5))
             for n, s in vecinos.items()
             if len(s) >= RAMAS_MIN and n in nodos)
    return cr, dos, sum(1 for e in osm["elements"] if e["type"] == "way"), len(nodos)


def ya_guardados():
    """Los cruces que ya estan en data/cruces-zona.json, descifrados."""
    f = os.path.join(ROOT, "data", "cruces-zona.json")
    if not os.path.exists(f):
        return set(), ""
    d = json.load(io.open(f, encoding="utf-8"))
    esc = d.get("escala", ESCALA)
    out = set()
    x = y = 0
    dif = d.get("dif", [])
    for i in range(0, len(dif) - 1, 2):
        x += dif[i]
        y += dif[i + 1]
        out.add((round(x / esc, 5), round(y / esc, 5)))
    return out, d.get("fecha_osm", "")


def escribe(cruces, fecha):
    dif = []
    px = py = 0
    for x, y in sorted(cruces):
        ex, ey = int(round(x * ESCALA)), int(round(y * ESCALA))
        dif.append(ex - px)
        dif.append(ey - py)
        px, py = ex, ey
    salida = os.path.join(ROOT, "data", "cruces-zona.json")
    doc = {"bbox": BBOX, "fecha_osm": fecha, "ramas_min": RAMAS_MIN,
           "escala": ESCALA, "dif": dif}
    with io.open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    print("escrito data/cruces-zona.json: %d cruces, %.0f KB, datos de OSM de %s"
          % (len(cruces), os.path.getsize(salida) / 1024., fecha or "?"))


def main():
    if len(sys.argv) < 2:
        print("Falta la respuesta de Overpass. Bajala asi:\n")
        print("  curl -s --data-urlencode 'data=%s' \\" % CONSULTA)
        print("    https://overpass.kumi.systems/api/interpreter > /tmp/osm.json\n")
        print("y vuelve a pasar:  python3 scripts/make_cruces.py /tmp/osm.json")
        print("\nSon 27 MB y el servidor tarda un par de minutos.")
        sys.exit(1)

    fusiona = "--fusiona" in sys.argv[1:]
    ficheros = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not ficheros:
        sys.exit("Falta el fichero de Overpass.")

    cruces = set()
    fechas = []
    if fusiona:
        cruces, vieja = ya_guardados()
        print("ya guardados: %d cruces (OSM de %s)" % (len(cruces), vieja or "?"))
        if vieja:
            fechas.append(vieja)

    for f in ficheros:
        osm = json.load(io.open(f, encoding="utf-8"))
        nuevos, dos, vias, nodos = cruces_de(osm)
        fecha = osm.get("osm3s", {}).get("timestamp_osm_base", "")
        if fecha:
            fechas.append(fecha)
        antes = len(cruces)
        cruces |= nuevos
        print("%s: %d caminos, %d nodos, %d de dos ramas (no son cruce), "
              "%d cruces -> %d nuevos" % (os.path.basename(f), vias, nodos,
                                          dos, len(nuevos), len(cruces) - antes))

    if not cruces:
        sys.exit("No ha salido ningun cruce: revisa la respuesta de Overpass.")
    # Dos descargas distintas pueden traer datos de fechas distintas: se
    # apuntan las dos, que es la verdad, en vez de fingir una sola.
    escribe(cruces, " y ".join(sorted(set(fechas))))


if __name__ == "__main__":
    main()
