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
PAGES = ["mallabia", "trabakua", "iturrizuri", "zenarruza", "osma", "gerea", "zengotitagane", "oiz", "arietzu", "urko", "sancristobal", "iturreta", "egoarbitza", "urregarai", "kalamua", "mundiokokoba", "iruzubieta", "mendibil", "arteta", "goita", "hirutxikiak", "zaldibar", "maguna", "7pago", "7pago16", "barinaga", "muniozguren", "exigente", "potrera", "aixola", "intxorta", "artetaasuntza", "trabakuamallabia", "betzun", "sarrimendi", "longa", "zengotitaosmagain", "axmakuriturrizuri", "amaraune", "astarlokoatxa", "garaimaguna", "sanpedrobidarte", "sancristobaloiz", "axmakurandikoa", "markinabolibar", "asuntzabira", "gereaoculta", "sancristobalgaraiandikoa", "zengotitaiturzuri", "santamanazarandikoa", "aviso-legal"]
OUT_NAME = {"mallabia": "index"}  # others default to their own name

# lang code -> (source-file suffix, output-file suffix)
LANGS = {"es": ("", ""), "eu": (".eu", ".eu")}

SITE_URL = "https://trabakutik.com/"


def out_name(page, out_suffix):
    return f"{OUT_NAME.get(page, page)}{out_suffix}.html"


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
    "ibmplexmono-500.woff2",
    "ibmplexmono-600.woff2",
    "karla.woff2",
]


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


def similar_routes(slug, cards, count=2):
    """Las rutas mas parecidas: misma actividad, y las mas cercanas en distancia.

    Sin inventar nada -- la semejanza sale de los datos reales del GPX que ya
    llevan las tarjetas.
    """
    me = cards.get(slug)
    if not me:
        return []
    otras = [c for s, c in cards.items() if s != slug]
    misma_actividad = [c for c in otras if c["activities"] & me["activities"]]
    candidatas = misma_actividad or otras
    candidatas.sort(key=lambda c: abs(c["km"] - me["km"]))
    return candidatas[:count]


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
    bloque = (f'  <section class="next-routes">\n'
              f'    <p class="eyebrow">{titulo}</p>\n'
              f'    <div class="next-route-list">\n{tarjetas}\n    </div>\n'
              f'  </section>\n\n')
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


def main():
    copy_font_files()
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
            page_html = add_estimated_time(page_html, lang)
            page_html = add_route_facts_time(page_html, name, cards[lang], lang)
            page_html = add_tourist_trip_properties(page_html, name)
            page_html = shorten_breadcrumb(page_html)
            page_html = page_html.replace(
                '<div class="map-legend" data-map-legend></div>',
                f'<div class="map-legend">{map_legend(cards[lang], lang)}</div>')
            page_html = page_html.replace(
                '<link rel="stylesheet" href="fonts.css">',
                '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n'
                '<link rel="stylesheet" href="fonts.css">')
            page_html = add_cache_busting(page_html, versions)
            page_html = add_data_cache_busting(page_html)
            out_path = os.path.join(ROOT, out_name(name, out_suffix))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page_html)
            print(f"wrote {out_path} ({len(page_html)} bytes) [{lang}]")

    write_sitemap()


def write_sitemap():
    # One <url> per page, with an xhtml:link alternate for every language --
    # tells Google the es/eu pages are translations of each other rather
    # than duplicate content.
    urls = []
    for name in PAGES:
        alternates = {
            lang: SITE_URL + out_name(name, out_suffix)
            for lang, (_, out_suffix) in LANGS.items()
        }
        if name == "mallabia":
            # La portada es la unica pagina cuyo canonical apunta a la raiz
            # (ver mallabia_head.html), no a su propio nombre de fichero.
            alternates["es"] = SITE_URL
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
