#!/usr/bin/env python3
"""Aparta un track publicado del domicilio del autor.

    python3 scripts/aleja_de_casa.py <ruta> [<ruta>...]      # reescribe el GPX
    python3 scripts/aleja_de_casa.py --revisa                # solo informa

POR QUE EXISTE
--------------
Los GPX se graban saliendo de casa, y publicados tal cual dicen donde vive el
autor. El 26 de agosto de 2026 se limpiaron de golpe las 17 rutas que habia
entonces (commit c9b00918), pero aquello fue una limpieza puntual, no una
regla: las rutas que entraron despues volvieron a traer el arranque real, y
el problema se fue arreglando a parches, de una en una. Esto lo convierte en
algo repetible, y scripts/check_site.py comprueba el resultado.

QUE HACE
--------
Dos operaciones, ninguna de las cuales inventa trazado:

  - RECORTE: si el track ya pasa por Trabakua en el primer o el ultimo
    kilometro y medio, se le quita lo que sobra por fuera. Conserva los
    tiempos: siguen siendo los de la grabacion original.
  - EMPALME: si no pasa, se le quita el ramal privado y se le pega el trozo
    real de BI-633 del GPX de galdaramino -- la ruta que el autor dio por
    buena como ejemplo de por donde hay que pasar. Al mezclar dos
    grabaciones los tiempos dejarian de ser ciertos, asi que se quitan, como
    ya se hizo en sancristobaloiz, muniozguren y santaeufemia.

Y un tercer caso, para las que solo PASAN por delante a mitad de recorrido:
se sustituye ese tramo concreto por el mismo trozo de BI-633 y el resto del
track se queda igual.

EL PUNTO A EVITAR
-----------------
Vive en scripts/.punto-privado.json, que esta EXCLUIDO DE GIT a proposito:
este repositorio es publico y escribir ahi la coordenada seria publicar justo
lo que se intenta quitar. Sin ese fichero, el script no hace nada y avisa.

Los dos margenes del fichero no son el mismo numero por una razon: la propia
BI-633 pasa a 39 m de la casa y eso el autor lo da por bueno, asi que un PASO
solo es "por delante" por debajo de 37 m. El ramal de un extremo se corta con
100 m. Con un unico margen de 100 el desvio se desviaba a si mismo y la
correccion no terminaba nunca.
"""
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NS = "{http://www.topografix.com/GPX/1/1}"
PUNTO = os.path.join(HERE, ".punto-privado.json")
TRABAKUA = (43.210466, -2.5460838)
CERCA_TRABAKUA = 60.0      # "pasa por Trabakua"
MAX_RECORTE_M = 1500       # mas que esto no es un ramal, es media ruta
DONANTE = "galdaraminio"   # la BI-633 que el autor dio por buena

ET.register_namespace("", "http://www.topografix.com/GPX/1/1")


def privado():
    if not os.path.exists(PUNTO):
        raise SystemExit(
            f"\nFalta {os.path.relpath(PUNTO, ROOT)}, que no va en git.\n"
            "Sin el no se puede saber que punto hay que evitar.")
    with open(PUNTO, encoding="utf-8") as f:
        d = json.load(f)
    d["casa"] = (d["lat"], d["lon"])
    return d


def haversine(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    return 2 * r * math.asin(math.sqrt(
        math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))


def a_la_recta(q, a, b, lat0):
    """Distancia de q al segmento a-b, en metros."""
    k = math.cos(math.radians(lat0))
    def xy(p):
        return ((p[1] - a[1]) * 111320 * k, (p[0] - a[0]) * 110540)
    qx, qy = xy(q)
    bx, by = xy(b)
    largo2 = bx * bx + by * by
    s = 0.0 if largo2 == 0 else max(0.0, min(1.0, (qx * bx + qy * by) / largo2))
    return math.hypot(qx - s * bx, qy - s * by)


def leer(slug):
    """(lat, lon, ele, time) de cada punto del GPX."""
    arbol = ET.parse(os.path.join(ROOT, "src", slug + ".gpx"))
    out = []
    for p in arbol.getroot().iter(NS + "trkpt"):
        ele = p.find(NS + "ele")
        t = p.find(NS + "time")
        out.append((float(p.get("lat")), float(p.get("lon")),
                    ele.text if ele is not None else None,
                    t.text if t is not None else None))
    return out, arbol


def largo(ps):
    return sum(haversine(ps[i - 1], ps[i]) for i in range(1, len(ps))) / 1000


def arregla(slug, cfg, donante):
    """Devuelve (puntos nuevos, lista de lo que se ha hecho, hubo_empalme)."""
    casa = cfg["casa"]
    margen = cfg["margen_extremo_m"]
    margen_paso = cfg["margen_paso_m"]
    margen_carretera = cfg["margen_carretera_m"]
    ps, _ = leer(slug)
    hechos = []
    empalme = False
    iT = min(range(len(donante)), key=lambda i: haversine(donante[i], TRABAKUA))

    def bi633(hasta):
        j = min(range(len(donante)), key=lambda i: haversine(donante[i], hasta))
        a, b = (iT, j) if iT <= j else (j, iT)
        trozo = donante[a:b + 1]
        return trozo if iT <= j else trozo[::-1]

    dT = [haversine(p, TRABAKUA) for p in ps]
    extremos_ok = max(dT[0], dT[-1]) < 200

    cab = col = None
    ini, fin = 0, len(ps) - 1
    if not extremos_ok:
        pri = next((i for i, d in enumerate(dT) if d < CERCA_TRABAKUA), None)
        if pri is not None and largo(ps[:pri + 1]) * 1000 < MAX_RECORTE_M:
            ini = pri
            hechos.append("recortado el arranque (%.2f km): ya pasaba por Trabakua" % largo(ps[:pri + 1]))
        else:
            ini = next(i for i, p in enumerate(ps) if haversine(p, casa) > margen)
            cab = bi633(ps[ini]); empalme = True
            hechos.append("quitado el ramal del arranque y empalmado %.2f km de BI-633" % largo(cab))

        ult = next((i for i in range(len(ps) - 1, -1, -1) if dT[i] < CERCA_TRABAKUA), None)
        if ult is not None and ult > ini and largo(ps[ult:]) * 1000 < MAX_RECORTE_M:
            fin = ult
            hechos.append("recortado el final (%.2f km): ya pasaba por Trabakua" % largo(ps[ult:]))
        else:
            fin = next(i for i in range(len(ps) - 1, -1, -1) if haversine(ps[i], casa) > margen)
            col = bi633(ps[fin])[::-1]; empalme = True
            hechos.append("quitado el ramal del final y empalmado %.2f km de BI-633" % largo(col))

    nuevos = (cab or []) + ps[ini:fin + 1] + (col or [])

    # Los pasos por delante, a mitad de recorrido.
    while True:
        malos = [i for i, p in enumerate(nuevos) if haversine(p, casa) < margen_paso]
        if not malos:
            break
        a = malos[0] - 1
        b = malos[0]
        for i in malos:
            if i <= b + 5:
                b = i
            else:
                break
        b = min(b + 1, len(nuevos) - 1)
        # El puente tiene que arrancar y morir YA en la carretera: si se
        # engancha a un punto que sigue cerca de la casa, el desvio deja los
        # dos cabos pegados a ella.
        while a > 0 and haversine(nuevos[a], casa) < margen_carretera:
            a -= 1
        while b < len(nuevos) - 1 and haversine(nuevos[b], casa) < margen_carretera:
            b += 1
        if a < 0 or b >= len(nuevos) - 1:
            raise SystemExit(f"{slug}: el tramo a desviar toca un extremo; revisalo a mano")
        ja = min(range(len(donante)), key=lambda k: haversine(donante[k], nuevos[a]))
        jb = min(range(len(donante)), key=lambda k: haversine(donante[k], nuevos[b]))
        puente = donante[ja:jb + 1] if ja <= jb else donante[jb:ja + 1][::-1]
        hechos.append("desviado a la BI-633 un paso por delante (%.2f km)" % largo(puente))
        nuevos = nuevos[:a + 1] + puente + nuevos[b:]
        empalme = True

    # El camino particular. Cerca de la casa hay dos vias casi paralelas: la
    # BI-633, por la que el autor da por bueno pasar, y su camino, que sale de
    # ella y pasa por delante. Las dos quedan a parecida distancia de la casa,
    # asi que no se distinguen por eso: se distinguen por separarse de la
    # general. Lo que ande cerca de la casa y a mas de margen_fuera de la
    # BI-633 se cambia por la BI-633, enganchando el puente donde el track ya
    # va pegado a ella.
    radio = cfg["radio_delante_m"]
    fuera_max = cfg["margen_fuera_m"]
    pegado = cfg["pegado_carretera_m"]
    cerca_casa = [d for d in donante if haversine(d, casa) < 800]

    def fuera(q):
        return min(a_la_recta(q, cerca_casa[i], cerca_casa[i + 1], casa[0])
                   for i in range(len(cerca_casa) - 1))

    while True:
        malos = [i for i, q in enumerate(nuevos)
                 if haversine(q, casa) < radio and fuera(q) > fuera_max]
        if not malos:
            break
        a, b = malos[0] - 1, malos[0]
        for i in malos:
            if i <= b + 5:
                b = i
            else:
                break
        b = min(b + 1, len(nuevos) - 1)
        # El puente tiene que nacer y morir con el track ya encima de la
        # general; si no, deja un cabo suelto apuntando al camino.
        while a > 0 and fuera(nuevos[a]) > pegado:
            a -= 1
        while b < len(nuevos) - 1 and fuera(nuevos[b]) > pegado:
            b += 1
        if a < 0 or b >= len(nuevos) - 1:
            raise SystemExit(f"{slug}: el camino particular llega a un extremo; revisalo a mano")
        ja = min(range(len(donante)), key=lambda k: haversine(donante[k], nuevos[a]))
        jb = min(range(len(donante)), key=lambda k: haversine(donante[k], nuevos[b]))
        puente = donante[ja:jb + 1] if ja <= jb else donante[jb:ja + 1][::-1]
        hechos.append("sacado del camino particular y devuelto a la BI-633 (%.2f km)"
                      % largo(puente))
        nuevos = nuevos[:a + 1] + puente + nuevos[b:]
        empalme = True
    return nuevos, hechos, empalme


def escribe(slug, puntos, con_tiempos):
    """Reescribe src/<slug>.gpx conservando su cabecera."""
    ruta = os.path.join(ROOT, "src", slug + ".gpx")
    arbol = ET.parse(ruta)
    seg = arbol.getroot().find(f".//{NS}trkseg")
    for hijo in list(seg):
        seg.remove(hijo)
    for lat, lon, ele, t in puntos:
        p = ET.SubElement(seg, NS + "trkpt", {"lat": str(lat), "lon": str(lon)})
        if ele is not None:
            ET.SubElement(p, NS + "ele").text = str(ele)
        if con_tiempos and t is not None:
            ET.SubElement(p, NS + "time").text = t
    ET.indent(arbol, space="  ")
    arbol.write(ruta, encoding="UTF-8", xml_declaration=True)


def main():
    cfg = privado()
    casa, margen_paso = cfg["casa"], cfg["margen_paso_m"]
    solo_revisa = "--revisa" in sys.argv
    slugs = [a for a in sys.argv[1:] if not a.startswith("--")]
    donante, _ = leer(DONANTE)
    if solo_revisa:
        import glob
        slugs = sorted(os.path.basename(g)[:-4]
                       for g in glob.glob(os.path.join(ROOT, "src", "*.gpx")))
    for slug in slugs:
        ps, _ = leer(slug)
        antes = min(haversine(p, casa) for p in ps)
        if solo_revisa:
            if antes < margen_paso:
                print("  %-28s a %3.0f m del punto" % (slug, antes))
            continue
        nuevos, hechos, empalme = arregla(slug, cfg, donante)
        despues = min(haversine(p, casa) for p in nuevos)
        print("== %s" % slug)
        for h in hechos:
            print("   %s" % h)
        print("   %.2f km -> %.2f km | al punto: %.0f m -> %.0f m | extremos a Trabakua: %.0f / %.0f m%s"
              % (largo(ps), largo(nuevos), antes, despues,
                 haversine(nuevos[0], TRABAKUA), haversine(nuevos[-1], TRABAKUA),
                 " | sin tiempos (empalme)" if empalme else ""))
        escribe(slug, nuevos, con_tiempos=not empalme)


if __name__ == "__main__":
    main()
