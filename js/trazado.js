// Dibujar un trazado propio sobre la red de caminos de la web (solo portada).
//
// La idea es del autor: casi nadie se hace de una tirada una ruta de 37 km, y
// lo que pide la gente es unir dos, acortar una, o montarse la suya. Dibujar
// a mano alzada no vale -- un garabato no va por los caminos y el kilometraje
// que saldria seria mentira --, asi que aqui se dibuja TOCANDO PUNTOS y el
// camino entre dos toques se calcula sobre los tracks reales de la web.
//
// La red sale de los 65 tracks que la portada ya se ha bajado (data/
// trailhead.json): se pegan los puntos a una rejilla de 15 m, y cada punto
// pegado es un nodo. Medido sobre los datos de hoy son 8.418 nodos y 10.796
// tramos, y forman UNA SOLA componente conexa: desde cualquier punto de
// cualquier ruta se llega a cualquier otro sin salirse de terreno grabado.
// Por eso no hace falta ningun servicio de rutas de fuera, que es la regla de
// esta web.
//
// Las alturas van aparte, en data/alturas.json (56 kB), y se bajan solo al
// abrir el modo de dibujo: el mapa de la portada no las necesita y no tiene
// sentido cobrarselas a todo el que abre el mapa.
//
// Lo que dibuja un visitante NO es una ruta de la web: va en otro color, se
// llama «tu trazado», se guarda solo en su navegador y nunca aparece entre
// las 65.
(function(){
  'use strict';

  var CELDA_M = 15;              // rejilla con la que se pegan los puntos
  var PASO_M = 5;                // se rellenan los tramos cada 5 m (ver construyeRed)
  var MAX_ENGANCHE_M = 120;      // mas lejos de esto, el toque no coge camino
  var UMBRAL_SUBIDA_M = 5;       // para no sumar el ruido del GPS como desnivel
  var ALMACEN = 'rutas-mallabia-trazados';
  var COLOR = '#38BDF8';
  var LAT0 = 43.2;
  var KX = 111320 * Math.cos(LAT0 * Math.PI / 180);

  var T = {
    es: {
      abrir: 'Dibujar un trazado', cerrar: 'Cerrar el dibujo',
      titulo: 'Tu trazado', arranque: 'Toca el mapa sobre un camino para empezar.',
      sigue: 'Toca otro punto: el camino va por los senderos de las rutas.',
      lejos: 'Ahi no pasa ninguna ruta. Toca mas cerca de un camino dibujado.',
      sinpaso: 'No hay camino hasta ahi dentro de la red.',
      deshacer: 'Deshacer', borrar: 'Borrar', guardar: 'Guardar', gpx: 'Bajar GPX',
      guardados: 'Guardados', abrirlo: 'Abrir', quitar: 'Quitar',
      nombre: 'Trazado', aprox: 'aprox.', ultimo: '\u00daltimo tramo', cargando: 'Preparando la red de caminos…',
      fallo: 'No se ha podido preparar la red. Prueba a recargar.',
      rodeo: 'Ese tramo da un rodeo de %s km: entre esos dos puntos no hay ning\u00fan camino grabado m\u00e1s corto. Deshazlo y prueba con un punto intermedio.',
      aviso: 'Esto lo dibujas tu: va por caminos que salen en las rutas, pero no es ninguna de ellas.'
    },
    eu: {
      abrir: 'Marrazki bat egin', cerrar: 'Marrazkia itxi',
      titulo: 'Zure marrazkia', arranque: 'Ukitu mapa bide baten gainean hasteko.',
      sigue: 'Ukitu beste puntu bat: bidea ibilbideetako bidexketatik doa.',
      lejos: 'Hor ez da ibilbiderik pasatzen. Ukitu marraztutako bide batetik gertuago.',
      sinpaso: 'Ez dago biderik hormaino sarearen barruan.',
      deshacer: 'Desegin', borrar: 'Ezabatu', guardar: 'Gorde', gpx: 'GPXa jaitsi',
      guardados: 'Gordeta', abrirlo: 'Ireki', quitar: 'Kendu',
      nombre: 'Marrazkia', aprox: 'gutxi gorabehera', ultimo: 'Azken tartea', cargando: 'Bideen sarea prestatzen…',
      fallo: 'Ezin izan da sarea prestatu. Saiatu orria berriro kargatzen.',
      rodeo: 'Tarte horrek %s km-ko bira ematen du: bi puntu horien artean ez dago grabatutako bide laburragorik. Desegin eta saiatu tarteko puntu batekin.',
      aviso: 'Hau zuk marrazten duzu: ibilbideetan agertzen diren bideetatik doa, baina ez da haietako bat.'
    }
  };

  function metros(a, b){
    var dy = (a[0] - b[0]) * 111320, dx = (a[1] - b[1]) * KX;
    return Math.sqrt(dy * dy + dx * dx);
  }

  // ---- la red ------------------------------------------------------------

  function construyeRed(tracks, alturas){
    var nodos = [], clave = Object.create(null), ady = [];
    function id(p){
      var k = Math.round(p[0] * 111320 / CELDA_M) + ':' +
              Math.round(p[1] * KX / CELDA_M);
      var i = clave[k];
      if (i === undefined) { i = nodos.length; clave[k] = i; nodos.push([p[0], p[1], null]); ady.push([]); }
      return i;
    }
    function une(a, b){
      if (a === b) return;
      var d = metros(nodos[a], nodos[b]);
      var i, vs = ady[a];
      for (i = 0; i < vs.length; i++) if (vs[i][0] === b) return;
      ady[a].push([b, d]); ady[b].push([a, d]);
    }
    // Los puntos vienen simplificados a 10 m y dos caminos que se CRUZAN
    // pueden caer en celdas distintas: el cruce no existe para la red y el
    // calculo tiene que irse a buscar la vuelta larga. Rellenando cada tramo
    // cada 5 m antes de pegar a la rejilla, el cruce cae en la misma celda.
    // Medido sobre 120 pares de puntos a 100-600 m: el rodeo mediano baja de
    // 1,94 a 1,58 veces la linea recta y los rodeos de mas de 3x pasan de 31
    // a 22. Los que quedan son de verdad: solo hay caminos grabados.
    tracks.forEach(function(t){
      var pts = t.points || [];
      var alt = (alturas && t.href) ? alturas[String(t.href).split('/').pop().replace('.html', '')] : null;
      var prev = -1;
      for (var i = 0; i < pts.length; i++) {
        if (i > 0) {
          var a = pts[i - 1], b = pts[i], largo = metros(a, b);
          // La altura del punto de relleno se interpola entre los dos puntos
          // grabados que tiene a los lados. Sin esto, el GPX que se baja
          // salia con altura solo en uno de cada cinco puntos.
          var ea = alt ? alt[i - 1] : null, eb = alt ? alt[i] : null;
          var hayE = typeof ea === 'number' && typeof eb === 'number';
          for (var k = 1; k * PASO_M < largo; k++) {
            var f = k * PASO_M / largo;
            var m = id([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]);
            if (hayE && nodos[m][2] === null) nodos[m][2] = Math.round(ea + (eb - ea) * f);
            if (prev >= 0) une(prev, m);
            prev = m;
          }
        }
        var n = id(pts[i]);
        if (alt && nodos[n][2] === null && typeof alt[i] === 'number') nodos[n][2] = alt[i];
        if (prev >= 0) une(prev, n);
        prev = n;
      }
    });
    // rejilla de 100 m para buscar el nodo mas cercano a un toque
    var cestas = Object.create(null);
    nodos.forEach(function(n, i){
      var k = Math.round(n[0] * 111320 / 100) + ':' + Math.round(n[1] * KX / 100);
      (cestas[k] || (cestas[k] = [])).push(i);
    });
    return { nodos: nodos, ady: ady, cestas: cestas };
  }

  function nodoCerca(red, lat, lon){
    var cx = Math.round(lat * 111320 / 100), cy = Math.round(lon * KX / 100);
    var mejor = -1, mejorD = Infinity;
    for (var dx = -2; dx <= 2; dx++) for (var dy = -2; dy <= 2; dy++) {
      var lista = red.cestas[(cx + dx) + ':' + (cy + dy)];
      if (!lista) continue;
      for (var i = 0; i < lista.length; i++) {
        var d = metros(red.nodos[lista[i]], [lat, lon]);
        if (d < mejorD) { mejorD = d; mejor = lista[i]; }
      }
    }
    return mejorD <= MAX_ENGANCHE_M ? mejor : -1;
  }

  // Dijkstra con monticulo binario. 8.418 nodos: sobra de rapido.
  function camino(red, desde, hasta){
    if (desde === hasta) return [desde];
    var n = red.nodos.length;
    var dist = new Float64Array(n); dist.fill(Infinity);
    var antes = new Int32Array(n); antes.fill(-1);
    var visto = new Uint8Array(n);
    var heap = [[0, desde]];
    dist[desde] = 0;
    function sube(i){
      while (i > 0) {
        var p = (i - 1) >> 1;
        if (heap[p][0] <= heap[i][0]) break;
        var t = heap[p]; heap[p] = heap[i]; heap[i] = t; i = p;
      }
    }
    function baja(i){
      for (;;) {
        var l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap.length && heap[l][0] < heap[m][0]) m = l;
        if (r < heap.length && heap[r][0] < heap[m][0]) m = r;
        if (m === i) break;
        var t = heap[m]; heap[m] = heap[i]; heap[i] = t; i = m;
      }
    }
    while (heap.length) {
      var top = heap[0];
      heap[0] = heap[heap.length - 1]; heap.pop(); if (heap.length) baja(0);
      var u = top[1];
      if (visto[u]) continue;
      visto[u] = 1;
      if (u === hasta) break;
      var vs = red.ady[u];
      for (var i = 0; i < vs.length; i++) {
        var v = vs[i][0], nd = top[0] + vs[i][1];
        if (nd < dist[v]) { dist[v] = nd; antes[v] = u; heap.push([nd, v]); sube(heap.length - 1); }
      }
    }
    if (!visto[hasta]) return null;
    var ruta = [], x = hasta;
    while (x !== -1) { ruta.push(x); x = antes[x]; }
    return ruta.reverse();
  }

  // ---- la herramienta ----------------------------------------------------

  document.addEventListener('mapa:listo', function(ev){
    var d = ev.detail;
    if (!d.esPortada || !d.map || !d.L) return;
    var L = d.L, map = d.map, caja = d.caja, marco = caja.parentElement;
    var t = T[document.documentElement.lang === 'eu' ? 'eu' : 'es'];

    var red = null, cargando = false;
    var anclas = [];     // nodos que ha tocado el visitante
    var tramos = [];     // un array de nodos por cada tramo calculado
    var linea = null, puntitos = [], activo = false;
    // Un trazado reabierto de los guardados no tiene anclas ni tramos: solo
    // sus coordenadas. Sin esto, «Bajar GPX» no hacia nada despues de abrir
    // uno guardado, porque el recorrido se armaba solo desde los tramos.
    var cargado = null;

    function icono(p){
      return '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor"' +
        ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>';
    }
    var ICO = {
      lapiz: '<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>' +
             '<path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/>',
      undo:  '<path d="M9 14L4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10H9"/>',
      clear: '<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/>',
      save:  '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
      gpx:   '<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/>',
      lista: '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>'
    };

    // El lapiz, arriba a la derecha, debajo del boton de ampliar.
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'map-draw-btn';
    btn.setAttribute('aria-label', t.abrir);
    btn.title = t.abrir;
    btn.innerHTML = icono(ICO.lapiz);
    marco.appendChild(btn);

    // Y las opciones en columna, justo debajo del lapiz y dentro del mapa:
    // el autor las queria ahi, en una esquina y en vertical, para que el
    // mapa se lleve casi toda la pantalla. Antes iban en un panel ancho
    // debajo del mapa.
    var tools = document.createElement('div');
    tools.className = 'draw-tools';
    tools.hidden = true;
    tools.innerHTML = [['undo', t.deshacer], ['clear', t.borrar], ['save', t.guardar],
                       ['gpx', t.gpx], ['list', t.guardados]].map(function(par){
      var k = par[0] === 'list' ? 'lista' : par[0];
      return '<button type="button" class="draw-t" data-a="' + par[0] + '" title="' + par[1] +
             '" aria-label="' + par[1] + '">' + icono(ICO[k]) + '</button>';
    }).join('');
    marco.appendChild(tools);

    // Los totales y el aviso, en una pastilla pequena abajo a la izquierda.
    var readout = document.createElement('div');
    readout.className = 'draw-readout';
    readout.hidden = true;
    readout.innerHTML = '<div class="draw-perfil-caja"></div>' +
                        '<div class="draw-cifras">' +
                        '<p class="draw-tot" hidden><span class="draw-km"></span><span class="draw-des"></span></p>' +
                        '<p class="draw-ult" hidden></p></div>' +
                        '<p class="draw-msg"></p>';
    marco.appendChild(readout);

    var saved = document.createElement('div');
    saved.className = 'draw-saved';
    saved.hidden = true;
    marco.appendChild(saved);

    var elMsg = readout.querySelector('.draw-msg');
    var elPerfil = readout.querySelector('.draw-perfil-caja');
    var elUlt = readout.querySelector('.draw-ult');
    var elTot = readout.querySelector('.draw-tot');
    var elKm = readout.querySelector('.draw-km');
    var elDes = readout.querySelector('.draw-des');
    var fab = document.querySelector('.view-fab');
    var arriba = document.getElementById('toTop');

    // Casi toda la pantalla para el mapa mientras se dibuja: se descuentan
    // la cabecera pegajosa y, en el movil, la barra fija de abajo («Lista /
    // Todas / A pie…»), que el autor quiere seguir viendo.
    var CABECERA = 62;
    var altoPrevio = '';
    function encaja(){
      if (!activo) return;
      var abajo = 0, barra = document.querySelector('.finder-toolbar');
      if (barra) {
        var r = barra.getBoundingClientRect();
        if (getComputedStyle(barra).position === 'fixed' && r.bottom > window.innerHeight - 6) abajo = r.height;
      }
      // De lado a lado: la caja del mapa vive en una columna centrada mas
      // estrecha que la pantalla, asi que se la saca de ella con un margen
      // negativo. El ancho se toma de clientWidth y no de 100vw, que incluye
      // la barra de desplazamiento y dejaria la pagina moviendose de lado.
      marco.style.marginLeft = '0px';
      marco.style.width = '';
      var izq = marco.getBoundingClientRect().left;
      marco.style.marginLeft = (-izq) + 'px';
      marco.style.width = document.documentElement.clientWidth + 'px';
      marco.style.borderRadius = '0';
      marco.style.aspectRatio = 'auto';
      marco.style.height = Math.max(300, window.innerHeight - CABECERA - abajo - 14) + 'px';
      if (map && map.invalidateSize) map.invalidateSize();
    }
    function sueltaEncaje(){
      marco.style.aspectRatio = '';
      marco.style.height = altoPrevio;
      marco.style.marginLeft = '';
      marco.style.width = '';
      marco.style.borderRadius = '';
      if (map && map.invalidateSize) setTimeout(function(){ map.invalidateSize(); }, 60);
    }
    window.addEventListener('resize', encaja);

    // El trazo lleva un reborde por debajo, del color del fondo de la web:
    // asi se lee igual sobre el naranja de bici, el verde de a pie o el
    // callejero, y no hace falta apagar los 65 tracks mas de la cuenta.
    function dibujaLinea(coords){
      var fondo = getComputedStyle(document.documentElement)
        .getPropertyValue('--ground').trim() || '#020617';
      var borde = L.polyline(coords, {
        color: fondo, weight: 10, opacity: .55, lineCap: 'round',
        interactive: false, className: 'draw-line'
      }).addTo(map);
      var trazo = L.polyline(coords, {
        color: COLOR, weight: 5, opacity: 1, dashArray: '1 9', lineCap: 'round',
        interactive: false, className: 'draw-line'
      }).addTo(map);
      return [borde, trazo];
    }
    function quitaLinea(){
      if (!linea) return;
      linea.forEach(function(l){ map.removeLayer(l); });
      linea = null;
    }

    function recorrido(){
      if (!tramos.length && cargado) return cargado;
      var out = [];
      tramos.forEach(function(tr, i){
        for (var k = (i ? 1 : 0); k < tr.length; k++) out.push(red.nodos[tr[k]]);
      });
      return out;
    }

    function totales(){
      var pts = recorrido(), km = 0, sub = 0, baj = 0, base = null, cima = null;
      for (var i = 1; i < pts.length; i++) km += metros(pts[i - 1], pts[i]);
      pts.forEach(function(p){
        if (typeof p[2] !== 'number') return;
        if (base === null) { base = cima = p[2]; return; }
        if (p[2] > base + UMBRAL_SUBIDA_M) { sub += p[2] - base; base = p[2]; }
        else if (p[2] < base) base = p[2];
        if (p[2] < cima - UMBRAL_SUBIDA_M) { baj += cima - p[2]; cima = p[2]; }
        else if (p[2] > cima) cima = p[2];
      });
      return { km: km / 1000, subida: Math.round(sub), bajada: Math.round(baj),
               conAltura: base !== null };
    }

    // Un perfil pequeno debajo de los totales: lo pidio el autor para saber
    // de un vistazo si el tramo que acaba de coger sube o baja, que en bici
    // y andando no da igual. Se dibuja en el sentido de la marcha, de
    // izquierda a derecha, con una rayita vertical en cada punto tocado para
    // ver donde empieza y acaba cada tramo.
    // Lo que sube y lo que baja un tramo suelto, con el mismo umbral que el
    // total. Es la pregunta del autor: «¿este tramo lo cojo de subida?».
    function desnivelDe(tr){
      var sub = 0, baj = 0, base = null, cima = null;
      tr.forEach(function(id){
        var e = red.nodos[id][2];
        if (typeof e !== 'number') return;
        if (base === null) { base = cima = e; return; }
        if (e > base + UMBRAL_SUBIDA_M) { sub += e - base; base = e; }
        else if (e < base) base = e;
        if (e < cima - UMBRAL_SUBIDA_M) { baj += cima - e; cima = e; }
        else if (e > cima) cima = e;
      });
      return '+' + Math.round(sub) + ' / -' + Math.round(baj) + ' m';
    }

    function perfil(){
      var pts = recorrido();
      if (pts.length < 2) return '';
      var acc = [0], i;
      for (i = 1; i < pts.length; i++) acc.push(acc[i - 1] + metros(pts[i - 1], pts[i]));
      var total = acc[acc.length - 1];
      if (!total) return '';
      var N = 120, W = 1000, H = 100, alt = [], ultima = null;
      var j = 0;
      for (var k = 0; k <= N; k++) {
        var dd = total * k / N;
        while (j < acc.length - 1 && acc[j + 1] < dd) j++;
        var e = pts[j][2];
        if (typeof e === 'number') ultima = e;
        alt.push(typeof e === 'number' ? e : ultima);
      }
      var hay = alt.filter(function(e){ return typeof e === 'number'; });
      if (hay.length < 2) return '';
      var min = Math.min.apply(null, hay), max = Math.max.apply(null, hay);
      var rango = Math.max(1, max - min);
      var d = '', px = [];
      for (k = 0; k <= N; k++) {
        var x = (k * W / N).toFixed(1);
        var y = (H - 6 - ((alt[k] === null ? min : alt[k]) - min) / rango * (H - 12)).toFixed(1);
        d += (k ? ' L' : 'M') + x + ',' + y;
        px.push([x, y]);
      }
      // una rayita en cada punto que ha tocado el visitante, y el ultimo
      // tramo sombreado: es el que acaba de anadir y el que quiere mirar.
      var marcas = '', llevo = 0, inicioUltimo = 0;
      tramos.forEach(function(tr, idx){
        if (!idx) return;
        inicioUltimo = llevo;
        for (var q = 1; q < tr.length; q++) {
          llevo += metros(red.nodos[tr[q - 1]], red.nodos[tr[q]]);
        }
        var xm = (llevo / total * W).toFixed(1);
        marcas += '<line x1="' + xm + '" y1="0" x2="' + xm + '" y2="' + H + '"/>';
      });
      var sombra = '';
      if (tramos.length > 1) {
        var x0 = inicioUltimo / total * W;
        sombra = '<rect class="ult" x="' + x0.toFixed(1) + '" y="0" width="' +
                 (W - x0).toFixed(1) + '" height="' + H + '"/>';
      }
      return '<svg class="draw-perfil" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none"' +
        ' aria-hidden="true">' + sombra + '<path class="rell" d="' + d + ' L' + W + ',' + H + ' L0,' + H + ' Z"/>' +
        '<path class="lin" d="' + d + '"/><g class="mrc">' + marcas + '</g></svg>';
    }

    function pinta(){
      var pts = recorrido();
      quitaLinea();
      puntitos.forEach(function(m){ map.removeLayer(m); });
      puntitos = [];
      if (pts.length > 1) linea = dibujaLinea(pts.map(function(p){ return [p[0], p[1]]; }));
      anclas.forEach(function(id, i){
        var n = red.nodos[id];
        puntitos.push(L.marker([n[0], n[1]], {
          interactive: false,
          icon: L.divIcon({ className: 'draw-dot' + (i === 0 ? ' is-first' : ''),
                            iconSize: [12, 12], iconAnchor: [6, 6] })
        }).addTo(map));
      });
      var tt = totales();
      elTot.hidden = pts.length < 2;
      elKm.textContent = tt.km.toFixed(2).replace('.', ',') + ' km';
      elDes.textContent = tt.conAltura && (tt.subida || tt.bajada)
        ? ' · +' + tt.subida + ' / -' + tt.bajada + ' m ' + t.aprox : '';
      elPerfil.innerHTML = perfil();
      elUlt.textContent = tramos.length > 1 ? t.ultimo + ' ' + desnivelDe(tramos[tramos.length - 1]) : '';
      elUlt.hidden = tramos.length < 2;
      elMsg.textContent = anclas.length ? t.sigue : t.arranque;
    }

    function alTocar(e){
      if (!activo || !red) return;
      var n = nodoCerca(red, e.latlng.lat, e.latlng.lng);
      if (n < 0) { elMsg.textContent = t.lejos; return; }
      if (!anclas.length) { cargado = null; anclas.push(n); tramos.push([n]); pinta(); return; }
      var ultimo = anclas[anclas.length - 1];
      var tr = camino(red, ultimo, n);
      if (!tr) { elMsg.textContent = t.sinpaso; return; }
      anclas.push(n); tramos.push(tr); pinta();
      // Un tramo puede salir disparado a un lado y no se entiende por que:
      // es que entre esos dos puntos no hay ningun camino grabado mas corto
      // y la red tiene que dar la vuelta. Se dice, con los metros de mas.
      var largo = 0, i;
      for (i = 1; i < tr.length; i++) largo += metros(red.nodos[tr[i - 1]], red.nodos[tr[i]]);
      var recto = metros(red.nodos[ultimo], red.nodos[n]);
      if (recto > 30 && largo > recto * 2.5 && largo - recto > 300) {
        elMsg.textContent = t.rodeo.replace('%s', (largo / 1000).toFixed(2).replace('.', ','));
      }
    }

    function gpx(){
      var pts = recorrido();
      if (pts.length < 2) return;
      var x = '<?xml version="1.0" encoding="UTF-8"?>\n' +
        '<gpx version="1.1" creator="trabakutik.com" xmlns="http://www.topografix.com/GPX/1/1">\n' +
        '<trk><name>' + t.titulo + '</name><trkseg>\n';
      pts.forEach(function(p){
        x += '<trkpt lat="' + p[0].toFixed(6) + '" lon="' + p[1].toFixed(6) + '">' +
             (typeof p[2] === 'number' ? '<ele>' + p[2] + '</ele>' : '') + '</trkpt>\n';
      });
      x += '</trkseg></trk></gpx>\n';
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([x], { type: 'application/gpx+xml' }));
      a.download = t.titulo.toLowerCase().replace(/\s+/g, '-') + '.gpx';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
    }

    function leeGuardados(){
      try { return JSON.parse(localStorage.getItem(ALMACEN) || '[]'); } catch (e) { return []; }
    }
    function escribeGuardados(v){
      try { localStorage.setItem(ALMACEN, JSON.stringify(v)); } catch (e) {}
    }
    function pintaGuardados(){
      var v = leeGuardados();
      if (!v.length) { saved.innerHTML = '<p class="draw-saved-t">' + t.guardados + '</p>'; return; }
      var html = '<p class="draw-saved-t">' + t.guardados + '</p><ul>';
      v.forEach(function(g, i){
        html += '<li><button type="button" class="draw-open" data-i="' + i + '">' +
          g.nombre + ' <span>' + g.km + ' km</span></button>' +
          '<button type="button" class="draw-del" data-i="' + i + '" aria-label="' + t.quitar + '">&times;</button></li>';
      });
      saved.innerHTML = html + '</ul>';
    }

    saved.addEventListener('click', function(e){
      var b = e.target.closest('button');
      if (!b) return;
      if (b.classList.contains('draw-open')) {
        var g = leeGuardados()[+b.dataset.i];
        if (!g) return;
        anclas = []; tramos = [];
        cargado = g.coords;
        quitaLinea();
        puntitos.forEach(function(m){ map.removeLayer(m); }); puntitos = [];
        linea = dibujaLinea(g.coords.map(function(p){ return [p[0], p[1]]; }));
        map.fitBounds(linea[1].getBounds(), { padding: [30, 30] });
        elTot.hidden = false;
        elKm.textContent = g.km + ' km';
        var tg = totales();
        elDes.textContent = tg.conAltura && (tg.subida || tg.bajada)
          ? ' · +' + tg.subida + ' / -' + tg.bajada + ' m ' + t.aprox : '';
        elPerfil.innerHTML = perfil();
        elUlt.hidden = true;
        elMsg.textContent = g.nombre;
        saved.hidden = true;
        return;
      }
      if (b.classList.contains('draw-del')) {
        var v = leeGuardados(); v.splice(+b.dataset.i, 1); escribeGuardados(v); pintaGuardados();
      }
    });

    tools.addEventListener('click', function(e){
      var b = e.target.closest('button');
      if (!b) return;
      var a = b.dataset.a;
      if (a === 'undo') { cargado = null; anclas.pop(); tramos.pop(); pinta(); }
      else if (a === 'clear') { cargado = null; anclas = []; tramos = []; pinta(); }
      else if (a === 'gpx') { gpx(); }
      else if (a === 'list') { pintaGuardados(); saved.hidden = !saved.hidden; }
      else if (a === 'save') {
        var pts = recorrido();
        if (pts.length < 2) return;
        var tt = totales(), v2 = leeGuardados();
        v2.unshift({
          nombre: t.nombre + ' ' + (v2.length + 1),
          km: tt.km.toFixed(2).replace('.', ','),
          subida: tt.conAltura ? tt.subida : 0,
          coords: pts.map(function(p){
            return typeof p[2] === 'number' ? [+p[0].toFixed(5), +p[1].toFixed(5), p[2]]
                                            : [+p[0].toFixed(5), +p[1].toFixed(5)];
          })
        });
        escribeGuardados(v2.slice(0, 12));
        pintaGuardados();
        saved.hidden = false;
      }
    });

    function apaga(){
      activo = false;
      tools.hidden = true; readout.hidden = true; saved.hidden = true;
      btn.classList.remove('is-active');
      btn.setAttribute('aria-label', t.abrir);
      btn.title = t.abrir;
      caja.classList.remove('is-drawing');
      sueltaEncaje();
      if (fab) fab.classList.remove('is-hidden-behind-panel');
      if (arriba) arriba.style.display = '';
      map.off('click', alTocar);
    }

    function enciende(){
      activo = true;
      tools.hidden = false; readout.hidden = false;
      btn.classList.add('is-active');
      btn.setAttribute('aria-label', t.cerrar);
      btn.title = t.cerrar;
      caja.classList.add('is-drawing');
      // El boton flotante de «Lista» y el de «volver arriba» caen justo
      // encima de la pastilla y de la columna de opciones.
      if (fab) fab.classList.add('is-hidden-behind-panel');
      if (arriba) arriba.style.display = 'none';
      if (d.cerrarPanel) { try { d.cerrarPanel(); } catch (e) {} }
      altoPrevio = marco.style.height || '';
      map.on('click', alTocar);
      encaja();
      window.scrollTo({ top: Math.max(0, marco.getBoundingClientRect().top + window.pageYOffset - CABECERA),
                        behavior: 'smooth' });
      if (red) { pinta(); return; }
      if (cargando) return;
      cargando = true;
      elMsg.textContent = t.cargando;
      fetch('data/alturas.json').then(function(r){ return r.ok ? r.json() : null; })
        .catch(function(){ return null; })
        .then(function(alt){
          red = construyeRed(d.datos.tracks || [], alt);
          cargando = false;
          pinta();
        })
        .catch(function(){ cargando = false; elMsg.textContent = t.fallo; });
    }

    btn.addEventListener('click', function(){ activo ? apaga() : enciende(); });
  });
})();
