# Guía del proyecto — trabakutik.com

Todo lo que hace falta para seguir trabajando en este sitio sin mí. Escrita el
21 de octubre de 2026, con 61 rutas publicadas.

Si vas a pedirle ayuda a otra herramienta o a otra persona, dale este fichero
entero. Está pensado para leerse de arriba abajo una vez y volver a él por
partes.

---

## 1. Qué es esto y dónde vive

Un sitio estático de rutas de senderismo y e-bike por Mallabia y alrededores,
en castellano y euskera, publicado en **https://trabakutik.com/** con **GitHub
Pages** desde la **rama `main`** del repositorio, sirviendo **la raíz tal cual**.

No hay servidor, ni base de datos, ni framework. Son ficheros HTML, CSS y
JavaScript escritos a mano, más unos scripts de Python que los montan.

**La regla de oro:** todos los `.html`, `.css` y `.js` que están en la raíz del
repositorio **son generados**. No se tocan nunca a mano: se editan los fuentes
de `src/` y se vuelve a construir. Si editas la raíz, el siguiente `build.py`
se lleva tu cambio por delante.

`_config.yml` es lo que impide que GitHub publique los fuentes (`src/*.html`,
`src/css`, `src/js`, `src/i18n`, `scripts/`, las notas del proyecto). Lo que sí
se publica de `src/` son **las descargas**: los `.gpx`, los `.kml` y
`todas-las-rutas.zip`, porque cada ficha los enlaza.

---

## 2. Las dos órdenes que hay que saber

Después de tocar cualquier texto en castellano, siempre las dos y en este orden:

```
python3 src/i18n/make_eu.py    # regenera las páginas en euskera
python3 src/build.py           # monta el sitio entero en la raíz
```

`make_eu.py` **se niega a funcionar** si una clave de traducción ya no coincide
letra por letra con el texto en castellano. No es un fallo: es el aviso de que
has cambiado algo en castellano y falta cambiarlo en `src/i18n/eu.py`. Arréglalo
ahí y vuelve a pasarlo.

`build.py` tarda **1,5 segundos**. Si alguna vez tarda 6, es que se ha borrado
`.cache-build/`, que se puede borrar entera sin perder nada.

---

## 3. Cómo está organizado

```
src/<ruta>_head.html   la cabecera de una ficha (title, meta, JSON-LD)
src/<ruta>_tail.html   el cuerpo: héroe, datos, fotos, texto, mapa, pie
src/<ruta>.gpx         el track de verdad, grabado sobre el terreno
src/<ruta>.kml         lo mismo en KML (generado)
src/mallabia_*.html    la portada
src/i18n/eu.py         todas las traducciones al euskera
src/i18n/make_eu.py    genera las páginas .eu.html desde esas tablas
src/build.py           junta cabecera + cuerpo y escribe la raíz
src/css/, src/js/      estilos y scripts, compartidos por todas las páginas
data/<ruta>.json       los puntos del track para el mapa de esa ficha
data/trailhead.json    todos los tracks juntos, para el mapa de la portada
data/fuentes.json      las fuentes de agua (generado)
img/                   las fotos publicadas, en varias tallas
img/orig/              los originales de 1600 px, NO publicados
scripts/               las herramientas (ver más abajo)
```

**Cada página es un fichero de verdad** (`urko.html`, `kalamua.html`…), no una
ruta de una aplicación. Se puede abrir, marcar y compartir cada una.

`PAGES` en `src/build.py` es la lista mandante: **una página que no esté ahí no
existe**. Hay que añadirla también a `PAGES` y `ROUTE_PAGES` de
`src/i18n/make_eu.py`.

---

## 4. Las herramientas de `scripts/`

Cada una hace una cosa y se pasa cuando toca:

| Script | Para qué | Cuándo |
|---|---|---|
| `make_map_data.py` | rehace `data/<ruta>.json` y `trailhead.json` desde los GPX | **siempre que cambie un GPX** |
| `make_kml.py` | el `.kml` de cada ruta | al cambiar un GPX |
| `bundle_gpx.py` | rehace `todas-las-rutas.zip` | al cambiar o añadir un GPX |
| `rehaz_perfil.py` | el perfil de alturas y los kilómetros de los puntos numerados | al cambiar un GPX |
| `optimize_images.py` | reduce a 1600 px y genera los `.webp` | al meter fotos nuevas |
| `make_wide_variants.py` | las versiones de 800 px que sirve la galería | al meter fotos nuevas |
| `make_card_thumbs.py` | la foto de la tarjeta de la portada, en tres tallas | al meter una ruta en la portada |
| `make_card_maps.py` | la miniatura de mapa de cada tarjeta | al meter una ruta nueva |
| `make_places.py` | los nombres por los que se puede buscar cada ruta | al meter o cambiar una ruta |
| `make_fuentes.py` | `data/fuentes.json`, la página del agua | al tocar las fuentes |
| `check_site.py` | 26.451 comprobaciones sobre el sitio ya construido | **antes de publicar** |

Dos avisos que cuestan caros si se olvidan:

- `optimize_images.py` **no vuelve a tocar** una foto ya procesada. Es a
  propósito: volver a comprimir un JPEG da bytes distintos cada vez (ahí se
  fueron cientos de MB de historial) y además la degrada un poco más.
- `make_places.py` **conserva lo que ya hay** en la tarjeta y añade lo que saca
  del mapa. Si cambias el trazado de una ruta, los nombres viejos se quedan
  pegados: hay que dejar a mano solo los buenos y volver a pasarlo.

---

## 5. Verificar antes de publicar

**Una sola orden, y se mira su código de salida:**

```
python3 .claude/skills/run-rutas-mallabia/driver.py verifica
```

Tarda unos 3 minutos. Abre el sitio en un navegador de verdad y comprueba el
diseño a cuatro anchos en los dos temas, la búsqueda, los filtros, el mapa, los
colores del héroe, el modo sin cobertura, el panel «Lo mío», el visor de fotos y
el aviso. Termina en una línea: `VERIFICACION CORRECTA (3 pasos)` o
`VERIFICACION FALLIDA`, con código 0 o 1.

Con `--rapido` va sin navegador en 50 segundos.

**No encadenes comprobaciones con `| grep … && echo "TODO CORRECTO"`.** `grep`
sale con éxito por haber *encontrado* la línea, diga «fallo 0» o «fallo 1». El
18 de octubre una misma salida dijo «# fail 1» y debajo «TODO CORRECTO».

También: `node scripts/test_ui.cjs` (14 pruebas del JavaScript, 3 segundos).

---

## 6. Cómo se mete una ruta nueva, paso a paso

Esto es lo que se hizo con las dos últimas. En orden:

1. **El GPX** a `src/<ruta>.gpx`. Si hay que coser dos grabaciones, se cosen
   por puntos reales donde los dos tracks se tocan (por debajo de 10 m) y **se
   quitan las horas de cada punto**, que ya no serían verdad.
2. **Las fotos** a `img/orig/<ruta>-01.jpg`, `-02`… y pasar
   `optimize_images.py`, `make_wide_variants.py` y `make_card_thumbs.py`. La
   que vaya de `og:image` tiene que quedarse en `img/` (no en `img/orig/`),
   porque la vista previa de redes necesita una URL que exista de verdad.
3. **`data/<ruta>.json`**: los puntos simplificados, el marcador de salida y
   las coordenadas de los puntos numerados. Luego `make_map_data.py`.
4. **El perfil de alturas**: 161 muestras repartidas por distancia, en un
   `viewBox="0 0 1000 300"`, con dos trazados — el relleno
   (`fill="var(--teal-soft)"`, cerrado con `L1000,300 L0,300 Z`) y la línea
   encima (`stroke="var(--teal)"`). **Si el relleno no cierra por abajo**, el
   navegador une el último punto con el primero y en una travesía sale una
   diagonal cruzando el dibujo.
5. **`src/<ruta>_head.html` y `_tail.html`**, copiando la estructura de una
   ficha que ya esté bien (`arteta` o `garaigaztelu` sirven).
6. **El euskera** en `src/i18n/eu.py`: un diccionario nuevo con cada cadena en
   castellano como clave, y registrarlo en `PAGE_STRINGS`, `TITLES` y
   `DESCRIPTIONS`.
7. **La lista `PAGES`** en `build.py` y en `make_eu.py` (y `ROUTE_PAGES`).
8. **La tarjeta** en `src/mallabia_tail.html`, **la primera de la rejilla**, y
   cambiar `ULTIMA_ENTRADA` en `build.py` (eso le pone la pastilla «Nueva»).
9. `make_places.py`, `make_card_maps.py`, `make_kml.py`, `bundle_gpx.py`.
10. `make_eu.py`, `build.py`, `check_site.py`, `driver.py verifica`.
11. Commit y push a `main`.

---

## 7. Las reglas de contenido (esto es lo importante)

Lo demás se arregla; esto no.

- **Nunca inventar datos de una ruta.** Ni distancias, ni alturas, ni nombres de
  sitios, ni fuentes de agua. Este sitio documenta rutas pisadas de verdad. Si
  un dato no se sabe, se pregunta.
- **El desnivel acumulado no sale del GPX.** Sumar las subidas en crudo se va
  hasta un 43%. La cifra viene de la fuente de cada ruta (Wikiloc, la
  organización de la carrera) y la propia ficha lo dice.
- **Unos metros de diferencia no son un error.** Un tramo que en el mapa va por
  la recta en vez de por la curva no le cambia nada a quien va al monte. Y un
  GPS tiene error de hasta 15 m: si una cima aparece con 795, 791 y 783 m en
  tres sitios, es el mismo monte. **Lo que sí son fallos** son los datos que
  contradicen la realidad: una distancia que no cuadra con el GPX, un nombre
  equivocado, una fuente que no existe.
- **No reescribir un texto que no te han pedido tocar.** Si el autor manda un
  párrafo, va casi literal: solo se le ponen las negritas y los enlaces. Si
  algo cercano parece mejorable, se dice y que decida él.
- **Avisar siempre de lo que falte o no cuadre**, aunque no venga a cuento y
  aunque nadie lo haya preguntado. Con la prueba delante, y que decida él.
- **Un GPX no puede empezar, acabar ni pasar por delante de la casa del autor.**
  Siempre por la BI-633. Hay un script (`por_la_general.py`) que sustituye ese
  trozo por los puntos de otra ruta aprobada, y `check_site.py` lo comprueba por
  segmentos. Los márgenes están en `scripts/.punto-privado.json`, que **no está
  en git** porque el repositorio es público: sin ese fichero los dos scripts se
  saltan solos y lo dicen.

**Decidido y cerrado — no volver a plantearlo:**

- Los kilómetros de los puntos numerados de nueve fichas van sobre la base
  antigua. El autor lo ha mirado y los deja así.
- `intxorta` tiene un corte de grabación de 644 m: **el original de Wikiloc
  trae el mismo corte**, no hay nada que recuperar.
- `longa` no está grabada, está trazada en Wikiloc. Sus tramos rectos son como
  se trazó.

---

## 8. El euskera

Solo se escriben a mano los ficheros en castellano. Los `.eu.html` **se generan
y se sobrescriben**: para cambiar un texto en euskera se edita
`src/i18n/eu.py`.

El tono importa: natural y cercano, no un calco del castellano. Vale reordenar
una frase si en euskera suena mejor, mientras no cambie ningún dato.

- «eolikoak» para los aerogeneradores (no «aerosorgailuak»), salvo dentro de
  «parke eolikoaren aerosorgailuak».
- Siempre «zirkuitua» para circuito, nunca «zirkulua».
- La negrita, solo en la raíz de la palabra: `<b>Kalamua</b>ko`, no
  `<b>Kalamuako</b>`.
- Guiones y apóstrofos normales, nada de los raros que mete el dictado.

---

## 9. Cosas que conviene saber antes de tocarlas

- **Las fichas pesan**. Un `_tail.html` con fotos lleva líneas de base64 de
  megabytes. No las abras enteras: filtra por longitud de línea.
- **Nada de terceros nuevos.** Las tipografías y Leaflet están alojados aquí.
  Solo se piden fuera dos cosas, y nunca desde el HTML: **las teselas de los
  mapas** y **el tiempo** (Open-Meteo, que es gratis, sin clave y con CORS
  abierto, que es por lo que se puede llamar desde una web estática). Cada
  tercero nuevo ve la IP de quien entra y habría que decirlo en el aviso legal.
- **Las teselas no se guardan nunca.** Las condiciones de uso de OpenStreetMap,
  CyclOSM y el IGN lo prohíben. Sin cobertura el track se dibuja sobre un fondo
  vacío, y es correcto que así sea.
- **El sitio funciona sin cobertura**: un service worker guarda cada ficha ya
  visitada. Estrategia: la red primero para las páginas, la caché primero para
  lo demás. Si alguna vez hay que matarlo, se publica un `sw.js` cuyo cuerpo
  entero sea `self.registration.unregister()`.
- **El tema oscuro es el de por defecto.** El claro es una elección guardada en
  el navegador y aplicada antes de pintar.
- **GitHub Pages tiene un techo de 1 GB.** El sitio publicado va por 445 MB:
  caben unas 70 rutas más. El repositorio pesa más (944 MB de historial), pero
  eso no afecta a la web.

---

## 10. Git

- Se trabaja directamente sobre **`main`** y se publica con `git push`.
- **Mensajes de commit en castellano**, explicando *por qué*, no solo *qué*.
- Al empujar se disparan tres comprobaciones en GitHub: consistencia de rutas,
  sitio generado y el despliegue de Pages. **Las tres tienen que quedar en
  verde.**
- El despliegue tarda **uno o dos minutos** en llegar a la web. Si acabas de
  subir algo y lo ves igual, casi siempre es eso.

---

## 11. Qué herramienta sirve para seguir

Con franqueza: **Lovable no encaja con este repositorio**. Lovable construye
aplicaciones nuevas de React y Tailwind en su propio entorno; aquí hay HTML
escrito a mano, scripts de Python con la biblioteca estándar, tracks GPX,
fotografías y un navegador de verdad para verificar. Pedirle que mantenga esto
es pedirle algo para lo que no está hecho, y lo más probable es que acabe
reescribiendo el sitio en otra tecnología.

Lo que sí sirve:

1. **Esto mismo** (Claude Code sobre el repositorio), que es como está hecho
   todo lo anterior.
2. **Cualquier asistente con acceso al repositorio**, dándole este fichero y
   `CLAUDE.md`. Para ChatGPT y Codex en concreto, mira el apartado 12: llegan,
   pero con un agujero que conviene conocer antes.
3. **A mano**: editar `src/`, pasar las dos órdenes del apartado 2, mirar
   `check_site.py` y empujar. No hace falta nada más instalado que Python 3.

Lo que nunca debería pasar, lo trabaje quien lo trabaje: que alguien edite los
`.html` de la raíz, que se publique sin pasar `check_site.py`, o que se invente
un dato de una ruta.

---

## 12. ChatGPT y Codex: hasta dónde llegan

La pregunta de siempre es si lo puede seguir ChatGPT. La respuesta depende de
cuál de los dos ChatGPT, porque no son lo mismo.

### Codex (el agente de OpenAI): sí, con un agujero

Codex — en `codex.chatgpt.com` o su herramienta de línea de órdenes — clona el
repositorio de verdad, ejecuta órdenes y hace commit. Sobre esto puede
trabajar. Lo que le funciona y lo que no:

| Orden | ¿Funciona? | Por qué |
| --- | --- | --- |
| `python3 src/i18n/make_eu.py` | Sí | Python de la biblioteca estándar, sin instalar nada |
| `python3 src/build.py` | Sí | Igual |
| `python3 scripts/check_site.py` | Sí | Las 26.451 comprobaciones, sin dependencias |
| `node scripts/test_ui.cjs` | Sí | Node viene en el entorno |
| `driver.py verifica` | **Probablemente no** | Necesita Chromium y Playwright |

El agujero es el último y no es pequeño. El `driver.py` abre un navegador de
verdad y comprueba ocho cosas que ningún script de texto puede ver: que el
mapa cargue, que los filtros filtren, que los temas claro y oscuro cambien,
que el sitio funcione sin conexión, que «Lo mío» recuerde las rutas, que el
visor de fotos abra, que el aviso se cierre dejando la portada donde estaba, y
la auditoría de la página. Para eso hace falta descargar Chromium, y los
entornos de Codex vienen **con la red cortada por defecto**. Hay que
activársela en los ajustes del entorno, y aun así no está garantizado.

Sin el `driver.py`, Codex publica a ciegas en todo lo que sea JavaScript o
mapa. Puede seguir añadiendo rutas y arreglando textos con bastante
seguridad — eso lo cubre `check_site.py` —, pero no debería tocar
`src/js/` sin alguien que mire la página después.

### ChatGPT a secas (la ventana de chat): no

Con el conector de GitHub puede leer el repositorio y explicarte cosas, y
escribe bien. Pero **no ejecuta nada**: no construye, no verifica, no hace
commit. Pegar fragmentos de un lado a otro con 61 páginas, dos idiomas y
26.451 comprobaciones no acaba bien. Es exactamente lo mismo que pasa con
Lovable (apartado 11). Para consultar y para escribir, bien; para construir,
no.

### Lo que hay que darle el primer día, sea la herramienta que sea

1. **Este fichero y `CLAUDE.md`, enteros**, no resumidos.
2. **`make_eu.py` antes que `build.py`, siempre, y en ese orden.** Si cambia
   una frase en castellano y no se pasa `make_eu.py`, la traducción al
   euskera se queda descolgada y el build falla a propósito. Es la trampa en
   la que cae todo el que llega nuevo.
3. **Nunca inventar un dato**: desniveles, tiempos, fuentes, nombres de
   sitios. Lo que no esté en la fuente, se pregunta o se dice que falta
   (apartado 7).
4. **No reescribir el texto de las rutas.** Lo escribe el autor. Se corrige una
   falta o se ajusta una frase si él lo pide, nada más.
5. **Verificar antes de publicar**, y si no puede pasar el `driver.py`, que lo
   diga en vez de dar por buena la parte que no ha mirado.
