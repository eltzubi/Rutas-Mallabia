#!/usr/bin/env python3
"""Escribe data/fuentes.json: los puntos de agua del sitio, para agua.html.

Por que un script y no un JSON a mano: la coordenada de cada fuente NO se
inventa aqui. Cada una se declara como "el waypoint numero N de tal ruta" --
es decir, un punto que ya esta publicado en el mapa de esa ficha y que salio
del GPX real-- y el script lo resuelve leyendo data/<ruta>.json. Si manana se
regraba un track y ese waypoint se mueve, la fuente se mueve con el; no hay
dos verdades.

De cada fuente se guarda ademas que rutas pasan por ella. Solo se apunta una
ruta cuando su propio texto dice que ahi hay agua: pasar cerca no es lo mismo
que poder llenar el bidon. El script comprueba que el track de cada una de
esas rutas pase de verdad a menos de MAX_RUTA_M de la fuente, y falla si no
-- es la red que impide que una errata en la tabla publique un dato falso.

Hay una segunda forma de declararla, "coord": la coordenada medida sobre el
terreno por el autor. Manda sobre el waypoint cuando la da, porque el
waypoint es un punto del recorrido -- donde pasa el camino -- y la fuente
suele estar unos metros a un lado. Entonces "punto" solo dice de que ruta se
saca la altura.

Las que llevan aprox=True no tienen una coordenada propia: la posicion es la
del lugar (el pueblo, la presa, el alto) y el texto del sitio dice donde esta
la fuente dentro de el ("junto al fronton", "unos metros a la izquierda").
Salen marcadas como aproximadas en el mapa, con su nota, en vez de fingir
una precision que no tenemos.

Uso:
    python3 scripts/make_fuentes.py
"""
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Cuanto puede alejarse el track de una ruta de la fuente que dice tener.
# 350 m: la coordenada es un punto del recorrido, pero la de una fuente de
# pueblo (Elgeta, Barinaga) es la del pueblo y otra ruta puede cruzarlo por
# otra calle.
MAX_RUTA_M = 350

# zona -> (castellano, euskera). El orden es el de la lista de la pagina:
# de Trabakua hacia fuera.
ZONAS = [
    ("trabakua", "Trabakua", "Trabakua"),
    ("zengotita", "Zengotita y Oiz", "Zengotita eta Oiz"),
    ("garai", "Garai, Berriz y Gaztelu", "Garai, Berriz eta Gaztelu"),
    ("aixola", "Elgeta y Aixola", "Elgeta eta Aixola"),
    ("markina", "Urko y Markina", "Urko eta Markina"),
]

# Cada entrada: de donde sale la coordenada (ruta + indice de waypoint, base 1,
# el mismo numero que se ve en el perfil de esa ficha) y que rutas tienen agua
# ahi segun su propio texto.
FUENTES = [
    {
        "id": "trabakua",
        "zona": "trabakua",
        "es": "Fuente del alto de Trabakua",
        "eu": "Trabakuko mendateko iturria",
        # Coordenada medida por el autor, a 6,7 m del punto de referencia del
        # puerto que comparten 30 rutas: la fuente esta en el alto mismo.
        "coord": (43.210466, -2.546084),
        "punto": ("trabakua", "salida"),
        "nota_es": "En el alto, junto al bar de arriba y los columpios.",
        "nota_eu": "Mendatean bertan, goiko tabernaren eta kulunken ondoan.",
        "rutas": ["mendibil", "urko", "hirutxikiak"],
    },
    {
        "id": "arteta",
        "zona": "trabakua",
        "es": "Fuente de Arteta",
        "eu": "Artetako iturria",
        "punto": ("arteta", 3),
        "nota_es": "Agua todo el año. Brota de la roca y está algo escondida entre los árboles.",
        "nota_eu": "Ura urte osoan. Harkaitzetik sortzen da eta zuhaitzen artean ezkutatuta dago.",
        "rutas": ["arteta", "artetaasuntza", "sanpedrobidarte", "sarrimendi", "karabieta"],
    },
    {
        "id": "iturzuri",
        "zona": "zengotita",
        "es": "Fuente de Iturzuri",
        "eu": "Iturzuriko iturria",
        "punto": ("iturrizuri", 1),
        "nota_es": "Junto al refugio, en lo alto.",
        "nota_eu": "Aterpearen ondoan, goialdean.",
        "rutas": ["iturrizuri", "axmakuriturrizuri", "zengotitaiturzuri", "longa", "betzun",
                  "sarrimendi", "oiz", "axmakurandikoa", "maguna", "sancristobal", "hirutxikiak"],
    },
    {
        "id": "zengotita",
        "zona": "zengotita",
        "es": "Fuente de Zengotita",
        "eu": "Zengotitako iturria",
        "punto": ("zengotitaosmagain", 1),
        "nota_es": "A la entrada del barrio, a mano derecha. Agua todo el año.",
        "nota_eu": "Auzoaren sarreran, eskuinaldean. Ura urte osoan.",
        "rutas": ["zengotitaosmagain", "betzun", "intxorta", "egoarbitza", "sarrimendi",
                  "trabakuamallabia", "hirutxikiak"],
    },
    {
        "id": "sancristobaltxiki",
        "zona": "zengotita",
        "es": "Fuente de San Kristobal Txiki",
        "eu": "San Kristobal Txikiko iturria",
        "punto": ("sancristobalgaraiandikoa", 1),
        "nota_es": "Arriba, junto a la ermita.",
        "nota_eu": "Goian, baselizaren ondoan.",
        "rutas": ["sancristobalgaraiandikoa", "garaigaztelu", "maguna", "potrera"],
    },
    {
        "id": "oiz",
        "zona": "zengotita",
        "es": "Fuente Oiz",
        "eu": "Oiz Iturria",
        "punto": ("sancristobaloiz", 4),
        "nota_es": "Bastante escondida y fácil de pasar de largo.",
        "nota_eu": "Nahiko ezkutuan dago eta erraz pasa daiteke ohartu gabe.",
        "rutas": ["sancristobaloiz"],
    },
    {
        "id": "maguna",
        "zona": "zengotita",
        "es": "Fuente de Maguna",
        "eu": "Magunako iturria",
        # El autor dice que esta en el casco del barrio, y el waypoint caia
        # 300 m al norte: es el punto del RECORRIDO, no el del barrio. La
        # coordenada es la del nucleo de Maguna en OpenStreetMap (hamlet).
        "coord": (43.22822, -2.63766),
        "punto": ("maguna", 3),
        "aprox": True,
        "nota_es": "En el casco del barrio.",
        "nota_eu": "Auzoaren erdigunean.",
        "rutas": ["maguna"],
    },
    {
        "id": "garai",
        "zona": "garai",
        "es": "Fuente de Garai",
        "eu": "Garaiko iturria",
        "punto": ("sancristobalgaraiandikoa", 5),
        "nota_es": "Comparte sitio con un antiguo lavadero.",
        "nota_eu": "Antzinako garbitokiarekin batera dago.",
        "rutas": ["sancristobalgaraiandikoa", "garaimaguna", "garaigaztelu"],
    },
    {
        "id": "sanmartin",
        "zona": "garai",
        "es": "Fuente de San Martín",
        "eu": "San Martin baselizako iturria",
        "punto": ("garaigaztelu", 8),
        "nota_es": "Junto a la ermita de San Martín, en Gaztelu.",
        "nota_eu": "San Martin baselizaren ondoan, Gaztelun.",
        "rutas": ["garaigaztelu"],
    },
    {
        "id": "berriozabaleta",
        "zona": "garai",
        "es": "Fuente de Berriozabaleta",
        "eu": "Berriozabaletako iturria",
        "punto": ("santamanazarandikoa", 5),
        "nota_es": "Forma conjunto con un lavadero y una zona de descanso.",
        "nota_eu": "Garbitoki batekin eta atseden gunearekin osatzen du multzoa.",
        "rutas": ["santamanazarandikoa"],
    },
    {
        "id": "goierri",
        "zona": "aixola",
        "es": "Fuente de Goierri",
        "eu": "Goierriko iturria",
        "punto": ("argineta", 2),
        "nota_es": "Junto a la ermita y el merendero.",
        "nota_eu": "Baselizaren eta merenderoaren ondoan.",
        "rutas": ["argineta", "karabieta", "galdaraminio", "intxorta", "aixola", "hirutxikiak"],
    },
    {
        "id": "aixola",
        "zona": "aixola",
        "es": "Fuente de la presa de Aixola",
        "eu": "Aixolako presako iturria",
        "punto": ("egoarbitza", 4),
        "aprox": True,
        "nota_es": "Agua todo el año. Hay que desviarse unos metros a la izquierda al llegar al camino de la presa.",
        "nota_eu": "Ura urte osoan. Presako bidera iristean, metro batzuk ezkerrera jo behar da.",
        "rutas": ["egoarbitza", "zaldibar", "hirutxikiak"],
    },
    {
        "id": "eitzaga",
        "zona": "aixola",
        "es": "Fuente de Eitzaga",
        "eu": "Eitzagako iturria",
        "punto": ("zaldibar", 2),
        "nota_es": "En el barrio, antes de bajar hacia la presa de Aixola.",
        "nota_eu": "Auzoan, Aixolako presara jaitsi aurretik.",
        "rutas": ["zaldibar", "hirutxikiak"],
    },
    {
        "id": "elgeta",
        "zona": "aixola",
        "es": "Fuente de Elgeta",
        "eu": "Elgetako iturria",
        "punto": ("zaldibar", 4),
        "aprox": True,
        "nota_es": "En el pueblo, junto al polideportivo y el frontón.",
        "nota_eu": "Herrian, kiroldegiaren eta pilotalekuaren ondoan.",
        "rutas": ["zaldibar"],
    },
    {
        "id": "larrosa",
        "zona": "aixola",
        "es": "Larrosako Iturri",
        "eu": "Larrosako Iturri",
        # Coordenada medida por el autor, a 32 m del waypoint de argineta: la
        # fuente esta al lado del camino, no sobre el.
        "coord": (43.149030, -2.501700),
        "punto": ("argineta", 4),
        "nota_es": "Sale directamente de la pared de la monta\u00f1a, al salir "
                   "de la presa camino de Elgeta.",
        "nota_eu": "Zuzenean mendiaren hormatik ateratzen da, presatik "
                   "irtetean Elgetarako bidean.",
        "rutas": ["argineta", "aixola", "galdaraminio", "zaldibar"],
    },
    {
        "id": "drogeten",
        "zona": "markina",
        "es": "Drogeten Iturria",
        "eu": "Drogeten Iturria",
        "punto": ("sanpedrobidarte", 3),
        "rutas": ["sanpedrobidarte"],
    },
    {
        "id": "barinaga",
        "zona": "markina",
        "es": "Fuente de Barinaga",
        "eu": "Barinagako iturria",
        "punto": ("barinaga", 3),
        "aprox": True,
        "nota_es": "En el pueblo, junto al frontón.",
        "nota_eu": "Herrian, pilotalekuaren ondoan.",
        "rutas": ["barinaga"],
    },
    {
        "id": "iturreta",
        "zona": "markina",
        "es": "Fuente de Iturreta",
        "eu": "Iturretako iturria",
        "punto": ("exigente", 1),
        "aprox": True,
        "nota_es": "Junto a la ermita.",
        "nota_eu": "Baselizaren ondoan.",
        "rutas": ["exigente", "urregarai"],
    },
    {
        "id": "markina",
        "zona": "markina",
        "es": "Fuente de Markina",
        "eu": "Markinako iturria",
        # Junto a la iglesia del Carmen, dice el autor, y el waypoint caia
        # 279 m al norte. Se partio de la iglesia (Karmengo eliza eta
        # komentua, en OpenStreetMap) y el autor la corrigio 20 m al este,
        # que es donde esta la fuente; por eso ya no va como aproximada.
        "coord": (43.267020, -2.498543),
        "punto": ("urregarai", 2),
        "nota_es": "Fuente grande, junto a la iglesia del Carmen.",
        "nota_eu": "Iturri handia, Karmengo elizaren ondoan.",
        "rutas": ["urregarai"],
    },
    {
        "id": "camino",
        "zona": "markina",
        "es": "Fuente del Camino de Santiago",
        "eu": "Done Jakue bideko iturria",
        # Coordenada medida por el autor, a 41 m del waypoint de santaeufemia.
        "coord": (43.257042, -2.526330),
        "punto": ("santaeufemia", 1),
        "nota_es": "Junto al camino, entre Markina-Xemein e Iruzubieta.",
        "nota_eu": "Bidearen ondoan, Markina-Xemein eta Iruzubieta artean.",
        "rutas": ["santaeufemia", "markinaurjauziak", "markinabolibar"],
    },
    {
        "id": "atxagarai",
        "zona": "markina",
        "es": "Fuente de Atxagarai",
        "eu": "Atxagaraiko iturria",
        "punto": ("santaeufemia", 2),
        "aprox": True,
        "nota_es": "Frente al refugio y la bolera, en el collado de Urregarai.",
        "nota_eu": "Aterpearen eta bolatokiaren parean, Urregaraiko lepoan.",
        "rutas": ["santaeufemia", "markinabolibar", "urregarai"],
    },
]

GPX_NS = "{http://www.topografix.com/GPX/1/1}"


def haversine(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


_tracks = {}


def track(slug):
    """Puntos (lat, lon, ele) del GPX real de una ruta."""
    if slug not in _tracks:
        arbol = ET.parse(os.path.join(ROOT, "src", slug + ".gpx"))
        puntos = []
        for p in arbol.getroot().iter(GPX_NS + "trkpt"):
            ele = p.find(GPX_NS + "ele")
            puntos.append((float(p.get("lat")), float(p.get("lon")),
                           float(ele.text) if ele is not None else None))
        _tracks[slug] = puntos
    return _tracks[slug]


def waypoint(slug, n):
    """El waypoint numero n (base 1) de una ruta, tal como lo pinta su mapa."""
    with open(os.path.join(ROOT, "data", slug + ".json"), encoding="utf-8") as f:
        datos = json.load(f)
    if n == "salida":
        return tuple(datos["marker"]["at"])
    wps = datos.get("waypoints", [])
    if not 1 <= n <= len(wps):
        raise SystemExit(f"{slug}: no tiene waypoint {n} (tiene {len(wps)})")
    return tuple(wps[n - 1])


def altitud(slug, pt):
    """Altura del punto del track mas cercano a la fuente."""
    mejor, mejor_d = None, None
    for p in track(slug):
        d = (p[0] - pt[0]) ** 2 + (p[1] - pt[1]) ** 2
        if mejor_d is None or d < mejor_d:
            mejor_d, mejor = d, p
    return round(mejor[2]) if mejor and mejor[2] is not None else None


def distancia_al_track(slug, pt):
    return min(haversine(pt, (p[0], p[1])) for p in track(slug))


def nombres_de_ruta(suffix):
    """slug -> nombre de la ruta, leido de las tarjetas de la portada.

    Se lee de ahi y no de una lista aparte para que el nombre que sale en la
    lista de fuentes sea el mismo que el de su tarjeta, en los dos idiomas.
    La portada en euskera enlaza <slug>.eu.html, asi que la clave se guarda
    siempre como el slug pelado.
    """
    with open(os.path.join(ROOT, "src", f"mallabia_tail{suffix}.html"), encoding="utf-8") as f:
        t = f.read()
    nombres = {}
    for m in re.finditer(r'<a class="route-card"[^>]*href="([^"]+)"(.*?)</a>', t, re.S):
        n = re.search(r'<h3 class="route-card-name">(.*?)</h3>', m.group(2), re.S)
        if n:
            slug = re.sub(r"(\.eu)?\.html$", "", m.group(1))
            nombres[slug] = " ".join(n.group(1).split())
    return nombres


def main():
    nombres_es = nombres_de_ruta("")
    nombres_eu = nombres_de_ruta(".eu")
    zonas_es = {k: es for k, es, _eu in ZONAS}
    zonas_eu = {k: eu for k, _es, eu in ZONAS}
    orden = [k for k, _es, _eu in ZONAS]

    salida = []
    problemas = []
    for f in FUENTES:
        slug, n = f["punto"]
        pt = tuple(f["coord"]) if "coord" in f else waypoint(slug, n)
        if "coord" in f:
            # No se acepta a ciegas: si la coordenada medida se va lejos del
            # waypoint que decia ser la misma fuente, es que una de las dos
            # esta mal, y eso hay que mirarlo, no publicarlo.
            desvio = haversine(pt, waypoint(slug, n))
            if desvio > MAX_RUTA_M:
                problemas.append(
                    f"{f['id']}: la coordenada dada esta a {desvio:.0f} m del "
                    f"waypoint {n} de {slug}; o es otra fuente o uno de los dos esta mal")
        for ruta in f["rutas"]:
            d = distancia_al_track(ruta, pt)
            if d > MAX_RUTA_M:
                problemas.append(
                    f"{f['id']}: la ruta {ruta} dice tener agua aqui pero su track "
                    f"pasa a {d:.0f} m (maximo {MAX_RUTA_M} m)")
        faltan = [r for r in f["rutas"]
                  if r not in nombres_es or r not in nombres_eu]
        if faltan:
            problemas.append(f"{f['id']}: rutas sin tarjeta en la portada: {faltan}")
        salida.append({
            "id": f["id"],
            "lat": round(pt[0], 5),
            "lon": round(pt[1], 5),
            "ele": altitud(slug, pt),
            "aprox": bool(f.get("aprox")),
            "es": {
                "nombre": f["es"],
                "zona": zonas_es[f["zona"]],
                "nota": f.get("nota_es", ""),
                "rutas": [{"href": r + ".html", "nombre": nombres_es[r]}
                          for r in f["rutas"]],
            },
            "eu": {
                "nombre": f["eu"],
                "zona": zonas_eu[f["zona"]],
                "nota": f.get("nota_eu", ""),
                "rutas": [{"href": r + ".html", "nombre": nombres_eu[r]}
                          for r in f["rutas"]],
            },
            "_orden": (orden.index(f["zona"]), len(salida)),
        })

    if problemas:
        raise SystemExit("\n".join(["No se escribe nada:"] + problemas))

    salida.sort(key=lambda x: x.pop("_orden"))
    destino = os.path.join(ROOT, "data", "fuentes.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump({"fuentes": salida}, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    aprox = sum(1 for x in salida if x["aprox"])
    print(f"data/fuentes.json: {len(salida)} fuentes ({aprox} de posicion aproximada), "
          f"{os.path.getsize(destino)} bytes")


if __name__ == "__main__":
    sys.exit(main())
