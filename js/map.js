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

  fetch(el.dataset.mapSrc).then(function(r){ return r.json(); }).then(function(data){
    var map = L.map(el, {
      zoomControl: true,
      scrollWheelZoom: false,
      center: data.tracks[0].points[0],
      zoom: 13
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    }).addTo(map);

    var bounds = null;
    data.tracks.forEach(function(t){
      var line = L.polyline(t.points, {
        color: COLORS[t.color] || COLORS.teal,
        weight: 4,
        opacity: data.tracks.length > 1 ? 0.85 : 0.9,
        lineJoin: 'round'
      }).addTo(map);
      bounds = bounds ? bounds.extend(line.getBounds()) : line.getBounds();

      if (t.href) {
        var href = isEu ? t.href.replace(/\.html$/, '.eu.html') : t.href;
        line.on('click', function(){ window.location.href = href; });
        line.on('mouseover', function(){ line.setStyle({ weight: 6 }); });
        line.on('mouseout', function(){ line.setStyle({ weight: 4 }); });
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
