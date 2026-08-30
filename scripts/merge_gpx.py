#!/usr/bin/env python3
"""Combines every route's src/<name>.gpx into one multi-track src/todas-las-rutas.gpx.

Run after adding a new route (once its GPX and its home-page signpost entry
both exist):

    python3 scripts/merge_gpx.py

Reads the route order and display names straight from the home page's own
signpost list (src/mallabia_tail.html), so it stays in sync with whatever is
actually published there -- no separate route list to maintain by hand. Each
source GPX becomes one <trk> in the output, named after its route, with the
original <trkseg>/<trkpt> lat/lon/ele/time copied verbatim (no resampling, no
elevation recalculation). Per-point <extensions> (heart rate, cadence,
temperature -- whatever the recording device added) are dropped: some source
files use namespace prefixes for these that aren't declared on this combined
file's root, and none of it is needed for a track-only download.
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")

OUT_PATH = os.path.join(SRC, "todas-las-rutas.gpx")

SIGNPOST_RE = re.compile(
    r'<a class="signpost-sign" href="(\w+)\.html"[^>]*>.*?'
    r'<span class="signpost-name">(.*?)</span>',
    re.S,
)
TRKSEG_RE = re.compile(r"<trkseg>.*?</trkseg>", re.S)
EXTENSIONS_RE = re.compile(r"\s*<extensions>.*?</extensions>", re.S)


def route_list():
    with open(os.path.join(SRC, "mallabia_tail.html"), encoding="utf-8") as f:
        home = f.read()
    routes = []
    for m in SIGNPOST_RE.finditer(home):
        slug, name = m.group(1), html.unescape(m.group(2))
        gpx_path = os.path.join(SRC, f"{slug}.gpx")
        if os.path.exists(gpx_path):
            routes.append((slug, name, gpx_path))
    return routes


def main():
    routes = route_list()
    if not routes:
        raise SystemExit("no routes with a GPX found via the home page signpost list")

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<gpx creator="trabakutik.com" version="1.1" '
        'xmlns="http://www.topografix.com/GPX/1/1" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
        'http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
        "  <metadata>\n"
        "    <name>Rutas Mallabia - todos los tracks</name>\n"
        "    <link href=\"https://trabakutik.com/\"><text>trabakutik.com</text></link>\n"
        "  </metadata>\n"
    ]

    for slug, name, gpx_path in routes:
        with open(gpx_path, encoding="utf-8") as f:
            gpx = f.read()
        seg_match = TRKSEG_RE.search(gpx)
        if not seg_match:
            raise SystemExit(f"{slug}.gpx: no <trkseg> found")
        # Strip device extensions (heart rate, cadence, temperature...): they can
        # reference namespace prefixes (gpxtpx, gpxx, ns2...) not declared on this
        # file's root, and aren't needed for a combined track-only download.
        trkseg = EXTENSIONS_RE.sub("", seg_match.group(0))
        escaped_name = (
            name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        parts.append(
            f"  <trk>\n    <name>{escaped_name}</name>\n    {trkseg}\n  </trk>\n"
        )

    parts.append("</gpx>\n")

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("".join(parts))

    print(f"wrote {os.path.relpath(OUT_PATH, ROOT)} ({len(routes)} tracks)")


if __name__ == "__main__":
    main()
