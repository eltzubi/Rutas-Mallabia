#!/usr/bin/env python3
"""Los cruces de TODA EUSKADI, en cuadrados de 0,1 grados (22 de noviembre de 2026).

    pip install osmium
    curl -O https://download.openstreetmap.fr/extracts/europe/spain/euskadi-latest.osm.pbf
    python3 scripts/make_cruces_euskadi.py euskadi-latest.osm.pbf

Escribe data/cruces/t_<lat*10>_<lon*10>.json (uno por cuadrado, el mismo formato
que data/cruces-zona.json) y data/cruces/indice.json con la lista. El navegador
baja solo los cuadrados que toca la ruta que se carga.

Por que: el autor hizo una ruta en Gorbeia (Otzarreta y Uguna), fuera de la zona
de Mallabia que cubre cruces-zona.json, y el navegador no le aviso de ningun
cruce: alli solo sabia de las curvas del trazado. «¿Puedes bajarte de toda
Euskadi?». Un fichero unico de Euskadi serian unos 6 MB, que no caben en el
almacenamiento de la pagina y tardan en bajar en el monte: por eso en cuadrados.

Cada cuadrado se calcula con las vias de un margen de MARGEN grados alrededor,
para que un cruce del borde vea sus ramas enteras (su punto a 25 m, si es una
entrada sin salida), y se guardan solo los cruces de dentro. Mismo calculo que
make_cruces_calles.py (calcula_cruces y codifica), mismas rotondas que
make_cruces.py (rotondas_de).

El extracto es de Geofabrik/OpenStreetMap France (datos (c) colaboradores de
OpenStreetMap, ODbL). No se guarda en el repositorio: pesa 80 MB.
"""
import base64
import datetime
import io
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_cruces_calles as mc  # noqa: E402
import make_cruces as mk  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASO = 0.1          # lado del cuadrado, en grados
MARGEN = 0.006      # unos 600 m de vias de mas alrededor de cada cuadrado
ETIQUETAS = ("highway", "ref", "name", "oneway", "junction", "oneway:bicycle")
CARRETERA = mc.CARRETERA


def lee_pbf(ruta):
    import osmium

    vias = []

    class H(osmium.SimpleHandler):
        def way(self, w):
            if "highway" not in w.tags:
                return
            nodos, geo = [], []
            for n in w.nodes:
                if not n.location.valid():
                    return
                nodos.append(n.ref)
                geo.append((n.location.lat, n.location.lon))
            if len(nodos) < 2:
                return
            tags = {k: w.tags[k] for k in ETIQUETAS if k in w.tags}
            vias.append((w.id, nodos, geo, tags))

    H().apply_file(ruta, locations=True)
    fecha = ""
    try:
        f = osmium.io.Reader(ruta, osmium.osm.osm_entity_bits.NOTHING)
        fecha = (f.header().get("osmosis_replication_timestamp") or "")[:10]
        f.close()
    except Exception:
        pass
    return vias, fecha


def clave_tesela(la, lo):
    return int(math.floor(la / PASO + 1e-9)), int(math.floor(lo / PASO + 1e-9))


def main():
    pbf = sys.argv[1]
    salida = os.path.join(ROOT, "data", "cruces")
    os.makedirs(salida, exist_ok=True)
    vias, fecha = lee_pbf(pbf)
    fecha = fecha or datetime.date.today().isoformat()
    print("vias", len(vias), "fecha", fecha)
    # Cada via, a los cuadrados que toca con su margen.
    porTesela = {}
    for idx, (_, _, geo, _) in enumerate(vias):
        las = [p[0] for p in geo]
        los = [p[1] for p in geo]
        a0, b0 = clave_tesela(min(las) - MARGEN, min(los) - MARGEN)
        a1, b1 = clave_tesela(max(las) + MARGEN, max(los) + MARGEN)
        for a in range(a0, a1 + 1):
            for b in range(b0, b1 + 1):
                porTesela.setdefault((a, b), []).append(idx)
    escritas = []
    total_kb = 0
    for (a, b), lista in sorted(porTesela.items()):
        S, W = a * PASO, b * PASO
        elementos, coord, vs = [], {}, {}
        for idx in lista:
            wid, nodos, geo, tags = vias[idx]
            e = {"type": "way", "id": wid, "nodes": nodos,
                 "geometry": [{"lat": la, "lon": lo} for la, lo in geo], "tags": tags}
            elementos.append(e)
            vs[wid] = e
            for n, g in zip(nodos, geo):
                coord[n] = g
        cruces = mc.calcula_cruces(vs, coord)
        dentro = {k: v for k, v in cruces.items()
                  if S <= k[0] < S + PASO and W <= k[1] < W + PASO}
        # Con menos de dos no merece fichero (el lector exige dos: asi
        # distingue un fichero vacio); son esquinas del borde de Euskadi.
        if len(dentro) < 2:
            continue
        doc = {"bbox": [round(S, 4), round(W, 4), round(S + PASO, 4), round(W + PASO, 4)],
               "escala": mc.ESCALA, "paso_rama": mc.PASO, "ramas_min": 3}
        mc.codifica(dentro, {}, doc)
        doc["fecha_osm"] = fecha
        # Carretera que sigue con un ramal menor: el mismo bit que pone
        # make_cruces.py --carreteras, sacado aqui del tipo de via de las ramas.
        orden = sorted(dentro)
        bits = bytearray((len(orden) + 7) // 8)
        for i, k in enumerate(orden):
            tipos = [x["w"].get("tags", {}).get("highway") for x in dentro[k]]
            mayor = sum(1 for t in tipos if t in CARRETERA and t != "unclassified")
            if mayor >= 2 and mayor < len(tipos):
                bits[i >> 3] |= 1 << (i & 7)
        doc["cruces_carretera"] = base64.b64encode(bytes(bits)).decode("ascii")
        # Las rotondas con su centro dentro del cuadrado.
        rot = [r for r in mk.rotondas_de({"elements": elementos})
               if S <= r[0] < S + PASO and W <= r[1] < W + PASO]
        plano, sal, px, py = [], [], 0, 0
        for la, lo, r, sentido, salidas in rot:
            ex, ey = int(round(la * mc.ESCALA)), int(round(lo * mc.ESCALA))
            plano += [ex - px, ey - py, r]
            sal.append([sentido] + [g if libre else g + 360 for g, libre in salidas])
            px, py = ex, ey
        doc["rotondas"] = plano
        doc["rotondas_salidas"] = sal
        doc["fecha_rotondas"] = fecha
        nombre = "t_%d_%d.json" % (a, b)
        with io.open(os.path.join(salida, nombre), "w", encoding="utf-8") as f:
            json.dump(doc, f, separators=(",", ":"))
        kb = os.path.getsize(os.path.join(salida, nombre)) / 1024
        total_kb += kb
        escritas.append([a, b])
        print("%s: %d cruces, %d rotondas, %.0f KB" % (nombre, len(dentro), len(rot), kb))
    indice = {"fecha_osm": fecha, "paso": PASO, "teselas": escritas,
              "fuente": "OpenStreetMap (ODbL), extracto de Euskadi"}
    with io.open(os.path.join(salida, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, separators=(",", ":"))
    print("%d cuadrados, %.1f MB en total" % (len(escritas), total_kb / 1024))


if __name__ == "__main__":
    main()
