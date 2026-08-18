#!/usr/bin/env python3
"""Generates the Basque *_tail.eu.html / *_head.eu.html from the Spanish ones.

Run it after editing any Spanish text:

    python3 src/i18n/make_eu.py

It applies src/i18n/eu.py's translation tables and REFUSES to write anything
if a translation key no longer appears in the Spanish source -- that is the
signal that a Spanish string changed and its Basque counterpart is now stale.
Fix eu.py, re-run, then run build.py.

The Basque pages are generated, not hand-edited: to change Basque wording,
edit src/i18n/eu.py and re-run this script.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import eu  # noqa: E402

PAGES = ["mallabia", "trabakua", "iturrizuri", "zenarruza"]
ROUTE_PAGES = {"trabakua", "iturrizuri", "zenarruza"}

# es filename -> eu filename, for the cross-language links
EU_OF = {"index.html": "index.eu.html"}
for _p in ROUTE_PAGES:
    EU_OF[f"{_p}.html"] = f"{_p}.eu.html"


# Spanish words that must never survive into a Basque page. Deliberately
# words with no Basque homograph, so a hit is always a real miss.
SPANISH_TELLS = [
    "Distancia", "Desnivel", "Superficie", "Actividad", "Salida", "Circuito",
    "Sendero", "Senderismo", "Bici", "Mixta", "Ampliar", "Cerrar", "Volver",
    "Descargar", "ruta", "Ruta", "camino", "hacia", "desde", "sobre el terreno",
    "Mapa", "Puerto", "aparcamiento", "aparcar", "cascada", "Fuente",
    "Monasterio", "Ermita", "Dolmen", "Refugio", "Borda abandonada",
    "Altitud", "perfil real", "tema oscuro", "tema claro",
]


def tables_for(page):
    """(shared, specific) -- shared keys may legitimately be absent from a
    given page; every key in the page's own table must be present."""
    shared = dict(eu.COMMON)
    if page in ROUTE_PAGES:
        shared.update(eu.ROUTE)
    return shared, dict(eu.PAGE_STRINGS[page])


def translate(text, shared, specific, page):
    missing = [k for k in specific if k not in text]
    if missing:
        raise SystemExit(
            f"\n{page}: {len(missing)} translation key(s) no longer found in the Spanish source.\n"
            "The Spanish text changed -- update src/i18n/eu.py to match, then re-run.\n\n"
            + "\n".join(f"  - {k[:110]!r}" for k in missing)
        )
    table = dict(shared)
    table.update(specific)
    # Longest first, so a short key can't eat part of a longer one.
    for k in sorted(table, key=len, reverse=True):
        text = text.replace(k, table[k])
    return text


def check_no_spanish(text, page):
    """Catch anything the tables forgot: strip markup, look for Spanish."""
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)          # tags out, attribute text too
    body = re.sub(r"https?://\S+", " ", body)      # URLs are not prose
    found = sorted({w for w in SPANISH_TELLS if re.search(r"\b" + re.escape(w) + r"\b", body)})
    if found:
        raise SystemExit(
            f"\n{page}: Spanish text survived into the Basque page: {found}\n"
            "Add the missing string to src/i18n/eu.py and re-run."
        )


def main():
    for page in PAGES:
        # ---- tail ----
        es_path = os.path.join(SRC, f"{page}_tail.html")
        with open(es_path, encoding="utf-8") as f:
            es = f.read()

        shared, specific = tables_for(page)
        out = translate(es, shared, specific, page)

        # Order matters: retarget ordinary navigation first, THEN flip the
        # language switch. Doing it the other way round turns the switch's
        # freshly-written href="index.html" straight back into the Basque one.
        for es_file, eu_file in EU_OF.items():
            out = out.replace(f'href="{es_file}"', f'href="{eu_file}"')

        out = re.sub(
            r'<a class="lang-switch" href="([\w.]+)\.eu\.html" hreflang="eu" lang="eu" title="Euskaraz">EU</a>',
            r'<a class="lang-switch" href="\1.html" hreflang="es" lang="es" title="En castellano">ES</a>',
            out,
        )

        check_no_spanish(out, page)

        eu_path = os.path.join(SRC, f"{page}_tail.eu.html")
        with open(eu_path, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote {os.path.relpath(eu_path, SRC)}")

        # ---- head ----
        with open(os.path.join(SRC, f"{page}_head.html"), encoding="utf-8") as f:
            head = f.read()
        head = head.replace('<html lang="es">', '<html lang="eu">')
        head = re.sub(r"<title>.*?</title>", f"<title>{eu.TITLES[page]}</title>", head)
        with open(os.path.join(SRC, f"{page}_head.eu.html"), "w", encoding="utf-8") as f:
            f.write(head)
        print(f"wrote {page}_head.eu.html")


if __name__ == "__main__":
    main()
