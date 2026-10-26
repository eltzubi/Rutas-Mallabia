---
name: run-rutas-mallabia
description: Construye, sirve y maneja trabakutik.com (rutas-mallabia) en este contenedor. Úsalo para build, rebuild, regenerar el euskera, lanzar el sitio, servirlo, abrirlo en un navegador de verdad, hacer capturas de pantalla, revisar la maquetación a 320/390/768/1280, comprobar el tema claro y el oscuro, probar el buscador y los filtros de la portada, verificar que el mapa de Leaflet pinta el track, probar el modo offline del service worker, o pasar los tests. También cuando alguien diga "run the site", "screenshot the home", "¿se ve bien en móvil?", "compruébalo en el navegador" o "¿esto desborda?".
---

# Ejecutar y manejar rutas-mallabia

Sitio estático bilingüe (ES/EU): 66 rutas más portada, preguntas, agua y
aviso legal, en los dos idiomas. No hay `package.json` ni
`Makefile`: el build es Python de la biblioteca estándar y se publica desde la
**raíz del repo**, así que todos los `.html`, `.css` y `.js` de la raíz son
artefactos generados.

Se maneja con **`.claude/skills/run-rutas-mallabia/driver.py`**, que levanta un
servidor y conduce Chromium real (Playwright de Python). No hay `chromium-cli`
en este contenedor.

Todas las rutas son relativas a la raíz del repo.

## Qué cubre el driver que no cubre nada más

`scripts/test_ui.cjs` ejecuta el JS contra un DOM de mentira y lo dice en su
primera línea: *"does not test browser layout"*. El driver es lo otro — CSS
real, maquetación real, capturas de verdad.

## Requisitos

Nada que instalar. Ya están Python 3.11, Node 22, el Playwright de Python y
Chromium en `/opt/pw-browsers/`. El driver lo encuentra solo.

## Construir

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py build
```

Encadena `src/i18n/make_eu.py` y `src/build.py`, **mira el código de salida de
cada uno** y resume las 250 líneas que escriben. Al final dice si quedan
ficheros sin commitear, que es lo que CI comprueba con `git diff --exit-code`.

A mano, si prefieres verlo entero (siempre en este orden):

```bash
python3 src/i18n/make_eu.py
python3 src/build.py
```

## Verificar antes de publicar: una sola orden, un solo veredicto

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py verifica            # todo (~3 min)
python3 .claude/skills/run-rutas-mallabia/driver.py verifica --rapido   # sin navegador (~50 s)
```

Construye, pasa la batería de ficheros y (sin `--rapido`) las ocho pruebas
de navegador, y **termina en una sola línea**: `VERIFICACION CORRECTA (N
pasos)` o `VERIFICACION FALLIDA: <qué pasos>`, con código de salida 0 o 1.

**Usa esto y no encadenes las comprobaciones a mano.** Lo que se hacía antes
—`python3 ... | grep -E "^# (pass|fail)" && echo "TODO CORRECTO"`— daba por
bueno lo que no lo era: `grep` sale con éxito por haber *encontrado* la
línea, diga «fail 0» o «fail 1». El 18 de octubre una misma salida dijo
«# fail 1» y debajo «TODO CORRECTO».

## Manejar el sitio (lo que hace un agente)

```bash
D=.claude/skills/run-rutas-mallabia/driver.py

python3 $D todo                                    # audit + filtros + mapa + temas + offline (~60 s)
                                                   # (lo incluye "verifica"; suelto, sólo el navegador)

python3 $D shot index.es.html --ancho 390 --tema light --sel .hero-compact
python3 $D audit index.es.html                     # desborde a 320/360/390/768/1280, dos temas (~60 s)
python3 $D probe index.es.html --sel ".hero-compact h1"   # color/fondo/tipo/sombra calculados
python3 $D temas                                   # el héroe se lee igual en claro y oscuro
python3 $D filtros                                 # escribe en el buscador y pulsa los chips
python3 $D mapa longaurjauziak.html                # Leaflet monta y pinta el track
python3 $D offline index.es.html                   # service worker + red cortada
```

Las capturas van a `.claude/skills/run-rutas-mallabia/capturas/`.

Las páginas se nombran como el fichero: **`index.html` es la portada en
castellano** e **`index.eu.html` la de euskera**; luego
`longaurjauziak.html`, `betzun.eu.html`... (`index.es.html` existe pero son
352 bytes de redirección heredada: no lo captures, sale en blanco.)

Salida real de `filtros` y de `offline`:

```
  sin filtrar            66 tarjetas
  buscando 'cascada'     7
  tras cerrar la lupa    66
  solo e-bike            32
  de vuelta a todas      66
  barra del movil        se aparta al bajar; vuelve al parar y al subir

  service worker        activo, controla la pagina
  sin red, recargada    «Trabakutik · Rutas Mallabia · Senderismo y e-bik»
```

## Renombrar una ruta

Cambiar el título de una ruta toca **nueve sitios**, y a mano se escapa alguno
—las cuatro apariciones del `_head.html` son `<title>`, `og:title` y los **dos**
bloques JSON-LD—. Esta orden los hace todos:

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py renombrar betzun \
  --es "Zengotita, Iturzurigaina y Betzun por San Kristobal Txiki" \
  --es-h1 "Zengotita, Iturzurigaina|y Betzun por San Kristobal Txiki" \
  --eu "Zengotita, Iturzurigaina eta Betzun San Kristobal Txikitik" \
  --eu-h1 "Zengotita, Iturzurigaina|eta Betzun San Kristobal Txikitik"
```

**Por defecto solo simula**: imprime cada sustitución con su recuento y no
escribe nada. Añade `--aplica` para escribirlo; entonces encadena `make_eu.py`,
`build.py`, `bundle_gpx.py` (el ZIP nombra sus entradas con las tarjetas) y
`check_site.py`.

No se le dice el título viejo: lo lee él de los ficheros —el plano de la tarjeta
de la portada, el `h1` de la ficha, el de descarga de su atributo—. El `|` separa
las dos líneas del `h1` (lo de antes del `<br>` y lo de dentro del `<em>`).

Simulacro real sobre `betzun`:

```
    1x  src/betzun_tail.html    <h1>Zengotita, Iturzurigaina<br><em>y Betzun</em></h1>
    4x  src/betzun_head.html    Zengotita, Iturzurigaina y Betzun
    1x  src/mallabia_tail.html  Zengotita, Iturzurigaina y Betzun
    5x  src/i18n/eu.py          Zengotita, Iturzurigaina y Betzun
    6x  src/i18n/eu.py          Zengotita, Iturzurigaina eta Betzun
  29 sustitucion(es) en 4 fichero(s)
```

Dos cosas que hace a propósito:

- **No toca el nombre de descarga si hoy no es el título.** 8 de las 56 rutas lo
  tienen más corto aposta (`hirutxikiak` descarga «Hiru Txikiak»). Lo avisa y lo
  deja.
- **Solo reescribe los enlaces entrantes que usan el título entero.** Los 221
  que usan el nombre corto («Oiz», «Gerea», «Osmagain») se quedan como están,
  que es lo correcto.

Probado con una ida y vuelta: renombrar y volver a renombrar al nombre
original deja el árbol de git idéntico.

## Pasar los tests

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py check
```

Los tres que ejecuta CI: `scripts/check_site.py` (**14.023** comprobaciones),
`node scripts/test_ui.cjs` (**14 tests**) y `scripts/verify_route_consistency.py`
(66 tarjetas ES, 66 EU, 66 tracks).

## Servirlo a mano

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py serve
```

Sirve la raíz y se queda en primer plano. Ctrl-C para parar. Equivale a
`python3 -m http.server` desde la raíz; el driver solo elige un puerto libre.

## Manejar el mapa desde Playwright (recetas que funcionan)

El driver cubre el sitio; para tocar el mapa punto por punto hace falta
Playwright a pelo. Estas cuatro cosas cuestan media hora de descubrir y son el
80 % de lo que hace falta. Todas ejecutadas en este contenedor:

```python
from playwright.sync_api import sync_playwright
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'   # el -1243 no esta
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={'width': 393, 'height': 852}, device_scale_factor=2)
    # 1) coger el mapa: map.js dispara «mapa:listo» al terminar de montarlo
    pg.add_init_script("document.addEventListener('mapa:listo',"
                       "e=>{window.__m=e.detail.map;window.__L=e.detail.L;})")
    pg.goto('http://localhost:8111/index.html', wait_until='load')
    # 2) la portada arranca en lista y el mapa mide 0x0 hasta que se cambia.
    #    El boton esta OCULTO por debajo de 360 px (ahi manda la barra fija de
    #    abajo), asi que .click() de Playwright falla: se pulsan todos por JS.
    pg.evaluate("document.querySelectorAll('[data-view=\"map\"]')"
                ".forEach(b=>b.click())")
    pg.wait_for_function("window.__m", timeout=30000)
    pg.wait_for_timeout(2500)
    # 3) abrir una ruta sin raton: Enter sobre su trazado
    pg.evaluate("""()=>{const l=[...document.querySelectorAll(
        '.leaflet-overlay-pane path[tabindex=\"0\"]')][20];
        l.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));}""")
    # 4) poner un punto del trazado propio: SIEMPRE con fire, nunca con el raton
    pg.evaluate("window.__m.fire('click',{latlng:{lat:43.2096,lng:-2.5468}})")
```

Y el servidor, en otra terminal o en segundo plano:

```bash
(python3 -m http.server 8111 >/dev/null 2>&1 &)
```

## Trampas

- **`make_eu.py` no dice «error» cuando falla.** Dice *"N translation key(s) no
  longer found in the Spanish source"* y sale con código 1. Si filtras su
  salida buscando «error» no te enteras, `build.py` sigue adelante reutilizando
  los `.eu.html` viejos y publicas euskera desfasado sin avisos. **Mira el
  código de salida.** Esto pasó de verdad y estuvo dos días sin detectarse.

- **No toques `eu.py` con sustituciones literales a lo bruto.** Sus claves son
  concatenaciones de literales de Python y un nombre puede partirse entre dos
  líneas (`'...Ermita de San '` + `'Crist&oacute;bal Txiki.'`). Un
  `replace("San Cristóbal", ...)` no las alcanza, la clave deja de casar con el
  castellano y el generador se planta. Cambia el castellano, ejecuta `build` y
  deja que el generador te diga qué claves quedaron descolgadas.

- **Playwright no encuentra su navegador.** Pide
  `chromium_headless_shell-1243` y aquí solo está `-1194`:
  `BrowserType.launch: Executable doesn't exist`. Hay que pasarle
  `executable_path`; el driver lo resuelve en su función `navegador()`.
  **No ejecutes `playwright install`.**

- **El service worker no controla la página que lo instala.** La primera carga
  lo registra pero no pasa por él, así que esa visita no se cachea. Si cortas la
  red después de una sola carga te sirve `offline.html`. Hacen falta **dos
  cargas** antes de desconectar. El driver espera a
  `navigator.serviceWorker.controller` y recarga.

- **Las teselas del mapa nunca cargan aquí.** Salen con
  `ERR_CERT_AUTHORITY_INVALID` contra el proxy TLS. El track sí se pinta. El
  driver filtra ese ruido; si ves ese error en la consola, no es del sitio.

- **El texto del héroe va en blanco fijo, no en tokens.** La foto es oscura en
  los dos temas, así que `var(--ink)`, `var(--violet)` y `var(--teal)` (que en
  claro son tinta, verde y azul oscuros) lo vuelven ilegible. `temas` lo caza:
  con el bug reintroducido a propósito sale
  `MAL .hero-compact h1 em .pie  rgb(166,255,77) -> rgb(58,107,21)` y código 1.

- **El desborde de la página no lo ve todo.** El héroe recorta por dentro
  (`overflow:hidden`), así que una línea que no cabe se corta en silencio sin
  que `scrollWidth` se entere. `audit` mide además el texto contra su caja en
  los elementos que no pueden partirse en dos líneas. Pasó de verdad: la línea
  de cifras se comía el «+» final en móviles de 320-360 px y a 390 px entraba
  por 5 px, que es justo donde yo hacía las capturas.

- **El euskera es más largo que el castellano.** «56 ibilbide» frente a «56
  rutas». Si algo va justo de ancho, revisa `index.html` antes que
  `index.es.html`.

- **`index.html` es la portada en castellano** y `index.eu.html` la de
  euskera. El que es una redirección heredada —352 bytes, sin contenido— es
  **`index.es.html`**: capturarlo da una página en blanco. (Hasta octubre de
  2026 era al revés y esta misma skill lo decía mal.)

- **Las fotos y los `_tail.html` llevan líneas base64 larguísimas.** No los
  abras enteros ni los imprimas; filtra por longitud de línea.

- **`verifica` falla a veces por un 429 de Open-Meteo, y no es tu código.** La
  comprobación de «Lo mío» no admite **ningún** error de consola, y el bloque
  del tiempo de cada ficha llama a `api.open-meteo.com`. Si se han hecho
  muchas peticiones desde esta IP, devuelve *429 Too Many Requests* y la da
  por fallida. Se distingue mirando la lista de errores que imprime: si lo
  único que sale es ese 429, repite la pasada. Pasó de verdad el 26 de
  octubre: tres ejecuciones seguidas del mismo código dieron correcta,
  fallida y correcta.

- **Leaflet pone la opacidad en `stroke-opacity`, no en `opacity` de CSS.**
  Medir con `getComputedStyle(path).opacity` para ver si un trazado está
  apagado devuelve `1` siempre y te hace creer que un filtro no funciona.
  Lo que hay que leer es `path.getAttribute('stroke-opacity')`.

- **Los rebordes de los trazados no están en `.leaflet-overlay-pane`** sino en
  `.leaflet-rebordes-pane`, que `map.js` crea aparte con `z-index` 395.
  Buscarlos en el primero devuelve cero.

- **Los controles de Leaflet van en `z-index` 1000.** Cualquier panel propio
  que se ponga encima del mapa tiene que ir por encima de eso, o la línea de
  créditos le cae dentro. Ya pasó con la ficha de la portada.

- **`pkill -f <patrón>` se mata a sí mismo.** El patrón aparece en la línea de
  órdenes del propio shell, así que `pkill -f make_alturas` mata el shell
  antes de ejecutar lo que venía detrás, y lo que creías haber hecho no se
  hizo. Usa `kill <pid>` sacando el PID con `ps -eo pid,args | grep 'patr[ó]n'`
  (con el corchete, que si no vuelves a lo mismo).

- **Las comprobaciones de la pastilla del mapa en `test_ui.cjs` cuentan
  capas**, así que filtran las clases de los botones que no lo son
  (`map-rutas-btn`…). Si añades un botón a esa pastilla y no lo añades al
  filtro, fallan dos tests sin motivo aparente.

## Si algo falla

| Síntoma | Causa y arreglo |
|---|---|
| `BrowserType.launch: Executable doesn't exist at .../chromium_headless_shell-1243` | Versión de Chromium que no está. Pasa `executable_path=` apuntando a `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. |
| `make_eu.py` sale 1 con *"translation key(s) no longer found"* | Cambiaste el castellano y su clave en `src/i18n/eu.py` dejó de casar. El mensaje imprime los primeros 110 caracteres de cada clave: búscala en `eu.py` y actualízala. |
| `offline` dice «Konexiorik gabe · Sin conexión» | Cortaste la red tras una sola carga. Hacen falta dos. |
| `Locator.screenshot() got an unexpected keyword argument 'full_page'` | `full_page` solo existe en `Page.screenshot()`, no en el de un `Locator`. |
| 20 líneas de `BrokenPipeError` de `socketserver` | El navegador cortó descargas de fotos a medias al cerrarse. Inofensivo; el driver lo silencia. |
| `check_site.py` falla con `ZIP omits <ruta>.gpx` | Tocaste un `.gpx` y no regeneraste el paquete: `python3 scripts/bundle_gpx.py`. |
| `check_site.py` falla con `js/agua.js no tiene la capa de map.js: <url>` | Cambiaste una capa de teselas en `src/js/map.js` y no en `src/js/agua.js`, que lleva su propia copia. Las URL tienen que ser idénticas. |
| `verifica` falla y los errores que imprime son sólo `429 (Too Many Requests)` | Cuota de Open-Meteo agotada desde esta IP. No es el código: repite la pasada. |
| `build.py` avisa de que falta `img/mapa-<ruta>.webp` | Ruta nueva sin miniatura de mapa: `python3 scripts/make_card_maps.py`. |
| Una captura de `index.es.html` sale en blanco | Es la redirección heredada de 352 bytes. La portada castellana es `index.html`. |
