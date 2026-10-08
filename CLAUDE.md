# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
`<link rel=stylesheet|preconnect|preload>` ever points off-site again. The only thing still fetched from
outside are the map tiles, and those are requested by the JS, not the HTML.

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

- `add_ultima_entrada` pone en la portada, debajo de los totales, **la última ruta publicada y su
  fecha** (`ULTIMA_ENTRADA`, que **se cambia a mano al publicar una ruta nueva**). Es la única fecha
  de todo el sitio. Antes se puso una fecha de revisión **en cada ficha**, sacada de la hora del
  track, y el autor la quitó el mismo día: no quiere 57 fechas, quiere saber cuál es la última
  entrada. No volver a ponerla por ruta.
- `add_tecnica` pone la **dificultad técnica** junto a la física, leyendo `TECNICA`, **que está vacío
  a propósito**: la física sale de la distancia y el desnivel, que son datos, pero la técnica depende
  de lo pedregoso, estrecho, expuesto o embarrado que esté un sendero y eso solo lo sabe quien lo ha
  pisado. La pone el autor ruta por ruta; sin valor, el dato no aparece. El antiguo «Dificultad» pasó
  a llamarse **«Dificultad física»** en las 57 fichas, en la nota y en el JSON-LD.
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

**Map tiles are deliberately never cached.** They come from OpenStreetMap, CyclOSM and Spain's IGN —
volunteer-run servers whose usage policy forbids bulk caching. Without signal the track is drawn on an
empty background, not on the map.

A **Waymarked Trails overlay** (the waymarked PR/GR/SL trails on top of the chosen base map) was
built and published on 7 October 2026 and **removed the same day at the user's request** — don't
re-add it. What it left behind is `.map-extras`, the second pill below `.map-layers`, which now holds
only the slope toggle: it is attached to the map lazily (`ponExtra`), so a page with nothing to put
in it — the home overview — gets no empty pill at all. The base layers stay mutually exclusive in
`.map-layers`; `.map-layer-btn` appears in both bars, so any selector counting them must be scoped
(`scripts/test_ui.cjs` does).

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

**A GPX must never start or end at the user's house — always at Trabakua (the pass) or thereabouts.**
He has asked for this explicitly, for every route, standing instruction. A track recorded from home
starts/ends however far his house is from Trabakua's shared reference point (`43.210466, -2.5460838`,
the same one in every route's `marker.at`). **Do not judge this by raw distance from that point.**
Measured over the 56 published routes, 27 of them start more than 200 m away and `ahuntzen` starts
9.5 km away — they simply begin at a different trailhead, so "far from Trabakua" flags half the site
as suspect. The reliable signal is isolation from the trail network: every published route's
first/last point sits within **88 m** of some point on another route's own track (`src/*.gpx`), and
most within 11 m. A real trailhead or junction is shared trail; a private approach from home is not.
So the test is: measure the new track's first/last point against every other route's track, and if
the nearest one is well beyond ~90 m, treat it as a track recorded from home. Then don't publish it
as-is and don't ask him for his address either — check first whether an
already-published route's own GPX (`src/<other-route>.gpx`) happens to pass close to the new track's
actual start/end (a shared road several routes use to leave Trabakua often does); if so, splice in the
real segment of that other GPX between Trabakua and the join point, and trim any leftover tail that
drifts back out toward the house after the loop returns near Trabakua. Recompute distance, elevation
gain/loss, min/max altitude, the elevation-profile SVG and every waypoint's km from the resulting
track — all of it shifts with a new start point. This is exactly what `sancristobaloiz` needed: its
own recording started 544 m from Trabakua and diverged from there, but `zengotitagane.gpx`'s track
passed 28 m from that same start point, so the real 476 m stretch between them (in effect, the N-633
from Trabakua to Zengotita) was spliced in — no coordinate in the published GPX/KML/map JSON was
invented.

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
