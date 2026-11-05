# Estado de la ruta Trabakua–Lekeitio — 5 de noviembre de 2026

Trabajo en la rama `ruta-trabakua-lekeitio`, PR #461. Sigue siendo un borrador; no hay ficha construida ni publicación.

## Material recuperado

- Textos completos ES/EU: `docs/borradores/lekeitio.es.md` y `lekeitio.eu.md`. Leídos de nuevo, sin modificarlos.
- GPX definitivo aportado de nuevo el 5 de noviembre: `gerea-zapola-urregarai-bedartzandi-lekeitio.gpx`. Analizado localmente: 25.984 puntos GPS, 32,743 km por suma geodésica de segmentos, un track, datos de elevación en todos los puntos y sin saltos consecutivos superiores a 50 m. Desnivel positivo +1.533 m confirmado por el autor (no calculado sumando el ruido del GPX). El archivo binario aún NO está en el repositorio; la revisión local no equivale a subirlo. Sustituye al anterior.
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

Actualización: existe un entorno local para analizar el GPX recibido y se ha comprobado su lectura y continuidad de puntos. El acceso de red Git al repositorio desde ese entorno falla por resolución DNS, mientras que el conector GitHub sí permite editar textos. Todavía no se han incorporado el GPX binario ni las fotografías, ni se han ejecutado los generadores y pruebas sobre una copia completa del repositorio. No se ha publicado.

No confundir localizar los originales con incorporarlos al repositorio. No marcar el PR como listo ni fusionarlo hasta completar la ficha y las comprobaciones.

## Trabajo pendiente

1. Incorporar el GPX definitivo recibido y recuperar/incorporar las 22 fotografías binarias. No utilizar el GPX anterior.
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

## Actualización: selección definitiva y material preparado (5 noviembre)

- El autor ha elegido explícitamente como **portada** la foto original **`1000125894.jpg`** (puente de Lekeitio). Sustituye la propuesta anterior `1000125736.jpg`. No duplicarla en la galería.
- Ha reenviado **25 fotografías originales**, registradas por nombres reales y orden de envío en tres notas `lekeitio-fotos-recibidas-05-11*.md`. Portada primera, 24 restantes en galería.
- El GPX definitivo se ha abierto correctamente: **25.984 puntos**, longitud aproximada **32,74 km**. Desnivel **+1.533 m** confirmado por el autor.
- Se ha generado en el entorno local un paquete ZIP verificando su CRC: contiene GPX, KML de todos los puntos, JPG originales y versiones web 800 px / completas WebP y JPG. **Este ZIP NO está en el repositorio GitHub**, solo se ha entregado como archivo descargable en la conversación. No publicar ni fusionar suponiendo que está incorporado.
- Requisito explícito del autor: **mapa y perfil en ficha, descarga del GPX, enlace Navegar y visibilidad en Trabakutik GPS**, incluida entrada ES/EU en `data/rutas.json` y track en `data/trailhead.json` a través de generadores y sincronización.
- **Bloqueante:** el entorno local no resuelve github.com por DNS para clonar/push; el conector GitHub funciona para texto, pero no transmite directamente los archivos binarios adjuntos. También falta validar el GPX contra los márgenes privados del autor antes de publicar. No se ha publicado ni verificado la ficha.
