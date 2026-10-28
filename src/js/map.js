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
        // Y se reencuadra: ampliar es para ver la ruta entera, no el trozo
        // en el que te hubieras quedado despues de arrastrar o hacer zoom.
        if (resetView) { userMoved = false; resetView(); }
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
  // La ficha toma el color de su actividad (verde a pie, naranja en bici),
  // leido del <main data-activity> que escribe build.py -- la misma fuente
  // que colorea las tarjetas de la portada. Sin atributo (portada, paginas
  // sin ficha) no cambia nada.
  var actEl = document.querySelector('main[data-activity]');
  var actColor = actEl ? (actEl.getAttribute('data-activity') === 'bici' ? COLORS.teal : COLORS.violet) : null;

  // Waypoint labels come from the elevation legend, in the same order.
  // Acotado a la leyenda del mapa: una ficha lleva dos leyendas iguales (la
  // del perfil y la del mapa), asi que buscando en todo el documento salian
  // el doble de items que waypoints y la correspondencia se sostenia de puro
  // milagro -- el dia que las dos dejasen de coincidir, etiquetas cambiadas.
  var legendScope = el.closest('.map-section') || document;
  var wpNames = Array.prototype.filter.call(
    legendScope.querySelectorAll('.elev-legend-item'),
    // El renglon del agua vive en la misma lista y no es un punto numerado.
    // Se filtra por .gota y no con :not(:has(.gota)) porque :has() no esta
    // en todos los navegadores que abren esto en el monte.
    function(item){ return !item.querySelector('.gota'); }
  ).map(function(item){ return item.textContent.replace(/^\s*\d+\s*/, '').trim(); });

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
    // route's own map alike. Three free layers, none needing an API key:
    // the Spanish IGN's topographic map (contour lines, named streams and
    // villages), CyclOSM (bike-oriented rendering: contour lines, named
    // peaks and streams, every track and path drawn differently) and Esri
    // World Imagery (aerial photo). Same three everywhere, opening in
    // CyclOSM.
    var cycleLayer = L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
      maxZoom: 20,
      attribution: '&copy; <a href="https://www.cyclosm.org" target="_blank" rel="noopener">CyclOSM</a>, &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
    });
    var satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.esri.com" target="_blank" rel="noopener">Esri</a>, Maxar'
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
    // La portada abre con las calles y las fichas con el IGN, que es como lo
    // quiere el autor: en la vista de conjunto, con las 57 rutas a la vez, lo
    // que situa es el callejero; en una ruta, los rios, los toponimos y las
    // curvas de nivel del IGN. El mapa no cambia solo nunca: ni al acercarse
    // ni al elegir una ruta. Se probaron las dos cosas y el autor las quito:
    // que el mapa cambie debajo sin haberlo pedido desconcierta mas de lo que
    // ayuda. Solo lo cambian los botones.
    var esPortada = el.dataset.mapSrc.split('?')[0] === 'data/trailhead.json';
    var LABEL_MIN_ZOOM = 12;   // el zoom al que salen los kilometros de cada ruta
    // Los nombres sobre el satelite. Lo pidio el autor: «el mapa sat, ¿pueden
    // aparecer nombres?». Es una capa transparente de solo rotulos que se
    // enciende con el satelite y se apaga con el. Va encima de las teselas y
    // debajo de los trazados, que viven en otro panel.
    //
    // Se compararon dos sobre el mismo trozo de Berriz y Osmagain, a z12, z13
    // y z16, y se eligio el hibrido de geoEuskadi:
    //
    // - Esri «World Boundaries and Places» pone solo los nombres y no toca la
    //   imagen, pero es ESCUETISIMO: sobre toda la ruta de Zengotitagane, en
    //   1280x900, saca UN SOLO rotulo («Garai»).
    // - El hibrido de geoEuskadi saca treinta y tantos en ese mismo encuadre
    //   -- Askako, Sarrimendi, Urdaia, Axmakurra, Iturrizu, Zengotitagana,
    //   Kurutzetorri, Olatzamendi, Gaztelumendi, Osmagain, Sallobente,
    //   Besoita, Andikoa, Momoitio, Galarraga... -- mas los arroyos y los
    //   numeros de carretera.
    //
    // Se temia que pintara las carreteras de naranja y compitiera con los
    // tracks de bici (es por lo que se descarto OpenTopoMap), pero sobre la
    // foto las saca en AMARILLO, y el track va mas grueso y con flechas: se
    // distinguen. Comprobado en la pagina de verdad y no en una tesela
    // suelta. Pesa unos 10 kB por tesela y no anade ningun dominio nuevo,
    // que geoEuskadi ya sirve la capa «Euskadi».
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
      { layer: satLayer, label: isEu ? 'Satelitea' : 'Satélite', short: 'Sat', rotulos: esPortada ? nombresEsri : nombresLayer }
    ];
    // Las capas, a la vista: antes eran un icono de tres rombos que abria un
    // menu, y un icono que no dice que hace no lo pulsa nadie. Ahora son
    // botones, con el activo encendido, como en cualquier mapa de movil.
    //
    // Las mismas tres en la portada y en una ficha, y las dos abren en Bici.
    // En octubre se saco la Bici de las fichas y se puso un callejero porque
    // el autor avisó de que «al mapa bici le cuesta abrir mucho»; despues
    // dijo que la tardanza le da igual («no me preocupa lo que tarde en el
    // monte, la ruta la organizo en casa»), asi que la razon para no usarla
    // desaparecio. Y es el mapa que quiere: comparados los ocho candidatos
    // sobre el mismo trozo de Zaldibar, CyclOSM es el que mas informacion
    // trae -- curvas de nivel con su altura, todas las cimas rotuladas, los
    // arroyos con nombre, y cada pista y sendero con su propio trazo. Se
    // probaron y se descartaron el callejero de OSM, el estilo Humanitarian
    // («no me gusta este mapa»), OSM Francia y Alemania, OpenTopoMap (sus
    // carreteras son naranjas, el mismo color que los tracks de bici) y MTB
    // Map (el que mas toponimos saca, pero pinta las carreteras en rojo y
    // amarillo chillon y lo sirve un servidor de aficionados sin condiciones
    // de uso publicadas). CyclOSM-lite y 4UMaps estan muertos: devuelven
    // error en las doce teselas.
    var layerIndex = 1;
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
      if (layerDefs[layerIndex].rotulos) layerDefs[layerIndex].rotulos.addTo(map);
    }
    var layersBar = document.createElement('div');
    layersBar.className = 'map-layers';
    layersBar.setAttribute('role', 'group');
    layersBar.setAttribute('aria-label', isEu ? 'Mapa mota' : 'Tipo de mapa');
    // Al cambiar de capa, la vieja no se quita hasta que la nueva esta
    // pintada. Antes se quitaba primero, y con el mapa ciclista -- que lo
    // sirve un servidor de voluntarios y tarda el triple que los demas (0,8 s
    // por tesela frente a 0,3) -- el mapa se quedaba en blanco casi un
    // segundo: parecia roto. Leaflet pone la capa nueva por encima de la
    // vieja, asi que la va tapando segun llega.
    var quitarPendiente = null;
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
      if (!capaPuesta) return;
      if (quitarPendiente) { quitarPendiente(); quitarPendiente = null; }
      nueva.addTo(map);
      if (layerDefs[i].rotulos) layerDefs[i].rotulos.addTo(map);
      var hecho = false;
      function listo(){
        if (hecho) return;
        hecho = true;
        clearTimeout(reloj);
        nueva.off('load', listo);
        quitarPendiente = null;
        if (vieja !== nueva && map.hasLayer(vieja)) map.removeLayer(vieja);
        // los rotulos se van con su capa y no antes: si se quitaran ya, al
        // cambiar de capa desapareceran mientras la nueva aun carga.
        layerDefs.forEach(function(d, j){
        if (d.rotulos && j !== layerIndex && map.hasLayer(d.rotulos)) map.removeLayer(d.rotulos);
        });
        layerBtns.forEach(function(b){ b.classList.remove('is-loading'); });
      }
      // Y si las teselas no llegan nunca (sin cobertura en el monte), se
      // quita igual pasados tres segundos: mejor el fondo vacio que dos
      // mapas superpuestos para siempre.
      var reloj = setTimeout(listo, 3000);
      nueva.on('load', listo);
      quitarPendiente = listo;
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

    // «Rutas»: un interruptor para quitar los trazados y ver el mapa a pelo.
    // Lo pidio el autor -- sobre el satelite, y donde se juntan varias rutas,
    // los trazados tapan justo lo que quiere mirar. Va en la misma pastilla
    // que las capas, detras de la raya, como el de la pendiente. No borra
    // nada: solo los esconde, y el trazado que el visitante este dibujando
    // (.draw-line) se queda, que para eso lo esta dibujando.
    var rutasBtn = document.createElement('button');
    rutasBtn.type = 'button';
    rutasBtn.className = 'map-layer-btn map-rutas-btn is-selected';
    // En un movil estrecho las cuatro capas ya van justas: ahi el boton se
    // queda en un ojo, y el rotulo solo sale cuando hay sitio.
    rutasBtn.innerHTML = '<span class="rutas-txt">' + (isEu ? 'Ibilbideak' : 'Rutas') + '</span>' +
      '<svg class="rutas-ico" width="15" height="15" viewBox="0 0 24 24" fill="none"' +
      ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"' +
      ' aria-hidden="true"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/>' +
      '<circle cx="12" cy="12" r="3"/></svg>';
    rutasBtn.setAttribute('aria-label', isEu ? 'Ibilbideak' : 'Rutas');
    rutasBtn.title = isEu ? 'Ibilbideak ezkutatu eta mapa soilik ikusi'
                          : 'Esconder las rutas y ver solo el mapa';
    rutasBtn.setAttribute('aria-pressed', 'true');
    rutasBtn.addEventListener('click', function(e){
      e.stopPropagation();
      var ocultas = el.classList.toggle('sin-rutas');
      rutasBtn.classList.toggle('is-selected', !ocultas);
      rutasBtn.setAttribute('aria-pressed', String(!ocultas));
      rutasBtn.title = ocultas
        ? (isEu ? 'Ibilbideak berriro erakutsi' : 'Volver a ver las rutas')
        : (isEu ? 'Ibilbideak ezkutatu eta mapa soilik ikusi'
                : 'Esconder las rutas y ver solo el mapa');
    });
    ponExtra(rutasBtn);

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
    // Las dos versiones de la ficha abierta, para poder cambiar de una a otra
    // si la ventana cruza los 768 px sin cerrarla.
    var fichaHtml = null;
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
    // Con el mapa a pantalla entera, el boton de volver arriba cae encima de
    // el (abajo a la derecha). El modo de dibujar ya lo esconde por lo mismo.
    var botonArriba = document.getElementById('toTop');
    // Con una ruta elegida, los kilometros de las otras 64 siguen ahi y
    // ensucian justo lo que el visitante ha ido a mirar. Mientras la ficha
    // este abierta solo se ve la etiqueta de la suya; al cerrarla vuelven
    // todas. Lo pidio el autor: «quedarse solo en la ruta limpia».
    var labelSoloHref = null;
    // La capa de pastillas agrupadas. Va declarada AQUI y no junto a su
    // funcion, que esta mas abajo: updateLabelVisibility() se llama durante
    // el montaje, antes de llegar a aquella linea, y un «var x = null» alli
    // volvia a poner la variable a cero DESPUES de que la primera pasada ya
    // hubiera creado la capa. La referencia se perdia y los marcadores se
    // quedaban huerfanos en el mapa: con 66 rutas salian grupos sumando 100.
    var grupoCapa = null;
    // La tira de «lo que tienes delante». Declarada AQUI por lo mismo que
    // grupoCapa, y es que se repitio el fallo: pintaCercanas() se llama
    // durante el montaje, antes de llegar a su funcion, asi que un
    // «var tiraCercanas = null» alla abajo borraba la referencia despues de
    // que la primera pasada ya hubiera creado la tira -- y se creaba una
    // segunda. Salian dos tiras, una viva y otra congelada con 22 fichas.
    var tiraCercanas = null;
    var firmaTira = null;   // la firma, en variable y NO en dataset
    // La caja que envuelve al mapa: es la que crece con la ficha abierta.
    // Solo existe en la portada; en una ficha de ruta no hay panel.
    var marcoMapa = el.closest ? el.closest('.route-map-box') : null;

    // Con una ruta elegida, el mapa se queda con la pantalla entera y la
    // ficha se pone en un lateral, como en AllTrails: lo pidio el autor con
    // esa pantalla delante («el mapa ocupa la pantalla entera»). Es la misma
    // mecanica que el modo de dibujar, ya probada ahi: se saca la caja de su
    // columna centrada con un margen negativo y se le da el alto que queda
    // bajo la cabecera pegajosa.
    //
    // Solo de 768 px en adelante. Por debajo manda lo que el autor eligio en
    // octubre -- caja a 72svh y ficha abajo --, que ahi un lateral deja una
    // tira de 134 px donde los textos se parten.
    var CABECERA_FICHA = 62;
    function reduceMovimiento(){
      return !!(window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    }
    function esLateral(){
      return !!(window.matchMedia && window.matchMedia('(min-width:768px)').matches);
    }
    function aPantallaEntera(){
      if (!marcoMapa) return;
      var abajo = 0, barra = document.querySelector('.finder-toolbar');
      if (barra) {
        var r = barra.getBoundingClientRect();
        if (getComputedStyle(barra).position === 'fixed' &&
            r.bottom > window.innerHeight - 6) abajo = r.height;
      }
      // El ancho sale de clientWidth y no de 100vw: 100vw cuenta la barra de
      // desplazamiento y dejaria la pagina moviendose de lado.
      marcoMapa.style.marginLeft = '0px';
      marcoMapa.style.width = '';
      var izq = marcoMapa.getBoundingClientRect().left;
      marcoMapa.style.marginLeft = (-izq) + 'px';
      marcoMapa.style.width = document.documentElement.clientWidth + 'px';
      marcoMapa.style.borderRadius = '0';
      marcoMapa.style.aspectRatio = 'auto';
      marcoMapa.style.height =
        Math.max(300, window.innerHeight - CABECERA_FICHA - abajo - 14) + 'px';
    }
    function ponPleno(si){
      if (!marcoMapa) return;
      marcoMapa.classList.toggle('ficha-pleno', !!si);
      document.body.classList.toggle('mapa-pleno', !!si);
      if (si) sueltaPantallaEntera();   // manda el CSS, no los estilos en linea
    }
    function sueltaPantallaEntera(){
      if (!marcoMapa) return;
      marcoMapa.style.aspectRatio = '';
      marcoMapa.style.height = '';
      marcoMapa.style.marginLeft = '';
      marcoMapa.style.width = '';
      marcoMapa.style.borderRadius = '';
    }
    // Si se gira el movil o se cambia el tamano de la ventana con la ficha
    // abierta, la caja tiene que volver a cuadrar. Y si al redimensionar se
    // cruza el corte de 768 px, se pasa de un modo al otro sin cerrarla.
    var alRedimensionarFicha = null;
    function vigilaTamanoFicha(encender){
      if (encender && !alRedimensionarFicha) {
        alRedimensionarFicha = function(){
          if (!panel || !panel.classList.contains('open')) return;
          var lat = esLateral();
          el.classList.toggle('ficha-lateral', lat);
          ponPleno(!lat);
          if (lat) aPantallaEntera();
          if (fichaHtml) {
            var quiere = lat ? fichaHtml.amplia : fichaHtml.breve;
            if (panelBody.innerHTML !== quiere) panelBody.innerHTML = quiere;
          }
          map.invalidateSize({ animate: false });
        };
        window.addEventListener('resize', alRedimensionarFicha);
      } else if (!encender && alRedimensionarFicha) {
        window.removeEventListener('resize', alRedimensionarFicha);
        alRedimensionarFicha = null;
      }
    }

    var vigilaFicha = null;
    function marcaAltoFicha(alto){
      el.style.setProperty('--ficha-alto', Math.round(alto) + 'px');
      if (vigilaFicha || typeof ResizeObserver === 'undefined') return;
      // getBoundingClientRect y no contentRect: el panel lleva 16 px de
      // relleno arriba y abajo, y contentRect los deja fuera.
      vigilaFicha = new ResizeObserver(function(){
        if (!el.classList.contains('con-ficha')) return;
        el.style.setProperty('--ficha-alto',
          Math.round(panel.getBoundingClientRect().height) + 'px');
      });
      vigilaFicha.observe(panel);
    }

    function closePanel(){
      if (!panel || !panel.classList.contains('open')) return;
      var returnFocus = panel.contains(document.activeElement);
      panel.classList.remove('open');
      panel.hidden = true;
      el.classList.remove('con-ficha');
      el.classList.remove('ficha-lateral');
      vigilaTamanoFicha(false);
      if (marcoMapa && marcoMapa.classList.contains('ficha-abierta')) {
        marcoMapa.classList.remove('ficha-abierta');
      }
      ponPleno(false);
      sueltaPantallaEntera();
      if (botonArriba) botonArriba.style.display = '';
      map.invalidateSize({ animate: false });
      if (viewFab) viewFab.classList.remove('is-hidden-behind-panel');
      if (activeLine) {
        var path = activeLine.getElement();
        activeLine.setStyle({ color: activeBaseColor, weight: 4, opacity: baseOpacity });
        if (path) {
          path.setAttribute('aria-pressed', 'false');
          if (returnFocus) path.focus({ preventScroll: true });
        }
        activeLine = null;
        labelSoloHref = null;
        updateLabelVisibility();
        Object.keys(hrefToLine).forEach(function(href){
          var entry = hrefToLine[href];
          var entryPath = entry.line.getElement();
          var hidden = entryPath && entryPath.getAttribute('aria-hidden') === 'true';
          entry.line.setStyle({
            color: entry.currentColor,
            weight: pesoTrack,
            opacity: hidden ? 0.06 : baseOpacity
          });
          if (entry.reborde) entry.reborde.setStyle({ opacity: hidden ? 0.04 : 0.55 });
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
      labelSoloHref = null;
      Object.keys(hrefToLine).forEach(function(href){
        var entry = hrefToLine[href];
        var entryPath = entry.line.getElement();
        var hidden = entryPath && entryPath.getAttribute('aria-hidden') === 'true';
        if (entry.line === line) {
          labelSoloHref = href;
          entry.line.setStyle({ color: COLORS.parking, weight: 3, opacity: 1 });
          if (entry.line.bringToFront) entry.line.bringToFront();
        } else {
          entry.line.setStyle({ opacity: hidden ? 0.06 : 0.22, weight: pesoTrack });
        }
        // El reborde se apaga con su trazado: si no, al elegir una ruta
        // quedarian 64 lineas oscuras marcando las que estan apagadas.
        if (entry.reborde) entry.reborde.setStyle({
          opacity: hidden ? 0.04 : (entry.line === line ? 0.55 : 0.1) });
      });
      updateLabelVisibility();
      line.getElement().setAttribute('aria-pressed', 'true');
      fichaHtml = html;
      panelBody.innerHTML = esLateral() ? html.amplia : html.breve;
      panel.hidden = false;
      panel.classList.add('open');
      if (viewFab) viewFab.classList.add('is-hidden-behind-panel');
      var panelHeight = panel.getBoundingClientRect().height;
      // La linea de creditos de Leaflet va en z-index 1000 y el panel en 500,
      // asi que caia justo encima del enlace «Ver ruta completa» y lo tapaba
      // -- lo vio el autor en su movil. El panel sube por encima de los
      // controles y los creditos se corren hacia arriba lo que mide el
      // panel, que no se pueden esconder: son la atribucion de OSM.
      //
      // La altura se vuelve a mirar con un ResizeObserver y no solo aqui: la
      // foto de la ficha todavia no ha colocado cuando se mide, y el panel
      // crece despues. Sin eso, los creditos se quedaban unos pixeles bajos
      // y seguian metidos debajo del panel.
      marcaAltoFicha(panelHeight);
      el.classList.add('con-ficha');
      var lateral = esLateral();
      el.classList.toggle('ficha-lateral', lateral);
      // Y la caja crece, que es lo que de verdad arregla el «tapa el mapa»
      // (solo por debajo de 768 px; lo decide el CSS). Hay que avisar a
      // Leaflet del tamano nuevo ANTES de encuadrar, o encuadra sobre el
      // alto viejo y la ruta se queda pequena en la mitad de arriba.
      if (marcoMapa) {
        marcoMapa.classList.add('ficha-abierta');
        // Pantalla completa en las dos, que es lo que pidio el autor: la caja
        // sale de su columna centrada y se queda con todo lo que hay bajo la
        // cabecera pegajosa (y, en el movil, sobre la barra fija de abajo).
        // Lo que cambia con el ancho es donde va la ficha: a un lado de 768
        // en adelante, y abajo por debajo.
        // En el movil, pantalla completa de verdad: la caja se pone fija
        // ocupando la ventana entera y se esconden la cabecera y la barra de
        // abajo (lo hace el CSS con estas dos clases). Asi no hay que
        // calcular ningun desplazamiento. En el ordenador se queda la caja a
        // lo ancho bajo la cabecera, con la ficha a un lado.
        ponPleno(!lateral);
        if (lateral) {
          aPantallaEntera();
          window.scrollTo({
            top: Math.max(0, marcoMapa.getBoundingClientRect().top +
                             window.pageYOffset - CABECERA_FICHA),
            behavior: reduceMovimiento() ? 'auto' : 'smooth'
          });
        }
        if (botonArriba) botonArriba.style.display = 'none';
        map.invalidateSize({ animate: false });
        panelHeight = panel.getBoundingClientRect().height;
        marcaAltoFicha(panelHeight);
      }
      vigilaTamanoFicha(true);
      // Con el panel en un lateral el hueco que hay que dejar es de ancho,
      // no de alto: si no, la ruta se encuadra por debajo de el.
      var anchoPanel = lateral ? Math.round(panel.getBoundingClientRect().width) : 0;
      var vuela = function(){
        if (!panel.classList.contains('open')) return;
        map.flyToBounds(line.getBounds(), {
          paddingTopLeft: [anchoPanel + 24, 24],
          paddingBottomRight: [24, lateral ? 24 : panelHeight + 24],
          maxZoom: 15,
          animate: !reduceMovimiento()
        });
      };
      // Dos fotogramas de espera antes de encuadrar: al crecer la caja salta
      // el ResizeObserver de fit(), que llama a invalidateSize(), y eso corta
      // el vuelo en seco -- la ruta se quedaba sin acercar, con el mapa en la
      // vista de conjunto. El ResizeObserver corre tras el calculo de estilos
      // y antes de pintar, asi que al segundo fotograma ya ha pasado.
      if (typeof requestAnimationFrame === 'function') {
        requestAnimationFrame(function(){ requestAnimationFrame(vuela); });
      } else {
        vuela();
      }
      if (keyboard) panelClose.focus({ preventScroll: true });
    }

    var bounds = null;
    var hrefToLine = {};
    var hrefToLabel = {};
    var labelFilterVisible = {}; // href -> false solo cuando el filtro lo oculta
    // Con las 46 rutas a la vista de conjunto, mostrar las etiquetas desde el
    // primer momento las amontona todas sobre Trabakua. Se quedan ocultas
    // hasta que el visitante se acerca de verdad a una zona del mapa.
    // Los trazados de la portada van algo por debajo del opaco del todo: con
    // los 66 a la vez, y sobre el verde y el naranja fuertes del mapa ciclista,
    // al 100 % el autor los veia duros («hazlos un poco mas suaves, solo un
    // poquito»). El reborde oscuro es el que da la definicion, asi que bajar
    // esto no devuelve el problema de antes. En una ficha, con un solo track y
    // reborde blanco, se queda opaco.
    var baseOpacity = (data.tracks.length === 1 && !track0bis(data)) ? 1 : 0.85;
    // El grosor no es fijo en la portada: ver mas abajo «ajustaGrosor».
    var pesoTrack = 4.5;
    var pesoReborde = 8;
    // Un reborde debajo del trazado. En las fichas es blanco y ancho; en la
    // portada, oscuro y algo mas fino. El verde de «a pie» es un lima que
    // sobre el verde del campo del callejero casi no se veia, y el naranja
    // se confundia con las carreteras naranjas del IGN -- el autor lo dijo:
    // «el color en el mapa index es pobre». Se compararon cuatro arreglos
    // (subir opacidad y grosor, este reborde, y colores mas vivos) y este es
    // el unico que arregla las dos capas sin tocar la paleta de la web.
    // Antes la portada no lo llevaba por no dibujar 57 lineas mas.
    var unaSola = data.tracks.length === 1 && !track0bis(data);
    // Los rebordes van en su propio panel, por debajo del de los trazados:
    // asi ninguno puede quedar por encima del track de otra ruta, cosa que
    // pasaria si se intercalaran en el mismo panel.
    if (!unaSola && map.createPane) {
      var panelReborde = map.createPane('rebordes');
      panelReborde.style.zIndex = 395;
      panelReborde.style.pointerEvents = 'none';
    }
    data.tracks.forEach(function(t){
      var baseColor = COLORS[t.color] || actColor || COLORS.teal;
      var reborde = null;
      if (unaSola) {
        L.polyline(t.points, {
          color: '#ffffff', weight: 7, opacity: 0.75,
          lineJoin: 'round', lineCap: 'round', interactive: false
        }).addTo(map);
      } else {
        reborde = L.polyline(t.points, {
          color: '#0B1020', weight: pesoReborde, opacity: 0.55, pane: 'rebordes',
          lineJoin: 'round', lineCap: 'round', interactive: false
        }).addTo(map);
      }
      var line = L.polyline(t.points, {
        color: baseColor,
        weight: pesoTrack,
        opacity: baseOpacity,
        lineJoin: 'round'
      }).addTo(map);
      // El conjunto necesita su propia caja: extend() modifica el objeto.
      // Compartir la caja de la primera linea la hacia abarcar todas las rutas.
      bounds = bounds ? bounds.extend(line.getBounds()) : line.getBounds().pad(0);

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
        // Dos versiones de la ficha, y manda el sitio que hay:
        //
        // - **Breve** (movil, ficha abajo): solo nombre, datos y enlace. La
        //   foto y el perfil se comian 195 px de un mapa que en un movil
        //   mide 311 -- el 63 % --, el autor se quejo de que tapaba, se le
        //   enseñaron cuatro maneras medidas y eligio esta.
        // - **Amplia** (ordenador, panel lateral): con la foto y el perfil.
        //   En una columna alta sobra sitio, y es lo que el autor pidio al
        //   enseñar la pantalla de AllTrails: «si hace falta clona cosas de
        //   la pagina». Aqui no repiten -- en el lateral no se ve la tarjeta
        //   de la que salen.
        //
        // La foto se clona de la propia tarjeta: asi no hay que deducir el
        // fichero del href (en euskera acaba en .eu.html), el alt ya viene en
        // su idioma, y el navegador no descarga nada que no tuviera ya.
        var pic = sign && sign.querySelector('.route-card-photo picture');
        var foto = pic ? '<div class="route-popup-photo">' + pic.outerHTML + '</div>' : '';
        var perfil = t.chart ? '<svg class="route-popup-chart" viewBox="0 0 1000 300" ' +
          'preserveAspectRatio="none" aria-hidden="true"><path d="' + t.chart +
          '" fill="var(--teal-soft)"/></svg>' : '';
        // La linea de resumen de la tarjeta, clonada tal cual (ya viene en
        // su idioma). Solo en el panel lateral: en el movil la ficha tiene
        // que seguir cabiendo en dos dedos de alto.
        var desc = sign && sign.querySelector('.route-card-desc');
        var resumen = desc ? '<p class="route-popup-desc">' + desc.innerHTML + '</p>' : '';
        var datos = '<div class="route-popup-facts">' + facts + '</div>' +
          '<a href="' + href + '">' + seeLabel + ' &rarr;</a></div>';
        var html = {
          breve: '<div class="route-popup"><h3>' + name + '</h3>' + datos,
          amplia: '<div class="route-popup">' + foto + perfil +
                  '<h3>' + name + '</h3>' + resumen + datos
        };
        line.on('click', function(e){ L.DomEvent.stopPropagation(e); openPanel(line, hrefToLine[t.href].currentColor, html); });
        line.on('mouseover', function(){ if (!activeLine) line.setStyle({ weight: pesoTrack + 1.5 }); });
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
          labelMarker.on('mouseover', function(){ if (!activeLine) line.setStyle({ weight: pesoTrack + 1.5 }); });
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
          pathEl.addEventListener('focus', function(){ if (!activeLine) line.setStyle({ weight: pesoTrack + 1.5 }); });
          pathEl.addEventListener('blur', function(){ if (!activeLine) line.setStyle({ weight: 4 }); });
        }
        hrefToLine[t.href] = { line: line, reborde: reborde, baseColor: baseColor,
          activity: activity, currentColor: baseColor,
          // para la tira de «lo que tienes delante»: el nombre y los km salen de
          // la tarjeta de la portada, que ya esta en la pagina y en su idioma
          nombre: name, km: distanceKm, desnivel: desnivelM, puntos: t.points,
          foto: (sign && sign.querySelector('.route-card-photo img') &&
                 sign.querySelector('.route-card-photo img').getAttribute('src')) || '',
          abre: function(){ openPanel(line, hrefToLine[t.href].currentColor, html); } };
      }
    });

    // ---- El grosor, segun lo lejos que se mire ----------------------------
    // Lo pidio el autor: con las 66 rutas a la vez y el mapa entero a la
    // vista, «ocupan mucho» y se juntan en una mancha naranja y verde. De
    // cerca pasa justo lo contrario: una linea fina cuesta de ver sobre el
    // satelite y de acertarle con el dedo. Asi que la linea se afina al
    // alejarse y recupera su grosor al acercarse, en vez de elegir un numero
    // que este mal en los dos sitios. Solo en la portada: una ficha tiene un
    // track y no hay mancha que deshacer.
    function pesosDeZoom(z){
      // Por debajo del 11 el reborde se va del todo (grosor 0, que en SVG no
      // dibuja nada). Lo pidio el autor y tiene sentido: ahi las 66 rutas
      // estan tan enredadas que el reborde no separa nada, solo engorda la
      // mancha. La portada abre en zoom 10, asi que lo primero que se ve es
      // esto. Se apaga con el grosor y no con la opacidad a proposito: la
      // opacidad del reborde la llevan el filtro y la ficha abierta, y
      // tocarla aqui se pisaria con ellos.
      if (z <= 10) return [2.5, 0];    // la vista de conjunto, sin reborde
      if (z <= 12) return [2.5, 4];    // todo el mapa: 66 trazados a la vez
      if (z >= 14) return [3.5, 6];    // una zona
      return [3, 5];                   // el escalon de en medio
    }
    function ajustaGrosor(){
      var p = pesosDeZoom(map.getZoom());
      // Los dos, no solo el trazado: entre el zoom 10 y el 12 el trazado mide
      // igual y lo que cambia es el reborde.
      if (p[0] === pesoTrack && p[1] === pesoReborde) return;
      pesoTrack = p[0];
      pesoReborde = p[1];
      Object.keys(hrefToLine).forEach(function(h){
        var e = hrefToLine[h];
        // Solo el grosor: la opacidad la llevan el filtro y la ficha abierta,
        // y pisarla aqui encenderia rutas que estan apagadas a proposito.
        e.line.setStyle({ weight: pesoTrack });
        if (e.reborde) e.reborde.setStyle({ weight: pesoReborde });
      });
    }
    if (!unaSola) {
      map.on('zoomend', ajustaGrosor);
      ajustaGrosor();
    }

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
            weight: pesoTrack
          });
          if (entry.reborde) entry.reborde.setStyle({
            opacity: show ? (activeLine ? 0.1 : 0.55) : 0.04 });
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
      if (esPortada) encuadraVisibles();
    }

    // El filtro reencuadra el mapa de la portada. Pasar de «A pie» a
    // «E-bike» dejaba la vista donde estuviera -- a veces sin ninguna de las
    // rutas que quedaban a la vista -- y lo pidio el autor: que se centre
    // siempre. Se reencuadra aunque el visitante ya hubiera movido el mapa,
    // y por eso cuenta como movimiento suyo: si no, el siguiente cambio de
    // tamano del contenedor devolveria el encuadre general y desharia esto.
    // Solo cuando el conjunto visible cambia de verdad, para no dar un salto
    // por cada tecla del buscador que no quita ninguna ruta, y la primera
    // vez solo se anota: de ese primer encuadre ya se ocupa fit().
    var ultimoEncuadre = null;
    function encuadraVisibles(){
      if (!el.clientWidth || !el.clientHeight) return;
      var visibles = Object.keys(hrefToLine).filter(function(h){
        return labelFilterVisible[h] !== false;
      }).sort();
      var firma = visibles.join('|');
      if (firma === ultimoEncuadre) return;
      var primera = ultimoEncuadre === null;
      ultimoEncuadre = firma;
      if (primera || !visibles.length) return;
      var caja = null;
      visibles.forEach(function(h){
        var b = hrefToLine[h].line.getBounds();
        if (!b || !b.isValid()) return;
        if (caja) caja.extend(b);
        else caja = L.latLngBounds(b.getSouthWest(), b.getNorthEast());
      });
      if (!caja || !caja.isValid()) return;
      userMoved = true;
      map.fitBounds(caja, { padding: [24, 24] });
    }

    applyRouteFilter(pendingVisibleHrefs, pendingActivity);
    onRouteFilterChange = applyRouteFilter;

    if (data.marker) {
      var c = COLORS[data.marker.color] || COLORS.violet;
      var size = data.marker.color === 'parking' ? 16 : 14;
      L.marker(data.marker.at, {
        title: el.dataset.markerTitle || '',
        // Por encima de todo lo demas del panel de marcadores: con las
        // pastillas agrupadas, la de «38 rutas» cae justo sobre Trabakua y
        // tapaba la salida. El autor la quiere siempre a la vista: «la
        // salida que siga marcada en rojo».
        zIndexOffset: 2000,
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

    // Las fuentes de agua de esta ruta, en gota azul. El dato lo escribe
    // add_fuentes_ficha() en src/build.py desde data/fuentes.json, en el
    // idioma de la pagina; no viene en data/<ruta>.json porque ese fichero
    // lo reescribe make_map_data.py cada vez que se toca un GPX.
    //
    // Azul y con forma de gota a proposito: los puntos de referencia son
    // circulos de color --teal con su numero dentro, y el agua tiene que
    // distinguirse de ellos sin leer nada.
    if (el.dataset.fuentes) {
      var agua;
      try { agua = JSON.parse(el.dataset.fuentes); } catch (e) { agua = []; }
      (agua || []).forEach(function(f){
        if (!f || !f.at) return;
        L.marker(f.at, {
          title: f.nombre || '',
          icon: L.divIcon({
            className: '',
            html: '<span style="display:flex;align-items:center;justify-content:center;' +
                  'width:20px;height:20px;border-radius:50%;background:#3B82F6;' +
                  'border:2px solid ' + ground + ';box-shadow:0 0 0 1.5px #3B82F6;">' +
                  '<svg viewBox="0 0 24 24" width="11" height="11" fill="#fff" aria-hidden="true">' +
                  '<path d="M12 2.5c3.8 4.6 6 7.9 6 10.6a6 6 0 0 1-12 0c0-2.7 2.2-6 6-10.6z"/>' +
                  '</svg></span>',
            iconSize: [20, 20], iconAnchor: [10, 10]
          })
        }).addTo(map);
      });
    }

    (data.waypoints || []).forEach(function(pt, i){
      L.marker(pt, {
        title: wpNames[i] || '',
        icon: L.divIcon({
          className: '',
          html: '<span style="display:flex;align-items:center;justify-content:center;' +
                'width:18px;height:18px;border-radius:50%;background:' + (actColor || COLORS.teal) + ';' +
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
    // no el estado normal: el color de la ruta (verde a pie, naranja en bici) es
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

        // Los extremos reales del dibujo, leidos del propio trazado. Hacen
        // falta para devolver la y a metros, y NO se pueden dar por sabidos:
        // scripts/rehaz_perfil.py documenta y = 285 - (ele-min)/(max-min)*270,
        // pero las fichas publicadas usan seis convenciones distintas -- 160,
        // 161, 163, 200 y 201 muestras, y la y va de (0,300) en astarlokoatxa
        // a (47,225) en oiz. Aqui habia un margen fijo de 8 px, es decir se
        // suponia que la y iba de 8 a 292 siempre, y la lectura se iba
        // **hasta 153 metros**: en zenarruza el punto mas bajo decia 385 m
        // donde la ficha dice 232, y en oiz 547 donde dice 399. Midiendo los
        // extremos del trazado sale exacto en las seis convenciones, y
        // seguira saliendo si manana se dibuja de otra manera.
        // Ojo: en dos fichas (axmakuriturrizuri y zengotitaosmagain) la
        // LINEA arrastra el cierre del relleno -- acaba en «L1000,300 L0,300»
        // --, asi que trae dos puntos de mas pegados al suelo del recuadro.
        // Un perfil va siempre hacia la derecha, de modo que en cuanto la x
        // retrocede se deja de contar: eso descarta el cierre sin tener que
        // reconocerlo, y de paso protege la busqueda binaria de yAtX, que da
        // por hecho que la x es monotona. Sin esto, esas dos fichas leian el
        // punto mas bajo 46 m por encima de lo que dice su propio pie.
        var yTope = Infinity, ySuelo = -Infinity, xPrev = -Infinity;
        var pares = (heroPath.getAttribute('d') || '')
          .match(/[ML]\s*-?[\d.]+[ ,]\s*-?[\d.]+/g) || [];
        for (var pi = 0; pi < pares.length; pi++) {
          var nn = pares[pi].match(/-?[\d.]+/g);
          var xx = parseFloat(nn[0]), yy = parseFloat(nn[1]);
          if (xx <= xPrev) break;
          xPrev = xx;
          if (yy < yTope) yTope = yy;
          if (yy > ySuelo) ySuelo = yy;
        }
        var hayEscala = isFinite(yTope) && ySuelo - yTope > 1;
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
          if (!hayEscala) return km + ' km';
          var ele = Math.round(minEle + (maxEle - minEle) * ((ySuelo - y) / (ySuelo - yTope)));
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

  /* ------------------------------------------------------------------ */
  /* La tira de rutas que tienes delante.
   *
   * Lo pidio el autor: «si no, es dificil saber si estoy en Mallabia, si
   * estoy en Durango o donde, cuando tengo el zoom aumentado». Con el mapa
   * muy cerca solo se ven dos trazados sin nombre, y el mapa de fondo no
   * siempre rotula el pueblo.
   *
   * Asi que debajo del mapa va una tira con las rutas que caben en lo que
   * se esta mirando, con su nombre y sus kilometros, y **cambia sola al
   * mover o al acercar**. Si entran dos, salen dos; si al subir al norte
   * entran tres, salen esas tres. Tocar una abre su ficha, igual que tocar
   * su pastilla de kilometros.
   *
   * Se cuelga del mismo sitio que la pastilla de las capas (hermana del
   * contenedor del mapa) y se rellena desde updateLabelVisibility(), que ya
   * corre en zoomend y en moveend: el conjunto que calcula para agrupar es
   * exactamente el que hace falta aqui, asi que no se recorre nada dos veces.
   */
  // SIN TOPE. Lo hubo, y era el propio fallo: comprobadas las 66 una a una,
  // con tope 12 veinte rutas tenian el track a la vista y se quedaban sin
  // ficha, y con 25 todavia cuatro. La regla que pidio el autor es «si veo
  // la ruta trazada, que me salga su plantilla», y un tope la rompe. Cuesta
  // unas decenas de nodos y las fotos ya estan cargadas; van ordenadas por
  // cercania al centro, asi que las que de verdad miras son las primeras.
  var TOPE_TIRA = 999;

  function creaTira(){
    if (tiraCercanas || !esPortada) return;
    tiraCercanas = document.createElement('div');
    tiraCercanas.className = 'map-cercanas';
    tiraCercanas.setAttribute('role', 'list');
    tiraCercanas.setAttribute('aria-label',
      isEu ? 'Ikusgai dauden ibilbideak' : 'Rutas que se ven ahora');
    // DESPUES de la caja del mapa, no dentro: la caja tiene el alto fijo
    // (aspect-ratio) y lo que se le mete debajo queda recortado y no se ve.
    var cajaMapa = el.closest ? el.closest('.route-map-box') : null;
    var padre = cajaMapa && cajaMapa.parentElement;
    if (padre && padre.insertBefore) {
      padre.insertBefore(tiraCercanas, cajaMapa.nextSibling || null);
    } else {
      (padre || el.parentElement).appendChild(tiraCercanas);
    }
  }

  // Que rutas se estan VIENDO. No vale mirar donde cae su pastilla de
  // kilometros, que va en el punto medio del recorrido: el autor se quejo de
  // que «no veo las plantillas de bajada a Unbe y a Ipurua, por mucho que veo
  // la ruta trazada no me abre ni una». Y tenia razon -- Unbe e Ipurua no son
  // rutas, son sitios por los que pasan galdaramino y karabieta, y mirando
  // ese tramo el punto medio de esas rutas queda fuera de la pantalla.
  //
  // Asi que se mira el propio track: si alguno de sus puntos cae en lo que se
  // ve, esa ruta tiene ficha. Son 66 rutas de unos 220 puntos y sale en
  // cuanto encuentra el primero, asi que no se nota.
  //
  // Lo que no coge: un track que cruce la pantalla de lado a lado sin ningun
  // punto dentro. A estos zooms no pasa -- los puntos van cada 10 m.
  function rutasEnVista(){
    var caja = null;
    if (map.getBounds) { try { caja = map.getBounds().pad(0.08); } catch (e) { caja = null; } }
    return Object.keys(hrefToLine).filter(function(href){
      if (labelFilterVisible[href] === false) return false;
      if (labelSoloHref && href !== labelSoloHref) return false;
      var r = hrefToLine[href];
      if (!caja || !caja.contains || !r.puntos) return true;
      for (var i = 0; i < r.puntos.length; i++) {
        if (caja.contains(r.puntos[i])) return true;
      }
      return false;
    });
  }

  function pintaCercanas(hrefs){
    if (!esPortada) return;
    creaTira();
    if (!tiraCercanas) return;
    // Con una ficha abierta manda la ficha, y dibujando manda el trazo.
    var fuera = labelSoloHref || el.classList.contains('is-drawing') || !hrefs.length;
    if (fuera) {
      if (firmaTira !== null) { tiraCercanas.innerHTML = ''; firmaTira = null; }
      tiraCercanas.hidden = true;
      return;
    }
    // Primero las mas cercanas al centro de lo que se esta mirando: son las
    // que el visitante tiene de verdad delante.
    var orden = hrefs.slice();
    if (map.getCenter && map.distance) {
      var centro = map.getCenter();
      orden.sort(function(a, b){
        return map.distance(centro, hrefToLabel[a].getLatLng()) -
               map.distance(centro, hrefToLabel[b].getLatLng());
      });
    }
    orden = orden.slice(0, TOPE_TIRA);
    // Se repinta entera solo si cambia lo que hay: al arrastrar sin que
    // entre ni salga ninguna no se toca el DOM ni se pierde el desplazado.
    // La firma va en una variable del cierre y NO en tiraCercanas.dataset:
    // el DOM de mentira de scripts/test_ui.cjs devuelve un dataset NUEVO en
    // cada lectura, asi que lo escrito se perdia y ademas no tiene
    // childNodes -- entre las dos cosas el test se colgaba sin imprimir
    // nada, que parecia falta de memoria y no lo era.
    var firma = orden.join('|');
    if (firma === firmaTira) { tiraCercanas.hidden = false; return; }
    firmaTira = firma;
    tiraCercanas.innerHTML = '';
    var puestas = 0;
    orden.forEach(function(href){
      var r = hrefToLine[href];
      if (!r || !r.nombre) return;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'map-cercana is-' + (r.activity === 'bici' ? 'bici' : 'pie');
      b.setAttribute('role', 'listitem');
      if (r.foto) {
        // La misma imagen que ya muestra su tarjeta en la lista: el
        // navegador la tiene cargada, asi que no descarga nada nuevo.
        var im = document.createElement('img');
        im.className = 'map-cercana-foto';
        im.src = r.foto;
        im.alt = '';
        im.loading = 'lazy';
        im.decoding = 'async';
        b.appendChild(im);
      }
      var txt = document.createElement('span');
      txt.className = 'map-cercana-txt';
      var n = document.createElement('span');
      n.className = 'map-cercana-nombre';
      n.textContent = r.nombre;
      txt.appendChild(n);
      var datos = [];
      if (r.km) datos.push(r.km.replace('.', ',') + ' km');
      if (r.desnivel) datos.push('+' + r.desnivel.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ' m');
      if (datos.length) {
        var d = document.createElement('span');
        d.className = 'map-cercana-datos';
        d.textContent = datos.join(' \u00b7 ');
        txt.appendChild(d);
      }
      b.appendChild(txt);
      b.addEventListener('click', function(e){
        e.stopPropagation();
        if (r.abre) r.abre();
      });
      tiraCercanas.appendChild(b);
      puestas++;
    });
    tiraCercanas.hidden = !puestas;
  }

    // Las pastillas de kilometros, agrupadas cuando se pisan.
    //
    // Hasta ahora no salian por debajo del zoom 12, y con razon: medidos los
    // puntos medios de las 66 rutas, al zoom de apertura (10) caben TODOS en
    // un recuadro de 145x177 px, y una pastilla de «32,46 km» mide 76x24. Son
    // 717 parejas pisandose. No es un problema de codigo: las rutas viven en
    // un valle de seis kilometros y a esa escala caben en un sello.
    //
    //   z10  145x177 px   717 parejas se pisan
    //   z11  291x354 px   245
    //   z12  581x707 px    69
    //   z13 1163x1414 px   23
    //
    // La salida es la que usa AllTrails y que el autor señalo en su captura:
    // cuando varias se pisan, se juntan en una que dice cuantas hay («18
    // rutas»), y al tocarla el mapa se acerca a ellas. Asi el mapa de
    // conjunto ya dice algo en vez de estar mudo hasta el zoom 12.
    var RADIO_GRUPO = 46;       // a menos de esto, dos puntos van al mismo grupo

    function candidatasKm(){
      // Las que podrian salir: ni filtradas fuera, ni tapadas por una ficha,
      // y **dentro de lo que se esta mirando**. Lo pidio el autor: «que
      // aparezcan las pastillas que estan en esa zona»; al moverse al norte,
      // las de alli. Asi un grupo no se queda diciendo «38 rutas» cuando de
      // esas 38 solo quedan cuatro en pantalla. El margen del 15 % evita que
      // una pastilla aparezca y desaparezca al rozar el borde.
      // getBounds/pad existen en Leaflet de verdad; la comprobacion es por si
      // el mapa todavia no tiene vista (o por un Leaflet reducido, como el de
      // scripts/test_ui.cjs), para no tumbar la pagina por una pastilla.
      var caja = null;
      if (esPortada && map.getBounds) {
        try { caja = map.getBounds().pad(0.15); } catch (e) { caja = null; }
      }
      return Object.keys(hrefToLabel).filter(function(href){
        if (labelFilterVisible[href] === false) return false;
        if (labelSoloHref && href !== labelSoloHref) return false;
        return !caja || !caja.contains || caja.contains(hrefToLabel[href].getLatLng());
      });
    }

    function agrupaKms(hrefs){
      // agrupado codicioso por cercania en pixeles: se recorre en orden y
      // cada una cae en el primer grupo que la acepte. Con 66 puntos es
      // instantaneo y da grupos estables entre repintados.
      var pts = hrefs.map(function(h){
        return map.latLngToContainerPoint(hrefToLabel[h].getLatLng());
      });
      var grupos = [];
      for (var i = 0; i < hrefs.length; i++) {
        var metida = false;
        for (var g = 0; g < grupos.length && !metida; g++) {
          var dx = pts[i].x - grupos[g].x, dy = pts[i].y - grupos[g].y;
          if (dx * dx + dy * dy < RADIO_GRUPO * RADIO_GRUPO) {
            grupos[g].miembros.push(i);
            // el centro se recalcula para que el grupo no se vaya con el
            // primero que entro
            grupos[g].x += (pts[i].x - grupos[g].x) / grupos[g].miembros.length;
            grupos[g].y += (pts[i].y - grupos[g].y) / grupos[g].miembros.length;
            metida = true;
          }
        }
        if (!metida) grupos.push({ x: pts[i].x, y: pts[i].y, miembros: [i] });
      }
      // Segunda pasada: el radio de arriba junta PUNTOS, pero una pastilla
      // «32 rutas» mide unos 76x24, asi que dos centros a 50 px todavia se
      // pisan. Se funden los grupos cuyas pastillas se tocarian, y se repite
      // hasta que no quede ninguno -- medido, con esto se pasa de 8 parejas
      // solapadas a cero al zoom de apertura.
      var ANCHO = 84, ALTO = 28, cambio = true;
      while (cambio) {
        cambio = false;
        for (var a = 0; a < grupos.length && !cambio; a++) {
          for (var c = a + 1; c < grupos.length && !cambio; c++) {
            if (Math.abs(grupos[a].x - grupos[c].x) < ANCHO &&
                Math.abs(grupos[a].y - grupos[c].y) < ALTO) {
              var na = grupos[a].miembros.length, nc = grupos[c].miembros.length;
              grupos[a].x = (grupos[a].x * na + grupos[c].x * nc) / (na + nc);
              grupos[a].y = (grupos[a].y * na + grupos[c].y * nc) / (na + nc);
              grupos[a].miembros = grupos[a].miembros.concat(grupos[c].miembros);
              grupos.splice(c, 1);
              cambio = true;
            }
          }
        }
      }
      return grupos;
    }

    function pintaGrupos(grupos, hrefs){
      if (grupoCapa) { map.removeLayer(grupoCapa); grupoCapa = null; }
      var conVarias = grupos.filter(function(g){ return g.miembros.length > 1; });
      if (!conVarias.length || !L.layerGroup || !map.containerPointToLatLng) return;
      grupoCapa = L.layerGroup();
      conVarias.forEach(function(g){
        var puntos = g.miembros.map(function(i){ return hrefToLabel[hrefs[i]].getLatLng(); });
        var cuantas = g.miembros.length;
        var texto = cuantas + ' ' + (isEu ? 'ibilbide' : 'rutas');
        // De Leaflet.markercluster se toma la idea, no el codigo: la pastilla
        // crece con lo que agrupa, asi se ve de un vistazo donde esta el
        // grueso. La libreria en si seria un canon para matar moscas -- son
        // 66 puntos -- y lleva cinco años sin publicar version.
        var talla = cuantas >= 20 ? ' es-grande' : (cuantas >= 6 ? ' es-media' : '');
        var m = L.marker(map.containerPointToLatLng(L.point(g.x, g.y)), {
          icon: L.divIcon({
            className: 'route-dist-label route-group-label' + talla,
            html: '<span class="route-dist-label-inner">' + texto + '</span>',
            iconSize: null
          }),
          title: texto,
          keyboard: true
        });
        m.on('click', function(e){
          L.DomEvent.stopPropagation(e);
          userMoved = true;
          map.fitBounds(L.latLngBounds(puntos).pad(0.35), {
            maxZoom: 15,
            animate: !(window.matchMedia &&
                       window.matchMedia('(prefers-reduced-motion: reduce)').matches)
          });
        });
        grupoCapa.addLayer(m);
      });
      grupoCapa.addTo(map);
    }

    function updateLabelVisibility(){
      var hrefs = candidatasKm();
      // En una ficha de ruta hay una sola etiqueta: ahi no hay nada que
      // agrupar y se deja como estaba.
      if (!esPortada) {
        var zoomOk = map.getZoom() >= LABEL_MIN_ZOOM;
        Object.keys(hrefToLabel).forEach(function(href){
          var e1 = hrefToLabel[href].getElement();
          if (!e1) return;
          var ver = zoomOk && hrefs.indexOf(href) !== -1;
          e1.style.opacity = ver ? '1' : '0';
          e1.style.pointerEvents = ver ? '' : 'none';
        });
        if (zoomOk) repositionLabels();
        return;
      }
      var grupos = agrupaKms(hrefs);
      var sueltas = {};
      grupos.forEach(function(g){
        if (g.miembros.length === 1) sueltas[hrefs[g.miembros[0]]] = true;
      });
      Object.keys(hrefToLabel).forEach(function(href){
        var e2 = hrefToLabel[href].getElement();
        if (!e2) return;
        var ver = sueltas[href] === true;
        e2.style.opacity = ver ? '1' : '0';
        e2.style.pointerEvents = ver ? '' : 'none';
      });
      pintaGrupos(grupos, hrefs);
      // La tira enseña **las rutas que se estan viendo**, con el track dentro
      // de la pantalla. Antes iba por la pastilla de kilometros y se perdian
      // las que cruzan la vista con el punto medio fuera -- ver rutasEnVista.
      pintaCercanas(rutasEnVista());
      repositionLabels();
    }

    map.on('click', closePanel);
    map.on('zoomend', updateLabelVisibility);
    // Gancho para filters.js: al pasar de lista a mapa la caja cambia de
    // tamano por CSS, y Leaflet no se entera solo.
    if (esPortada) {
      window.__avisaMapaTamano = function(){
        setTimeout(function(){
          map.invalidateSize({ animate: false });
          updateLabelVisibility();
        }, 60);
      };
    }
    // Y tambien al desplazar: lo que se agrupa es lo que hay delante, asi
    // que al moverse cambia. Son 66 puntos, el recalculo es instantaneo.
    if (esPortada) map.on('moveend', updateLabelVisibility);

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
    // La herramienta de dibujar un trazado (js/trazado.js, solo en la
    // portada) se engancha aqui: necesita el mapa ya montado, los tracks con
    // los que construye su red y la caja. Va por evento y no por una
    // variable global para que este fichero no sepa nada de ella: si
    // trazado.js no esta cargado, no pasa absolutamente nada.
    try {
      document.dispatchEvent(new CustomEvent('mapa:listo', { detail: {
        map: map, L: L, datos: data, esPortada: esPortada, caja: el,
        cerrarPanel: closePanel
      }}));
    } catch (e) {}
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
