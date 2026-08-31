#!/usr/bin/env python3
"""Generates one src/<name>.kml per route, converted from its src/<name>.gpx.

Run after adding a new route's GPX (once its home-page signpost entry exists):

    python3 scripts/make_kml.py

Reads the route order and display names straight from the home page's own
signpost list (src/mallabia_tail.html), same as scripts/bundle_gpx.py, so it
stays in sync with whatever is actually published there -- no separate route
list to maintain by hand.

Each KML mirrors the GPX one-to-one: same track name, same lat/lon/ele
points, no resampling or simplification. Elevation is written as real
altitude with <altitudeMode>clampToGround</altitudeMode> so it renders
correctly (draped on terrain) in Google Earth and other KML viewers that
don't have accurate elevation data of their own.
"""
import html
import os
import re
import xml.sax.saxutils as sx

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")

SIGNPOST_RE = re.compile(
    r'<a class="signpost-sign" href="(\w+)\.html"[^>]*>.*?'
    r'<span class="signpost-name">(.*?)</span>',
    re.S,
)

TRKPT_RE = re.compile(
    r'<trkpt lat="([\-\d.]+)" lon="([\-\d.]+)">\s*(?:<ele>([\-\d.]+)</ele>)?',
)


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


def gpx_to_coordinates(gpx_path):
    with open(gpx_path, encoding="utf-8") as f:
        text = f.read()
    coords = []
    for m in TRKPT_RE.finditer(text):
        lat, lon, ele = m.group(1), m.group(2), m.group(3)
        coords.append(f"{lon},{lat},{ele or '0'}")
    if not coords:
        raise SystemExit(f"\n{gpx_path}: no <trkpt> found -- is this a valid GPX track?")
    return coords


def write_kml(slug, name, coords):
    escaped_name = sx.escape(name)
    kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>{escaped_name}</name>
<Style id="track">
<LineStyle><color>ff2fe0f5</color><width>4</width></LineStyle>
</Style>
<Placemark>
<name>{escaped_name}</name>
<styleUrl>#track</styleUrl>
<LineString>
<tessellate>1</tessellate>
<altitudeMode>clampToGround</altitudeMode>
<coordinates>{" ".join(coords)}</coordinates>
</LineString>
</Placemark>
</Document>
</kml>
'''
    out_path = os.path.join(SRC, f"{slug}.kml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(kml)
    return out_path


def main():
    routes = route_list()
    if not routes:
        raise SystemExit("no routes with a GPX found via the home page signpost list")
    for slug, name, gpx_path in routes:
        coords = gpx_to_coordinates(gpx_path)
        out_path = write_kml(slug, name, coords)
        print(f"wrote {os.path.relpath(out_path, ROOT)} ({len(coords)} points)")


if __name__ == "__main__":
    main()
