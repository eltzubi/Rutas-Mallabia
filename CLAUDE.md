# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Idioma: responde siempre en castellano**, incluidos los avisos intermedios, los mensajes de commit y
las pull requests. El euskera solo para los textos de la web en euskera.

## What this is

A static site of hiking/biking routes around Mallabia (Bizkaia), documented on the ground with real
data (GPX tracks, own photos). Bilingual (Spanish + Basque). Published via GitHub Pages (custom domain, see `CNAME`) at
https://trabakutik.com/ from the repo root — every root-level `.html`/`.css`/`.js`
file is a **build artifact**. Never hand-edit them; edit the sources in `src/` and rebuild.

GitHub Pages would otherwise publish the repo verbatim, so `_config.yml` keeps the sources out of the site
(`src/*.html`, `src/css|js|fonts|i18n`, `scripts/`, `CLAUDE.md`, `README.md`) and `robots.txt` says the same to
crawlers. What stays published from `src/` are the **downloads** — `src/*.gpx`, `src/*.kml` and
`src/todas-las-rutas.zip` are linked from every route page — so don't add anything to those exclusion lists
without checking nothing links to it.

## Build commands

After editing any Spanish source text, always run both, in this order:

```
python3 src/i18n/make_eu.py    # regenerate Basque pages from src/i18n/eu.py; FAILS if Spanish text drifted
python3 src/build.py           # assemble both languages into root .html/.css/.js + sitemap.xml
```

`make_eu.py` deliberately refuses to run (`SystemExit`) if a translation-table key in `src/i18n/eu.py`
no longer matches the Spanish source verbatim — that's the signal a Spanish edit needs its Basque
counterpart updated too. Fix `eu.py`, re-run. It also scans the generated Basque output for a fixed
list of Spanish "tell" words (`SPANISH_TELLS`) to catch anything the tables missed, including inside
attribute values like `alt`/`title`/`data-marker-title`.

`build.py` also validates HTML entities (catches things like `case&riacute;os` — a letter swallowed
into an entity name) and fails loudly if it finds one.

**`build.py` tarda 1,5-1,7 s, no 85.** El 99% del build se iba en una sola cuenta: las «Rutas por esta
zona» comparaban punto a punto los tracks de las 60 rutas, 165.054.409 distancias en Python puro por
construcción. Esa cuenta sólo depende de `data/trailhead.json`, así que ahora se guarda calculada en
**`.cache-build/`** (fuera de git y fuera de la web) con la huella sha256 del fichero del que sale: si
cambias un track, la huella no coincide y se recalcula entera; si no, se lee del disco. Lo mismo con
las celdas de cada GPX (`celdas.json`, huella del propio `.gpx`), que costaban 2 s de analizar los
60 GPX (51 MB de XML), y las fechas del sitemap, que eran 64 llamadas a `git log` y ahora son una sola pasada.
**La carpeta `.cache-build/` se puede borrar entera sin perder nada**: la siguiente construcción la
rehace (6 s en frío). Si tocas los umbrales de `vecinas_cercanas` o el muestreo de `_cobertura`,
no hace falta acordarse de nada: la clave se forma con los propios
valores (`_UMBRAL_CERCA`, `_UMBRAL_LEJOS`, `_MUESTRA_A`, `_MUESTRA_B`, `_CELDA`, `_CELDA_PASO`) y
cambiar cualquiera caduca la caché sola. `_SOLAPES_VERSION` y `_CELDAS_VERSION` están para forzarlo
a mano si alguna vez cambia el *algoritmo* sin cambiar ninguna constante.

La poda de `_cobertura` (saltarse los puntos cuya latitud ya los deja fuera del umbral) es **exacta,
no una aproximación**: la distancia nunca es menor que su componente norte-sur. Se comprobó par por
par — los 1.767 pares dan exactamente los mismos dos números que antes, y una
comparación exhaustiva de las 3.540 parejas ordenadas × los dos umbrales tampoco encuentra ni una
diferencia — y la huella sha256 de los
151 ficheros publicados es idéntica.

Other scripts:

```
python3 scripts/optimize_images.py    # resize the master JPEGs to MAX_SIDE=1600px, recompress, write .webp
python3 scripts/make_wide_variants.py # img/<name>-800.{webp,jpg}: what the gallery actually serves
python3 scripts/make_card_thumbs.py   # img/<name>-card.{jpg,webp}: the home page's card photos
```

**Where the photos live.** The 1600 px master JPEGs are in **`img/orig/`, which is not published**
(`_config.yml` excludes it) — nobody was downloading them: the galleries serve WebP through
`<source type="image/webp">`, the `<img src>` is only a fallback and now points at the 800 px JPEG,
and the lightbox's `data-lightbox-src` is the full-size `.webp` (`src/js/app.js` falls back to
`-800.jpg` on error). That took the published site from 529 to 393 MB of GitHub Pages' 1 GB limit.
**The 57 masters still sitting in `img/` are the ones each route declares as `og:image`** — the
social preview has to be a real, downloadable URL at a decent size, so those stay. So a master is in
one of two places and the scripts look in both (`optimize_images.py`, `make_wide_variants.py`,
`make_card_thumbs.py`); anything they generate always lands in `img/`, never in `img/orig/`.
`check_site.py` now verifies that every `src`/`srcset`/`data-lightbox-src` in both languages exists
**and is not inside an excluded path** — a reference to a master would work locally and 404 on the
real site, which is exactly the mistake this guards against.

`make_card_thumbs.py` is the one to re-run when a route joins the home page: the card `<picture>` points at
`img/<name>-card.webp` (a 1100 px, 16:10 centre crop — the same crop `object-fit:cover` was doing in the
browser), not at the full 1600 px photo. Without it the new card has no image. Everything below the first two
cards is `loading="lazy"`, so the home page loads ~0.6 MB instead of ~6.6 MB.

`optimize_images.py` only touches what needs it. It keeps a register of what it wrote in
`img/.optimized.json` and skips any photo whose `.jpg` and `.webp` still match that register, so a run
after adding one photo processes that photo and leaves the other 565 alone. This matters for two reasons:
re-encoding an already-processed JPEG produces **different bytes every time** (1,026 new blobs per run —
that's where the hundreds of MB of git history came from) and it also degrades the photo a little more
each pass, because it re-quantizes an already-quantized image. Pass `--force` to reprocess everything
anyway. It also skips `-card` and `-800` files (`EXCLUIR`), which belong to the two scripts below: running
it over a `<name>-card.jpg` used to overwrite that card's `.webp` with a worse, heavier one.

`make_card_thumbs.py` derives its output from the master `<name>.jpg` (in `img/` or `img/orig/`) rather
than from its own previous output, so it is deterministic: re-running it rewrites byte-identical files and git sees no change.

```
python3 scripts/check_site.py          # 9.236 comprobaciones sobre el sitio ya construido
python3 scripts/make_icons.py          # icon-192.png / icon-512.png desde favicon.svg
```

```
python3 scripts/make_places.py         # data-places de cada tarjeta: lugares por los que pasa su track
```

```
python3 scripts/make_card_maps.py      # img/mapa-<ruta>.webp: la miniatura de mapa de cada tarjeta
```

`make_card_maps.py` dibuja, con MapLibre y **OpenFreeMap** dentro del Chromium del driver, la miniatura
de mapa que lleva cada tarjeta de la portada en la esquina de la foto: el track sobre un mapa de verdad,
con la salida marcada y los nombres de los pueblos por los que pasa. **Hay que volver a pasarlo al meter
una ruta nueva**; si falta la imagen, `build.py` lo avisa por pantalla y esa tarjeta se queda sin
miniatura (no sale un hueco roto). El mapa sale de OpenFreeMap y no del IGN ni de OpenStreetMap porque
es de los pocos que **deja guardar las teselas** — las de los otros dos lo prohiben sus condiciones de
uso. La atribucion va al pie de la portada. Se quitan del mapa los iconos, los numeros de carretera y
los nombres de calle: cada uno de esos rotulos le quitaba el sitio a un nombre de pueblo. Donde
alrededor no hay nada registrado en OpenStreetMap (longaurjauziak, por ejemplo) no sale ningun nombre,
y es correcto que no salga.

`make_places.py` feeds the home-page search. For every card it writes `data-places` (never shown, only
searched) with the places its real track (`data/<name>.json`) passes: the hand-written ones already there,
the page's own numbered waypoints, and OpenStreetMap villages, neighbourhoods, localities, peaks, passes,
churches/hermitages and waterfalls within a per-type distance (`MAX_M`). OSM comes from a fixed snapshot in
`scripts/osm/` (query and date in its `LEEME.txt`), so it runs offline and is reproducible. Re-run it when a
route joins the home page. The search itself (`src/js/filters.js`) ignores accents, case and hyphens and
requires every typed word.

`check_site.py` is the closest thing to a test suite: read-only, stdlib only, run it after `build.py`.
Besides the page/marker/download/asset checks it already had, it now contrasts every route page against
its own GPX and against its Basque twin:

- **distance** in `.facts` vs the real track (1% tolerance; today's worst case is 0.7%)
- **min/max altitude** vs the track (8 m; worst case 6 m)
- **same `<a>` and `<picture>` count** in the Spanish and Basque body copy — a missing one means a key in
  `eu.py` swallowed a cross-reference or a responsive image (ahuntzen was missing all six)
- every route page has at least one `<picture>`

It deliberately does **not** check cumulative elevation gain: summing the GPX's climbs raw drifts up to 43%
from the figure on the page, and even smoothed it stays around 9% on average. Those figures come from the
route's own source (Wikiloc, the race organiser) and the page says so. Checking it would only cry wolf.

It also does not check the waypoint kilometres in the elevation-profile markers — see the note in
"Content rules" about them still being on the old distance basis.

There is no linter or package manifest — this is plain Python (stdlib only) + hand-written
HTML/CSS/JS with no build tooling beyond the scripts above.

## Architecture

**Page assembly.** Each page is a `<name>_head.html` + `<name>_tail.html` pair in `src/`. `build.py`
concatenates the pair and writes it to the repo root. The home page is `mallabia` → `index.html`
(so GitHub Pages serves it at `/`); every other page keeps its own name (`trabakua.html`,
`egoarbitza.html`, etc.) as a real, independently loadable, bookmarkable file — not an SPA route.
`PAGES` at the top of `src/build.py` is the authoritative page list; **adding a new route page means
adding its name there too** (and to `ROUTE_PAGES`/`PAGES` in `src/i18n/make_eu.py`).

**One card per route, newest first — except the top few, which alternate activity.** The home
page lists every route exactly once, in `#routeResults` inside `src/mallabia_tail.html`. Below the
top section, cards are ordered from most recently added to oldest — **a new route goes at the top
of that grid**. No separate "latest routes" block and no route repeated in two places: the order
itself is what says which ones are new.

The exception, by explicit user request: the first six cards (the two visible grid rows on a wide
screen, three columns each — see "Rejilla de tarjetas...") are hand-interleaved bici/senderismo so
the top of the grid doesn't show a run of same-activity cards, instead of strict recency. When a
new route is added, insert it among those six by activity (swap it in for the oldest card of the
same activity currently there, pushing that one down to resume its place in the plain-recency
tail) rather than always slotting it first — recompute the interleave by hand, there's no script
for this. Position 7 onward stays pure recency, untouched.

**El sitemap lleva la fecha de cada página.** `fecha_de_la_fuente()` en `src/build.py` pregunta a
git cuándo se tocó por última vez `<pag>_head.html`/`<pag>_tail.html` y la escribe como `<lastmod>`.
**No vale la fecha de construcción**: un retoque del CSS no cambia lo que cuenta una ruta, y poner la
fecha de hoy en las 118 páginas cada vez que se publica algo es mentirle al buscador — que entonces
deja de hacer caso al dato. Sin git (una copia en zip) devuelve `None` y el sitemap sale sin fechas,
como antes. Ojo: una edición global de las cabeceras o de las colas (un renombrado de etiqueta en las
57 fichas, por ejemplo) sí pone a todas la misma fecha, y es correcto que lo haga.

**hreflang, siempre absoluto.** Las etiquetas `<link rel="alternate" hreflang>` de cada
`*_head.html` llevan la URL completa (`https://trabakutik.com/…`), no el nombre del fichero: Google
pide URL absoluta en hreflang y las relativas se las puede saltar. Van **idénticas en las dos
lenguas** (cada página declara el par entero, más `x-default` apuntando al castellano), y por eso
`make_eu.py` las **aparta** antes de cambiar `https://trabakutik.com/<pag>.html` por su versión en
euskera: si entraran en ese cambio, la línea del castellano acabaría apuntando a la página en
euskera y las dos versiones dirían ser la castellana. El `canonical` de cada página sí apunta a sí
misma, y el sitemap ya llevaba los alternates absolutos.

**Bilingual generation, not duplication.** Only the Spanish `_head.html`/`_tail.html` files are
hand-written. The Basque `*_head.eu.html`/`*_tail.eu.html` are generated by
`src/i18n/make_eu.py` from string tables in `src/i18n/eu.py` (`COMMON` + `ROUTE` shared across pages,
plus a per-page dict such as `EGOARBITZA`, wired up via `PAGE_STRINGS`, `TITLES`, `DESCRIPTIONS`).
**Never edit an `*.eu.html` file directly — it gets overwritten.** To reword Basque text, edit
`eu.py`. Internal links between pages (`href="urko.html"`) are auto-swapped to the Basque
counterpart (`href="urko.eu.html"`) by `EU_OF` in `make_eu.py` — write plain `.html` hrefs in both
the Spanish source and the `eu.py` translation values, never the `.eu.html` form by hand.

**No third parties.** The fonts were already self-hosted; **Leaflet is too**, in `src/vendor/leaflet`
(copied to `vendor/leaflet` by `build.py`). It is the official 1.9.4 distribution, unmodified: its bytes
match the SRI hashes the HTML used to declare while it came from jsdelivr, so it is exactly the same code
that was already being served — only now without a CDN seeing every visitor's IP, and without the map
going blank on 112 pages if that CDN has a bad day. `check_site.py` fails if any `<script src>` or
`<link rel=stylesheet|preconnect|preload>` ever points off-site again. Two things are still fetched
from outside, both by the JS and never by the HTML: the **map tiles**, and the **weather forecast**
(see below). Nothing else may be added without the user saying so.

**«Rutas por esta zona», en el build.** The three neighbouring routes at the foot of each page are
chosen by `vecinas_cercanas()` in `src/build.py` from the real tracks in `data/trailhead.json`
(coverage at 70 m and 250 m, score = shared×4 + nearby, hand-picked `VECINAS_FIJAS` first). This used
to run in the browser: every route page downloaded `data/trailhead.json` (399 kB) **and the whole home
page** (355 kB) to recompute a list that never changes between visits — 754 kB, half the weight of a
route page. Moving it to the build cut a mobile route page from 1.564 to 805 kB, and the list is now
visible to Google and without JavaScript. The Python reproduces the old JS point for point; the
migration was checked by capturing what the browser rendered on all 114 pages first and requiring the
generated HTML to match it exactly. `add_similar_routes` **replaces** a hand-written `next-routes`
block if it finds one (ahuntzen had one, with figures copied by hand that nobody was updating).

**Última entrada, dificultad técnica y barra fija del móvil.** Tres datos nuevos en la ficha,
los tres escritos por `src/build.py`:

- `add_ultima_entrada` marca en la portada **la última ruta que entró**: va la primera de la rejilla
  (el orden lo lleva a mano `src/mallabia_tail.html`) y lleva `class="route-card is-new"` más una
  pastilla `.route-card-new` sobre la foto, «Nueva · 5 oct 2026». La fecha sale de `ULTIMA_ENTRADA`,
  que **se cambia a mano al publicar una ruta nueva**, y es la única de todo el sitio. La pastilla va
  en blanco/negro a propósito: el verde es «a pie» y el naranja «en bici», y en uno de esos colores se
  leería como la actividad de la ruta. Se probaron antes dos cosas que el autor quitó: una fecha de
  revisión **en cada ficha** (no quiere 57 fechas) y esto mismo como **una línea de texto bajo los
  totales** (lo prefiere en la tarjeta). El `is-new` obliga a que cualquier selector de
  `class="route-card"` admita la clase extra — ya se arreglaron `check_site.py` y
  `verify_route_consistency.py`; `build.py` lee el origen, donde no existe.
- `add_tecnica` pone **«Terreno»** junto a **«Esfuerzo»**, leyendo `TECNICA`, **que está vacío a
  propósito**: el esfuerzo sale de la distancia y el desnivel, que son datos, pero el terreno depende
  de lo pedregoso, estrecho, expuesto o embarrado que esté un sendero y eso solo lo sabe quien lo ha
  pisado. Lo pone el autor ruta por ruta; sin valor, el dato no aparece. **No derivarlo de
  `Superficie`**: una reconstrucción del sitio que el autor trajo lo hacía así y le salían 45 de 57
  rutas con la misma etiqueta — un dato que no distingue nada y que además afirma algo que no
  sabemos. El antiguo «Dificultad» se llama ahora **«Esfuerzo»** en las 57 fichas, en el filtro de la
  portada, en la nota y en el JSON-LD; los valores (Fácil/Media/Difícil) no cambian, que son los que
  usa el filtro.
- `add_quick_bar` deja **Mapa y GPX fijos abajo en el móvil** (`.quick-bar`, solo por debajo de
  768 px). El `body` gana 62 px de `padding-bottom` y el botón de volver arriba sube a 74 px para no
  quedar debajo.

**Las tarjetas de la portada, en tres tallas.** `make_card_thumbs.py` escribe, además del
`-card.webp` de 1100 px, un `-card-800.webp` y un `-card-450.webp`, y el `<picture>` de
`src/mallabia_tail.html` los declara con `sizes="(min-width:1024px) 340px, (min-width:768px) 46vw,
92vw"`. Medido en el navegador: la tarjeta ocupa 286-506 px por debajo de 768, 351-430 hasta 1023 y
340 clavados de ahí en adelante, así que un escritorio normal se lleva la de 450, un móvil corriente
la de 800 y uno muy fino (dpr3) la de 1100 — antes todos se bajaban la de 1100. Portada en un
escritorio normal: 2.350 → 1.102 kB. Cuesta 5,4 MB en el repositorio. Las tallas pequeñas salen de la
imagen ya nivelada de tono, no del original, para que las tres sean la misma foto.

**La portada no pide sus tracks hasta que se abre el mapa.** `data/trailhead.json` son 399 kB —
más que todas las fotos visibles de la portada juntas— y la portada arranca en vista de lista, con el
mapa dentro de un bloque oculto que mide 0x0. `src/js/map.js` espera a que la caja mida algo (el mismo
`ResizeObserver` que ya avisa de cuándo aparece) antes de pedir nada; en una ficha de ruta el mapa está
en la página desde el principio, así que ahí carga de inmediato, y sin `ResizeObserver` también, antes
que dejar a nadie sin mapa. Portada en móvil: 1.895 → 1.496 kB. Los dos caminos están cubiertos en
`scripts/test_ui.cjs` (los dos últimos tests).

**Shared assets, not embedded per-page.** `css/home.css`, `css/route.css`,
`fonts/inline_fonts.css` (self-hosted `@font-face`, base64) and `js/{app,map,filters}.js` live once
in `src/` and are copied to the repo root by `build.py`, referenced by every page via a real `<link>`/
`<script src>` (not inlined), so browsers cache them once across pages. `build.py` appends a content
hash (`?v=<sha256[:8]>`) to each reference so a stale browser cache never pairs old CSS/JS with new
HTML.

**Offline (service worker).** The site is opened on the mountain, where there is no signal, so `sw.js`
makes an already-visited route page work without data: its text, elevation profile, photos and GPX.
`build.py` writes it from `src/js/sw.js`, stamping in a version and the precache list (the CSS/JS with
their `?v=` hashes, the five `.woff2`, `offline.html` and the icon — about 210 kB). Pages and photos are
**not** precached; they are stored as they are visited, which is what keeps it from pulling the site's
400 MB of images.

Strategy: **network-first for pages** (whoever has signal always sees the latest; the stored copy is only
the fallback), cache-first for everything else, since the CSS/JS carry a content hash in the URL. The
shell cache is named after its own hash, so it is dropped whole when any asset changes; the page and
photo caches survive, which is the point. `offline.html` (built from `src/offline.html`, bilingual) is
what a never-visited page falls back to.

**Cambiar de capa no deja el mapa en blanco.** `ponerCapa()` añade la nueva capa y **no quita la
vieja hasta que la nueva dispara `load`** (con un plazo de 3 s por si las teselas no llegan nunca).
Leaflet pinta la nueva encima, así que la va tapando según llega. Hacía falta por el mapa ciclista:
CyclOSM lo sirve un servidor de voluntarios y tarda el triple que los demás — medido desde aquí,
0,82 s por tesela de mediana frente a 0,34 del IGN, 0,29 de Esri y 0,17 de OSM, y además sus teselas
pesan 39 kB frente a 13-23 kB. Antes se quitaba la capa vieja primero y el mapa se quedaba casi un
segundo en blanco: parecía roto. El botón recién pulsado parpadea (`.is-loading`) mientras tanto.

**El sentido de la marcha, en flechas.** El mapa de cada ficha dibuja de 6 a 14 flechas sobre el
track (`.track-arrow` en `src/js/map.js`), repartidas **por distancia recorrida, no cada N puntos**:
el GPX está más poblado en las curvas (Douglas-Peucker) y contando puntos se amontonarían justo donde
estorban. El rumbo se calcula corrigiendo la longitud por el coseno de la latitud — sin eso apuntan
torcido — y sale del propio orden de los puntos del track, que es el de la marcha. El mapa de la
portada no las lleva: 57 tracks a la vez.

**Las capas, distintas en la portada y en una ficha.** La portada lleva las cuatro (IGN, Bici,
Calles, Satélite) y abre en **Calles**: de lejos, con las 57 rutas a la vez, lo que sitúa es el
callejero. Una ficha lleva **tres** — sin Calles — y abre en **IGN**: dentro de una ruta lo que hace
falta son las curvas de nivel, los ríos y los caminos. Lo decidió el autor; `src/js/map.js` quita
`osmLayer` de `layerDefs` cuando no es la portada, y `scripts/test_ui.cjs` comprueba las dos listas.

**El tiempo de los proximos dias, en cada ficha.** `add_weather()` en `src/build.py` escribe debajo
del mapa un bloque vacio y **oculto** (`<section class="weather" hidden>`) con las coordenadas del
primer punto del track de esa ruta; `src/js/weather.js` pide el pronostico y lo rellena. Si no hay
cobertura, si el servicio no responde o si la respuesta no trae lo esperado, **el bloque se queda
oculto** y la ficha se ve igual que antes: un extra no puede romper la pagina.

Los datos son de **Open-Meteo**, que es gratis, sin clave, sin cuenta y con CORS abierto — por eso se
puede llamar desde el navegador en una web estatica. **AEMET** pide una clave que en un sitio estatico
quedaria a la vista de cualquiera, y **met.no** exige identificarse en una cabecera `User-Agent` que un
navegador no deja poner: ninguno de los dos vale aqui. La respuesta se guarda **una hora** en
`sessionStorage` con las coordenadas redondeadas a 1 km, asi que mirar cuatro fichas que salen de
Trabakua hace una sola peticion. El service worker no lo toca (solo atiende peticiones del propio
origen), asi que nunca se sirve un pronostico viejo de la cache.

Las etiquetas que escribe el JavaScript (Hoy/Mañana, los dias de la semana, los diez estados del cielo)
viven en `eu.UI` como todas las demas y `build.py` se las pasa en un `data-textos` con JSON, en vez de
duplicar las traducciones dentro del `.js` — que es uno solo para los dos idiomas.

Esto suma **un tercero mas** a los que ya veian la IP de cada visitante al pintar el mapa; esta dicho
en el aviso legal, en los dos idiomas, y al pie del propio bloque.

**Map tiles are deliberately never cached.** They come from OpenStreetMap, CyclOSM and Spain's IGN —
volunteer-run servers whose usage policy forbids bulk caching. Without signal the track is drawn on an
empty background, not on the map.

A **Waymarked Trails overlay** (the waymarked PR/GR/SL trails on top of the chosen base map) was
built and published on 7 October 2026 and **removed the same day at the user's request** — don't
re-add it. The slope toggle lives **inside `.map-layers`**, after a `.map-layers-sep` hairline: it
was in a second pill below the bar and the author wanted everything in one horizontal row. Only the
route pages have it (the home has no elevations in `trailhead.json`), and `ponExtra` adds the
separator the first time something is appended, so the home's bar stays as it was.

If the service worker ever needs killing, publish a `sw.js` whose whole body is
`self.registration.unregister()`; browsers that already have it will pick that up and detach themselves.

Each language links its own `manifest.webmanifest` / `manifest.es.webmanifest`, differing only in
`start_url`, so installing from the Spanish side opens the Spanish home and not the Basque root.

**Theme.** Dark is the default for first-time visitors; light is the explicit opt-in, stored in
`localStorage` and applied by an inline script at the top of `<head>` (before first paint, to avoid a
flash of the wrong theme). The toggle button's script just flips it and writes back. Every page's inline
script must use the same criterion (`localStorage.getItem(key)==='light'`) — a route page that instead
defaulted to light unless `'dark'` was already stored caused a real bug: the very first page a new
visitor saw looked right, but the toggle button's own init code (`src/js/app.js`) wrote `'dark'` into
storage on that first load, so the second page (or the home page, if visited first) came up dark anyway.

**Route data pipeline.** Each route has a `src/<name>.gpx` (the real recorded track) and a
`data/<name>.json` (`tracks[].points` lat/lon pairs + `marker`/`waypoints`, consumed by
`src/js/map.js` via `data-map-src` on the page's map container). Those points are written by
`python3 scripts/make_map_data.py`, which also rewrites `data/trailhead.json` — **re-run it after
adding or replacing any GPX.** It simplifies with Douglas-Peucker (1 m on a route page, 10 m on the
home overview, which is seen far away), not by keeping one point in N. Decimation was what made the
tracks look hand-drawn: the site used to draw 16.556 of the GPXs' 427.501 points, 4%, and every bend
came out as a straight line. Keep it that way — the whole of `data/` is 2 MB on a 587 MB site, and
the heaviest route map is 53 kB. The elevation-profile SVG in the
route hero and the numbered waypoint markers are derived from the GPX by hand (Haversine cumulative
distance, local-maxima detection for peaks) when a page is built — there's no script that regenerates
them automatically; distance/elevation-gain figures in `.facts` are meant to reflect the real GPX, not
invented numbers. `data/trailhead.json` holds every route's track for the home-page overview map.
`src/js/map.js` reads waypoint labels straight from the page's already-rendered `.elev-legend` items
(not duplicated in the JSON), and derives the route's compass heading itself.

**A GPX must never start or end at the user's house, and must never go in front of it — always
along the BI-633.** Standing instruction, for every route. Two earlier attempts at this got it wrong
and both shipped, so read this before touching any track near Trabakua:

- The old rule measured **isolation from the trail network** (is the first point within ~90 m of
  another route's track?). It reads 0-5 m here, because the house fronts a road a dozen routes use,
  so it passed everything. Don't use it.
- The second attempt measured **distance from the house, point by point**. That also passed, for two
  reasons. First, what the map draws is the **straight lines between points**, and cutting a piece out
  and splicing another in left chords of up to 40 m that crossed the bend and went through ground the
  track had no point on. Second, beside the house there are **two ways that reach the same place**: the
  BI-633, and the author's own road, which leaves it, passes in front of the house about 25 m away and
  rejoins it 110 m to the south-west. Both sit a similar distance from the house, so distance alone
  cannot tell them apart.

What holds: **galdaramiño is the reference the author approved**, and it passes 39 m from the house.
`scripts/por_la_general.py` replaces a track's whole neighbourhood of the house with galdaramiño's own
points, stitched at two places where the track is already on the road (under 8 m), with the stitch ends
computed on the line rather than rounded to the nearest vertex. So the passage in front of the house is,
point for point, galdaramiño — there is no invented geometry. It is idempotent: running it twice changes
nothing the second time. `scripts/check_site.py` checks **segments, not points**: near the house no
segment may stray 15 m from the BI-633 nor be longer than 15 m. The margins live in
`scripts/.punto-privado.json`, which is **excluded from git** because this repository is public —
without it both scripts skip themselves and say so.

Mixing two recordings makes the per-point `<time>` false, so the splice drops it, as was already done in
sancristobaloiz, muniozguren and santaeufemia. Everything downstream shifts with the track and has to be
regenerated: `make_kml.py`, `make_map_data.py`, `rehaz_perfil.py` (profile, numbered points, distance),
`bundle_gpx.py`, the distance on the card and in the home page's `data-distance-km`, the kilometres the
body copy quotes for each numbered point, and the Basque behind all of them. The cumulative elevation
gain does **not** change: it comes from the route's own source, not from the GPX.

`scripts/rehaz_perfil.py` has two locks worth knowing about. It keeps the nine routes on the old
kilometre basis untouched (see "Content rules"), and it refuses to redraw a profile that is not drawn
with the 161-evenly-spaced-sample convention — trabakuamallabia's has 201 samples spaced by track point
and separated by spaces, and redrawing it would restyle it rather than correct it. It also picks which
**pass** a numbered point belongs to by the kilometre the author already wrote, not by the nearest point
on the track: trabakuamallabia goes through Zengotita at km 3,67 and again at km 14,71, and the nearest
point is the second one.

**Huge generated files.** Once a route page has embedded photos, `*_tail.html` and
`fonts/inline_fonts.css` contain very long base64 lines. **Do not open these with a plain read/edit
that loads the whole file, and do not print them in full** — filter by line length first (e.g. only
lines under ~300 chars) to find the real markup, and prefer targeted string replacement over
whole-file rewrites.

## Verifying changes

There's no automated test suite — verification is manual:

- After any Spanish text edit: `make_eu.py` (zero errors) → `build.py`, then check the rendered
  Spanish *and* Basque output (`grep`/read the generated root `.html`, not just the source) before
  committing.
- For layout/CSS/map changes: check with Playwright at multiple widths (at least 320, 390, 768,
  1280px) for horizontal overflow, and actually look at screenshots — not just the code — before
  calling it done. A local server (`python3 -m http.server` from the repo root) is enough to preview
  the built site.
- `git status` after `build.py` before committing — it regenerates files across the whole tree, so it's
  easy to accidentally stage an unrelated change. `optimize_images.py` no longer rewrites untouched
  photos, but check anyway after `--force`.
- **Una sola orden para verificar, y se mira su código de salida:**
  `python3 .claude/skills/run-rutas-mallabia/driver.py verifica` (todo, ~3 min) o
  `verifica --rapido` (sin navegador, ~50 s). Termina en una línea: `VERIFICACION CORRECTA (N pasos)`
  o `VERIFICACION FALLIDA: <pasos>`, con código 0 o 1. **No encadenes las comprobaciones a mano con
  `| grep … && echo "TODO CORRECTO"`**: `grep` sale con éxito por haber *encontrado* la línea, diga
  «fail 0» o «fail 1», y por eso el 18 de octubre una misma salida dijo «# fail 1» y debajo «TODO
  CORRECTO». Si lo que escribes acaba en `&& echo` algo, estás a punto de repetir ese fallo.
- **For a brand-new route page, or one you're doing major surgery on: before calling it done, diff
  its `_tail.html` structurally against a known-good page's (e.g. `arteta_tail.html`), and run
  `python3 .claude/skills/run-rutas-mallabia/driver.py todo`, which opens the built site in a real
  browser and checks layout at four widths in both themes, the search and filters, the map, the hero
  colours and the offline mode.** `trabakuamallabia` shipped missing the map/JS, the `<footer>`, the
  `#toTop` button, the elevation-profile markers, with a duplicated icon and untranslated strings —
  none of it caught because each fix only checked the one thing just reported, never the whole page
  against the template every other route already follows. Checking piecemeal, one user-reported bug
  at a time, is what let all of that ship in the first place — don't repeat it.

## Content rules

- **The waypoint kilometres stay as they are — decided, do not "fix" them.** Commit `e4967121`
  corrected the total distance of 17 routes against their GPX (e.g. trabakua 16,5 → 15,65 km) without
  recomputing the per-waypoint kilometres in the elevation-profile markers (`<g class="elev-marker">
  <title>Name · X km · Y m</title>`). 35 of the site's 239 waypoints therefore sit between +0,30 and
  +0,84 km ahead of where that point falls on the current track, every deviation positive; on trabakua
  all six match the old basis exactly (16,5/15,65 = 1,054, and 6,45 × 1,054 = 6,8, the figure on the
  page). Affected: sancristobal, trabakua, urregarai, zengotitagane, egoarbitza, kalamua, urko, arteta,
  zenarruza. **The user has looked at this and decided to leave them.** Recomputing them would also move
  each marker's `cx`, changing the elevation profile of nine pages. Don't raise it again or change it
  unless he asks; `check_site.py` deliberately does not check it.

- **Unos metros de diferencia en un track no son un error: no los trates como tal.** Lo dijo el autor
  con todas las letras — «100 o 300 metros no me llevan a nada» — y tiene razón: a quien usa la web
  para ir al monte, un tramo que en el mapa va por la recta en vez de por la curva no le cambia nada.
  No es un fallo que haya que arreglar ni que avisar. Lo que sí son fallos, y hay que seguir diciendo,
  son los datos que **contradicen** la realidad: una distancia que no cuadra con el GPX, un nombre de
  sitio equivocado, una fuente que no existe.
- **Los dos tracks que quedan con tramos rectos están decididos: no los vuelvas a plantear.**
  `intxorta` tiene un corte de grabación de 644 m al principio y **ninguna otra ruta recorre ese tramo
  entero**, así que cerrarlo exigiría inventarse el enlace. **El original de Wikiloc trae el mismo
  corte**: el autor lo bajó el 20-oct-2026 y lleva el salto exacto, entre (43.20953,-2.54842) y
  (43.21143,-2.55592), 644,4 m, los mismos metros y las mismas coordenadas. No es que el repositorio
  tenga una copia recortada: es que el aparato dejó de grabar ese día. No hay nada que recuperar. `longa` no tiene cortes: es una ruta
  **trazada en Wikiloc, no grabada** (81 puntos/km, sin `<time>`, cierra el círculo a 0,00 m exactos),
  y su descarga de Wikiloc es byte a byte la que ya está en `src/longa.gpx`, así que no hay original
  mejor que recuperar. Sus 52 tramos rectos son como se trazó. Déjalo estar salvo que él lo saque.
- Never invent route facts (distances, elevations, place names, waypoint order, water sources). This
  site documents real, personally-verified routes; when a detail is uncertain, ask rather than guess.
- **Always tell the user about missing data or factual errors you notice, even when they didn't ask
  and even when it's outside the task at hand.** He has asked for this explicitly: a page missing
  something every other page has (numbered waypoints, a card photo, an `og:image`), a figure that
  doesn't match the GPX, a place name that doesn't match the map, a stale generated file. Say it
  plainly, with the evidence, and let him decide — don't quietly fix a *fact* and don't quietly let
  it pass. Verify against a primary source first (the GPX itself, OpenStreetMap by coordinates,
  the built output) so the report is a finding and not a hunch.
- **Never reword text he didn't ask you to touch.** Adding a photo means: process it, add the
  gallery item, write its `alt` in both languages. It does *not* mean improving the neighbouring
  alts, retitling anything, or rewriting a paragraph because you now know more — he has asked for
  this explicitly. Same for a route text: change the sentence he pointed at, nothing else. When a
  nearby text looks wrong or improvable, say so and let him decide (see the rule above); don't
  fold the edit into an unrelated change.
- Cross-reference other routes by name where the text mentions them (e.g. "el mismo pico de la ruta de
  `<a href="arietzu.html">Osmagain y Arietzu</a>`") using a plain `.html` href, letting `make_eu.py`'s
  `EU_OF` swap handle the Basque variant.
- **The cement climb from Osma to Zengotitagane is hard for a normal (non-electric) bike.** Standing
  instruction from the user: whenever a route's track uses this climb, say so in the short "para quién
  es" summary (not necessarily in the user's own narrative body-copy, which stays near-verbatim per the
  rule above) — e.g. "la subida de cemento desde Osma hasta Zengotitagane es dura para una bici normal,
  recomendable con e-bike." First applied on `axmakurandikoa`.

## Basque translation style

The user has repeatedly rewritten machine-drafted Basque body text with their own preferred wording.
When writing or revising Basque route text, favor their established tone and word choices over a
literal/formal translation:

- Natural, friendly, close-to-spoken register — not a stiff calque of the Spanish sentence structure.
  It's fine to reorder a sentence or split/merge clauses if that reads better in Basque, as long as no
  fact changes.
- Preferred vocabulary: **"eolikoak"** as the standalone noun for wind turbines (not "aerosorgailuak"),
  except inside a "parke eolikoaren aerosorgailuak/aerosorgailuek" construction, where "aerosorgailu"
  is the correct head noun and "eoliko" already modifies "parke" — don't double up on "eoliko" there.
  "Haize-errotak" is also an accepted alternative in some contexts, by the user's own choice. Always
  **"zirkuitua"** for "circuito" (never "zirkulua").
- Bold placement on inflected words: bold only the stem and leave the case suffix outside, e.g.
  `<b>Egoarbitza</b>rako`, `<b>San Migel</b>eko`, `<b>Kalamua</b>ko`, matching the pattern already used
  throughout `eu.py` — not `<b>Egoarbitzarako</b>`.
- Use plain ASCII hyphens (`-`) and apostrophes; normalize any non-breaking hyphen (U+2011) or curly
  punctuation that shows up in dictated text before it lands in `eu.py`.
- When the user pastes a full replacement paragraph in Basque, treat it as close to final: reuse it
  near-verbatim, re-inserting only the `<b>`/`<a>` tags at the equivalent spots and fixing the items
  above — don't rewrite their phrasing back toward a more literal translation.
