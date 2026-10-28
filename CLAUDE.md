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
python3 scripts/make_alturas.py        # data/alturas.json: la altura de cada punto del mapa de la portada
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

**Las capas: cuatro, iguales en la portada y en una ficha, y las dos abren en Bici.**
IGN, **Bici** (CyclOSM), **Topo** (OpenTopoMap) y Satélite.

**El 28 de octubre salió «Euskadi» y entró OpenTopoMap, y conviene leer por qué antes de deshacerlo.**
El autor: «el mapa Euskadi no me dice nada; quiero nombres abundantes y más curvas de nivel, para que
al mover el mapa se sepa dónde andas buscando». Medido sobre **la misma tesela** de Mallabia a **zoom
13**, que es el zoom al que uno busca:

| capa | nombres | curvas |
|---|---|---|
| Euskadi (geoEuskadi topo) | **3**: Markina, Mallabia, Mendibil | sí, finas |
| Bici (CyclOSM) | **0**, sólo «BI-633» | sí |
| **OpenTopoMap** | **8, y con su altura**: Mendigaña 467, Mendibil 613, Olamendi 600, Arteta 514, Ariznabar 592, Galarraga 415, Trabakua 404, más la BI-633 | sí, **rotuladas** |

Lo de Euskadi no era falso —rotula los caseríos uno a uno y en euskera— pero **sólo de z15 para
arriba**: a la distancia a la que uno busca, callaba. Se probó además ponerle encima el híbrido de
geoEuskadi y a z13 saca **los mismos tres**, así que no arreglaba nada. El autor las vio juntas y dijo
«quita Euskadi».

**El pero sigue en pie: las carreteras de OpenTopoMap son naranjas**, el mismo color que los trazados
de bici, y es justo por lo que estaba descartada desde octubre. Pesa menos que entonces porque desde
octubre los trazados llevan reborde oscuro, pero en la portada, al zoom de apertura y con las 67 a la
vez, **se nota**. Si vuelve a salir el tema, es esto y no otra cosa.

**El híbrido de geoEuskadi NO se fue**: sigue encendiéndose con el satélite en las fichas y en
`agua.html`, así que geoEuskadi continúa en el aviso legal. Y **OpenTopoMap se añadió a esa lista**,
que es un tercero nuevo: la sirve un proyecto de voluntarios, como CyclOSM, llega a **z17** y su
licencia pide citar a OpenTopoMap y a OpenStreetMap. Esto se movió mucho entre el 23 y el 26 de octubre de 2026 y
conviene leer el recorrido entero antes de volver a tocarlo, porque cada paso lo pidió el autor:

1. Hasta el 23 de octubre las fichas abrían en Bici. El autor avisó de que «al mapa bici le cuesta
   abrir mucho» y se metió un callejero de OSM, que pasó a ser el que abría en las dos.
2. El 26 pidió «un mapa muy detallado con rutas y calles, que se vean bien los nombres de lugares».
   Se midieron siete candidatos sobre 18 teselas reales de Mallabia a zoom 13-14 y entró el estilo
   **Humanitarian (HOT)** como quinta capa; el autor quitó «Calles» en cuanto los comparó.
3. Horas después: **«no me gusta este mapa, Bici tiene más información»**. Y tiene razón — ver abajo.
   Fuera HOT, y **Bici vuelve a ser la que abre**, también en las fichas.

4. El 27 de octubre el autor pidió **una capa más**: «busca hasta encontrar algo que se te haya
   pasado por alto, algo decente». Y había un hueco de verdad: **todo lo probado hasta entonces era
   global** (OSM y sus derivados, Esri, el IGN estatal). Faltaba la cartografía **propia de
   Euskadi**. Entró el **mapa topográfico del Gobierno Vasco (geoEuskadi)**.

**Por qué el de Euskadi merece estar, mirado sobre el mismo trozo de Garai y Zengotitagane:** es la
única carta de la lista que hace quien conoce el terreno. Rotula **los caseríos y los parajes uno a
uno y en euskera** —Askako, Zazpiatxeta, Aretxerriaga, Urdaia, Sarrimendi, Gaztelumendi, Axmakurra,
Iturrizuri, Zengotitagana, Kurutzetorri, Olatzamendi, Osmagain, Besoita, Galarraga—, que son
literalmente los nombres de las rutas de esta web, y ninguno de los otros tres los saca. Las curvas
de nivel son mucho más finas que las del IGN y van con sombreado del relieve.

Datos del servicio, comprobados desde aquí y no leídos en su web:

- WMTS con **`GoogleMapsCompatible`**, así que entra en Leaflet tal cual, sin reproyectar — y eso no
  era de esperar, porque sus metadatos anuncian EPSG:25830. Probablemente sea la razón por la que
  casi nadie lo usa fuera de su propio visor.
  `https://www.geo.euskadi.eus/geoeuskadi/rest/services/U11/WMTS_TOPO/MapServer/WMTS/tile/1.0.0/U11_WMTS_TOPO/default/GoogleMapsCompatible/{z}/{y}/{x}.png`
- Llega a **z18**. Teselas de 80-145 kB y 0,5-1 s: de las más pesadas, pero la tardanza ya no es un
  criterio (ver abajo).
- **Licencia CC BY**: «se permite cualquier uso si se menciona la autoría del siguiente modo: Eusko
  Jaurlaritza / Gobierno Vasco». Es la más clara de todas las candidatas, mejor que la del IGN y que
  la de CyclOSM.
- **Cubre las 66 rutas enteras**, Gipuzkoa incluida: comprobadas tesela a tesela las cuatro esquinas
  del conjunto (43,1234-43,3274 N, 2,6524-2,3561 O), todas con contenido.

**Nombres sobre el satélite.** Lo pidió el autor: «el mapa sat, ¿pueden aparecer nombres?». Con el
satélite se enciende además una capa transparente de rótulos, el **híbrido de geoEuskadi**, y se
apaga al cambiar de capa. Va en `rotulos`, dentro del `layerDef` del satélite, y **se quita dentro
de `listo()`, con su capa y no antes**: si se quitara en cuanto se pulsa otro botón, desaparecería
mientras la capa nueva todavía está cargando. Se compararon dos sobre la ruta de Zengotitagane en
1280x900:

- **Esri «World Boundaries and Places»** pone sólo los nombres y no toca la imagen — pero es
  escuetísimo: en ese encuadre saca **un solo rótulo** («Garai»).
- **El híbrido de geoEuskadi** saca **treinta y tantos** —Askako, Sarrimendi, Urdaia, Axmakurra,
  Iturrizu, Zengotitagana, Kurutzetorri, Olatzamendi, Gaztelumendi, Osmagain, Sallobente, Besoita,
  Andikoa, Momoitio, Galarraga…— más los arroyos y los números de carretera.

**Y al final se usan los dos, uno en cada mapa.** Sobre una ficha, con un solo track, el híbrido es
el bueno: las carreteras las saca en amarillo, el track va más grueso y con flechas, y se
distinguen. **Sobre la portada no**: con las 66 rutas a la vez, las carreteras amarillas se enredan
con los trazados naranjas y verdes — «se lía buena», dijo el autor con la pantalla delante. Así que
la portada lleva el de Esri (nombres y nada más) y la ficha y `agua.html` el de Euskadi. `agua.html`
no dibuja ningún track, solo los puntos de agua, así que ahí no hay nada con lo que enredarse.

Lo que se pierde en la portada: los rótulos de Esri **no están en euskera** (dice «Guipúzcoa», no
«Gipuzkoa»). Es el mismo caso que el IGN y CyclOSM, que tampoco lo están.

El híbrido pesa unos 10 kB por tesela y no añade ningún dominio nuevo. Cubre las cuatro esquinas del
conjunto; la del noreste devuelve una tesela vacía de 192 bytes porque es **mar abierto al norte de
Mutriku**, y es correcto que lo haga.

**La línea de créditos ya no es un banderín blanco.** Con el satélite citando a Esri y a geoEuskadi
se iba a **dos líneas** y cruzaba el mapa de lado a lado (390x34 px, medido en un móvil), con el
fondo blanco al 80 % que trae Leaflet de serie — en una web oscura, un cartel. No se pueden
esconder, son la atribución de quien sirve las teselas, así que se les puso el color de la web, 10,5
px y una esquina redondeada, y los textos se acortaron a lo que cada licencia pide de verdad. Los
rótulos de Esri van **sin `attribution` propia**: la foto de debajo ya cita a Esri y repetido salía
«© Esri, Maxar, © Esri». Ahora son 125x15 px y una línea.

**Cuatro botones ya no caben en una fila estrecha, y la pastilla pasa a dos filas.** A 320 px la
pastilla mide 142 y el texto 182; en una ficha, con «Pendiente», tampoco entra a 360 ni a 390. Antes
salían con puntos suspensivos, que es peor que partir: `.map-layers` lleva ahora `flex-wrap:wrap` y
sólo crece cuando hace falta. Medido en las dos lenguas, en la portada y en una ficha, a
320/360/390/768: **no se corta ningún rótulo en ninguna**.

**La razón por la que la lentitud ya no cuenta** es que el autor la retiró con todas las letras: «no
me preocupa lo que tarde en abrir en el monte, poca gente o ninguno; la ruta la organizo en casa».
CyclOSM sigue siendo de las más pesadas (medido aquí, 125 ms y 41,3 kB por tesela frente a 122 ms y
19,8 kB de HOT), pero eso ya no es un criterio. `ponerCapa()` tapa la capa vieja con la nueva, así
que cambiar de capa no deja el mapa en blanco.

**Por qué Bici gana, comparado sobre el mismo trozo de Zaldibar a zoom 14:** curvas de nivel con su
altura, todas las cimas rotuladas con la suya, los arroyos con nombre (Zolduerreka), y cada pista y
sendero dibujado con un trazo distinto según lo que sea. Ningún otro junta las cuatro cosas.

**Los descartados, todos medidos y mirados, para no volver a probarlos:**

| | por qué no |
|---|---|
| **HOT / Humanitarian** | rotula menos cimas que el OSM normal; el autor lo rechazó a la vista |
| **Calles / OSM estándar** | menos información que Bici; lo quitó el autor |
| **OSM Francia** | muchos topónimos pero **sin curvas de nivel** |
| **OSM Alemania** | es el OSM de siempre con otro color; lento e irregular desde aquí |
| ~~**OpenTopoMap**~~ | **entró el 28 de octubre en lugar de «Euskadi»** — ver arriba. Lo de las carreteras naranjas sigue siendo verdad |
| **MTB Map** (mtbmap.cz) | el que más topónimos saca de todos, pero pinta las carreteras en rojo y amarillo chillón y lo sirve un servidor de aficionados **sin condiciones de uso publicadas** |
| **CyclOSM-lite**, **4UMaps** | **muertos**: error en las doce teselas |
| **Esri World Topo / Street**, **IGN Mapa Base** | limpios pero sin senderos: el monte sale vacío |
| **CARTO Voyager** | ya no es libre: devuelve una tesela con «API KEY REQUIRED» estampado |
| **Hike & Bike Map** | **muerto**: ni `tiles.wmflabs.org` ni `a.tiles.hikebikemap.org` responden |
| **Strava / Garmin (mapa de calor)** | **no se puede**: desde 2018 sus teselas exigen sesión iniciada y sus condiciones no permiten usarlas fuera de su web. No es cuestión de buscar la vuelta |

`scripts/check_site.py` exige que `map.js` declare **seis** `L.tileLayer` —cuatro de fondo más los
dos juegos de rótulos del satélite— y que `js/agua.js` lleve las mismas seis URL (su copia existe porque `map.js`
son 1.100 líneas atadas a los tracks). `test_ui.cjs` comprueba la lista de botones y que la que abre
es la segunda, en la portada y en una ficha. **Al añadir o quitar una capa hay que tocar cuatro
sitios**: `map.js`, `agua.js`, el número de `check_site.py` y las tres listas de `test_ui.cjs`.

**Lo del ancho de los rótulos, que acabó arreglándose de otra manera:** en octubre, con cuatro
botones, eran 144 px de texto en una pastilla de 142 y «Bici» y «Calles» salían con puntos
suspensivos, y se resolvió quitando una capa. Al volver a cuatro en octubre se resolvió bien, con
`flex-wrap`.

**«Rutas»: el interruptor para ver el mapa a pelo.** Lo pidió el autor — sobre el satélite, y donde
se juntan varias rutas, los trazados tapan justo lo que quiere mirar. Va **en la misma pastilla que
las capas**, detrás de la raya, como el de la pendiente (`ponExtra`), y lo llevan la portada y las
fichas. No borra nada: la clase `sin-rutas` en `[data-map-src]` esconde los trazados, sus rebordes y
los marcadores (salida, puntos numerados, kilómetros), y **deja el trazado que se esté dibujando**,
que lleva `.draw-line`.

Dos cosas de sitio, medidas: por debajo de **420 px** el rótulo no cabe y el botón se queda en un
ojo; por debajo de **360 px** no caben ni cinco botones en la pastilla (a 320 la caja del mapa mide
238 px y la pastilla 142), así que ahí el ojo **se sale de la pastilla** y baja a la columna de la
derecha, bajo el botón de ampliar, con el lápiz corrido a 94 px y las opciones de dibujo a 136.
Ojo con `scripts/test_ui.cjs`: las comprobaciones de la barra cuentan **capas**, así que filtran
`.map-rutas-btn`, y la portada ya sí tiene `.map-layers-sep` aunque no tenga «Pendiente».

**El reborde oscuro de los tracks de la portada.** El autor avisó: «el color en el mapa index es
pobre». Los tracks iban al 85 % de opacidad y 4 px **sin reborde** — el reborde blanco solo lo
llevaban las fichas, y en la portada se había descartado por no dibujar 57 líneas más. Sin él, el
verde lima de «a pie» se funde con el verde del campo del callejero y el naranja se confunde con las
carreteras naranjas del IGN. Se compararon cuatro arreglos sobre el mismo trozo de mapa y las dos
capas: subir la opacidad y el grosor (mejora poco), **el reborde oscuro**, y colores más vivos
(`#FF6A00` / `#43D419`, que funciona pero obliga a elegir entre dos verdes distintos en la misma
página o a cambiar la paleta entera). Se eligió el reborde: arregla las dos capas **sin tocar ni un
color de la web**.

Va en **su propio panel** (`map.createPane('rebordes')`, `z-index` 395, bajo el de los trazados en
400): intercalado en el mismo panel, el reborde de una ruta taparía el track de otra. Y **se apaga
con su trazado** en los tres sitios donde se apagan las líneas (filtro, abrir ficha, cerrar ficha);
si no, al elegir una ruta quedarían 64 líneas oscuras marcando justo las que están apagadas. Los
tracks suben a 4,5 px. La opacidad subió a 1 con el reborde y el autor la vio dura con los 66
trazados a la vez sobre el mapa ciclista («hazlos un poco más suaves, solo un poquito»): **en la
portada van al 0,85** y en una ficha, con un solo track y reborde blanco, se quedan en 1. Quien da
la definición es el reborde, así que bajar la opacidad no devuelve el problema de antes. Medido: el mapa queda listo en **0,22 s** en escritorio y
**0,75 s en un móvil con la CPU frenada 4x**, con 65 trazados y 65 rebordes.

**El grosor de la portada va con el zoom** (`ajustaGrosor` / `pesosDeZoom` en `src/js/map.js`). El
autor: «las líneas de las rutas en index que sean más estrechas, ocupan mucho en el mapa». Y es
verdad de lejos —las 66 a la vez se juntan en una mancha— pero no de cerca, donde una línea fina
cuesta de ver sobre el satélite y de acertarle con el dedo. Por eso no hay un número fijo: **2,5/4
hasta el zoom 12**, **3,5/6 del 14 en adelante** y 3/5 en el escalón de en medio. (Arrancó en
3/5–4,5/8 y el autor las quiso aún más finas: «así se verá mejor la información de fondo».) La portada
abre en zoom 10, así que lo que se ve al entrar es la fina.

**Y por debajo del 11 el reborde se va del todo** (grosor 0, que en SVG no dibuja nada): ahí las 66
están tan enredadas que no separa nada, sólo engorda la mancha. Lo pidió el autor sabiendo lo que
cuesta. Dos avisos medidos: se apaga **con el grosor y no con la opacidad**, porque la opacidad del
reborde la llevan el filtro y la ficha abierta y se pisarían; y la salida temprana de
`ajustaGrosor` **compara los dos pesos**, que entre el zoom 10 y el 12 el trazado mide igual (3) y
lo único que cambia es el reborde. Sobre satélite y sobre el callejero queda limpio; **sobre el IGN
se paga**, que es donde el naranja de los tracks y el de sus carreteras vuelven a competir — es
justo el problema que el reborde arregló en octubre, y a zoom 10 reaparece. Se reengancha en `zoomend` y sale pronto
si el peso no cambia, así que no recorre los 66 por cada rueda del ratón.

Los pesos son ahora `pesoTrack`/`pesoReborde` y **no quedan literales**: el filtro, abrir ficha,
cerrar ficha y el resalte del ratón los leen de ahí, que si no se pisan entre ellos. `ajustaGrosor`
toca **sólo el grosor**, nunca la opacidad: ésa la llevan el filtro y la ficha abierta, y pisarla
encendería rutas apagadas a propósito. Ojo al medir desde Playwright: los rebordes **no están en
`.leaflet-overlay-pane`** sino en `.leaflet-rebordes-pane`, y buscarlos en el primero devuelve cero.

**La ficha del mapa tapaba demasiado: panel sin foto y caja alta.** El autor, con la captura de su
movil delante: «algún otro método que abra todo sin tapar tanto los mapas». Se midieron cuatro
maneras sobre la misma ruta, en 393 px, contando el mapa que queda libre:

| | mapa libre |
|---|---|
| **la caja crece a 72svh** | **68 %** |
| **ficha sin foto** | 60 % |
| ficha en un lateral | 43 % |
| como estaba | 37 % |

**El lateral se descartó en octubre y en noviembre se hizo, porque cambió la premisa.** Entonces se
midió sobre la caja tal cual —**cuadrada**, no apaisada— y salía peor: un lateral de 177 px sobre
311 deja una tira de 134 px en el móvil, y en el ordenador 54 % de mapa libre frente al 74 % de
entonces, porque allí la caja también es cuadrada (718x718). Lo que faltaba era la otra mitad de la
idea, que el autor dio después con la pantalla de AllTrails delante: **«el mapa ocupa la pantalla
entera»**. Con eso el lateral deja de quitar sitio, porque la caja gana ancho en vez de perderlo.
Medido en 1280x900: la caja pasa de 718x718 a **1280x824** y el mapa visible de 442.000 a
**792.000 px²**, casi el doble que con la ficha abajo. La lección es la de siempre: la medida valía
para la caja de entonces, no para siempre.

**El mapa a pantalla completa, y la ficha a un lado en el ordenador.** Al abrir una ruta, `map.js`
saca la caja de su columna centrada con un margen negativo y le da todo lo que queda bajo la
cabecera pegajosa (y, en el movil, sobre la barra fija de abajo) — **es la misma mecanica de
`encaja()` en `trazado.js`**, ya probada ahi, y el ancho sale de `clientWidth` y no de `100vw` por
la barra de desplazamiento. Lo pidio el autor dos veces y con las mismas palabras: «el mapa ocupa
la pantalla entera», «pantalla completa».

**Lo que cambia con el ancho es solo donde va la ficha**: de 768 px en adelante a la izquierda, de
arriba abajo, 320 px (280 entre 768 y 1023); por debajo, flotando sobre el mapa con 10 px de margen
y esquinas redondeadas, y escueta, como el autor eligio en octubre.

**En el movil la caja va `position:fixed; inset:0`** y se esconden la cabecera y la barra de abajo
(`body.mapa-pleno`, `.route-map-box.ficha-pleno`), no el alto en linea que escribe `map.js` para el
ordenador: asi no hay que calcular ningun desplazamiento para pegarla al borde de arriba —con la
cabecera escondida la pagina se recoloca sola— y la caja sigue a la ventana visible cuando el
navegador del movil esconde o saca su barra de direcciones. Se sale con la equis o tocando el mapa.

Medido en 390x844, el porcentaje de **pantalla** que es mapa visible:

| | |
|---|---|
| **asi, con la ficha flotando** | **86 %** |
| la ficha pegada abajo, sin margen | 85 % |
| solo sin cabecera, con la barra | 78 % |
| como estaba (caja de 390x711 bajo la cabecera) | 69 % |
| la ficha en un lateral, como AllTrails | **52 %** |

**El lateral se volvio a medir en el movil, ya con pantalla completa y a peticion del autor, y
vuelve a salir el peor**: 172 px de panel sobre 390 se comen casi la mitad. En el ordenador si gana.
En 1280 el porcentaje apenas se mueve (74 → 75 %), pero ahi lo que cuenta es el absoluto: de
442.000 a **792.000 px² de mapa**, casi el doble.

Tres cosas que hay que mover con ella y que costaron una vuelta:

- **Los botones de zoom y la escala** van en `.leaflet-left` y caen debajo del panel: se corren a
  `left:var(--ficha-ancho)`. Los creditos vuelven a `bottom:0`, que ahi ya no los tapa nadie.
- **La pastilla de las capas** va centrada entre `left:52px` y `right:52px` del mapa entero, asi que
  con el panel delante «IGN» se quedaba medio tapado. Se corre lo mismo.
- **El encuadre se hace dos fotogramas despues.** Al crecer la caja salta el `ResizeObserver` de
  `fit()`, que llama a `invalidateSize()`, y eso **corta el vuelo en seco**: la ruta se quedaba sin
  acercar, con el mapa en la vista de conjunto. El observador corre tras el calculo de estilos y
  antes de pintar, asi que al segundo `requestAnimationFrame` ya ha pasado. El hueco que se le pasa
  a `flyToBounds` es de **ancho** (`paddingTopLeft`), no de alto.

Y en el lateral **vuelven la foto y el perfil**, que se habian quitado por falta de sitio: en una
columna alta sobran, y ahi no repiten porque no se ve la tarjeta de la que salen. Con ellos va la
linea de resumen de la tarjeta, clonada tal cual — el autor lo autorizo con todas las letras: «si
hace falta clona cosas de la pagina». Todo se clona del DOM que ya esta en la pagina, asi que viene
en el idioma correcto y el navegador no descarga nada nuevo. Son **dos versiones de la ficha**
(`breve` y `amplia`) y manda el ancho; si la ventana cruza los 768 px con la ficha abierta, se
cambia de una a otra sin cerrarla.

La ficha del movil sigue siendo la escueta que el autor eligio en octubre, con las dos ganadoras
de entonces (que por si solas daban **78 % libre en un movil de 393 px**):

- **Sin foto ni perfil en la ficha** (`src/js/map.js`): solo nombre, datos y enlace. La foto se
  clonaba de la tarjeta de la portada —donde el visitante ya la ha visto— y cuando no había foto
  entraba el perfil de alturas en su lugar; entre las dos cosas, 195 px de ficha. Ahora son 134. En
  escritorio tambien baja, de 184 a 102 px, y ahí el mapa libre sube del 74 al 86 %.
- **La caja crece mientras hay una ficha abierta** (`.route-map-box.ficha-abierta`, **solo por
  debajo de 768 px**): de 311x311 a 311x611. Por encima de 768 no se toca, que allí la caja ya mide
  718x718 y ponerle 72svh la **encogería**. Va por clase y no por estilo en linea a propósito: el
  modo de dibujar escribe el alto en linea y tiene que seguir mandando — comprobado, abrir el lápiz
  con una ficha abierta la cierra y se queda con su propio alto, y al salir todo vuelve a 311x311.
  Hay que llamar a `invalidateSize()` **antes** de encuadrar, o Leaflet encuadra sobre el alto viejo
  y la ruta sale pequeña en la mitad de arriba.

**La linea de creditos de Leaflet iba por encima de la ficha del mapa.** Lo vio el autor en su
movil: al abrir una ruta en la portada, «© CyclOSM, © OpenStreetMap contributors» caia justo sobre el
enlace naranja «Ver ruta completa» y lo dejaba ilegible. La causa es de libro: los controles de
Leaflet van en **`z-index` 1000** y `.route-info-panel` estaba en **500**. Ahora el panel va en
**1100** y, como los creditos **no se pueden esconder** —son la atribucion de OpenStreetMap y de
quien sirve las teselas—, se corren hacia arriba lo que mide el panel
(`[data-map-src].con-ficha .leaflet-bottom{ bottom:var(--ficha-alto) }`).

La altura la escribe `map.js` en `--ficha-alto`, y **no basta con medirla al abrir**: la foto de la
ficha todavia no ha colocado y el panel crece despues, con lo que los creditos se quedaban unos
pixeles bajos y seguian metidos debajo. La vigila un `ResizeObserver` sobre el panel, que mide con
`getBoundingClientRect` y **no con `contentRect`** —el panel lleva 16 px de relleno arriba y abajo y
`contentRect` los deja fuera—. Comprobado a 320, 390, 768 y 1280 en los dos idiomas.

**Ojo al verificar: `driver.py verifica` falla a veces por un 429 de Open-Meteo.** La comprobacion
de «Lo mio» no admite errores de consola, y si el servicio del tiempo devuelve «429 Too Many
Requests» —porque se han hecho muchas peticiones desde esta IP— la da por fallida sin que haya
ninguna regresion. Se distingue mirando la lista de errores que imprime: si lo unico que sale es ese
429, no es el codigo. A los visitantes no les afecta, que el limite es por IP.

**La lectura del perfil de alturas se equivocaba hasta en 153 metros.** El perfil de cada ficha ya
era interactivo desde antes (`map.js`: raya, bola, «12,3 km · 450 m» y un punto que se mueve por el
track del mapa). Lo que estaba mal era devolver la `y` del dibujo a metros: usaba un **margen fijo
de 8 px**, es decir daba por hecho que la `y` iba de 8 a 292 en todas las fichas.

**No es así, y esto es lo que hay que recordar: las fichas publicadas usan seis convenciones
distintas.** `scripts/rehaz_perfil.py` documenta 161 muestras con
`y = 285 - (ele-min)/(max-min)*270`, pero lo que hay en la web son **160, 161, 163, 200 y 201**
muestras, y la `y` va de `(0, 300)` en astarlokoatxa a `(47, 225)` en oiz. Medido sobre la web
publicada, el error de la lectura llegaba a **153 m**: en zenarruza el punto más bajo decía 385 m
donde su propio pie dice 232, y en oiz 547 donde dice 399.

La escala se saca ahora **del propio trazado**: la `y` más alta es la altura mínima y la más baja la
máxima, y esos dos números están escritos en `.elev-tags`. Se autocalibra, da igual con qué
convención se dibujara la ficha y seguirá valiendo si mañana se dibuja de otra manera. Comprobado en
18 fichas de todas las convenciones: el peor error pasa de 153 m a **6 m**, y lo que queda es la
resolución del ratón sobre un pico estrecho, no la cuenta.

**Y se dejan de contar los puntos en cuanto la x retrocede.** `axmakuriturrizuri` y
`zengotitaosmagain` tenían la **línea** del perfil con el cierre del relleno pegado al final
(`… L1000,300 L0,300`): era copia literal del trazado de relleno, cierre incluido, así que traían
dos puntos de más pegados al suelo y **una raya naranja sobrante cruzando el fondo del recuadro**.
Ya se ha quitado ese trozo del `d` del trazado con `fill="none"` (el relleno sigue igual, y no se ha
tocado ningún número), pero la defensa se queda puesta: un perfil va siempre hacia la derecha, así
que en cuanto la x retrocede se corta. Eso protege además la búsqueda binaria de `yAtX`, que da por
hecho que la x es monótona.

Ojo: esas dos se generaron con otra receta — el relleno lleva `fill="url(#lg)"` y el trazado de la
línea va **primero**, al revés que en las demás. Si aparece una tercera así, es el mismo molde.

**No hace falta escribir otro módulo para esto.** Se intentó (`src/js/perfil.js`, 26 de octubre de
2026) sin haber mirado antes `map.js`, y salió un duplicado entero de algo que ya existía. Se
retiró. Antes de dar por nueva una función del mapa o del perfil, buscar en `map.js`: son 1.400
líneas y lleva dentro mucho más de lo que parece.

**Al elegir una ruta, los kilometros de las demas desaparecen.** Con la ficha abierta seguian
ahi las 64 etiquetas restantes, justo encima de lo que el visitante ha ido a mirar. `labelSoloHref`
en `src/js/map.js` guarda el `href` de la elegida y `updateLabelVisibility()` deja ver solo esa;
al cerrar la ficha vuelven todas. Lo pidio el autor: «quedarse solo en la ruta limpia». Ojo: si al
encuadrar la ruta el mapa baja del zoom 12 no se ve ninguna, y es correcto — por debajo de ese zoom
no hay etiquetas.

**Las pastillas de kilómetros se agrupan cuando se pisan.** Idea del autor, con la pantalla de
AllTrails delante: que el mapa de la portada sea un mapa de kilómetros por los que elegir, y que al
tocar uno se abra esa ruta. «Los kilómetros los dejas donde están, por donde pasan» — en el punto
medio del recorrido, no en la salida.

**Por qué hacía falta agrupar, medido:** al zoom de apertura (10) los puntos medios de las 66 rutas
caben **todos en un recuadro de 145x177 px**, y una pastilla de «32,46 km» mide 76x24. Son **717
parejas pisándose**. No es un problema de código: las rutas viven en un valle de seis kilómetros y a
esa escala caben en un sello. Por eso las etiquetas no salían por debajo del zoom 12.

| zoom | sitio que ocupan las 66 | parejas que se pisan sin agrupar |
|---|---|---|
| 10 (al abrir) | 145x177 px | **717** |
| 11 | 291x354 px | 245 |
| 12 | 581x707 px | 69 |
| 13 | 1163x1414 px | 23 |

Con el agrupado, **cero solapamientos a cualquier zoom**: al abrir salen «38 rutas», «17 rutas»,
«10 rutas» y un kilómetro suelto; al zoom 13, 15 grupos pequeños y 27 kilómetros sueltos. Suman
siempre 66.

Cómo está hecho, y las cuatro cosas que costaron:

- **Agrupado codicioso por cercanía en píxeles** (`RADIO_GRUPO` 46) **más una segunda pasada que
  funde los grupos cuyas pastillas aún se tocarían** (84x28 px). Sin esa segunda pasada quedaban 8
  parejas solapadas al abrir: el radio junta *puntos*, pero lo que no puede pisarse es la *pastilla*.
- **Se agrupa sólo lo que está en pantalla** (`map.getBounds().pad(0.15)`), y se recalcula también
  en `moveend`. Lo pidió el autor: al moverse al norte salen las de allí. Si no, un grupo seguiría
  diciendo «38 rutas» con cuatro en pantalla. Comprobado: en Markina salen 3 rutas, en Elorrio 7.
- **`var grupoCapa` va declarada arriba, con el resto del estado de las etiquetas, no junto a su
  función.** Estaba abajo con `= null`, y `updateLabelVisibility()` se llama durante el montaje,
  **antes** de llegar a esa línea: la primera pasada creaba la capa y esa línea borraba después la
  referencia, dejando los marcadores huérfanos para siempre. Se notó porque los grupos sumaban
  **100 rutas** habiendo 66.
- **`scripts/test_ui.cjs` usa un Leaflet de mentira** y no tenía `getBounds`, `containerPointToLatLng`,
  `L.layerGroup`, `L.point` ni `L.latLngBounds`. Sin ellos el test moría con código 137 (parecía
  falta de memoria y no lo era). Se le añadieron a la imitación, y `map.js` comprueba que existan
  antes de usarlos.

**La pastilla de grupo va en blanco y negro, no en naranja**, por la misma razón que la etiqueta
«Nueva»: en esta web el naranja es «en bici» y el verde «a pie», y un grupo mezcla las dos. Se
distingue de una de kilómetros por el tamaño y el peso. Crece con lo que agrupa (`es-media` a
partir de 6, `es-grande` a partir de 20) — **esa idea sí es de Leaflet.markercluster**, pero la
librería no se ha metido: son 66 puntos, lleva cinco años sin publicar versión y sería una
dependencia nueva, que aquí no entra sin que lo diga el autor.

**Y la salida sigue marcada en rojo, por encima de todo.** La pastilla de «38 rutas» cae justo
sobre Trabakua: el marcador lleva `zIndexOffset: 2000` y la pastilla se sube 16 px sobre su centro,
que señala una zona y no un punto exacto.

**La tira de rutas que tienes delante, debajo del mapa.** Lo pidió el autor: «si no, es difícil
saber si estoy en Mallabia, si estoy en Durango o dónde, cuando tengo el zoom aumentado». Con el
mapa muy cerca sólo se ven dos trazados sin nombre y el fondo no siempre rotula el pueblo.

Debajo del mapa van **las rutas que se están viendo** —las que tienen algún punto de su track
dentro del encuadre—, **con foto, título, distancia y desnivel**, y **cambian solas al mover o al
acercar**.

**La regla costó dos intentos, y el bueno es éste.** Primero fueron «todas las que caen en
pantalla», y el autor lo corrigió: «cuando aparecen los kilómetros de la ruta, si me aparecen 2 de
ellos que aparezcan 2 plantillas». Se pasó a mirar la pastilla de kilómetros… y eso rompía otra
cosa: **«no veo las plantillas de bajada a Unbe y a Ipurua; por mucho que veo la ruta trazada no me
abre ni una»**. Tenía razón: Unbe e Ipurua no son rutas, son sitios por los que pasan galdaramiño y
karabieta, y **la pastilla va en el punto medio del recorrido**, que mirando ese tramo queda fuera
de la pantalla. La regla que vale las cumple las dos: **si se ve el trazado, hay ficha.**

**Y sin tope.** Lo hubo y era el mismo fallo con otra cara. Comprobadas **las 66 rutas una a una**
—centrando el mapa en un punto al 15 % de cada track, lejos de su punto medio, a zoom 15— con tope
12 se quedaban **20** sin ficha teniendo el trazado delante, con 25 todavía **4**, y sin tope
**ninguna**. Cuesta unas decenas de nodos y las fotos ya están cargadas. Van ordenadas por cercanía
al centro, así que las que de verdad miras son las primeras. Las pidió así: «si son 7, aunque aparezcan
las primeras 4, las demás se quedan ocultas abajo» — en columna, con cuatro a la vista y el resto
desplazándose. **Tocar una encuadra la ruta entera y abre su ficha**, igual que tocar su pastilla:
medido, de zoom 15 pasa a 12 para que quepa completa. Eso responde a «¿pueden aparecer las rutas
enteras?» sin añadir nada.

**Y los trazados NO se quitan del mapa.** Se planteó un mapa de sólo kilómetros y el autor lo
paró: «yo no he dicho que no aparezcan los trazados». No volver a proponerlo.

Cómo está hecho:

- Se rellena desde `updateLabelVisibility()`, que ya corre en `zoomend` y en `moveend`: **el
  conjunto que calcula para agrupar las pastillas es exactamente el que hace falta aquí**, así que
  no se recorre nada dos veces.
- Las primeras son las más cercanas al centro de lo que se mira (`map.distance`), sin tope.
- El encuadre se comprueba contra **los puntos del track** (`rutasEnVista`), no contra la etiqueta.
  Son 66 rutas de unos 220 puntos y sale en cuanto encuentra el primero dentro, así que no se nota.
  Lo que no coge: un track que cruce la pantalla de lado a lado sin ningún punto dentro; a estos
  zooms no pasa, los puntos van cada 10 m.
- La foto es la que ya muestra su tarjeta en la lista, por `src`: el navegador la tiene cargada y
  no descarga nada nuevo.
- Se esconde con una ficha abierta o dibujando: ahí manda lo otro.

**Y va DESPUÉS de la caja del mapa, no dentro.** Metida dentro queda recortada y no se ve, porque
la caja tiene el alto fijo por `aspect-ratio`. Se inserta con `insertBefore` sobre el hermano
siguiente.

**Tres fallos propios al montarla, los tres del mismo tipo y por eso vale la pena recordarlos:**

- **`var tiraCercanas` declarada debajo de su primer uso.** Es **exactamente** el fallo de
  `grupoCapa` de unas horas antes, repetido: `pintaCercanas()` se llama durante el montaje, antes
  de llegar a esa línea, así que la primera pasada creaba la tira y la línea borraba después la
  referencia — y se creaba **una segunda tira**. Salían dos, una viva y otra congelada con 22
  fichas. **Todo lo que se cree desde `updateLabelVisibility()` va declarado arriba, con
  `labelSoloHref`.**
- **La firma de «lo que ya está pintado» no puede ir en `dataset`.** El DOM de mentira de
  `test_ui.cjs` devuelve un objeto **nuevo** en cada lectura de `dataset`, así que lo escrito se
  perdía; y no tiene `childNodes`. Entre las dos cosas el test se colgaba **sin imprimir nada**.
  Va en una variable del cierre.
- **A ese DOM de mentira le faltaba `insertBefore`**, y el test moría con código 137, que parece
  falta de memoria y no lo es. Se le añadieron `insertBefore`, `firstChild` y `nextSibling`, y
  `map.js` comprueba que existan antes de usarlos.

La lección, por tercera vez en el mismo día: **cuando el test de interfaz muere con 137 o se cuelga
sin imprimir, no es memoria — es que `map.js` está usando algo que su Leaflet o su DOM de mentira
no implementan.**

**La vista de mapa de la portada se lleva la pantalla (móvil).** Lo pidió el autor con su captura
delante: «¿cuándo se agranda el mapa? Es posible que ocupe más pantalla, más arriba, más ajustado,
para que abajo haya más sitio para las plantillas. Quisiera aprovechar todo lo más posible. Sobre
todo trazado, kilómetros y plantillas, lo que más se vea. Lo demás no tiene importancia mientras
esté a pantalla completa el mapa».

Entre la cabecera y el mapa había una franja muerta y la primera ficha salía cortada. Con
`body.vista-mapa` (lo pone `filters.js` al cambiar de vista) se esconde la cabecera, la caja se
pone **fija de borde a borde** y la tira se lleva una franja de verdad justo encima de la barra de
abajo. Medido en 390x844: la caja pasa de **310x310 a 390x587** —casi el doble de superficie— y la
tira de quedarse cortada a **200 px**, tres fichas enteras y la cuarta asomando. El reparto es un
solo número, `--tira-alto`.

Tres cosas de las que acordarse:

- **La barra de abajo se queda.** Es por donde se vuelve a la lista y donde están A pie / E-bike /
  Filtrar. En una primera pasada se escondió también el botón flotante y **se quedó sin salida**:
  ése es precisamente «Lista».
- **`:not(.ficha-pleno)`** en la regla de la caja: al abrir una ruta manda la otra regla, que es
  `inset:0`, y sin eso no ganaría por especificidad.
- `filters.js` llama a **`window.__avisaMapaTamano()`**, que `map.js` publica sólo en la portada:
  la caja cambia de tamaño por CSS y Leaflet no se entera solo. **Lo llama también `trazado.js`**
  al entrar y salir del lápiz: la tira se pinta desde `updateLabelVisibility()`, que corre en
  `zoomend` y en `moveend`, y abrir el lápiz no dispara ninguno de los dos — sin el aviso la tira
  se quedaba puesta mientras se dibujaba, y tocar una ficha abría una ruta encima del trazo.

**Y el filtro de actividad, en una fila fina flotando sobre el mapa.** Lo pidió el autor: «muy
disimulada, donde no ocupe; a pie o bicicleta o todas, arriba, en una fila horizontal muy fina, por
color verde o naranja».

Son 28 px translúcidos con desenfoque, como la pastilla de las capas, **encima del mapa y no antes
de él**: así no le quita ni un píxel de alto ni al mapa ni a la tira de fichas — medido, la caja
sigue siendo 390x587 y la tira 200 px. El color es el que pidió y es el de toda la web: **verde
andando, naranja en bici**, y «Todas» en el color del texto, que no es ninguna de las dos
actividades. Abajo quedan **Lista y Filtrar**, dos cajones anchos en vez de cinco estrechos.

Cuatro cosas que costaron una vuelta:

- **`.finder-toolbar` lleva `z-index:70`, o sea que es su propio contexto de apilamiento**, y el
  `z-index` de la fila sólo cuenta dentro de él. Con la barra en 70 y la caja del mapa en 150, la
  fila **se veía dibujada y no se podía pulsar**: todos los toques se los quedaba el mapa. Lo que
  sube a 160 es la barra entera, no la fila.
- En la barra `.activity-filter` es `display:contents` —se disuelve para que sus tres chips sean
  celdas de la rejilla—, así que aquí vuelve a ser una caja de verdad y la rejilla baja a **dos
  columnas**.
- **La barra no se aparta en esta vista** (`transform:none`). Además de que no hay nada que
  desplazar, un `transform` en ella la convertiría en el marco de referencia de la fila fija y ésta
  dejaría de ir pegada a la ventana.
- **Los mandos del mapa bajan los 28 px**: los de Leaflet por `.leaflet-top`, la pastilla de las
  capas por su `top`, y la columna de la derecha (ampliar, lápiz, opciones y, por debajo de 360 px,
  el ojo de «Rutas») con un `translateY` — cada uno tiene su propio `top` y por debajo de 360 todos
  cambian, así que trasladarlos vale para los dos repartos sin repetir ni un número.

Y **dibujando la caja se queda también con la franja de la tira** (390x787 en vez de 390x587), que
ahí la tira no está. Lo marca `body.dibujando`, que pone `trazado.js`.

**Ojo al mirar capturas de la portada en el móvil: hay un iframe de Google Maps detrás** (el de
«Dónde aparcar», en el acordeón). Chromium lo compone en su propia capa y **en las capturas de
Playwright el texto de alrededor aparece pintado por encima de la barra fija**, como si se
transparentara. No es un fallo de CSS: `elementFromPoint` dice que arriba está la barra, y quitando
el iframe del DOM la captura sale limpia. Se perdió un rato dándole vueltas a un `background`
translúcido que no tenía nada que ver.

**Los atajos a la información del final.** Lo levantó el autor: «no creo que nadie baje hasta
abajo, así que es posible que nunca lleguen a leer dónde comer o dónde dormir». Y tenía razón,
medido: **la portada mide 43 pantallas en un móvil** (36.506 px con 67 tarjetas) y el bloque de
«Dónde aparcar» empieza en la **42**; en el ordenador, 15 pantallas y empieza en la 15. En vista de
mapa sí queda cerca, porque el mapa ocupa una pantalla y la información viene detrás, y por eso él
notaba la diferencia.

Debajo de la cabecera va ahora una fila fina de cinco pastillas —**Aparcar, Comer, Dormir, Agua,
Preguntas**— que lleva allí de un toque. Cuesta **30 px** y cabe entera a 390 px en los dos
idiomas. Resuelve las dos mitades del problema: el viaje y, sobre todo, **saber que eso existe**.
Las rutas siguen siendo lo primero; se descartó subir el bloque entero encima de la rejilla, que
cuesta unos 300 px y pone «Dónde aparcar» antes que las rutas.

Dos cosas del montaje:

- **El enlace solo no basta.** Ahí abajo hay `<details>` plegados, así que saltar al ancla deja al
  visitante delante de un título cerrado. El bloque del final de `src/js/app.js` abre el que toca
  antes de ir, y espera **dos fotogramas** antes de medir, como en las preguntas: al abrir el
  `<details>` la página crece y la posición de antes ya no vale.
- **El salto es instantáneo, no suave.** Son 35.000 px en un móvil; animarlos sería un viaje de
  varios segundos.

Ojo: la portada tiene **dos** `section.info-accordion`. La de arriba es `#beforeYouGo` («Léelo antes
de salir») y la de abajo es `.practical-info`, que es ésta. Buscar por `info-accordion` a secas coge
la de arriba.

**Y una vez allí, saber dónde estás y cómo salir.** Lo levantó el autor en cuanto probó los atajos:
«cuando uno abre dormir o aparcar no sabe en qué parte de la página está, ni cómo salir de ahí».
Medido: caes en el **píxel 35.859 de 36.933**, la fila de atajos queda 35.332 px arriba y el bloque
**no tenía título** — la cabecera es la misma en toda la web, así que no orienta. El botón redondo de
«volver arriba» sí se ve ahí (comprobado, `y=720`, opacidad 1), pero él no lo registró como la salida,
que para el caso es como si no estuviera.

Dos cosas, las dos en el flujo y no flotando: un **título** al bloque («Información práctica») y un
**«↑ Volver arriba» escrito al final**, que hace lo mismo que el botón redondo —se le engancha la
misma función en `app.js`— para que no suba uno de golpe y el otro rodando.

**Y el atajo encuadra el BLOQUE, no el apartado.** Con el apartado, saltando a «Dormir» el título se
quedaba fuera de pantalla y seguías sin saber dónde habías caído. Los cinco plegados ocupan unos
250 px, así que yendo al principio del bloque se ven el título, las cinco filas —puedes saltar de
Dormir a Aparcar sin subir— y el que se acaba de abrir.

**Se descartó una X**, que fue lo primero que él propuso: una X significa «cerrar lo que se ha abierto
encima», aquí no hay nada encima —sólo has bajado— y al pulsarla seguirías en el píxel 36.000.
También se descartó, de momento, repetir la fila de atajos dentro del bloque o dejarla pegada arriba.

**Y un poco de color en esos desplegables.** El autor los vio en su móvil: todo gris, cinco filas
iguales. Llevan ahora el mismo tratamiento que los de `preguntas.html` —un `--acento` con su versión
suave— y el acento es **`var(--link)`**, que es el que esa página usa para lo que **no es una
actividad**: el verde y el naranja están cogidos y aquí dirían algo que no es. Se enciende lo justo:
el icono siempre teñido, y al abrir el círculo pasa a relleno, el título y el signo toman el acento y
el cuerpo coge un lavado muy suave. Cerrado sigue siendo una lista tranquila.

**La provincia se va de la barra en todo el móvil.** El autor lo vio en el suyo: «Bizkaia» acababa
justo donde empiezan los iconos. Medido el hueco entre el rótulo y el primer botón: **0 px a 360, a
390 y a 412** —se tocaban—, 17 a 430 y 67 a 480. Apretaba en todos los móviles corrientes, no sólo
en el más estrecho, que es donde se había arreglado en octubre al entrar «Compartir». Ahora
`.place-prov` se esconde hasta **479 px** y el hueco pasa a 24 / 54 / 76 / 94 px. De 480 en adelante
se queda. Las fichas de ruta no se tocan: ahí sobran 204 px a 390, que llevan menos botones.

**El filtro de actividad recentra el mapa de la portada.** Pasar de «A pie» a «E-bike» dejaba el
encuadre donde estuviera — y si el visitante había arrastrado el mapa, podía quedarse mirando una
zona sin ninguna de las rutas que el filtro deja. `encuadraVisibles()` en `src/js/map.js` reencuadra
sobre las rutas visibles **aunque el visitante ya hubiera movido el mapa**, y marca `userMoved` para
que el siguiente cambio de tamaño del contenedor no devuelva el encuadre general y lo deshaga. Solo
se dispara **cuando el conjunto visible cambia de verdad** (la firma de los `href` visibles), para no
dar un salto por cada tecla del buscador que no quita ninguna ruta; la primera vez solo se anota la
firma, porque de ese encuadre inicial ya se ocupa `fit()`. Solo en la portada.

**Compartir, también en la portada.** Lo pidió el autor: hasta ahora el botón sólo salía en las
fichas y no había forma de pasarle la web entera a nadie desde la principal. Va en la misma barra de
arriba y en el mismo sitio que en una ficha, delante del idioma. **Guardar no**, que ahí el corazón
va en cada tarjeta y uno para «toda la web» no diría nada. El texto que comparte no sale del `h1`
—que ya es «Trabakutik» y saldría repetido— sino de una línea propia con **las rutas contadas en el
momento**, para que el número no se quede viejo: «Trabakutik · 66 rutas a pie y en e-bike por
Mallabia y alrededores».

Costó un arreglo de sitio: a **320 px** la barra ya iba al límite («ahí no sobran más que un par de
píxeles», dice el comentario de `home.css`) y el botón la sacaba **30 px** de la pantalla. Por debajo
de 360 px la portada deja el rótulo en **«Mallabia»** a secas (`.place-prov`, sólo en la portada):
son 69 px que sobran de la provincia, de sobra para el botón y para la holgura que faltaba desde
antes.

**El número de rutas lo escribe el build, no la mano.** Las fuentes ponen `{{RUTAS}}` y
`pon_cuantas_rutas()` lo cambia por `len(_trailhead())`, que es la lista de tracks del mapa de la
portada — justo de lo que hablan esos textos («caminos grabados en alguna de las N rutas», «esconde
los N trazados») y el mismo fichero del que sale el zip, así que las dos cifras no se pueden
separar. Lo pidió el autor después de encontrárselo viejo: la página de preguntas decía «las 65
rutas» con 66 publicadas, el euskera «65ak zip bakar batean» y el comentario de la 404 seguía en 61.
Eran **ocho sitios** que había que recordar en cada ruta nueva.

Va al final de la cadena de cada página, y **la 404 se escribe fuera de ese bucle**, así que
`write_404_page` lo llama aparte. Las dos comprueban que no quede ninguna marca sin sustituir y
**paran el build** si queda. Probado de verdad: con un track de más en `trailhead.json` las páginas
pasan a decir 67, y al quitarlo vuelven a 66.

**Cuando el autor escribe el texto, manda el que escriba primero — y puede ser el euskera.** En
`zaldutrail` dio su versión en castellano, luego la reescribió entera en **euskera** y dijo: «el
euskera prioriza; si quieres dale el mismo tono al castellano». Así que el euskera entró tal cual
—sólo se le pusieron los `<b>` en los mismos nombres y se normalizó un guion que no se parte
(U+2011) en «erritmo-aldaketetan»— y el **castellano se rehízo detrás** para ir en paralelo: los
mismos nueve párrafos, el mismo tono. Es al revés de lo normal en esta web, donde el castellano es
la fuente y `eu.py` la traducción, pero la tabla funciona igual: la clave es el castellano y el
valor su párrafo en euskera.

Lo que no funcionó, por si vuelve a pasar: su euskera agrupaba los párrafos de otra manera (nueve
frente a once del castellano), y no hay correspondencia uno a uno. Se probó una clave única con el
bloque entero —`make_eu` sustituye cadenas literales de más larga a más corta, así que entra la
primera y vale—, pero deja un diccionario ilegible. **Lo que vale es rehacer el castellano con los
mismos cortes que el euskera** y volver a emparejar párrafo a párrafo.

Y **el título no se traduce, se escribe dos veces**: el suyo en euskera era «Zaldibarko mendietan
barrena, gogorra eta ederra», y pasarlo al castellano como «por los montes de Zaldibar, dura y
hermosa» le sonó **hortera**. El castellano volvió al que él había escrito, «una ruta exigente por
los montes de Zaldibar», y el euskera se quedó con el suyo. Las dos lenguas pueden tener títulos
distintos; lo que no puede es inventarse uno en castellano a partir del otro.

**Preguntas frecuentes (`preguntas.html`).** Tercera pagina que no es una ruta, junto a `agua` y
`aviso-legal`, y como ellas va en `PAGES` (build y make_eu), en `ROUTE_PAGES` de make_eu y en
`NO_RUTA` de `check_site.py` — esa tupla es la que dice que no lleva tarjeta en la portada, y
`preguntas` es ademas la segunda pagina sin mapa. Nueve preguntas y la guía, en `<details name="faq">` nativo:
sin una linea de JavaScript, con teclado, y el propio navegador cierra la anterior al abrir otra
(«que se cierren facil», lo pidio el autor). Si un navegador viejo no entiende `name`, lo unico que
pasa es que se pueden quedar varias abiertas. El color sale de la actividad, como en todo el sitio:
naranja las de bici (`data-tema="bici"`), verde las de andar (`data-tema="pie"`) y el color de
enlace las generales, que no es ninguna de las dos y por eso no se lee como una actividad.
**Sin JSON-LD de `FAQPage` a proposito**: desde agosto de 2023 Google solo muestra ese resultado
enriquecido a webs oficiales de sanidad y administracion, asi que seria un segundo sitio donde
mantener las mismas diez respuestas, en dos idiomas, a cambio de nada.

**La guía paso a paso de «monta tu ruta»** es **un `<details>` más de la lista**, el último, con
el mismo `name="faq"` que los demás: el autor no la quiere abierta de por vida ocupando media
página. Va pegada a «¿Puedo montarme mi propia ruta?», que es su pregunta. Son siete pasos con su
captura, del lápiz al GPX, incluido el ojo de «Rutas» para ver qué hay debajo (si por ahí pasa un
camino que no es ninguna de las 65, o si el tramo enganchado cruza campo a través).

**Las preguntas van agrupadas por tema**, no por orden de llegada: las tres de bici, luego las tres
de elegir ruta (Esfuerzo, niños, carreras), luego las dos de campo (agua, tracks) y al final las dos
de montarse la ruta. Lo pidió el autor: «las que más se parecen, juntas».

**Al abrir una pregunta, la página la pone a la vista** (el bloque del final de `src/js/app.js`).
Hace falta porque `<details name="faq">` cierra la anterior en el mismo paso y la página se encoge
de golpe: lo que acabas de tocar se va hacia arriba, a veces debajo de la cabecera pegajosa. Si la
pregunta cabe entera en la pantalla se centra; si no cabe —la guía mide 3.303 px en un móvil— se
lleva el título justo debajo de la cabecera, que es lo útil. Se esperan **dos fotogramas** antes de
medir: en el primero el navegador todavía no ha recalculado el alto de la que se cierra.

**Cada lengua tiene sus capturas.** Las de euskera son `img/guia/<paso>.eu.webp` y están hechas
sobre `index.eu.html`, porque en el mapa cambian los rótulos (**Bizi**, **Kaleak**, **Satelitea**) y
en la herramienta también. El cambio de ruta se hace con ocho claves de `img/guia/x.webp` a
`img/guia/x.eu.webp` en el diccionario `PREGUNTAS`, y **los dos juegos miden exactamente lo mismo**,
para que el `width`/`height` del marcado valga para ambos. Para rehacerlas: viewport de 390x844 y
dpr 2 (la franja del perfil, a 800 de ancho, que es la proporción de 760x79), los puntos del trazado
se meten con `window.__m.fire('click', {latlng})` y **no con el ratón** — traducir a coordenadas de
pantalla falla en cuanto la página se desplaza un poco—, y el recorte se centra en el propio
`.draw-line`. La lista de guardados se abre sola al pulsar «Gorde»: si además pulsas el botón de la
lista, la cierras.

El texto de la guía en euskera **lo escribió el autor entero**, y en el paso 6 lleva **dos viñetas**
donde el castellano tiene una frase seguida. Ojo con eso: `.guia-pasos li::before` pintaba el número
del paso también en las viñetas (salían «7» y «8»), así que el selector es **`.guia-pasos > li`**,
sólo hijos directos. Y donde él escribió «Rutas botoia» va **«Ibilbideak»**: es como se llama el
botón en la página en euskera, y además «Rutas» está en `SPANISH_TELLS` y tumbaría el build.

Las capturas están en **`img/guia/`**, en WebP de 760 px y 545 kB en total, y **no pasan por el
tren de imágenes**: `optimize_images.py` y compañía sólo miran los `.jpg` de `img/` y de `img/orig/`
con `os.listdir`, así que una subcarpeta les es invisible, y eso es justo lo que se quiere — son
pantallazos, no fotos, y reprocesarlos los estropearía. Se regeneran a mano con Playwright cuando la
herramienta cambie de aspecto. Todas van `loading="lazy"` menos la primera, y se muestran **a su
tamaño real como mucho** (`width:auto; max-width:100%`): estiradas a la columna entera se ven
borrosas.

**Dibujar un trazado propio, sobre los caminos de la web** (`src/js/trazado.js`, solo portada).
Idea del autor: casi nadie se hace de una tirada una ruta de 37 km, y lo que pide la gente es unir
dos, acortar una o montarse la suya. Dibujar a mano alzada se descartó — un garabato no va por los
caminos y su kilometraje sería mentira —, así que **se dibuja tocando puntos y el camino entre dos
toques se calcula sobre los tracks reales**.

La red se construye en el navegador con los mismos tracks que la portada ya tiene
(`data/trailhead.json`): los puntos se pegan a una rejilla de 15 m y cada celda es un nodo. Con los
datos de hoy salen **8.418 nodos y 10.796 tramos, y forman una sola componente conexa** — desde
cualquier punto de cualquier ruta se llega a cualquier otro sin salirse de terreno grabado —, así
que **no hace falta ningún servicio de rutas de fuera**, que es la regla de esta web. Antes de pegar a la rejilla **cada tramo se rellena cada 5 m**: los puntos vienen simplificados a 10 m
y dos caminos que se *cruzan* pueden caer en celdas distintas, con lo que el cruce no existe para la
red y el cálculo se va a buscar la vuelta larga. Medido sobre 120 pares de puntos a 100-600 m, el
rodeo mediano baja de 1,94 a 1,58 veces la línea recta y los rodeos de más de 3x pasan de 31 a 22.
**Los que quedan son de verdad** — entre esos dos puntos no hay camino grabado —, y por eso cuando un
tramo sale más de 2,5 veces la recta y se pasa de 300 m, el panel lo dice con los kilómetros que son.
La red pasa de 8.375 a 46.226 nodos y se construye en 0,25 s medidos en el navegador. El camino se
busca con Dijkstra sobre montículo binario; un toque tarda milisegundos.

Las alturas van aparte, en **`data/alturas.json`** (56 kB), que escribe `scripts/make_alturas.py`
cogiendo para cada punto de la portada la altura del punto más cercano del `data/<ruta>.json` de esa
misma ruta (esos sí las llevan). **Hay que volver a pasarlo después de `make_map_data.py`.** El
fichero se baja solo al abrir el modo de dibujo: el mapa de la portada no necesita alturas y no hay
por qué cobrárselas a todo el que lo abre.

Tres cosas que costaron una vuelta y conviene no volver a tropezar:

- La clase `is-drawing` va en **`[data-map-src]`**, que es el `.leaflet-container`, no en el
  `.route-map-box` de fuera. Con ella, los 65 tracks y sus marcadores pierden el `pointer-events`:
  sin eso, tocar encima de una ruta abría su ficha y el toque nunca llegaba al mapa. Y se bajan al
  30 % de opacidad para que el trazo azul se vea; el propio trazo lleva `.draw-line` y se libra.
- **Todo vive dentro del mapa, y el mapa se lleva casi la pantalla entera.** Al entrar en modo
  dibujo, `encaja()` le da a la caja el alto que queda tras la cabecera pegajosa y, en el móvil, la
  barra fija de abajo («Lista / Todas / A pie…», que el autor quiere seguir viendo), y la saca de su
  columna centrada con un margen negativo para que ocupe todo el ancho. **El ancho se toma de
  `clientWidth`, no de `100vw`**: `100vw` incluye la barra de desplazamiento y dejaría la página
  moviéndose de lado. Medido: 388x709 en un móvil de 390x844 y 1278x822 en 1280x900, sin desbordar.
  Al salir se restaura todo.
- **Un perfil pequeño en la pastilla**, en el sentido de la marcha, con una rayita en cada punto
  tocado y **el último tramo sombreado**, más su propio «+69 / −52 m» debajo del total. Lo pidió el
  autor: lo que quiere saber al enganchar un tramo es si lo coge de subida o de bajada, porque en
  bici y andando no da igual. El desnivel se suma con el mismo umbral de 5 m que el total, para no
  contar el ruido del GPS, y por eso va con un «aprox.» al lado.
- Las opciones (deshacer, borrar, guardar, GPX, guardados) van **en columna dentro del mapa, justo
  debajo del lápiz**, en la esquina de arriba a la derecha, y los totales en una pastilla pequeña
  abajo a la izquierda. Se probaron antes dos sitios que el autor descartó: un panel flotante encima
  del mapa (tapaba justo donde hay que tocar) y el mismo panel debajo del mapa, en el flujo de la
  página (con el mapa grande se iba fuera de la pantalla y había que bajar a por «Deshacer» después
  de cada toque). Mientras dura se esconden el botón flotante de «Lista» y el de «volver arriba»,
  que caen encima de la columna y de la pastilla.
- `map.js` no sabe nada de todo esto: al terminar de montar el mapa dispara un evento
  **`mapa:listo`** con el mapa, Leaflet, los datos, la caja y `cerrarPanel`. Si `trazado.js` no está
  cargado, no pasa nada.

Lo que dibuja un visitante **no es una ruta de la web**: va en otro color (`--trazo`, que no es
ninguna de las dos actividades a propósito), se llama «tu trazado», se guarda solo en su navegador
(`localStorage`, hasta 12) y nunca aparece entre las 65. Se puede deshacer tramo a tramo, borrar,
guardar, reabrir y bajar como GPX.

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

**Y debajo de los cuatro dias, el texto oficial de Euskalmet.** Lo pidio el autor: «el tiempo creo
que esta aplicacion no da una, busca otra alternativa». Se probaron las alternativas de verdad, no
leyendo sus webs:

- **Euskalmet si se puede usar, y es el hallazgo bueno.** Hay un fichero abierto **sin clave**,
  `opendata.euskadi.eus/contenidos/prevision_tiempo/met_forecast/opendata/met_forecast.xml`, que
  responde `Access-Control-Allow-Origin: *` y se actualiza a las 06:00. Trae el texto de la
  prevision **en castellano y en euskera**, escrito por quien pronostica este valle.
- **Solo se enseña el de hoy.** Entraban hoy y manana y eran dos parrafos largos debajo de cada
  ficha; el autor dijo «recorta». El de manana sigue llegando en el mismo fichero: volver a
  ponerlo es cambiar `DIAS_LOCAL` de 1 a 2 en `src/js/weather.js`.
- **Pero no sustituye a Open-Meteo**: solo da **hoy y manana**, sin probabilidad de lluvia, y sus
  temperaturas son de seis ciudades (Bilbao, Donostia, Vitoria, Pamplona, Mondragon, Laguardia),
  ninguna de por aqui. Por eso se **suma** debajo en vez de reemplazar la tira de cuatro dias.
- **Dos trampas al leerlo**: el fichero viene en **ISO-8859-1**, asi que hay que decodificarlo a
  mano (`arrayBuffer()` + `TextDecoder('iso-8859-1')`); con `response.text()` los acentos salen
  rotos. Y `pideLocal()` se llama **tambien en la rama de la cache**, que ahi habia un `return`
  temprano y si no el texto no salia al volver a una ficha.

**Lo que NO se hizo, y por que.** Se compararon ocho modelos para el mismo punto y dia y la
probabilidad de lluvia iba de **30 %** (lo que da la mezcla por defecto, que es lo que usa la web) a
**88 %** (ECMWF, MET Norway, UK Met Office). Tentaba cambiar de modelo, pero **el texto oficial de
Euskalmet para ese dia no mencionaba lluvia**, asi que el 30 % se le parecia mas que el 88 %.
Cambiar de modelo a ciegas podia empeorarlo, y no hay manera de saber cual acierta sin seguirlo
varios dias. Tampoco sirve **pasarle la altura real** a Open-Meteo: el modelo ya situa Trabakua a
430 m frente a los 412 reales, 0,1 oC de diferencia. AEMET y met.no siguen descartados por lo de
siempre (clave a la vista, cabecera que un navegador no deja poner).

Esto suma **dos terceros mas** a los que ya veian la IP de cada visitante al pintar el mapa
—geoEuskadi por las teselas y Open Data Euskadi por este texto—; esta dicho en el aviso legal, en
los dos idiomas, y al pie del propio bloque. **El aviso legal se habia quedado atras** cuando entro
la capa de geoEuskadi: nombraba solo al IGN, CyclOSM, Esri y Open-Meteo. Al anadir una capa o un
servicio hay que tocarlo, y su clave en `eu.py`.

**Y hay un iframe de Google Maps en la portada**, dentro del desplegable «Dónde aparcar»: marca el
puerto de Trabakua, las mismas coordenadas que el marcador de aparcamiento del mapa propio. Va con
`loading="lazy"`, así que sólo carga si alguien abre ese desplegable, pero cuando carga **Google
pone sus cookies**, y eso contradecía dos frases del aviso legal: la lista cerrada de servicios
externos (IGN, CyclOSM, geoEuskadi, Esri, Open-Meteo, Euskalmet) y el «esta web no usa cookies de
rastreo ni analítica de ningún tipo». Se le planteó al autor quitarlo —el mapa de la web ya marca
ese punto— y eligió dejarlo y declararlo, así que **el aviso legal lo nombra ahora en los dos
idiomas** y la frase de las cookies dice «no pone ninguna cookie propia», con Google como única
excepción. Si algún día entra otro contenido incrustado, lo mismo: mirar esas dos frases.

**Map tiles are deliberately never cached.** They come from CyclOSM and Spain's IGN —
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
  sitio equivocado, una fuente que no existe. Esto vale igual para las **alturas**: un GPS tiene
  error de hasta 15 m, así que si una cumbre aparece con 795, 791 y 783 m en tres sitios distintos,
  es el mismo monte y no hay nada que contrastar ni que avisar. No descartes una fuente por eso.
- **Los dos tracks que quedan con tramos rectos están decididos: no los vuelvas a plantear.**
  `intxorta` tiene un corte de grabación de 644 m al principio y **ninguna otra ruta recorre ese tramo
  entero**, así que cerrarlo exigiría inventarse el enlace. **El original de Wikiloc trae el mismo
  corte**: el autor lo bajó el 20-oct-2026 y lleva el salto exacto, entre (43.20953,-2.54842) y
  (43.21143,-2.55592), 644,4 m, los mismos metros y las mismas coordenadas. No es que el repositorio
  tenga una copia recortada: es que el aparato dejó de grabar ese día. No hay nada que recuperar. `longa` no tiene cortes: es una ruta
  **trazada en Wikiloc, no grabada** (81 puntos/km, sin `<time>`, cierra el círculo a 0,00 m exactos),
  y su descarga de Wikiloc es byte a byte la que ya está en `src/longa.gpx`, así que no hay original
  mejor que recuperar. Sus 52 tramos rectos son como se trazó. Déjalo estar salvo que él lo saque.
- **`garaimaguna` nombra Maguna en su título y la ruta pasa a 329 m. Está medido y NO es un error:
  no volver a sacarlo.** Se midieron los 96 lugares nombrados en los títulos de todas las rutas
  contra su propio GPX (de cada nombre repetido, el más cercano): la mediana es **16 m**, pero
  `argineta` nombra **Trabakua a 763 m**, `iturreta` y `exigente` nombran **Barinaga a 495 m**, y 16
  de 96 pasan de 150 m. Los títulos de esta web nombran los sitios por los que la ruta **pasa**, no
  sólo los que pisa, y 329 m queda dentro de lo normal. El punto numerado, que es donde el dato
  tiene que ser exacto, ya dice «Cerca de Maguna». Esto se le planteó al autor tres veces como si
  fuera un fallo antes de molestarse en medirlo.

- **Si falta `scripts/.punto-privado.json`, `check_site.py` lo dice ahora.** Esa comprobación —la
  única instrucción permanente del autor sobre los tracks— se saltaba **en silencio** cuando el
  fichero no estaba, y las 14.023 comprobaciones salían correctas sin haberla hecho ni una vez.
  Ahora imprime `AVISO:` y lo cuenta al pie. No tumba el build a propósito: sin el fichero no hay
  nada que comprobar, y en GitHub Actions tampoco va a estar.

- **Un nombre de sitio en la prosa tiene que estar donde dice el texto que pasamos, y el criterio ya
  existe: el de `make_places.py`.** Un `locality` entra si el track pasa a menos de **70 m**, un
  `hamlet` o un barrio a 200, una cima a 60. Montando la ficha de `zaldutrail` se colaron en el
  cuerpo seis topónimos de OpenStreetMap que ese mismo criterio ya había rechazado — Arkatxe a
  399 m, Zabaldiak a 335, Aginde a 244, Potzueta a 243, Aginaga a 224 y Berrenguren a 104 — y el
  autor los sacó: «¿merece la pena meter estos nombres?». No. Un caserío suelto a 300 m no lo ve
  quien va por el camino, no ayuda a orientarse y afirma algo que los datos no dan. Los nombres
  eran reales; la afirmación, no. Para los **títulos** la regla es otra y más laxa (ver
  `garaimaguna` más arriba): ahí se nombra por donde la ruta pasa, no sólo lo que pisa.

- **Que un sitio no salga en `scripts/osm/` no quiere decir que no exista: la consulta sólo baja
  PUNTOS.** El autor preguntó si el barrio del km 18,1 de `zaldutrail` podía ser **Gazaga**, y la
  copia de OSM no tenía ningún Gazaga. Lo tenía, pero como **área administrativa**, y
  `places.json`/`pois.json` sólo traen nodos. Se vio preguntándole a Nominatim por la ermita: su
  dirección completa es «Ermita de San Lorenzo de Urizar, Bizkaiko Golkoko Autobidea, **Gatzaga**,
  Zaldibar», y el mapa de Wikiloc rotula ahí mismo «Lugar Bo. Gazaga». Antes de dar un topónimo por
  inexistente, preguntar a Nominatim por la dirección completa de algo que sí esté en ese punto.

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
