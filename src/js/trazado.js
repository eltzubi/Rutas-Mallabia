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
      sigue: 'Toca otro punto y el camino se calcula solo, por los senderos de las rutas.',
      lejos: 'Ahi no pasa ninguna ruta. Toca mas cerca de un camino dibujado.',
      sinpaso: 'No hay camino hasta ahi dentro de la red.',
      deshacer: 'Deshacer', borrar: 'Borrar', guardar: 'Guardar', gpx: 'Bajar GPX',
      guardados: 'Guardados', abrirlo: 'Abrir', quitar: 'Quitar',
      nombre: 'Trazado', aprox: 'aprox.', cargando: 'Preparando la red de caminos…',
      fallo: 'No se ha podido preparar la red. Prueba a recargar.',
      aviso: 'Esto lo dibujas tu: va por caminos que salen en las rutas, pero no es ninguna de ellas.'
    },
    eu: {
      abrir: 'Marrazki bat egin', cerrar: 'Marrazkia itxi',
      titulo: 'Zure marrazkia', arranque: 'Ukitu mapa bide baten gainean hasteko.',
      sigue: 'Ukitu beste puntu bat eta bidea bakarrik kalkulatzen da, ibilbideetako bidexketatik.',
      lejos: 'Hor ez da ibilbiderik pasatzen. Ukitu marraztutako bide batetik gertuago.',
      sinpaso: 'Ez dago biderik hormaino sarearen barruan.',
      deshacer: 'Desegin', borrar: 'Ezabatu', guardar: 'Gorde', gpx: 'GPXa jaitsi',
      guardados: 'Gordeta', abrirlo: 'Ireki', quitar: 'Kendu',
      nombre: 'Marrazkia', aprox: 'gutxi gorabehera', cargando: 'Bideen sarea prestatzen…',
      fallo: 'Ezin izan da sarea prestatu. Saiatu orria berriro kargatzen.',
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
    tracks.forEach(function(t){
      var pts = t.points || [];
      var alt = (alturas && t.href) ? alturas[String(t.href).split('/').pop().replace('.html', '')] : null;
      var prev = -1;
      for (var i = 0; i < pts.length; i++) {
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
    var L = d.L, map = d.map, caja = d.caja;
    var t = T[document.documentElement.lang === 'eu' ? 'eu' : 'es'];

    var red = null, cargando = false;
    var anclas = [];     // nodos que ha tocado el visitante
    var tramos = [];     // un array de nodos por cada tramo calculado
    var linea = null, puntitos = [], activo = false;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'map-draw-btn';
    btn.setAttribute('aria-label', t.abrir);
    btn.title = t.abrir;
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"' +
      ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>' +
      '<path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>';
    caja.parentElement.appendChild(btn);

    var panel = document.createElement('div');
    panel.className = 'draw-panel';
    panel.hidden = true;
    panel.innerHTML =
      '<div class="draw-head"><b>' + t.titulo + '</b>' +
      '<button type="button" class="draw-close" aria-label="' + t.cerrar + '">&times;</button></div>' +
      '<p class="draw-msg"></p>' +
      '<p class="draw-tot" hidden><span class="draw-km"></span><span class="draw-des"></span></p>' +
      '<div class="draw-acts">' +
      '<button type="button" class="draw-b" data-a="undo">' + t.deshacer + '</button>' +
      '<button type="button" class="draw-b" data-a="clear">' + t.borrar + '</button>' +
      '<button type="button" class="draw-b" data-a="save">' + t.guardar + '</button>' +
      '<button type="button" class="draw-b" data-a="gpx">' + t.gpx + '</button>' +
      '</div>' +
      '<div class="draw-saved"></div>' +
      '<p class="draw-nota">' + t.aviso + '</p>';
    caja.parentElement.appendChild(panel);

    var elMsg = panel.querySelector('.draw-msg');
    var elTot = panel.querySelector('.draw-tot');
    var elKm = panel.querySelector('.draw-km');
    var elDes = panel.querySelector('.draw-des');
    var elSaved = panel.querySelector('.draw-saved');

    function recorrido(){
      var out = [];
      tramos.forEach(function(tr, i){
        for (var k = (i ? 1 : 0); k < tr.length; k++) out.push(red.nodos[tr[k]]);
      });
      return out;
    }

    function totales(){
      var pts = recorrido(), km = 0, sub = 0, base = null;
      for (var i = 1; i < pts.length; i++) km += metros(pts[i - 1], pts[i]);
      pts.forEach(function(p){
        if (typeof p[2] !== 'number') return;
        if (base === null) { base = p[2]; return; }
        if (p[2] > base + UMBRAL_SUBIDA_M) { sub += p[2] - base; base = p[2]; }
        else if (p[2] < base) base = p[2];
      });
      return { km: km / 1000, subida: Math.round(sub), conAltura: base !== null };
    }

    function pinta(){
      var pts = recorrido();
      if (linea) { map.removeLayer(linea); linea = null; }
      puntitos.forEach(function(m){ map.removeLayer(m); });
      puntitos = [];
      if (pts.length > 1) {
        linea = L.polyline(pts.map(function(p){ return [p[0], p[1]]; }), {
          color: COLOR, weight: 5, opacity: 1, dashArray: '1 9', lineCap: 'round',
          className: 'draw-line'
        }).addTo(map);
      }
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
      elDes.textContent = tt.conAltura && tt.subida ? ' · +' + tt.subida + ' m ' + t.aprox : '';
      elMsg.textContent = anclas.length ? t.sigue : t.arranque;
    }

    function alTocar(e){
      if (!activo || !red) return;
      var n = nodoCerca(red, e.latlng.lat, e.latlng.lng);
      if (n < 0) { elMsg.textContent = t.lejos; return; }
      if (!anclas.length) { anclas.push(n); tramos.push([n]); pinta(); return; }
      var tr = camino(red, anclas[anclas.length - 1], n);
      if (!tr) { elMsg.textContent = t.sinpaso; return; }
      anclas.push(n); tramos.push(tr); pinta();
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
      if (!v.length) { elSaved.innerHTML = ''; return; }
      var html = '<p class="draw-saved-t">' + t.guardados + '</p><ul>';
      v.forEach(function(g, i){
        html += '<li><button type="button" class="draw-open" data-i="' + i + '">' +
          g.nombre + ' <span>' + g.km + ' km</span></button>' +
          '<button type="button" class="draw-del" data-i="' + i + '" aria-label="' + t.quitar + '">&times;</button></li>';
      });
      elSaved.innerHTML = html + '</ul>';
    }

    panel.addEventListener('click', function(e){
      var b = e.target.closest('button');
      if (!b) return;
      if (b.classList.contains('draw-close')) { apaga(); return; }
      if (b.classList.contains('draw-open')) {
        var g = leeGuardados()[+b.dataset.i];
        if (!g) return;
        anclas = []; tramos = [];
        if (linea) map.removeLayer(linea);
        puntitos.forEach(function(m){ map.removeLayer(m); }); puntitos = [];
        linea = L.polyline(g.coords.map(function(p){ return [p[0], p[1]]; }), {
          color: COLOR, weight: 5, opacity: 1, dashArray: '1 9', lineCap: 'round',
          className: 'draw-line'
        }).addTo(map);
        map.fitBounds(linea.getBounds(), { padding: [30, 30] });
        elTot.hidden = false;
        elKm.textContent = g.km + ' km';
        elDes.textContent = g.subida ? ' · +' + g.subida + ' m ' + t.aprox : '';
        elMsg.textContent = g.nombre;
        return;
      }
      if (b.classList.contains('draw-del')) {
        var v = leeGuardados(); v.splice(+b.dataset.i, 1); escribeGuardados(v); pintaGuardados(); return;
      }
      var a = b.dataset.a;
      if (a === 'undo') { anclas.pop(); tramos.pop(); pinta(); }
      else if (a === 'clear') { anclas = []; tramos = []; pinta(); }
      else if (a === 'gpx') { gpx(); }
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
      }
    });

    function apaga(){
      activo = false;
      panel.hidden = true;
      btn.classList.remove('is-active');
      btn.setAttribute('aria-label', t.abrir);
      caja.classList.remove('is-drawing');
      map.off('click', alTocar);
    }

    function enciende(){
      activo = true;
      panel.hidden = false;
      btn.classList.add('is-active');
      btn.setAttribute('aria-label', t.cerrar);
      caja.classList.add('is-drawing');
      if (d.cerrarPanel) { try { d.cerrarPanel(); } catch (e) {} }
      // En un movil el mapa de la portada mide 308x308 y el panel se come
      // dos tercios: ahi no se puede dibujar. Al entrar en modo dibujo se
      // amplia solo (592 px de alto, el panel baja al 26%). No se vuelve a
      // encoger al salir: eso ya lo decide quien mira.
      if (window.innerWidth < 768) {
        var ampliar = caja.parentElement.querySelector('.map-expand-btn');
        if (ampliar && !caja.parentElement.classList.contains('is-expanded')) ampliar.click();
      }
      map.on('click', alTocar);
      pintaGuardados();
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
