---
name: run-rutas-mallabia
description: Construye, sirve y maneja trabakutik.com (rutas-mallabia) en este contenedor. Úsalo para build, rebuild, regenerar el euskera, lanzar el sitio, servirlo, abrirlo en un navegador de verdad, hacer capturas de pantalla, revisar la maquetación a 320/390/768/1280, comprobar el tema claro y el oscuro, probar el buscador y los filtros de la portada, verificar que el mapa de Leaflet pinta el track, probar el modo offline del service worker, o pasar los tests. También cuando alguien diga "run the site", "screenshot the home", "¿se ve bien en móvil?", "compruébalo en el navegador" o "¿esto desborda?".
---

# Ejecutar y manejar rutas-mallabia

Sitio estático bilingüe (ES/EU) de 57 páginas. No hay `package.json` ni
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

## Manejar el sitio (lo que hace un agente)

```bash
D=.claude/skills/run-rutas-mallabia/driver.py

python3 $D todo                                    # audit + filtros + mapa + temas + offline (~60 s)

python3 $D shot index.es.html --ancho 390 --tema light --sel .hero-compact
python3 $D audit index.es.html                     # desborde a 320/390/768/1280, dos temas (~40 s)
python3 $D probe index.es.html --sel ".hero-compact h1"   # color/fondo/tipo/sombra calculados
python3 $D temas                                   # el héroe se lee igual en claro y oscuro
python3 $D filtros                                 # escribe en el buscador y pulsa los chips
python3 $D mapa longaurjauziak.html                # Leaflet monta y pinta el track
python3 $D offline index.es.html                   # service worker + red cortada
```

Las capturas van a `.claude/skills/run-rutas-mallabia/capturas/`.

Las páginas se nombran como el fichero: `index.html` es **la portada en
euskera**, `index.es.html` la castellana, `longaurjauziak.html`,
`betzun.eu.html`...

Salida real de `filtros` y de `offline`:

```
  sin filtrar            56 tarjetas
  buscando 'cascada'     7
  solo e-bike            26
  de vuelta a todas      56

  service worker        activo, controla la pagina
  sin red, recargada    «Trabakutik · Rutas Mallabia · Senderismo y e-bik»
  contenido servido     56 bloque(s)
```

## Pasar los tests

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py check
```

Los tres que ejecuta CI: `scripts/check_site.py` (2.035 comprobaciones),
`node scripts/test_ui.cjs` (61 asserts) y
`scripts/verify_route_consistency.py`.

## Servirlo a mano

```bash
python3 .claude/skills/run-rutas-mallabia/driver.py serve
```

Sirve la raíz y se queda en primer plano. Ctrl-C para parar. Equivale a
`python3 -m http.server` desde la raíz; el driver solo elige un puerto libre.

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

- **`index.html` es la portada en euskera**, no la castellana. La castellana es
  `index.es.html`. `index.eu.html` es una redirección heredada de 356 bytes.

- **Las fotos y los `_tail.html` llevan líneas base64 larguísimas.** No los
  abras enteros ni los imprimas; filtra por longitud de línea.

## Si algo falla

| Síntoma | Causa y arreglo |
|---|---|
| `BrowserType.launch: Executable doesn't exist at .../chromium_headless_shell-1243` | Versión de Chromium que no está. Pasa `executable_path=` apuntando a `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. |
| `make_eu.py` sale 1 con *"translation key(s) no longer found"* | Cambiaste el castellano y su clave en `src/i18n/eu.py` dejó de casar. El mensaje imprime los primeros 110 caracteres de cada clave: búscala en `eu.py` y actualízala. |
| `offline` dice «Konexiorik gabe · Sin conexión» | Cortaste la red tras una sola carga. Hacen falta dos. |
| `Locator.screenshot() got an unexpected keyword argument 'full_page'` | `full_page` solo existe en `Page.screenshot()`, no en el de un `Locator`. |
| 20 líneas de `BrokenPipeError` de `socketserver` | El navegador cortó descargas de fotos a medias al cerrarse. Inofensivo; el driver lo silencia. |
| `check_site.py` falla con `ZIP omits <ruta>.gpx` | Tocaste un `.gpx` y no regeneraste el paquete: `python3 scripts/bundle_gpx.py`. |
