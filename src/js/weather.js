/* El tiempo de los proximos dias en la salida de la ruta.
 *
 * Es lo primero que se mira antes de salir al monte, y hasta ahora habia que
 * buscarlo fuera. El bloque va vacio y oculto en el HTML: si no hay cobertura,
 * si la peticion falla o si la respuesta no trae lo que se espera, se queda
 * oculto y la ficha se ve igual que antes. Un extra no puede romper la pagina.
 *
 * Los datos son de Open-Meteo: gratis, sin clave, sin cuenta y con permiso
 * para usarlo desde el navegador (CORS abierto). Es el unico servicio de
 * fuera al que esta web le pide algo aparte de las teselas del mapa, y por
 * eso esta dicho en el aviso legal y en el pie del propio bloque. El servicio
 * ve la IP de quien entra, como ya la ven el IGN y OpenStreetMap al pintar el
 * mapa; no se le manda nada mas que las coordenadas de la salida, que son las
 * mismas para todo el mundo.
 *
 * La respuesta se guarda una hora en sessionStorage, con las coordenadas
 * redondeadas a 1 km: casi todas las rutas salen de Trabakua, asi que quien
 * mire cuatro fichas seguidas hace una sola peticion, no cuatro.
 */
(function () {
  'use strict';

  var caja = document.getElementById('weather');
  if (!caja || !caja.dataset.lat || !window.fetch) return;

  var VIDA = 60 * 60 * 1000;   // una hora: el pronostico diario no cambia mas
  var DIAS = 4;

  var textos;
  try { textos = JSON.parse(caja.dataset.textos || '{}'); } catch (e) { return; }
  if (!textos.dias) return;

  // Los codigos de la Organizacion Meteorologica Mundial, agrupados en los
  // diez estados que de verdad se distinguen de un vistazo. Los que no esten
  // aqui (y los hay, como el granizo fino) caen en «nuboso», que es lo menos
  // comprometido que se puede decir.
  var CIELO = {
    0: 'despejado', 1: 'poco-nuboso', 2: 'poco-nuboso', 3: 'cubierto',
    45: 'niebla', 48: 'niebla',
    51: 'llovizna', 53: 'llovizna', 55: 'llovizna', 56: 'llovizna', 57: 'llovizna',
    61: 'lluvia', 63: 'lluvia', 65: 'lluvia', 66: 'lluvia', 67: 'lluvia',
    71: 'nieve', 73: 'nieve', 75: 'nieve', 77: 'nieve', 85: 'nieve', 86: 'nieve',
    80: 'chubascos', 81: 'chubascos', 82: 'chubascos',
    95: 'tormenta', 96: 'tormenta', 99: 'tormenta'
  };

  var SOL = '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M4.3 4.3l1.6 1.6M18.1 18.1l1.6 1.6M2.6 12h2.2M19.2 12h2.2M4.3 19.7l1.6-1.6M18.1 5.9l1.6-1.6"/>';
  var NUBE = '<path d="M7 19h10.5a3.5 3.5 0 0 0 .4-7 5.5 5.5 0 0 0-10.6-1.2A4 4 0 0 0 7 19z"/>';
  var SOL_NUBE = '<circle cx="8.5" cy="8" r="3"/><path d="M8.5 2.2v1.6M3.6 8H2M4.2 3.7l1.1 1.1M13.4 8H15M12.8 3.7l-1.1 1.1"/>' +
                 '<path d="M9 20h8.5a3.3 3.3 0 0 0 .3-6.6A5 5 0 0 0 8.5 12 3.9 3.9 0 0 0 9 20z"/>';
  var GOTAS = '<path d="M9 20.5l-1 2.2M13 20.5l-1 2.2M17 20.5l-1 2.2"/>';
  var ICONOS = {
    'despejado': SOL,
    'poco-nuboso': SOL_NUBE,
    'nuboso': NUBE,
    'cubierto': NUBE,
    'niebla': '<path d="M4 9h16M3 13h18M5 17h14M7 21h10"/>',
    'llovizna': NUBE + '<path d="M9.5 20.5l-.7 1.6M14.5 20.5l-.7 1.6"/>',
    'lluvia': NUBE + GOTAS,
    'chubascos': SOL_NUBE + GOTAS,
    'nieve': NUBE + '<path d="M9 21h.01M13 21h.01M17 21h.01M11 23h.01M15 23h.01"/>',
    'tormenta': NUBE + '<path d="M13 19.5l-2.5 3.5h3l-2 3"/>'
  };

  var lat = Number(caja.dataset.lat);
  var lon = Number(caja.dataset.lon);
  if (!isFinite(lat) || !isFinite(lon)) return;

  var clave = 'tiempo:' + lat.toFixed(2) + ',' + lon.toFixed(2);

  function guardado() {
    try {
      var crudo = sessionStorage.getItem(clave);
      if (!crudo) return null;
      var d = JSON.parse(crudo);
      return (Date.now() - d.cuando < VIDA) ? d.datos : null;
    } catch (e) { return null; }
  }

  function guarda(datos) {
    try {
      sessionStorage.setItem(clave, JSON.stringify({ cuando: Date.now(), datos: datos }));
    } catch (e) { /* modo privado, cuota llena: da igual, se vuelve a pedir */ }
  }

  function nombreDia(iso, i) {
    if (i === 0) return textos.hoy;
    if (i === 1) return textos.maniana;
    // Al mediodia, no a medianoche: asi ningun huso horario corre el dia.
    var d = new Date(iso + 'T12:00:00');
    return isNaN(d) ? '' : textos.dias[d.getDay()];
  }

  function grados(n) {
    return Math.round(n) + '°';
  }

  function pinta(datos) {
    var dia = datos.daily;
    if (!dia || !dia.time || !dia.time.length) return;
    var n = Math.min(DIAS, dia.time.length);
    var filas = document.getElementById('weatherDays');
    if (!filas) return;

    for (var i = 0; i < n; i++) {
      var estado = CIELO[dia.weather_code[i]] || 'nuboso';
      var col = document.createElement('div');
      col.className = 'weather-day';

      var cuando = document.createElement('p');
      cuando.className = 'weather-when';
      cuando.textContent = nombreDia(dia.time[i], i);
      col.appendChild(cuando);

      var icono = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      icono.setAttribute('viewBox', '0 0 24 26');
      icono.setAttribute('class', 'weather-icon is-' + estado);
      icono.setAttribute('aria-hidden', 'true');
      icono.innerHTML = ICONOS[estado] || NUBE;
      col.appendChild(icono);

      var cielo = document.createElement('p');
      cielo.className = 'weather-sky';
      cielo.textContent = (textos.cielo && textos.cielo[estado]) || '';
      col.appendChild(cielo);

      var temp = document.createElement('p');
      temp.className = 'weather-temp';
      var alta = document.createElement('b');
      alta.textContent = grados(dia.temperature_2m_max[i]);
      temp.appendChild(alta);
      temp.appendChild(document.createTextNode(' ' + grados(dia.temperature_2m_min[i])));
      col.appendChild(temp);

      var p = dia.precipitation_probability_max ? dia.precipitation_probability_max[i] : null;
      var agua = document.createElement('p');
      agua.className = 'weather-rain';
      // Por debajo del 20% no se escribe nada: un 10% es ruido y ensucia las
      // cuatro columnas. La linea se queda vacia para no desalinearlas.
      agua.textContent = (p >= 20) ? p + '% ' + textos.lluvia : ' ';
      col.appendChild(agua);

      filas.appendChild(col);
    }
    caja.hidden = false;
  }


  /* ------------------------------------------------------------------ */
  /* El texto oficial de Euskalmet, debajo de los numeros.
   *
   * Lo pidio el autor despues de decir que el pronostico «no da una».
   * Euskalmet es la agencia que pronostica este valle, y publica un fichero
   * abierto que **no pide clave** y que deja llamarlo desde el navegador
   * (Access-Control-Allow-Origin: *), comprobado. Trae el texto de hoy y de
   * manana escrito en castellano y en euskera, que es justo lo que hace
   * falta en una web en dos lenguas.
   *
   * No sustituye a Open-Meteo: solo da dos dias, sin probabilidad de lluvia,
   * y sus temperaturas son de seis ciudades, ninguna de por aqui. Por eso se
   * suma debajo en vez de reemplazar la tira de cuatro dias.
   *
   * El fichero viene en ISO-8859-1, asi que hay que decodificarlo a mano:
   * con response.text() el navegador lo lee como UTF-8 y los acentos salen
   * rotos. Y, como todo lo de este bloque, si algo falla no se enseña nada.
   */
  var EUSKALMET = 'https://opendata.euskadi.eus/contenidos/prevision_tiempo/' +
                  'met_forecast/opendata/met_forecast.xml';

  function pintaLocal(xml) {
    var caja2 = document.getElementById('weatherLocal');
    if (!caja2 || !xml) return;
    var lengua = document.documentElement.lang === 'eu' ? 'eu' : 'es';
    // Solo el de hoy. Entraban hoy y manana y eran dos parrafos largos
    // debajo de cada ficha; el autor dijo «recorta». El de manana sigue
    // llegando en el mismo fichero, asi que volver a ponerlo es cambiar
    // este 1 por un 2.
    var DIAS_LOCAL = 1;
    var dias = xml.getElementsByTagName('forecast');
    var puestos = 0;
    for (var i = 0; i < dias.length && puestos < DIAS_LOCAL; i++) {
      var cual = dias[i].getAttribute('forecastDay');
      var d = dias[i].getElementsByTagName('description')[0];
      var e = d && d.getElementsByTagName(lengua)[0];
      var txt = e && e.textContent ? e.textContent.trim() : '';
      if (!txt) continue;
      var p = document.createElement('p');
      p.className = 'weather-local-day';
      var cuando = document.createElement('b');
      cuando.textContent = (cual === 'tomorrow' ? textos.maniana : textos.hoy) + ': ';
      p.appendChild(cuando);
      p.appendChild(document.createTextNode(txt));
      caja2.appendChild(p);
      puestos++;
    }
    if (!puestos) return;
    var pie = document.createElement('p');
    pie.className = 'weather-local-credit';
    pie.textContent = textos.oficial;
    caja2.appendChild(pie);
    caja.hidden = false;
  }

  function pideLocal() {
    var clave = 'euskalmet';
    try {
      var hay = JSON.parse(sessionStorage.getItem(clave) || 'null');
      if (hay && Date.now() - hay.t < VIDA && hay.x) {
        pintaLocal(new DOMParser().parseFromString(hay.x, 'application/xml'));
        return;
      }
    } catch (e) { /* sin sessionStorage: se pide y ya */ }
    fetch(EUSKALMET, { mode: 'cors' })
      .then(function (r) { return r.ok ? r.arrayBuffer() : Promise.reject(r.status); })
      .then(function (buf) {
        // ISO-8859-1: con .text() los acentos saldrian rotos
        var txt = new TextDecoder('iso-8859-1').decode(buf);
        var xml = new DOMParser().parseFromString(txt, 'application/xml');
        if (xml.getElementsByTagName('parsererror').length) return;
        try { sessionStorage.setItem(clave, JSON.stringify({ t: Date.now(), x: txt })); }
        catch (e) { /* cuota llena: da igual, es solo cache */ }
        pintaLocal(xml);
      })
      .catch(function () { /* sin cobertura o servicio caido: no se enseña nada */ });
  }

  function pide() {
    var url = 'https://api.open-meteo.com/v1/forecast'
      + '?latitude=' + lat.toFixed(4) + '&longitude=' + lon.toFixed(4)
      + '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max'
      + '&timezone=Europe%2FMadrid&forecast_days=' + DIAS;
    fetch(url, { mode: 'cors' })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (datos) { guarda(datos); pinta(datos); })
      .catch(function () { /* sin cobertura o servicio caido: no se enseña nada */ });
  }

  var ya = guardado();
  if (ya) { pinta(ya); pideLocal(); return; }

  // Despues de lo que de verdad importa de la pagina: el texto, las fotos y
  // el mapa van primero.
  function pideTodo() { pide(); pideLocal(); }
  if ('requestIdleCallback' in window) {
    requestIdleCallback(pideTodo, { timeout: 3000 });
  } else {
    setTimeout(pideTodo, 600);
  }
})();
