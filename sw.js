/* Service worker de trabakutik.com.

   Esta web se abre en el monte, que es justo donde no hay cobertura. Con esto,
   una ficha que ya se haya visitado se abre sin datos: su texto, su perfil de
   altitud, sus fotos y su GPX.

   Lo que NO se guarda son los tiles del mapa. Vienen de OpenStreetMap,
   CyclOSM y el IGN: los dos primeros son servidores de voluntarios y su
   politica de uso prohibe expresamente cachearlos en bloque. Sin cobertura se vera el
   track sobre un fondo vacio, no el mapa.

   Para desactivarlo del todo si algun dia diera problemas: publicar un sw.js
   cuyo contenido sea solo  self.registration.unregister()  -- los navegadores
   que ya lo tengan instalado lo recogeran y se desengancharan solos.

   build.py sustituye VERSION y CONCHA al escribirlo. */
const VERSION = "5d6cf476";
const CONCHA = [
  "base.css?v=95f38cb0",
  "fonts.css?v=1204aafe",
  "home.css?v=83202595",
  "js/agua.js?v=05cd944f",
  "js/app.js?v=38a4f38f",
  "js/filters.js?v=16e104fd",
  "js/info-panel.js?v=2d06fbbb",
  "js/map.js?v=bda69fec",
  "js/trazado.js?v=f04d6e7b",
  "js/weather.js?v=249afb08",
  "js/webmcp.js?v=ed4e6132",
  "route.css?v=969d5add",
  "fonts/fraunces-italic.woff2",
  "fonts/fraunces-normal.woff2",
  "fonts/ibmplexmono-500.woff2",
  "fonts/ibmplexmono-600.woff2",
  "fonts/karla.woff2",
  "fonts/sourceserif-italic.woff2",
  "fonts/sourceserif.woff2",
  "offline.html",
  "favicon.svg",
  "icon-192.png",
  "vendor/leaflet/leaflet.css",
  "vendor/leaflet/leaflet.js"
];

const CACHE_CONCHA = 'concha-' + VERSION;
const CACHE_PAGINAS = 'paginas-v1';
const CACHE_MEDIOS = 'medios-v1';
const MAX_MEDIOS = 150;          // ~150 imagenes cacheadas; las mas viejas se van
const FUERA = 'offline.html';

const MEDIO = /\.(webp|jpg|jpeg|png|svg|woff2)$/i;

self.addEventListener('install', function (evento) {
  evento.waitUntil(
    caches.open(CACHE_CONCHA)
      .then(function (c) { return c.addAll(CONCHA); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (evento) {
  evento.waitUntil(
    caches.keys().then(function (nombres) {
      return Promise.all(nombres.map(function (n) {
        // La concha lleva la version dentro del nombre: al cambiar cualquier
        // css o js, la anterior entera se tira. Las paginas y los medios
        // sobreviven, que es lo que hace util seguir teniendolos sin cobertura.
        if (n === CACHE_PAGINAS || n === CACHE_MEDIOS || n === CACHE_CONCHA) return null;
        return caches.delete(n);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

function recortar(cache, maximo) {
  return cache.keys().then(function (claves) {
    if (claves.length <= maximo) return null;
    return Promise.all(claves.slice(0, claves.length - maximo)
      .map(function (k) { return cache.delete(k); }));
  });
}

function guardar(nombreCache, peticion, respuesta, maximo) {
  // Solo respuestas completas y propias: una opaca (type 'opaque') ocuparia
  // sitio sin que se pueda saber siquiera si trae un error.
  if (!respuesta || !respuesta.ok || respuesta.type === 'opaque') return respuesta;
  const copia = respuesta.clone();
  caches.open(nombreCache).then(function (c) {
    return c.put(peticion, copia).then(function () {
      return maximo ? recortar(c, maximo) : null;
    });
  });
  return respuesta;
}

function refresca(peticion) {
  // Vuelve a pedir una foto por detras y deja la copia al dia si ha cambiado.
  // Va con el fetch normal, no con aLaRed(): asi la peticion pasa por la cache
  // del propio navegador, que con el max-age=600 de GitHub Pages hace que lo
  // normal sea no tocar la red siquiera, y cuando la toca sea un 304 de nada.
  // Si no hay cobertura falla en silencio: la copia guardada ya se ha servido.
  return fetch(peticion)
    .then(function (r) { return guardar(CACHE_MEDIOS, peticion, r, MAX_MEDIOS); })
    .catch(function () { return null; });
}

function aLaRed(peticion) {
  // «Primero la red» no basta: GitHub Pages manda cache-control: max-age=600
  // en el HTML, asi que el fetch del service worker se lo puede servir la
  // cache del propio navegador sin preguntar al servidor, y durante diez
  // minutos se sigue viendo la pagina vieja -- que ademas pide el css viejo
  // por el ?v= y deja la web entera con el aspecto anterior. Con no-cache se
  // revalida: si no ha cambiado, el servidor contesta 304 y no se baja nada.
  //
  // Se construye una peticion nueva desde la URL en vez de pasarle opciones a
  // la que llega: una peticion de navegacion no se puede clonar con cambios.
  return fetch(new Request(peticion.url, {
    cache: 'no-cache', credentials: 'same-origin', redirect: 'follow'
  }));
}

self.addEventListener('fetch', function (evento) {
  const peticion = evento.request;
  if (peticion.method !== 'GET') return;
  const url = new URL(peticion.url);
  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
  // Solo lo que sirve este mismo sitio. Lo unico de fuera son los tiles del
  // mapa, y esos van a la red sin pasar por aqui: son de OpenStreetMap,
  // CyclOSM y el IGN; los dos primeros, servidores de voluntarios cuya
  // politica de uso prohibe cachearlos en bloque. Leaflet ya no viene de un CDN, se sirve
  // desde vendor/leaflet, asi que entra por la via normal.
  if (url.origin !== self.location.origin) return;

  // Paginas: primero la red, para que quien tenga cobertura vea siempre la
  // ultima version; la copia guardada es solo el plan B.
  //
  // Y no solo al navegar: app.js se descarga la portada con fetch() para sacar
  // de ahi los nombres de las rutas vecinas. Si eso se sirviera de la cache,
  // quien ya hubiera visitado la web construiria esa lista con una portada
  // vieja, sin las rutas nuevas. Cualquier HTML va a la red primero.
  const esPagina = peticion.mode === 'navigate'
    || url.pathname === '/' || url.pathname.endsWith('/')
    || /\.html$/.test(url.pathname);
  if (esPagina) {
    evento.respondWith(
      aLaRed(peticion)
        .then(function (r) { return guardar(CACHE_PAGINAS, peticion, r); })
        .catch(function () {
          return caches.match(peticion).then(function (r) {
            return r || caches.match(FUERA) || Response.error();
          });
        })
    );
    return;
  }

  // Los datos de una ruta: primero la red. El track, el perfil y el GPX pueden
  // corregirse sin que cambie ni un css ni un js, y entonces la concha
  // conserva su nombre y no se tira: quien ya hubiera abierto la ficha seguia
  // viendo el track viejo para siempre. Paso justo con el trazado que se
  // aparto del domicilio del autor -- se corrigio tres veces en el servidor y
  // en el movil se seguia dibujando el de antes. Sin cobertura se sirve la
  // copia, que es lo que hace util tener esto.
  if (/^\/(data\/.*\.json|src\/.*\.(gpx|kml|zip))$/.test(url.pathname)) {
    evento.respondWith(
      aLaRed(peticion)
        .then(function (r) { return guardar(CACHE_CONCHA, peticion, r); })
        .catch(function () {
          return caches.match(peticion).then(function (r) { return r || Response.error(); });
        })
    );
    return;
  }

  // Las FOTOS: se sirve la copia guardada -- al instante y sin cobertura, que
  // es para lo que esta -- y ademas se vuelve a pedir por detras. Hace falta
  // porque una foto cambiada se publica CON EL MISMO NOMBRE: los css y js
  // llevan ?v=<hash> y al cambiar cambia su URL, pero img/loquesea.webp no.
  // Con «primero lo guardado» a secas, quien ya tuviera la foto se quedaba con
  // la vieja para siempre. Paso con la del amanecer de garaiurdaixa: el
  // servidor ya daba la nueva y en el movil seguia saliendo la anterior.
  // Refrescando por detras, la siguiente visita ya la ve bien.
  const esMedio = MEDIO.test(url.pathname);
  if (esMedio) {
    // La peticion de fondo se lanza aqui, antes de nada, para poder pasarsela
    // a waitUntil mientras el evento sigue vivo: hacerlo dentro de un .then
    // posterior es tarde y algunos navegadores lo rechazan.
    const red = refresca(peticion);
    evento.waitUntil(red);
    evento.respondWith(
      caches.match(peticion).then(function (guardado) {
        return guardado || red.then(function (r) { return r || fetch(peticion); });
      })
    );
    return;
  }

  // Lo demas: primero lo guardado. Los css y js llevan ?v=<hash> en la URL, de
  // modo que al cambiar el fichero cambia la URL y no hay copia vieja posible.
  evento.respondWith(
    caches.match(peticion).then(function (guardado) {
      if (guardado) return guardado;
      return fetch(peticion).then(function (r) {
        return guardar(CACHE_CONCHA, peticion, r, 0);
      });
    })
  );
});
