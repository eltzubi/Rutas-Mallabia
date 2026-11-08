# Rutas Mallabia — trabakutik.com

Sitio de rutas de senderismo y e-bike por Mallabia (Bizkaia) y alrededores,
documentadas sobre el terreno con datos reales: tracks GPX grabados y fotos
propias. En castellano y euskera.

Publicado en **https://trabakutik.com/** con GitHub Pages, desde la rama `main`
y sirviendo la raíz del repositorio.

## Cómo está hecho

Sitio estático: HTML, CSS y JavaScript escritos a mano, montados por unos
scripts de Python (solo biblioteca estándar). Sin framework, sin servidor y sin
base de datos. Cada ruta es una página de verdad (`urko.html`, `kalamua.html`…),
y hay 61.

**Los `.html`, `.css` y `.js` de la raíz son generados: no se editan a mano.**
Se editan los fuentes de `src/` y se vuelve a construir:

```
python3 src/i18n/make_eu.py    # regenera el euskera desde src/i18n/eu.py
python3 src/build.py           # monta el sitio en la raíz
python3 scripts/check_site.py  # 26.451 comprobaciones sobre lo construido
```

Y antes de publicar, la verificación entera, que abre el sitio en un navegador
de verdad:

```
python3 .claude/skills/run-rutas-mallabia/driver.py verifica
```

## Para seguir trabajando

**[GUIA.md](GUIA.md)** lo cuenta todo: la estructura, las herramientas de
`scripts/`, cómo se mete una ruta nueva paso a paso, las reglas de contenido
—que son lo importante— y lo que está decidido y no se vuelve a plantear.

`CLAUDE.md` es lo mismo con más detalle técnico, para un asistente de código.
