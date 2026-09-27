# DESIGN.md — Trabakutik

Sistema de diseño de [trabakutik.com](https://trabakutik.com/), un sitio de rutas de
senderismo y BTT por el entorno de Mallabia (Bizkaia).

Este documento describe cómo se ve el sitio para que cualquiera —persona o agente— pueda
añadir una página nueva que encaje con las que ya hay. Todos los valores salen de
`src/css/base.css`, `src/css/home.css` y `src/css/route.css`; si cambias el CSS, cambia
esto también.

---

## 1. Tema visual y atmósfera

Un cuaderno de campo mirado de noche. El fondo es casi negro (`#0D0D0F`) y sobre él las
cifras —los kilómetros, el desnivel, la altitud— brillan en turquesa con un halo suave,
como la pantalla de un GPS en la oscuridad. Todo lo que es dato se comporta como un
instrumento de medición: monoespaciado, en mayúsculas, alineado en columnas. Todo lo que
es nombre de sitio se comporta como lo contrario: una serif de contraste alto con la
segunda mitad en cursiva, más cercana a la portada de un libro que a una interfaz.

Esa tensión entre las dos cosas es la identidad del sitio. No hay degradados, ni sombras
difusas grises, ni relleno decorativo: el brillo siempre sale del propio color del texto
(`currentColor`), no de una capa aparte, y solo lo llevan las cifras y la línea del perfil
de altura. Las fotos son del autor, están tomadas sobre el terreno y ocupan el ancho
completo de su hueco, con contraste y saturación subidos para que aguanten sobre el fondo
oscuro.

El oscuro es la identidad, no una opción: el claro es el que se pide expresamente, con
`data-theme="light"`. Un comentario del propio CSS lo dice así — *"Sendero de noche: dark
is the identity now, light is the opt-out"*.

**Rasgos que lo definen:**
- Fondo casi negro con acentos turquesa y lima, sin más color que esos dos
- Tres tipografías con papeles que no se mezclan nunca: mono para datos, serif para
  nombres, sans para leer
- Las cifras llevan halo (`text-shadow:0 0 14px currentColor`); el resto del texto no
- Cada hueco de imagen reserva su espacio con `aspect-ratio` antes de que cargue la foto
- Bordes de 1px con blanco al 16% de opacidad en vez de sombras para separar superficies
- Píldoras completamente redondeadas (`999px`) para lo interactivo, esquinas de 16-20px
  para las tarjetas
- Mayúsculas con mucho tracking (`.1em`-`.13em`) en cabecera y etiquetas

---

## 2. Paleta y papel de cada color

### Tema oscuro (el de por defecto)

| Token | Valor | Para qué |
|---|---|---|
| `--ground` | `#0D0D0F` | Fondo de la página. Casi negro, con una pizca de azul. |
| `--ground-raised` | `#17171A` | Superficies elevadas: tarjetas, `.fact`, modales. |
| `--ink` | `#EAF5E2` | Texto principal. Blanco tirando a verde, nunca blanco puro. |
| `--ink-dim` | `#8FA382` | Texto secundario, etiquetas, cabecera. Verde apagado. |
| `--teal` | `#2FE0F5` | Acento primario: cifras, línea del perfil, CTA, rutas de BTT. |
| `--teal-soft` | `rgba(47,224,245,.14)` | Relleno bajo la línea del perfil de altura. |
| `--violet` | `#A6FF4D` | Acento secundario: senderismo, estado activo, hover. |
| `--violet-soft` | `rgba(166,255,77,.14)` | Su equivalente de relleno. |
| `--line` | `rgba(234,245,226,.16)` | **El separador de todo.** Bordes de 1px en vez de sombras. |
| `--ink-deep` | `#050805` | Texto sobre fondos de acento (sobre turquesa o lima). |
| `--readout-a` / `--readout-b` | `#2FE0F5` / `#A6FF4D` | Las dos cifras grandes del bloque de totales. |

> **Ojo con `--violet`:** el nombre viene de una versión anterior, pero el valor es un
> verde lima (`#A6FF4D`). Es intencionado. No lo "corrijas" a morado.

### Tema claro (`:root[data-theme="light"]`)

No es una inversión: los acentos bajan mucho de luminosidad para que sigan legibles sobre
fondo claro. `--teal` pasa de `#2FE0F5` a `#006E86` y `--violet` de `#A6FF4D` a `#3A6B15`.
El fondo es `#F5F5F3` y la tinta `#16210F`. Si añades un color, defínelo en los dos
bloques.

### Reglas de color

- Turquesa = bici/BTT y datos. Lima = senderismo y estado activo. No se intercambian.
- Nunca uses un color fuera de los tokens. Si hace falta uno nuevo, es que el diseño está
  pidiendo otra cosa.
- El texto sobre un fondo de acento va en `--ink-deep`, nunca en blanco.

---

## 3. Tipografía

Tres familias, servidas desde el propio dominio (`fonts/*.woff2`, `font-display:swap`) y
declaradas en `src/fonts/inline_fonts.css`.

### IBM Plex Mono — los datos y la interfaz
Pesos 500 y 600. Es la que más aparece (45 declaraciones). Se usa para **todo lo que se
mide o se pulsa**: cifras, etiquetas, cabecera, botones, filtros, migas.

- **Cabecera y etiquetas:** 11px, `letter-spacing:.13em`, `text-transform:uppercase`,
  color `--ink-dim`
- **Cifras (`.fact .v`):** 19px, peso 600, `font-variant-numeric:tabular-nums`
  (imprescindible: hace que los números se alineen en columna), con halo
- **Clave de la cifra (`.fact .k`):** 10px, `.07em`, mayúsculas, `--ink-dim`
- **Botones:** 12px, peso 500

### Fraunces — los nombres
Pesos 600 (cursiva) y 600-900 (normal). Solo para títulos y nombres de ruta. Nunca para
texto corrido ni para interfaz.

- **`h1`:** peso 900, `clamp(2.4rem, 9vw, 4.4rem)`, `line-height:.94`,
  `letter-spacing:-.01em`, `text-wrap:balance`
- **El acento:** dentro del `h1`, un `<em>` en cursiva peso 600 y color `--readout-a`.
  Es el gesto de marca del sitio: la primera parte del nombre en romana, la segunda en
  cursiva turquesa. Ej. `<h1>Asuntza<br><em>bira</em></h1>`
- **Nombre de tarjeta:** cursiva peso 700, 17px

### Karla — para leer
Pesos 400-700. El texto corrido de las rutas y las entradillas. 15,5px con
`line-height:1.5`.

### Escala
El sitio vive en tamaños pequeños: 11px y 12px son los más frecuentes, con mucho aire
alrededor. Las cifras (19px) y los títulos son lo único grande. No introduzcas tamaños
intermedios nuevos sin motivo.

---

## 4. Componentes

### Cabecera (`.masthead`)
Fila mono en mayúsculas, 11px, `.1em`, `--ink-dim`, `padding:9px 18px`. A la izquierda el
enlace de vuelta, en el centro `MALLABIA · BIZKAIA`, a la derecha el conmutador de idioma
y el de tema, ambos circulares.

### Dato (`.fact`)
Borde de 1px `--line`, fondo `--ground-raised`, `padding:11px 15px`, `min-width:96px`.
Dentro, la cifra (`.v`) grande con halo y la clave (`.k`) diminuta en mayúsculas debajo.
Se agrupan en rejilla. **Distancia, desnivel y dificultad pesan más** que superficie, tipo
o actividad: son los que deciden si haces la ruta.

### Tarjeta de ruta (`.route-card`)
Columna flex, borde `--line`, `border-radius:16px`, fondo `--ground-raised`,
`overflow:hidden`. Arriba la foto en un hueco `aspect-ratio:16/10`, debajo el nombre en
Fraunces cursiva y las cifras en mono 13px con `tabular-nums`. Al pasar el ratón, la foto
escala a 1.06.

### Botón principal (`.wikiloc-link`)
`inline-flex`, mono 12px peso 500, fondo `--teal`, texto `--ground`, `padding:9px 14px`,
con `gap:7px` para el icono. La variante `.ghost` va sin relleno.

### Perfil de altura
Un SVG hecho a mano a partir del GPX real. La línea lleva
`filter:drop-shadow(0 0 6px var(--teal))` y el relleno de debajo va en `--teal-soft`. Los
puntos numerados (`.elev-marker circle`) llevan su propio halo y se corresponden uno a uno
con los de la leyenda (`.elev-legend-item`), que es de donde `js/map.js` saca las
etiquetas. **Si añades un punto en el perfil, añádelo también en la leyenda y en el JSON.**

---

## 5. Maquetación

- **Anchos:** 820px para el contenido normal, 1100px para lo ancho (portada a partir de
  1024px). Centrado con `margin:auto`.
- **Puntos de ruptura:** 640px y 1024px son los que importan; hay ajustes puntuales por
  debajo de 520/480/420/400px. Diseña primero para móvil.
- **Separación:** por `gap` en flex y grid, no por márgenes sueltos entre hermanos.
- **Nada de desbordamiento horizontal.** Se comprueba a 320, 390, 768 y 1280px.

### Imágenes — la regla que no se salta
Todo hueco de imagen declara su proporción **antes** de que la foto cargue:

| Contenedor | Proporción |
|---|---|
| `.photo-slot` (foto principal de ficha) | `15/7` |
| `.gallery-item` (galería) | `4/3` |
| `.route-card-photo` (tarjeta de portada) | `16/10` |
| `.mini-gallery .gallery-item` | `1/1` |

La `<img>` va dentro con `width:100%; height:100%; object-fit:cover`. Gracias a esto las
fotos no mueven la página al cargar, y por eso los atributos `width`/`height` en el `<img>`
sobran aquí: el hueco ya está reservado.

Las fotos se sirven adaptadas al tamaño de pantalla:

```html
<picture><source srcset="img/x-800.webp 800w, img/x.webp 1600w"
  sizes="(min-width:1024px) 520px, (min-width:768px) 350px, 45vw"
  type="image/webp"><img src="img/x.jpg" alt="..." loading="lazy" decoding="async"></picture>
```

El `sizes` cambia según el contenedor (los de arriba son los de galería); están medidos,
no estimados. Genera la versión de 800px con `python3 scripts/make_wide_variants.py`.

---

## 6. Profundidad

No hay sombras al uso. La separación entre planos se consigue con:

1. **Borde de 1px en `--line`** — el recurso principal
2. **`--ground-raised`** para lo que está por encima del fondo
3. **Halo de color** solo en las cifras y en la línea del perfil, siempre con
   `currentColor` para que funcione en los dos temas:
   - `.fact .v` → `text-shadow:0 0 14px currentColor`
   - `.readout-item .v` → `0 0 18px` (el más intenso, para los totales del sitio)
   - `.feat-facts .fact .v` → `0 0 12px`

Las sombras negras solo aparecen en lo que flota de verdad: modales y visor de fotos.

---

## 7. Qué sí y qué no

**Sí**
- Usar los tokens; definir cualquier color nuevo en los dos temas
- Mono con `tabular-nums` para cualquier número que se compare con otro
- Reservar el hueco de cada imagen con `aspect-ratio`
- Mayúsculas y tracking para etiquetas; Fraunces solo para nombres
- Escribir el texto en castellano en `src/*_tail.html` y su traducción en `src/i18n/eu.py`

**No**
- Colores sueltos fuera de los tokens, ni degradados
- Fraunces en botones, etiquetas o texto corrido
- Halo en texto que no sea una cifra — pierde el sentido y ensucia
- Sombras grises difusas para separar cosas: para eso está `--line`
- Tocar los `.html` de la raíz: son generados, se editan las fuentes de `src/`
- Editar un `*.eu.html`: lo sobrescribe `make_eu.py`

---

## 8. Comportamiento responsive

Móvil primero. El `h1` escala con `clamp(2.4rem, 9vw, 4.4rem)` y el resto de la interfaz
se queda en tamaño fijo: lo que cambia es la disposición, no el tamaño de letra.

- A partir de **640px** el contenido respira más y algunas rejillas pasan a dos columnas
- A partir de **1024px** el contenedor crece a 1100px y la rejilla de tarjetas va a tres
- Por debajo de **520px** se ajustan tamaños puntuales

Cuidado con las líneas mono largas: son de ancho fijo por carácter y no perdonan. La línea
de cifras del hero lleva `white-space:nowrap` y un `clamp` calculado para que quepa en
euskera —que es más largo que el castellano— a 320px. **El euskera es el que marca el
límite**: si un texto cabe en castellano, compruébalo también en euskera.

---

## 9. Guía para el agente

Al construir una página nueva de este sitio:

1. **Parte de una ficha existente**, no del folio en blanco. `arteta_tail.html` es un buen
   patrón. Una ficha lleva, en este orden: cabecera, perfil de altura con marcadores y
   leyenda, eyebrow, `h1` con su `<em>`, `full-name`, foto principal, rejilla de datos,
   nota de datos, texto de la ruta, galería, mapa, descarga de GPX, enlace a Wikiloc,
   "para quién es", enlace de vuelta, footer, botón de subir y visor de fotos.
2. **Compárala con las demás antes de darla por buena.** Una ficha se publicó sin mapa,
   sin footer y sin botón de subir porque solo se revisaba lo que alguien reportaba. Mira
   la página entera contra el patrón, no el último fallo.
3. **No inventes datos.** Distancia, desnivel, altitudes, nombres de sitios y orden de los
   puntos salen del GPX real (`src/<ruta>.gpx`). Si algo no cuadra, dilo; no lo rellenes.
4. **Los dos idiomas van juntos.** Texto en castellano en la fuente, traducción en
   `src/i18n/eu.py`. Después, siempre en este orden:
   ```
   python3 src/i18n/make_eu.py
   python3 src/build.py
   ```
   `make_eu.py` falla a propósito si una traducción se ha quedado desfasada.
5. **Comprueba en navegador**, a 320/390/768/1280px, que no hay desbordamiento y que las
   fotos no mueven la página.

Para el detalle de la arquitectura, el pipeline de datos y las normas de contenido, lee
`CLAUDE.md`.
