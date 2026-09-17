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
      Array.prototype.forEach.call(box.querySelectorAll('.map-expand-btn, .map-layers-btn'),
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
        // Scroll to the mini elevation chart when there is one (it sits
        // right above the map box, inside the same .map-section) so
        // expanding the map doesn't push it off the top of the screen --
        // otherwise the elevation<->map link has nothing to show up next
        // to once the map takes over most of the viewport.
        var mapSection = el.closest('.map-section');
        var miniChart = mapSection && mapSection.querySelector('.mini-elev-chart');
        (miniChart || el.parentElement).scrollIntoView(scrollOpts());
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
    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    }).addTo(map);

    // Layer switcher, on every map -- the home page's overview and each
    // route's own map alike. Four free layers, none needing an API key:
    // OSM (default), Esri World Imagery (aerial photo), OpenTopoMap
    // (contour lines -- useful to gauge terrain at a glance) and CyclOSM
    // (bike-oriented rendering: surfaces, cycle lanes).
    var satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; <a href="https://www.esri.com" target="_blank" rel="noopener">Esri</a> &mdash; Esri, Maxar, Earthstar Geographics'
    });
    var topoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17,
      attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors, SRTM | Map style: &copy; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'
    });
    var cycleLayer = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
      maxZoom: 20,
      attribution: '&copy; <a href="https://www.cyclosm.org" target="_blank" rel="noopener">CyclOSM</a>, &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
    });
    var layerDefs = [
      { layer: osmLayer, label: isEu ? 'Kaleak' : 'Calles' },
      { layer: satLayer, label: isEu ? 'Satelitea' : 'Satélite' },
      { layer: topoLayer, label: isEu ? 'Topografikoa' : 'Topográfico' },
      { layer: cycleLayer, label: isEu ? 'Bizikleta' : 'Ciclista' }
    ];
    var layerIndex = 0;
    var layersBtn = document.createElement('button');
    layersBtn.type = 'button';
    layersBtn.className = 'map-layers-btn';
    layersBtn.setAttribute('aria-label', isEu ? 'Aldatu mapa mota' : 'Cambiar tipo de mapa');
    layersBtn.setAttribute('aria-haspopup', 'true');
    layersBtn.setAttribute('aria-expanded', 'false');
    layersBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>';
    var layersMenu = document.createElement('div');
    layersMenu.className = 'map-layers-menu';
    layersMenu.setAttribute('role', 'menu');
    layersMenu.hidden = true;
    function closeLayersMenu(){
      layersMenu.hidden = true;
      layersBtn.setAttribute('aria-expanded', 'false');
    }
    function openLayersMenu(){
      layersMenu.hidden = false;
      layersBtn.setAttribute('aria-expanded', 'true');
    }
    layerDefs.forEach(function(def, i){
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'map-layers-item' + (i === 0 ? ' is-selected' : '');
      item.setAttribute('role', 'menuitemradio');
      item.setAttribute('aria-checked', String(i === 0));
      item.textContent = def.label;
      item.addEventListener('click', function(){
        if (i !== layerIndex) {
          map.removeLayer(layerDefs[layerIndex].layer);
          layerIndex = i;
          layerDefs[layerIndex].layer.addTo(map);
          Array.from(layersMenu.children).forEach(function(child, j){
            child.classList.toggle('is-selected', j === layerIndex);
            child.setAttribute('aria-checked', String(j === layerIndex));
          });
          layersBtn.classList.toggle('is-active', layerIndex !== 0);
        }
        closeLayersMenu();
      });
      layersMenu.appendChild(item);
    });
    layersBtn.addEventListener('click', function(e){
      e.stopPropagation();
      if (layersMenu.hidden) openLayersMenu(); else closeLayersMenu();
    });
    var closeLayersMenuOnOutsideClick = function(e){
      if (!layersMenu.hidden && e.target !== layersBtn && !layersMenu.contains(e.target)) closeLayersMenu();
    };
    var closeLayersMenuOnEscape = function(e){
      if (e.key === 'Escape' && !layersMenu.hidden) { closeLayersMenu(); layersBtn.focus(); }
    };
    document.addEventListener('click', closeLayersMenuOnOutsideClick);
    document.addEventListener('keydown', closeLayersMenuOnEscape);
    cleanups.push(function(){
      document.removeEventListener('click', closeLayersMenuOnOutsideClick);
      document.removeEventListener('keydown', closeLayersMenuOnEscape);
    });
    el.parentElement.appendChild(layersBtn);
    el.parentElement.appendChild(layersMenu);

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
    function closePanel(){
      if (!panel || !panel.classList.contains('open')) return;
      var returnFocus = panel.contains(document.activeElement);
      panel.classList.remove('open');
      panel.hidden = true;
      if (activeLine) {
        var path = activeLine.getElement();
        activeLine.setStyle({ color: activeBaseColor, weight: 4 });
        if (path) {
          path.setAttribute('aria-pressed', 'false');
          if (returnFocus) path.focus({ preventScroll: true });
        }
        activeLine = null;
      }
      // Antes esto reencuadraba el mapa entero al cerrar la ficha (y como
      // cualquier toque en el mapa cierra la ficha, se salia del zoom sin
      // querer). Ahora la vista se queda donde el visitante la ha dejado.
    }
    function openPanel(line, baseColor, html, keyboard){
      ensurePanel();
      if (activeLine && activeLine !== line) {
        activeLine.setStyle({ color: activeBaseColor, weight: 4 });
        activeLine.getElement().setAttribute('aria-pressed', 'false');
      }
      activeLine = line; activeBaseColor = baseColor;
      userMoved = true;
      line.setStyle({ color: COLORS.parking, weight: 6 });
      line.getElement().setAttribute('aria-pressed', 'true');
      panelBody.innerHTML = html;
      panel.hidden = false;
      panel.classList.add('open');
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
    var LABEL_MIN_ZOOM = 13;
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
          return a === 'bici' ? 'BTT/e-bike' : a === 'senderismo' ? (isEu ? 'Oinez' : 'Senderismo') : '';
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
        line.on('mouseover', function(){ line.setStyle({ weight: 6 }); });
        line.on('mouseout', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });

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
          labelMarker.on('mouseover', function(){ line.setStyle({ weight: 6 }); });
          labelMarker.on('mouseout', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });
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
          pathEl.addEventListener('focus', function(){ line.setStyle({ weight: 6 }); });
          pathEl.addEventListener('blur', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });
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
        } else {
          entry.line.setStyle({ opacity: show ? baseOpacity : 0.06, color: color });
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

        // A second, compact copy of the same profile right above the map:
        // on a phone the hero chart (top of page) and the map (much lower
        // down) are never both on screen together, so hovering one to see
        // it move on the other was invisible in practice. Cloned -- same
        // <path> "d", so the same x/y coordinate space -- BEFORE the hero
        // gets its own cursor line/dot below, so there's nothing to strip
        // back out of the clone. Placed right next to the map this way,
        // with no need to touch every route's own _tail.html by hand.
        var mapSection = el.closest('.map-section');
        var mapBox = mapSection && mapSection.querySelector('.route-map-box');
        var miniSvg = null;
        if (mapSection && mapBox) {
          var miniWrap = document.createElement('div');
          miniWrap.className = 'mini-elev-chart';
          miniSvg = heroSvg.cloneNode(true);
          miniWrap.appendChild(miniSvg);
          mapBox.parentNode.insertBefore(miniWrap, mapBox);
        }

        addChart(heroSvg);
        if (miniSvg) addChart(miniSvg);

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
      map.invalidateSize();
      if (!userMoved) map.fitBounds(bounds, { padding: [24, 24] });
    }
    resetView = function(){ map.invalidateSize(); map.fitBounds(bounds, { padding: [24, 24] }); };
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
    Array.prototype.forEach.call(el.parentElement.querySelectorAll('.map-layers-btn, .route-info-panel'),
      function(node){ node.remove(); });
    loading = false;
    showUnavailable(loadMap);
    if (window.console) console.error('No se pudo cargar el mapa:', err);
    });
  }
  loadMap();
})();
