# Traspaso: cómo seguir trabajando en Trabakutik

Documento para dárselo entero a otro asistente (ChatGPT o el que sea) antes de
pedirle nada. Está escrito el 2 de noviembre de 2026 y describe el estado real
de ese día, comprobado, no de memoria.

**Instrucción para el asistente que lea esto:** no hace falta que contestes a
este documento. Léelo, y a partir de ahí haz lo que se te pida respetando lo
que aquí se dice. Si algo de lo que te piden choca con una de las reglas de la
sección 2, dilo antes de tocar nada.

---

## 1. Los dos repositorios

| | `rutas-mallabia` | `trabakutik-gps-pruebas` |
|---|---|---|
| Qué es | La web, https://trabakutik.com | El navegador GPS y la app Android |
| Se publica con | GitHub Pages desde la **raíz** del repo | GitHub Pages (`nuevo.html`) |
| Rama | `main`, directo, sin pull request | `main`, directo |
| Idiomas | Castellano y euskera, 70 rutas en cada uno | Solo la página del navegador |

Los mensajes de commit van **en castellano**.

Los dos están enlazados: `.github/workflows/sincronizar-rutas.yml` copia
automáticamente `trailhead.json` al repositorio del GPS cada 15 minutos.
**`rutas.json` NO lo copia nadie: hay que llevarlo a mano.** Es un fallo
conocido y sin arreglar.

---

## 2. Reglas que no se negocian

Estas no son preferencias de estilo. Romper cualquiera de ellas hace daño de
verdad.

1. **Nunca inventes datos de una ruta.** Ni distancias, ni desniveles, ni
   nombres de sitios, ni el orden de los waypoints, ni dónde hay agua. Si no
   lo sabes, pregúntalo. Una ruta mal descrita manda a alguien al monte con
   información falsa.
2. **Los GPX de esta zona salen y llegan a Trabakua, y lo garantiza el autor
   en origen.** Lo dijo el 3 de noviembre de 2026: «siempre que sean de esta
   zona, a Trabakua; ninguna saldrá de casa, si saliera os avisaré siempre».
   Comprobado ese mismo día: 54 de los 70 GPX arrancan a menos de 300 m de
   Trabakua, y los 16 restantes son de otras zonas (Ahuntzen a 9,5 km,
   Markina a 7,5). **Así que no le pidas que revise cada ruta nueva**: se
   estaba haciendo y es ruido, porque el problema se evita antes de empezar.
   **Si el autor no dice nada, despreocúpate: no hay que comprobar nada ni
   pedirle que compruebe nada.** Él avisa si alguna sale de su casa; mientras
   no avise, se da por bueno. Sus palabras: «si algunas saliera de mi casa lo
   avisaré, si no despreocuparos».
   La regla de abajo sigue viva solo para cuando avise.
3. **Un GPX no puede empezar ni acabar en casa del autor, ni pasar por
   delante.** Siempre por la BI-633. Si el autor avisa de que una ruta sale
   de casa, se arregla con `python3 scripts/por_la_general.py <ruta>`, que
   tiene que ejecutar **en su propia máquina**: el
   archivo con la coordenada (`scripts/.punto-privado.json`) está excluido de
   git a propósito, porque el repositorio es público y meterlo ahí publicaría
   justo lo que se quiere esconder. Por eso `check_site.py` siempre avisa de
   que falta: **ese aviso es normal aquí, no es un fallo**.
4. **No reescribas texto que no te hayan pedido tocar.** Ni para «mejorarlo».
   El texto de las rutas lo escribe el autor.
5. **Avisa siempre de datos que faltan o de errores que veas**, aunque estén
   fuera de lo que te han pedido.
6. **Los kilómetros de los waypoints se quedan como están.** Están decididos.
7. **Los tracks no se quitan del mapa.**
8. **La subida de cemento de Osma a Zengotitagane es dura para una bici
   normal.** Si una ruta la usa, hay que decirlo en el apartado de «para quién
   es».
9. **Nada de ermitas en los títulos de las rutas.**
10. Cuando el autor escribe el texto primero en **euskera**, el euskera manda y
   el castellano se reescribe detrás con los mismos cortes de párrafo.
11. Estilo en euskera: «eolikoak», nunca «aerosorgailuak». Siempre
    «zirkuitua», nunca «zirkulua». La negrita solo en la raíz
    (`<b>Berriz</b>en`). Guiones ASCII normales, no rayas tipográficas.

---

## 3. La web: construir y comprobar

### Construir

Siempre en este orden, desde la raíz de `rutas-mallabia`:

```bash
python3 src/i18n/make_eu.py     # genera el euskera
python3 src/build.py            # genera todas las páginas
```

`make_eu.py` **falla a propósito** si una clave de traducción ya no coincide
**byte a byte** con el castellano. Eso no es un fallo del script: es que has
cambiado el castellano y la traducción se ha quedado huérfana. Hay que
actualizar la clave en `src/i18n/eu.py`.

También revisa el euskera generado buscando palabras castellanas
(`SPANISH_TELLS`). Si salta con una palabra que es del autor, **no la cambies
por tu cuenta: avísale**.

### Comprobar

```bash
python3 scripts/check_site.py              # 15.076 comprobaciones (1 aviso normal)
python3 scripts/verify_route_consistency.py  # 70 tarjetas ES, 70 EU, 70 tracks
node scripts/test_ui.cjs
python3 .claude/skills/run-rutas-mallabia/driver.py verifica
```

**Nunca encadenes una comprobación con `| grep … && echo "TODO CORRECTO"`.**
Eso esconde los fallos. Lee la salida entera.

`driver.py verifica` falla de vez en cuando con un **429 de Open-Meteo**. Es el
servicio del tiempo limitando peticiones, **no es una regresión**. Reintenta
más tarde.

### Cómo está hoy

- 70 rutas, 70 tarjetas en cada idioma, 70 tracks en el mapa.
- 15.076 comprobaciones en verde, con el único aviso del punto privado.

---

## 4. Añadir una ruta nueva

El orden importa, porque unos pasos dependen de otros.

1. `src/<slug>.gpx` — el track.
2. `src/<slug>_head.html` y `src/<slug>_tail.html`. **Lo más seguro es
   copiarlos de una ruta parecida y sustituir**, para que la estructura sea
   idéntica: el mismo número de `<picture>`, de `elev-marker`, los dos bloques
   `elev-legend` iguales entre sí y los dos `.eyebrow` iguales entre sí.
3. `src/i18n/eu.py`: el diccionario de la ruta, `PAGE_STRINGS['<slug>']`,
   `TITLES`, `DESCRIPTIONS` y el `HOME.update`.
4. `src/build.py` y `src/i18n/make_eu.py`: añadir el slug a `PAGES` y a
   `ROUTE_PAGES`.
5. **La tarjeta en la portada** (`src/mallabia_tail.html`). Tiene que existir
   **antes** de generar los KML y el zip, porque `make_kml.py` y
   `bundle_gpx.py` sacan la lista de rutas de las tarjetas de la portada. Si
   la tarjeta no está, el KML no se genera y `check_site.py` falla pidiéndolo.
6. `data/<slug>.json` con `tracks`, `marker` y `waypoints`.
7. **A mano**, en `data/trailhead.json`: la entrada con `color`, `href`,
   `chart` y `points` (simplificados con Douglas-Peucker a 10 m).
   **Esto no lo crea ningún script.** Cuidado con el malentendido:
   `make_map_data.py` dice que «rehace `trailhead.json`», pero lo que hace es
   **refrescar los puntos de las entradas que ya están**. Recorre los
   `data/*.json` existentes —y se salta los que no tengan exactamente un
   track, diciéndolo por pantalla— y los tracks ya presentes en
   `trailhead.json`. Si la entrada no existe, no la inventa.
8. Y ahora, en este orden:

```bash
python3 scripts/make_map_data.py     # refresca los puntos de los dos ficheros
python3 scripts/make_alturas.py      # DESPUÉS de make_map_data
python3 scripts/make_places.py       # los lugares para el buscador de la portada
python3 scripts/make_card_thumbs.py  # la foto de la tarjeta; sin esto no hay imagen
python3 scripts/make_card_maps.py    # el mini-mapa de la esquina de la tarjeta
python3 scripts/make_kml.py
python3 scripts/bundle_gpx.py
```

9. **Copiar `data/trailhead.json` y `data/rutas.json` al repositorio del GPS.**
   El primero para que el botón «Navegar esta ruta» encuentre la ruta; el
   segundo porque de ahí saca el navegador los **títulos** de su lista (sin
   él enseña el nombre del archivo). `check_site.py` comprueba los dos si
   encuentra el otro repositorio al lado, o donde diga `TRABAKUTIK_GPS=<ruta>`.
10. Actualizar `ULTIMA_ENTRADA` en `src/build.py` y **recolocar a mano** la
    tarjeta entre las seis primeras, que van alternando bici y senderismo.

### Detalles que se olvidan

- **El perfil de alturas** tiene convención fija: 161 muestras,
  `x = k*1000/160`, `y = 285 − (ele−min)/(max−min)*270`, `viewBox 0 0 1000 300`,
  y **dos** caminos (el relleno y la línea).
- El `"name"` del JSON-LD **se queda en castellano** en las páginas en euskera.
  Es así en 69 de las 70; no lo «arregles».
- `translate()` solo se aplica al **tail**. Toda clave del diccionario de una
  página tiene que aparecer en su tail. En el head solo van títulos,
  descripciones y las sustituciones de hreflang y locale.

---

## 5. Las fotos

- Los originales viven en `img/orig/`. **La única excepción es el original del
  `og:image`, que se queda en `img/`.** Si el `og:image` apunta a una foto que
  solo está en `img/orig/`, dará 404. Ya pasó una vez.
- `scripts/optimize_images.py` lleva un registro sha256 en `img/.optimized.json`
  y aplica `ImageOps.exif_transpose` antes de nada.
- **`scripts/make_wide_variants.py` se salta los archivos que ya existen.** Por
  eso una variante `-800` vieja nunca se refresca sola. Nueve fotos salieron
  publicadas tumbadas por esto: los originales estaban derechos, pero las
  `-800` se habían generado antes de enderezar los originales. Si una foto sale
  girada, **borra la variante y vuelve a generarla**.
- `scripts/make_card_thumbs.py` solo genera tarjetas de las fotos que la
  portada referencia.

---

## 6. El navegador (`nuevo.html`)

Es una sola página con todo el JavaScript en línea, **envuelto en una IIFE**:
no hay nada global. Si quieres sondearlo desde Playwright no puedes llamar a
sus funciones; tienes que extraerlas o inyectar un enganche.

Es solo página: **se publica sin compilar APK**.

### Lo que se ha hecho estos días

- Pitidos: 4 agudos al salirse de ruta, 2 en los giros, avisos a tres fases.
  Las distancias dependen de la velocidad: largo `min(90,max(25,v*9))`, corto
  `min(30,max(8,v*3))`.
- Tarjeta de giro grande con la flecha dibujada al ángulo real
  (`flechaGiro(deg,dir,tam,grosor)`). **El signo va dentro de `a`; no vuelvas a
  multiplicar por `dir`.**
- Sentido de la ruta decidido por el **avance sobre la ruta**
  (`decideSentido`, 30 m netos), no comparando rumbos. Lo de los rumbos daba
  ocho falsos «AL REVÉS» en 3 km.
- Brújula, distancia hecha y que falta, pausa y reanudación, confirmación antes
  de terminar y aviso de cortes en la grabación.
- **Mapa orientado al rumbo** (lo último). Ver abajo.

### El mapa orientado al rumbo: cómo funciona y qué no tocar

Leaflet 1.9 **no sabe girar el mapa**. Se gira un contenedor, `#mapRot`, por
CSS. Hay tres cosas delicadas:

1. **El tamaño del contenedor tiene que ser un cuadrado del lado de la
   diagonal** de lo que se ve. Girado un ángulo cualquiera, lo visible ocupa
   `W·|cos| + H·|sin|`, y en el peor ángulo eso es la diagonal. Si te quedas
   corto salen triángulos vacíos en las esquinas **solo a ciertos ángulos** (a
   0° y 90° se ve bien, y por eso cuesta detectarlo). Lo calcula
   `dimensionaMapa()` y lo rehace con un `ResizeObserver`.
2. **No vale parchear `L.DomEvent.getMousePosition`.** Leaflet viene empaquetado
   de módulos ES y por dentro llama a la función local del módulo, no a la del
   objeto que exporta. El parche ahí no lo ve nadie: medido, **465 m de error**
   al tocar con el mapa girado, mientras una sonda directa decía que estaba
   perfecto. Lo que hay que parchear es
   **`L.Map.prototype.mouseEventToContainerPoint`**, que sí se llama como
   método y por el que pasan el clic, el pellizco y la detección de líneas
   sobre el canvas. Medido después: 0,87 m girado y 0,87 m sin girar.
3. **Arrastrar es la excepción.** Leaflet calcula el arrastre con restas de
   coordenadas de pantalla directas, sin pasar por ese método. Por eso al
   empezar a arrastrar el mapa vuelve **de golpe** al norte. No es un descuido:
   es la solución.

Reglas de cuándo gira, pensadas para que no se vuelva loco:

- **Sobre la ruta el rumbo no sale del GPS**, sale de la geometría del camino
  corregida por el sentido en que se hace. Eso es geométrico y no puede dar
  vueltas.
- **Fuera de la ruta** solo se hace caso al GPS por encima de **7 km/h**, el
  mismo umbral que usa Komoot. Por debajo se mantiene el último rumbo bueno.
- **El primer rumbo de todos va aparte del umbral.** Sin eso, recién cargada la
  página y parado fuera de ruta no había ningún rumbo que aplicar y el botón
  solo cambiaba de color.
- Zona muerta de 4° para que no tiemble.
- En modo «Crear» no gira nunca.

**Limitación conocida y sin solución con este mapa:** al girar teselas de
imagen, los nombres de los pueblos y las carreteras salen tumbados. Komoot y
Wikiloc no lo sufren porque usan mapas vectoriales que vuelven a dibujar el
texto derecho. Aquí no se puede sin cambiar de tipo de mapa.

### Los mandos de la derecha

Cada uno se enciende del color de lo que manda: **naranja** las otras rutas (el
color de la leyenda), **azul** seguir mi posición (el del punto azul), **cian**
el rumbo, que además cambia el dibujo a una «N» cuando está en norte fijo.

**El rojo está reservado para la grabación** en esta pantalla. No lo uses para
otra cosa o de reojo y en marcha se lee «estoy grabando».

Hay un `.tools button{background:…!important}` **sin comentario** que clava los
cinco botones en gris. No se ha quitado porque no consta de qué se defendía; se
gana por especificidad. Si necesitas colorear uno, usa un selector con
identificador y `!important`.

---

## 7. La app Android

- **No hay SDK de Android en el contenedor.** El APK lo compila únicamente
  `.github/workflows/android-apk.yml`, que se dispara al tocar `android/**`. El
  artefacto se llama `TrabakutikGPS-APK` y caduca a los 30 días.
- La versión está en una sola línea: `android/app/build.gradle.kts`. Hoy es la
  **3.3** (`versionCode 33`).
- El servicio manda una posición cada 1,5 s
  (`requestLocationUpdates(GPS_PROVIDER, 1500, 2, …)`).
- El puente con la página es `getPosition()`, más `setSentido(int)`,
  `pauseRecording()` y `resumeRecording()`.
- La pestaña Web recarga si lleva más de 10 minutos cargada; el navegador va
  con `LOAD_NO_CACHE`.
- El zoom a pellizco está encendido **solo en la pestaña Web**: el navegador
  tiene su propio pellizco de Leaflet sobre el mapa.

**Importante:** cambiar `nuevo.html` NO necesita APK. Solo necesitan APK los
cambios dentro de `android/`.

---

## 8. Trampas en las que ya se ha caído

Vale la pena leerlas: todas costaron tiempo.

- **Una sonda que miente es peor que no probar.** Pasó dos veces: una prueba
  que llamaba a la función parcheada «desde fuera» daba perfecto mientras el
  uso real fallaba por 465 m; y un contador de cortes de grabación que
  alimentaba posiciones cada 8 ms de reloj real y contaba 193 cortes donde
  había 1. **Haz siempre el control negativo:** rompe el código a propósito y
  comprueba que tu prueba lo detecta. Si no lo detecta, la prueba no vale.
- **GitHub Pages manda `cache-control: max-age=600`** y no se puede cambiar.
  Diez minutos para ver un cambio es normal. No lo persigas.
- Alguna vez el despliegue de Pages se queda colgado `in_progress` 20 minutos
  cuando lo normal son 2. Un commit vacío cancela el atascado y arranca otro.
- **No dejes `main` en rojo.** Si una comprobación falla por algo que ya sabías
  que iba a fallar (por ejemplo un KML que aún no existe), arréglalo en el
  mismo empujón, no «luego».
- `#app` usa `height:100dvh`. **Hace falta `height:100vh` antes** como
  respaldo: en un motor anterior a diciembre de 2022 el mapa se queda sin
  altura y desaparece.
- `watchPosition` no debe borrar la vigilancia ante cualquier error, solo ante
  el de permiso denegado (`err.code===1`). Si no, un hueco de GPS bajo los
  árboles mata el GPS para el resto de la salida.
- Nada de `alert()` en bucle mientras se circula.
- Cuidado con `.at(-1)`: se sustituyeron once por compatibilidad.
- En CSS, `.info span` y `.info b` ponen `display:block` y ganan a los
  selectores por clase. Usa identificadores.
- `pkill -f "un patrón"` puede matar su propio intérprete si el patrón aparece
  en su línea de comando. No lo metas en la misma orden que algo importante.

---

## 9. Lo que queda pendiente

**De la web**

- El **terreno de la ruta `lejarreta` está vacío a propósito**. Hay una
  propuesta sacada del propio texto del autor: «Raíces y hojas». Él decide.
- Le quedan por revisar, de `lejarreta`: los **diez pies de foto**, los
  **cuatro nombres de waypoint** (Aparkalekua, Eremu erraza, Eremu
  aurreratuagoa, Hartu behar ez den desbideratzea) y el **párrafo del desvío
  del km 3,2** en euskera. Los tradujo el asistente, no él.
- 13 originales de `zaldutrail` están en `img/` en vez de en `img/orig/`.
- Las cabeceras de las rutas siguen poniendo «Mallabia · Bizkaia» con el punto.
- Rama sin fusionar: `codex/gps-installable-review-20261031`.
- `rutas.json` no entra en el workflow de sincronización automática.

**Del navegador**

- Pasos 18 y 19 del documento de investigación del autor: guardar en «mis
  rutas» con confirmaciones, y distinguir exportar de compartir.
- Del repaso de la app, ofrecido y nunca hecho: firma de publicación, envoltorio
  de Gradle, entrada y salida de archivos en el hilo principal, exposición del
  puente JavaScript, y que el botón «Navegar esta ruta» abra la app de un toque
  y siga el tema claro.

---

## 10. Cómo pedir las cosas

Lo que mejor ha funcionado:

- **Di lo que quieres conseguir, no cómo hacerlo.** «Que el mapa vaya en la
  dirección que voy» dio mejor resultado que describir una solución técnica.
- **Si algo no se ve, di exactamente qué ves.** Una foto de la pantalla vale
  más que una descripción. El fallo de las esquinas vacías se encontró por una
  captura.
- **Exige que te enseñen los números.** «Funciona» no es una comprobación.
  «0,87 m girado y 0,87 m sin girar» sí lo es.
- **Desconfía de la primera explicación.** En este proyecto, varias veces la
  causa real no era la obvia.

### Advertencia sobre otros asistentes

Un asistente que no pueda ejecutar comandos ni abrir un navegador **no puede
comprobar nada de lo que dice**. Puede escribir el código, pero no puede
afirmar que funciona. Si te da algo, pídele que te diga **cómo comprobarlo tú**,
y no lo subas a `main` sin pasar al menos:

```bash
python3 src/i18n/make_eu.py && python3 src/build.py
python3 scripts/check_site.py
python3 scripts/verify_route_consistency.py
```

Y en el navegador, antes de subir `nuevo.html`, comprobar que el JavaScript al
menos se analiza sin errores de sintaxis: un error de sintaxis mata el archivo
entero y la página se queda muerta sin avisar.
