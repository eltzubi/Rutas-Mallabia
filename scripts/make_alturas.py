#!/usr/bin/env python3
"""data/alturas.json: la altura de cada punto del mapa de la portada.

`data/trailhead.json` lleva solo latitud y longitud -- se simplifica a 10 m y
se ve de lejos, asi que la altura no le hacia falta y son 57 kB de mas para
todo el que abre el mapa. Pero la herramienta de dibujar un trazado
(`src/js/trazado.js`) construye su red con esos mismos puntos y necesita
saber a que altura esta cada uno para dar el desnivel de lo que el visitante
dibuja. De ahi este fichero aparte: se baja solo cuando alguien abre el modo
de dibujo, no al abrir el mapa.

Cada altura sale del punto mas cercano del `data/<ruta>.json` de esa misma
ruta, que si las lleva (ahi los puntos son [lat, lon, altura] y van
simplificados a 1 m). No se inventa nada: es la altura grabada por el GPS en
el punto de al lado.

Hay que volver a pasarlo despues de `make_map_data.py`, que es quien escribe
trailhead.json.
"""
import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
CELDA_M = 40.0          # rejilla para buscar el punto mas cercano
LAT0 = 43.2


def _slug(href):
    return (href or "").split("/")[-1].replace(".html", "")


def _rejilla(puntos):
    """Indice espacial casero: celda -> indices de los puntos que caen en ella."""
    kx = 111320 * math.cos(math.radians(LAT0))
    celdas = {}
    for i, p in enumerate(puntos):
        c = (int(p[0] * 111320 / CELDA_M), int(p[1] * kx / CELDA_M))
        celdas.setdefault(c, []).append(i)
    return celdas, kx


def alturas_de(track, detalle):
    """Una altura por cada punto del track de la portada."""
    puntos = detalle["tracks"][0]["points"] if detalle.get("tracks") else []
    puntos = [p for p in puntos if len(p) > 2]
    if not puntos:
        return [None] * len(track["points"])
    celdas, kx = _rejilla(puntos)
    salida = []
    for lat, lon in (p[:2] for p in track["points"]):
        cx, cy = int(lat * 111320 / CELDA_M), int(lon * kx / CELDA_M)
        mejor, mejor_d = None, None
        radio = 1
        while mejor is None and radio <= 6:
            for dx in range(-radio, radio + 1):
                for dy in range(-radio, radio + 1):
                    for i in celdas.get((cx + dx, cy + dy), ()):
                        q = puntos[i]
                        d = math.hypot((lat - q[0]) * 111320, (lon - q[1]) * kx)
                        if mejor_d is None or d < mejor_d:
                            mejor, mejor_d = q[2], d
            radio += 1
        salida.append(round(mejor) if mejor is not None else None)
    return salida


def main():
    th = json.loads((DATOS / "trailhead.json").read_text(encoding="utf-8"))
    fuera, sin_detalle, n = {}, [], 0
    for track in th.get("tracks", []):
        slug = _slug(track.get("href"))
        fichero = DATOS / f"{slug}.json"
        if not slug or not fichero.exists():
            sin_detalle.append(slug or "(sin href)")
            continue
        detalle = json.loads(fichero.read_text(encoding="utf-8"))
        fuera[slug] = alturas_de(track, detalle)
        n += len(fuera[slug])
    destino = DATOS / "alturas.json"
    destino.write_text(json.dumps(fuera, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {destino.relative_to(RAIZ)} "
          f"({len(fuera)} rutas, {n} alturas, {destino.stat().st_size // 1024} kB)")
    if sin_detalle:
        print("  sin fichero de detalle:", ", ".join(sin_detalle))
    huecos = sum(1 for v in fuera.values() for a in v if a is None)
    if huecos:
        print(f"  {huecos} puntos sin altura")


if __name__ == "__main__":
    main()
