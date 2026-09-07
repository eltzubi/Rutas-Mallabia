#!/usr/bin/env python3
"""Read-only regression checks. Run after make_eu.py and build.py; stdlib only."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


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
            filename = build.out_name(page, suffix)
            document = Document((ROOT / filename).read_text())
            nodes = document.nodes
            require(any('leaflet.css' in n['attrs'].get('href', '') for n in nodes),
                    f'{filename}: missing Leaflet stylesheet')
            theme = next(n for n in nodes if n['attrs'].get('id') == 'themeToggle')
            require(all(theme['attrs'].get(k) for k in ('data-label-light', 'data-label-dark')),
                    f'{filename}: missing theme translations')
            require(theme['attrs']['data-label-dark'] ==
                    ('Aldatu gai ilunera' if lang == 'eu' else 'Cambiar a tema oscuro'), filename)
            if page != 'mallabia':
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
            else:
                cards = [n for n in nodes if n['attrs'].get('class') == 'route-card']
                require(len(cards) == len(build.PAGES) - 1, f'{filename}: missing card')
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
