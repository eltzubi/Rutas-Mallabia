// One map implementation for every page and both languages.
//
// Orden de carga: en los *_tail.html Leaflet va al final, DETRAS de filters.js,
// app.js y webmcp.js, y este fichero es el ultimo de todos. Estaba al reves, y
// eso ataba toda la interactividad de la web a un CDN ajeno: una hoja de estilos
// dentro del body bloquea el pintado, y un script clasico bloquea el parser, asi
// que los filtros, el cambio de tema y el visor de fotos no despertaban hasta que
// jsdelivr contestaba. Solo este fichero necesita Leaflet: si se vuelve a mover,
// que sea sin poner nada ajeno por delante de lo propio.
//
// The page supplies only what is page- or language-specific, as data
// attributes on the map container:
//   data-map-src      geometry (tracks / start marker / waypoints), from data/
//   data-marker-title tooltip for the start (or parking) marker -- translated
// Numbered waypoint names are read straight from the .elev-legend items
// already rendered on the page, so they are never duplicated here.
(function(){
  var el = document.querySelector('[data-map-src]');
  if (!el) return;
  var isEu = document.documentElement.lang === 'eu';
  var map = null;
  var loading = false;
  var cleanups = [];

  function showUnavailable(retry){
    el.classList.add('map-unavailable');
    el.setAttribute('aria-busy', 'false');
    el.textContent = '';
    var message = document.createElement('p');
    message.setAttribute('role', 'status');
    message.textContent = isEu ?
      'Ezin izan da mapa kargatu. Ibilbideak deskargatzeko estekak erabil ditzakezu.' :
      'No se ha podido cargar el mapa. Puedes usar los enlaces de descarga de las rutas.';
    el.appendChild(message);
    var retryButton = document.createElement('button');
    retryButton.type = 'button';
    retryButton.className = 'map-retry';
    retryButton.textContent = isEu ? 'Saiatu berriro' : 'Reintentar';
    retryButton.addEventListener('click', retry);
    el.appendChild(retryButton);
    var box = el.parentElement;
    if (box) {
      box.classList.remove('is-expanded');
      Array.prototype.forEach.call(box.querySelectorAll('.map-expand-btn, .map-layers'),
        function(b){ b.hidden = true; });
    }
  }

  // Se consulta en cada salto, no una vez al cargar: la preferencia puede
  // cambiar con la sesion abierta.
  function scrollOpts(){
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    return { behavior: reduce ? 'auto' : 'smooth', block: 'start' };
  }

  // Leaflet viene de un CDN externo. Cuando no llega, lo que quedaba era una
  // caja gris vacia sin ninguna explicacion -- y el boton de ampliar seguia
  // funcionando, asi que se podia ampliar la nada a 80vh. Mejor decirlo y
  // retirar los botones que ya no mandan sobre nada.
  if (typeof L === 'undefined') {
    showUnavailable(function(){ window.location.reload(); });
    return;
  }

  // Se pone a true en cuanto el visitante mueve el mapa (zoom o arrastre).
  // A partir de ahi el mapa ya no vuelve solo al encuadre general: la vista
  // es suya. Volver a cerrar el mapa grande la reinicia.
  var userMoved = false;
  var resetView = null;   // lo rellena el bloque del mapa, mas abajo

  var expandBtn = el.parentElement && el.parentElement.querySelector('.map-expand-btn');
  function updateViewportWidth(){
    el.parentElement.style.setProperty('--map-viewport-width', document.documentElement.clientWidth + 'px');
  }
  updateViewportWidth();
  window.addEventListener('resize', updateViewportWidth, { passive: true });
  if (expandBtn) {
    expandBtn.addEventListener('click', function(){
      updateViewportWidth();
      var expanded = el.parentElement.classList.toggle('is-expanded');
      expandBtn.setAttribute('aria-label', expanded ?
        expandBtn.dataset.labelCollapse : expandBtn.dataset.labelExpand);
      expandBtn.classList.toggle('is-active', expanded);
      if (expanded) {
        // El perfil pequeno esta debajo del mapa, asi que lo que se lleva
        // arriba es la caja del mapa: el perfil queda justo a continuacion.
        // Antes estaba encima y habia que subir hasta el, que es lo que ya
        // no hace falta.
        el.parentElement.scrollIntoView(scrollOpts());
      } else if (resetView) {
        // Al reducir el mapa se vuelve a ver todo, que es para lo que sirve
        // la vista pequena; y asi queda una forma clara de reencuadrar.
        userMoved = false;
        resetView();
      }
    });
  }

  // The home page's "Explorar en el mapa" button (js/mallabia_tail.html)
  // jumps straight to an already-expanded map instead of a plain anchor
  // scroll to the small, collapsed default view.
  var exploreLink = document.getElementById('exploreMapLink');
  if (exploreLink && expandBtn) {
    exploreLink.addEventListener('click', function(e){
      e.preventDefault();
      if (el.parentElement.classList.contains('is-expanded')) {
        el.parentElement.scrollIntoView(scrollOpts());
      } else {
        expandBtn.click();
      }
    });
  }

  var css = getComputedStyle(document.documentElement);
  function token(name, fallback){
    return css.getPropertyValue(name).trim() || fallback;
  }
  var COLORS = {
    teal: token('--teal', '#2FE0F5'),
    violet: token('--violet', '#A6FF4D'),
    parking: '#E24C4C'
  };
  var ground = token('--ground', '#0A0F0A');

  // Waypoint labels come from the elevation legend, in the same order.
  // Acotado a la leyenda del mapa: una ficha lleva dos leyendas iguales (la
  // del perfil y la del mapa), asi que buscando en todo el documento salian
  // el doble de items que waypoints y la correspondencia se sostenia de puro
  // milagro -- el dia que las dos dejasen de coincidir, etiquetas cambiadas.
  var legendScope = el.closest('.map-section') || document;
  var wpNames = Array.prototype.map.call(
    legendScope.querySelectorAll('.elev-legend-item'),
    function(item){ return item.textContent.replace(/^\s*\d+\s*/, '').trim(); }
  );

  // Compass direction the route heads out into: bearing from the start
  // point to the point farthest from it (a loop's own "endpoint" isn't
  // meaningful, but its farthest reach is).
  var COMPASS = isEu ?
    ['Ipar', 'Ipar-ekialde', 'Ekialde', 'Hego-ekialde', 'Hego', 'Hego-mendebalde', 'Mendebalde', 'Ipar-mendebalde'] :
    ['Norte', 'Noreste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste'];
  function bearing(a, b) {
    var p1 = a[0] * Math.PI / 180, p2 = b[0] * Math.PI / 180;
    var dl = (b[1] - a[1]) * Math.PI / 180;
    var y = Math.sin(dl) * Math.cos(p2);
    var x = Math.cos(p1) * Math.sin(p2) - Math.sin(p1) * Math.cos(p2) * Math.cos(dl);
    return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
  }
  function directionLabel(points) {
    var start = points[0], far = start, maxD = -1;
    points.forEach(function(pt) {
      var d = Math.pow(pt[0] - start[0], 2) + Math.pow(pt[1] - start[1], 2);
      if (d > maxD) { maxD = d; far = pt; }
    });
    var deg = bearing(start, far);
    return COMPASS[Math.round(deg / 45) % 8];
  }

  // Punto medio por distancia real recorrida (no el punto central del
  // array): en el mapa de conjunto todas las rutas salen de Trabakua, asi
  // que una etiqueta de distancia puesta en el arranque se amontona con las
  // de las demas. A mitad de recorrido ya se han separado casi siempre --
  // comprobado contra las 46 rutas reales: la separacion minima entre la
  // etiqueta de una ruta y la de su vecina mas cercana pasa de 8 m de
  // mediana (en el arranque) a 824 m (en el punto medio).
  function haversineMeters(a, b) {
    var R = 6371000;
    var p1 = a[0] * Math.PI / 180, p2 = b[0] * Math.PI / 180;
    var dphi = (b[0] - a[0]) * Math.PI / 180;
    var dl = (b[1] - a[1]) * Math.PI / 180;
    var x = Math.sin(dphi / 2) * Math.sin(dphi / 2) +
            Math.cos(p1) * Math.cos(p2) * Math.sin(dl / 2) * Math.sin(dl / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  // En la portada cada track lleva su href; el de una ficha no.
  function track0bis(data){ return !!data.tracks[0].href; }
  function trackMidpoint(points) {
    var total = 0, cum = [0], i;
    for (i = 1; i < points.length; i++) {
      total += haversineMeters(points[i - 1], points[i]);
      cum.push(total);
    }
    var half = total / 2;
    for (i = 0; i < cum.length; i++) {
      if (cum[i] >= half) return points[i];
    }
    return points[points.length - 1];
  }

  // js/filters.js (only present on the home page) announces its current
  // visible-routes set on every change. Registered before the fetch below
  // resolves, since the two scripts' load order isn't guaranteed relative
  // to each other -- whichever fires first, the other picks up the latest
  // state once it's ready (onRouteFilterChange is wired up once the map's
  // lines exist).
  var pendingVisibleHrefs = window.trabakutikVisibleRoutes || null;
  var pendingActivity = window.trabakutikActivity || 'all';
  var onRouteFilterChange = null;
  document.addEventListener('routefilters:apply', function(e){
    pendingVisibleHrefs = e.detail.visibleHrefs;
    pendingActivity = e.detail.activity || 'all';
    if (onRouteFilterChange) onRouteFilterChange(pendingVisibleHrefs, pendingActivity);
  });

  function loadMap(){
    if (loading) return;
    loading = true;
    el.classList.remove('map-unavailable');
    el.textContent = '';
    el.setAttribute('aria-busy', 'true');
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timeout;
    var request = fetch(el.dataset.mapSrc, controller ? { signal: controller.signal } : {}).then(function(r){
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
    // A stalled request must also reach the visible error/retry state.
    var deadline = new Promise(function(resolve, reject){
      timeout = setTimeout(function(){
        if (controller) controller.abort();
        reject(new Error('Map request timed out'));
      }, 15000);
    });
    Promise.race([request, deadline]).then(function(data){
    clearTimeout(timeout);
    if (!data || !Array.isArray(data.tracks) || !data.tracks.length ||
        data.tracks.some(function(t){ return !Array.isArray(t.points) || !t.points.length; })) {
      throw new Error('Invalid map tracks');
    }
    map = L.map(el, {
      zoomControl: true,
      scrollWheelZoom: false,
      center: data.tracks[0].points[0],
      zoom: 13
    });
    // Layer switcher, on every map -- the home page's overview and each
    // route's own map alike. Four free layers, none needing an API key:
    // the Spanish IGN's topographic map (contour lines, named streams and
    // villages), CyclOSM (bike-oriented rendering, surfaces, cycle lanes),
    // OSM and Esri World Imagery (aerial photo). Same four and same default
    // everywhere.
    var cycleLayer = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
      maxZoom: 20,
      attribution: '&copy; <a href="https://www.cyclosm.org" target="_blank" rel="noopener">CyclOSM</a>, &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
    });
    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    });
    var satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; <a href="https://www.esri.com" target="_blank" rel="noopener">Esri</a> &mdash; Esri, Maxar, Earthstar Geographics'
    });
    // El topografico oficial español (el MTN de toda la vida) en vez del
    // OpenTopoMap que habia. Por aqui OpenTopoMap dibuja los arroyos como un
    // pelo azul sin nombre, cuando se molesta, y el autor echaba en falta los
    // rios que si se ven en Wikiloc -- que usa precisamente este mapa. El IGN
    // los dibuja gruesos y con su nombre, igual que los toponimos y las
    // curvas de nivel. Llega hasta z20, tres mas que OpenTopoMap.
    var topoLayer = L.tileLayer('https://www.ign.es/wmts/mapa-raster?layer=MTN&style=default' +
      '&tilematrixset=GoogleMapsCompatible&Service=WMTS&Request=GetTile&Version=1.0.0' +
      '&Format=image/jpeg&TileMatrix={z}&TileCol={x}&TileRow={y}', {
      maxZoom: 20,
      attribution: '&copy; <a href="https://www.ign.es" target="_blank" rel="noopener">Instituto Geogr&aacute;fico Nacional de Espa&ntilde;a</a>'
    });
    // La portada abre con las calles y las fichas con el IGN, que es como lo
    // quiere el autor: en la vista de conjunto, con las 57 rutas a la vez, lo
    // que situa es el callejero; en una ruta, los rios, los toponimos y las
    // curvas de nivel del IGN. El mapa no cambia solo nunca: ni al acercarse
    // ni al elegir una ruta. Se probaron las dos cosas y el autor las quito:
    // que el mapa cambie debajo sin haberlo pedido desconcierta mas de lo que
    // ayuda. Solo lo cambian los botones.
    var esPortada = el.dataset.mapSrc.split('?')[0] === 'data/trailhead.json';
    var LABEL_MIN_ZOOM = 13;   // el zoom al que salen los kilometros de cada ruta
    var layerDefs = [
      { layer: topoLayer, label: isEu ? 'IGN mapa topografikoa' : 'Mapa topográfico del IGN', short: 'IGN' },
      { layer: cycleLayer, label: isEu ? 'Bizikleta' : 'Ciclista', short: isEu ? 'Bizi' : 'Bici' },
      { layer: osmLayer, label: isEu ? 'Kaleak' : 'Calles', short: isEu ? 'Kaleak' : 'Calles' },
      { layer: satLayer, label: isEu ? 'Satelitea' : 'Satélite', short: 'Sat' }
    ];
    // Las capas, a la vista: antes eran un icono de tres rombos que abria un
    // menu, y un icono que no dice que hace no lo pulsa nadie. Ahora son
    // botones, con el activo encendido, como en cualquier mapa de movil.
    // El callejero solo en la portada, que es donde situa: ahi se ven las 57
    // rutas de lejos y lo que ubica es el pueblo. Dentro de una ruta no
    // pinta nada -- lo que hace falta son las curvas de nivel, los rios y los
    // caminos -- y el autor lo ha quitado de las fichas.
    if (!esPortada) {
      layerDefs = layerDefs.filter(function(def){ return def.layer !== osmLayer; });
    }
    var layerIndex = esPortada ? 2 : 0;   // 2 = Calles en la portada, 0 = IGN en una ficha
    // El mapa de la portada nace dentro de un bloque oculto: hasta que el
    // visitante no cambia a la vista de mapa mide 0x0. Y un contenedor de 0x0
    // le hace creer a Leaflet que cabe todo a zoom maximo, asi que pedia las
    // teselas del zoom 20 -- las mas detalladas que hay -- de un mapa que
    // nadie estaba viendo, en cada visita a la portada. La capa no se engancha
    // hasta que la caja mide algo; fit() lo hace en cuanto aparece.
    var capaPuesta = false;
    function asegurarCapa(){
      if (capaPuesta || !el.clientWidth || !el.clientHeight) return;
      capaPuesta = true;
      layerDefs[layerIndex].layer.addTo(map);
    }
    var layersBar = document.createElement('div');
    layersBar.className = 'map-layers';
    layersBar.setAttribute('role', 'group');
    layersBar.setAttribute('aria-label', isEu ? 'Mapa mota' : 'Tipo de mapa');
    function ponerCapa(i){
      if (i === layerIndex) return;
      if (capaPuesta) map.removeLayer(layerDefs[layerIndex].layer);
      layerIndex = i;
      if (capaPuesta) layerDefs[layerIndex].layer.addTo(map);
      layerBtns.forEach(function(b, j){
        b.classList.toggle('is-selected', j === layerIndex);
        b.setAttribute('aria-pressed', String(j === layerIndex));
      });
    }
    var layerBtns = layerDefs.map(function(def, i){
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'map-layer-btn' + (i === layerIndex ? ' is-selected' : '');
      b.setAttribute('aria-pressed', String(i === layerIndex));
      b.textContent = def.short;
      b.title = def.label;
      b.addEventListener('click', function(e){
        e.stopPropagation();
        ponerCapa(i);
      });
      layersBar.appendChild(b);
      return b;
    });
    el.parentElement.appendChild(layersBar);

    // Lo que no es "que mapa" sino como se pinta encima va en la misma
    // pastilla, detras de una raya: estaba en una segunda pastilla debajo y
    // el autor lo quiere todo seguido y en horizontal. La raya es lo unico
    // que dice que es otra cosa -- las capas son excluyentes, esto es un
    // interruptor suelto.
    function ponExtra(btn){
      if (!layersBar.querySelector('.map-layers-sep')) {
        var raya = document.createElement('span');
        raya.className = 'map-layers-sep';
        raya.setAttribute('aria-hidden', 'true');
        layersBar.appendChild(raya);
      }
      layersBar.appendChild(btn);
    }

    // On a page with several routes (the home overview), clicking one opens
    // a bottom info panel instead of a Leaflet popup anchored to the click
    // point -- a popup placed on the line itself covers the very route it
    // describes, especially once we've zoomed in on it below. A fixed panel
    // never does, and its own height feeds back into the zoom padding so
    // the route never renders underneath it either.
    var panel = null, panelBody = null, panelClose = null, activeLine = null, activeBaseColor = null;
    function ensurePanel(){
      if (panel) return;
      panel = document.createElement('div');
      panel.className = 'route-info-panel';
      panel.hidden = true;
      panel.setAttribute('role', 'region');
      panel.setAttribute('aria-label', isEu ? 'Ibilbidearen informazioa' : 'Información de la ruta');
      var close = document.createElement('button');
      panelClose = close;
      close.type = 'button';
      close.className = 'route-info-panel-close';
      close.setAttribute('aria-label', isEu ? 'Itxi' : 'Cerrar');
      close.innerHTML = '&#10005;';
      close.addEventListener('click', closePanel);
      panelBody = document.createElement('div');
      panel.appendChild(close);
      panel.appendChild(panelBody);
      el.parentElement.appendChild(panel);
      panel.addEventListener('keydown', function(e){
        if (e.key === 'Escape') { e.preventDefault(); closePanel(); }
      });
    }
    // The mapa/lista FAB is position:fixed at the bottom centre, same spot
    // the panel's "Ver ruta completa" link ends up at on a short viewport --
    // it sat on top of the link and swallowed the tap ("no me deja entrar").
    // Hiding it while the panel is open removes the overlap outright instead
    // of fighting over z-index across two separate stacking contexts.
    var viewFab = document.getElementById('viewFab');
    function closePanel(){
      if (!panel || !panel.classList.contains('open')) return;
      var returnFocus = panel.contains(document.activeElement);
      panel.classList.remove('open');
      panel.hidden = true;
      if (viewFab) viewFab.classList.remove('is-hidden-behind-panel');
      if (activeLine) {
        var path = activeLine.getElement();
        activeLine.setStyle({ color: activeBaseColor, weight: 4, opacity: baseOpacity });
        if (path) {
          path.setAttribute('aria-pressed', 'false');
          if (returnFocus) path.focus({ preventScroll: true });
        }
        activeLine = null;
        Object.keys(hrefToLine).forEach(function(href){
          var entry = hrefToLine[href];
          var entryPath = entry.line.getElement();
          var hidden = entryPath && entryPath.getAttribute('aria-hidden') === 'true';
          entry.line.setStyle({
            color: entry.currentColor,
            weight: 4,
            opacity: hidden ? 0.06 : baseOpacity
          });
        });
      }
      // Antes esto reencuadraba el mapa entero al cerrar la ficha (y como
      // cualquier toque en el mapa cierra la ficha, se salia del zoom sin
      // querer). Ahora la vista se queda donde el visitante la ha dejado.
    }
    function openPanel(line, baseColor, html, keyboard){
      ensurePanel();
      if (activeLine && activeLine !== line) {
        activeLine.setStyle({ color: activeBaseColor, weight: 4, opacity: baseOpacity });
        activeLine.getElement().setAttribute('aria-pressed', 'false');
      }
      activeLine = line; activeBaseColor = baseColor;
      userMoved = true;

      // La ruta elegida manda visualmente: rojo fino por encima; el resto
      // conserva su color pero se apaga para no taparla ni ensuciar el mapa.
      Object.keys(hrefToLine).forEach(function(href){
        var entry = hrefToLine[href];
        var entryPath = entry.line.getElement();
        var hidden = entryPath && entryPath.getAttribute('aria-hidden') === 'true';
        if (entry.line === line) {
          entry.line.setStyle({ color: COLORS.parking, weight: 3, opacity: 1 });
          if (entry.line.bringToFront) entry.line.bringToFront();
        } else {
          entry.line.setStyle({ opacity: hidden ? 0.06 : 0.22, weight: 4 });
        }
      });
      line.getElement().setAttribute('aria-pressed', 'true');
      panelBody.innerHTML = html;
      panel.hidden = false;
      panel.classList.add('open');
      if (viewFab) viewFab.classList.add('is-hidden-behind-panel');
      var panelHeight = panel.getBoundingClientRect().height;
      map.flyToBounds(line.getBounds(), {
        paddingTopLeft: [24, 24],
        paddingBottomRight: [24, panelHeight + 24],
        maxZoom: 15,
        animate: !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)
      });
      if (keyboard) panelClose.focus({ preventScroll: true });
    }

    var bounds = null;
    var hrefToLine = {};
    var hrefToLabel = {};
    var labelFilterVisible = {}; // href -> false solo cuando el filtro lo oculta
    // Con las 46 rutas a la vista de conjunto, mostrar las etiquetas desde el
    // primer momento las amontona todas sobre Trabakua. Se quedan ocultas
    // hasta que el visitante se acerca de verdad a una zona del mapa.
    var baseOpacity = data.tracks.length > 1 ? 0.85 : 0.9;
    data.tracks.forEach(function(t){
      var baseColor = COLORS[t.color] || COLORS.teal;
      var line = L.polyline(t.points, {
        color: baseColor,
        weight: 4,
        opacity: baseOpacity,
        lineJoin: 'round'
      }).addTo(map);
      bounds = bounds ? bounds.extend(line.getBounds()) : line.getBounds();

      if (t.href) {
        var href = isEu ? t.href.replace(/\.html$/, '.eu.html') : t.href;
        // Signpost hrefs are .eu.html on the Basque page, but t.href is
        // always the language-independent .html name -- compare normalized.
        var sign = document.querySelector('.route-card[href="' + t.href + '"], .route-card[href="' + href + '"]');
        var name = sign ? sign.querySelector('.route-card-name').textContent.trim() : t.href;
        var distanceKm = sign ? sign.dataset.distanceKm : null;
        var desnivelM = sign ? sign.dataset.desnivelM : null;
        var activity = sign ? sign.dataset.activity : null;
        var activityLabel = (activity || '').split(',').map(function(a){
          return a === 'bici' ? 'E-bike' : a === 'senderismo' ? (isEu ? 'Oinez' : 'Senderismo') : '';
        }).filter(Boolean).join(' · ');
        var distLabel = isEu ? 'Distantzia' : 'Distancia';
        var descLabel = isEu ? 'Desnibela' : 'Desnivel';
        var actLabel = isEu ? 'Jarduera' : 'Actividad';
        var dirLabel = isEu ? 'Norabide orokorra' : 'Dirección general';
        var seeLabel = isEu ? 'Ikusi ibilbide osoa' : 'Ver ruta completa';
        var facts = '';
        if (distanceKm) facts += '<span>' + distLabel + ': <b>' +
          distanceKm.replace('.', ',') + ' km</b></span>';
        if (desnivelM) facts += '<span>' + descLabel + ': <b>+' +
          desnivelM.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' m</b></span>';
        if (activityLabel) facts += '<span>' + actLabel + ': <b>' + activityLabel + '</b></span>';
        // La orientacion va en la misma fila que el resto de datos, no en una
        // linea aparte: en un movil la ficha mide 250 px y cada linea suelta
        // empujaba el boton fuera de la vista.
        facts += '<span>' + dirLabel + ': <b>' + directionLabel(t.points) + '</b></span>';
        // La foto sale de la propia tarjeta de la portada, clonada tal cual:
        // asi no hay que deducir el nombre del fichero del href (que en la
        // pagina en euskera acaba en .eu.html), el alt viene ya en el idioma
        // correcto, y el navegador no descarga nada nuevo porque esa miniatura
        // ya esta en la pagina.
        var pic = sign && sign.querySelector('.route-card-photo picture');
        var photo = pic ? '<div class="route-popup-photo">' + pic.outerHTML + '</div>' : '';
        // El perfil solo cuando no hay foto. Los dos juntos no caben: la ficha
        // mide como mucho el 78% del mapa, y en un movil eso son 229 px, que
        // con foto y perfil dejaban el nombre y el boton fuera de vista.
        var chart = (!photo && t.chart) ? '<svg class="route-popup-chart" viewBox="0 0 1000 300" ' +
          'preserveAspectRatio="none"><path d="' + t.chart + '" fill="var(--teal-soft)"/></svg>' : '';
        var html = '<div class="route-popup">' + photo + chart + '<h3>' + name + '</h3>' +
          '<div class="route-popup-facts">' + facts + '</div>' +
          '<a href="' + href + '">' + seeLabel + ' &rarr;</a></div>';
        line.on('click', function(e){ L.DomEvent.stopPropagation(e); openPanel(line, hrefToLine[t.href].currentColor, html); });
        line.on('mouseover', function(){ if (!activeLine) line.setStyle({ weight: 6 }); });
        line.on('mouseout', function(){ if (!activeLine) line.setStyle({ weight: 4 }); });

        // Etiqueta de distancia en el punto medio, solo en el mapa de
        // conjunto (aqui es donde 46 rutas comparten el mismo arranque).
        if (distanceKm) {
          var labelMarker = L.marker(trackMidpoint(t.points), {
            icon: L.divIcon({
              className: 'route-dist-label',
              html: '<span class="route-dist-label-inner">' +
                distanceKm.replace('.', ',') + ' km</span>',
              iconSize: null
            }),
            title: name + ' — ' + distanceKm.replace('.', ',') + ' km',
            keyboard: false
          }).addTo(map);
          labelMarker.on('click', function(e){
            L.DomEvent.stopPropagation(e);
            openPanel(line, hrefToLine[t.href].currentColor, html);
          });
          labelMarker.on('mouseover', function(){ if (!activeLine) line.setStyle({ weight: 6 }); });
          labelMarker.on('mouseout', function(){ if (!activeLine) line.setStyle({ weight: 4 }); });
          hrefToLabel[t.href] = labelMarker;
        }
        var pathEl = line.getElement();
        if (pathEl) {
          pathEl.style.cursor = 'pointer';
          pathEl.setAttribute('tabindex', '0');
          pathEl.setAttribute('role', 'button');
          pathEl.setAttribute('aria-label', name);
          pathEl.setAttribute('aria-pressed', 'false');
          pathEl.addEventListener('keydown', function(e){
            if (pathEl.getAttribute('aria-hidden') === 'true') return;
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault(); e.stopPropagation();
              openPanel(line, hrefToLine[t.href].currentColor, html, true);
            } else if (e.key === 'Escape') {
              e.preventDefault(); closePanel();
            }
          });
          pathEl.addEventListener('focus', function(){ if (!activeLine) line.setStyle({ weight: 6 }); });
          pathEl.addEventListener('blur', function(){ if (!activeLine) line.setStyle({ weight: 4 }); });
        }
        hrefToLine[t.href] = { line: line, baseColor: baseColor, activity: activity, currentColor: baseColor };
      }
    });

    // Fades out routes that the home page's activity/distance/desnivel
    // filters (js/filters.js) have hidden, instead of the map staying
    // stuck showing every route regardless of the filter state.
    function applyRouteFilter(visibleHrefs, activity){
      var hrefs = Object.keys(hrefToLine);
      if (!hrefs.length) return;
      var visible = null;
      if (visibleHrefs) {
        visible = {};
        visibleHrefs.forEach(function(h){ visible[h] = true; });
      }
      // With a single activity selected, every visible track (including
      // mixed a-pie/BTT routes, whose stored color always leans "en bici")
      // is forced to that activity's color, so the map reads as one
      // consistent color instead of a teal/violet mix. "Todas las
      // actividades" leaves each route its own stored color.
      var forcedColor = activity === 'senderismo' ? COLORS.violet :
        activity === 'bici' ? COLORS.teal : null;
      hrefs.forEach(function(href){
        var entry = hrefToLine[href];
        var show = !visible || !!visible[href];
        if (!show && entry.line === activeLine) closePanel();
        var color = forcedColor || entry.baseColor;
        entry.currentColor = color;
        if (entry.line === activeLine) {
          activeBaseColor = color;
          entry.line.setStyle({ color: COLORS.parking, weight: 3, opacity: 1 });
          if (entry.line.bringToFront) entry.line.bringToFront();
        } else {
          entry.line.setStyle({
            opacity: show ? (activeLine ? 0.22 : baseOpacity) : 0.06,
            color: color,
            weight: 4
          });
        }
        var pathEl = entry.line.getElement();
        if (pathEl) {
          if (!show && pathEl === document.activeElement) el.focus({ preventScroll: true });
          pathEl.style.pointerEvents = show ? '' : 'none';
          pathEl.setAttribute('tabindex', show ? '0' : '-1');
          pathEl.setAttribute('aria-hidden', show ? 'false' : 'true');
        }
        labelFilterVisible[href] = show;
      });
      // Con menos etiquetas visibles cambia lo que se solapa entre si.
      updateLabelVisibility();
    }
    applyRouteFilter(pendingVisibleHrefs, pendingActivity);
    onRouteFilterChange = applyRouteFilter;

    if (data.marker) {
      var c = COLORS[data.marker.color] || COLORS.violet;
      var size = data.marker.color === 'parking' ? 16 : 14;
      L.marker(data.marker.at, {
        title: el.dataset.markerTitle || '',
        icon: L.divIcon({
          className: '',
          html: '<span style="display:block;width:' + size + 'px;height:' + size + 'px;' +
                'border-radius:50%;background:' + c + ';border:3px solid ' + ground + ';' +
                'box-shadow:0 0 0 1.5px ' + c + ';"></span>',
          iconSize: [size, size], iconAnchor: [size / 2, size / 2]
        })
      }).addTo(map);
    }

    // El sentido de la marcha, con flechas sobre el trazado. Un circuito
    // dibujado no dice por donde se empieza a girar, y hacerlo al reves
    // cambia una ruta entera: las subidas son otras. Los numeros de los
    // puntos ya lo insinuan, pero hay que pararse a leerlos.
    //
    // Van repartidas a lo largo del recorrido, no cada N puntos: el GPX
    // esta mas poblado en las curvas (Douglas-Peucker), asi que contando
    // puntos se amontonarian justo donde mas estorban.
    if (data.tracks.length === 1 && !track0bis(data) && data.tracks[0].points.length > 8) {
      var puntos = data.tracks[0].points;
      var total = 0;
      var acumulado = [0];
      for (var ia = 1; ia < puntos.length; ia++) {
        total += haversineMeters(puntos[ia - 1], puntos[ia]);
        acumulado.push(total);
      }
      var CUANTAS = Math.max(6, Math.min(14, Math.round(total / 1500)));
      for (var f = 1; f <= CUANTAS; f++) {
        var meta = total * f / (CUANTAS + 1);
        var j = 1;
        while (j < acumulado.length - 1 && acumulado[j] < meta) j++;
        var a = puntos[j - 1], b = puntos[j];
        // Rumbo en pantalla: la longitud se encoge con el coseno de la
        // latitud, y sin eso las flechas apuntan torcido.
        var dx = (b[1] - a[1]) * Math.cos(a[0] * Math.PI / 180);
        var dy = b[0] - a[0];
        if (!dx && !dy) continue;
        var giro = Math.atan2(dx, dy) * 180 / Math.PI;   // 0 = al norte
        L.marker(b, {
          interactive: false,
          keyboard: false,
          icon: L.divIcon({
            className: 'track-arrow',
            html: '<svg width="13" height="13" viewBox="0 0 24 24" aria-hidden="true" ' +
                  'style="transform:rotate(' + giro.toFixed(1) + 'deg)">' +
                  '<path d="M12 3 L19 20 L12 16 L5 20 Z" fill="' + ground + '" ' +
                  'stroke="' + ground + '" stroke-width="2" stroke-linejoin="round"/></svg>',
            iconSize: [13, 13], iconAnchor: [6.5, 6.5]
          })
        }).addTo(map);
      }
    }

    (data.waypoints || []).forEach(function(pt, i){
      L.marker(pt, {
        title: wpNames[i] || '',
        icon: L.divIcon({
          className: '',
          html: '<span style="display:flex;align-items:center;justify-content:center;' +
                'width:18px;height:18px;border-radius:50%;background:' + COLORS.teal + ';' +
                'border:2px solid ' + ground + ';color:' + ground + ';' +
                'font:700 9px \'IBM Plex Mono\',monospace;">' + (i + 1) + '</span>',
          iconSize: [18, 18], iconAnchor: [9, 9]
        })
      }).addTo(map);
    });

    // Elevation profile <-> map, linked (Wikiloc-style): only on a route's
    // own page, where there's exactly one track and its own elevation-
    // profile SVG in .hero-chart (the home overview map has many tracks
    // and no such SVG, so this stays off there). The profile's path is
    // drawn at N evenly-distance-spaced samples over x=[0,1000] (see the
    // by-hand elevation script this pipeline uses), so a screen-x fraction
    // maps directly onto the same fraction of this track's own point array.
    var track0 = data.tracks[0];

    // El track pintado por pendiente, como en los editores de GPX: el mismo
    // trazado, pero cada tramo del color de lo que empina. Es un interruptor,
    // no el estado normal: el color de la ruta (verde a pie, azul en bici) es
    // parte de la casa. Solo en la ficha de una ruta, y solo si sus puntos
    // traen altura (el tercer numero que escribe make_map_data.py; la portada
    // no la lleva).
    //
    // La pendiente no se mide entre dos puntos seguidos: el GPS se equivoca
    // unos metros en vertical, y entre dos puntos a 3 m de distancia eso da
    // pendientes del 100% que no existen. Se mide sobre VENTANA metros de
    // recorrido, que es como la calculan los ciclometros.
    if (data.tracks.length === 1 && !track0.href && track0.points.length > 2 &&
        track0.points[0].length > 2) {
      var VENTANA = 60;
      var TRAMOS = [
        { hasta: -8,       color: '#2f80c4' },
        { hasta: -4,       color: '#7fb9e3' },
        { hasta: 4,        color: '#6e7f86' },
        { hasta: 8,        color: '#e8c34a' },
        { hasta: 14,       color: '#e5853c' },
        { hasta: Infinity, color: '#d4453c' }
      ];
      var pts = track0.points;
      var acum = [0];
      for (var ip = 1; ip < pts.length; ip++) {
        acum.push(acum[ip - 1] + haversineMeters(pts[ip - 1], pts[ip]));
      }
      function claseEn(i){
        var atras = i, alante = i;
        while (atras > 0 && acum[i] - acum[atras] < VENTANA / 2) atras--;
        while (alante < pts.length - 1 && acum[alante] - acum[i] < VENTANA / 2) alante++;
        var corrido = acum[alante] - acum[atras];
        if (corrido < 1) return 2;   // parado: llano
        var pc = (pts[alante][2] - pts[atras][2]) / corrido * 100;
        for (var c = 0; c < TRAMOS.length; c++) if (pc < TRAMOS[c].hasta) return c;
        return TRAMOS.length - 1;
      }
      // Un trazo por tramo de pendiente, no uno por punto: los puntos
      // seguidos que empinan igual van en la misma linea, y cada una empieza
      // donde acaba la anterior para que no queden huecos.
      var capaPendiente = L.layerGroup();
      var claseAnterior = claseEn(0);
      var desde = 0;
      for (var i = 1; i < pts.length; i++) {
        var clase = claseEn(i);
        if (clase !== claseAnterior || i === pts.length - 1) {
          L.polyline(pts.slice(desde, i + 1), {
            color: TRAMOS[claseAnterior].color, weight: 5, opacity: 1,
            lineCap: 'butt', lineJoin: 'round', interactive: false
          }).addTo(capaPendiente);
          desde = i;
          claseAnterior = clase;
        }
      }

      // La leyenda va debajo del mapa, en el flujo de la pagina, no flotando
      // encima: abajo a la izquierda chocaria con la linea de creditos, que
      // en un movil ocupa dos lineas.
      var leyenda = document.createElement('div');
      leyenda.className = 'slope-legend';
      leyenda.hidden = true;
      var titulo = document.createElement('span');
      titulo.className = 'slope-legend-title';
      titulo.textContent = isEu ? 'Malda (%)' : 'Pendiente (%)';
      leyenda.appendChild(titulo);
      ['< -8', '-8 / -4', '-4 / 4', '4 / 8', '8 / 14', '> 14'].forEach(function(txt, i){
        var chip = document.createElement('span');
        chip.className = 'slope-key';
        var muestra = document.createElement('i');
        muestra.style.background = TRAMOS[i].color;
        chip.appendChild(muestra);
        chip.appendChild(document.createTextNode(txt));
        leyenda.appendChild(chip);
      });
      // Se coloca al encenderla, no ahora: el perfil y la lista de puntos se
      // mudan a esta misma altura mas abajo en este fichero, y una leyenda
      // puesta de antemano acababa la ultima de la seccion, lejos del mapa.
      var mapBox = el.parentElement;
      function ponLeyenda(){
        mapBox.parentNode.insertBefore(leyenda, mapBox.nextSibling);
      }

      var pendienteOn = false;
      var slopeBtn = document.createElement('button');
      slopeBtn.type = 'button';
      slopeBtn.className = 'map-layer-btn';
      slopeBtn.textContent = isEu ? 'Malda' : 'Pendiente';
      slopeBtn.title = isEu ? 'Ibilbidea maldaren arabera margotu'
                            : 'Pintar el track según la pendiente';
      slopeBtn.setAttribute('aria-pressed', 'false');
      slopeBtn.addEventListener('click', function(e){
        e.stopPropagation();
        pendienteOn = !pendienteOn;
        if (pendienteOn) { capaPendiente.addTo(map); ponLeyenda(); }
        else map.removeLayer(capaPendiente);
        leyenda.hidden = !pendienteOn;
        slopeBtn.classList.toggle('is-selected', pendienteOn);
        slopeBtn.setAttribute('aria-pressed', String(pendienteOn));
      });
      ponExtra(slopeBtn);
    }

    if (data.tracks.length === 1 && !track0.href && track0.points.length > 1) {
      // Direct child only: the hero-activity-badge's own small icon <svg>
      // also lives inside .chart-visual, ahead of the elevation profile
      // one in document order, and would otherwise win a plain "svg" match.
      var heroSvg = document.querySelector('.chart-visual > svg');
      var heroPath = heroSvg && heroSvg.querySelector('path[stroke]');
      if (heroSvg && heroPath) {
        var svgNS = 'http://www.w3.org/2000/svg';
        var charts = [];

        // Parsed once from the page's own already-rendered figures (the
        // facts row and the elevation tags), rather than recomputed here:
        // there is exactly one source of truth for distance/altitude range,
        // and it is the text every visitor already reads.
        function parseNum(str){
          var m = str && str.match(/[\d.,]+(?=\s*(?:km|m)\b)/);
          if (!m) return null;
          return parseFloat(m[0].replace(/\./g, '').replace(',', '.'));
        }
        var factsBox = document.querySelector('.facts');
        var tagsBox = document.querySelector('.elev-tags');
        var totalKm = factsBox && parseNum(factsBox.querySelector('.fact .v').textContent);
        var minEle = tagsBox && parseNum(tagsBox.querySelector('.end.left .v').textContent);
        var maxEle = tagsBox && parseNum(tagsBox.querySelector('.end.right .v').textContent);
        var hasReadout = totalKm != null && minEle != null && maxEle != null && maxEle > minEle;

        function addChart(svg){
          var cursorLine = document.createElementNS(svgNS, 'line');
          cursorLine.setAttribute('y1', '0');
          cursorLine.setAttribute('y2', '300');
          cursorLine.setAttribute('stroke', ground);
          cursorLine.setAttribute('stroke-width', '1.5');
          cursorLine.setAttribute('stroke-dasharray', '4 3');
          cursorLine.setAttribute('opacity', '0');
          cursorLine.style.pointerEvents = 'none';
          svg.appendChild(cursorLine);
          var cursorDot = document.createElementNS(svgNS, 'circle');
          cursorDot.setAttribute('r', '6');
          cursorDot.setAttribute('fill', COLORS.teal);
          cursorDot.setAttribute('stroke', ground);
          cursorDot.setAttribute('stroke-width', '2');
          cursorDot.setAttribute('opacity', '0');
          cursorDot.style.pointerEvents = 'none';
          svg.appendChild(cursorDot);
          var readout = null;
          if (hasReadout) {
            readout = document.createElementNS(svgNS, 'g');
            readout.setAttribute('class', 'elev-readout');
            readout.setAttribute('opacity', '0');
            readout.style.pointerEvents = 'none';
            var readoutBg = document.createElementNS(svgNS, 'rect');
            readoutBg.setAttribute('height', '38');
            readoutBg.setAttribute('rx', '7');
            readoutBg.setAttribute('fill', ground);
            readoutBg.setAttribute('opacity', '0.85');
            var readoutText = document.createElementNS(svgNS, 'text');
            readoutText.setAttribute('y', '25');
            readoutText.setAttribute('text-anchor', 'middle');
            readoutText.setAttribute('font-family', "IBM Plex Mono, monospace");
            readoutText.setAttribute('font-size', '23');
            readoutText.setAttribute('font-weight', '700');
            readoutText.setAttribute('fill', COLORS.teal);
            readout.appendChild(readoutBg);
            readout.appendChild(readoutText);
            svg.appendChild(readout);
          }
          var chart = { svg: svg, line: cursorLine, dot: cursorDot, readout: readout,
            readoutBg: readoutBg, readoutText: readoutText };
          charts.push(chart);
          function fractionFromEvent(e){
            var rect = svg.getBoundingClientRect();
            var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
            return x / rect.width;
          }
          svg.addEventListener('mousemove', function(e){ showAtFraction(fractionFromEvent(e)); });
          svg.addEventListener('mouseleave', hideCursor);
          svg.addEventListener('touchstart', function(e){ showAtFraction(fractionFromEvent(e)); }, { passive: true });
          svg.addEventListener('touchmove', function(e){ showAtFraction(fractionFromEvent(e)); }, { passive: true });
          // Deliberately no touchend->hideCursor: lifting the finger leaves
          // the cursor, readout and map dot right where the visitor left
          // them, instead of vanishing the instant contact ends -- there is
          // no hover state on a touchscreen to fall back to, so this is the
          // only way the reading stays visible long enough to actually read.
          return chart;
        }

        // El perfil, una sola vez y abajo con el mapa. Antes estaba arriba
        // en la cabecera y aqui se ponia una copia: dos dibujos iguales en
        // la misma pagina. El autor quiere solo el de abajo, asi que se
        // mueve el de verdad. Debajo del mapa y no encima porque con el
        // perfil arriba la mano que arrastra el dedo tapa justo el mapa.
        // Se mueve aqui y no en build.py para no recortar el HTML de las 57
        // fichas a base de expresiones regulares: el DOM es un arbol y
        // moverlo no puede dejar una etiqueta sin cerrar.
        var mapSection = el.closest('.map-section');
        var mapBox = mapSection && mapSection.querySelector('.route-map-box');
        if (mapSection && mapBox) {
          var visual = heroSvg.parentNode;                       // .chart-visual
          var cabecera = visual.parentNode;                      // .hero-chart
          var tags = cabecera.querySelector('.elev-tags');
          var sobra = cabecera.querySelector('.elev-legend');     // la de la cabecera
          var nombres = mapSection.querySelector('.elev-legend'); // la del mapa, se queda
          if (sobra) sobra.remove();
          var detras = mapBox;
          if (nombres) {
            mapBox.parentNode.insertBefore(nombres, mapBox.nextSibling);
            detras = nombres;
          }
          mapBox.parentNode.insertBefore(visual, detras.nextSibling);
          if (tags) visual.parentNode.insertBefore(tags, visual.nextSibling);
          cabecera.classList.add('sin-perfil');
        }

        addChart(heroSvg);

        // Binary search along the (monotonic-in-x) stroke path for the y
        // at a given x -- there's no direct "value at x" query on <path>.
        // Every chart here is a clone of the same original, so they all
        // share one coordinate space and this one lookup serves them all.
        var pathLen = heroPath.getTotalLength();
        function yAtX(x){
          var lo = 0, hi = pathLen, pt;
          for (var i = 0; i < 20; i++){
            var mid = (lo + hi) / 2;
            pt = heroPath.getPointAtLength(mid);
            if (pt.x < x) lo = mid; else hi = mid;
          }
          return pt.y;
        }

        var mapCursor = L.circleMarker(track0.points[0], {
          radius: 7, weight: 2.5, color: ground, fillColor: COLORS.parking,
          fillOpacity: 1, opacity: 0, interactive: false
        }).addTo(map);

        // "12,3 km" / "12,3 km &middot; 450 m", matching the comma-decimal,
        // <b>-free plain format already used for every marker's km/ele pair
        // in the body copy (site-wide convention, see eu.py/CLAUDE.md).
        function fmtKm(km){ return km.toFixed(1).replace('.', ','); }
        function readoutLabel(frac, y){
          var km = fmtKm(frac * totalKm);
          if (!isFinite(y)) return km + ' km';
          var pad = 8;
          var ele = Math.round(minEle + (maxEle - minEle) * (1 - (y - pad) / (300 - 2 * pad)));
          return km + ' km · ' + ele + ' m';
        }
        function showAtFraction(frac){
          frac = Math.max(0, Math.min(1, frac));
          var x = frac * 1000;
          var y = yAtX(x);
          var idx = Math.round(frac * (track0.points.length - 1));
          var label = hasReadout ? readoutLabel(frac, y) : null;
          charts.forEach(function(c){
            c.line.setAttribute('x1', x); c.line.setAttribute('x2', x);
            c.line.setAttribute('opacity', '1');
            c.dot.setAttribute('cx', x); c.dot.setAttribute('cy', y);
            c.dot.setAttribute('opacity', '1');
            if (c.readout && label) {
              c.readoutText.textContent = label;
              // Measured after the text is set (its width depends on the
              // string), then the background rect and the whole group are
              // placed from that -- centered over the dot, clamped so a
              // reading near either end of the chart never spills outside
              // the 0-1000 viewBox.
              var textWidth = c.readoutText.getComputedTextLength();
              var boxWidth = textWidth + 32;
              var boxX = Math.max(4, Math.min(1000 - boxWidth - 4, x - boxWidth / 2));
              var boxY = Math.max(4, y - 48);
              c.readoutBg.setAttribute('x', boxX);
              c.readoutBg.setAttribute('y', boxY);
              c.readoutBg.setAttribute('width', boxWidth);
              c.readoutText.setAttribute('x', boxX + boxWidth / 2);
              c.readoutText.setAttribute('y', boxY + 25);
              c.readout.setAttribute('opacity', '1');
            }
          });
          mapCursor.setLatLng(track0.points[idx]);
          mapCursor.setStyle({ opacity: 1, fillOpacity: 1 });
        }
        function hideCursor(){
          charts.forEach(function(c){
            c.line.setAttribute('opacity', '0');
            c.dot.setAttribute('opacity', '0');
            if (c.readout) c.readout.setAttribute('opacity', '0');
          });
          mapCursor.setStyle({ opacity: 0, fillOpacity: 0 });
        }

        // The other direction: hovering the track on the map highlights the
        // matching point on the elevation profile.
        var trackLine = hrefToLine[track0.href] ? hrefToLine[track0.href].line : null;
        if (!trackLine) {
          // A route's own map track carries no href (see above), so grab
          // the one and only polyline drawn for it directly.
          map.eachLayer(function(layer){ if (layer instanceof L.Polyline) trackLine = layer; });
        }
        if (trackLine) {
          trackLine.on('mousemove', function(e){
            var nearest = 0, best = Infinity;
            for (var i = 0; i < track0.points.length; i++){
              var p = track0.points[i];
              var d = Math.pow(p[0] - e.latlng.lat, 2) + Math.pow(p[1] - e.latlng.lng, 2);
              if (d < best) { best = d; nearest = i; }
            }
            showAtFraction(nearest / (track0.points.length - 1));
          });
          trackLine.on('mouseout', hideCursor);
        }
      }
    }

    // Reparte las etiquetas de distancia que, a la vista actual, caen a
    // menos de MIN_DIST px de otra -- separandolas en vertical, un pequeno
    // numero de pasadas basta con 46 rutas. Se recalcula en cada zoom (un
    // pan no cambia la distancia relativa en pantalla entre dos puntos).
    function repositionLabels(){
      var hrefs = Object.keys(hrefToLabel);
      if (!hrefs.length) return;
      var pts = hrefs.map(function(h){
        return map.latLngToContainerPoint(hrefToLabel[h].getLatLng());
      });
      var offsets = hrefs.map(function(){ return 0; });
      var MIN_DIST = 42, ITER = 6;
      for (var iter = 0; iter < ITER; iter++) {
        for (var i = 0; i < pts.length; i++) {
          for (var j = i + 1; j < pts.length; j++) {
            var ay = pts[i].y + offsets[i], by = pts[j].y + offsets[j];
            var dist = Math.sqrt(Math.pow(pts[j].x - pts[i].x, 2) + Math.pow(by - ay, 2));
            if (dist < MIN_DIST) {
              var push = (MIN_DIST - dist) / 2 + 1;
              if (ay <= by) { offsets[i] -= push; offsets[j] += push; }
              else { offsets[i] += push; offsets[j] -= push; }
            }
          }
        }
      }
      hrefs.forEach(function(h, i){
        var markerEl = hrefToLabel[h].getElement();
        var inner = markerEl && markerEl.querySelector('.route-dist-label-inner');
        if (inner) inner.style.transform = 'translate(-50%, calc(-50% + ' + offsets[i].toFixed(1) + 'px))';
      });
    }

    // Solo con zoom alto (el visitante ya se ha acercado a una zona
    // concreta) se muestran las etiquetas; a la vista de conjunto quedarian
    // 46 numeros amontonados sobre Trabakua.
    function updateLabelVisibility(){
      var zoomOk = map.getZoom() >= LABEL_MIN_ZOOM;
      Object.keys(hrefToLabel).forEach(function(href){
        var labelEl = hrefToLabel[href].getElement();
        if (!labelEl) return;
        var show = zoomOk && labelFilterVisible[href] !== false;
        labelEl.style.opacity = show ? '1' : '0';
        labelEl.style.pointerEvents = show ? '' : 'none';
      });
      if (zoomOk) repositionLabels();
    }

    map.on('click', closePanel);
    map.on('zoomend', updateLabelVisibility);

    // Cualquier cambio de tamano del contenedor (abrir el mapa grande, girar
    // el movil, o la barra del navegador que aparece y desaparece al hacer
    // scroll) disparaba un fitBounds y devolvia el mapa al encuadre general.
    // Ahora solo se recalcula el tamano; el encuadre se rehace unicamente
    // mientras nadie haya tocado el mapa.
    // Solo cuenta lo que hace el visitante: 'zoomstart' saltaria tambien con
    // los encuadres automaticos (el primero, sin ir mas lejos), asi que se
    // escuchan el arrastre y los gestos de zoom sobre el propio contenedor.
    function markMoved(){ userMoved = true; }
    map.on('dragstart', markMoved);
    ['wheel', 'touchstart', 'dblclick', 'pointerdown'].forEach(function(ev){
      map.getContainer().addEventListener(ev, markMoved, { passive: true });
      cleanups.push(function(){ el.removeEventListener(ev, markMoved); });
    });

    function fit(){
      if (!el.clientWidth || !el.clientHeight) return;   // todavia oculto
      map.invalidateSize();
      asegurarCapa();
      if (!userMoved) map.fitBounds(bounds, { padding: [24, 24] });
    }
    resetView = function(){ map.invalidateSize(); asegurarCapa(); map.fitBounds(bounds, { padding: [24, 24] }); };
    fit();
    updateLabelVisibility();
    if ('ResizeObserver' in window) {
      var observer = new ResizeObserver(fit);
      observer.observe(el);
      cleanups.push(function(){ observer.disconnect(); });
    } else {
      window.addEventListener('resize', fit);
      cleanups.push(function(){ window.removeEventListener('resize', fit); });
    }
    if (expandBtn) {
      expandBtn.hidden = false;
      var expanded = el.parentElement.classList.contains('is-expanded');
      expandBtn.classList.toggle('is-active', expanded);
      expandBtn.setAttribute('aria-label', expanded ?
        expandBtn.dataset.labelCollapse : expandBtn.dataset.labelExpand);
    }
    el.setAttribute('aria-busy', 'false');
    loading = false;
    }).catch(function(err){
    clearTimeout(timeout);
    cleanups.forEach(function(cleanup){ cleanup(); });
    cleanups = [];
    if (map) { map.remove(); map = null; }
    resetView = null;
    onRouteFilterChange = null;
    Array.prototype.forEach.call(el.parentElement.querySelectorAll('.map-layers, .route-info-panel'),
      function(node){ node.remove(); });
    loading = false;
    showUnavailable(loadMap);
    if (window.console) console.error('No se pudo cargar el mapa:', err);
    });
  }
  // En la portada el mapa nace dentro de un bloque oculto: hasta que alguien
  // no pulsa «mapa» mide 0x0 y nadie lo esta viendo. Pedir ahi sus tracks
  // nada mas abrir la pagina son 399 kB -- lo mas pesado de la portada, mas
  // que todas sus fotos juntas -- para una vista que mucha gente no llega a
  // abrir. Se espera a que la caja mida algo, con el mismo ResizeObserver que
  // ya avisa de cuando aparece. En la ficha de una ruta el mapa esta en la
  // pagina desde el principio, asi que ahi carga de inmediato, como siempre;
  // y sin ResizeObserver (un navegador viejo) tambien, antes que dejar a
  // nadie sin mapa.
  if ((el.clientWidth && el.clientHeight) || typeof ResizeObserver === 'undefined') {
    loadMap();
  } else {
    var esperaVisible = new ResizeObserver(function(){
      if (!el.clientWidth || !el.clientHeight) return;
      esperaVisible.disconnect();
      loadMap();
    });
    esperaVisible.observe(el);
  }
})();
