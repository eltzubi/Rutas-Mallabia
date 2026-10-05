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
  temas [pagina]              el texto del heroe se lee igual en claro y oscuro\n  mapa [pagina]               comprueba que Leaflet pinta el track
  offline [pagina]            registra el service worker, corta la red y recarga
  todo                        audit + filtros + mapa + temas + offline

Las paginas se nombran como el fichero: index.html (euskera), index.es.html
(castellano), longaurjauziak.html, betzun.eu.html...
"""
import argparse, contextlib, glob, http.server, os, socket, subprocess, sys, threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CAPTURAS = RAIZ / ".claude" / "skills" / "run-rutas-mallabia" / "capturas"
ANCHOS = (320, 390, 768, 1280)


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
                    ok = real <= ancho
                    mal += 0 if ok else 1
                    err = f"  JS: {pg.errores[0][:60]}" if pg.errores else ""
                    print(f"  {ancho:>5}px {tema:<5}  scrollWidth {real:<5} "
                          f"{'ok' if ok else 'DESBORDA'}{err}")
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
        total = visibles(); print(f"  sin filtrar            {total} tarjetas")
        assert total == 56, f"se esperaban 56, hay {total}"

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
