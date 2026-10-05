#!/usr/bin/env python3
"""Lanza el sitio en un navegador de verdad y lo manosea.

scripts/test_ui.cjs ya ejecuta el JS contra un DOM de mentira y dice en su
primera linea que no prueba la maquetacion. Esto es lo otro: Chromium real,
CSS real, capturas de verdad.

  python3 .claude/skills/run-rutas-mallabia/driver.py <orden>

Ordenes:
  build                       make_eu + build + aviso si quedan cambios sin commitear
  check                       check_site.py + test_ui.cjs + verify_route_consistency.py
  serve                       servidor en primer plano (Ctrl-C para parar)
  shot <pagina> [opciones]    captura; --ancho 390 --tema light --sel .hero-compact
  audit [pagina]              desborde horizontal a 320/390/768/1280, en los dos temas
  probe <pagina> --sel S      color/fondo/tipografia calculados de un selector
  filtros                     flujo real de busqueda y filtros de la portada
  renombrar <slug> ...        cambia el titulo de una ruta en los nueve sitios
  temas [pagina]              el texto del heroe se lee igual en claro y oscuro\n  mapa [pagina]               comprueba que Leaflet pinta el track
  offline [pagina]            registra el service worker, corta la red y recarga
  todo                        audit + filtros + mapa + temas + offline

Las paginas se nombran como el fichero: index.html (euskera), index.es.html
(castellano), longaurjauziak.html, betzun.eu.html...
"""
import argparse, contextlib, glob, http.server, os, re, socket, subprocess, sys, threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CAPTURAS = RAIZ / ".claude" / "skills" / "run-rutas-mallabia" / "capturas"
ANCHOS = (320, 360, 390, 768, 1280)   # 360 es el ancho real de muchos moviles
# Texto que no cabe en su caja: solo cuenta donde no puede partirse en dos lineas.
JS_CORTE = "() => { const out = []; for (const e of document.querySelectorAll('.hero-compact-stats, .hero-compact h1, .hero-compact-content .eyebrow, .route-card-name')) {  if (getComputedStyle(e).whiteSpace.indexOf('nowrap') < 0) continue;  const r = document.createRange(); r.selectNodeContents(e);  const texto = Math.ceil(r.getBoundingClientRect().width);  const caja = Math.floor(e.getBoundingClientRect().width);  if (texto > caja + 1) out.push((e.className || e.tagName) + ': ' + (texto - caja) + 'px de mas'); } return out; }"


def paginas():
    """La lista de paginas del sitio, leida de src/build.py. Asi una ruta nueva
    no hace fallar las comprobaciones que cuentan tarjetas."""
    sys.path.insert(0, str(RAIZ / "src"))
    import build
    return build.PAGES


def navegador():
    """Playwright busca una version de Chromium que aqui no esta; se le da la
    que hay. Sin esto falla con 'Executable doesn't exist'."""
    for patron in ("chromium-*/chrome-linux/chrome", "chromium/chrome-linux/chrome"):
        for c in sorted(glob.glob(f"/opt/pw-browsers/{patron}")):
            if os.access(c, os.X_OK):
                return c
    return None


@contextlib.contextmanager
def servidor():
    """http.server en un hilo, en un puerto libre. El sitio se publica desde la
    raiz del repo, asi que se sirve la raiz tal cual."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); puerto = s.getsockname()[1]; s.close()
    os.chdir(RAIZ)
    clase = http.server.SimpleHTTPRequestHandler
    clase.log_message = lambda *a, **k: None
    # Al cerrar el navegador quedan descargas de fotos a medias y http.server
    # vomita un BrokenPipeError de 20 lineas por cada una. No es un fallo.
    clase.handle_error = lambda *a, **k: None
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), clase)
    httpd.handle_error = lambda *a, **k: None
    hilo = threading.Thread(target=httpd.serve_forever, daemon=True); hilo.start()
    try:
        yield f"http://127.0.0.1:{puerto}"
    finally:
        httpd.shutdown()


@contextlib.contextmanager
def pagina(base, ruta, ancho=1280, tema=None, alto=1000, escala=2):
    from playwright.sync_api import sync_playwright
    exe = navegador()
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        ctx = nav.new_context(viewport={"width": ancho, "height": alto},
                              device_scale_factor=escala, service_workers="allow")
        pg = ctx.new_page()
        # Las teselas del mapa vienen de OSM/OpenTopoMap y en este contenedor
        # mueren contra el proxy TLS. Es ruido esperado, no un fallo del sitio.
        RUIDO = ("ERR_CERT_AUTHORITY_INVALID", "ERR_NAME_NOT_RESOLVED",
                 "ERR_PROXY_CONNECTION_FAILED", "tile.openstreetmap", "opentopomap",
                 "cyclosm")
        errores = []
        anota = lambda s: errores.append(s) if not any(r in s for r in RUIDO) else None
        pg.on("pageerror", lambda e: anota(str(e)))
        pg.on("console", lambda m: anota(m.text) if m.type == "error" else None)
        pg.goto(f"{base}/{ruta}", wait_until="load")
        if tema:
            pg.evaluate("t => document.documentElement.setAttribute('data-theme', t)", tema)
        pg.wait_for_timeout(1800)          # app.js recalcula vecinas y totales pidiendo la portada
        pg.errores = errores
        try:
            yield pg
        finally:
            ctx.close(); nav.close()


def corre(*cmd, callado=False):
    """make_eu.py y build.py escriben 250 lineas. Cuando va bien sobra; cuando
    falla hay que verlo entero."""
    print("  $", " ".join(cmd))
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=callado, text=True)
    if callado and r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-2000:])
    elif callado:
        print(f"    ok, {len(r.stdout.splitlines())} lineas")
    return r.returncode


# ---------------------------------------------------------------- ordenes ---
def cmd_build(a):
    """make_eu.py no dice 'error' cuando falla: dice que una clave ya no esta en
    el castellano y sale con codigo 1. Hay que mirar el codigo, no el texto."""
    for paso in (("python3", "src/i18n/make_eu.py"), ("python3", "src/build.py")):
        if corre(*paso, callado=True) != 0:
            print(f"FALLO: {' '.join(paso)}"); return 1
    sucio = subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ,
                           capture_output=True, text=True).stdout.strip()
    print(f"\nconstruido. {len(sucio.splitlines())} fichero(s) con cambios sin commitear"
          if sucio else "\nconstruido, arbol limpio")
    return 0


def cmd_check(a):
    fallos = 0
    for paso in (("python3", "scripts/check_site.py"),
                 ("node", "scripts/test_ui.cjs"),
                 ("python3", "scripts/verify_route_consistency.py")):
        if corre(*paso) != 0:
            fallos += 1
    return 1 if fallos else 0


def cmd_serve(a):
    with servidor() as base:
        print(f"sirviendo {RAIZ} en {base}  (Ctrl-C para parar)")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            print()
    return 0


def cmd_shot(a):
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    with servidor() as base, pagina(base, a.pagina, a.ancho, a.tema) as pg:
        destino = CAPTURAS / (a.salida or
                              f"{a.pagina.replace('.html','')}-{a.ancho}-{a.tema or 'dark'}.png")
        # Locator.screenshot() no acepta full_page; solo Page lo tiene.
        if a.sel:
            pg.locator(a.sel).screenshot(path=str(destino))
        else:
            pg.screenshot(path=str(destino), full_page=bool(a.completa))
        print(f"{destino.relative_to(RAIZ)}  ({destino.stat().st_size // 1024} kB)")
        if pg.errores: print("  errores de consola:", pg.errores[:3])
    return 0


def cmd_audit(a):
    """CLAUDE.md pide revisar 320/390/768/1280 antes de dar por buena una
    maquetacion. Esto lo automatiza y de paso mira el tema claro, donde ya se
    colo una vez texto oscuro sobre foto oscura."""
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    mal = 0
    with servidor() as base:
        for ancho in ANCHOS:
            for tema in ("dark", "light"):
                with pagina(base, a.pagina, ancho, tema) as pg:
                    real = pg.evaluate("document.body.scrollWidth")
                    # El desborde de la pagina no lo ve todo: el heroe recorta por
                    # dentro (overflow:hidden), asi que una linea que no cabe se
                    # corta en silencio. Hay que medir el texto contra su caja. La
                    # linea de cifras se comia el «+» en moviles de 320-360 px y a
                    # 390 px entraba por 5 px, por eso no salia en las capturas.
                    cortados = pg.evaluate(JS_CORTE)
                    ok = real <= ancho and not cortados
                    mal += 0 if ok else 1
                    err = f"  JS: {pg.errores[0][:60]}" if pg.errores else ""
                    if cortados:
                        err += "  TEXTO CORTADO: " + "; ".join(cortados)
                    print(f"  {ancho:>5}px {tema:<5}  scrollWidth {real:<5} "
                          f"{'ok' if ok else 'MAL'}{err}")
                    pg.screenshot(path=str(CAPTURAS / f"audit-{a.pagina.replace('.html','')}"
                                                      f"-{ancho}-{tema}.png"))
    print(f"\n{'todo dentro del ancho' if not mal else f'{mal} desbordes'}"
          f" — capturas en {CAPTURAS.relative_to(RAIZ)}/")
    return 1 if mal else 0


def cmd_probe(a):
    with servidor() as base, pagina(base, a.pagina, a.ancho, a.tema) as pg:
        datos = pg.evaluate("""s => {
            const e = document.querySelector(s);
            if (!e) return null;
            const c = getComputedStyle(e), r = e.getBoundingClientRect();
            return {texto: (e.textContent||'').trim().slice(0,60), color: c.color,
                    fondo: c.backgroundColor, tipo: c.fontFamily.split(',')[0],
                    tam: c.fontSize, sombra: c.textShadow.slice(0,70),
                    caja: `${Math.round(r.width)}x${Math.round(r.height)}`};
        }""", a.sel)
        if not datos:
            print(f"no existe {a.sel} en {a.pagina}"); return 1
        for k, v in datos.items(): print(f"  {k:<7} {v}")
    return 0


def cmd_filtros(a):
    """El flujo real de la portada: escribir en el buscador y pulsar los chips.
    filters.js ignora tildes, mayusculas y guiones y exige todas las palabras."""
    with servidor() as base, pagina(base, "index.es.html", 1280) as pg:
        visibles = lambda: pg.evaluate(
            "() => [...document.querySelectorAll('a.route-card')]"
            ".filter(c => c.offsetParent !== null).length")
        # cuantas rutas hay se saca de build.py, no de un numero a mano: cada
        # ruta nueva hacia fallar esta comprobacion sin que nada estuviera mal.
        esperadas = len([p for p in paginas() if p not in ("mallabia", "aviso-legal")])
        total = visibles(); print(f"  sin filtrar            {total} tarjetas")
        assert total == esperadas, f"se esperaban {esperadas}, hay {total}"

        pg.fill(".route-search input", "cascada")
        pg.wait_for_timeout(600)
        con_busqueda = visibles(); print(f"  buscando 'cascada'     {con_busqueda}")
        assert 0 < con_busqueda < total, "la busqueda no filtro nada"

        pg.fill(".route-search input", "")
        pg.wait_for_timeout(400)
        pg.click('.activity-chip[data-activity="bici"]')
        pg.wait_for_timeout(600)
        bici = visibles(); print(f"  solo e-bike            {bici}")
        assert 0 < bici < total, "el chip de bici no filtro"

        pg.click('.activity-chip[data-activity="all"]')
        pg.wait_for_timeout(600)
        vuelta = visibles(); print(f"  de vuelta a todas      {vuelta}")
        assert vuelta == total, f"no volvio a {total}"
    print("\nbusqueda y filtros, correctos")
    return 0


def cmd_mapa(a):
    """Leaflet se sirve desde vendor/leaflet, sin CDN. Las teselas vienen de
    fuera y en este contenedor no cargan: lo que se comprueba es que el mapa se
    monta y pinta el track, no el fondo."""
    with servidor() as base, pagina(base, a.pagina, 1280, alto=1400) as pg:
        pg.wait_for_timeout(2500)
        d = pg.evaluate("""() => {
            const m = document.querySelector('.leaflet-container');
            return {montado: !!m,
                    trazos: document.querySelectorAll('.leaflet-overlay-pane path').length,
                    marcas: document.querySelectorAll('.leaflet-marker-icon').length};
        }""")
        print(f"  contenedor Leaflet   {d['montado']}")
        print(f"  trazos del track     {d['trazos']}")
        print(f"  marcadores           {d['marcas']}")
        if pg.errores: print("  errores de consola:", pg.errores[:2])
        if not d["montado"] or d["trazos"] == 0:
            print("\nel mapa no se pinto"); return 1
    print("\nmapa correcto")
    return 0


def cmd_offline(a):
    """El sitio se abre en el monte sin cobertura: sw.js guarda cada pagina
    visitada. Se visita, se corta la red y se recarga."""
    from playwright.sync_api import sync_playwright
    with servidor() as base:
        with sync_playwright() as p:
            nav = p.chromium.launch(executable_path=navegador(), args=["--no-sandbox"])
            ctx = nav.new_context(viewport={"width": 390, "height": 900},
                                  service_workers="allow")
            pg = ctx.new_page()
            # La primera carga instala el SW pero NO pasa por el: esa visita no
            # se cachea. Hace falta una segunda carga, ya controlada, para que
            # la pagina entre en cache. Sin esto el offline sirve offline.html.
            pg.goto(f"{base}/{a.pagina}", wait_until="load")
            pg.wait_for_function("() => navigator.serviceWorker.controller !== null "
                                 "|| performance.now() > 8000", timeout=12000)
            pg.reload(wait_until="load")
            pg.wait_for_timeout(2500)
            estado = pg.evaluate("""async () => {
                const r = await navigator.serviceWorker.getRegistration();
                return (r && r.active ? 'activo' : 'sin activar')
                       + (navigator.serviceWorker.controller ? ', controla la pagina' : ', NO controla');
            }""")
            print(f"  service worker        {estado}")
            ctx.set_offline(True)
            try:
                pg.reload(wait_until="load", timeout=15000)
                titulo = pg.title()
                tarjetas = pg.evaluate("document.querySelectorAll('a.route-card, .facts').length")
                print(f"  sin red, recargada    «{titulo[:48]}»")
                print(f"  contenido servido     {tarjetas} bloque(s)")
                ok = bool(titulo) and tarjetas > 0
            except Exception as e:
                print(f"  sin red, recargada    FALLO: {str(e)[:70]}"); ok = False
            finally:
                ctx.set_offline(False); ctx.close(); nav.close()
    print("\nmodo offline correcto" if ok else "\nel modo offline no sirvio la pagina")
    return 0 if ok else 1


def cmd_temas(a):
    """Sobre la foto del heroe el texto va en blanco siempre: la foto es oscura
    en los dos temas. Usar tokens (--ink, --violet, --teal) hace que en claro
    salga tinta oscura sobre foto oscura. Ya paso una vez."""
    SELECTORES = (".hero-compact-content .eyebrow", ".hero-compact h1",
                  ".hero-compact h1 em .pie", ".hero-compact h1 em .bici",
                  ".hero-compact-lead", ".hero-compact-stats")
    with servidor() as base:
        colores = {}
        for tema in ("dark", "light"):
            with pagina(base, a.pagina, 1280, tema) as pg:
                colores[tema] = pg.evaluate(
                    """ss => ss.map(s => {const e=document.querySelector(s);
                       return e ? getComputedStyle(e).color : 'NO EXISTE';})""", list(SELECTORES))
    mal = 0
    for sel, osc, cla in zip(SELECTORES, colores["dark"], colores["light"]):
        igual = osc == cla
        mal += 0 if igual else 1
        print(f"  {'ok ' if igual else 'MAL'} {sel:<34} {osc}" + ("" if igual else f"  ->  {cla}"))
    print(f"\n{'el heroe se lee igual en los dos temas' if not mal else f'{mal} color(es) cambian con el tema sobre la foto'}")
    return 1 if mal else 0


def _lee_actuales(slug):
    """Lee de los ficheros lo que la ruta se llama AHORA. No se supone nada: el
    titulo plano sale de la tarjeta de la portada, el h1 de la propia ficha y el
    nombre de descarga de su atributo, que en 8 rutas es mas corto a proposito."""
    a = {}
    home = (RAIZ / "src/mallabia_tail.html").read_text(encoding="utf-8")
    m = re.search(rf'<a class="route-card" href="{slug}\.html".*?'
                  rf'<h3 class="route-card-name">(.*?)</h3>', home, re.S)
    if not m:
        raise SystemExit(f"{slug}: no tiene tarjeta en src/mallabia_tail.html")
    a["es_plano"] = " ".join(m.group(1).split())

    tail = (RAIZ / f"src/{slug}_tail.html").read_text(encoding="utf-8")
    m = re.search(r"<h1>(.*?)<br><em>(.*?)</em></h1>", tail, re.S)
    if not m:
        raise SystemExit(f"{slug}: su <h1> no tiene la forma linea1<br><em>linea2</em>")
    a["es_h1"] = (m.group(1).strip(), m.group(2).strip())
    m = re.search(r'download="([^"]+)\.gpx"', tail)
    a["descarga"] = m.group(1) if m else None

    eu_home = (RAIZ / "src/mallabia_tail.eu.html").read_text(encoding="utf-8")
    m = re.search(rf'<a class="route-card" href="{slug}\.eu\.html".*?'
                  rf'<h3 class="route-card-name">(.*?)</h3>', eu_home, re.S)
    a["eu_plano"] = " ".join(m.group(1).split()) if m else None
    eu_tail = (RAIZ / f"src/{slug}_tail.eu.html").read_text(encoding="utf-8")
    m = re.search(r"<h1>(.*?)<br><em>(.*?)</em></h1>", eu_tail, re.S)
    a["eu_h1"] = (m.group(1).strip(), m.group(2).strip()) if m else None
    m = re.search(r'download="([^"]+)\.gpx"', eu_tail)
    a["eu_descarga"] = m.group(1) if m else None
    return a


def cmd_renombrar(a):
    """Renombrar una ruta toca nueve sitios y se me escapo uno las tres veces
    que lo hice a mano. Aqui van todos, contados, y por defecto sin escribir."""
    v = _lee_actuales(a.slug)
    n_es_h1 = tuple(x.strip() for x in a.es_h1.split("|"))
    n_eu_h1 = tuple(x.strip() for x in a.eu_h1.split("|"))
    if len(n_es_h1) != 2 or len(n_eu_h1) != 2:
        raise SystemExit("--es-h1 y --eu-h1 se escriben 'primera linea|segunda linea'")

    print(f"  ahora      ES  {v['es_plano']}")
    print(f"             EU  {v['eu_plano']}")
    print(f"  pasaria a  ES  {a.es}")
    print(f"             EU  {a.eu}")
    print("")

    h1 = lambda par: f"<h1>{par[0]}<br><em>{par[1]}</em></h1>"
    cambios = []

    def anota(rel, viejo, nuevo):
        if viejo and nuevo and viejo != nuevo:
            cambios.append((rel, viejo, nuevo))

    anota(f"src/{a.slug}_tail.html", h1(v["es_h1"]), h1(n_es_h1))
    anota("src/i18n/eu.py", h1(v["es_h1"]), h1(n_es_h1))
    if v["eu_h1"]:
        anota("src/i18n/eu.py", h1(v["eu_h1"]), h1(n_eu_h1))
    # El titulo plano esta en el <title>, el og:title, los DOS bloques JSON-LD,
    # el alt de la foto ampliada, la tarjeta de la portada y las claves de eu.py.
    for rel in (f"src/{a.slug}_tail.html", f"src/{a.slug}_head.html",
                "src/mallabia_tail.html", "src/i18n/eu.py"):
        anota(rel, v["es_plano"], a.es)
    anota("src/i18n/eu.py", v["eu_plano"], a.eu)

    if v["descarga"] == v["es_plano"]:
        for ext in ("gpx", "kml"):
            for rel in (f"src/{a.slug}_tail.html", "src/i18n/eu.py"):
                anota(rel, f'download="{v["descarga"]}.{ext}"', f'download="{a.es}.{ext}"')
        if v["eu_descarga"] and v["eu_descarga"] == v["eu_plano"]:
            for ext in ("gpx", "kml"):
                anota("src/i18n/eu.py", f'download="{v["eu_descarga"]}.{ext}"',
                      f'download="{a.eu}.{ext}"')
    else:
        print(f"  (la descarga se llama «{v['descarga']}», distinto del titulo: se deja)")
        print("")

    # Enlaces entrantes que usan el titulo ENTERO. Los que usan el nombre corto
    # («Oiz», «Gerea») son 221 en el sitio y se quedan como estan, a proposito.
    for f in sorted(glob.glob(str(RAIZ / "src/*_tail.html"))):
        if f.endswith(".eu.html"):
            continue
        anota(os.path.relpath(f, RAIZ),
              f'<a href="{a.slug}.html">{v["es_plano"]}</a>',
              f'<a href="{a.slug}.html">{a.es}</a>')

    total, tocados = 0, set()
    for rel, viejo, nuevo in cambios:
        c = (RAIZ / rel).read_text(encoding="utf-8").count(viejo)
        if c:
            total += c; tocados.add(rel)
            print(f"  {c:>3}x  {rel:<34} {viejo[:62]}")
    if not total:
        print("  nada que cambiar"); return 1
    print("")
    print(f"  {total} sustitucion(es) en {len(tocados)} fichero(s)")

    if not a.aplica:
        print("")
        print("  simulacro. Repite con --aplica para escribirlo.")
        return 0

    for rel, viejo, nuevo in cambios:
        p = RAIZ / rel
        t = p.read_text(encoding="utf-8")
        if viejo in t:
            p.write_text(t.replace(viejo, nuevo), encoding="utf-8")
    print("")
    print("  escrito. Reconstruyendo:")
    for paso in (("python3", "src/i18n/make_eu.py"), ("python3", "src/build.py"),
                 ("python3", "scripts/bundle_gpx.py")):   # el ZIP nombra sus entradas con las tarjetas
        if corre(*paso, callado=True) != 0:
            return 1
    return corre("python3", "scripts/check_site.py")


def cmd_todo(a):
    fallos = 0
    for nombre, fn, arg in (("audit", cmd_audit, argparse.Namespace(pagina="index.es.html")),
                            ("filtros", cmd_filtros, a),
                            ("mapa", cmd_mapa, argparse.Namespace(pagina="longaurjauziak.html")),
                            ("temas", cmd_temas, argparse.Namespace(pagina="index.es.html")),
                            ("offline", cmd_offline, argparse.Namespace(pagina="index.es.html"))):
        print(f"\n=== {nombre}")
        fallos += 1 if fn(arg) else 0
    print(f"\n{'TODO CORRECTO' if not fallos else f'{fallos} comprobacion(es) fallidas'}")
    return 1 if fallos else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("serve").set_defaults(fn=cmd_serve)
    sub.add_parser("filtros").set_defaults(fn=cmd_filtros)
    sub.add_parser("todo").set_defaults(fn=cmd_todo)

    s = sub.add_parser("shot"); s.set_defaults(fn=cmd_shot)
    s.add_argument("pagina"); s.add_argument("--ancho", type=int, default=1280)
    s.add_argument("--tema", choices=("light", "dark")); s.add_argument("--sel")
    s.add_argument("--salida"); s.add_argument("--completa", action="store_true")

    s = sub.add_parser("audit"); s.set_defaults(fn=cmd_audit)
    s.add_argument("pagina", nargs="?", default="index.es.html")

    s = sub.add_parser("probe"); s.set_defaults(fn=cmd_probe)
    s.add_argument("pagina"); s.add_argument("--sel", required=True)
    s.add_argument("--ancho", type=int, default=1280)
    s.add_argument("--tema", choices=("light", "dark"))

    s = sub.add_parser("renombrar"); s.set_defaults(fn=cmd_renombrar)
    s.add_argument("slug")
    s.add_argument("--es", required=True, help="titulo plano en castellano")
    s.add_argument("--es-h1", required=True, help="'primera linea|segunda linea'")
    s.add_argument("--eu", required=True, help="titulo plano en euskera")
    s.add_argument("--eu-h1", required=True, help="'lehen lerroa|bigarren lerroa'")
    s.add_argument("--aplica", action="store_true", help="sin esto solo simula")

    s = sub.add_parser("temas"); s.set_defaults(fn=cmd_temas)
    s.add_argument("pagina", nargs="?", default="index.es.html")

    s = sub.add_parser("mapa"); s.set_defaults(fn=cmd_mapa)
    s.add_argument("pagina", nargs="?", default="longaurjauziak.html")

    s = sub.add_parser("offline"); s.set_defaults(fn=cmd_offline)
    s.add_argument("pagina", nargs="?", default="index.es.html")

    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
