#!/usr/bin/env python3
"""Regresión mapa/perfil: Chromium real, ES/EU, ratón y eventos táctiles.

Ejecutar tras build.py: python3 scripts/test_profile_browser.py
Usa Playwright y el servidor/navegador del driver del proyecto.
"""
import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "driver", ROOT / ".claude/skills/run-rutas-mallabia/driver.py")
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

CHECK = """({fraction, touch}) => {
  const svg = document.querySelector('.chart-visual > svg');
  const rect = svg.getBoundingClientRect();
  const x = rect.left + fraction * rect.width;
  if (touch) {
    const t = new Touch({identifier: 1, target: svg, clientX:x, clientY:rect.top+30});
    for (const type of ['touchstart','touchmove'])
      svg.dispatchEvent(new TouchEvent(type,{touches:[t],changedTouches:[t],bubbles:true}));
    svg.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[t],bubbles:true}));
  } else {
    const event = new MouseEvent('mousemove',{clientX:x,bubbles:true});
    // MouseEvent redondea clientX a píxeles enteros; Touch conserva decimales.
    fraction = Math.max(0,Math.min(1,(event.clientX-rect.left)/rect.width));
    svg.dispatchEvent(event);
  }
  const layers = Object.values(window.profileMap._layers);
  const cursor = layers.find(l => l instanceof L.CircleMarker && l.options.radius === 7);
  const p = cursor.getLatLng();
  const points = window.profileData.tracks[0].points;
  const distances = [0];
  for (let i=1; i<points.length; i++)
    distances.push(distances[i-1]+L.latLng(points[i-1]).distanceTo(L.latLng(points[i])));
  const target = fraction * distances.at(-1);
  let j = 1;
  while (j < points.length-1 && distances[j] < target) j++;
  const span = distances[j]-distances[j-1];
  const mix = span ? (target-distances[j-1])/span : 0;
  const a=points[j-1], b=points[j];
  const expected = L.latLng(a[0]+(b[0]-a[0])*mix,a[1]+(b[1]-a[1])*mix);
  const text = svg.querySelector('.elev-readout text').textContent;
  // Volver del mapa al gráfico: un vértice real debe recuperar su distancia.
  const line = layers.filter(l=>l instanceof L.Polyline).at(-1);
  line.fire('mousemove',{latlng:L.latLng(points[j])});
  const cursorLine = svg.querySelector('line[stroke-dasharray]');
  const actual = Number(cursorLine.getAttribute('x1'))/1000;
  return {error:p.distanceTo(expected), text,
    bedartzandiDistance:p.distanceTo(L.latLng(43.2864,-2.535)),
    reverseError:Math.abs(actual-distances[j]/distances.at(-1)),
    latitude:p.lat, longitude:p.lng};
}"""


def main():
    count = 0
    with driver.servidor() as base, sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=driver.navegador(), args=['--no-sandbox'])
        for width in (320, 390, 768, 1280):
            context = browser.new_context(viewport={'width': width, 'height': 900},
                                          has_touch=True, service_workers='block')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.add_init_script("document.addEventListener('mapa:listo',e=>{"
                                 "window.profileMap=e.detail.map;window.profileData=e.detail.datos;});")
            for route in ('lekeitio.html', 'lekeitio.eu.html', 'oiz.html'):
                page.goto(base + '/' + route, wait_until='domcontentloaded')
                page.wait_for_function('window.profileMap')
                page.locator('.chart-visual').scroll_into_view_if_needed()
                for fraction in (0, .0887, .398, .4481, .4985, .75, 1):
                    for touch in (False, True):
                        result = page.evaluate(CHECK, {'fraction': fraction, 'touch': touch})
                        assert result['error'] < .01, (route, width, result)
                        assert result['reverseError'] < 1e-8, (route, width, result)
                        assert ' km' in result['text'] and 'NaN' not in result['text'], result
                        if route.startswith('lekeitio') and touch and fraction == .4985:
                            assert result['bedartzandiDistance'] < 25, result
                            assert '697 m' in result['text'] or '696 m' in result['text'], result
                        count += 1
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, width)
            # Sin cotas en la ficha ni alturas en el track: los km siguen visibles.
            no_heights = json.loads((ROOT / 'data/lekeitio.json').read_text())
            for track in no_heights['tracks']:
                track['points'] = [p[:2] for p in track['points']]
            page.route('**/data/lekeitio.json*', lambda route: route.fulfill(json=no_heights))
            page.goto(base + '/lekeitio.html', wait_until='domcontentloaded')
            page.wait_for_function('window.profileMap')
            result = page.evaluate(CHECK, {'fraction': .5, 'touch': True})
            assert result['text'].endswith(' km'), result
            assert not errors, errors
            context.close()
        browser.close()
    print(f'CORRECTO: {count} comprobaciones bidireccionales, ES/EU, cuatro anchos; lectura sin alturas.')


if __name__ == '__main__':
    main()
