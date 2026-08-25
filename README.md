# Rutas Mallabia

Sitio de rutas del pueblo de Mallabia (Bizkaia) — BTT y senderismo, documentadas sobre el terreno con datos reales (GPX, fotos propias).

Publicado en: https://trabakutik.com/

## Cómo está hecho

`index.html` (en la raíz, lo que sirve GitHub Pages) es un único archivo autocontenido: dos páginas completas (inicio y la ficha de la ruta Trabakua) embebidas dentro, con navegación interna entre ellas vía `postMessage` — no son enlaces normales entre páginas.

El código fuente editable de verdad está en `src/`:

- `mallabia_head.html` / `mallabia_tail.html` — página de inicio
- `trabakua_head.html` / `trabakua_tail.html` — ficha de la ruta Trabakua
- `fonts/inline_fonts.css` — tipografías (Fraunces, Karla, IBM Plex Mono) auto-alojadas como `@font-face` en base64, compartidas por ambas páginas
- `trabakua.gpx` — track GPX real del que salen la distancia, el desnivel y el perfil de elevación
- `build.py` — junta todo lo anterior y genera `index.html`

**Para retomar el trabajo en una sesión nueva**: clona este repo, y para reconstruir el sitio tras editar algo en `src/`, ejecuta:

```
python3 src/build.py
```

Eso regenera `index.html` en la raíz. Hay que confirmarlo con git y hacer push para que se publique.

### Aviso importante para quien edite esto (humano o IA)

`src/trabakua_tail.html`, `src/mallabia_tail.html` y `src/fonts/inline_fonts.css` contienen imágenes y tipografías embebidas en base64 — líneas de cientos de miles de caracteres. **No los abras con un editor de texto normal ni los leas enteros** con una IA (se satura el contexto o el propio editor). Para inspeccionarlos, usar un script (Python, por ejemplo) que filtre líneas por longitud (`if len(line) < 300`) para encontrar solo las líneas de código de verdad, y editar por reemplazo de texto (no a mano) cuando el archivo contiene base64.

Antes de dar por bueno un cambio de maquetación (CSS, tamaños, mapas embebidos), verificar con Playwright en varios anchos de pantalla (320, 390, 768, 1280px como mínimo) que no hay desbordamiento horizontal, y revisar capturas de pantalla — no solo el código — antes de publicar.
