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
    ("mallabia", "Mallabia", "Mallabia"),
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
        "rutas": ["arteta", "artetaasuntza", "sanpedrobidarte", "sarrimendi", "karabieta", "egoarbitza"],
    },
    {
        "id": "mallabia",
        "zona": "mallabia",
        "es": "Fuente de Mallabia",
        "eu": "Mallabiko iturria",
        # Coordenada medida por el autor, en el pueblo: a 69 m del centro de
        # Mallabia segun OpenStreetMap.
        "coord": (43.188942, -2.530128),
        "punto": ("sarrimendi", None),
        # Las dos 7 Pago salen y llegan a 18-23 m de aqui, medido en sus GPX.
        "nota_es": "Junto a la salida de la 7 Pago.",
        "nota_eu": "7 Pagoren irteeraren ondoan.",
        "rutas": ["sarrimendi", "7pago", "7pago16"],
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
                  "sarrimendi", "oiz", "axmakurandikoa", "maguna", "sancristobal", "hirutxikiak", "7pago", "garaimaguna"],
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
                  "trabakuamallabia", "hirutxikiak", "7pago", "7pago16", "zengotitaiturzuri"],
    },
    {
        "id": "sancristobaltxiki",
        "zona": "zengotita",
        "es": "Fuente de San Kristobal Txiki",
        "eu": "San Kristobal Txikiko iturria",
        # Medida por el autor, 117 m al oeste del waypoint: la fuente esta en
        # el cruce de caminos, no donde pasaba el punto del recorrido.
        "coord": (43.199073, -2.583126),
        "punto": ("sancristobalgaraiandikoa", 1),
        "nota_es": "Arriba, junto a la ermita.",
        "nota_eu": "Goian, baselizaren ondoan.",
        "rutas": ["sancristobalgaraiandikoa", "garaigaztelu", "maguna", "potrera", "amaraune", "garaimaguna", "sancristobal", "sancristobaloiz", "sarrimendi", "zengotitagane"],
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
        "coord": (43.228643, -2.637205),
        "punto": ("maguna", 3),
        "nota_es": "En el casco del barrio.",
        "nota_eu": "Auzoaren erdigunean.",
        "rutas": ["maguna"],
    },
    {
        "id": "garai",
        "zona": "garai",
        "es": "Fuente de Garai",
        "eu": "Garaiko iturria",
        # Medida por el autor, a 32 m del waypoint.
        "coord": (43.195352, -2.610833),
        "punto": ("sancristobalgaraiandikoa", 5),
        "nota_es": "Comparte sitio con un antiguo lavadero.",
        "nota_eu": "Antzinako garbitokiarekin batera dago.",
        "rutas": ["sancristobalgaraiandikoa", "garaimaguna", "garaigaztelu", "sancristobal"],
    },
    {
        "id": "errotatxo",
        "zona": "garai",
        "es": "Fuente de Errotatxo",
        "eu": "Errotatxoko iturria",
        # Coordenada medida por el autor.
        "coord": (43.169057, -2.571949),
        "punto": ("garaigaztelu", None),
        "rutas": ["zaldibar", "argineta", "garaigaztelu"],
    },
    {
        "id": "sanmartin",
        "zona": "garai",
        "es": "Fuente de San Martín",
        "eu": "San Martin baselizako iturria",
        "punto": ("garaigaztelu", 8),
        "nota_es": "Junto a la ermita de San Martín, en Gaztelu.",
        "nota_eu": "San Martin baselizaren ondoan, Gaztelun.",
        "rutas": ["garaigaztelu", "santamanazarandikoa"],
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
        "rutas": ["argineta", "karabieta", "galdaraminio", "intxorta", "aixola", "hirutxikiak", "egoarbitza", "santamanazarandikoa"],
    },
    {
        "id": "aixola",
        "zona": "aixola",
        "es": "Fuente de la presa de Aixola",
        "eu": "Aixolako presako iturria",
        # Medida por el autor, 625 m al sur del waypoint de egoarbitza que
        # se usaba antes: aquel era el punto del RECORRIDO. Se contrasta con
        # el de aixola, que es el que cae cerca (95 m).
        "coord": (43.157893, -2.505235),
        "punto": ("aixola", 4),
        "nota_es": "Agua todo el año. Hay que desviarse unos metros a la izquierda al llegar al camino de la presa.",
        "nota_eu": "Ura urte osoan. Presako bidera iristean, metro batzuk ezkerrera jo behar da.",
        "rutas": ["egoarbitza", "zaldibar", "hirutxikiak", "aixola"],
    },
    {
        "id": "zaldibar",
        "zona": "aixola",
        "es": "Fuente del pol\u00edgono de Zaldibar",
        "eu": "Zaldibarko poligonoko iturria",
        # Medida por el autor. Ninguna ficha la menciona, asi que las rutas
        # son las que pasan por el punto: aixola a 8 m y zaldibar a 11 m.
        "coord": (43.171824, -2.538339),
        "punto": ("zaldibar", None),
        "nota_es": "Junto al pol\u00edgono, de camino a Zaldibar.",
        "nota_eu": "Poligonoaren ondoan, Zaldibarrerako bidean.",
        "rutas": ["aixola", "zaldibar"],
    },
    {
        "id": "eitzaga",
        "zona": "aixola",
        "es": "Fuente de Eitzaga",
        "eu": "Eitzagako iturria",
        "punto": ("zaldibar", 2),
        "nota_es": "En el barrio, antes de bajar hacia la presa de Aixola.",
        "nota_eu": "Auzoan, Aixolako presara jaitsi aurretik.",
        "rutas": ["zaldibar", "hirutxikiak", "aixola"],
    },
    {
        "id": "elgeta",
        "zona": "aixola",
        "es": "Fuente de Elgeta",
        "eu": "Elgetako iturria",
        "coord": (43.137005, -2.488427),
        "punto": ("zaldibar", 4),
        "nota_es": "En el pueblo, junto al polideportivo y el frontón.",
        "nota_eu": "Herrian, kiroldegiaren eta pilotalekuaren ondoan.",
        "rutas": ["zaldibar", "argineta", "galdaraminio", "karabieta"],
    },
    {
        "id": "sansalvador",
        "zona": "aixola",
        "es": "Fuente de San Salvador",
        "eu": "San Salvador baselizako iturria",
        # Medida por el autor. intxorta la citaba ("pasar junto a la ermita de
        # San Salvador, donde encontraremos tambien una fuente") pero no habia
        # forma de situarla: su waypoint mas cercano queda a 811 m, asi que la
        # ruta solo sirve aqui para sacar la altura.
        "coord": (43.133318, -2.489740),
        "punto": ("intxorta", None),
        "nota_es": "Junto a la ermita, bajando de Intxorta hacia Elgeta.",
        "nota_eu": "Baselizaren ondoan, Intxortatik Elgetara jaistean.",
        "rutas": ["intxorta", "ahuntzen"],
    },
    {
        "id": "arginieta",
        "zona": "aixola",
        "es": "Fuente de Argi\u00f1eta",
        "eu": "Argi\u00f1etako iturria",
        # Medida por el autor. argineta la citaba ("hay tambien una fuente
        # junto a la necropolis para llenar cantimploras") pero no habia
        # forma de situarla.
        "coord": (43.139550, -2.535917),
        "punto": ("argineta", 7),
        "nota_es": "Junto a la nec\u00f3polis de Argi\u00f1eta.",
        "nota_eu": "Argi\u00f1etako nekropoliaren ondoan.",
        "rutas": ["argineta"],
    },
    {
        "id": "larrosa",
        "zona": "aixola",
        "es": "Larrosako Iturri",
        "eu": "Larrosako Iturri",
        # Coordenada medida por el autor, a 32 m del waypoint de argineta: la
        # fuente esta al lado del camino, no sobre el.
        # Enganchada al camino: la medida que dio el autor caia 30 m dentro
        # del monte y la fuente esta en el camino mismo, asi que se usa el
        # punto del track mas cercano -- el de galdaramino, que a esa altura
        # coincide con argineta, zaldibar y aixola a menos de 6 m.
        "coord": (43.149112, -2.502047),
        "punto": ("argineta", 4),
        "nota_es": "Sale directamente de la pared de la monta\u00f1a, al salir "
                   "de la presa camino de Elgeta.",
        "nota_eu": "Zuzenean mendiaren hormatik ateratzen da, presatik "
                   "irtetean Elgetarako bidean.",
        "rutas": ["argineta", "aixola", "galdaraminio", "zaldibar"],
    },
    {
        "id": "usartza",
        "zona": "markina",
        "es": "Fuente de Usartza",
        "eu": "Usartzako iturria",
        # Medida por el autor. Es una de las «varias fuentes en la subida a
        # Kalamua» que citan kalamua y barinaga sin decir donde estaban.
        "coord": (43.209722, -2.471947),
        "punto": ("kalamua", None),
        "nota_es": "En el camino que sube a Kalamua.",
        "nota_eu": "Kalamuara igotzen den bidean.",
        "rutas": ["kalamua", "barinaga"],
    },
    {
        "id": "urkieta",
        "zona": "markina",
        "es": "Fuente de Urkieta",
        "eu": "Urkietako iturria",
        # Medida por el autor: la tercera de la subida a Kalamua, entre la de
        # Usartza (864 m mas abajo) y la de Intxaurkorta (552 m mas arriba).
        # El nombre sale del paraje de al lado en OpenStreetMap (250 m); si el
        # autor la llama de otra forma, se cambia aqui.
        "coord": (43.217490, -2.471804),
        "punto": ("kalamua", None),
        "nota_es": "En el camino a Kalamua, entre la de Usartza y la de Intxaurkorta.",
        "nota_eu": "Kalamuarako bidean, Usartzakoaren eta Intxaurkortakoaren artean.",
        "rutas": ["kalamua", "barinaga"],
    },
    {
        "id": "intxaurkorta",
        "zona": "markina",
        "es": "Fuente de Intxaurkorta",
        "eu": "Intxaurkortako iturria",
        # Medida por el autor, 1,3 km por encima de la de Usartza: la segunda
        # de las «varias fuentes en la subida a Kalamua». El nombre sale del
        # paraje que tiene al lado en OpenStreetMap (212 m); si el autor la
        # llama de otra forma, se cambia aqui.
        "coord": (43.221017, -2.467010),
        "punto": ("kalamua", None),
        "nota_es": "M\u00e1s arriba en el camino a Kalamua, pasada la de Usartza.",
        "nota_eu": "Kalamuarako bidean gorago, Usartzakoa pasata.",
        "rutas": ["kalamua", "barinaga"],
    },
    {
        "id": "drogeten",
        "zona": "markina",
        "es": "Drogeten Iturria",
        "eu": "Drogeten Iturria",
        "punto": ("sanpedrobidarte", 3),
        "rutas": ["sanpedrobidarte", "zaldibar"],
    },
    {
        "id": "barinaga",
        "zona": "markina",
        "es": "Fuente de Barinaga",
        "eu": "Barinagako iturria",
        # Medida por el autor, a 519 m del waypoint «Barinaga» de la ruta,
        # que es por donde pasa el recorrido y no donde esta la fuente; por
        # eso la ruta solo sirve aqui para sacar la altura.
        "coord": (43.236678, -2.492017),
        "punto": ("barinaga", None),
        "nota_es": "En el pueblo, junto al frontón.",
        "nota_eu": "Herrian, pilotalekuaren ondoan.",
        "rutas": ["barinaga"],
    },
    {
        "id": "iturreta",
        "zona": "markina",
        "es": "Fuente de Iturreta",
        "eu": "Iturretako iturria",
        # 10 m al este de la primera medida: el autor la corrigio porque
        # aquella caia en mitad de la campa y la fuente esta junto al sendero.
        "coord": (43.243311, -2.510417),
        "punto": ("exigente", 1),
        "nota_es": "Junto a la ermita.",
        "nota_eu": "Baselizaren ondoan.",
        "rutas": ["exigente", "urregarai", "kalamua"],
    },
    {
        "id": "markina",
        "zona": "markina",
        "es": "Fuente de Markina",
        "eu": "Markinako iturria",
        # El punto que senalo el autor sobre el mapa, junto a Karmengo kalea.
        # Se llego a el en dos pasos: primero la iglesia del Carmen (Karmengo
        # eliza eta komentua, en OpenStreetMap), porque el waypoint de la ruta
        # caia 279 m al norte, y despues esta correccion suya. Ya no va como
        # aproximada: esta donde el dice que esta.
        "coord": (43.267060, -2.497890),
        "punto": ("urregarai", 2),
        "nota_es": "Fuente grande, junto a la iglesia del Carmen.",
        "nota_eu": "Iturri handia, Karmengo elizaren ondoan.",
        "rutas": ["urregarai", "kalamua"],
    },
    {
        "id": "bolibar",
        "zona": "markina",
        "es": "Fuente de Bolibar",
        "eu": "Bolibarko iturria",
        # Medida por el autor. Ninguna ficha decia que hubiera agua aqui, asi
        # que las rutas de la lista son las que pasan por el punto: las cinco
        # que cruzan el pueblo, todas a menos de 20 m.
        "coord": (43.249883, -2.549516),
        "punto": ("markinabolibar", None),
        "nota_es": "En el pueblo, junto al monumento a Sim\u00f3n Bol\u00edvar.",
        "nota_eu": "Herrian, Simon Bolivarren monumentuaren ondoan.",
        "rutas": ["markinabolibar", "astorkigane", "markinaurjauziak", "urregarai", "exigente"],
    },
    {
        "id": "ziortza",
        "zona": "markina",
        "es": "Fuente del camino de Zenarruza",
        "eu": "Zenarruzarako bideko iturria",
        # Medida por el autor, en la calzada del Camino de Santiago que sube
        # de Bolibar a Ziortza, 500 m antes de la Colegiata. El nombre es
        # provisional: ninguna ficha la menciona, asi que no hay uno suyo.
        "coord": (43.245637, -2.557064),
        "punto": ("markinabolibar", None),
        "nota_es": "En la calzada que sube de Bolibar a la Colegiata de Zenarruza.",
        "nota_eu": "Bolibartik Zenarruzako Kolegiatara igotzen den galtzadan.",
        "rutas": ["markinaurjauziak", "markinabolibar", "exigente", "urregarai"],
    },
    {
        "id": "munitibar",
        "zona": "markina",
        "es": "Fuente de Munitibar",
        "eu": "Munitibarko iturria",
        # Medida por el autor. Solo pasa por aqui astorkigane, a 3 m.
        "coord": (43.265603, -2.592610),
        "punto": ("astorkigane", None),
        "nota_es": "En la plaza del pueblo.",
        "nota_eu": "Herriko plazan.",
        "rutas": ["astorkigane"],
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
        "rutas": ["santaeufemia", "markinaurjauziak", "markinabolibar", "exigente"],
    },
    {
        "id": "atxagarai",
        "zona": "markina",
        "es": "Fuente de Atxagarai",
        "eu": "Atxagaraiko iturria",
        "coord": (43.281323, -2.532273),
        "punto": ("santaeufemia", 2),
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
    """El waypoint numero n (base 1) de una ruta, tal como lo pinta su mapa.

    n puede ser None: entonces la ruta solo sirve para sacar la altura, porque
    la fuente no cae cerca de ningun waypoint suyo. Pasa con las que el autor
    ha medido en sitios por los que la ruta pasa sin pararse a numerarlos.
    """
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
        if "coord" in f and n is not None:
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
