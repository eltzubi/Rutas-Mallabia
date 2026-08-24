// One map implementation for every page and both languages.
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

  var expandBtn = el.parentElement && el.parentElement.querySelector('.map-expand-btn');
  if (expandBtn) {
    expandBtn.addEventListener('click', function(){
      var expanded = el.parentElement.classList.toggle('is-expanded');
      expandBtn.setAttribute('aria-label', expanded ?
        expandBtn.dataset.labelCollapse : expandBtn.dataset.labelExpand);
      expandBtn.classList.toggle('is-active', expanded);
      if (expanded) {
        el.parentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  if (typeof L === 'undefined') return;

  var isEu = document.documentElement.lang === 'eu';

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
  var wpNames = Array.prototype.map.call(
    document.querySelectorAll('.elev-legend-item'),
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

  fetch(el.dataset.mapSrc).then(function(r){ return r.json(); }).then(function(data){
    var map = L.map(el, {
      zoomControl: true,
      scrollWheelZoom: false,
      center: data.tracks[0].points[0],
      zoom: 13
    });
    L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17,
      attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors, SRTM | Map style: &copy; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'
    }).addTo(map);

    // On a page with several routes (the home overview), clicking one opens
    // a bottom info panel instead of a Leaflet popup anchored to the click
    // point -- a popup placed on the line itself covers the very route it
    // describes, especially once we've zoomed in on it below. A fixed panel
    // never does, and its own height feeds back into the zoom padding so
    // the route never renders underneath it either.
    var panel = null, panelBody = null, activeLine = null, activeBaseColor = null;
    function ensurePanel(){
      if (panel) return;
      panel = document.createElement('div');
      panel.className = 'route-info-panel';
      var close = document.createElement('button');
      close.type = 'button';
      close.className = 'route-info-panel-close';
      close.setAttribute('aria-label', isEu ? 'Itxi' : 'Cerrar');
      close.innerHTML = '&#10005;';
      close.addEventListener('click', closePanel);
      panelBody = document.createElement('div');
      panel.appendChild(close);
      panel.appendChild(panelBody);
      el.parentElement.appendChild(panel);
    }
    function closePanel(){
      if (!panel) return;
      panel.classList.remove('open');
      if (activeLine) { activeLine.setStyle({ color: activeBaseColor, weight: 4 }); activeLine = null; }
      map.flyToBounds(bounds, { padding: [24, 24] });
    }
    function openPanel(line, baseColor, html){
      ensurePanel();
      if (activeLine && activeLine !== line) activeLine.setStyle({ color: activeBaseColor, weight: 4 });
      activeLine = line; activeBaseColor = baseColor;
      line.setStyle({ color: COLORS.parking, weight: 6 });
      panelBody.innerHTML = html;
      panel.classList.add('open');
      var panelHeight = panel.getBoundingClientRect().height;
      map.flyToBounds(line.getBounds(), {
        paddingTopLeft: [24, 24],
        paddingBottomRight: [24, panelHeight + 24],
        maxZoom: 15
      });
    }

    var bounds = null;
    data.tracks.forEach(function(t){
      var baseColor = COLORS[t.color] || COLORS.teal;
      var line = L.polyline(t.points, {
        color: baseColor,
        weight: 4,
        opacity: data.tracks.length > 1 ? 0.85 : 0.9,
        lineJoin: 'round'
      }).addTo(map);
      bounds = bounds ? bounds.extend(line.getBounds()) : line.getBounds();

      if (t.href) {
        var href = isEu ? t.href.replace(/\.html$/, '.eu.html') : t.href;
        var sign = document.querySelector('.signpost-sign[href="' + t.href + '"]');
        var name = sign ? sign.querySelector('.signpost-name').textContent.trim() : t.href;
        var distanceKm = sign ? sign.dataset.distanceKm : null;
        var desnivelM = sign ? sign.dataset.desnivelM : null;
        var activity = sign ? sign.dataset.activity : null;
        var activityLabel = activity === 'bici' ? (isEu ? 'Bizikleta' : 'Bici')
          : activity === 'senderismo' ? (isEu ? 'Oinez' : 'Senderismo') : null;
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
        var chart = t.chart ? '<svg class="route-popup-chart" viewBox="0 0 1000 300" ' +
          'preserveAspectRatio="none"><path d="' + t.chart + '" fill="var(--teal-soft)"/></svg>' : '';
        var html = '<div class="route-popup">' + chart + '<h3>' + name + '</h3>' +
          '<div class="route-popup-facts">' + facts + '</div>' +
          '<div class="route-popup-dir">' + dirLabel + ': <b>' + directionLabel(t.points) + '</b></div>' +
          '<a href="' + href + '">' + seeLabel + ' &rarr;</a></div>';
        line.on('click', function(e){ L.DomEvent.stopPropagation(e); openPanel(line, baseColor, html); });
        line.on('mouseover', function(){ line.setStyle({ weight: 6 }); });
        line.on('mouseout', function(){ if (line !== activeLine) line.setStyle({ weight: 4 }); });
        var pathEl = line.getElement();
        if (pathEl) pathEl.style.cursor = 'pointer';
      }
    });

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

    function fit(){
      map.invalidateSize();
      map.fitBounds(bounds, { padding: [24, 24] });
    }
    fit();
    if ('ResizeObserver' in window) new ResizeObserver(fit).observe(el);
    else window.addEventListener('resize', fit);
  }).catch(function(err){
    if (window.console) console.error('No se pudo cargar el mapa:', err);
  });
})();
