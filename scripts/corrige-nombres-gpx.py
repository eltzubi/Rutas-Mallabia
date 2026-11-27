from pathlib import Path
import json
import re
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'data/rutas.json').read_text())['es']
changed = 0
for slug, entry in catalog.items():
    path = root / 'src' / (slug + '.gpx')
    prior = path.read_bytes()
    text = prior.decode('utf-8')
    title = entry['n']
    name = '<name>' + escape(title) + '</name>'
    def rename_body(match):
        head, body = match.groups()
        new, count = re.subn(r'^(\s*)<name>(?:<!\[CDATA\[.*?\]\]>|[^<]*)</name>', lambda m: m[1] + name, body, count=1)
        if not count:
            pad = re.match(r'\s*', body)[0]
            new = pad + name + body
        return head + new
    text, count = re.subn(r'(<metadata>)([\s\S]*?)(?=</metadata>)', rename_body, text)
    if not count:
        text = re.sub(r'(<gpx\b[^>]*>)', lambda m: m[0] + '\n  <metadata>' + name + '</metadata>', text, count=1)
    text = re.sub(r'(<trk>)([\s\S]*?)(?=<trkseg(?:\s|>))', rename_body, text)
    data = text.encode('utf-8')
    old, new = ET.fromstring(prior), ET.fromstring(data)
    assert new.findtext('./{*}metadata/{*}name') == title, slug
    tracks = new.findall('./{*}trk')
    assert tracks and all(t.findtext('./{*}name') == title for t in tracks), slug
    # Compare every XML element except the title metadata being corrected.
    for tree in (old, new):
        meta = tree.find('./{*}metadata')
        if meta is not None:
            title_node = meta.find('./{*}name')
            if title_node is not None:
                meta.remove(title_node)
            if not len(meta):
                tree.remove(meta)
        for track in tree.findall('./{*}trk'):
            title_node = track.find('./{*}name')
            if title_node is not None:
                track.remove(title_node)
    def elements(node):
        return (node.tag, node.attrib, (node.text or '').strip(), tuple(map(elements, node)))
    assert elements(old) == elements(new), slug
    if data != prior:
        path.write_bytes(data)
        changed += 1
print(f'{changed} GPX con nombres corregidos; los {len(catalog)} conservan todos sus datos de recorrido.')
