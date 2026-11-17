#!/usr/bin/env python3
"""data/cruces-zona.json con las ramas agrupadas por CALLE y la forma real de
cada rama (17 de noviembre de 2026).

    python3 scripts/make_cruces_calles.py <salida.json> <base-cruces.json> w_*.json
    python3 scripts/make_cruces.py --rotondas <rotondas.json ...>
    python3 scripts/make_cruces.py --carreteras

Los w_*.json son respuestas de Overpass con TODAS las vias de un recuadro y su
geometria con los nodos (out body geom):

    [out:json][timeout:55];way["highway"](S,O,N,E);out body geom;

El nombre del fichero dice el recuadro: w_<S>_<O>.json (0,02 x 0,0475 grados),
w_q_<S>_<O>.json (la cuarta parte) o w_t_<S>_<O>_<N>_<E>.json (el que sea). Se
bajaron en trozos porque el espejo de Overpass que respondia
(maps.mail.ru/osm/tools/overpass) corta a los 60 s.

Por que: el autor oyo «cruce a la izquierda» donde la carretera solo tuerce
(el fronton de Eltzubi) y en cambio en otros sitios igual de curvos SI queria
el aviso (recyde 4,49 y 14,79). Con las ramas de antes -solo su rumbo en el
primer nodo, agrupadas por via de OSM- no se podian separar. Ahora cada rama
lleva su CALLE (ref o nombre; sin nombre, la via y su continuacion en linea
del mismo tipo), un punto a 25 m por su propia geometria (ramas_lejos) y su
clase (ramas_clase: 1 carretera, 2 calle, 0 camino). El navegador reconoce asi
por que rama llegas y por cual sales, y si sigues la MISMA via que tuerce dice
«sigue la carretera a la izquierda» en vez de «cruce a la izquierda».

Dentro de los recuadros bajados (con 40 m de margen) los cruces se rehacen;
fuera se copian del fichero base tal cual, sin forma ni clase, y alli el
navegador decide como siempre.
"""
import sys, json, glob, math, base64

ESCALA = 100000
PASO = 6
LEJOS_M = 25.0


def m(a, b):
    return math.hypot((b[1] - a[1]) * 111195 * math.cos(math.radians(a[0])), (b[0] - a[0]) * 111195)


def rumbo(a, b):
    return math.degrees(math.atan2((b[1] - a[1]) * math.cos(math.radians(a[0])), b[0] - a[0])) % 360


def dif(a, b):
    return abs((a - b + 180) % 360 - 180)


def carga(ficheros):
    vias, coord = {}, {}
    for f in ficheros:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for e in d.get("elements", []):
            if e.get("type") != "way" or not e.get("geometry") or not e.get("nodes"):
                continue
            if len(e["nodes"]) != len(e["geometry"]):
                continue
            vias[e["id"]] = e
            for n, g in zip(e["nodes"], e["geometry"]):
                if g:
                    coord[n] = (g["lat"], g["lon"])
    return vias, coord


def clave_calle(w):
    t = w.get("tags", {})
    if t.get("ref"):
        return "r:" + t["ref"]
    if t.get("name"):
        return "n:" + t["name"]
    return None


CARRETERA = {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified",
             "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"}
CALLE = {"residential", "living_street", "pedestrian"}


def clase_de(w):
    """1 carretera, 2 calle, 0 camino (pista, sendero, servicio...)."""
    h = w.get("tags", {}).get("highway")
    return 1 if h in CARRETERA else 2 if h in CALLE else 0


def cubierto(p, celdas):
    """Dentro de alguna celda bajada, con 40 m de margen hacia dentro."""
    mla, mlo = 40 / 111195.0, 40 / (111195.0 * math.cos(math.radians(p[0])))
    return any(a + mla <= p[0] <= b - mla and c + mlo <= p[1] <= d - mlo for a, b, c, d in celdas)


def celdas_de(ficheros):
    import os
    out = []
    for f in ficheros:
        n = os.path.basename(f)[2:-5].split("_")
        if n[0] == "t":
            out.append((float(n[1]), float(n[3]), float(n[2]), float(n[4])))
        elif n[0] == "q":
            la, lo = float(n[1]), float(n[2]); out.append((la, la + 0.01, lo, lo + 0.02375))
        else:
            la, lo = float(n[0]), float(n[1]); out.append((la, la + 0.02, lo, lo + 0.0475))
    return out


def viejos(base):
    """Los cruces del fichero publicado: {clave: [(paso, mismo), ...]}."""
    doc = json.load(open(base))
    esc, dif, raw = doc.get("escala", ESCALA), doc["dif"], base64.b64decode(doc["ramas"])
    out, x, y, o = {}, 0, 0, 0
    for k in range(0, len(dif) - 1, 2):
        x += dif[k]; y += dif[k + 1]
        lst = []
        while o < len(raw):
            b = raw[o]; o += 1
            lst.append((b & 63, bool(b & 64)))
            if b & 128:
                break
        out[(round(x / esc, 5), round(y / esc, 5))] = lst
    return out


def main():
    salida, base = sys.argv[1], sys.argv[2]
    vias, coord = carga(sys.argv[3:])
    print("vias", len(vias), "nodos", len(coord))
    pornodo = {}
    for w in vias.values():
        ns = w["nodes"]
        for k, n in enumerate(ns):
            pornodo.setdefault(n, []).append((w, k))

    def pierna_lejos(w, k, paso):
        """Punto a LEJOS_M m siguiendo la via; si se acaba, sigue por la via que
        continua en su extremo con la misma calle (o, sin nombre, del mismo
        tipo y casi en linea)."""
        pts = [coord[w["nodes"][k]]]
        rec = 0.0
        visto = {w["id"]}
        clave = clave_calle(w)
        tipo = w.get("tags", {}).get("highway")
        while True:
            ns = w["nodes"]
            j = k
            while 0 <= j + paso < len(ns):
                a, b = coord.get(ns[j]), coord.get(ns[j + paso])
                if a is None or b is None:
                    return pts[-1]
                d = m(a, b)
                if rec + d >= LEJOS_M:
                    t = (LEJOS_M - rec) / d
                    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                rec += d
                pts.append(b)
                j += paso
            # al final de la via: buscar la continuacion
            fin = ns[j]
            if len(pts) < 2:
                return pts[-1]
            r0 = rumbo(pts[-2], pts[-1])
            mejor = None
            md = 60
            for w2, k2 in pornodo.get(fin, []):
                if w2["id"] in visto:
                    continue
                c2 = clave_calle(w2)
                if clave is not None and c2 != clave:
                    continue
                if clave is None and (c2 is not None or w2.get("tags", {}).get("highway") != tipo):
                    continue
                for p2 in (1, -1):
                    if 0 <= k2 + p2 < len(w2["nodes"]) and coord.get(w2["nodes"][k2 + p2]):
                        dd = dif(rumbo(coord[fin], coord[w2["nodes"][k2 + p2]]), r0)
                        if dd < md:
                            md, mejor = dd, (w2, k2, p2)
            if mejor is None:
                return pts[-1]
            w, k, paso = mejor
            visto.add(w["id"])

    cruces = {}
    for n, lst in pornodo.items():
        if n not in coord:
            continue
        vecinos = set()
        piernas = []
        for w, k in lst:
            for paso in (1, -1):
                j = k + paso
                if 0 <= j < len(w["nodes"]) and w["nodes"][j] in coord:
                    # Una pierna por nodo vecino: dos vias encima de la misma
                    # geometria no son dos ramas (revision con GPT).
                    if w["nodes"][j] in vecinos:
                        continue
                    vecinos.add(w["nodes"][j])
                    piernas.append((w, k, paso))
        if len(vecinos) < 3:
            continue
        p = coord[n]
        ramas = []
        for w, k, paso in piernas:
            r = rumbo(p, coord[w["nodes"][k + paso]])
            lej = pierna_lejos(w, k, paso)
            ramas.append({"r": r, "w": w, "lejos": lej, "extremo": k in (0, len(w["nodes"]) - 1), "clase": clase_de(w)})
        # LA CALLE de cada rama: ref o nombre; sin nombre, la via, y dos vias sin
        # nombre del mismo tipo que se continuan casi en linea son la misma.
        for x in ramas:
            x["calle"] = clave_calle(x["w"]) or ("w:%d" % x["w"]["id"])
        sin = [x for x in ramas if clave_calle(x["w"]) is None and x["extremo"]]
        for i, a in enumerate(sin):
            for b in sin[i + 1:]:
                if a["w"]["id"] != b["w"]["id"] and a["w"].get("tags", {}).get("highway") == b["w"].get("tags", {}).get("highway") and dif(a["r"], b["r"]) >= 150:
                    nuevo = a["calle"]
                    viejo = b["calle"]
                    for x in ramas:
                        if x["calle"] == viejo:
                            x["calle"] = nuevo
        # Una calle es UN PAR de piernas casi opuestas. Si con el mismo nombre
        # salen mas de dos (una horquilla de dos ramas que se llaman igual), se
        # queda en la calle el par mas opuesto y las demas van sueltas.
        porcalle = {}
        for x in ramas:
            porcalle.setdefault(x["calle"], []).append(x)
        for cl, lst in porcalle.items():
            if len(lst) <= 2:
                continue
            par = max(((u, v) for i, u in enumerate(lst) for v in lst[i + 1:]), key=lambda uv: dif(uv[0]["r"], uv[1]["r"]))
            # Si ni el par mas opuesto lo es (una horquilla de dos ramas con el
            # mismo nombre), no hay calle que siga: todas sueltas.
            if dif(par[0]["r"], par[1]["r"]) < 120:
                par = ()
            for k, x in enumerate(lst):
                if x not in par:
                    x["calle"] = cl + "#%d" % k
        clave = (round(p[0], 5), round(p[1], 5))
        cruces[clave] = ramas

    celdas = celdas_de(sys.argv[3:])
    nuevos = {k: v for k, v in cruces.items() if cubierto(k, celdas)}
    antes = viejos(base)
    guardados = {k: v for k, v in antes.items() if not cubierto(k, celdas)}
    print("nuevos dentro", len(nuevos), "viejos fuera", len(guardados), "viejos dentro descartados", len(antes) - len(guardados))
    cruces = nuevos
    # codificar en el formato de siempre + ramas_lejos y ramas_clase alineados
    crudo = bytearray()
    lejos = bytearray()
    dif_ = []
    px = py = 0
    total = 0
    clases = bytearray()
    con_forma = []
    todas = sorted(set(cruces) | set(guardados))
    for clave in todas:
        if clave in guardados:
            ex, ey = int(round(clave[0] * ESCALA)), int(round(clave[1] * ESCALA))
            dif_ += [ex - px, ey - py]
            px, py = ex, ey
            lst = guardados[clave]
            for idx, (paso, mismo) in enumerate(lst):
                crudo.append((paso & 63) | (64 if mismo else 0) | (128 if idx == len(lst) - 1 else 0))
                clases.append(0); total += 1
            con_forma.append(0)
            continue
        con_forma.append(1)
        ex, ey = int(round(clave[0] * ESCALA)), int(round(clave[1] * ESCALA))
        dif_ += [ex - px, ey - py]
        px, py = ex, ey
        grupos = {}
        for x in cruces[clave]:
            paso = int(round(x["r"] / PASO)) % (360 // PASO)
            g = grupos.setdefault(x["calle"], {})
            if paso not in g:
                g[paso] = (x["lejos"], x["clase"])
        orden = sorted(grupos.values(), key=lambda g: min(g))
        plano = []
        for g in orden:
            for kk, paso in enumerate(sorted(g)):
                plano.append((paso, kk > 0, g[paso]))
        for idx, (paso, mismo, (lej, cl)) in enumerate(plano):
            clases.append(cl)
            b = paso & 63
            if mismo:
                b |= 64
            if idx == len(plano) - 1:
                b |= 128
            crudo.append(b)
            dla = round((lej[0] - clave[0]) * ESCALA)
            dlo = round((lej[1] - clave[1]) * ESCALA)
            if -127 <= dla <= 127 and -127 <= dlo <= 127 and (dla or dlo):
                lejos += bytes([dla & 255, dlo & 255])
            else:
                lejos += bytes([0, 0])
            total += 1
    doc = json.load(open(base))
    import datetime
    doc["fecha_osm"] = datetime.date.today().isoformat()
    doc["dif"] = dif_
    doc["ramas"] = base64.b64encode(bytes(crudo)).decode("ascii")
    # COMPACTO (el navegador lo guarda en el movil, junto a las rutas del
    # autor): la forma solo de los cruces que la tienen, marcados con un bit
    # por cruce en «ramas_con_forma»; la clase en 2 bits por rama, 4 por byte.
    bits = bytearray((len(con_forma) + 7) // 8)
    for i, b in enumerate(con_forma):
        if b:
            bits[i >> 3] |= 1 << (i & 7)
    cl = bytearray((len(clases) + 3) // 4)
    for i, c in enumerate(clases):
        cl[i >> 2] |= (c & 3) << ((i & 3) * 2)
    doc["ramas_con_forma"] = base64.b64encode(bytes(bits)).decode("ascii")
    doc["ramas_lejos"] = base64.b64encode(bytes(lejos)).decode("ascii")
    doc["ramas_clase2"] = base64.b64encode(bytes(cl)).decode("ascii")
    doc.pop("ramas_clase", None)
    doc.pop("cruces_carretera", None)
    json.dump(doc, open(salida, "w"), separators=(",", ":"))
    print("cruces", len(todas), "ramas", total)


if __name__ == "__main__":
    main()
