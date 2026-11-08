# AGENTS.md — léeme antes de tocar nada

Sitio de rutas de montaña y bicicleta eléctrica por Mallabia (Bizkaia),
bilingüe castellano/euskera, publicado en <https://trabakutik.com> desde la
raíz de este repositorio con GitHub Pages. 61 rutas. HTML escrito a mano,
scripts de Python con la biblioteca estándar, nada de frameworks.

**La documentación de verdad son dos ficheros de la raíz. Léelos antes de
empezar, enteros:**

- **`GUIA.md`** — cómo se construye, cómo se verifica, cómo se mete una ruta
  nueva paso a paso, y qué herramienta sirve para seguir.
- **`CLAUDE.md`** — el detalle: decisiones tomadas y cerradas, trampas
  conocidas, por qué cada cosa está como está.

Lo de abajo es solo el mínimo para no romper nada en los primeros cinco
minutos.

## Las dos órdenes, siempre y en este orden

```
python3 src/i18n/make_eu.py    # regenera las páginas en euskera
python3 src/build.py           # monta el sitio entero en la raíz
```

`make_eu.py` **se niega a funcionar** si una clave de traducción ya no coincide
letra por letra con el texto en castellano. No es un fallo: es el aviso de que
has cambiado algo en castellano y falta cambiarlo en `src/i18n/eu.py`. Es la
trampa en la que cae todo el que llega nuevo.

## Verificar antes de publicar

```
python3 scripts/check_site.py                                  # 26.451 comprobaciones
node scripts/test_ui.cjs                                       # 14 pruebas del JS
python3 .claude/skills/run-rutas-mallabia/driver.py verifica    # 8 en navegador
```

La tercera necesita Chromium y Playwright. Si tu entorno tiene la red cortada
y no puedes pasarla, **dilo**: te quedas sin ver el mapa, los filtros, los
temas, el modo sin conexión, el visor y el aviso. Sin eso, no toques
`src/js/`.

## Cuatro reglas que no se saltan

1. **Se edita `src/`, nunca los `.html` de la raíz.** Los de la raíz los
   genera `build.py` y se sobrescriben.
2. **Nunca inventar un dato de una ruta** — distancias, desniveles, tiempos,
   fuentes de agua, nombres de sitios. Esto documenta rutas pisadas de verdad.
   Lo que no se sepa, se pregunta. Y avisa siempre de lo que falte o no cuadre,
   aunque nadie lo haya preguntado.
3. **El texto de las rutas lo escribe el autor.** Va casi literal: negritas y
   enlaces, nada más. Si algo parece mejorable, se dice y decide él.
4. **Un GPX no puede empezar, acabar ni pasar por delante de la casa del
   autor.** Siempre por la BI-633. Los márgenes están en
   `scripts/.punto-privado.json`, que no está en git porque este repositorio
   es público.

Y una que no es una regla sino un aviso: **unos metros de diferencia no son un
error.** Un GPS tiene error de hasta 15 m. Si una cima aparece con 795, 791 y
783 m en tres sitios, es el mismo monte. Lo que sí son fallos son los datos que
contradicen la realidad.
