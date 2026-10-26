#!/usr/bin/env python3
"""data/alturas-caminos.json: la altura de cada punto de data/caminos.json.

Los caminos de OpenStreetMap no traen altura ninguna, asi que al dibujar un
trazado que se sale de las rutas de la web el panel se quedaba sin desnivel y
sin perfil. El autor pregunto por que. Esto la trae de fuera, **una sola vez y
en el build**, no desde el navegador del visitante.

La fuente es la API de elevacion de Open-Meteo, que es gratis, sin clave y sin
cuenta -- la misma casa que ya da el pronostico de cada ficha -- y por debajo
es el modelo de terreno Copernicus de 90 m. Son unas 1.120 peticiones de 100
puntos; se guardan a medias en .cache-build/ para poder reanudar si una falla.

**El dato no es tan bueno como un GPX y hay que saberlo.** Medido contra las
alturas reales de las rutas de la web, cada punto se desvia 12-19 m de media.
Peor aun: sumar las subidas punto a punto da casi el doble del desnivel real
(841 -> 1.849 m en trabakuaondarroa), porque un modelo de 90 m muestreado cada
pocos metros es una escalera. Por eso **el navegador no suma punto a punto**
cuando hay alturas de aqui: remuestrea el perfil cada 300 m, y asi el desnivel
cae a un 9 % de error medio. Esa parte esta en src/js/trazado.js.

  python3 scripts/make_alturas_caminos.py

Hay que volver a pasarlo despues de make_caminos.py.
"""
import http.client
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRADA = ROOT / 'data' / 'caminos.json'
SALIDA = ROOT / 'data' / 'alturas-caminos.json'
MEDIAS = ROOT / '.cache-build' / 'alturas-caminos-parcial.json'

SERVIDOR = 'api.open-meteo.com'
RUTA = '/v1/elevation'
LOTE = 100           # el maximo que acepta la API por peticion
HILOS = 3            # Con 8 hilos y la conexion reutilizada salian tantas
DESCANSO = 0.6       # por segundo que Open-Meteo devolvia 429. Con 3 y 0,6 s
                     # de espera salen unas 300 por minuto, la mitad del tope.
REINTENTOS = 8
# El proxy de salida corta conexiones TLS a media (SSLEOFError) cada pocas
# peticiones. No es culpa del servicio y se arregla reintentando enseguida,
# asi que la espera empieza en medio segundo y no en tres: con tres, los
# reintentos se comian la descarga entera.
ESPERA = 0.5
ESPERA_429 = 45      # cuando el servicio dice que vamos muy deprisa
# Y cada hilo se queda con SU conexion abierta en vez de abrir una nueva por
# peticion: el saludo TLS a traves del proxy de salida es lo que cuesta, y
# abriendo una cada vez la descarga entera se iba a 72 minutos.
_local = threading.local()


def _conexion(nueva=False):
    if nueva or getattr(_local, 'c', None) is None:
        try:
            if getattr(_local, 'c', None):
                _local.c.close()
        except Exception:
            pass
        _local.c = http.client.HTTPSConnection(SERVIDOR, timeout=60)
    return _local.c


def puntos_de(caminos):
    """Todos los puntos, en el mismo orden en que estan en el fichero."""
    esc = caminos.get('escala', 100000)
    todos = []
    cuantos = []
    for via in caminos['vias']:
        la, lo = via[1], via[2]
        n = 1
        todos.append((la / esc, lo / esc))
        for j in range(3, len(via), 2):
            la += via[j]
            lo += via[j + 1]
            todos.append((la / esc, lo / esc))
            n += 1
        cuantos.append(n)
    return todos, cuantos


def pide(lote):
    camino = (RUTA + '?latitude=' + ','.join('%.5f' % p[0] for p in lote) +
              '&longitude=' + ','.join('%.5f' % p[1] for p in lote))
    for intento in range(REINTENTOS):
        try:
            c = _conexion(intento > 0)
            c.request('GET', camino, headers={'Accept': 'application/json'})
            r = c.getresponse()
            cuerpo = r.read()
            if r.status == 429:
                # Nos hemos pasado de ritmo: esto no se arregla reintentando
                # enseguida, hay que esperar de verdad.
                time.sleep(ESPERA_429)
                raise ValueError('HTTP 429')
            if r.status != 200:
                raise ValueError('HTTP %d' % r.status)
            d = json.loads(cuerpo)
            if 'elevation' not in d or len(d['elevation']) != len(lote):
                raise ValueError('respuesta inesperada')
            return d['elevation']
        except Exception:
            if intento == REINTENTOS - 1:
                raise
            time.sleep(ESPERA * (2 ** intento))
    return None


def main():
    caminos = json.loads(ENTRADA.read_text())
    todos, cuantos = puntos_de(caminos)
    print(f'{len(caminos["vias"])} vias, {len(todos)} puntos, '
          f'{(len(todos) + LOTE - 1) // LOTE} peticiones')

    alturas = []
    if MEDIAS.exists():
        alturas = json.loads(MEDIAS.read_text())
        print(f'  reanudando: ya habia {len(alturas)} puntos')
    MEDIAS.parent.mkdir(exist_ok=True)

    def uno(lote):
        time.sleep(DESCANSO)
        return pide(lote)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=HILOS) as pool:
        while len(alturas) < len(todos):
            # Una tanda de 40 lotes y se guarda al acabarla: asi un corte
            # cuesta como mucho esa tanda y no la descarga entera.
            desde, tanda = len(alturas), []
            while desde + len(tanda) * LOTE < len(todos) and len(tanda) < 40:
                i = desde + len(tanda) * LOTE
                tanda.append(todos[i:i + LOTE])
            for trozo in pool.map(uno, tanda):
                alturas += trozo
            MEDIAS.write_text(json.dumps(alturas))
            hecho = len(alturas) / len(todos)
            falta = (time.time() - t0) * (1 - hecho) / max(hecho, 1e-9)
            print(f'  {len(alturas)}/{len(todos)} ({100 * hecho:.0f} %), '
                  f'faltan unos {falta / 60:.0f} min', flush=True)

    # Por via y como diferencias, igual que las coordenadas de caminos.json:
    # en metros enteros, que el modelo no da para decimales.
    salida, i = [], 0
    for n in cuantos:
        trozo = [int(round(h)) for h in alturas[i:i + n]]
        i += n
        enc = [trozo[0]]
        for k in range(1, n):
            enc.append(trozo[k] - trozo[k - 1])
        salida.append(enc)

    texto = json.dumps({'formato': 1, 'alturas': salida}, separators=(',', ':'))
    SALIDA.write_text(texto)
    MEDIAS.unlink(missing_ok=True)
    print(f'{SALIDA.relative_to(ROOT)}: {len(todos)} alturas, '
          f'{len(texto) / 1024:.0f} kB')


if __name__ == '__main__':
    main()
