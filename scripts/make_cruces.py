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

Y DESDE NOVIEMBRE DE 2026 VAN TAMBIEN LOS RUMBOS DE LAS RAMAS, en "ramas".
Por que: saber DONDE esta el cruce no basta para decir que hacer en el. El
autor se salio de galdaramiño en el km 2,45, en la salida de la BI-633 encima
de Osma: el ramal arranca casi recto y la que se va hacia un lado es la
carretera, asi que el track se dobla 8-19 grados -lo medido en ventanas de 12,
20, 40 y 60 m- y el navegador, que decidia por la forma del track, se callo.
Con los rumbos de las ramas la cuenta sale sola: llegas con rumbo 263, la
BI-633 sigue a 264 y la ruta coge la rama de 299, o sea que NO coges la rama
mas recta -> "en el cruce, sigue por la derecha". Eso no se puede deducir de
la linea de la ruta por mucho que se afine el umbral.

Y hace falta saber MAS que el rumbo: que ramas son el MISMO camino. La regla
que pidio el autor es "si se continua por el mismo camino no hay perdida,
solo si hay que dejarlo para tomar otro". Por los grados no se distingue: una
carretera que dobla 40 grados en un cruce sigue siendo la misma carretera.

Como van codificadas. Un byte por rama, y nada mas -ni cuentas ni
separadores-, en base64 y en el mismo orden que "dif":

    bits 0-5   el rumbo en pasos de 6 grados (0-59)
    bit 6      esta rama es del MISMO camino que la anterior
    bit 7      ultima rama de este cruce

Las ramas van ordenadas por camino, asi que con el bit 6 se sabe cuales van
juntas sin guardar ningun identificador. Seis grados de resolucion sobran: lo
que se decide con esto son desvios de 25 grados para arriba.
"""
import base64
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# La misma caja que scripts/osm/LEEME.txt, con sitio de sobra alrededor de las
# rutas. Si alguna ruta se sale, ampliala ahi y aqui y vuelve a bajarlo.
BBOX = [43.10, -2.72, 43.42, -2.34]
RAMAS_MIN = 3
ESCALA = 100000  # cienmilesimas de grado, 1,1 m
PASO_RAMA = 6    # grados por paso al guardar el rumbo de una rama

CONSULTA = ('[out:json][timeout:600];way["highway"](%.2f,%.2f,%.2f,%.2f);'
            'out skel;>;out skel;' % tuple(BBOX))


def rumbo(a, b):
    """Rumbo de a a b en grados, 0 al norte."""
    dlon = (b[1] - a[1]) * math.cos(a[0] * math.pi / 180)
    return math.degrees(math.atan2(dlon, b[0] - a[0])) % 360


def cruces_de(osm):
    """Los nodos de camino con RAMAS_MIN ramas o mas, redondeados.

    Devuelve {(lat, lon): [(rumbo en grados, id del camino), ...]}.
    """
    nodos = {}
    vecinos = {}
    for e in osm["elements"]:
        if e["type"] == "node":
            nodos[e["id"]] = (e["lat"], e["lon"])
        elif e["type"] == "way":
            ns = e.get("nodes", [])
            for i, n in enumerate(ns):
                s = vecinos.setdefault(n, [])
                if i > 0:
                    s.append((ns[i - 1], e["id"]))
                if i < len(ns) - 1:
                    s.append((ns[i + 1], e["id"]))
    dos = sum(1 for s in vecinos.values() if len(set(v for v, _ in s)) == 2)
    cr = {}
    for n, vs in vecinos.items():
        if len(set(v for v, _ in vs)) < RAMAS_MIN or n not in nodos:
            continue
        p = nodos[n]
        ramas = []
        visto = set()
        for v, camino in vs:
            if v in nodos and (v, camino) not in visto:
                visto.add((v, camino))
                ramas.append((rumbo(p, nodos[v]), camino))
        if len(ramas) >= RAMAS_MIN:
            cr[(round(p[0], 5), round(p[1], 5))] = ramas
    return cr, dos, sum(1 for e in osm["elements"] if e["type"] == "way"), len(nodos)


def cifra_ramas(cruces):
    """Un byte por rama, y nada mas: ni cuentas ni separadores.

    bits 0-5  el rumbo en pasos de PASO_RAMA (0-59)
    bit 6     esta rama es del MISMO camino que la anterior
    bit 7     ultima rama de este cruce

    Las ramas van ordenadas por camino, asi que el bit 6 basta para saber
    cuales son el mismo camino sin guardar ningun identificador. Eso es lo
    que de verdad hace falta: el aviso salta cuando hay que DEJAR el camino
    por el que vas para coger otro, no por los grados que gires.
    """
    crudo = bytearray()
    for clave in sorted(cruces):
        grupos = agrupa(cruces[clave])
        if not grupos:
            grupos = [[0]]
        plano = []
        for g in grupos:
            for k, r in enumerate(g):
                plano.append((r, k > 0))
        for k, (r, mismo) in enumerate(plano):
            b = r & 63
            if mismo:
                b |= 64
            if k == len(plano) - 1:
                b |= 128
            crudo.append(b)
    return base64.b64encode(bytes(crudo)).decode("ascii")


def agrupa(ramas):
    """Las ramas de un cruce, en pasos de PASO_RAMA y agrupadas por camino.

    Devuelve una lista de grupos; cada grupo es la lista de rumbos de las
    ramas que pertenecen al mismo camino de OSM, ordenadas.
    """
    porcamino = {}
    for grados, camino in ramas:
        paso = int(round(grados / float(PASO_RAMA))) % (360 // PASO_RAMA)
        porcamino.setdefault(camino, set()).add(paso)
    grupos = [sorted(v) for v in porcamino.values()]
    grupos.sort(key=lambda g: g[0])
    return grupos


def descifra_ramas(texto, cuantos):
    """Lo contrario de cifra_ramas: una lista de grupos por cruce."""
    if not texto:
        return [[] for _ in range(cuantos)]
    out = []
    grupos = []
    for b in bytearray(base64.b64decode(texto)):
        if (b & 64) and grupos:
            grupos[-1].append(b & 63)
        else:
            grupos.append([b & 63])
        if b & 128:
            out.append(grupos)
            grupos = []
    if grupos:
        out.append(grupos)
    while len(out) < cuantos:
        out.append([])
    return out


def ya_guardados():
    """Los cruces que ya estan en data/cruces-zona.json, descifrados."""
    f = os.path.join(ROOT, "data", "cruces-zona.json")
    if not os.path.exists(f):
        return {}, ""
    d = json.load(io.open(f, encoding="utf-8"))
    esc = d.get("escala", ESCALA)
    dif = d.get("dif", [])
    claves = []
    x = y = 0
    for i in range(0, len(dif) - 1, 2):
        x += dif[i]
        y += dif[i + 1]
        claves.append((round(x / esc, 5), round(y / esc, 5)))
    ramas = descifra_ramas(d.get("ramas", ""), len(claves))
    out = {}
    for clave, grupos in zip(claves, ramas):
        # Se devuelven como (grados, camino) para poder sumarles descargas
        # nuevas; el "camino" aqui es inventado y solo vale para agrupar.
        out[clave] = [(g * PASO_RAMA, "g%d-%d" % (k, len(grupos)))
                      for k, grupo in enumerate(grupos) for g in grupo]
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
           "escala": ESCALA, "paso_rama": PASO_RAMA, "dif": dif,
           "ramas": cifra_ramas(cruces)}
    with io.open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    total = sum(len(v) for v in cruces.values())
    print("escrito data/cruces-zona.json: %d cruces, %d ramas, %.0f KB, "
          "datos de OSM de %s"
          % (len(cruces), total, os.path.getsize(salida) / 1024., fecha or "?"))


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

    cruces = {}
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
        # Las ramas se SUMAN: una franja puede traer el nodo con parte de sus
        # caminos y la de al lado con el resto.
        for clave, ramas in nuevos.items():
            cruces.setdefault(clave, []).extend(ramas)
        print("%s: %d caminos, %d nodos, %d de dos ramas (no son cruce), "
              "%d cruces -> %d nuevos" % (os.path.basename(f), vias, nodos,
                                          dos, len(nuevos), len(cruces) - antes))

    if not cruces:
        sys.exit("No ha salido ningun cruce: revisa la respuesta de Overpass.")
    # Dos descargas distintas pueden traer datos de fechas distintas: se
    # apuntan las dos, que es la verdad, en vez de fingir una sola. Si todas
    # son del mismo DIA se escribe el dia y ya: bajando la zona por franjas
    # salen una docena de sellos de hora del mismo rato y la linea se hacia
    # ilegible sin decir nada mas.
    marcas = sorted(set(fechas))
    dias = sorted(set(m[:10] for m in marcas if m))
    escribe(cruces, dias[0] if len(dias) == 1 else " y ".join(marcas))


if __name__ == "__main__":
    main()
