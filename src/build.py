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
PAGES = ["mallabia", "trabakua", "iturrizuri", "zenarruza", "osma", "gerea", "zengotitagane", "oiz", "arietzu", "urko", "sancristobal", "iturreta", "egoarbitza", "urregarai", "kalamua", "mundiokokoba", "iruzubieta", "mendibil", "arteta", "goita", "hirutxikiak", "zaldibar", "maguna", "7pago", "7pago16", "barinaga", "muniozguren", "exigente", "potrera", "aixola", "intxorta", "artetaasuntza"]
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
        r' data-distance-km="([^"]*)" data-desnivel-m="([^"]*)"'
        r'[\s\S]*?<h3 class="route-card-name">(.*?)</h3>'
        r'[\s\S]*?<p class="route-card-stats">(.*?)</p>')
    for href, activity, km, desnivel, name, stats in pattern.findall(html_text):
        slug = href.replace(".eu.html", "").replace(".html", "")
        cards[slug] = {
            "href": href,
            "activities": set(activity.split(",")),
            "km": float(km or 0),
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
    """Cierra la ficha con dos rutas parecidas en vez de con un enlace al indice."""
    vecinas = similar_routes(page, cards)
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
            check_entities(page_html, f"{name} [{lang}]")
            page_html = add_similar_routes(page_html, name, cards[lang], lang)
            page_html = page_html.replace(
                '<div class="map-legend" data-map-legend></div>',
                f'<div class="map-legend">{map_legend(cards[lang], lang)}</div>')
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
