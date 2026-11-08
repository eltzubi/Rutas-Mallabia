# Estado de la ruta Garai – Urdaixa — 8 de noviembre de 2026

Rama `ruta/garai-urdaixa`. Borrador: NO hay ficha construida ni publicacion, y
`main` no se ha tocado.

## Lo que ya esta hecho

- `src/garaiurdaixa.gpx`: el GPX del autor, grabado el 8 de noviembre de 2026
  de 07:19 a 09:02 con Wikiloc. 5.897 puntos, un solo tramo, todos con altura.
- `data/garaiurdaixa.json`: trazado simplificado (405 puntos) y marcador de
  salida en el aparcamiento de Garai. Hecho con `make_map_data.py`.
- `data/alturas.json` rehecho.
- Los textos del autor, en castellano y en euskera, en los dos ficheros de al
  lado. El euskera lo escribio el, asi que manda su redaccion.

## Datos medidos sobre el GPX

| | |
|---|---|
| distancia | 7,14 km (7,03 tras simplificar) |
| altura minima | 247 m |
| altura maxima | 454 m |
| desnivel medido aqui | +225 / -222 m |
| cierra el circulo a | 30 m |
| duracion de la grabacion | 1 h 43 min |

## Lo que FALTA, y por que no se puede publicar todavia

1. **Una foto, por lo menos.** `check_site.py` exige que toda ficha de ruta
   lleve al menos un `<picture>`, y la tarjeta de la portada necesita su
   imagen. Sin foto, el sitio no pasa las comprobaciones.
2. **El desnivel acumulado de Wikiloc.** Regla del sitio: esa cifra no sale
   del GPX, sale de la fuente de la ruta. Los +225 / -222 de arriba son una
   medida propia y no valen para la ficha.
3. **Los puntos numerados**: cuales quiere el autor y como se llaman. La ruta
   hermana, `garaikanala`, lleva tres. Del texto saldrian la balsa, el
   nacedero, la presa y la ermita de Urdaixa, pero el autor decide.
4. Esfuerzo y Terreno: los pone el autor; `Terreno` esta vacio a proposito en
   todo el sitio y solo lo sabe quien ha pisado la ruta.

## Cuando llegue eso

Queda la cadena de siempre: perfil de alturas, `_head.html` y `_tail.html`
copiando la estructura de `garaikanala`, el euskera en `eu.py`, `PAGES` en
`build.py` y en `make_eu.py`, la tarjeta en `mallabia_tail.html` con
`ULTIMA_ENTRADA`, la entrada de `trailhead.json`, y luego `make_places.py`,
`make_card_maps.py`, `make_kml.py`, `bundle_gpx.py`, `make_eu.py`,
`build.py`, `check_site.py` y `driver.py verifica`.
