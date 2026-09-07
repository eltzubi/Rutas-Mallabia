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

  // js/filters.js (only present on the home page) announces its current
  // visible-routes set on every change. Registered before the fetch below
  // resolves, since the two scripts' load order isn't guaranteed relative
  // to each other -- whichever fires first, the other picks up the latest
  // state once it's ready (onRouteFilterChange is wired up once the map's
  // lines exist).
  var pendingVisibleHrefs = window.trabakutikVisibleRoutes || null;
  var onRouteFilterChange = null;
  document.addEventListener('routefilters:apply', function(e){
    pendingVisibleHrefs = e.detail.visibleHrefs;
    if (onRouteFilterChange) onRouteFilterChange(pendingVisibleHrefs);
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

    // Layer switcher (topographic view), on every map -- the home page's
    // overview and each route's own map alike.
    var topoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> &middot; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'
    });
    var isTopo = false;
    var layersBtn = document.createElement('button');
    layersBtn.type = 'button';
    layersBtn.className = 'map-layers-btn';
    layersBtn.setAttribute('aria-label', isEu ? 'Aldatu mapa mota' : 'Cambiar tipo de mapa');
    layersBtn.setAttribute('aria-pressed', 'false');
    layersBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>';
    layersBtn.addEventListener('click', function(){
      isTopo = !isTopo;
      if (isTopo) { map.removeLayer(osmLayer); topoLayer.addTo(map); }
      else { map.removeLayer(topoLayer); osmLayer.addTo(map); }
      layersBtn.classList.toggle('is-active', isTopo);
      layersBtn.setAttribute('aria-pressed', String(isTopo));
    });
    el.parentElement.appendChild(layersBtn);

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
        line.on('click', function(e){ L.DomEvent.stopPropagation(e); openPanel(line, baseColor, html); });
        line.on('mouseover', function(){ line.setStyle({ weight: 6 }); });
        line.on('mouseout', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });
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
              openPanel(line, baseColor, html, true);
            } else if (e.key === 'Escape') {
              e.preventDefault(); closePanel();
            }
          });
          pathEl.addEventListener('focus', function(){ line.setStyle({ weight: 6 }); });
          pathEl.addEventListener('blur', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });
        }
        hrefToLine[t.href] = { line: line, baseColor: baseColor };
      }
    });

    // Fades out routes that the home page's activity/distance/desnivel
    // filters (js/filters.js) have hidden, instead of the map staying
    // stuck showing every route regardless of the filter state.
    function applyRouteFilter(visibleHrefs){
      var hrefs = Object.keys(hrefToLine);
      if (!hrefs.length) return;
      var visible = null;
      if (visibleHrefs) {
        visible = {};
        visibleHrefs.forEach(function(h){ visible[h] = true; });
      }
      hrefs.forEach(function(href){
        var entry = hrefToLine[href];
        var show = !visible || visible[href];
        if (!show && entry.line === activeLine) closePanel();
        entry.line.setStyle({ opacity: show ? baseOpacity : 0.06 });
        var pathEl = entry.line.getElement();
        if (pathEl) {
          if (!show && pathEl === document.activeElement) el.focus({ preventScroll: true });
          pathEl.style.pointerEvents = show ? '' : 'none';
          pathEl.setAttribute('tabindex', show ? '0' : '-1');
          pathEl.setAttribute('aria-hidden', show ? 'false' : 'true');
        }
      });
    }
    applyRouteFilter(pendingVisibleHrefs);
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

    map.on('click', closePanel);

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
