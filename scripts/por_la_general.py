#!/usr/bin/env python3
"""Hace que todo track que pase junto al domicilio vaya por la BI-633.

    python3 scripts/por_la_general.py --revisa
    python3 scripts/por_la_general.py <ruta> [<ruta>...]
    python3 scripts/por_la_general.py --todas

POR QUE ESTE Y NO scripts/aleja_de_casa.py
------------------------------------------
aleja_de_casa.py miraba PUNTOS: que ninguno cayera cerca del domicilio. Pero
lo que se dibuja son las RECTAS entre punto y punto, y al quitar un trozo y
pegar otro quedaban saltos de hasta 40 m que cortaban la curva y pasaban por
donde el track ya no tenia ni un punto. Ademas junto a la casa hay dos vias
que llegan al mismo sitio: la general y el camino particular, que sale de
ella, pasa por delante de la casa y vuelve a juntarse mas al suroeste. Los
tracks cogian el camino.

QUE HACE
--------
Donde un track se acerca al domicilio y no va por la general, se sustituye
ese trozo entero por el trozo real de BI-633 del GPX de galdaramino -- la
ruta que el autor dio por buena -- cosido en dos puntos donde el track ya
esta encima de la general, a menos de SUTURA metros. Asi no queda ninguna
recta inventada: el paso por delante de la casa es, punto por punto, el de
galdaramino.

Al mezclar dos grabaciones los tiempos dejarian de ser ciertos, asi que se
quitan, como ya se hizo en sancristobaloiz, muniozguren y santaeufemia.

EL PUNTO A EVITAR vive en scripts/.punto-privado.json, EXCLUIDO DE GIT: este
repositorio es publico y escribir ahi la coordenada seria publicar justo lo
que se intenta esconder.
"""
import json
import math
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NS = "{http://www.topografix.com/GPX/1/1}"
PUNTO = os.path.join(HERE, ".punto-privado.json")
DONANTE = "galdaraminio"
TRABAKUA = (43.210466, -2.5460838)

AVISO = 150.0     # si un track entra aqui, hay que repasarle el paso
VENTANA = 200.0   # y se le sustituye todo este entorno por la general
SUTURA = 8.0      # el cosido tiene que caer encima de la general
IGUAL = 4.0       # por debajo de esto el track ya ES la general
ENTORNO = 900.0   # trozo de galdaramino que se usa como referencia
HUECO = 40.0      # a partir de aqui, un salto del GPS no se cruza con una recta
PEGADO = 12.0     # y se cierra con la general si los dos extremos van por ella

ET.register_namespace("", "http://www.topografix.com/GPX/1/1")


def privado():
    if not os.path.exists(PUNTO):
        raise SystemExit(
            f"\nFalta {os.path.relpath(PUNTO, ROOT)}, que no va en git.\n"
            "Sin el no se puede saber que punto hay que evitar.")
    with open(PUNTO, encoding="utf-8") as f:
        d = json.load(f)
    return (d["lat"], d["lon"])


def haversine(a, b):
    r = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    return 2 * r * math.asin(math.sqrt(
        math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))


def leer(slug):
    arbol = ET.parse(os.path.join(ROOT, "src", slug + ".gpx"))
    out = []
    for p in arbol.getroot().iter(NS + "trkpt"):
        ele = p.find(NS + "ele")
        t = p.find(NS + "time")
        out.append((float(p.get("lat")), float(p.get("lon")),
                    ele.text if ele is not None else None,
                    t.text if t is not None else None))
    return out


class General:
    """El trozo de BI-633 que pasa junto a la casa, como linea continua."""

    def __init__(self, puntos, casa):
        self.casa = casa
        j = min(range(len(puntos)), key=lambda i: haversine(puntos[i], casa))
        a = j
        while a > 0 and haversine(puntos[a - 1], casa) < ENTORNO:
            a -= 1
        b = j
        while b < len(puntos) - 1 and haversine(puntos[b + 1], casa) < ENTORNO:
            b += 1
        self.ps = puntos[a:b + 1]
        self.k = math.cos(math.radians(casa[0]))

    def xy(self, p):
        return ((p[1] - self.casa[1]) * 111320 * self.k,
                (p[0] - self.casa[0]) * 110540)

    def cerca(self, q):
        """(distancia en metros, posicion a lo largo de la linea)."""
        qx, qy = self.xy(q)
        mejor = (1e9, 0.0)
        for i in range(len(self.ps) - 1):
            ax, ay = self.xy(self.ps[i])
            bx, by = self.xy(self.ps[i + 1])
            dx, dy = bx - ax, by - ay
            L = dx * dx + dy * dy
            s = 0.0 if L == 0 else max(0.0, min(1.0, ((qx - ax) * dx + (qy - ay) * dy) / L))
            d = math.hypot(qx - ax - s * dx, qy - ay - s * dy)
            if d < mejor[0]:
                mejor = (d, i + s)
        return mejor

    def en(self, t):
        """El punto exacto de la general en esa posicion."""
        i = min(int(t), len(self.ps) - 2)
        s = t - i
        a, b = self.ps[i], self.ps[i + 1]
        return (a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s, a[2], None)

    def trozo(self, t0, t1):
        """La general entre dos posiciones, con los extremos exactos.

        Los extremos van calculados y no redondeados al vertice mas cercano:
        asi el cosido con el track mide lo que mide la perpendicular, y no
        queda una recta de varios metros atravesando la curva.
        """
        a, b = (t0, t1) if t0 <= t1 else (t1, t0)
        out = [self.en(a)]
        out += [self.ps[i] for i in range(int(math.ceil(a)), int(math.floor(b)) + 1)]
        out += [self.en(b)]
        return out if t0 <= t1 else out[::-1]


def arregla(slug, casa, gen):
    ps = leer(slug)
    d = [haversine(p, casa) for p in ps]
    if min(d) > AVISO:
        return None, []
    # Se sustituye TODO el entorno, no solo lo que se sale de la general.
    # Cambiar unicamente los trozos malos dejaba puntos del track y puntos de
    # galdaramino alternados, y como una grabacion va unos metros corrida
    # respecto de la otra el dibujo iba y volvia: justo el gancho que se veia
    # en axmakurandikoa. Pegado entero no hay donde alternar.
    malo = [i for i, p in enumerate(ps) if d[i] < VENTANA]
    if not malo:
        return None, []
    # los puntos se agrupan: un track puede pasar dos veces
    grupos, actual = [], [malo[0]]
    for i in malo[1:]:
        if i - actual[-1] <= 40:
            actual.append(i)
        else:
            grupos.append(actual); actual = [i]
    grupos.append(actual)

    hechos = []
    for g in reversed(grupos):           # de atras adelante, no mueve indices
        # Un track puede asomarse al entorno y volverse por donde ha venido,
        # sin llegar a pasar por delante. Eso no se toca: los dos cosidos
        # caerian en el mismo sitio de la general y el cambio se comeria el
        # recorrido.
        ts = [gen.cerca(ps[i])[1] for i in g]
        if abs(ts[-1] - ts[0]) < 5:
            continue
        # Y si ya es la general, tampoco. El margen es estrecho a proposito:
        # una grabacion va unos metros corrida respecto de otra, y mezclar sus
        # puntos con los de galdaramino dibuja idas y venidas aunque ninguno
        # se salga de la carretera. Era el gancho que se veia en
        # axmakurandikoa. Puesta entera, la ventana es galdaramino y ya esta.
        # Se juzga por el nucleo (AVISO), no por todo el entorno: el punto
        # del cosido vive en el borde y puede quedar a unos metros de la
        # general sin que eso sea nada. Mirando el entorno entero el script
        # se veia trabajo a si mismo cada vez que se pasaba.
        nucleo = [i for i in g if d[i] < AVISO]
        if nucleo and max(gen.cerca(ps[i])[0] for i in nucleo) <= IGUAL:
            continue
        if not nucleo:
            continue
        # El cosido se busca primero donde el track ES la general (IGUAL), y
        # solo si no aparece en 400 m se conforma con SUTURA. Buscarlo con el
        # margen ancho dejaba el propio punto del cosido unos metros fuera, y
        # al volver a pasar el script lo veia como pendiente.
        a, b = g[0], g[-1]
        for tope in (IGUAL, SUTURA):
            a, b = g[0], g[-1]
            while a > 0 and gen.cerca(ps[a])[0] > tope and haversine(ps[a], casa) < 400:
                a -= 1
            while (b < len(ps) - 1 and gen.cerca(ps[b])[0] > tope
                   and haversine(ps[b], casa) < 400):
                b += 1
            if gen.cerca(ps[a])[0] <= tope and gen.cerca(ps[b])[0] <= tope:
                break
        if gen.cerca(ps[a])[0] > SUTURA or gen.cerca(ps[b])[0] > SUTURA:
            hechos.append("AVISO: el tramo llega a un extremo del track sin "
                          "tocar la general; hay que mirarlo a mano")
            continue
        t0 = gen.cerca(ps[a])[1]
        t1 = gen.cerca(ps[b])[1]
        trozo = gen.trozo(t0, t1)
        quitado = sum(haversine(ps[i], ps[i + 1]) for i in range(a, b))
        puesto = sum(haversine(trozo[i], trozo[i + 1]) for i in range(len(trozo) - 1))
        # Si el track entra y sale por el mismo lado, los dos cosidos caen en
        # el mismo sitio de la general y el cambio se comeria el recorrido.
        # Eso no es un paso por delante de la casa: es otra cosa, y se avisa.
        if not 0.6 * quitado <= puesto <= 1.6 * quitado + 20:
            hechos.append("AVISO: cambiarlo dejaria %.0f m donde hay %.0f m; "
                          "no es un paso por la general, hay que mirarlo a mano"
                          % (puesto, quitado))
            continue
        ps = ps[:a + 1] + [(q[0], q[1], q[2], None) for q in trozo] + ps[b:]
        hechos.append("puesto por la general %.0f m donde habia %.0f m"
                      % (puesto, quitado))
    # Los huecos de la grabacion. Donde el GPS se quedo sin señal el fichero
    # salta de un punto a otro y el mapa cruza el hueco con una recta: la de
    # axmakurandikoa mide 316 m y se va 18 m de la carretera, dibujando una
    # lazada que no existe. Si los dos extremos estan sobre la general, el
    # hueco se rellena con la general, que es por donde iba.
    i = 1
    while i < len(ps):
        salto = haversine(ps[i - 1], ps[i])
        if salto > HUECO:
            da, ta = gen.cerca(ps[i - 1])
            db, tb = gen.cerca(ps[i])
            if da <= PEGADO and db <= PEGADO:
                trozo = gen.trozo(ta, tb)
                ps = ps[:i] + [(q[0], q[1], q[2], None) for q in trozo] + ps[i:]
                hechos.append("cerrado con la general un hueco de %.0f m de la grabacion"
                              % salto)
                i += len(trozo)
        i += 1
    return ps, hechos


def escribe(slug, puntos):
    ruta = os.path.join(ROOT, "src", slug + ".gpx")
    arbol = ET.parse(ruta)
    seg = arbol.getroot().find(f".//{NS}trkseg")
    for hijo in list(seg):
        seg.remove(hijo)
    for lat, lon, ele, _ in puntos:
        p = ET.SubElement(seg, NS + "trkpt", {"lat": str(lat), "lon": str(lon)})
        if ele is not None:
            ET.SubElement(p, NS + "ele").text = str(ele)
    ET.indent(arbol, space="  ")
    arbol.write(ruta, encoding="UTF-8", xml_declaration=True)


def largo(ps):
    return sum(haversine(ps[i - 1], ps[i]) for i in range(1, len(ps))) / 1000


def main():
    casa = privado()
    gen = General(leer(DONANTE), casa)
    import glob
    todos = sorted(os.path.basename(g)[:-4]
                   for g in glob.glob(os.path.join(ROOT, "src", "*.gpx")))
    revisa = "--revisa" in sys.argv
    slugs = [a for a in sys.argv[1:] if not a.startswith("--")]
    if revisa or "--todas" in sys.argv:
        slugs = todos
    for slug in slugs:
        if slug == DONANTE:
            continue
        ps = leer(slug)
        nuevos, hechos = arregla(slug, casa, gen)
        if not hechos:
            continue
        print("== %s" % slug)
        for h in hechos:
            print("   %s" % h)
        if not revisa and nuevos:
            print("   %.2f km -> %.2f km" % (largo(ps), largo(nuevos)))
            escribe(slug, nuevos)


if __name__ == "__main__":
    main()
