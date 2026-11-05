# Estado de la ruta Trabakua–Lekeitio — 5 de noviembre de 2026

Trabajo en la rama `ruta-trabakua-lekeitio`, PR #461. Sigue siendo un borrador; no hay ficha construida ni publicación.

## Material recuperado

- Textos completos ES/EU: `docs/borradores/lekeitio.es.md` y `lekeitio.eu.md`. Leídos de nuevo, sin modificarlos.
- GPX definitivo localizado entre los adjuntos guardados: `gerea-zapola-urregarai-bedartzandi-lekeitio.gpx`, 3.372.538 bytes. Todavía no se ha incorporado ni analizado. Sustituye al GPX anterior.
- Localizadas las 22 fotografías originales entre los adjuntos guardados; no es necesario volver a solicitarlas mientras sigan disponibles.
- Las primeras veinte tienen descripciones ES/EU en `lekeitio-fotos.md` y `lekeitio-fotos-11-20.md`.
- Las dos últimas, `1000125909.jpg` y `1000125913.jpg`, faltaban en las notas del PR. Ambas existen. Pendiente verlas para escribir sus textos alternativos y confirmar el orden de este último par.
- Portada prevista en las notas anteriores: `1000125736.jpg`. Conservar la portada sola antes del texto de entrada, sin duplicarla en la galería.

## Inventario completo

Se conserva el orden documentado de las primeras veinte. La numeración del último par es provisional hasta confirmar su orden visual en el envío original.

| Posición | Original | Estado |
|---|---|---|
| 1 | 1000125736.jpg | Orden documentado en las notas anteriores |
| 2 | 1000125737.jpg | Orden documentado en las notas anteriores |
| 3 | 1000125742.jpg | Orden documentado en las notas anteriores |
| 4 | 1000125757.jpg | Orden documentado en las notas anteriores |
| 5 | 1000125762.jpg | Orden documentado en las notas anteriores |
| 6 | 1000125767.jpg | Orden documentado en las notas anteriores |
| 7 | 1000125768.jpg | Orden documentado en las notas anteriores |
| 8 | 1000125769.jpg | Orden documentado en las notas anteriores |
| 9 | 1000125784.jpg | Orden documentado en las notas anteriores |
| 10 | 1000125788.jpg | Orden documentado en las notas anteriores |
| 11 | 1000125808.jpg | Orden documentado en las notas anteriores |
| 12 | 1000125811.jpg | Orden documentado en las notas anteriores |
| 13 | 1000125816.jpg | Orden documentado en las notas anteriores |
| 14 | 1000125822.jpg | Orden documentado en las notas anteriores |
| 15 | 1000125823.jpg | Orden documentado en las notas anteriores |
| 16 | 1000125827.jpg | Orden documentado en las notas anteriores |
| 17 | 1000125855.jpg | Orden documentado en las notas anteriores |
| 18 | 1000125859.jpg | Orden documentado en las notas anteriores |
| 19 | 1000125865.jpg | Orden documentado en las notas anteriores |
| 20 | 1000125874.jpg | Orden documentado en las notas anteriores |
| 21 | 1000125909.jpg | Último par; confirmar orden y alt ES/EU |
| 22 | 1000125913.jpg | Último par; confirmar orden y alt ES/EU |

## Comprobación del estado real

Leídos `AGENTS.md`, `GUIA.md` y `CLAUDE.md`. El PR contenía cuatro documentos de borrador, sin GPX, imágenes ni fuentes de ficha. Los textos conservan la advertencia sobre la subida directa a Santa Eufemia y el atajo anterior a Iturreta.

La sesión no dispone de un entorno de ejecución: la llamada de prueba devuelve «No usable execution environment is available». Esto impide procesar las fotos, analizar el GPX, ejecutar Python/Node, construir el sitio y abrir el navegador de verificación. No se ha ejecutado ninguna prueba ni se ha publicado.

No confundir localizar los originales con incorporarlos al repositorio. No marcar el PR como listo ni fusionarlo hasta completar la ficha y las comprobaciones.

## Trabajo pendiente

1. Recuperar los archivos originales por sus nombres del inventario y el GPX definitivo. No utilizar el GPX anterior.
2. Obtener distancia, alturas y perfil del GPX. El desnivel acumulado y los tiempos necesitan la fuente del autor; no deducir el acumulado sumando elevaciones en bruto.
3. Montar `src/lekeitio_head.html` y `src/lekeitio_tail.html` siguiendo una ficha completa como `arteta`, sin reescribir los textos guardados.
4. Conservar mapa, perfil con puntos numerados, descargas, formulario de incidencias, pie, botón de volver arriba y scripts. Comparar estructura con la ficha de referencia.
5. Incorporar traducciones a `src/i18n/eu.py` y registrar la ruta en `src/build.py` y `src/i18n/make_eu.py`.
6. Procesar fotos y variantes con los scripts existentes; mantener una portada y 21 fotos de galería.
7. Añadir tarjeta a la portada respetando la alternancia de actividades entre las primeras seis y actualizar `ULTIMA_ENTRADA`.
8. Generar datos de mapa, perfil, KML, ZIP, lugares de búsqueda y miniatura del mapa.
9. Ejecutar `make_eu.py` antes de `build.py`, después `check_site.py`, `test_ui.cjs`, `driver.py verifica` y la revisión completa de la ficha en navegador.
10. Comprobar la sincronización de `data/trailhead.json` y `data/rutas.json` con el GPS y, tras publicar, las comprobaciones y el despliegue de Pages.

Estas notas permiten retomar el trabajo sin depender únicamente del historial del chat. No son una copia binaria de los adjuntos ni una garantía de conservación de la conversación.
