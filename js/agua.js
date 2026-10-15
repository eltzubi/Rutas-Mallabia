// El mapa de agua.html: solo los puntos de agua, sin ningun track.
//
// No pide nada: las coordenadas y el texto de cada globo salen de la lista
// que ya esta en la pagina (.agua-item, escrita por add_fuentes() en
// src/build.py desde data/fuentes.json), igual que js/map.js lee los nombres
// de los waypoints de la leyenda ya pintada. Asi la lista y el mapa no pueden
// decir cosas distintas, la pagina funciona sin JavaScript -- queda la lista
// con sus notas y sus enlaces -- y no hay una segunda descarga.
//
// Las capas estan copiadas de js/map.js a proposito: esa es una funcion de
// 1.100 lineas atada a los tracks, y partirla para compartir treinta era
// arriesgar las 118 fichas por una pagina. scripts/check_site.py comprueba
// que las cuatro URL de teselas sean identicas en los dos ficheros, asi que
// la copia no puede quedarse atras sin que salte.
(function(){
  var caja = document.querySelector('[data-fuentes-mapa]');
  var lista = document.getElementById('aguaLista');
  if (!caja || !lista) return;
  var isEu = document.documentElement.lang === 'eu';

  var items = Array.prototype.slice.call(lista.querySelectorAll('.agua-item'));
  if (!items.length) return;

  function texto(item, clase){
    var el = item.querySelector(clase);
    return el ? el.textContent.trim() : '';
  }

  var fuentes = items.map(function(item){
    return {
      item: item,
      lat: parseFloat(item.dataset.lat),
      lon: parseFloat(item.dataset.lon),
      aprox: item.dataset.aprox === '1',
      nombre: texto(item, '.agua-nombre'),
      aproxTexto: texto(item, '.agua-aprox'),
      nota: texto(item, '.agua-nota'),
      rutas: item.querySelector('.agua-rutas')
    };
  }).filter(function(f){ return isFinite(f.lat) && isFinite(f.lon); });
  if (!fuentes.length) return;

  function noDisponible(){
    caja.classList.add('map-unavailable');
    caja.setAttribute('aria-busy', 'false');
    caja.textContent = '';
    var p = document.createElement('p');
    p.setAttribute('role', 'status');
    p.textContent = isEu ?
      'Ezin izan da mapa kargatu. Iturrien zerrenda behean duzu.' :
      'No se ha podido cargar el mapa. Tienes la lista de fuentes debajo.';
    caja.appendChild(p);
  }

  if (typeof L === 'undefined') { noDisponible(); return; }

  var css = getComputedStyle(document.documentElement);
  function token(name, fallback){
    return css.getPropertyValue(name).trim() || fallback;
  }
  var TEAL = token('--teal', '#2FE0F5');
  var GROUND = token('--ground', '#0A0F0A');

  var map = L.map(caja, { zoomControl: true, scrollWheelZoom: false });

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
  var topoLayer = L.tileLayer('https://www.ign.es/wmts/mapa-raster?layer=MTN&style=default' +
    '&tilematrixset=GoogleMapsCompatible&Service=WMTS&Request=GetTile&Version=1.0.0' +
    '&Format=image/jpeg&TileMatrix={z}&TileCol={x}&TileRow={y}', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://www.ign.es" target="_blank" rel="noopener">Instituto Geogr&aacute;fico Nacional de Espa&ntilde;a</a>'
  });

  // Abre en el IGN, como las fichas: para buscar una fuente lo que situa son
  // los barrios, los arroyos y las curvas de nivel, no el callejero.
  var layerDefs = [
    { layer: topoLayer, label: isEu ? 'IGN mapa topografikoa' : 'Mapa topográfico del IGN', short: 'IGN' },
    { layer: cycleLayer, label: isEu ? 'Bizikleta' : 'Ciclista', short: isEu ? 'Bizi' : 'Bici' },
    { layer: osmLayer, label: isEu ? 'Kaleak' : 'Calles', short: isEu ? 'Kaleak' : 'Calles' },
    { layer: satLayer, label: isEu ? 'Satelitea' : 'Satélite', short: 'Sat' }
  ];
  var layerIndex = 0;
  layerDefs[layerIndex].layer.addTo(map);

  var layersBar = document.createElement('div');
  layersBar.className = 'map-layers';
  layersBar.setAttribute('role', 'group');
  layersBar.setAttribute('aria-label', isEu ? 'Mapa mota' : 'Tipo de mapa');

  // La capa vieja no se quita hasta que la nueva esta pintada: ver el mismo
  // comentario en js/map.js (CyclOSM tarda el triple y el mapa se quedaba en
  // blanco casi un segundo).
  function ponerCapa(i){
    if (i === layerIndex) return;
    var vieja = layerDefs[layerIndex].layer;
    var nueva = layerDefs[i].layer;
    layerIndex = i;
    layerBtns.forEach(function(b, j){
      b.classList.toggle('is-selected', j === layerIndex);
      b.classList.toggle('is-loading', j === layerIndex);
      b.setAttribute('aria-pressed', String(j === layerIndex));
    });
    nueva.addTo(map);
    var hecho = false;
    function listo(){
      if (hecho) return;
      hecho = true;
      clearTimeout(reloj);
      nueva.off('load', listo);
      if (vieja !== nueva && map.hasLayer(vieja)) map.removeLayer(vieja);
      layerBtns.forEach(function(b){ b.classList.remove('is-loading'); });
    }
    var reloj = setTimeout(listo, 3000);
    nueva.on('load', listo);
  }
  var layerBtns = layerDefs.map(function(def, i){
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'map-layer-btn' + (i === layerIndex ? ' is-selected' : '');
    b.setAttribute('aria-pressed', String(i === layerIndex));
    b.textContent = def.short;
    b.title = def.label;
    b.addEventListener('click', function(e){ e.stopPropagation(); ponerCapa(i); });
    layersBar.appendChild(b);
    return b;
  });
  caja.parentElement.appendChild(layersBar);

  var GOTA = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true">' +
             '<path d="M12 2.5c3.8 4.6 6 7.9 6 10.6a6 6 0 0 1-12 0c0-2.7 2.2-6 6-10.6z"/></svg>';

  function icono(aprox){
    var fondo = aprox ? 'transparent' : TEAL;
    var tinta = aprox ? TEAL : GROUND;
    var borde = aprox ? ('2px dashed ' + TEAL) : ('2px solid ' + GROUND);
    return L.divIcon({
      className: 'agua-marker',
      html: '<span style="display:flex;align-items:center;justify-content:center;' +
            'width:24px;height:24px;border-radius:50%;background:' + fondo + ';' +
            'border:' + borde + ';color:' + tinta + ';fill:currentColor;' +
            'box-shadow:0 0 0 1.5px ' + TEAL + ';">' + GOTA + '</span>',
      iconSize: [24, 24], iconAnchor: [12, 12]
    });
  }

  var marcadores = [];
  fuentes.forEach(function(f){
    var globo = document.createElement('div');
    globo.className = 'agua-popup';
    var h = document.createElement('p');
    h.className = 'agua-popup-nombre';
    h.textContent = f.nombre;
    globo.appendChild(h);
    if (f.aproxTexto) {
      var a = document.createElement('p');
      a.className = 'agua-popup-aprox';
      a.textContent = f.aproxTexto;
      globo.appendChild(a);
    }
    if (f.nota) {
      var n = document.createElement('p');
      n.className = 'agua-popup-nota';
      n.textContent = f.nota;
      globo.appendChild(n);
    }
    if (f.rutas) {
      var r = f.rutas.cloneNode(true);
      r.className = 'agua-popup-rutas';
      globo.appendChild(r);
    }
    var m = L.marker([f.lat, f.lon], { title: f.nombre, icon: icono(f.aprox) })
      .bindPopup(globo, { maxWidth: 260 })
      .addTo(map);
    marcadores.push(m);

    // Desde la lista al mapa: pulsar una fuente la centra y abre su globo.
    // Es lo que se busca al leer la lista en el movil -- donde cae esta.
    var nombre = f.item.querySelector('.agua-nombre');
    if (!nombre) return;
    var boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'agua-ver';
    boton.textContent = isEu ? 'Mapan ikusi' : 'Ver en el mapa';
    boton.addEventListener('click', function(){
      caja.scrollIntoView({
        behavior: (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)
          ? 'auto' : 'smooth',
        block: 'center'
      });
      map.setView([f.lat, f.lon], Math.max(map.getZoom(), 15));
      m.openPopup();
    });
    nombre.appendChild(boton);
  });

  map.fitBounds(L.featureGroup(marcadores).getBounds(), { padding: [34, 34] });
  caja.setAttribute('aria-busy', 'false');
})();
