// EL LAPIZ, EN UN NAVEGADOR DE VERDAD Y CON LA RED DE CAMINOS ENTERA.
//
// Lo que prueba, y por que:
//
// 1. QUE LA RED SE PREPARE. Son 41.632 cruces y 52.567 tramos; si la
//    construccion se pasa de tiempo o de memoria, el lapiz no abre.
// 2. QUE SE PUEDA DIBUJAR DONDE NO PASA NINGUNA RUTA PUBLICADA. Es la razon
//    de ser del cambio: con la red vieja -hecha solo con los tracks- el
//    toque devolvia -1 y salia «ahi no pasa ninguna ruta». Los dos puntos de
//    abajo estan en el monte al oeste de Mallabia, a mas de 800 m de
//    cualquier ruta de la web.
// 3. QUE SOBRE UNA RUTA PUBLICADA SIGA HACIENDO LO DE ANTES, alturas
//    incluidas: las cotas no salen de OpenStreetMap -no las tiene- sino de
//    data/alturas.json, por celdas de 50 m.
//
// Se ejecuta con: node scripts/test_lapiz.cjs
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const tipos = { '.html': 'text/html', '.js': 'text/javascript',
  '.json': 'application/json', '.css': 'text/css', '.woff2': 'font/woff2',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png',
  '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const limpio = decodeURIComponent(req.url.split('?')[0]).replace(/^\//, '');
  const f = path.join(root, limpio || 'index.html');
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' });
    res.end(d);
  });
});

// Dos puntos a mas de 800 m de cualquier ruta publicada, y dos del km 6 y el
// km 8 de galdaramiño.
const LEJOS = [[43.17579, -2.63351], [43.16049, -2.62573]];
const SOBRE_RUTA = [[43.18117, -2.53896], [43.17174, -2.52374]];

(async () => {
  let browser;
  try {
    await new Promise(r => server.listen(0, r));
    const base = 'http://127.0.0.1:' + server.address().port + '/';
    browser = await chromium.launch({
      executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
      args: ['--no-sandbox'] });
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    // Ni teselas ni tiempo: esto mide el lapiz, no la red del que lo prueba.
    for (const patron of ['**://*.tile.*/**', '**://tile.openstreetmap.org/**',
                          '**://*.ign.es/**', '**://api.open-meteo.com/**',
                          '**://opendata.euskadi.eus/**',
                          '**://*.arcgisonline.com/**', '**://*.geo.euskadi.eus/**']) {
      await ctx.route(patron, r => r.abort());
    }
    await ctx.addInitScript(() => {
      document.addEventListener('mapa:listo', e => { window.__m = e.detail.map; });
    });
    const p = await ctx.newPage();
    const errores = [];
    p.on('pageerror', e => errores.push(e.message));

    await p.goto(base, { waitUntil: 'domcontentloaded' });
    assert.equal(await p.locator('.hero-compact').getByRole('link',{name:'Crear ruta',exact:true}).count(),0);
    await p.evaluate(() => document.querySelector('[data-view="map"]').click());
    await p.waitForSelector('.map-draw-btn', {timeout:60000});
    const t0 = Date.now();
    await p.click('.map-draw-btn');
    await p.locator('.draw-plan-activity').waitFor();
    await p.waitForFunction(() => {
      const r = document.querySelector('.draw-plan-activity').getBoundingClientRect();
      return r.top >= 0 && r.bottom <= innerHeight;
    });
    await p.waitForFunction(
      () => { const m = document.querySelector('.draw-readout');
              return m && !/Preparando|prestatzen/.test(m.textContent); },
      null, { timeout: 120000 });
    const tardo = Date.now() - t0;
    assert(tardo < 30000, 'la red tarda ' + tardo + ' ms en estar lista');

    const toca = async pares => {
      await p.evaluate(([a, b]) => {
        window.__m.fire('click', { latlng: { lat: a[0], lng: a[1] } });
        window.__m.fire('click', { latlng: { lat: b[0], lng: b[1] } });
      }, pares);
      await p.waitForTimeout(500);
      return (await p.locator('.draw-readout').textContent()).replace(/\s+/g, ' ');
    };

    let texto = await toca(LEJOS);
    let km = Number((texto.match(/([\d,]+) km/) || [])[1].replace(',', '.'));
    assert(km > 1.5 && km < 4,
      'donde no hay ruta publicada tiene que salir camino, y salio: ' + texto);
    assert.equal(await p.evaluate(() => document.querySelectorAll('.draw-dot').length), 2);

    await p.evaluate(() => {
      document.querySelectorAll('.draw-tools button').forEach(b => {
        if (/Borrar|Ezabatu/.test(b.getAttribute('title') || '')) b.click();
      });
    });
    await p.waitForTimeout(200);

    texto = await toca(SOBRE_RUTA);
    km = Number((texto.match(/([\d,]+) km/) || [])[1].replace(',', '.'));
    assert(km > 1.5 && km < 2.5, 'sobre galdaramiño: ' + texto);
    // El desnivel del TOTAL, no el del ultimo tramo: la linea del total es la
    // unica que lleva «aprox.» detras, y es la que desaparece si las alturas
    // no llegan. Mirando cualquier «+x / -y» colaba un trazado sin cotas,
    // porque el del ultimo tramo sale igual con ceros.
    const cotas = texto.match(/\+(\d+) \/ -(\d+) m aprox/);
    assert(cotas, 'sobre una ruta publicada tiene que traer alturas: ' + texto);
    assert(Number(cotas[1]) + Number(cotas[2]) > 20,
      'y no pueden ser cero: ' + texto);

    p.on('dialog', d => d.accept());
    const perfiles = [];
    await ctx.route('https://valhalla1.openstreetmap.de/**', r => r.abort());
    await ctx.route('https://routing.openstreetmap.de/**', r => {
      const url = new URL(r.request().url());
      perfiles.push(url.pathname.split('/')[1]);
      const [a,b] = url.pathname.split('/').at(-1).split(';').map(pair => pair.split(',').map(Number));
      const middle = [(a[0]+b[0])/2,(a[1]+b[1])/2];
      const routes = [0,.002,-.002].map(offset => {
        const m = [middle[0]+offset,middle[1]];
        const distance = (Math.hypot((a[0]-m[0])*.73,a[1]-m[1]) + Math.hypot((b[0]-m[0])*.73,b[1]-m[1]))*111195;
        return {distance,geometry:{coordinates:[a,m,b]},legs:[{steps:[]}]};
      });
      return r.fulfill({json:{routes},headers:{'Access-Control-Allow-Origin':'*'}});
    });
    assert.equal(await p.locator('.draw-plan-activity').textContent(),'Senderismo');
    assert.equal(await p.locator('.draw-plan-controls select').count(),0,'no hay selector de actividad');
    await p.locator('[data-mode="extremos"]').click();
    await toca(SOBRE_RUTA);
    const opciones = p.locator('.draw-choice-colors button');
    await opciones.nth(2).waitFor();
    await opciones.nth(1).click();
    await opciones.nth(0).click();
    assert.equal(await opciones.nth(0).getAttribute('aria-pressed'), 'true');
    await p.getByRole('button', {name:'Descartar',exact:true}).click();
    await p.locator('[data-mode="extremos"]').click();
    await toca(SOBRE_RUTA);
    await p.getByRole('button', {name:'Elegir ruta',exact:true}).click();
    assert.equal(await p.locator('.draw-dot').count(), 2);
    assert(perfiles.length > 0 && perfiles.every(p => p === 'routed-foot'));
    assert.deepEqual(errores, [], 'errores JS');
    const eu = await ctx.newPage();
    await eu.setViewportSize({width:320,height:720});
    await eu.goto(base + 'index.eu.html#crear-ruta', {waitUntil:'domcontentloaded'});
    await eu.locator('.draw-plan-activity').waitFor();
    assert.equal(await eu.locator('.hero-compact').getByRole('link',{name:'Ibilbidea sortu',exact:true}).count(),0);
    assert.equal(await eu.locator('.draw-plan-activity').textContent(), 'Mendi-ibiliak');
    await ctx.close();
    console.log('PASS lapiz: red lista en %d ms · dibuja donde no hay ruta publicada ' +
                '(%s) y sigue trayendo alturas sobre las rutas', tardo, LEJOS.length + ' toques');
  } finally {
    if (browser) await browser.close();
    await new Promise(r => server.close(r));
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
