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
        esperadas = len([p for p in paginas()
                         if p not in ("mallabia", "agua", "aviso-legal")])
        total = visibles(); print(f"  sin filtrar            {total} tarjetas")
        assert total == esperadas, f"se esperaban {esperadas}, hay {total}"

        # El buscador ya no es una caja fija: es la lupa de la cabecera, y
        # hay que abrirla antes de poder escribir.
        pg.click("#openSearch")
        pg.wait_for_timeout(350)
        assert pg.eval_on_selector("#searchBar", "n => n.classList.contains('is-open')"), \
            "la lupa no abrio el buscador"
        pg.fill("#routeSearch", "cascada")
        pg.wait_for_timeout(600)
        con_busqueda = visibles(); print(f"  buscando 'cascada'     {con_busqueda}")
        assert 0 < con_busqueda < total, "la busqueda no filtro nada"

        # Y la X tiene que devolver el listado entero, no solo cerrar la tira.
        pg.click("#closeSearch")
        pg.wait_for_timeout(500)
        assert not pg.eval_on_selector("#searchBar", "n => n.classList.contains('is-open')"), \
            "la X no cerro el buscador"
        tras_cerrar = visibles(); print(f"  tras cerrar la lupa    {tras_cerrar}")
        assert tras_cerrar == total, "al cerrar el buscador no volvieron todas"

        pg.click('.activity-chip[data-activity="bici"]')
        pg.wait_for_timeout(600)
        bici = visibles(); print(f"  solo e-bike            {bici}")
        assert 0 < bici < total, "el chip de bici no filtro"

        pg.click('.activity-chip[data-activity="all"]')
        pg.wait_for_timeout(600)
        vuelta = visibles(); print(f"  de vuelta a todas      {vuelta}")

        # La barra del movil se aparta al bajar y vuelve al subir. Se estrecha
        # la ventana en vez de abrir otra pagina: Playwright no deja anidar
        # dos sesiones sincronas.
        pg.set_viewport_size({"width": 390, "height": 844})
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(400)
        apartada = lambda: pg.eval_on_selector(
            ".finder-toolbar", "n => n.classList.contains('se-aparta')")
        assert not apartada(), "arriba del todo no deberia estar apartada"
        pg.mouse.wheel(0, 900); pg.wait_for_timeout(250)
        assert apartada(), "al bajar no se aparto"
        pg.wait_for_timeout(900)
        assert not apartada(), "parada la pagina, tiene que volver sola"
        pg.mouse.wheel(0, 600); pg.wait_for_timeout(250)
        assert apartada(), "al bajar otra vez no se aparto"
        pg.mouse.wheel(0, -200); pg.wait_for_timeout(300)
        assert not apartada(), "al subir no volvio"
        pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        pg.wait_for_timeout(600)
        assert not apartada(), "al final de la pagina tiene que verse"
        print("  barra del movil        se aparta al bajar; vuelve al parar y al subir")
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
    """El titular ya no va sobre la foto, sino sobre el fondo de la pagina.

    Antes esta comprobacion exigia que los seis colores del heroe fueran
    identicos en los dos temas: la foto es oscura siempre, asi que una tinta
    de tema (--ink, --violet, --teal) desaparecia en claro. Al sacar el texto
    de la foto esa regla deja de valer -- ahora los colores DEBEN cambiar con
    el tema -- y lo que hay que vigilar es otra cosa: que cada linea tenga
    contraste suficiente contra el fondo real que tiene detras, en los dos
    temas. Se mide como manda la WCAG: 4.5:1 para el texto normal y 3:1 para
    el grande (el h1 y las cifras, que pasan de 24 px)."""
    GRANDE = (".hero-compact h1", ".hero-compact h1 em .pie",
              ".hero-compact h1 em .bici", ".hero-compact-stats")
    SELECTORES = (".hero-compact-content .eyebrow", ".hero-compact h1",
                  ".hero-compact h1 em .pie", ".hero-compact h1 em .bici",
                  ".hero-compact-lead", ".hero-compact-stats")
    JS = """ss => {
      const rgb = s => (s.match(/[\\d.]+/g) || []).slice(0,3).map(Number);
      const opaco = e => {           // el primer fondo que no sea transparente
        for (let n = e; n; n = n.parentElement) {
          const c = getComputedStyle(n).backgroundColor;
          const a = (c.match(/[\\d.]+/g) || [])[3];
          if (c && c !== 'transparent' && a !== '0') return c;
        }
        return getComputedStyle(document.body).backgroundColor;
      };
      return ss.map(s => { const e = document.querySelector(s);
        return e ? [getComputedStyle(e).color, opaco(e)] : null; });
    }"""

    def canal(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    def luz(c):
        r, g, b = [canal(x) for x in c]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def contraste(txt, fondo):
        a, b = luz(txt), luz(fondo)
        if a < b: a, b = b, a
        return (a + 0.05) / (b + 0.05)

    def numeros(css):
        return [float(x) for x in re.findall(r"[\d.]+", css)[:3]]

    with servidor() as base:
        lecturas = {}
        for tema in ("dark", "light"):
            with pagina(base, a.pagina, 1280, tema) as pg:
                lecturas[tema] = pg.evaluate(JS, list(SELECTORES))
    mal = 0
    for tema in ("dark", "light"):
        print(f"  tema {tema}")
        for sel, par in zip(SELECTORES, lecturas[tema]):
            if par is None:
                print(f"    --  {sel:<32} no existe en la pagina"); continue
            minimo = 3.0 if sel in GRANDE else 4.5
            r = contraste(numeros(par[0]), numeros(par[1]))
            bien = r >= minimo
            mal += 0 if bien else 1
            print(f"    {'ok ' if bien else 'MAL'} {sel:<32} {r:4.1f}:1 "
                  f"(min {minimo}) {par[0]} sobre {par[1]}")
    print("\n" + ("el heroe tiene contraste de sobra en los dos temas" if not mal
                  else f"{mal} linea(s) del heroe sin contraste suficiente"))
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


def cmd_mio(a):
    """El panel «Lo mio»: que liste las favoritas con su nombre de verdad.

    Lo que se comprueba es lo que fallaba al montarlo: el panel se inyecta al
    final de la pagina y, si cae detras de los <script>, app.js corre con el
    dialogo todavia sin existir y el boton no se engancha a nada. Aqui se
    guardan dos favoritas a mano, se abre y se exige que salgan sus nombres,
    que es lo que prueba que data/rutas.json ha llegado y se ha leido.
    """
    with servidor() as base:
        for pag, idioma in (("index.es.html", "es"), ("trabakua.html", "es"),
                            ("index.html", "eu")):
            with pagina(base, pag, ancho=390, alto=844) as pg:
                pg.evaluate("localStorage.setItem('trabakutik_favs',"
                            " JSON.stringify(['oiz','urko']))")
                pg.evaluate("localStorage.setItem('trabakutik_vistas',"
                            " JSON.stringify(['gerea','arteta']))")
                pg.reload(wait_until="load"); pg.wait_for_timeout(1400)
                assert not pg.eval_on_selector("#mioAbrir", "n => n.hidden"), \
                    f"{pag}: el boton de «Lo mio» sigue oculto"
                pg.click("#mioAbrir"); pg.wait_for_timeout(900)
                datos = pg.evaluate("""() => ({
                    abierto: document.getElementById('mioDialog').open,
                    favs: [...document.querySelectorAll('#mioFavs .mio-nombre')]
                            .map(n => n.textContent),
                    cuenta: document.getElementById('mioCuenta').textContent,
                    guardar: !document.getElementById('mioGuardar').hidden })""")
                assert datos["abierto"], f"{pag}: el panel no se abrio"
                assert len(datos["favs"]) == 2, f"{pag}: {datos['favs']}"
                assert all(datos["favs"]), f"{pag}: alguna favorita sin nombre"
                assert datos["cuenta"] == "2", f"{pag}: la insignia dice {datos['cuenta']}"
                assert datos["guardar"], f"{pag}: no sale «guardar para el monte»"
                # Borrar: las vistas de un toque, las favoritas de dos. Y los
                # corazones de la portada tienen que apagarse solos, que el
                # cambio les llega de otro sitio.
                pg.click("#mioBorrar"); pg.wait_for_timeout(300)
                pg.click("#mioBorrarFavs"); pg.wait_for_timeout(250)
                pedido = pg.eval_on_selector("#mioBorrarFavs", "n => n.textContent")
                assert pedido in ("\u00bfSeguro?", "Ziur?"), \
                    f"{pag}: el primer toque no pide confirmacion ({pedido})"
                assert pg.evaluate("() => JSON.parse(localStorage.getItem"
                                   "('trabakutik_favs')||'[]').length") == 2, \
                    f"{pag}: el primer toque ya borro las favoritas"
                pg.click("#mioBorrarFavs"); pg.wait_for_timeout(400)
                tras = pg.evaluate("""() => ({
                    favs: JSON.parse(localStorage.getItem('trabakutik_favs')||'[]').length,
                    vistas: JSON.parse(localStorage.getItem('trabakutik_vistas')||'[]').length,
                    li: document.querySelectorAll('#mioFavs li').length,
                    corazones: document.querySelectorAll('.fav-heart.is-fav').length,
                    botones: document.getElementById('mioBorrarFavs').hidden
                             && document.getElementById('mioBorrar').hidden })""")
                assert tras["favs"] == 0 and tras["li"] == 0, f"{pag}: {tras}"
                assert tras["vistas"] == 0, f"{pag}: quedan vistas: {tras}"
                assert tras["corazones"] == 0, \
                    f"{pag}: {tras['corazones']} corazon(es) siguen encendidos"
                assert tras["botones"], f"{pag}: los «Borrar» siguen a la vista"
                pg.click("#mioCerrar"); pg.wait_for_timeout(400)
                assert not pg.eval_on_selector("#mioDialog", "n => n.open"), \
                    f"{pag}: no se cerro"
                print(f"  {pag:16} [{idioma}] {len(datos['favs'])} favoritas: "
                      f"{datos['favs'][0][:34]}… y se borran")
                if pg.errores:
                    print("   errores:", pg.errores[:2]); return 1
    print("\n«Lo mio», correcto")
    return 0


def cmd_visor(a):
    """La foto ampliada: pasar de una a otra y salir tocando fuera.

    Lo que se vigila es lo que fallo al montarlo: que un arrastre corto no
    cambie de foto sin querer, y que el gesto de pasar no acabe cerrando la
    foto -- un pase termina con un click sintetico que caia en el fondo.
    """
    gesto = """([a,b]) => {
      const el=document.getElementById('lightbox');
      const t=(tipo,x,fin)=>el.dispatchEvent(new TouchEvent(tipo,{bubbles:true,cancelable:true,
        touches: fin?[]:[new Touch({identifier:1,target:el,clientX:x,clientY:400})],
        changedTouches:[new Touch({identifier:1,target:el,clientX:x,clientY:400})]}));
      t('touchstart',a,false); t('touchmove',(a+b)/2,false); t('touchend',b,true);
    }"""
    estado = """() => ({abierta: document.getElementById('lightbox').classList.contains('open'),
        foto: (document.getElementById('lightboxImg').src||'').split('/').pop(),
        cuenta: (document.querySelector('.lightbox-cuenta')||{}).textContent||''})"""
    with servidor() as base:
        with pagina(base, "trabakua.html", ancho=390, alto=844) as pg:
            pg.eval_on_selector_all("[data-lightbox-src]", "n => n[0].click()")
            pg.wait_for_timeout(800)
            e = pg.evaluate(estado)
            assert e["abierta"] and e["cuenta"].startswith("1 "), e
            total = e["cuenta"].split("/")[-1].strip()
            print(f"  abre la 1 de {total}")
            primera = e["foto"]
            pg.evaluate(gesto, [300, 120]); pg.wait_for_timeout(600)
            e = pg.evaluate(estado)
            assert e["abierta"], "el gesto de pasar cerro la foto"
            assert e["foto"] != primera, "el dedo no paso de foto"
            print(f"  con el dedo pasa a la {e['cuenta']}")
            pg.evaluate(gesto, [120, 300]); pg.wait_for_timeout(600)
            e = pg.evaluate(estado)
            assert e["abierta"] and e["foto"] == primera, "al volver no quedo la primera"
            pg.evaluate(gesto, [300, 280]); pg.wait_for_timeout(500)
            e = pg.evaluate(estado)
            assert e["abierta"] and e["foto"] == primera, "un arrastre corto cambio de foto"
            print("  un arrastre corto no cambia de foto")
            pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(500)
            assert pg.evaluate(estado)["foto"] != primera, "la flecha del teclado no paso"
            pg.evaluate("document.getElementById('lightbox').click()"); pg.wait_for_timeout(500)
            assert not pg.evaluate(estado)["abierta"], "tocando fuera no cerro"
            print("  tocando fuera, cierra")
            if pg.errores:
                print("   errores:", pg.errores[:2]); return 1
    print("\nvisor de fotos, correcto")
    return 0


def cmd_aviso(a):
    """El aviso «Leelo antes de salir»: al cerrarlo, la portada vuelve donde estaba.

    Lo que fallaba: el aviso se lee de arriba abajo y se cierra con su propio
    boton, que esta al final del texto, asi que al cerrarlo te quedabas a
    media pagina, en mitad del listado, mirando una tarjeta cualquiera. El
    boton intentaba subir a la cabecera del <details>, pero con la insignia
    puesta esa cabecera lleva display:none y scrollIntoView sobre algo oculto
    no hace nada.
    """
    ABIERTO = "() => document.querySelector('#beforeYouGo details').open"
    Y = "() => Math.round(window.scrollY)"
    with servidor() as base:
        for pag in ("index.es.html", "index.html"):
            with pagina(base, pag, ancho=390, alto=844) as pg:
                pg.wait_for_timeout(700)
                for desde, por_el_boton in ((0, True), (240, True), (0, False)):
                    pg.evaluate(f"window.scrollTo(0,{desde})"); pg.wait_for_timeout(350)
                    antes = pg.evaluate(Y)
                    pg.click(".aviso-boton"); pg.wait_for_timeout(1300)
                    assert pg.evaluate(ABIERTO), f"{pag}: el aviso no se abrio"
                    if por_el_boton:
                        pg.evaluate("() => document.querySelector('.notice-close')"
                                    ".scrollIntoView({block:'center'})")
                        pg.wait_for_timeout(300)
                        bajo = pg.evaluate(Y)
                        assert bajo > antes + 300, \
                            f"{pag}: leyendo el aviso no se ha bajado ({bajo})"
                        pg.click(".notice-close")
                    else:
                        pg.click(".aviso-boton")
                    pg.wait_for_timeout(1600)
                    assert not pg.evaluate(ABIERTO), f"{pag}: el aviso no se cerro"
                    fin = pg.evaluate(Y)
                    assert abs(fin - antes) <= 2, \
                        f"{pag}: al cerrar se queda en {fin} y abrio desde {antes}"
                    print(f"  {pag:15} desde {antes:4} -> {'leido abajo' if por_el_boton else 'cerrado con la insignia':24}"
                          f" -> vuelve a {fin}")
                if pg.errores:
                    print("   errores:", pg.errores[:2]); return 1
    print("\nel aviso devuelve la portada a su sitio, correcto")
    return 0


def cmd_todo(a):
    fallos = 0
    for nombre, fn, arg in (("audit", cmd_audit, argparse.Namespace(pagina="index.es.html")),
                            ("filtros", cmd_filtros, a),
                            ("mapa", cmd_mapa, argparse.Namespace(pagina="longaurjauziak.html")),
                            ("temas", cmd_temas, argparse.Namespace(pagina="index.es.html")),
                            ("offline", cmd_offline, argparse.Namespace(pagina="index.es.html")),
                            ("mio", cmd_mio, a),
                            ("visor", cmd_visor, a),
                            ("aviso", cmd_aviso, a)):
        print(f"\n=== {nombre}")
        fallos += 1 if fn(arg) else 0
    print("\n" + ("navegador: las 8 comprobaciones, correctas" if not fallos
                   else f"navegador: {fallos} comprobacion(es) fallidas"))
    return 1 if fallos else 0


def cmd_verifica(a):
    """Todo lo que hay que pasar antes de publicar, en un solo codigo de salida.

    Existe porque encadenar las comprobaciones a mano con `| grep ... && echo
    TODO CORRECTO` daba por bueno lo que no lo era: grep sale con exito por
    haber *encontrado* la linea, diga «fail 0» o «fail 1». Aqui manda el
    codigo de salida de cada paso y el veredicto se imprime una sola vez, al
    final. Con --rapido se salta el navegador (lo lento) y se queda en la
    bateria de ficheros.
    """
    pasos = [("construir", cmd_build, a),
             ("ficheros", cmd_check, a)]
    if not getattr(a, "rapido", False):
        pasos.append(("navegador", cmd_todo, a))
    fallaron = []
    for nombre, fn, arg in pasos:
        print(f"\n===== {nombre}")
        try:
            malo = fn(arg)
        except Exception as e:          # noqa: BLE001 -- un paso que revienta
            # tambien es un paso que falla, y el veredicto tiene que salir
            print(f"  EXCEPCION en {nombre}: {type(e).__name__}: {e}")
            malo = True
        if malo:
            fallaron.append(nombre)
    print()
    if fallaron:
        print("VERIFICACION FALLIDA: " + ", ".join(fallaron))
        return 1
    print(f"VERIFICACION CORRECTA ({len(pasos)} pasos)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("serve").set_defaults(fn=cmd_serve)
    sub.add_parser("filtros").set_defaults(fn=cmd_filtros)
    sub.add_parser("mio").set_defaults(fn=cmd_mio)
    sub.add_parser("visor").set_defaults(fn=cmd_visor)
    sub.add_parser("aviso").set_defaults(fn=cmd_aviso)
    sub.add_parser("todo").set_defaults(fn=cmd_todo)
    s = sub.add_parser("verifica"); s.set_defaults(fn=cmd_verifica)
    s.add_argument("--rapido", action="store_true",
                   help="sin el navegador: solo construir y la bateria de ficheros")

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
