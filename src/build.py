#!/usr/bin/env python3
"""Rebuilds the site's HTML pages from the source templates in this folder.

Architecture:
  - Each page (mallabia = home, trabakua/iturrizuri/zenarruza = routes) is
    written as a <name>_head.html + <name>_tail.html pair, so they're small
    enough to edit directly even though the final assembled page has huge
    embedded base64 images.
  - fonts/inline_fonts.css holds the self-hosted @font-face rules
    (Fraunces, Karla, IBM Plex Mono). It's written out once as a real
    ../fonts.css file and linked from every page's <head>, so the browser
    downloads and caches it once instead of duplicating it inline per page.
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
  - To add a new route page: create <name>_head.html + <name>_tail.html,
    add "<name>" to PAGES below (home stays first), and link to it from
    wherever with a plain <a href="<name>.html">.

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
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


def assemble_page(name):
    return read(f"{name}_head.html") + read(f"{name}_tail.html")


# First entry is home; it's the one written to index.html.
PAGES = ["mallabia", "trabakua", "iturrizuri", "zenarruza"]
OUT_NAME = {"mallabia": "index.html"}  # others default to "<name>.html"


def out_name(page):
    return OUT_NAME.get(page, f"{page}.html")


def main():
    fonts_css = read("fonts", "inline_fonts.css")
    fonts_path = os.path.join(ROOT, "fonts.css")
    with open(fonts_path, "w", encoding="utf-8") as f:
        f.write(fonts_css)
    print(f"wrote {fonts_path} ({len(fonts_css)} bytes)")

    for name in PAGES:
        html = assemble_page(name)
        out_path = os.path.join(ROOT, out_name(name))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {out_path} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
