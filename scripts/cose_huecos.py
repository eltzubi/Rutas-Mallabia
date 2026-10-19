#!/usr/bin/env python3
"""Cierra un hueco de grabacion con el track real de otra ruta que pasa alli.

    python3 scripts/cose_huecos.py --revisa
    python3 scripts/cose_huecos.py <ruta> [<ruta>...]

QUE ES UN HUECO Y QUE NO
------------------------
Entre dos puntos seguidos de un GPX el mapa dibuja una RECTA. Cuando el
aparato deja de registrar un rato -- un tunel, una cuesta entre arboles, la
bateria -- esa recta se come cientos de metros de camino de verdad y en el
mapa se ve como un tajo que atraviesa lo que haya en medio.

Eso NO es lo mismo que un track poco poblado. Una grabacion normal de este
sitio tiene unos 318 puntos por kilometro; las hay de 81, y entonces casi
todos los tramos rectos son largos sin que falte nada. Ahi no hay nada que
cerrar: rellenar seria inventarse por donde se fue.

COMO SE CIERRA, SIN INVENTAR NADA
---------------------------------
Solo con el track de OTRA ruta que haya recorrido ese mismo trozo de verdad.
Se exige que esa otra ruta pase a menos de EXTREMO metros de los DOS
extremos del hueco, que su propio trozo no tenga ningun salto mayor de SALTO
metros (si no, es que tambien le falta grabacion) y que no se desvie mas de
VUELTA veces la recta (si no, es que va por otro sitio). Se pegan sus puntos
tal cual: ni una coordenada calculada.

Mezclar dos grabaciones hace falsa la hora de cada punto, asi que la hora se
cae -- como ya se hizo en sancristobaloiz, muniozguren y santaeufemia.

Es idempotente: cerrado el hueco, una segunda pasada no encuentra nada.

DESPUES HAY QUE REHACER LO QUE CUELGA DEL TRACK
-----------------------------------------------
make_kml.py, make_map_data.py, rehaz_perfil.py, bundle_gpx.py, la distancia
de la ficha y de la tarjeta, y el euskera de todo ello. El desnivel
acumulado NO cambia: sale de la fuente de la ruta, no del GPX.
"""
import collections
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "{http://www.topografix.com/GPX/1/1}"
TRKPT = re.compile(r"<trkpt\b")

Punto = collections.namedtuple("Punto", "lat lon slat slon ele")

HUECO = 40.0      # a partir de aqui el salto es sospechoso
EXTREMO = 15.0    # la donante tiene que pasar por los dos extremos
SALTO = 20.0      # y no tener ella misma un hueco dentro del trozo
VUELTA = 2.0      # ni dar un rodeo: largo del trozo / largo de la recta

# Quien puede donar el trozo de cada ruta. Se prueban en orden y se coge la
# primera que cumpla las tres condiciones.
DONANTES = {
    "hirutxikiak": ("egoarbitza", "gereaoculta"),
}


def leer(slug):
    """Cada punto con sus numeros ya en coma flotante y tal como estan escritos.

    Se guarda el texto literal de lat/lon/ele para poder pegarlos sin pasarlos
    por un float y que cambien de forma: 43.210790 no debe convertirse en
    43.21079.
    """
    arbol = ET.parse(os.path.join(ROOT, "src", slug + ".gpx"))
    out = []
    for p in arbol.getroot().iter(NS + "trkpt"):
        ele = p.find(NS + "ele")
        out.append(Punto(float(p.get("lat")), float(p.get("lon")),
                         p.get("lat"), p.get("lon"),
                         ele.text if ele is not None else None))
    return out


def metros(a, b):
    lat = math.radians((a[0] + b[0]) / 2)
    return math.hypot((a[1] - b[1]) * 111320 * math.cos(lat),
                      (a[0] - b[0]) * 111320)


def largo(ps):
    return sum(metros(ps[i - 1], ps[i]) for i in range(1, len(ps)))


def huecos(ps):
    return [i for i in range(1, len(ps)) if metros(ps[i - 1], ps[i]) > HUECO]


def trozo(donante, a, b):
    """El trozo de la donante entre los dos extremos, o None si no sirve."""
    ia = min(range(len(donante)), key=lambda i: metros(a, donante[i]))
    ib = min(range(len(donante)), key=lambda i: metros(b, donante[i]))
    da, db = metros(a, donante[ia]), metros(b, donante[ib])
    if da > EXTREMO or db > EXTREMO:
        return None, f"pasa a {da:.0f} m y {db:.0f} m de los extremos"
    al_reves = ia > ib
    i, j = (ib, ia) if al_reves else (ia, ib)
    t = donante[i:j + 1]
    if len(t) < 2:
        return None, "no tiene puntos entre medias"
    salto = max(metros(t[k - 1], t[k]) for k in range(1, len(t)))
    if salto > SALTO:
        return None, f"su propio trozo tiene un salto de {salto:.0f} m"
    recta = metros(a, b)
    if recta and largo(t) / recta > VUELTA:
        return None, f"da un rodeo de {largo(t) / recta:.1f} veces la recta"
    return (list(reversed(t)) if al_reves else t), None


def escribe(slug, inserciones):
    """Mete los puntos nuevos en el fichero, sin tocar ni una linea de las demas.

    Se hace sobre el texto y no reescribiendo el XML a proposito: volver a
    serializarlo le cambia el prefijo del espacio de nombres y la sangria a
    las 22.000 lineas, el diff se vuelve ilegible y make_kml.py deja de
    encontrar los puntos.

    `inserciones` es {indice del punto delante del cual se mete: [puntos]}.
    """
    ruta = os.path.join(ROOT, "src", slug + ".gpx")
    with open(ruta, encoding="utf-8") as f:
        lineas = f.readlines()
    donde = [i for i, l in enumerate(lineas) if TRKPT.search(l)]
    modelo = lineas[donde[0]]
    sangria = modelo[:len(modelo) - len(modelo.lstrip())]
    con_ele = "<ele>" in modelo
    salida, puesto = [], 0
    for i, linea in enumerate(lineas):
        if puesto < len(donde) and i == donde[puesto]:
            for p in inserciones.get(puesto, ()):
                cuerpo = f'<ele>{p.ele}</ele>' if con_ele and p.ele else ""
                salida.append(f'{sangria}<trkpt lat="{p.slat}" lon="{p.slon}">'
                              f'{cuerpo}</trkpt>\n')
            puesto += 1
        salida.append(linea)
    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(salida)


def arregla(slug, escribir):
    ps = leer(slug)
    hs = huecos(ps)
    if not hs:
        print(f"{slug}: sin huecos de mas de {HUECO:.0f} m")
        return False
    antes = largo(ps)
    inserciones, nuevos = {}, []
    for i, p in enumerate(ps):
        if i in hs:
            a, b = ps[i - 1], p
            for nombre in DONANTES.get(slug, ()):
                t, porque = trozo(leer(nombre), a, b)
                if t is None:
                    print(f"  {metros(a, b):6.0f} m: {nombre} no vale, {porque}")
                    continue
                print(f"  {metros(a, b):6.0f} m: lo cierra {nombre} con "
                      f"{len(t)} puntos y {largo(t):.0f} m de camino")
                inserciones[i] = t
                nuevos.extend(t)
                break
            else:
                print(f"  {metros(a, b):6.0f} m: SIN CERRAR, no hay donante")
        nuevos.append(p)
    if not inserciones:
        return False
    print(f"{slug}: {len(inserciones)} hueco(s) cerrado(s); "
          f"{len(ps)} -> {len(nuevos)} puntos, "
          f"{antes / 1000:.3f} -> {largo(nuevos) / 1000:.3f} km")
    if escribir:
        escribe(slug, inserciones)
        print(f"{slug}: escrito src/{slug}.gpx")
    return True


def main():
    args = sys.argv[1:]
    revisa = "--revisa" in args
    rutas = [a for a in args if not a.startswith("-")] or sorted(DONANTES)
    for slug in rutas:
        arregla(slug, not revisa)


if __name__ == "__main__":
    main()
