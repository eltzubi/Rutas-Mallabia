#!/usr/bin/env python3
"""Hace data/cruces-zona.json: los CRUCES de la zona, para el navegador GPS.

    python3 scripts/make_cruces.py <respuesta-de-overpass.json> [mas.json ...]
    python3 scripts/make_cruces.py --fusiona <franja.json>
    python3 scripts/make_cruces.py --rotondas <rotondas-de-overpass.json>

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

LAS ROTONDAS, desde el 15 de noviembre de 2026, en "rotondas". El autor
cruzo una rotonda siguiendo recto y el navegador le dijo «gira a la derecha»
(y a la derecha habia una calle de direccion prohibida). La causa: en OSM la
entrada y la salida de una rotonda son dos cruces, y cada uno, visto suelto,
es un giro de 50-90 grados. Simulado sobre las rotondas de la zona con sus
ramas reales: de 3.824 pasos siguiendo recto, en 3.473 se decia algun giro.
Con la rotonda marcada, el navegador la trata como UN cruce: compara el rumbo
con el que entras y con el que sales.

    "rotondas": [dlat, dlon, radio, dlat, dlon, radio, ...]

el centro en cienmilesimas de grado y en diferencias sobre el anterior, como
"dif", y el radio en metros enteros (el nodo del anillo mas alejado del
centro). Salen de way["junction"~"roundabout|circular"]; un anillo partido en
varios caminos se junta por los nodos que comparten. --rotondas reescribe solo
este campo y deja el resto del fichero como esta.

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


# Las rotondas CON LOS CAMINOS QUE LLEGAN A ELLAS: hacen falta sus etiquetas
# (tipo de via y sentido unico) para contar las salidas. La caja entera no la
# aguanta ningun servidor en 60 s: se baja en franjas y se pasan todas.
ROTONDAS_CONSULTA = ('[out:json][timeout:55];way["junction"~"roundabout|circular"]'
                     '(%.2f,%.2f,%.2f,%.2f);node(w);way(bn)["highway"];out tags geom;')
ROTONDA_MAX_M = 60  # mas grande no es una rotonda que se cruce de un vistazo
# Por donde un coche no sale de una rotonda: no cuentan como salida.
SIN_SALIDA = {"footway", "path", "cycleway", "steps", "pedestrian", "bridleway",
              "corridor", "construction", "proposed", "platform", "elevator",
              "bus_stop"}


def _anillo(w):
    j = w.get("tags", {}).get("junction", "")
    return "roundabout" in j or "circular" in j


def rotondas_de(osm):
    """[(lat, lon, radio_m, sentido, [rumbos de las salidas])] de cada anillo.

    LAS SALIDAS, desde el 16 de noviembre de 2026. El autor: «la primera
    salida, a la derecha, si la detecta; pero si es la segunda no sabe». Para
    decir «toma la segunda salida» hay que contarlas, y contar las ramas a
    ciegas falla: una carretera de dos calzadas llega con DOS ramas, una solo
    de entrada y otra solo de salida, y se contaria dos veces. Por eso:
    - se cuentan solo las vias por las que se puede SALIR (sentido unico
      hacia el anillo no; oneway=-1 al reves);
    - no cuentan senderos, aceras, bidegorris ni entradas de casas. Las
      PISTAS si: andando o en bici una pista que sale de la rotonda se ve y se
      cuenta como una salida mas.
    Cada salida se guarda como el rumbo del CENTRO al nodo donde sale. El
    «sentido» es 1 si el anillo gira al reves que el reloj (rumbo decreciente,
    el de todas las de aqui) y -1 si no; sale del orden de los nodos del
    anillo, que en OSM va en el sentido de la circulacion.
    Los nodos se identifican por sus coordenadas: la consulta usa «out tags
    geom», que no trae los ids, y un nodo compartido tiene las mismas.
    """
    vias = {}
    for w in osm["elements"]:
        if w.get("type") == "way" and w.get("geometry"):
            w = dict(w)
            w["nodos"] = [(round(g["lat"], 7), round(g["lon"], 7)) for g in w["geometry"]]
            vias[w["id"]] = w
    padre = {}

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    pares = []
    for w in vias.values():
        if not _anillo(w):
            continue
        ns = w["nodos"]
        for n in ns:
            padre.setdefault(n, n)
        for a, b in zip(ns, ns[1:]):
            padre[raiz(a)] = raiz(b)
            pares.append((a, b))
    anillos = {}
    for n in padre:
        anillos.setdefault(raiz(n), []).append(n)
    toca = {}
    for w in vias.values():
        if _anillo(w):
            continue
        for k, n in enumerate(w["nodos"]):
            if n in padre:
                toca.setdefault(n, []).append((w, k))
    out = []
    for ns in anillos.values():
        if len(ns) < 3:
            continue
        la = sum(p[0] for p in ns) / len(ns)
        lo = sum(p[1] for p in ns) / len(ns)
        k = math.cos(math.radians(la))
        r = max(math.hypot((p[0] - la) * 111195, (p[1] - lo) * 111195 * k) for p in ns)
        if r > ROTONDA_MAX_M:
            continue
        dentro = set(ns)
        giro = 0.0
        for a, b in pares:
            if a in dentro and b in dentro:
                ax, ay = (a[1] - lo) * k, a[0] - la
                bx, by = (b[1] - lo) * k, b[0] - la
                giro += ax * by - ay * bx
        sentido = 1 if giro > 0 else -1
        salidas = []
        for n in ns:
            for w, i in toca.get(n, []):
                t = w.get("tags", {})
                if (t.get("highway", "") in SIN_SALIDA or t.get("access") in ("private", "no")
                        or t.get("service") in ("driveway", "parking_aisle")):
                    continue
                unico = t.get("oneway", "no")
                for paso in (1, -1):
                    j = i + paso
                    if j < 0 or j >= len(w["nodos"]):
                        continue
                    if unico in ("yes", "1", "true") and paso < 0:
                        continue
                    if unico == "-1" and paso > 0:
                        continue
                    salidas.append(int(round(rumbo((la, lo), n))) % 360)
        out.append((la, lo, max(1, int(round(r))), sentido, sorted(salidas)))
    return sorted(out)


def escribe_rotondas(ficheros):
    elementos, vistos, fechas = [], set(), []
    for f in ficheros:
        osm = json.load(io.open(f, encoding="utf-8"))
        fechas.append(osm.get("osm3s", {}).get("timestamp_osm_base", "")[:10])
        for e in osm.get("elements", []):
            if (e.get("type"), e.get("id")) not in vistos:
                vistos.add((e.get("type"), e.get("id")))
                elementos.append(e)
    rot = rotondas_de({"elements": elementos})
    if not rot:
        sys.exit("No ha salido ninguna rotonda: revisa las respuestas de Overpass.")
    salida = os.path.join(ROOT, "data", "cruces-zona.json")
    doc = json.load(io.open(salida, encoding="utf-8"))
    plano, sal, px, py = [], [], 0, 0
    for la, lo, r, sentido, salidas in rot:
        ex, ey = int(round(la * ESCALA)), int(round(lo * ESCALA))
        plano += [ex - px, ey - py, r]
        sal.append([sentido] + salidas)
        px, py = ex, ey
    doc["rotondas"] = plano
    # Una lista por rotonda, en el MISMO orden que "rotondas": el sentido de
    # giro (1 o -1) y los rumbos, desde el centro, de los nodos por los que se
    # puede salir.
    doc["rotondas_salidas"] = sal
    doc["fecha_rotondas"] = max(f for f in fechas if f) if any(fechas) else ""
    with io.open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    print("escrito data/cruces-zona.json: %d rotondas, %d salidas, %.0f KB"
          % (len(rot), sum(len(x[4]) for x in rot), os.path.getsize(salida) / 1024.))


def main():
    if "--rotondas" in sys.argv[1:]:
        f = [x for x in sys.argv[1:] if not x.startswith("--")]
        if not f:
            print("Bajalas en franjas (la caja entera no cabe en 60 s), por ejemplo:\n")
            print("  curl -s --data-urlencode 'data=%s' \\" % (ROTONDAS_CONSULTA % (43.10, -2.72, 43.14, -2.625)))
            print("    https://maps.mail.ru/osm/tools/overpass/api/interpreter > /tmp/rf_0.json")
            print("\ny luego: python3 scripts/make_cruces.py --rotondas /tmp/rf_*.json")
            sys.exit(1)
        escribe_rotondas(f)
        return
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
