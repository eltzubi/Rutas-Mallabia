#!/usr/bin/env python3
"""Read-only regression checks. Run after make_eu.py and build.py; stdlib only."""
import hashlib
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

# Margenes de las comprobaciones contra el GPX. La distancia sale del track con
# una precision de metros, asi que basta un 1% (hoy el peor caso es 0,7%). Las
# altitudes minima y maxima son un solo punto del track, no una suma, asi que no
# acumulan el ruido del GPS: 8 m cubre las diferencias de redondeo entre fuentes
# (hoy el peor caso son 6 m).
#
# El DESNIVEL ACUMULADO no se comprueba a proposito: sumar los repechos del GPX
# en crudo se va hasta un 43% de la cifra de la ficha, y ni suavizando baja del
# 9% de media. Las fichas lo toman de la fuente de la ruta (Wikiloc, la
# organizacion de la carrera), y la propia ficha lo advierte. Una comprobacion
# asi solo daria falsas alarmas.
TOLERANCIA_KM_PCT = 1.0
TOLERANCIA_ALTITUD_M = 8.0

_FACT = r'<span class="v">{}</span><span class="k">{}</span>'
_CIFRA = r'([\d.,]+)'


def numero(texto):
    """'1.020,5' -> 1020.5 (miles con punto, decimales con coma)."""
    return float(texto.replace('.', '').replace(',', '.'))


def haversine(lat1, lon1, lat2, lon2):
    radio = 6371000.0
    f1, f2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin(math.radians(lat2 - lat1) / 2) ** 2
         + math.cos(f1) * math.cos(f2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * radio * math.asin(math.sqrt(a))


def datos_gpx(ruta):
    """(km totales, altitud minima, altitud maxima) del track real."""
    puntos = [(float(p.attrib['lat']), float(p.attrib['lon']), float(p.find('{*}ele').text))
              for p in ET.parse(ruta).findall('.//{*}trkpt')]
    metros = sum(haversine(a[0], a[1], b[0], b[1]) for a, b in zip(puntos, puntos[1:]))
    alturas = [e for _, _, e in puntos]
    return metros / 1000, min(alturas), max(alturas)


def body_copy(texto):
    """El cuerpo de la ficha, sin el mapa ni lo que viene detras."""
    inicio = texto.find('<div class="body-copy">')
    if inicio < 0:
        return ''
    resto = texto[inicio:]
    fin = resto.find('<section class="map-section"')
    return resto[:fin] if fin > 0 else resto


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'document', 'attrs': {}, 'children': []}
        self.stack = [self.root]
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'children': []}
        self.stack[-1]['children'].append(node)
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1]['children'].append(text)


def text(node):
    return node if isinstance(node, str) else ''.join(text(c) for c in node['children'])


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--fixture':
        print(json.dumps(Document((ROOT / sys.argv[2]).read_text()).root))
        return
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT / 'src'))
    import build
    checks = 0

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    for lang, (_, suffix) in build.LANGS.items():
        for page in build.PAGES:
            filename = build.out_name(page, lang)
            document = Document((ROOT / filename).read_text())
            nodes = document.nodes
            if page != 'aviso-legal':   # la unica pagina sin mapa
                require(any('leaflet.css' in n['attrs'].get('href', '') for n in nodes),
                        f'{filename}: missing Leaflet stylesheet')
            theme = next(n for n in nodes if n['attrs'].get('id') == 'themeToggle')
            require(all(theme['attrs'].get(k) for k in ('data-label-light', 'data-label-dark')),
                    f'{filename}: missing theme translations')
            require(theme['attrs']['data-label-dark'] ==
                    ('Aldatu gai ilunera' if lang == 'eu' else 'Cambiar a tema oscuro'), filename)
            if page not in ('mallabia', 'aviso-legal'):
                form = next(n for n in nodes if n['attrs'].get('id') == 'reportForm')
                require(all(form['attrs'].get('data-' + k) for k in ['sending', 'success', 'error', 'subject-prefix']),
                        f'{filename}: missing report translations')
                section = next(n for n in nodes if 'map-section' in n['attrs'].get('class', '').split())
                def walk(n):
                    if isinstance(n, dict):
                        yield n
                        for c in n['children']:
                            yield from walk(c)
                names = [n for n in walk(section) if 'elev-legend-item' in n['attrs'].get('class', '').split()]
                data = json.loads((ROOT / 'data' / f'{page}.json').read_text())
                require(len(names) == len(data.get('waypoints', [])), f'{filename}: waypoint/legend mismatch')
            elif page == 'mallabia':
                cards = [n for n in nodes if n['attrs'].get('class') == 'route-card']
                # PAGES lleva la portada y las paginas que no son rutas (aviso-legal),
                # y ninguna de las dos tiene tarjeta.
                rutas = [p for p in build.PAGES if p not in ('mallabia', 'aviso-legal')]
                require(len(cards) == len(rutas), f'{filename}: missing card')
                for slug in ('muniozguren', 'iruzubieta'):
                    card = next(n for n in cards if n['attrs'].get('href') == slug + suffix + '.html')
                    require(set(card['attrs']['data-activity'].split(',')) == {'bici', 'senderismo'}, slug)
                total = next(n for n in nodes if 'data-route-totals' in n['attrs'])
                km = round(sum(float(n['attrs']['data-distance-km']) for n in cards))
                gain = sum(int(n['attrs']['data-desnivel-m']) for n in cards)
                expected = f'{len(cards)} {"ibilbide" if lang == "eu" else "rutas"} · {km:,} km · {gain:,} m+'.replace(',', '.')
                require(text(total) == expected, f'{filename}: stale totals')
                finder = next(n for n in nodes if n['attrs'].get('class') == 'finder')
                require(finder['attrs']['data-count-many'] ==
                        ('ibilbide aurkitu dira' if lang == 'eu' else 'rutas encontradas'), filename)

    # --- las cifras de la ficha contra el track real -----------------------
    # Aqui es donde se habria visto sola la tanda de rutas que daban mas
    # kilometros que su GPX, en vez de descubrirla leyendo fichas a mano.
    for page in build.PAGES:
        if page in ('mallabia', 'aviso-legal'):
            continue
        gpx = ROOT / 'src' / f'{page}.gpx'
        require(gpx.exists(), f'{page}: falta su GPX')
        km_real, alt_min, alt_max = datos_gpx(gpx)
        html = (ROOT / f'{page}.html').read_text()

        ficha = re.search(_FACT.format(_CIFRA + r'\s*km', 'Distancia'), html)
        require(ficha is not None, f'{page}.html: no encuentro la distancia')
        km_ficha = numero(ficha.group(1))
        desvio = abs(km_ficha - km_real) / km_real * 100
        require(desvio <= TOLERANCIA_KM_PCT,
                f'{page}.html: distancia {km_ficha} km, el GPX da {km_real:.2f} km ({desvio:.1f}%)')

        for etiqueta, real in (('Altitud m&iacute;n.', alt_min), ('Altitud m&aacute;x.', alt_max)):
            m = re.search(_FACT.format(_CIFRA + r'\s*m', re.escape(etiqueta)), html)
            if m is None:
                continue          # no todas las fichas llevan las dos altitudes
            require(abs(numero(m.group(1)) - real) <= TOLERANCIA_ALTITUD_M,
                    f'{page}.html: {etiqueta} {m.group(1)} m, el GPX da {real:.0f} m')

    # --- castellano y euskera, el mismo cuerpo -----------------------------
    # La ficha en euskera se genera de la castellana, asi que el markup tiene
    # que salir igual. Un <a> o un <picture> de menos significa que una clave de
    # eu.py se ha comido una referencia a otra ruta o una imagen responsive
    # (a ahuntzen le faltaban las seis). Las NEGRITAS no se comparan: el autor
    # marca a veces un nombre distinto en cada idioma, y es decision suya.
    for page in build.PAGES:
        if page in ('mallabia', 'aviso-legal'):
            continue
        es = (ROOT / f'{page}.html').read_text()
        eu_html = (ROOT / f'{page}.eu.html').read_text()
        for etiqueta in ('a', 'picture'):
            patron = rf'<{etiqueta}\b'
            require(len(re.findall(patron, body_copy(es))) ==
                    len(re.findall(patron, body_copy(eu_html))),
                    f'{page}: el cuerpo en euskera no lleva los mismos <{etiqueta}>')
        require(len(re.findall(r'<picture\b', es)) == len(re.findall(r'<picture\b', eu_html)),
                f'{page}: numero de <picture> distinto entre idiomas')
        require('<picture' in es, f'{page}.html: ninguna imagen responsive')

    for gpx in (ROOT / 'src').glob('*.gpx'):
        points = [(float(p.attrib['lon']), float(p.attrib['lat']), float(p.find('{*}ele').text))
                  for p in ET.parse(gpx).findall('.//{*}trkpt')]
        kml = gpx.with_suffix('.kml')
        coords = ET.parse(kml).find('.//{*}coordinates').text.split()
        require(points == [tuple(map(float, p.split(','))) for p in coords], f'{kml.name}: stale coordinates/elevations')
    with zipfile.ZipFile(ROOT / 'src/todas-las-rutas.zip') as archive:
        require(archive.testzip() is None, 'ZIP CRC failed')
        hashes = {hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
        for gpx in (ROOT / 'src').glob('*.gpx'):
            require(hashlib.sha256(gpx.read_bytes()).hexdigest() in hashes, f'ZIP omits {gpx.name}')
    for src, target in build.ASSETS.items():
        require((ROOT / 'src').joinpath(*src).read_bytes() == (ROOT / target).read_bytes(), f'Stale asset: {target}')
    print(f'OK: {checks} comprobaciones de páginas, idiomas, marcadores, descargas y assets.')


if __name__ == '__main__':
    main()
