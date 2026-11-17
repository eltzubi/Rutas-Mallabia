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


# Las rotondas CON LAS CALLES DE ALREDEDOR: hacen falta sus etiquetas (tipo de
# via, sentido unico) y las que desembocan cerca para contar las salidas como
# las cuenta una persona. La caja entera no la aguanta ningun servidor en 60 s:
# se baja en franjas y se pasan todas.
ROTONDAS_CONSULTA = ('[out:json][timeout:55];way["junction"~"roundabout|circular"]'
                     '(%.2f,%.2f,%.2f,%.2f)->.r;way(around.r:30)["highway"];out tags geom;')
ROTONDA_MAX_M = 60  # mas grande no es una rotonda que se cruce de un vistazo
# Lo que no es una boca de calle: por ahi no se sale ni se ve como salida.
NO_ES_CALLE = {"footway", "path", "cycleway", "steps", "pedestrian", "bridleway",
               "corridor", "construction", "proposed", "platform", "elevator",
               "bus_stop"}
BOCA_MARGEN_M = 15   # calles que desembocan a menos de radio+15 m del centro
BOCA_LEJOS_M = 20    # el rumbo de cada boca, medido a radio+20 m del centro
BOCA_MISMA = 10      # dos ramas a menos de 10 grados son la misma boca
BOCA_CALZADAS = 35   # dos calzadas sin nombre, a menos de 35 grados
BOCA_CALZADAS_NOMBRE = 90  # dos calzadas de la misma carretera
BOCA_ENTRADA = 15    # lo mismo que SAL_ENTRADA en el navegador


def _anillo(w):
    j = w.get("tags", {}).get("junction", "")
    return "roundabout" in j or "circular" in j


def _es_calle(w):
    t = w.get("tags", {})
    return (bool(t.get("highway")) and t["highway"] not in NO_ES_CALLE
            and t.get("access") not in ("private", "no")
            and t.get("service") not in ("driveway", "parking_aisle"))


def _m(a, b):
    return math.hypot((a[1] - b[1]) * 111195 * math.cos(math.radians(a[0])),
                      (a[0] - b[0]) * 111195)


def _dif(a, b):
    return abs((a - b + 180) % 360 - 180)


def _pierna(nodos, k, paso, c, lejos):
    """Rumbo, desde el centro, del punto de la pierna a `lejos` m del centro."""
    j, prev = k, nodos[k]
    while 0 <= j + paso < len(nodos):
        j += paso
        p = nodos[j]
        if _m(p, c) >= lejos:
            d0, d1 = _m(prev, c), _m(p, c)
            t = (lejos - d0) / (d1 - d0) if d1 > d0 else 1
            return rumbo(c, (prev[0] + t * (p[0] - prev[0]), prev[1] + t * (p[1] - prev[1])))
        prev = p
    return rumbo(c, prev)


def _sale(w, paso):
    u = w.get("tags", {}).get("oneway", "no")
    if u in ("yes", "1", "true") and paso < 0:
        return False
    if u == "-1" and paso > 0:
        return False
    return True


def rotondas_de(osm):
    """[(lat, lon, radio_m, sentido, [bocas])] de cada anillo.

    LAS BOCAS, desde el 16 de noviembre de 2026. Para decir «toma la segunda
    salida» hay que contar como cuenta una persona, y el autor lo dejo claro en
    la rotonda del km 5 de recyde: la primera calle a la derecha es de
    direccion prohibida, «seria la segunda». Esa calle ni toca el anillo:
    desemboca en la carretera de salida a 13 m de la rotonda. Asi que:
    - cuenta cada BOCA que se ve: las calles pegadas al anillo y las que
      desembocan, a menos de BOCA_MARGEN_M del borde, en una pegada de doble
      sentido; prohibidas incluidas (se marcan: por ahi no se sale, pero se
      cuentan);
    - una carretera de DOS CALZADAS (las dos pegadas al anillo, las dos de
      sentido unico, una de entrada y otra de salida, de la misma carretera)
      es una sola boca, con el rumbo de la de salida;
    - una calle partida en OSM cerca del anillo es una sola boca (dos ramas a
      menos de BOCA_MISMA grados);
    - no son boca los senderos, aceras, bidegorris ni entradas de casas.
    El rumbo de cada boca se mide a BOCA_LEJOS_M del borde, donde la calle ya
    va hacia donde va, y no en el nodo del anillo. El «sentido» es 1 si el
    anillo gira al reves que el reloj (rumbo decreciente; todas las de aqui).
    Los nodos van por sus coordenadas: la consulta usa «out tags geom», que no
    trae los ids, y un nodo compartido tiene las mismas.
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
        for n in w["nodos"]:
            padre.setdefault(n, n)
        for a, b in zip(w["nodos"], w["nodos"][1:]):
            padre[raiz(a)] = raiz(b)
            pares.append((a, b))
    anillos = {}
    for n in padre:
        anillos.setdefault(raiz(n), []).append(n)
    pornodo = {}
    for w in vias.values():
        if _anillo(w) or not _es_calle(w):
            continue
        for k, n in enumerate(w["nodos"]):
            pornodo.setdefault(n, []).append((w, k))
    out = []
    for ns in anillos.values():
        if len(ns) < 3:
            continue
        la = sum(p[0] for p in ns) / len(ns)
        lo = sum(p[1] for p in ns) / len(ns)
        c = (la, lo)
        r = max(_m(p, c) for p in ns)
        if r > ROTONDA_MAX_M:
            continue
        dentro = set(ns)
        kx = math.cos(math.radians(la))
        giro = 0.0
        for a, b in pares:
            if a in dentro and b in dentro:
                ax, ay = (a[1] - lo) * kx, a[0] - la
                bx, by = (b[1] - lo) * kx, b[0] - la
                giro += ax * by - ay * bx
        sentido = 1 if giro > 0 else -1
        lejos = r + BOCA_LEJOS_M
        piernas, pegadas = [], set()
        for n in ns:
            for w, k in pornodo.get(n, []):
                pegadas.add(w["id"])
                for paso in (1, -1):
                    if 0 <= k + paso < len(w["nodos"]):
                        piernas.append((_pierna(w["nodos"], k, paso, c, lejos), _sale(w, paso), w, True))
        unico = lambda x: x.get("tags", {}).get("oneway", "no") in ("yes", "1", "true", "-1")
        # Las calles que desembocan cerca, SOLO en una via de doble sentido
        # pegada al anillo (como la del km 5). En los ramales de entrada o de
        # salida de una carretera de dos calzadas, una calle que desemboca no
        # se ve como una boca mas de la rotonda: sale de la carretera.
        for w in [vias[i] for i in pegadas if not unico(vias[i])]:
            for kk, n in enumerate(w["nodos"]):
                if n in dentro or _m(n, c) > r + BOCA_MARGEN_M:
                    continue
                todas = pornodo.get(n, [])
                otras = [(x, k) for x, k in todas if x["id"] != w["id"] and x["id"] not in pegadas]
                # Un camino partido en dos (extremo de las dos vias) no es boca.
                if (len(otras) == 1 and len(todas) == 2 and kk in (0, len(w["nodos"]) - 1)
                        and otras[0][1] in (0, len(otras[0][0]["nodos"]) - 1)):
                    continue
                for x, k in otras:
                    for paso in (1, -1):
                        if 0 <= k + paso < len(x["nodos"]) and _m(x["nodos"][k + paso], c) > _m(n, c) - 2:
                            piernas.append((_pierna(x["nodos"], k, paso, c, lejos), _sale(x, paso), x, False))
        piernas.sort(key=lambda p: p[0])
        nombre = lambda x: (x.get("tags", {}).get("ref") or "", x.get("tags", {}).get("name") or "")
        # DOS CALZADAS: cada pierna de solo entrada pegada al anillo se junta
        # con la de solo salida pegada mas cercana de la MISMA carretera (la
        # misma pareja referencia-nombre) a menos de BOCA_CALZADAS_NOMBRE grados
        # -las de una nacional llegan separadas hasta 66-; si solo una de las
        # dos lleva nombre, o ninguna, a menos de BOCA_CALZADAS; dos con nombres
        # distintos, nunca.
        usadas, pares_ = set(), []
        for i, (r1, s1, v1, p1) in enumerate(piernas):
            if s1 or not p1 or not unico(v1):
                continue
            mejor, md = None, None
            for j, (r2, s2, v2, p2) in enumerate(piernas):
                if j in usadas or not s2 or not p2 or not unico(v2):
                    continue
                d = _dif(r1, r2)
                tope = BOCA_CALZADAS_NOMBRE if nombre(v1) == nombre(v2) and any(nombre(v1)) else BOCA_CALZADAS
                if nombre(v1) != nombre(v2) and any(nombre(v1)) and any(nombre(v2)):
                    continue
                if d <= tope and (md is None or d < md):
                    mejor, md = j, d
            if mejor is not None:
                usadas.update((i, mejor))
                pares_.append((i, mejor))
        # UNA PAREJA AL REVES: la calzada de salida queda DELANTE de la de
        # entrada en el sentido de giro (con circulacion por la derecha va
        # detras). Entrando por esa carretera, su propia boca se contaria como
        # la primera salida y el numero saldria uno de mas (lo encontro la
        # revision con GPT; 3 de 367 parejas en la zona). Esa rotonda se queda
        # SIN numero: mejor nada que una salida equivocada.
        dudosa = False
        for i, j in pares_:
            tras = ((piernas[i][0] - piernas[j][0]) % 360) if sentido > 0 else ((piernas[j][0] - piernas[i][0]) % 360)
            if BOCA_ENTRADA < tras < 180:
                dudosa = True
        juntas = {}
        for i, j in pares_:
            juntas[i] = j
        bocas = []
        for idx, (rumbo_, sale, via, pegada) in enumerate(piernas):
            if idx in usadas and idx not in juntas:
                continue  # la de salida de un par: va con su entrada
            if idx in juntas:
                rumbo_ = piernas[juntas[idx]][0]   # la boca, donde se SALE
                sale = True
            junta = None
            for b in bocas:
                if _dif(b["r"], rumbo_) <= BOCA_MISMA:
                    junta = b
                    break
            if junta:
                junta["sale"] = junta["sale"] or sale
                junta["n"] += 1
            else:
                bocas.append({"r": rumbo_, "sale": sale, "via": via, "pegada": pegada, "n": 1})
        out.append((la, lo, max(1, int(round(r))), sentido,
                    [] if dudosa else sorted((int(round(b["r"])) % 360, b["sale"]) for b in bocas)))
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
        # Una boca prohibida (por ahi no se sale) va con 360 grados de mas: se
        # cuenta igual, pero la ruta no puede salir por ella.
        sal.append([sentido] + [g if libre else g + 360 for g, libre in salidas])
        px, py = ex, ey
    doc["rotondas"] = plano
    # Una lista por rotonda, en el MISMO orden que "rotondas": el sentido de
    # giro (1 o -1) y el rumbo, desde el centro, de cada boca (+360 si por
    # ella no se puede salir).
    doc["rotondas_salidas"] = sal
    doc["fecha_rotondas"] = max(f for f in fechas if f) if any(fechas) else ""
    with io.open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    print("escrito data/cruces-zona.json: %d rotondas, %d bocas, %.0f KB"
          % (len(rot), sum(len(x[4]) for x in rot), os.path.getsize(salida) / 1024.))


def marca_carreteras():
    """Escribe "cruces_carretera": un bit por cruce (en el orden de "dif") que
    dice si en el sigue una CARRETERA y sale un ramal MENOR.

    Lo pidio el autor el 16 de noviembre de 2026 en el km 6,37 de recyde: el
    navegador dijo «sigue recto por la izquierda» donde la carretera sigue y a
    la izquierda solo esta la entrada a un caserio. «La carretera continua, y
    un ramal a la izquierda no deberia influir en nada.» Con este bit, en esos
    cruces el navegador comprueba en el propio cruce si la ruta va por la
    carretera, y entonces se calla. En las horquillas de dos carreteras (o de
    dos pistas) no se toca nada: ahi el «sigue recto por» si sirve.
    Las clases salen de data/caminos-zona.json (make_caminos.py): 3 carretera
    y 5 nacional son carretera; lo demas, menor.
    """
    import make_caminos as mk
    nodos, tramos, _ = mk.lee_publicado()
    clases = {}
    for a, b, cl, largo, forma in tramos:
        clases.setdefault(a, []).append(cl)
        clases.setdefault(b, []).append(cl)
    cel, rej = 0.0002, {}
    for i, p in enumerate(nodos):
        rej.setdefault((int(p[0] / cel), int(p[1] / cel)), []).append(i)
    salida = os.path.join(ROOT, "data", "cruces-zona.json")
    doc = json.load(io.open(salida, encoding="utf-8"))
    esc, dif = doc.get("escala", ESCALA), doc["dif"]
    bits, x, y, cuantos = bytearray((len(dif) // 2 + 7) // 8), 0, 0, 0
    for k in range(0, len(dif) - 1, 2):
        x += dif[k]
        y += dif[k + 1]
        p = (x / esc, y / esc)
        c0 = (int(p[0] / cel), int(p[1] / cel))
        mejor, md = None, 3.0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for i in rej.get((c0[0] + dx, c0[1] + dy), []):
                    d = _m(p, nodos[i])
                    if d < md:
                        mejor, md = i, d
        cls = clases.get(mejor, []) if mejor is not None else []
        mayor = sum(1 for c in cls if c in (3, 5))
        if mayor >= 2 and mayor < len(cls):
            bits[(k // 2) // 8] |= 1 << ((k // 2) % 8)
            cuantos += 1
    doc["cruces_carretera"] = base64.b64encode(bytes(bits)).decode("ascii")
    with io.open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, separators=(",", ":"))
    print("escrito data/cruces-zona.json: %d cruces de carretera con un ramal menor, de %d"
          % (cuantos, len(dif) // 2))


def main():
    if "--carreteras" in sys.argv[1:]:
        marca_carreteras()
        return
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
