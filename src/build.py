#!/usr/bin/env python3
"""Rebuilds the site's HTML pages from the source templates in this folder.

Architecture:
  - Each page (mallabia = home, trabakua/iturrizuri/zenarruza = routes) is
    written as a <name>_head.html + <name>_tail.html pair, so they're small
    enough to edit directly even though the final assembled page has huge
    embedded base64 images.
  - Stylesheets live in css/ and are copied to the repo root as real files
    linked from each page's <head>, so the browser downloads and caches
    them once instead of duplicating them inline on every page:
      fonts/inline_fonts.css -> fonts.css   (self-hosted @font-face rules)
      css/home.css           -> home.css    (the home page)
      css/route.css          -> route.css   (every route page; they share
                                             one stylesheet, so a design
                                             change lands in one place)
  - Each pair is concatenated into a full standalone HTML document and
    written to its own file at the repo root (OUT_NAME below) -- these are
    real, independently loadable pages, not iframes. Home is index.html so
    GitHub Pages serves it at the site root; every other page keeps
    navigating between real files (<a href="trabakua.html">), so URLs are
    shareable/bookmarkable per route and each page only downloads its own
    photos.
  - Theme (light/dark) persists via localStorage directly -- every page
    shares the same real origin, so no cross-page relay is needed. A tiny
    inline script at the top of <head> applies the saved theme before first
    paint (avoids a flash of the wrong theme); the theme-toggle button's
    script (bottom of body) just flips it and writes back to localStorage.
  - The site is bilingual (Spanish + Basque). Only the Spanish _head/_tail
    files are written by hand; the Basque ones (*_head.eu.html /
    *_tail.eu.html) are GENERATED from them by src/i18n/make_eu.py using
    the string tables in src/i18n/eu.py. So the workflow after changing any
    Spanish text is always:

        python3 src/i18n/make_eu.py    # update Basque, fails if it's stale
        python3 src/build.py           # write both languages

    make_eu.py refuses to run when a Spanish string it knows has changed,
    which is what stops the two languages from drifting apart. To reword
    something in Basque, edit src/i18n/eu.py -- never the .eu.html files,
    they are overwritten.

  - To add a new route page: create <name>_head.html + <name>_tail.html,
    add "<name>" to PAGES below (home stays first), link to it with a plain
    <a href="<name>.html">, and add its strings to src/i18n/eu.py.

IMPORTANT: any file with embedded base64 (fonts/inline_fonts.css,
*_tail.html once photos are added) is huge -- do not open these with
a plain text editor or a tool that reads/prints whole files. Use
Python with a line-length filter (e.g. `if len(line) < 300`) to find
line numbers, and edit via string replacement in a script, not by
hand.

Usage:
    python3 src/build.py
Writes index.html, trabakua.html, iturrizuri.html, zenarruza.html and
fonts.css to the repo root, which GitHub Pages serves.
"""
import hashlib
import xml.etree.ElementTree as ET
import json
import html.entities
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, os.path.join(HERE, "i18n"))
import eu  # noqa: E402  -- el texto en euskera vive ahi, no aqui

# Catches a real bug class: writing "case&riacute;os" instead of
# "caser&iacute;os" (a letter from the word swallowed into the entity name)
# produces a name with no such HTML5 entity, so the browser prints the
# escape sequence literally instead of the accented letter. Python's own
# entity table is the authoritative list of what actually decodes.
_ENTITY_RE = re.compile(r"&(#?\w+);")


def check_entities(html_text, label):
    bad = sorted({
        m.group(0) for m in _ENTITY_RE.finditer(html_text)
        if not m.group(1).startswith("#") and (m.group(1) + ";") not in html.entities.html5
    })
    if bad:
        raise SystemExit(
            f"\n{label}: malformed/unknown HTML entities: {bad}\n"
            "A nearby letter was probably swallowed into the entity name "
            "(e.g. \"case&riacute;os\" instead of \"caser&iacute;os\") -- "
            "fix the source file, not this generated one."
        )


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


def assemble_page(name, suffix=""):
    return read(f"{name}_head{suffix}.html") + read(f"{name}_tail{suffix}.html")


# First entry is home; it's the one written to index.html.
PAGES = ["mallabia", "trabakua", "iturrizuri", "zenarruza", "argineta", "gerea", "zengotitagane", "oiz", "arietzu", "urko", "sancristobal", "iturreta", "egoarbitza", "urregarai", "kalamua", "mundiokokoba", "iruzubieta", "mendibil", "arteta", "goita", "hirutxikiak", "zaldibar", "maguna", "7pago", "7pago16", "barinaga", "muniozguren", "exigente", "potrera", "aixola", "intxorta", "artetaasuntza", "trabakuamallabia", "betzun", "sarrimendi", "longa", "zengotitaosmagain", "axmakuriturrizuri", "amaraune", "astarlokoatxa", "garaimaguna", "sanpedrobidarte", "sancristobaloiz", "axmakurandikoa", "markinabolibar", "asuntzabira", "gereaoculta", "sancristobalgaraiandikoa", "zengotitaiturzuri", "santamanazarandikoa", "markinakobau", "mallukitoko", "santaeufemia", "markinaurjauziak", "ahuntzen", "longaurjauziak", "astorkigane", "karabieta", "aviso-legal"]
# lang code -> (source-file suffix, output-file suffix)
LANGS = {"es": ("", ""), "eu": (".eu", ".eu")}

SITE_URL = "https://trabakutik.com/"

# La portada es la excepcion: lo que sirve trabakutik.com/ es el euskera, asi
# que el euskera se lleva el index.html a secas y el castellano se va a
# index.es.html. Antes la raiz servia el castellano y redirigia al euskera por
# JavaScript, lo que dejaba a Google con dos senales contradictorias (el
# canonical decia una cosa y la redireccion llevaba a otra); sirviendo el
# euskera de verdad en la raiz no hace falta redirigir nada.
HOME = "mallabia"
HOME_OUT = {"eu": "index.html", "es": "index.es.html"}


def out_name(page, lang):
    if page == HOME:
        return HOME_OUT[lang]
    return f"{page}{LANGS[lang][1]}.html"


def retarget_home_links(page_html, lang):
    """Reapunta los enlaces a la portada segun el idioma de la pagina.

    Las fuentes en castellano enlazan la portada como index.html y el
    conmutador de idioma como index.eu.html. Con el euskera en la raiz eso se
    invierte: en la salida ES la portada propia pasa a ser index.es.html y el
    conmutador apunta a la raiz; en la salida EU los index.html que dejo
    make_eu.py ya son la portada correcta y solo hay que sacar el conmutador
    hacia el castellano.
    """
    if lang == "es":
        # De golpe, no en dos pasadas: reescribir primero index.html dejaria
        # el index.eu.html del conmutador apuntando a un sitio que ya no toca.
        page_html = re.sub(
            r'href="index(\.eu)?\.html"',
            lambda m: 'href="index.html"' if m.group(1) else 'href="index.es.html"',
            page_html)
        page_html = page_html.replace(
            '<link rel="canonical" href="https://trabakutik.com/">',
            '<link rel="canonical" href="https://trabakutik.com/index.es.html">')
        page_html = page_html.replace(
            '<meta property="og:url" content="https://trabakutik.com/">',
            '<meta property="og:url" content="https://trabakutik.com/index.es.html">')
        # La raiz sin nombre de fichero solo la usa la portada, asi que esto no
        # toca el JSON-LD de ninguna otra pagina.
        page_html = page_html.replace(
            '"url": "https://trabakutik.com/",',
            '"url": "https://trabakutik.com/index.es.html",')
        return page_html
    # Las fichas con el tail EU escrito a mano (MANUAL_EU_PAGES en make_eu.py)
    # no pasan por el swap de EU_OF, asi que enlazan la portada como
    # index.eu.html, que ahora es solo la redireccion heredada.
    page_html = page_html.replace('href="index.eu.html"', 'href="index.html"')
    # El conmutador es ahora los dos idiomas a la vista, asi que el enlace al
    # castellano es el <a> con hreflang="es": el unico de la pagina.
    return page_html.replace(
        '<a href="index.html" hreflang="es" lang="es"',
        '<a href="index.es.html" hreflang="es" lang="es"')


# source asset -> file written at the repo root
ASSETS = {
    ("fonts", "inline_fonts.css"): "fonts.css",
    ("css", "base.css"): "base.css",
    ("css", "home.css"): "home.css",
    ("css", "route.css"): "route.css",
    ("js", "app.js"): "js/app.js",
    ("js", "map.js"): "js/map.js",
    ("js", "filters.js"): "js/filters.js",
    ("js", "webmcp.js"): "js/webmcp.js",
}

# Los .woff2 reales que referencia fonts.css (url('fonts/xxx.woff2')) --
# binarios, no pasan por read()/ASSETS (texto UTF-8). El contenido no
# cambia salvo que se cambie de tipografia, así que no llevan cache-busting
# por hash como el resto de assets.
FONT_FILES = [
    "fraunces-italic.woff2",
    "fraunces-normal.woff2",
    "sourceserif.woff2",
    "sourceserif-italic.woff2",
    "ibmplexmono-500.woff2",
    "ibmplexmono-600.woff2",
    "karla.woff2",
]


# Leaflet, servido desde el propio sitio en vez de desde un CDN. Se copia tal
# cual viene de la distribucion oficial 1.9.4: los bytes coinciden con el SRI
# que el HTML declaraba mientras venia de jsdelivr, asi que es exactamente el
# mismo codigo que ya se estaba sirviendo, solo que sin que un tercero vea la
# IP de cada visitante ni pueda dejar el mapa sin dibujar si se cae.
LEAFLET_DIR = ("vendor", "leaflet")


def copy_leaflet():
    origen = os.path.join(HERE, *LEAFLET_DIR)
    copiados = 0
    for raiz, _dirs, ficheros in os.walk(origen):
        rel = os.path.relpath(raiz, origen)
        destino = os.path.join(ROOT, *LEAFLET_DIR) if rel == "." else \
            os.path.join(ROOT, *LEAFLET_DIR, rel)
        os.makedirs(destino, exist_ok=True)
        for nombre in ficheros:
            datos = open(os.path.join(raiz, nombre), "rb").read()
            salida = os.path.join(destino, nombre)
            # Se reescribe solo si cambia: si no, cada build ensuciaria el arbol
            if not os.path.exists(salida) or open(salida, "rb").read() != datos:
                with open(salida, "wb") as f:
                    f.write(datos)
            copiados += 1
    print(f"vendor/leaflet: {copiados} ficheros")


def copy_font_files():
    out_dir = os.path.join(ROOT, "fonts")
    os.makedirs(out_dir, exist_ok=True)
    for name in FONT_FILES:
        with open(os.path.join(HERE, "fonts", name), "rb") as f:
            data = f.read()
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(data)
        print(f"wrote fonts/{name} ({len(data)} bytes)")


def add_cache_busting(page_html, versions):
    # fonts.css/home.css/route.css/js/*.js are real cached files (see the
    # module docstring), referenced by a bare filename that never changes.
    # Without this, a returning visitor can get fresh HTML paired with a
    # stylesheet or script their browser cached before the last deploy --
    # class names and markup drift apart and the page renders broken. A
    # content hash in the query string invalidates the cache exactly when
    # the file actually changes, and only then.
    def repl(m):
        attr, name = m.group(1), m.group(2)
        return f'{attr}="{name}?v={versions[name]}"'

    pattern = "|".join(re.escape(name) for name in versions)
    return re.sub(rf'(href|src)="({pattern})"', repl, page_html)


_data_versions = {}


def home_cards(src_suffix):
    """Los datos de cada ruta, leidos de las tarjetas de la portada.

    Se leen de ahi y no de un listado aparte para que no haya dos verdades: la
    tarjeta ya tiene el nombre, la actividad, la distancia y el desnivel, en el
    idioma que toca, y es lo unico que hay que tocar al anadir una ruta.
    """
    html_text = read(f"mallabia_tail{src_suffix}.html")
    cards = {}
    pattern = re.compile(
        r'<a class="route-card" href="([^"]+)" data-activity="([^"]*)"'
        r' data-distance-km="([^"]*)" data-desnivel-m="([^"]*)"([^>]*)>'
        r'[\s\S]*?<h3 class="route-card-name">(.*?)</h3>'
        r'[\s\S]*?<p class="route-card-stats">(.*?)</p>')
    for href, activity, km, desnivel, rest_attrs, name, stats in pattern.findall(html_text):
        slug = href.replace(".eu.html", "").replace(".html", "")
        tiempo_match = re.search(r'data-tiempo-corriendo-min="(\d+)"', rest_attrs)
        cards[slug] = {
            "href": href,
            "activities": set(activity.split(",")),
            "km": float(km or 0),
            "desnivel": int(desnivel or 0),
            "tiempo_real": int(tiempo_match.group(1)) if tiempo_match else None,
            "name": name.strip(),
            "stats": stats.strip(),
        }
    return cards


# Rejilla de unos 70 m. Dos rutas "se tocan" donde caen en la misma celda, que
# es una forma barata de medir cuanto camino comparten sin comparar punto a
# punto los 3.000-9.000 trkpt de cada una contra los de las otras 54.
_CELDA = 0.00063
_celdas_cache = {}


def celdas_de(slug):
    """Las celdas por las que pasa el track de una ruta."""
    if slug not in _celdas_cache:
        ruta = os.path.join(HERE, f"{slug}.gpx")
        if not os.path.exists(ruta):
            _celdas_cache[slug] = frozenset()
        else:
            puntos = ET.parse(ruta).findall(".//{*}trkpt")[::3]
            _celdas_cache[slug] = frozenset(
                (round(float(p.attrib["lat"]) / _CELDA),
                 round(float(p.attrib["lon"]) / (_CELDA * 1.37)))
                for p in puntos)
    return _celdas_cache[slug]


# Vecinas puestas a mano, para los casos en que el track no lo dice todo.
# gerea y la ruta nueva van las dos a la Cascada de Gerea, pero llegan por
# laderas distintas y solo comparten el 24% del camino, asi que por cercania
# no se encontraban. Van primero; el resto de huecos los sigue rellenando el
# calculo de siempre.
VECINAS_FIJAS = {
    "gerea": ("longaurjauziak",),
    "longaurjauziak": ("gerea",),
}


def similar_routes(slug, cards, count=2):
    """Las rutas de al lado: misma actividad, y las que mas camino comparten.

    Antes se ordenaban por parecido de kilometraje, y eso ponia al pie de una
    ruta de Mallabia otra de Markina solo porque median lo mismo. Lo que sirve
    a quien acaba de leer una ficha es saber que mas hay por esa zona, asi que
    ahora manda cuanto track comparten de verdad. Sin inventar nada: sale de
    los propios GPX.
    """
    me = cards.get(slug)
    if not me:
        return []
    mias = celdas_de(slug)
    otras = [c for s, c in cards.items() if s != slug]
    misma_actividad = [c for c in otras if c["activities"] & me["activities"]]
    candidatas = misma_actividad or otras

    def comparten(c):
        suyas = celdas_de(c["href"].replace(".eu.html", "").replace(".html", ""))
        return len(mias & suyas) / len(mias) if mias else 0.0

    # a igualdad de cercania (o si no comparten nada), la de kilometraje parecido
    candidatas.sort(key=lambda c: (-comparten(c), abs(c["km"] - me["km"])))
    fijas = [c for f in VECINAS_FIJAS.get(slug, ())
             for c in candidatas if c["href"].startswith(f + ".")]
    return (fijas + [c for c in candidatas if c not in fijas])[:count]


def add_similar_routes(page_html, page, cards, lang):
    """Cierra la ficha con dos rutas parecidas sin repetir enlaces ya usados en el texto."""
    body_match = re.search(r'<div class="body-copy">([\s\S]*?)</div>', page_html)
    used_hrefs = set()
    if body_match:
        used_hrefs = set(re.findall(r'href="([^"]+)"', body_match.group(1)))
    vecinas = [c for c in similar_routes(page, cards, count=len(cards))
               if c["href"] not in used_hrefs][:2]
    anchor = '  <div class="back-home">'
    if not vecinas or anchor not in page_html:
        return page_html
    titulo = "Rutas parecidas"
    if lang == "eu":
        titulo = eu.COMMON[titulo]
    tarjetas = "\n".join(
        f'      <a class="next-route" href="{c["href"]}">\n'
        f'        <span class="next-route-name">{c["name"]}</span>\n'
        f'        <span class="next-route-stats">{c["stats"]}</span>\n'
        f'      </a>' for c in vecinas)
    # Las fijas se declaran aqui para que el JS, que recalcula la lista en el
    # navegador, las respete en vez de tirarlas.
    fijas = " ".join(VECINAS_FIJAS.get(page, ()))
    attr = f' data-fijas="{fijas}"' if fijas else ""
    bloque = (f'  <section class="next-routes"{attr}>\n'
              f'    <p class="eyebrow">{titulo}</p>\n'
              f'    <div class="next-route-list">\n{tarjetas}\n    </div>\n'
              f'  </section>\n\n')
    return page_html.replace(anchor, bloque + anchor, 1)


def add_prev_next(page_html, page, cards, lang):
    """Pasar de una ruta a la de al lado sin volver a la portada.

    El orden es el mismo que se ve en la portada: la mas nueva primero. Es el
    unico orden que el visitante ya conoce, asi que «siguiente» le lleva a la
    tarjeta que tenia justo debajo. La primera no tiene anterior y la ultima no
    tiene siguiente: ahi se pone una sola, en vez de dar la vuelta al listado,
    que haria creer que despues de la ultima ruta hay mas.
    """
    # El tail de ahuntzen viene sin sangrar, asi que buscar la cadena con dos
    # espacios delante no lo encontraba y esa ficha se quedaba sin el paso.
    marca = re.search(r'[ \t]*<div class="back-home">', page_html)
    slugs = list(cards)
    if page not in slugs or not marca:
        return page_html
    anchor = marca.group(0)
    i = slugs.index(page)
    pasos = []
    for etiqueta, vecino, rel, flecha in (
            ("Anterior", slugs[i - 1] if i > 0 else None, "prev", "M15 18l-6-6 6-6"),
            ("Siguiente", slugs[i + 1] if i + 1 < len(slugs) else None, "next", "M9 18l6-6-6-6")):
        if not vecino:
            continue
        c = cards[vecino]
        texto = eu.COMMON[etiqueta] if lang == "eu" else etiqueta
        pasos.append(
            f'    <a class="route-step is-{rel}" href="{c["href"]}" rel="{rel}">\n'
            f'      <svg class="route-step-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none"'
            f' stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"'
            f' aria-hidden="true"><path d="{flecha}"/></svg>\n'
            f'      <span class="route-step-text">\n'
            f'        <span class="route-step-k">{texto}</span>\n'
            f'        <span class="route-step-name">{c["name"]}</span>\n'
            f'        <span class="route-step-stats">{c["stats"]}</span>\n'
            f'      </span>\n'
            f'    </a>')
    if not pasos:
        return page_html
    rotulo = "Ruta anterior y siguiente"
    if lang == "eu":
        rotulo = eu.COMMON[rotulo]
    bloque = ('  <nav class="route-steps" aria-label="' + rotulo + '">\n'
              + "\n".join(pasos) + '\n  </nav>\n\n')
    return page_html.replace(anchor, bloque + anchor, 1)


def add_ui_text(page_html, cards, lang):
    """Attach translated runtime labels to stable elements, not removed controls."""
    def attrs(values):
        return ''.join(f' data-{key}="{html.escape(eu.UI[value] if lang == "eu" else value, quote=True)}"'
                       for key, value in values.items())

    page_html = page_html.replace('id="themeToggle"', 'id="themeToggle"' + attrs({
        "label-light": "Cambiar a tema claro", "label-dark": "Cambiar a tema oscuro",
    }))
    page_html = page_html.replace('<form id="reportForm">', '<form id="reportForm"' + attrs({
        "sending": "Enviando…",
        "success": "Gracias, he recibido el aviso y lo revisaré en persona antes de actualizar la ruta.",
        "error": "No se ha podido enviar. Prueba de nuevo o escribe a trabakutik@gmail.com.",
        "subject-prefix": "Incidencia en ruta:",
    }) + '>')
    page_html = page_html.replace('<section class="finder">', '<section class="finder"' + attrs({
        "approx": "aprox.", "all-distance": "Todas", "all-desnivel": "Todos",
        "count-one": "ruta encontrada", "count-many": "rutas encontradas",
        "impossible-distance": "(rango de distancia imposible)",
        "impossible-desnivel": "(rango de desnivel imposible)",
    }) + '>')
    total_km = round(sum(c["km"] for c in cards.values()))
    total_gain = sum(c["desnivel"] for c in cards.values())
    route_word = "ibilbide" if lang == "eu" else "rutas"
    summary = (f'{len(cards)} {route_word} &middot; {total_km:,} km &middot; '
               f'{total_gain:,} m+').replace(',', '.')
    return page_html.replace('<p class="hero-compact-stats" data-route-totals></p>',
                             f'<p class="hero-compact-stats" data-route-totals>{summary}</p>')


def map_legend(cards, lang):
    """El resumen bajo el mapa, contado de las tarjetas.

    Antes eran dos parrafos con los nombres de las 30 rutas, escritos a mano:
    320 caracteres que en un movil son ocho o nueve lineas, y que se quedaban
    viejos cada vez que entraba una ruta. Contarlos aqui es mas corto de leer
    y no se puede desfasar.
    """
    bici = sum(1 for c in cards.values() if "bici" in c["activities"])
    pie = sum(1 for c in cards.values() if "senderismo" in c["activities"])
    ambas = sum(1 for c in cards.values()
                if {"bici", "senderismo"} <= c["activities"])
    t = lambda s: eu.COMMON[s] if lang == "eu" else s
    partes = [
        f'<p class="map-summary"><b>{len(cards)} {t("rutas en el mapa")}</b></p>',
        '<p class="map-legend-line">',
        f'<span class="map-legend-item"><span class="dot bici"></span>{bici} {t("en bici")}</span>',
        f'<span class="map-legend-item"><span class="dot senderismo"></span>{pie} {t("a pie")}</span>',
    ]
    if ambas:
        partes.append(f'<span class="map-legend-item">{ambas} {t("en ambas")}</span>')
    partes.append("</p>")
    return "".join(partes)


_BREADCRUMB2_RE = re.compile(r'("position": 2,\s*"name": ")([^"]*)(")')


def shorten_breadcrumb(page_html):
    """El segundo item de la miga de pan lleva el <title> completo (con el
    sufijo "&middot; Ruta de ... -- Rutas Mallabia"), cuando solo deberia
    llevar la etiqueta corta -- el nombre de la ruta, antes del primer
    " &middot; ".
    """
    def shorten(m):
        name = m.group(2)
        short = name.split(" · ", 1)[0]
        return m.group(1) + short + m.group(3)
    return _BREADCRUMB2_RE.sub(shorten, page_html, count=1)


_TOURIST_TRIP_RE = re.compile(r'("@type": "TouristTrip",[\s\S]*?"url": "[^"]*")\n(\}\n</script>)')


def add_tourist_trip_properties(page_html, name):
    """Aniade distancia/desnivel/dificultad al JSON-LD TouristTrip.

    Los lee del propio .fact ya renderizado en esta misma pagina -- son el
    mismo dato que ya se muestra, en el idioma que toca, sin duplicar la
    fuente de verdad en otro sitio.
    """
    if name == "mallabia":
        return page_html  # la portada lleva WebSite, no TouristTrip
    dist = re.search(r'<div class="fact"><span class="v">([^<]*)</span>'
                      r'<span class="k">(?:Distancia|Distantzia)</span>', page_html)
    gain = re.search(r'<div class="fact"><span class="v">([^<]*)</span>'
                      r'<span class="k">(?:Desnivel \+|Desnibela \+)</span>', page_html)
    diff = re.search(r'<div class="fact"><span class="v">([^<]*)</span>'
                      r'<span class="k">(?:Dificultad|Zailtasuna)</span>', page_html)
    if not (dist and gain and diff):
        return page_html
    props = (
        ',\n  "additionalProperty": [\n'
        f'    {{"@type": "PropertyValue", "name": "distance", "value": "{html.unescape(dist.group(1))}"}},\n'
        f'    {{"@type": "PropertyValue", "name": "elevationGain", "value": "{html.unescape(gain.group(1))}"}},\n'
        f'    {{"@type": "PropertyValue", "name": "difficulty", "value": "{html.unescape(diff.group(1))}"}}\n'
        '  ]\n'
    )
    return _TOURIST_TRIP_RE.sub(lambda m: m.group(1) + props + m.group(2), page_html, count=1)


_CARD_RE = re.compile(
    r'(<a class="route-card" href="[^"]+" data-activity="([^"]*)"'
    r' data-distance-km="([^"]*)" data-desnivel-m="([^"]*)"[^>]*>)'
    r'([\s\S]*?)(</a>)')
_TAGS_RE = re.compile(r'(<p class="route-card-tags">.*?</p>)')
_TIEMPO_REAL_RE = re.compile(r'data-tiempo-corriendo-min="(\d+)"')

# Ritmo a pie: 6 km/h en llano + 10 min por cada 100 m de desnivel positivo
# (regla de Naismith moderada). No es el ritmo del autor -- las rutas de
# senderismo del sitio se han hecho mayormente corriendo (ver CLAUDE.md) --
# sino un ritmo de caminante que cualquier visitante pueda cumplir. En bici
# no se estima: con asistencia el&eacute;ctrica variable el margen real es
# demasiado ancho para dar una cifra honesta.
WALK_KMH = 6.0
WALK_CLIMB_MIN_PER_100M = 10.0
WALK_RANGE_PCT = 0.10


def _fmt_hm(h, m):
    if h == 0:
        return f"{m} min"
    if m == 0:
        return f"{h}h"
    return f"{h}h{m:02d}"


def _fmt_minutes(total_min):
    total_min = int(round(total_min / 5.0)) * 5
    return _fmt_hm(*divmod(total_min, 60))


def _fmt_minutes_exact(total_min):
    # Tiempo real corriendo, dado por el usuario -- sin redondear, a
    # diferencia del estimado a pie: es un dato medido, no un calculo.
    return _fmt_hm(*divmod(int(total_min), 60))


def estimate_walk_time(km, desnivel):
    total_min = km / WALK_KMH * 60 + desnivel / 100.0 * WALK_CLIMB_MIN_PER_100M
    low = total_min * (1 - WALK_RANGE_PCT)
    high = total_min * (1 + WALK_RANGE_PCT)
    low_s, high_s = _fmt_minutes(low), _fmt_minutes(high)
    if low_s == high_s:
        high_s = _fmt_minutes(high + 5)
    return f"{low_s}–{high_s}"


def add_estimated_time(page_html, lang):
    """Tiempo a pie (estimado) y corriendo (real, si se ha dado) en cada
    tarjeta de la portada. El de a pie sale de sus propios
    data-distance-km/data-desnivel-m -- no hay una segunda fuente que se
    pueda desfasar. El de corriendo es un dato real, dado a mano
    (data-tiempo-corriendo-min), no calculado -- por eso se muestra sin
    redondear y como cifra unica, no como rango. No-op en las paginas que no
    tienen tarjetas.
    """
    label_pie = '<span class="k">A pie</span>'
    label_corriendo = '<span class="k">Corriendo</span>'
    if lang == "eu":
        label_pie = eu.COMMON[label_pie]
        label_corriendo = eu.COMMON[label_corriendo]

    def repl(m):
        open_tag, activity, km, desnivel, body, close_tag = m.groups()
        if "senderismo" not in set(activity.split(",")):
            return m.group(0)
        rango = estimate_walk_time(float(km or 0), int(desnivel or 0))
        nuevo = f'{label_pie} <span class="v">{rango}</span>'
        treal = _TIEMPO_REAL_RE.search(open_tag)
        if treal:
            corriendo = _fmt_minutes_exact(int(treal.group(1)))
            nuevo += f' &middot; {label_corriendo} <span class="v">{corriendo}</span>'
        body = _TAGS_RE.sub(
            lambda t: f'{t.group(1)}\n          <p class="route-card-time">{nuevo}</p>',
            body, count=1)
        return open_tag + body + close_tag

    return _CARD_RE.sub(repl, page_html)


_FACT_ITEM_RE = re.compile(r'<div class="fact">.*?</div>')


def add_route_facts_time(page_html, page, cards, lang):
    """El mismo tiempo a pie/corriendo de la tarjeta de la portada, tambien en
    la ficha de la propia ruta -- justo despues de Desnivel, en la fila de
    .facts. Una sola fuente (la tarjeta de la portada, leida por home_cards())
    para ambos sitios, asi que no hay dos cifras que puedan desfasarse.
    """
    card = cards.get(page)
    if not card or "senderismo" not in card["activities"]:
        return page_html
    label_pie = '<span class="k">A pie</span>'
    label_corriendo = '<span class="k">Corriendo</span>'
    if lang == "eu":
        label_pie = eu.COMMON[label_pie]
        label_corriendo = eu.COMMON[label_corriendo]
    rango = estimate_walk_time(card["km"], card["desnivel"])
    nuevo = f'<div class="fact"><span class="v">{rango}</span>{label_pie}</div>'
    if card["tiempo_real"]:
        corriendo = _fmt_minutes_exact(card["tiempo_real"])
        nuevo += f'\n    <div class="fact"><span class="v">{corriendo}</span>{label_corriendo}</div>'
    matches = list(_FACT_ITEM_RE.finditer(page_html))
    if len(matches) < 2:
        return page_html
    insert_at = matches[1].end()
    return page_html[:insert_at] + '\n    ' + nuevo + page_html[insert_at:]


def add_data_cache_busting(page_html):
    # Lo mismo para los tracks (data-map-src en las fichas y en el mapa
    # general). Un GPX corregido conserva el nombre del fichero, asi que
    # quien ya lo tuviera en cache podia seguir viendo el trazado viejo dentro
    # de una pagina ya actualizada, sin forma de enterarse.
    def repl(m):
        attr, path = m.group(1), m.group(2)
        if path not in _data_versions:
            with open(os.path.join(ROOT, path), "rb") as f:
                _data_versions[path] = hashlib.sha256(f.read()).hexdigest()[:8]
        return f'{attr}="{path}?v={_data_versions[path]}"'

    return re.sub(r'(data-map-src|data-track)="(data/[\w.\-]+\.json)"', repl, page_html)


def sync_trailhead_colors(cards):
    """El color de cada trazado del mapa general, sacado de su tarjeta.

    En el mapa de la portada, teal es "en bici" y violeta es "a pie", y la
    leyenda pinta sus dos puntos con esos mismos colores. Pero el color vivia
    escrito a mano en data/trailhead.json, asi que cambiar la actividad de una
    ruta en su tarjeta dejaba el trazado del color de antes -- una ruta a pie
    dibujada en azul, sin que nada avisara. Se deriva aqui de data-activity,
    que es la misma fuente que cuenta la leyenda, y ya no puede desfasarse.
    """
    path = os.path.join(ROOT, "data", "trailhead.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cambios = []
    for track in data.get("tracks", []):
        slug = track.get("href", "").replace(".eu.html", "").replace(".html", "")
        card = cards.get(slug)
        if not card:
            continue
        color = "teal" if "bici" in card["activities"] else "violet"
        if track.get("color") != color:
            cambios.append(f"{slug}: {track.get('color')} -> {color}")
            track["color"] = color
    if cambios:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
        print("data/trailhead.json: color corregido en " + ", ".join(cambios))
    return len(cambios)


def compact_route_header(page_html):
    """Put the original title and facts before the unchanged profile."""
    if '<div class="hero-chart">' not in page_html:
        return page_html
    label = re.search(r'<div class="hero-label">.*?</div>', page_html, re.S)
    facts = re.search(r'<div class="facts">.*?</div>\s*</div>', page_html, re.S)
    if not label or not facts:
        raise SystemExit('Route header is missing its label or facts')
    label_html, facts_html = label.group(), facts.group()
    page_html = page_html.replace(label_html, '', 1).replace(facts_html, '', 1)
    return page_html.replace('<div class="hero-chart">', '<div class="hero-chart">\n' + label_html + '\n' + facts_html, 1)


def main():
    copy_font_files()
    copy_leaflet()
    versions = {}
    for parts, out in ASSETS.items():
        body = read(*parts)
        out_path = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body)
        versions[out] = hashlib.sha256(body.encode("utf-8")).hexdigest()[:8]
        print(f"wrote {out_path} ({len(body)} bytes)")

    cards = {lang: home_cards(src_suffix) for lang, (src_suffix, _) in LANGS.items()}
    sync_trailhead_colors(cards["es"])

    for lang, (src_suffix, out_suffix) in LANGS.items():
        for name in PAGES:
            page_html = assemble_page(name, src_suffix)
            page_html = add_ui_text(page_html, cards[lang], lang)
            check_entities(page_html, f"{name} [{lang}]")
            page_html = add_similar_routes(page_html, name, cards[lang], lang)
            page_html = add_prev_next(page_html, name, cards[lang], lang)
            page_html = add_estimated_time(page_html, lang)
            page_html = add_route_facts_time(page_html, name, cards[lang], lang)
            page_html = compact_route_header(page_html)
            page_html = add_tourist_trip_properties(page_html, name)
            page_html = shorten_breadcrumb(page_html)
            page_html = page_html.replace(
                '<div class="map-legend" data-map-legend></div>',
                f'<div class="map-legend">{map_legend(cards[lang], lang)}</div>')
            page_html = page_html.replace(
                '<link rel="stylesheet" href="fonts.css">',
                add_manifest(lang) + '<link rel="stylesheet" href="fonts.css">')
            page_html = retarget_home_links(page_html, lang)
            page_html = add_cache_busting(page_html, versions)
            page_html = add_data_cache_busting(page_html)
            out_path = os.path.join(ROOT, out_name(name, lang))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page_html)
            print(f"wrote {out_path} ({len(page_html)} bytes) [{lang}]")

    write_legacy_eu_home()
    write_offline_page(versions)
    write_service_worker(versions)
    write_sitemap()


def add_manifest(lang):
    """El manifest y el color de barra, en cada pagina.

    Hay uno por idioma y solo por el start_url: quien instale la web desde la
    version en castellano tiene que abrirla en castellano, no en la portada en
    euskera que cuelga de la raiz.
    """
    nombre = "manifest.webmanifest" if lang == "eu" else "manifest.es.webmanifest"
    return (f'<link rel="manifest" href="{nombre}">\n'
            '<meta name="theme-color" content="#0D0D0F">\n')


def write_offline_page(versions):
    """La pagina que sale al pedir, sin cobertura, algo que no se ha visitado."""
    body = read("offline.html")
    body = add_cache_busting(body, versions)
    with open(os.path.join(ROOT, "offline.html"), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote offline.html")


# Lo que el service worker guarda nada mas instalarse: la tipografia, los
# estilos, el javascript y la pagina de sin-conexion. Son unos 210 kB y es lo
# que hace que una ficha ya visitada se vea entera y no en crudo. Las fichas y
# las fotos NO van aqui: se guardan segun se visitan, que es lo que evita
# bajarse los 400 MB de imagenes del sitio.
SHELL_EXTRA = ("offline.html", "favicon.svg", "icon-192.png",
               "vendor/leaflet/leaflet.css", "vendor/leaflet/leaflet.js")


def write_service_worker(versions):
    concha = [f"{name}?v={version}" for name, version in sorted(versions.items())]
    concha += [f"fonts/{name}" for name in sorted(FONT_FILES)]
    concha += list(SHELL_EXTRA)
    # La version de la concha es el hash de su propia lista: cambia exactamente
    # cuando cambia alguno de esos ficheros, ni antes ni despues.
    version = hashlib.sha256("\n".join(concha).encode("utf-8")).hexdigest()[:8]
    body = read("js", "sw.js")
    body = body.replace("'__VERSION__'", json.dumps(version))
    body = body.replace("__CONCHA__", json.dumps(concha, indent=2))
    with open(os.path.join(ROOT, "sw.js"), "w", encoding="utf-8") as f:
        f.write(body)
    for nombre in ("manifest.webmanifest", "manifest.es.webmanifest"):
        with open(os.path.join(ROOT, nombre), "w", encoding="utf-8") as f:
            f.write(read(nombre))
    print(f"wrote sw.js (concha {version}, {len(concha)} ficheros) + manifests")


def write_legacy_eu_home():
    """index.eu.html: la portada en euskera cuando no estaba en la raiz.

    Lleva tiempo indexada y compartida, asi que no puede quedarse en un 404 al
    mudar el euskera a la raiz. El canonical le dice a Google cual es ahora la
    buena y el refresh lleva a la persona alli sin que tenga que hacer nada.
    """
    html = (
        '<!doctype html>\n<html lang="eu">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<link rel="canonical" href="{SITE_URL}">\n'
        # El canonical va absoluto porque es la URL definitiva que se le declara
        # a Google; el salto va relativo para que funcione tambien sirviendo el
        # sitio desde otro sitio (una vista previa local, github.io).
        '<meta http-equiv="refresh" content="0; url=./">\n'
        "<title>Trabakutik</title>\n</head>\n<body>\n"
        '<p><a href="./">Trabakutik &mdash; Mallabiako ibilbideak</a></p>\n'
        "</body>\n</html>\n"
    )
    out_path = os.path.join(ROOT, "index.eu.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {out_path} ({len(html)} bytes) [redireccion heredada]")


def write_sitemap():
    # One <url> per page, with an xhtml:link alternate for every language --
    # tells Google the es/eu pages are translations of each other rather
    # than duplicate content.
    urls = []
    for name in PAGES:
        alternates = {lang: SITE_URL + out_name(name, lang) for lang in LANGS}
        if name == HOME:
            # La portada en euskera es la raiz, no "index.html" (ver
            # mallabia_head.html): es la URL que se enlaza y se comparte.
            alternates["eu"] = SITE_URL
        for loc in alternates.values():
            links = "\n".join(
                f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>'
                for lang, href in alternates.items()
            )
            urls.append(f"  <url>\n    <loc>{loc}</loc>\n{links}\n  </url>")

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n"
        "</urlset>\n"
    )
    out_path = os.path.join(ROOT, "sitemap.xml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"wrote {out_path} ({len(xml)} bytes)")


if __name__ == "__main__":
    main()
