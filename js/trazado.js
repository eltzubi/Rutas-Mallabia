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
      aviso: 'Esto lo dibujas tu: va por caminos que salen en las rutas, pero no es ninguna de ellas.',
      red: 'Por d\u00f3nde se puede ir', misRutas: 'Solo mis rutas',
      todosPie: 'Todos los caminos \u00b7 a pie', todosBici: 'Todos los caminos \u00b7 en bici',
      avisoOsm: 'Caminos de OpenStreetMap, sin comprobar sobre el terreno.',
      sigueOsm: 'Toca otro punto: el camino va por cualquier sendero del mapa.',
      lejosOsm: 'Ahi no hay ningun camino registrado. Toca mas cerca de uno.',
      sinAltura: 'sin datos de altura',
      cargandoOsm: 'Bajando los caminos del mapa\u2026'
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
      aviso: 'Hau zuk marrazten duzu: ibilbideetan agertzen diren bideetatik doa, baina ez da haietako bat.',
      red: 'Nondik joan daitekeen', misRutas: 'Nire ibilbideak bakarrik',
      todosPie: 'Bide guztiak · oinez', todosBici: 'Bide guztiak · bizikletaz',
      avisoOsm: 'OpenStreetMapeko bideak, lekuan bertan egiaztatu gabe.',
      sigueOsm: 'Ukitu beste puntu bat: bidea mapako edozein bidexkatatik doa.',
      lejosOsm: 'Hor ez dago erregistratutako biderik. Ukitu batetik gertuago.',
      sinAltura: 'altuera daturik gabe',
      cargandoOsm: 'Maparen bideak jaisten…'
    }
  };

  function metros(a, b){
    var dy = (a[0] - b[0]) * 111320, dx = (a[1] - b[1]) * KX;
    return Math.sqrt(dy * dy + dx * dx);
  }

  // ---- la red ------------------------------------------------------------

  // La red va en arrays tipados y la vecindad en CSR, no en un objeto por
  // nodo con clave de texto. Con los 66 tracks solos daba igual (46.000
  // nodos), pero con los caminos de OpenStreetMap son 354.216 nodos y la
  // diferencia es grande: medido en el navegador, construirla pasa de 908 a
  // 246 ms en escritorio y de 3.383 a 1.417 ms en un movil con la CPU
  // frenada 4x, y el consumo de memoria de 132 a 68 MB. Lo que mas costaba
  // eran las claves de texto de la tabla de celdas; ahora la celda se cifra
  // en un solo numero, que cabe de sobra en un double para este recuadro.
  //
  // Se mete en la red cada polilinea rellenada cada PASO_M: los puntos
  // vienen simplificados y dos caminos que se CRUZAN pueden caer en celdas
  // distintas, con lo que el cruce no existe y el calculo se va a buscar la
  // vuelta larga. Medido sobre 120 pares de puntos a 100-600 m: el rodeo
  // mediano baja de 1,94 a 1,58 veces la linea recta.
  function construyeRed(tracks, alturas, caminos, actividad){
    var clave = new Map();
    var lat = [], lon = [], alt = [];
    var ea = [], eb = [];

    function id(la, lo){
      var cx = Math.round(la * 111320 / CELDA_M);
      var cy = Math.round(lo * KX / CELDA_M);
      var k = cx * 4194304 + cy;
      var i = clave.get(k);
      if (i === undefined) {
        i = lat.length; clave.set(k, i);
        lat.push(la); lon.push(lo); alt.push(NaN);
      }
      return i;
    }
    // Sin comprobar si la arista ya existe: repetirla no cambia el resultado
    // de Dijkstra y buscarla costaba mas que el millon de aristas que salen.
    function une(a, b){ if (a !== b) { ea.push(a); eb.push(b); } }

    // alturas: un numero por punto de pts, o null. Los puntos de relleno la
    // interpolan entre los dos grabados que tienen a los lados; sin eso, el
    // GPX que se baja salia con altura en uno de cada cinco puntos.
    function mete(pts, alts){
      var prev = -1;
      for (var i = 0; i < pts.length; i++) {
        if (i > 0) {
          var A = pts[i - 1], B = pts[i];
          var dy = (A[0] - B[0]) * 111320, dx = (A[1] - B[1]) * KX;
          var largo = Math.sqrt(dy * dy + dx * dx);
          var hA = alts ? alts[i - 1] : null, hB = alts ? alts[i] : null;
          var hayH = typeof hA === 'number' && typeof hB === 'number';
          for (var k = 1; k * PASO_M < largo; k++) {
            var f = k * PASO_M / largo;
            var m = id(A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f);
            if (hayH && alt[m] !== alt[m]) alt[m] = Math.round(hA + (hB - hA) * f);
            if (prev >= 0) une(prev, m);
            prev = m;
          }
        }
        var n = id(pts[i][0], pts[i][1]);
        if (alts && alt[n] !== alt[n] && typeof alts[i] === 'number') alt[n] = alts[i];
        if (prev >= 0) une(prev, n);
        prev = n;
      }
    }

    tracks.forEach(function(t){
      var clv = t.href ? String(t.href).split('/').pop().replace('.html', '') : null;
      mete(t.points || [], (alturas && clv) ? alturas[clv] : null);
    });

    // Los caminos de OpenStreetMap, si el visitante ha pedido verlos. Vienen
    // como diferencias entre puntos consecutivos y con una mascara de para
    // que actividad sirve cada uno (1 = a pie, 2 = en bici). No traen altura:
    // ahi el perfil y el desnivel se quedan sin dato, y el panel lo dice.
    if (caminos && caminos.vias) {
      var esc = caminos.escala || 100000;
      var quiero = actividad === 'bici' ? 2 : 1;
      for (var v = 0; v < caminos.vias.length; v++) {
        var via = caminos.vias[v];
        if (!(via[0] & quiero)) continue;
        var la = via[1], lo = via[2];
        var pts = [[la / esc, lo / esc]];
        for (var j = 3; j < via.length; j += 2) {
          la += via[j]; lo += via[j + 1];
          pts.push([la / esc, lo / esc]);
        }
        mete(pts, null);
      }
    }

    var N = lat.length, M = ea.length;
    var LA = Float64Array.from(lat), LO = Float64Array.from(lon);
    var ALT = Float32Array.from(alt);
    lat = lon = alt = null;

    // CSR: se cuenta el grado de cada nodo, se acumulan los desplazamientos
    // y se vuelcan las aristas. Dos arrays planos en vez de 354.216 arrays.
    var off = new Int32Array(N + 1);
    for (var j2 = 0; j2 < M; j2++) { off[ea[j2]]++; off[eb[j2]]++; }
    var s = 0;
    for (var i2 = 0; i2 < N; i2++) { var g = off[i2]; off[i2] = s; s += g; }
    off[N] = s;
    var cursor = off.slice(0, N);
    var dest = new Int32Array(s), peso = new Float32Array(s);
    for (var j3 = 0; j3 < M; j3++) {
      var a = ea[j3], b = eb[j3];
      var dy3 = (LA[a] - LA[b]) * 111320, dx3 = (LO[a] - LO[b]) * KX;
      var w = Math.sqrt(dy3 * dy3 + dx3 * dx3);
      dest[cursor[a]] = b; peso[cursor[a]++] = w;
      dest[cursor[b]] = a; peso[cursor[b]++] = w;
    }
    ea = eb = null;

    // Rejilla de 100 m para encontrar el nodo mas cercano a un toque, en el
    // mismo formato CSR y con la misma clave numerica.
    var cCount = new Map();
    var cKey = new Int32Array(N);
    for (var i3 = 0; i3 < N; i3++) {
      var k3 = Math.round(LA[i3] * 111320 / 100) * 4194304 +
               Math.round(LO[i3] * KX / 100);
      cKey[i3] = cCount.has(k3) ? cCount.get(k3)[0] : cCount.size;
      if (!cCount.has(k3)) cCount.set(k3, [cCount.size, 0]);
      cCount.get(k3)[1]++;
    }
    var nC = cCount.size;
    var cOff = new Int32Array(nC + 1);
    cCount.forEach(function(par){ cOff[par[0]] = par[1]; });
    var t2 = 0;
    for (var c2 = 0; c2 < nC; c2++) { var gc = cOff[c2]; cOff[c2] = t2; t2 += gc; }
    cOff[nC] = t2;
    var cCur = cOff.slice(0, nC), cNod = new Int32Array(t2);
    for (var i4 = 0; i4 < N; i4++) cNod[cCur[cKey[i4]]++] = i4;

    return {
      N: N, LA: LA, LO: LO, ALT: ALT, off: off, dest: dest, peso: peso,
      cIndice: cCount, cOff: cOff, cNod: cNod,
      // Con la altura en el tercer sitio cuando la hay, que es lo que miran
      // «Guardar» y el GPX (typeof p[2] === 'number'). Los caminos de OSM no
      // la traen y ahi salen dos elementos, como antes salian los puntos sin
      // altura conocida.
      pt: function(i){
        return ALT[i] === ALT[i] ? [LA[i], LO[i], ALT[i]] : [LA[i], LO[i]];
      },
      alt: function(i){ return ALT[i] === ALT[i] ? ALT[i] : null; },
      largo: function(a, b){
        var dy = (LA[a] - LA[b]) * 111320, dx = (LO[a] - LO[b]) * KX;
        return Math.sqrt(dy * dy + dx * dx);
      }
    };
  }

  function nodoCerca(red, lat, lon){
    var cx = Math.round(lat * 111320 / 100), cy = Math.round(lon * KX / 100);
    var mejor = -1, mejorD = Infinity;
    for (var dx = -2; dx <= 2; dx++) for (var dy = -2; dy <= 2; dy++) {
      var par = red.cIndice.get((cx + dx) * 4194304 + (cy + dy));
      if (!par) continue;
      for (var p = red.cOff[par[0]]; p < red.cOff[par[0] + 1]; p++) {
        var i = red.cNod[p];
        var ey = (red.LA[i] - lat) * 111320, ex = (red.LO[i] - lon) * KX;
        var d = Math.sqrt(ey * ey + ex * ex);
        if (d < mejorD) { mejorD = d; mejor = i; }
      }
    }
    return mejorD <= MAX_ENGANCHE_M ? mejor : -1;
  }

  // Dijkstra con monticulo binario sobre el CSR. Con los 66 tracks solos son
  // 46.000 nodos; con los caminos de OSM, 354.216, y sigue tardando
  // milisegundos por toque porque para en cuanto saca el destino.
  function camino(red, desde, hasta){
    if (desde === hasta) return [desde];
    var n = red.N;
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
      for (var p2 = red.off[u]; p2 < red.off[u + 1]; p2++) {
        var v = red.dest[p2], nd = top[0] + red.peso[p2];
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
    // 'mis' = solo los 66 tracks de la web, como siempre. 'pie' y 'bici' =
    // esos mas los caminos de OpenStreetMap que sirvan para esa actividad.
    var modoRed = 'mis';
    var alturasDatos = null, caminosDatos = null;
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
      lista: '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
      // Una bifurcacion: de donde sale el lapiz y hacia donde puede tirar.
      red:   '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/>' +
             '<circle cx="18" cy="14" r="2.5"/><path d="M8 17.5l7.8-10.8"/><path d="M8.4 18l7.2-3.4"/>'
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
    tools.innerHTML = [['red', t.red], ['undo', t.deshacer], ['clear', t.borrar],
                       ['save', t.guardar], ['gpx', t.gpx], ['list', t.guardados]].map(function(par){
      var k = par[0] === 'list' ? 'lista' : par[0];
      return '<button type="button" class="draw-t" data-a="' + par[0] + '" title="' + par[1] +
             '" aria-label="' + par[1] + '">' + icono(ICO[k]) + '</button>';
    }).join('');
    marco.appendChild(tools);

    // Por donde se puede ir: solo las rutas del autor (lo de siempre) o
    // todos los caminos del mapa. Lo pidio el autor en dos opciones --
    // «mis rutas» y «para que pueda crear una ruta suya» -- y el «+» de
    // dentro, que elige la actividad, porque a pie se puede subir por unas
    // escaleras y en bici no.
    var redes = document.createElement('div');
    redes.className = 'draw-redes';
    redes.hidden = true;
    redes.innerHTML = [['mis', t.misRutas], ['pie', t.todosPie], ['bici', t.todosBici]]
      .map(function(par){
        return '<button type="button" class="draw-red-op" data-r="' + par[0] + '"' +
               ' aria-pressed="' + (par[0] === 'mis' ? 'true' : 'false') + '">' +
               par[1] + '</button>';
      }).join('') +
      '<p class="draw-red-nota">' + t.avisoOsm + '</p>';
    marco.appendChild(redes);

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
        for (var k = (i ? 1 : 0); k < tr.length; k++) out.push(red.pt(tr[k]));
      });
      return out;
    }

    // conAltura solo si la tienen TODOS los puntos, no si la tiene alguno.
    // Con los caminos de OpenStreetMap en la red esto importa: no traen
    // altura, y sumando solo los trozos que si la tienen salia un «+192 /
    // -297 m» que parecia el desnivel del recorrido entero y no lo era.
    // Antes no podia pasar, porque todos los nodos salian de los GPX.
    function totales(){
      var pts = recorrido(), km = 0, sub = 0, baj = 0, base = null, cima = null;
      var sinDato = 0;
      for (var i = 1; i < pts.length; i++) km += metros(pts[i - 1], pts[i]);
      pts.forEach(function(p){
        if (typeof p[2] !== 'number') { sinDato++; return; }
        if (base === null) { base = cima = p[2]; return; }
        if (p[2] > base + UMBRAL_SUBIDA_M) { sub += p[2] - base; base = p[2]; }
        else if (p[2] < base) base = p[2];
        if (p[2] < cima - UMBRAL_SUBIDA_M) { baj += cima - p[2]; cima = p[2]; }
        else if (p[2] > cima) cima = p[2];
      });
      return { km: km / 1000, subida: Math.round(sub), bajada: Math.round(baj),
               conAltura: base !== null && sinDato === 0 };
    }

    // Un perfil pequeno debajo de los totales: lo pidio el autor para saber
    // de un vistazo si el tramo que acaba de coger sube o baja, que en bici
    // y andando no da igual. Se dibuja en el sentido de la marcha, de
    // izquierda a derecha, con una rayita vertical en cada punto tocado para
    // ver donde empieza y acaba cada tramo.
    // Lo que sube y lo que baja un tramo suelto, con el mismo umbral que el
    // total. Es la pregunta del autor: «¿este tramo lo cojo de subida?».
    // Devuelve null si a algun nodo del tramo le falta la altura: mas vale
    // no decir nada que dar un numero que no cubre todo el tramo.
    function desnivelDe(tr){
      var sub = 0, baj = 0, base = null, cima = null, sinDato = 0;
      tr.forEach(function(id){
        var e = red.alt(id);
        if (typeof e !== 'number') { sinDato++; return; }
        if (base === null) { base = cima = e; return; }
        if (e > base + UMBRAL_SUBIDA_M) { sub += e - base; base = e; }
        else if (e < base) base = e;
        if (e < cima - UMBRAL_SUBIDA_M) { baj += cima - e; cima = e; }
        else if (e > cima) cima = e;
      });
      if (base === null || sinDato) return null;
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
          llevo += red.largo(tr[q - 1], tr[q]);
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
        var n = red.pt(id);
        puntitos.push(L.marker([n[0], n[1]], {
          interactive: false,
          icon: L.divIcon({ className: 'draw-dot' + (i === 0 ? ' is-first' : ''),
                            iconSize: [12, 12], iconAnchor: [6, 6] })
        }).addTo(map));
      });
      var tt = totales();
      elTot.hidden = pts.length < 2;
      elKm.textContent = tt.km.toFixed(2).replace('.', ',') + ' km';
      elDes.textContent = tt.conAltura
        ? ((tt.subida || tt.bajada) ? ' · +' + tt.subida + ' / -' + tt.bajada + ' m ' + t.aprox : '')
        : (pts.length > 1 ? ' \u00b7 ' + t.sinAltura : '');
      // Sin altura en todos los puntos, el perfil dibujaria una linea que no
      // es el terreno: mejor no dibujar ninguna.
      elPerfil.innerHTML = tt.conAltura ? perfil() : '';
      var dUlt = tramos.length > 1 ? desnivelDe(tramos[tramos.length - 1]) : null;
      elUlt.textContent = dUlt ? t.ultimo + ' ' + dUlt : '';
      elUlt.hidden = !dUlt;
      elMsg.textContent = anclas.length
        ? (modoRed === 'mis' ? t.sigue : t.sigueOsm)
        : t.arranque;
    }

    function alTocar(e){
      if (!activo || !red) return;
      var n = nodoCerca(red, e.latlng.lat, e.latlng.lng);
      if (n < 0) { elMsg.textContent = modoRed === 'mis' ? t.lejos : t.lejosOsm; return; }
      if (!anclas.length) { cargado = null; anclas.push(n); tramos.push([n]); pinta(); return; }
      var ultimo = anclas[anclas.length - 1];
      var tr = camino(red, ultimo, n);
      if (!tr) { elMsg.textContent = t.sinpaso; return; }
      anclas.push(n); tramos.push(tr); pinta();
      // Un tramo puede salir disparado a un lado y no se entiende por que:
      // es que entre esos dos puntos no hay ningun camino grabado mas corto
      // y la red tiene que dar la vuelta. Se dice, con los metros de mas.
      var largo = 0, i;
      for (i = 1; i < tr.length; i++) largo += red.largo(tr[i - 1], tr[i]);
      var recto = red.largo(ultimo, n);
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
        elDes.textContent = tg.conAltura
          ? ((tg.subida || tg.bajada) ? ' · +' + tg.subida + ' / -' + tg.bajada + ' m ' + t.aprox : '')
          : ' · ' + t.sinAltura;
        elPerfil.innerHTML = tg.conAltura ? perfil() : '';
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
      else if (a === 'red') { saved.hidden = true; redes.hidden = !redes.hidden; }
      else if (a === 'list') { redes.hidden = true; pintaGuardados(); saved.hidden = !saved.hidden; }
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
      preparaRed();
    }

    // Monta la red que toque. Los dos ficheros se bajan una sola vez y se
    // quedan: cambiar de modo no vuelve a pedirlos, solo reconstruye.
    function preparaRed(puntosViejos){
      if (cargando) return;
      cargando = true;
      var quiereOsm = modoRed !== 'mis';
      elMsg.textContent = (quiereOsm && !caminosDatos) ? t.cargandoOsm : t.cargando;
      var pide = [];
      pide.push(alturasDatos ? Promise.resolve(alturasDatos)
        : fetch('data/alturas.json').then(function(r){ return r.ok ? r.json() : null; })
            .catch(function(){ return null; }));
      pide.push(!quiereOsm ? Promise.resolve(null)
        : (caminosDatos ? Promise.resolve(caminosDatos)
            : fetch('data/caminos.json').then(function(r){ return r.ok ? r.json() : null; })
                .catch(function(){ return null; })));
      Promise.all(pide).then(function(r){
        alturasDatos = r[0] || alturasDatos;
        if (quiereOsm) {
          caminosDatos = r[1] || caminosDatos;
          // Si los caminos no llegan, no se deja al visitante con el modo
          // puesto y sin red: se vuelve a las rutas y se dice.
          if (!caminosDatos) { modoRed = 'mis'; marcaModo(); }
        }
        red = construyeRed(d.datos.tracks || [], alturasDatos,
                           modoRed === 'mis' ? null : caminosDatos, modoRed);
        cargando = false;
        if (puntosViejos) reengancha(puntosViejos);
        pinta();
      }).catch(function(){ cargando = false; elMsg.textContent = t.fallo; });
    }

    // Al cambiar de red, los nodos tocados ya no valen: son indices de la
    // red vieja. Se vuelven a enganchar por coordenadas y se recalculan los
    // tramos. Si alguno deja de tener camino, se para ahi y se queda lo que
    // si ha salido, en vez de borrarle el trabajo al visitante.
    function reengancha(puntos){
      if (!puntos.length) return;
      var nuevas = [], nuevosTramos = [];
      for (var i = 0; i < puntos.length; i++) {
        if (!puntos[i]) break;
        var n = nodoCerca(red, puntos[i][0], puntos[i][1]);
        if (n < 0) break;
        if (!nuevas.length) { nuevas.push(n); nuevosTramos.push([n]); continue; }
        var tr = camino(red, nuevas[nuevas.length - 1], n);
        if (!tr) break;
        nuevas.push(n); nuevosTramos.push(tr);
      }
      anclas = nuevas; tramos = nuevosTramos;
    }

    function marcaModo(){
      redes.querySelectorAll('.draw-red-op').forEach(function(b){
        b.setAttribute('aria-pressed', String(b.dataset.r === modoRed));
      });
      tools.querySelector('[data-a="red"]').classList.toggle('is-on', modoRed !== 'mis');
      caja.classList.toggle('red-osm', modoRed !== 'mis');
    }

    redes.addEventListener('click', function(e){
      var b = e.target.closest('.draw-red-op');
      if (!b || cargando) return;
      var r = b.dataset.r;
      redes.hidden = true;
      if (r === modoRed) return;
      // Las coordenadas de los puntos tocados, antes de tirar la red vieja:
      // despues sus indices no significan nada.
      var puntosViejos = red ? anclas.map(function(id){ return red.pt(id); }) : [];
      modoRed = r;
      marcaModo();
      red = null;
      preparaRed(puntosViejos);
    });

    btn.addEventListener('click', function(){ activo ? apaga() : enciende(); });
  });
})();
