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

  var UMBRAL_SUBIDA_M = 5;       // para no sumar el ruido del GPS como desnivel
  var ALMACEN = 'rutas-mallabia-trazados';
  var COLOR = '#38BDF8';
  var LAT0 = 43.2;
  var KX = 111320 * Math.cos(LAT0 * Math.PI / 180);

  var T = {
    es: {
      abrir: 'Dibujar un trazado', cerrar: 'Cerrar el dibujo',
      titulo: 'Tu trazado', arranque: 'Toca el mapa sobre un camino para empezar.',
      sigue: 'Toca otro punto: el camino va por los senderos y pistas de OpenStreetMap.',
      lejos: 'Ahi no hay ningun camino. Toca mas cerca de uno.',
      sinpaso: 'No hay camino hasta ahi dentro de la red.',
      deshacer: 'Deshacer', borrar: 'Borrar', guardar: 'Guardar', gpx: 'Bajar GPX',
      guardados: 'Guardados', abrirlo: 'Abrir', quitar: 'Quitar',
      circulo: 'Cerrar el c\u00edrculo', vaiven: 'Ida y vuelta',
      pocos: 'Marca al menos dos puntos antes.',
      yacerrado: 'El trazado ya vuelve al punto de partida.',
      nocierra: 'No hay camino de vuelta al principio dentro de la red.',
      mueve: 'Arrastra un punto para cambiar por d\u00f3nde va.',
      nombre: 'Trazado', aprox: 'aprox.', ultimo: '\u00daltimo tramo', cargando: 'Preparando la red de caminos…',
      fallo: 'No se ha podido preparar la red. Prueba a recargar.',
      rodeo: 'Ese tramo da un rodeo de %s km: entre esos dos puntos no hay ning\u00fan camino m\u00e1s corto. Deshazlo y prueba con un punto intermedio.',
      aviso: 'Esto lo dibujas tu: va por los caminos de OpenStreetMap y por las rutas de la web, pero no es ninguna de ellas.'
    },
    eu: {
      abrir: 'Marrazki bat egin', cerrar: 'Marrazkia itxi',
      titulo: 'Zure marrazkia', arranque: 'Ukitu mapa bide baten gainean hasteko.',
      sigue: 'Ukitu beste puntu bat: bidea OpenStreetMap-eko bidexka eta pistetatik doa.',
      lejos: 'Hor ez dago biderik. Ukitu bide batetik gertuago.',
      sinpaso: 'Ez dago biderik hormaino sarearen barruan.',
      deshacer: 'Desegin', borrar: 'Ezabatu', guardar: 'Gorde', gpx: 'GPXa jaitsi',
      guardados: 'Gordeta', abrirlo: 'Ireki', quitar: 'Kendu',
      circulo: 'Zirkulua itxi', vaiven: 'Joan-etorria',
      pocos: 'Markatu gutxienez bi puntu lehenago.',
      yacerrado: 'Marrazkia abiapuntura itzultzen da jada.',
      nocierra: 'Ez dago hasierara itzultzeko biderik sarearen barruan.',
      mueve: 'Arrastatu puntu bat nondik doan aldatzeko.',
      nombre: 'Marrazkia', aprox: 'gutxi gorabehera', ultimo: 'Azken tartea', cargando: 'Bideen sarea prestatzen…',
      fallo: 'Ezin izan da sarea prestatu. Saiatu orria berriro kargatzen.',
      rodeo: 'Tarte horrek %s km-ko bira ematen du: bi puntu horien artean ez dago bide laburragorik. Desegin eta saiatu tarteko puntu batekin.',
      aviso: 'Hau zuk marrazten duzu: OpenStreetMap-eko bideetatik eta webeko ibilbideetatik doa, baina ez da haietako bat.'
    }
  };

  function metros(a, b){
    var dy = (a[0] - b[0]) * 111320, dx = (a[1] - b[1]) * KX;
    return Math.sqrt(dy * dy + dx * dx);
  }

  // ---- la red ------------------------------------------------------------

  // ======================= LA RED DE CAMINOS =============================
  // Hasta noviembre de 2026 esta red se hacia con los tracks de las rutas
  // publicadas, pegados a una rejilla de 15 m. Tenia un techo medido: las
  // rutas abarcan 24 x 22,7 km y solo el 26% de ese recuadro esta a menos de
  // 120 m de un camino grabado, asi que 74 de cada 100 toques no enganchaban
  // nada. No era el codigo: es que la red solo tenia lo grabado.
  //
  // Ahora la red se baja hecha (data/caminos-zona.json, de scripts/
  // make_caminos.py): 41.632 cruces, 52.567 tramos y 6.656 km de caminos de
  // OpenStreetMap, MAS los 239 trozos de las rutas publicadas que OSM no
  // tiene -83 km-. Cubre el 99,8% de los puntos de las 72 rutas, asi que no
  // se pierde nada de lo que el lapiz ya sabia dibujar.
  //
  // POR QUE UN GRAFO CONTRAIDO Y NO PUNTO A PUNTO. Con 6.656 km, rellenar
  // cada 5 m como antes son 1,3 millones de nodos, y cada nodo y cada vecino
  // es un array de JavaScript: no cabe en un movil. Aqui los nodos son solo
  // los cruces y la forma del camino va colgada de cada tramo; el calculo
  // corre sobre los cruces y la forma solo se usa para dibujar. Las
  // coordenadas y la adyacencia van en arrays tipados -unos 10 MB en vez de
  // 80- y la adyacencia en formato CSR, que es un array plano y no 41.632
  // arrays sueltos.
  //
  // Y EL TOQUE NO SE PEGA AL CRUCE MAS CERCANO, sino al punto mas cercano
  // DEL CAMINO. Entre cruce y cruce hay 127 m de media: pegar al cruce
  // movería el punto hasta 60 m de donde has tocado. Lo que se hace es
  // proyectar el toque sobre el tramo y arrancar el calculo desde ahi, con
  // los dos extremos del tramo como primeros pasos.
  var MAX_ENGANCHE_M = 120;      // mas lejos de esto, el toque no coge camino
  var CELDA_BUSCA_M = 100;       // rejilla para encontrar el tramo de un toque
  var PASO_CESTA_M = 40;         // cada cuanto se marca un tramo en la rejilla
  var CELDA_ALTURA_M = 50;       // rejilla de alturas sacada de los tracks
  var ALTURA_CERCA_M = 60;       // mas lejos que esto, un punto va sin altura
  // Lo que cuesta un metro de cada clase de via. Un sendero y una pista
  // valen igual; una carretera pesa mas para que no te mande por ella
  // habiendo camino al lado, y una nacional o un camino privado, mucho mas.
  //   0 sendero  1 pista  2 calle o servicio  3 carretera  4 bidegorri
  //   5 nacional  6 privado  7 trozo grabado por el autor
  var COSTE_CLASE = [1, 1, 1.05, 1.35, 1, 3, 5, 1];

  function rejillaAlturas(alturas, tracks){
    // Las alturas siguen saliendo de los tracks publicados, como antes: OSM
    // no trae cotas. Se guardan en celdas de 50 m, asi que un camino que
    // pase por donde pasa una ruta hereda su altura y el perfil funciona.
    var rej = Object.create(null);
    if (!alturas || !tracks) return rej;
    tracks.forEach(function(tk){
      var pts = tk.points || [];
      var alt = tk.href ? alturas[String(tk.href).split('/').pop().replace('.html', '')] : null;
      if (!alt) return;
      for (var i = 0; i < pts.length; i++) {
        var e = alt[i];
        if (typeof e !== 'number') continue;
        var k = Math.round(pts[i][0] * 111320 / CELDA_ALTURA_M) + ':' +
                Math.round(pts[i][1] * KX / CELDA_ALTURA_M);
        if (rej[k] === undefined) rej[k] = e;
      }
    });
    return rej;
  }

  function alturaEn(red, lat, lon){
    var cx = Math.round(lat * 111320 / CELDA_ALTURA_M);
    var cy = Math.round(lon * KX / CELDA_ALTURA_M);
    var salto = Math.ceil(ALTURA_CERCA_M / CELDA_ALTURA_M);
    for (var r = 0; r <= salto; r++) {
      for (var dx = -r; dx <= r; dx++) for (var dy = -r; dy <= r; dy++) {
        if (r && Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
        var e = red.alturas[(cx + dx) + ':' + (cy + dy)];
        if (e !== undefined) return e;
      }
    }
    return null;
  }

  // Los puntos de un tramo, del extremo «ini» al «fin», forma incluida.
  function puntosDe(red, k){
    var g = red.geo[k], out = [[red.lat[red.ini[k]], red.lon[red.ini[k]]]], i;
    for (i = 0; i < g.length; i += 2) out.push([g[i], g[i + 1]]);
    out.push([red.lat[red.fin[k]], red.lon[red.fin[k]]]);
    return out;
  }

  function construyeRed(datos, alturas, tracks){
    var esc = datos.escala || 100000;
    var dn = datos.nodos, n = dn.length / 2, i, k;
    var lat = new Float64Array(n), lon = new Float64Array(n);
    var x = 0, y = 0;
    for (i = 0; i < n; i++) { x += dn[2 * i]; y += dn[2 * i + 1]; lat[i] = x / esc; lon[i] = y / esc; }
    var t = datos.tramos, ini = [], fin = [], cls = [], lar = [], geo = [];
    i = 0;
    while (i + 4 < t.length) {
      var a = t[i], b = t[i + 1], c = t[i + 2], largo = t[i + 3], kk = t[i + 4];
      i += 5;
      var g = new Float64Array(kk * 2);
      var gx = Math.round(lat[a] * esc), gy = Math.round(lon[a] * esc);
      for (k = 0; k < kk; k++) {
        gx += t[i]; gy += t[i + 1]; i += 2;
        g[2 * k] = gx / esc; g[2 * k + 1] = gy / esc;
      }
      ini.push(a); fin.push(b); cls.push(c); lar.push(largo); geo.push(g);
    }
    var m = ini.length;
    var grado = new Int32Array(n);
    for (k = 0; k < m; k++) { grado[ini[k]]++; grado[fin[k]]++; }
    var arranque = new Int32Array(n + 1);
    for (i = 0; i < n; i++) arranque[i + 1] = arranque[i] + grado[i];
    var cursor = arranque.slice(0, n);
    var vecino = new Int32Array(2 * m), porTramo = new Int32Array(2 * m);
    for (k = 0; k < m; k++) {
      vecino[cursor[ini[k]]] = fin[k]; porTramo[cursor[ini[k]]++] = k;
      vecino[cursor[fin[k]]] = ini[k]; porTramo[cursor[fin[k]]++] = k;
    }
    var red = {
      lat: lat, lon: lon, n: n, m: m,
      ini: Int32Array.from(ini), fin: Int32Array.from(fin),
      clase: Uint8Array.from(cls), largo: Float32Array.from(lar), geo: geo,
      arranque: arranque, vecino: vecino, porTramo: porTramo,
      alturas: rejillaAlturas(alturas, tracks), cestas: Object.create(null)
    };
    for (k = 0; k < m; k++) {
      var pts = puntosDe(red, k), visto = null;
      for (i = 1; i < pts.length; i++) {
        var p = pts[i - 1], q = pts[i], d = metros(p, q);
        var pasos = Math.max(1, Math.ceil(d / PASO_CESTA_M));
        for (var j = 0; j <= pasos; j++) {
          var f = j / pasos;
          var cx = Math.round((p[0] + (q[0] - p[0]) * f) * 111320 / CELDA_BUSCA_M);
          var cy = Math.round((p[1] + (q[1] - p[1]) * f) * KX / CELDA_BUSCA_M);
          var key = cx + ':' + cy;
          if (key === visto) continue;
          visto = key;
          var lista = red.cestas[key] || (red.cestas[key] = []);
          if (lista[lista.length - 1] !== k) lista.push(k);
        }
      }
    }
    return red;
  }

  // El punto del camino mas cercano a un toque. Devuelve un ancla:
  // {p:[lat,lon,altura], tr:tramo, seg:indice del trozo, t:fraccion}.
  function engancha(red, lat, lon){
    var cx = Math.round(lat * 111320 / CELDA_BUSCA_M);
    var cy = Math.round(lon * KX / CELDA_BUSCA_M);
    var kx = Math.cos(lat * Math.PI / 180) * 111195, ky = 111195;
    var mejor = null, mejorD = MAX_ENGANCHE_M, mirados = Object.create(null);
    for (var dx = -2; dx <= 2; dx++) for (var dy = -2; dy <= 2; dy++) {
      var lista = red.cestas[(cx + dx) + ':' + (cy + dy)];
      if (!lista) continue;
      for (var z = 0; z < lista.length; z++) {
        var k = lista[z];
        if (mirados[k]) continue;
        mirados[k] = 1;
        var pts = puntosDe(red, k);
        for (var i = 1; i < pts.length; i++) {
          var ax = (pts[i - 1][1] - lon) * kx, ay = (pts[i - 1][0] - lat) * ky;
          var bx = (pts[i][1] - pts[i - 1][1]) * kx, by = (pts[i][0] - pts[i - 1][0]) * ky;
          var nn = bx * bx + by * by;
          var tt = nn ? Math.max(0, Math.min(1, -(ax * bx + ay * by) / nn)) : 0;
          var d = Math.hypot(ax + tt * bx, ay + tt * by);
          if (d < mejorD) {
            mejorD = d;
            mejor = { tr: k, seg: i - 1, t: tt,
                      p: [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * tt,
                          pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * tt] };
          }
        }
      }
    }
    if (!mejor) return null;
    mejor.p.push(alturaEn(red, mejor.p[0], mejor.p[1]));
    return mejor;
  }

  // Del ancla hasta uno de los dos extremos de su tramo, con los puntos de
  // la forma que queden por el camino. hacia = 1 al «fin», -1 al «ini».
  function haciaExtremo(red, anc, hacia){
    var pts = puntosDe(red, anc.tr), out = [anc.p.slice(0, 2)], i;
    if (hacia > 0) for (i = anc.seg + 1; i < pts.length; i++) out.push(pts[i]);
    else for (i = anc.seg; i >= 0; i--) out.push(pts[i]);
    var largo = 0;
    for (i = 1; i < out.length; i++) largo += metros(out[i - 1], out[i]);
    return { pts: out, largo: largo };
  }

  // Dijkstra con monticulo binario sobre los cruces. 41.632 nodos y 52.567
  // tramos: unos milisegundos.
  function dijkstra(red, origenes){
    var n = red.n;
    var dist = new Float64Array(n); dist.fill(Infinity);
    var antes = new Int32Array(n); antes.fill(-1);
    var porDonde = new Int32Array(n); porDonde.fill(-1);
    var visto = new Uint8Array(n);
    var heap = [];
    function sube(i){
      while (i > 0) {
        var p = (i - 1) >> 1;
        if (heap[p][0] <= heap[i][0]) break;
        var tmp = heap[p]; heap[p] = heap[i]; heap[i] = tmp; i = p;
      }
    }
    function baja(i){
      for (;;) {
        var l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap.length && heap[l][0] < heap[m][0]) m = l;
        if (r < heap.length && heap[r][0] < heap[m][0]) m = r;
        if (m === i) break;
        var tmp = heap[m]; heap[m] = heap[i]; heap[i] = tmp; i = m;
      }
    }
    origenes.forEach(function(o){
      if (o.coste < dist[o.nodo]) { dist[o.nodo] = o.coste; heap.push([o.coste, o.nodo]); sube(heap.length - 1); }
    });
    while (heap.length) {
      var top = heap[0];
      heap[0] = heap[heap.length - 1]; heap.pop(); if (heap.length) baja(0);
      var u = top[1];
      if (visto[u]) continue;
      visto[u] = 1;
      for (var e = red.arranque[u]; e < red.arranque[u + 1]; e++) {
        var v = red.vecino[e], k = red.porTramo[e];
        var nd = top[0] + red.largo[k] * COSTE_CLASE[red.clase[k]];
        if (nd < dist[v]) {
          dist[v] = nd; antes[v] = u; porDonde[v] = k;
          heap.push([nd, v]); sube(heap.length - 1);
        }
      }
    }
    return { dist: dist, antes: antes, porDonde: porDonde, visto: visto };
  }

  // El camino entre dos anclas, ya en puntos [lat, lon, altura].
  function rutaEntre(red, A, B){
    if (!A || !B) return null;
    var out, i;
    if (A.tr === B.tr) {
      // En el mismo tramo no hay nada que calcular: es el trozo de camino
      // que va de uno a otro.
      var pts = puntosDe(red, A.tr);
      var delante = (B.seg > A.seg) || (B.seg === A.seg && B.t >= A.t);
      out = [A.p.slice(0, 2)];
      if (delante) for (i = A.seg + 1; i <= B.seg; i++) out.push(pts[i]);
      else for (i = A.seg; i > B.seg; i--) out.push(pts[i]);
      out.push(B.p.slice(0, 2));
      return conAltura(red, out);
    }
    var aIni = haciaExtremo(red, A, -1), aFin = haciaExtremo(red, A, 1);
    var bIni = haciaExtremo(red, B, -1), bFin = haciaExtremo(red, B, 1);
    var fA = COSTE_CLASE[red.clase[A.tr]], fB = COSTE_CLASE[red.clase[B.tr]];
    var res = dijkstra(red, [
      { nodo: red.ini[A.tr], coste: aIni.largo * fA },
      { nodo: red.fin[A.tr], coste: aFin.largo * fA }
    ]);
    var metas = [
      { nodo: red.ini[B.tr], cola: bIni, coste: bIni.largo * fB },
      { nodo: red.fin[B.tr], cola: bFin, coste: bFin.largo * fB }
    ];
    var mejor = null, mejorC = Infinity;
    metas.forEach(function(mt){
      if (!res.visto[mt.nodo]) return;
      var c = res.dist[mt.nodo] + mt.coste;
      if (c < mejorC) { mejorC = c; mejor = mt; }
    });
    if (!mejor) return null;
    // Desde la meta hacia atras, apuntando por que tramo se llego.
    var cadena = [], x = mejor.nodo;
    while (x !== -1 && res.porDonde[x] >= 0) {
      cadena.push({ hasta: x, tramo: res.porDonde[x] });
      x = res.antes[x];
    }
    cadena.reverse();
    // x es ahora el extremo de A por el que se salio.
    var salida = x;
    out = (salida === red.ini[A.tr] ? aIni : aFin).pts.slice();
    cadena.forEach(function(paso){
      var k = paso.tramo, pts = puntosDe(red, k);
      if (paso.hasta === red.fin[k]) { for (i = 1; i < pts.length; i++) out.push(pts[i]); }
      else { for (i = pts.length - 2; i >= 0; i--) out.push(pts[i]); }
    });
    var cola = mejor.cola.pts.slice().reverse();   // del extremo hasta B
    for (i = 1; i < cola.length; i++) out.push(cola[i]);
    return conAltura(red, out);
  }

  function conAltura(red, pts){
    var out = [], i, ultimo = null;
    for (i = 0; i < pts.length; i++) {
      var p = pts[i];
      if (ultimo && metros(ultimo, p) < 0.5) continue;
      ultimo = p;
      out.push([p[0], p[1], alturaEn(red, p[0], p[1])]);
    }
    return out.length > 1 ? out : null;
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
      lista: '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
      circulo: '<path d="M21 12a9 9 0 1 1-3.3-6.9"/><path d="M21 3v6h-6"/>',
      vaiven: '<path d="M4 12h16"/><path d="M8 7l-4 5 4 5"/><path d="M16 7l4 5-4 5"/>'
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
    // «Cerrar el circulo» e «Ida y vuelta» salen SOLO con dos puntos o mas
    // (los pone y los quita pinta()): sin ellos no hacen nada y la columna
    // de botones vive dentro del mapa, donde el alto cuenta.
    tools.innerHTML = [['undo', t.deshacer], ['circulo', t.circulo], ['vaiven', t.vaiven],
                       ['clear', t.borrar], ['save', t.guardar],
                       ['gpx', t.gpx], ['list', t.guardados]].map(function(par){
      var k = par[0] === 'list' ? 'lista' : par[0];
      var extra = (par[0] === 'circulo' || par[0] === 'vaiven') ? ' hidden' : '';
      return '<button type="button" class="draw-t" data-a="' + par[0] + '" title="' + par[1] +
             '" aria-label="' + par[1] + '"' + extra + '>' + icono(ICO[k]) + '</button>';
    }).join('');
    var btCirculo = tools.querySelector('[data-a="circulo"]');
    var btVaiven = tools.querySelector('[data-a="vaiven"]');
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
        for (var k = (i ? 1 : 0); k < tr.length; k++) out.push(tr[k]);
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
      tr.forEach(function(p){
        var e = p[2];
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
          llevo += metros(tr[q - 1], tr[q]);
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

    // CERRAR EL CIRCULO. 52 de las 68 rutas de la web empiezan y acaban a
    // menos de 100 m: el circuito es lo normal aqui, y hasta ahora habia que
    // volver al punto de partida a toques. Esto une el ultimo punto con el
    // primero por el camino mas corto de la red, que es lo mismo que hace
    // cualquier otro planificador («Loop to Start» en Garmin, «loop» en
    // HiiKER). El nodo repetido al final es a proposito: asi el trazado
    // sigue cumpliendo que tramos[k] va de anclas[k-1] a anclas[k].
    function cierraCirculo(){
      if (anclas.length < 2) { elMsg.textContent = t.pocos; return; }
      var ini = anclas[0], fin = anclas[anclas.length - 1];
      if (ini === fin) { elMsg.textContent = t.yacerrado; return; }
      var tr = rutaEntre(red, fin, ini);
      if (!tr) { elMsg.textContent = t.nocierra; return; }
      anclas.push(ini); tramos.push(tr); cargado = null; pinta();
    }

    // IDA Y VUELTA. No calcula nada: copia los tramos en orden inverso y
    // cada uno del reves, que es exactamente el camino de vuelta.
    function idaYVuelta(){
      if (anclas.length < 2) { elMsg.textContent = t.pocos; return; }
      var i, maa = [], mtt = [];
      for (i = tramos.length - 1; i >= 1; i--) {
        mtt.push(tramos[i].slice().reverse());
        maa.push(anclas[i - 1]);
      }
      anclas = anclas.concat(maa); tramos = tramos.concat(mtt);
      cargado = null; pinta();
    }

    // ARRASTRAR UN PUNTO YA PUESTO. Antes, para corregir el segundo toque de
    // ocho habia que deshacer los seis de despues. Aqui solo se recalculan
    // los dos tramos que tocan al punto movido, y si alguno no sale no se
    // toca nada. Si el trazado esta cerrado, el primer punto y el ultimo son
    // el mismo nodo: hay que mover los dos o el circulo se abre.
    function mueveAncla(i, lat, lon){
      var n = engancha(red, lat, lon);
      if (!n) { elMsg.textContent = t.lejos; pinta(); return; }
      var ult = anclas.length - 1;
      var cerrado = ult > 1 && anclas[0] === anclas[ult];
      var idx = (cerrado && i === ult) ? 0 : i;
      var na = anclas.slice(), nt = tramos.slice(), tocar = [], k, j, tr;
      na[idx] = n;
      if (cerrado && idx === 0) na[ult] = n;
      if (idx > 0) tocar.push(idx);
      if (idx + 1 <= ult) tocar.push(idx + 1);
      if (cerrado && idx === 0 && tocar.indexOf(ult) < 0) tocar.push(ult);
      for (k = 0; k < tocar.length; k++) {
        j = tocar[k];
        tr = rutaEntre(red, na[j - 1], na[j]);
        if (!tr) { elMsg.textContent = t.sinpaso; pinta(); return; }
        nt[j] = tr;
      }
      if (idx === 0) nt[0] = [n.p];
      anclas = na; tramos = nt; cargado = null; pinta();
    }

    function pinta(){
      var pts = recorrido();
      quitaLinea();
      puntitos.forEach(function(m){ map.removeLayer(m); });
      puntitos = [];
      if (pts.length > 1) linea = dibujaLinea(pts.map(function(p){ return [p[0], p[1]]; }));
      // Con el trazado cerrado, el ultimo punto es el mismo nodo que el
      // primero: se dibuja uno solo, o quedarian dos bolas superpuestas y no
      // se sabria cual estas arrastrando.
      var cerrado = anclas.length > 2 && anclas[0] === anclas[anclas.length - 1];
      anclas.forEach(function(anc, i){
        if (cerrado && i === anclas.length - 1) return;
        var n = anc.p;
        var m = L.marker([n[0], n[1]], {
          draggable: true, autoPan: true, keyboard: false,
          icon: L.divIcon({ className: 'draw-dot' + (i === 0 ? ' is-first' : ''),
                            iconSize: [12, 12], iconAnchor: [6, 6] })
        }).addTo(map);
        m.on('dragend', function(ev){
          var ll = ev.target.getLatLng();
          mueveAncla(i, ll.lat, ll.lng);
        });
        puntitos.push(m);
      });
      if (btCirculo) btCirculo.hidden = anclas.length < 2;
      if (btVaiven) btVaiven.hidden = anclas.length < 2;
      var tt = totales();
      elTot.hidden = pts.length < 2;
      elKm.textContent = tt.km.toFixed(2).replace('.', ',') + ' km';
      elDes.textContent = tt.conAltura && (tt.subida || tt.bajada)
        ? ' · +' + tt.subida + ' / -' + tt.bajada + ' m ' + t.aprox : '';
      elPerfil.innerHTML = perfil();
      elUlt.textContent = tramos.length > 1 ? t.ultimo + ' ' + desnivelDe(tramos[tramos.length - 1]) : '';
      elUlt.hidden = tramos.length < 2;
      elMsg.textContent = !anclas.length ? t.arranque : (anclas.length > 1 ? t.mueve : t.sigue);
    }

    function alTocar(e){
      if (!activo || !red) return;
      var n = engancha(red, e.latlng.lat, e.latlng.lng);
      if (n < 0) { elMsg.textContent = t.lejos; return; }
      if (!anclas.length) { cargado = null; anclas.push(n); tramos.push([n.p]); pinta(); return; }
      var ultimo = anclas[anclas.length - 1];
      var tr = rutaEntre(red, ultimo, n);
      if (!tr) { elMsg.textContent = t.sinpaso; return; }
      anclas.push(n); tramos.push(tr); pinta();
      // Un tramo puede salir disparado a un lado y no se entiende por que:
      // es que entre esos dos puntos no hay ningun camino grabado mas corto
      // y la red tiene que dar la vuelta. Se dice, con los metros de mas.
      var largo = 0, i;
      for (i = 1; i < tr.length; i++) largo += metros(tr[i - 1], tr[i]);
      var recto = metros(ultimo.p, n.p);
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
      else if (a === 'circulo') { cierraCirculo(); }
      else if (a === 'vaiven') { idaYVuelta(); }
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

    // La tira de fichas de debajo del mapa se esconde mientras se dibuja --
    // ahi manda el trazo, y tocar una ficha abriria una ruta encima de lo que
    // se esta dibujando. La pinta map.js desde updateLabelVisibility(), que
    // corre en zoomend y moveend: entrar o salir del lapiz no dispara
    // ninguno de los dos, asi que hay que avisarle. Es el mismo gancho que
    // usa filters.js al cambiar de vista, y tambien le viene bien el
    // invalidateSize, que la caja acaba de cambiar de tamano.
    // Y en la vista de mapa de la portada, con la tira escondida, la caja se
    // baja hasta la barra para quedarse con esos 200 px en vez de dejar un
    // hueco. Eso lo hace el CSS con body.dibujando.
    function avisaAlMapa(){
      if (document.body && document.body.classList) {
        document.body.classList.toggle('dibujando', activo);
      }
      if (window.__avisaMapaTamano) { try { window.__avisaMapaTamano(); } catch (e) {} }
    }

    function apaga(){
      activo = false;
      tools.hidden = true; readout.hidden = true; saved.hidden = true;
      btn.classList.remove('is-active');
      btn.setAttribute('aria-label', t.abrir);
      btn.title = t.abrir;
      caja.classList.remove('is-drawing');
      sueltaEncaje();
      avisaAlMapa();
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
      avisaAlMapa();
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
      // Dos ficheros: la red de caminos -638 KB por el cable- y las alturas.
      // La red es lo unico imprescindible; si fallan las alturas se dibuja
      // igual y lo que se pierde es el perfil, como antes.
      Promise.all([
        fetch('data/caminos-zona.json').then(function(r){ return r.ok ? r.json() : null; }),
        fetch('data/alturas.json').then(function(r){ return r.ok ? r.json() : null; })
          .catch(function(){ return null; })
      ]).then(function(pareja){
        if (!pareja[0] || !pareja[0].nodos || !pareja[0].tramos) throw new Error('sin red');
        red = construyeRed(pareja[0], pareja[1], d.datos.tracks || []);
        cargando = false;
        pinta();
      }).catch(function(){ cargando = false; elMsg.textContent = t.fallo; });
    }

    btn.addEventListener('click', function(){ activo ? apaga() : enciende(); });
  });
})();
