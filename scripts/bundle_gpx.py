#!/usr/bin/env python3
"""Bundles every route's src/<name>.gpx into one src/todas-las-rutas.zip.

Run after adding a new route (once its GPX and its home-page signpost entry
both exist):

    python3 scripts/bundle_gpx.py

Reads the route order and display names straight from the home page's own
signpost list (src/mallabia_tail.html), so it stays in sync with whatever is
actually published there -- no separate route list to maintain by hand.

Ships a ZIP of the original, untouched per-route GPX files rather than one
combined multi-track GPX: Garmin devices (and plenty of other GPS units/apps)
only import the *first* track from a multi-track file, silently dropping the
rest, so a single merged GPX looks fine in a text/XML viewer but is useless
for someone trying to load every route onto a device. A ZIP of one-track-per-
file GPXs is the form every device/app actually handles correctly.

Each entry is named after its route's own title (e.g. "Trabakua, Aixola y
Berriz.gpx"), the same name already used for that route's individual GPX
download link on its own page -- only characters illegal in a filename get
stripped, so the readable title (commas, accents and all) survives.
"""
import html
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")

OUT_PATH = os.path.join(SRC, "todas-las-rutas.zip")

# Las tarjetas de la portada son la lista de rutas: el antiguo bloque de
# "signpost" desaparecio del diseno hace tiempo y este patron dejo de encontrar
# nada, asi que el ZIP y los KML se quedaron congelados sin avisar.
CARD_RE = re.compile(
    r'<a class="route-card" href="([\w]+)\.html"[^>]*>.*?'
    r'<h3 class="route-card-name">(.*?)</h3>',
    re.S,
)


def route_list():
    with open(os.path.join(SRC, "mallabia_tail.html"), encoding="utf-8") as f:
        home = f.read()
    routes = []
    for m in CARD_RE.finditer(home):
        slug, name = m.group(1), html.unescape(m.group(2))
        gpx_path = os.path.join(SRC, f"{slug}.gpx")
        if os.path.exists(gpx_path):
            routes.append((slug, name, gpx_path))
    return routes


def main():
    routes = route_list()
    if not routes:
        raise SystemExit("no routes with a GPX found via the home page signpost list")

    if os.path.exists(OUT_PATH):
        os.remove(OUT_PATH)

    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for slug, name, gpx_path in routes:
            # Strip only characters illegal in a filename; keep the title
            # otherwise intact (accents, commas and all).
            safe_name = re.sub(r'[\\/:*?"<>|]', "", name).strip()
            zf.write(gpx_path, arcname=f"{safe_name}.gpx")

    print(f"wrote {os.path.relpath(OUT_PATH, ROOT)} ({len(routes)} files)")


if __name__ == "__main__":
    main()
