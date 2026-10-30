# Navegador Trabakutik — vuelta al inicio y asistencia

Estado: especificación de diseño para la PR #459. **No hay todavía un motor de retorno automático implementado ni verificado.**

## Objetivo
Desde una ruta abierta y con GPS autorizado, botón «Volver al inicio» que compare:
1. Volver exactamente sobre el propio recorrido realizado (si hay historial GPS fiable) o sobre el GPX en sentido inverso hasta la salida.
2. Continuar por el recorrido previsto hasta la salida, si el track es circular y es verificable.
3. Rutas alternativas formadas por tramos existentes de tracks de Trabakutik, con puntos de unión topológicamente verificados.

No enviar al usuario a una línea recta entre dos tracks, una propiedad privada, un vado o un cruce sin continuidad comprobada. Una coincidencia geométrica no garantiza un camino transitable.

## Fuente de datos existente
- `data/trailhead.json` contiene tracks de varias rutas con enlaces a sus fichas.
- `data/<ruta>.json` incluye puntos [lat, lon, altitud] de la ruta.
- `src/<ruta>.gpx` conserva el trazado original.
- `data/fuentes.json` conserva fuentes documentadas.
- Hay service worker y mapas Leaflet locales; las teselas externas OSM/CyclOSM/IGN **no pueden precargarse**. El track puede mostrarse sin fondo cuando se pierda la red.

## Algoritmo propuesto, NO integrado
- Construir un grafo de tramos: normalizar nodos de cruces reales, cada arista conserva GPX de origen, longitud, sentido conocido, desnivel aproximado, clase de uso (a pie / e-bike) y estado de validación.
- Empalmes automáticos únicamente entre segmentos que comparten geometría próxima *y* continuidad de camino contrastada; si hay duda, marcar unión «no verificada», excluirla del enrutado público.
- Poner la posición del GPS sobre un tramo con incertidumbre según la precisión recibida, evitar saltos de tramo en caminos paralelos, e identificar la salida real del GPX.
- Calcular candidatos con Dijkstra/A* sobre aristas verificadas; buscar trayectos alternativos y comparar con la vuelta inversa del mismo GPX.
- Impedir que la ruta de vuelta use un tramo cuyo GPX pudiera pasar por el entorno privado restringido documentado en AGENTS.md.
- Mostrar diferencias: kilómetros, ascenso restante estimado, fuentes documentadas, tramos de bici técnicamente complicados si constan, número y título de rutas de origen; sin etiquetas «seguro» sin evaluación.
- Evitar ahorro engañoso: distancia sobre el grafo, no distancia en línea recta; indicar la fuente de la estimación de subida.
- Si no hay enlace validado, decir «No hay atajo comprobado» y ofrecer vuelta por el track original.
- Evitar recomendaciones automáticas por carreteras generales, propiedades cerradas y puntos inaccesibles; los tracks históricos no garantizan condiciones actuales.
- **Exigir revisión sobre el terreno** de los empalmes antes de anunciar la opción como ruta practicable.

## Interfaz propuesta
Botón prominente «↶ Volver al inicio» en modo navegación. Abre panel inferior:
- «Por donde he venido» — distancia y ascenso estimados.
- «Seguir el circuito» — si empieza y termina en el mismo punto.
- «Otra ruta de Trabakutik» — solo si existen tramos enlazados y validados, con el nombre de sus fichas y previsualización del desvío.
- Confirmación visible antes de cambiar de ruta; conservar el track original y botón «Volver a ruta inicial».
- Al confirmar, dibujar alternativa con color distinto, mostrar punto de enlace, kilometraje y perfil actualizado.
- Aviso explícito «ruta orientativa, comprobar acceso y terreno» incluso con enlaces validados.

## Ayudas de navegación
- Aviso de separación a **más de 15 m**, confirmado con 3 posiciones consecutivas cuya precisión horizontal sea de 15 m o mejor; no ofrecer certeza con GPS impreciso.
- En cruces: mostrar flecha de rumbo *solo si el track permite determinar la continuidad y el dispositivo ofrece rumbo fiable*.
- Próximo ascenso, perfil, altitud y gradiente suavizado (no pendiente a partir de 2 puntos con ruido).
- Indicadores GPS / sin red / mapa base no disponible y botón de reencuadre.
- Acceso a fuentes y lugares existentes en datos documentados; no crear puntos de agua inventados.
- Marcador de último punto fiable, y opción manual para compartir ubicación actual usando herramientas del móvil (requiere interacción y permisos).
- Pausar, reanudar y finalizar con controles grandes y accesibles. No presuponer funcionamiento con pantalla bloqueada.
- Nunca bloquear el mapa si no hay atajo.

## Pruebas exigidas antes de lanzamiento
- Comparar alternativas con los GPX reales, intersecciones falsas (pasos por distinto nivel), tracks paralelos y bucles.
- Evaluar en rutas largas, ida y vuelta, circulares, cruces en X, trazados incompletos y tracks GPX sin altitud.
- Simular errores de GPS de 5, 15, 30, 60 metros, desconexión de red y volver al recorrido.
- Test de móvil con sol, guantes, orientación y bajo consumo, castellano/euskera, lector de pantalla.
- Ejecutar `python3 src/i18n/make_eu.py`, `python3 src/build.py`, `python3 scripts/check_site.py`, `node scripts/test_ui.cjs` y `python3 .claude/skills/run-rutas-mallabia/driver.py verifica`; inspección visual.
- No fusionar en main sin revisión.

## Límite de seguridad
El navegador web depende de que la pantalla/sistema permitan seguir recibiendo ubicación. No es un sustituto de un GPS dedicado ni un mecanismo de rescate. Los cálculos se deben etiquetar como estimaciones, nunca certezas.
