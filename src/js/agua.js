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

  var css = getComputedStyle(document.querySelector('main') || document.documentElement);
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
  var satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.esri.com" target="_blank" rel="noopener">Esri</a>, Maxar'
  });
  var topoLayer = L.tileLayer('https://www.ign.es/wmts/mapa-raster?layer=MTN&style=default' +
    '&tilematrixset=GoogleMapsCompatible&Service=WMTS&Request=GetTile&Version=1.0.0' +
    '&Format=image/jpeg&TileMatrix={z}&TileCol={x}&TileRow={y}', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://www.ign.es" target="_blank" rel="noopener">Instituto Geogr&aacute;fico Nacional de Espa&ntilde;a</a>'
  });

  // Abre en el IGN, como las fichas: para buscar una fuente lo que situa son
  // los barrios, los arroyos y las curvas de nivel, no el callejero.
  // El topografico del Gobierno Vasco (geoEuskadi). Es la unica carta de
  // esta lista que la hace quien conoce el terreno: curvas de nivel mucho
  // mas finas que las del IGN, los caserios con su nombre uno a uno
  // (Etxebarri, Lexarraga) y los toponimos en euskera, que es como se
  // llaman. Llega a z18 y cubre las 66 rutas enteras, Gipuzkoa incluida
  // -- comprobado tesela a tesela en las cuatro esquinas del conjunto.
  // Licencia CC BY: «se permite cualquier uso si se menciona la autoria».
  // OPENTOPOMAP, en el sitio que ocupaba la de Euskadi. La pidio el autor:
  // «el mapa Euskadi no me dice nada; quiero nombres abundantes y mas
  // curvas de nivel, para que al mover el mapa se sepa donde andas
  // buscando». Y tenia razon, medido sobre LA MISMA tesela de Mallabia a
  // zoom 13, que es el zoom al que uno busca:
  //
  //   Euskadi (geoEuskadi topo)  3 nombres: Markina, Mallabia, Mendibil
  //   Bici (CyclOSM)             0 nombres, solo «BI-633»
  //   OpenTopoMap                8, Y CON SU ALTURA: Mendigana 467,
  //                              Mendibil 613, Olamendi 600, Arteta 514,
  //                              Ariznabar 592, Galarraga 415,
  //                              Trabakua 404, mas la BI-633
  //
  // La de Euskadi si rotulaba los caserios uno a uno y en euskera, pero
  // solo de z15 para arriba: a la distancia a la que uno busca, callaba.
  // Se probo ponerle encima el hibrido de geoEuskadi y a z13 saca los
  // mismos tres, asi que no arreglaba nada. El autor la quito al verlas
  // juntas: «quita Euskadi».
  //
  // Estaba descartada desde octubre porque sus CARRETERAS SON NARANJAS, el
  // mismo color que los trazados de bici. Sigue siendo verdad, pero pesa
  // menos que entonces: desde octubre los trazados llevan reborde oscuro.
  // Si vuelve a molestar en la portada, esta es la razon.
  //
  // Llega a z17 (de ahi para arriba no tiene teselas propias). La sirve un
  // proyecto de voluntarios, igual que CyclOSM, y su licencia pide citar a
  // OpenTopoMap y a OpenStreetMap: eso hace la atribucion.
  var openTopoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    subdomains: 'abc', maxZoom: 17,
    attribution: '&copy; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (CC-BY-SA), &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
  });
  // Los nombres sobre el satelite. Lo pidio el autor: «el mapa sat, ¿pueden
  // aparecer nombres?». Es una capa transparente de solo rotulos que se
  // enciende con el satelite y se apaga con el. Va encima de las teselas y
  // debajo de los trazados, que viven en otro panel.
  //
  // Se compararon dos sobre el mismo trozo de Berriz y Osmagain, a z12, z13
  // y z16, y se eligio el **hibrido de geoEuskadi**:

  // - Esri «World Boundaries and Places» pone solo los nombres y no toca la
  //   imagen, pero es **escuetisimo**: sobre toda la ruta de Zengotitagane,
  //   en 1280x900, saca **un solo rotulo** («Garai»).
  // - El hibrido de geoEuskadi saca **treinta y tantos** en ese mismo
  //   encuadre -- Askako, Sarrimendi, Urdaia, Axmakurra, Iturrizu,
  //   Zengotitagana, Kurutzetorri, Olatzamendi, Gaztelumendi, Osmagain,
  //   Sallobente, Besoita, Andikoa, Momoitio, Galarraga...-- mas los
  //   arroyos y los numeros de carretera.
  //
  // Se temia que pintara las carreteras de naranja y compitiera con los
  // tracks de bici (es por lo que se descarto OpenTopoMap), pero sobre la
  // foto las saca en **amarillo**, y el track va mas grueso y con flechas:
  // se distinguen. Comprobado en la pagina de verdad, no en una tesela
  // suelta. Pesa unos 10 kB por tesela y no anade ningun dominio nuevo, que
  // geoEuskadi ya sirve la capa «Euskadi».
  var nombresLayer = L.tileLayer('https://www.geo.euskadi.eus/geoeuskadi/rest/services/' +
    'U11/WMTS_HIBRIDO/MapServer/WMTS/tile/1.0.0/U11_WMTS_HIBRIDO/default/' +
    'GoogleMapsCompatible/{z}/{y}/{x}.png', {
    maxZoom: 18, zIndex: 300,
    attribution: '&copy; <a href="https://www.geo.euskadi.eus" target="_blank" rel="noopener">geoEuskadi</a> / Gobierno Vasco'
  });
  // Y la alternativa, que es la que usa la PORTADA: Esri «World Boundaries
  // and Places», solo nombres y sin pintar una sola carretera. Con las 66
  // rutas a la vez sobre la foto, las carreteras amarillas del hibrido se
  // enredaban con los trazados naranjas y verdes -- «se lia buena», dijo el
  // autor con la pantalla delante. En una ficha hay un solo track y ahi si
  // manda el de Euskadi, que trae treinta veces mas nombres.
  var nombresEsri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/' +
    'Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
    // sin attribution: la foto de debajo ya cita a Esri, y repetido salia
    // «© Esri, Maxar, © Esri».
    maxZoom: 19, zIndex: 300
  });
  var layerDefs = [
    { layer: topoLayer, label: isEu ? 'IGN mapa topografikoa' : 'Mapa topográfico del IGN', short: 'IGN' },
    { layer: cycleLayer, label: isEu ? 'Bizikleta' : 'Ciclista', short: isEu ? 'Bizi' : 'Bici' },
    { layer: openTopoLayer, label: isEu ? 'OpenTopoMap mapa topografikoa' : 'Mapa topográfico OpenTopoMap', short: 'Topo' },
    { layer: satLayer, label: isEu ? 'Satelitea' : 'Satélite', short: 'Sat', rotulos: nombresLayer }
  ];
  // Abre en Topo (OpenTopoMap), no en el IGN. Lo pidio el autor: «mapa agua
  // que abra en topo». Es la capa que mas nombres y mas curvas de nivel saca
  // al zoom al que uno busca, y aqui no hay ningun trazado naranja con el
  // que puedan enredarse sus carreteras: esta pagina solo pinta los puntos
  // de agua.
  var layerIndex = 2;
  layerDefs[layerIndex].layer.addTo(map);
  if (layerDefs[layerIndex].rotulos) layerDefs[layerIndex].rotulos.addTo(map);

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
    if (layerDefs[i].rotulos) layerDefs[i].rotulos.addTo(map);
    var hecho = false;
    function listo(){
      if (hecho) return;
      hecho = true;
      clearTimeout(reloj);
      nueva.off('load', listo);
      if (vieja !== nueva && map.hasLayer(vieja)) map.removeLayer(vieja);
      // los rotulos se van con su capa y no antes: si se quitaran ya, al
      // cambiar de capa desapareceran mientras la nueva aun carga.
      layerDefs.forEach(function(d, j){
      if (d.rotulos && j !== layerIndex && map.hasLayer(d.rotulos)) map.removeLayer(d.rotulos);
      });
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

  // La salida de Trabakua, en rojo: situa el resto. Va antes que las fuentes
  // para que ninguna quede debajo de ella -- hay una fuente a 7 m, la del
  // alto, y al alejarse se montan. La salida va en aro hueco y grande para que
  // la gota de la fuente se siga viendo dentro del aro.
  var marcadores = [];
  if (caja.dataset.salida) {
    var salida = caja.dataset.salida.split(',').map(Number);
    if (salida.length === 2 && isFinite(salida[0]) && isFinite(salida[1])) {
      marcadores.push(L.marker(salida, {
        title: caja.dataset.markerTitle || '',
        icon: L.divIcon({
          className: 'agua-marker',
          html: '<span style="display:block;width:32px;height:32px;border-radius:50%;' +
                'background:transparent;border:3px solid #E24C4C;' +
                'box-shadow:0 0 0 1.5px rgba(226,76,76,.35);"></span>',
          iconSize: [32, 32], iconAnchor: [16, 16]
        })
      }).addTo(map));
    }
  }

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
      // La barra de capas flota sobre el mapa y tapaba el nombre del globo
      // cuando se abria arriba del todo. El relleno de autoPan le deja sitio.
      .bindPopup(globo, {
        maxWidth: 260,
        autoPanPaddingTopLeft: L.point(14, 74),
        autoPanPaddingBottomRight: L.point(14, 24)
      })
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

  var limites = L.featureGroup(marcadores).getBounds();
  map.fitBounds(limites, { padding: [34, 34] });

  // Ampliar el mapa, como en las fichas: mismo boton, misma clase y el mismo
  // apano del ancho -- clientWidth y no 100vw, que incluye la barra de
  // desplazamiento y creaba desbordamiento horizontal.
  var movido = false;
  ['wheel', 'touchstart', 'dblclick', 'pointerdown'].forEach(function(ev){
    caja.addEventListener(ev, function(){ movido = true; }, { passive: true });
  });
  function anchoUtil(){
    caja.parentElement.style.setProperty(
      '--map-viewport-width', document.documentElement.clientWidth + 'px');
  }
  anchoUtil();
  window.addEventListener('resize', anchoUtil, { passive: true });
  var botonAmpliar = caja.parentElement.querySelector('.map-expand-btn');
  if (botonAmpliar) {
    botonAmpliar.addEventListener('click', function(){
      anchoUtil();
      var abierto = caja.parentElement.classList.toggle('is-expanded');
      botonAmpliar.classList.toggle('is-active', abierto);
      botonAmpliar.setAttribute('aria-label', abierto ?
        botonAmpliar.dataset.labelCollapse : botonAmpliar.dataset.labelExpand);
      caja.parentElement.scrollIntoView({
        behavior: (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)
          ? 'auto' : 'smooth',
        block: 'start'
      });
      // Al ampliar y al reducir se vuelve a ver todo: es para lo que sirve.
      movido = false;
      map.invalidateSize();
      map.fitBounds(limites, { padding: [34, 34] });
    });
  }
  // La caja cambia de tamanio al ampliar y al girar el movil, y Leaflet no se
  // entera solo.
  if ('ResizeObserver' in window) {
    new ResizeObserver(function(){
      if (!caja.clientWidth || !caja.clientHeight) return;
      map.invalidateSize();
      if (!movido) map.fitBounds(limites, { padding: [34, 34] });
    }).observe(caja);
  }
  caja.setAttribute('aria-busy', 'false');
})();
