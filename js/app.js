// Shared behaviour for every page (both languages).
// Built from src/js/app.js by src/build.py -- edit there, not in app.js.

// Las "rutas por esta zona" las calcula ahora src/build.py y vienen escritas
// en la pagina. Aqui se hacian en el navegador, y para eso cada ficha se
// bajaba data/trailhead.json (399 kB) y la portada entera (355 kB): 754 kB por
// visita para una lista que no cambia entre una visita y otra. Ademas ahora la
// ven Google y quien tenga el JavaScript parado.

// --- close button inside an open <details> notice (e.g. "GPS obligatorio") ---
(function(){
  var buttons = document.querySelectorAll('.notice-close');
  for (var i = 0; i < buttons.length; i++){
    buttons[i].addEventListener('click', function(){
      var details = this.closest('details');
      if (!details) return;
      details.open = false;
      var summary = details.querySelector('summary');
      if (summary) summary.scrollIntoView({ block: 'nearest' });
    });
  }
})();

// --- photo lightbox ---
(function(){
  var box = document.getElementById('lightbox');
  var boxImg = document.getElementById('lightboxImg');
  var close = document.getElementById('lightboxClose');
  if (!box || !boxImg || !close) return; // page has no photo gallery
  var lastTrigger = null;
  function open(src, trigger){
    // data-lightbox-src es el .webp de tamano completo, que es lo que ve
    // casi todo el mundo. El respaldo es el -800.jpg, lo unico que puede
    // abrir un navegador sin WebP: el original de 1600 ya no se publica
    // (vive en img/orig/, ver _config.yml).
    boxImg.onerror = function(){
      boxImg.onerror = null;
      boxImg.src = src.replace(/\.webp$/i, '-800.jpg');
    };
    boxImg.src = src;
    var triggerImg = trigger.querySelector('img');
    if (triggerImg && triggerImg.alt) boxImg.alt = triggerImg.alt;
    lastTrigger = trigger;
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    close.focus();
  }
  function shut(){
    box.classList.remove('open');
    boxImg.src='';
    document.body.style.overflow = '';
    if(lastTrigger) lastTrigger.focus();
  }
  document.querySelectorAll('[data-lightbox-src]').forEach(function(el){
    el.addEventListener('click', function(){ open(el.dataset.lightboxSrc, el); });
  });
  close.addEventListener('click', shut);
  box.addEventListener('click', function(e){ if(e.target === box) shut(); });
  document.addEventListener('keydown', function(e){
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') { shut(); return; }
    if (e.key === 'Tab') { e.preventDefault(); close.focus(); }
  });
})();

// --- back-to-top button ---
(function(){
  var btn = document.getElementById('toTop');
  if (!btn) return;
  function reduceMotion(){
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function onScroll(){
    if (window.scrollY > window.innerHeight * 0.6) btn.classList.add('visible');
    else btn.classList.remove('visible');
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
  btn.addEventListener('click', function(){
    var root = document.documentElement;
    var masthead = document.querySelector('.masthead');
    root.classList.add('scrolling-to-top');
    if (masthead) masthead.classList.remove('is-compact');
    window.scrollTo({ top:0, behavior: reduceMotion() ? 'auto' : 'smooth' });
    var stop = function(){ root.classList.remove('scrolling-to-top'); };
    window.addEventListener('scrollend', stop, { once:true });
    setTimeout(stop, 1000);
  });
})();

// --- compact masthead on scroll (home page only) ---
(function(){
  var masthead = document.querySelector('.masthead');
  var brand = masthead && masthead.querySelector('.brand');
  if (!masthead || !brand) return;
  function onScroll(){
    if (document.documentElement.classList.contains('scrolling-to-top')) return;
    if (window.scrollY > 60) masthead.classList.add('is-compact');
    else if (window.scrollY < 20) masthead.classList.remove('is-compact');
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
})();

// --- fade the floating map/list button while the card list scrolls under it ---
// It's position:fixed, so anything scrolling past that screen position (card
// stats, tags) gets covered while it's fully opaque. Fading it out during the
// scroll gesture itself -- when nobody is trying to read a card anyway -- and
// back in ~150ms after scrolling stops fixes the overlap without touching the
// button's position or the card layout.
(function(){
  var fab = document.getElementById('viewFab');
  if (!fab) return;
  var timer = null;
  function onScroll(){
    fab.classList.add('is-scrolling');
    clearTimeout(timer);
    timer = setTimeout(function(){ fab.classList.remove('is-scrolling'); }, 150);
  }
  window.addEventListener('scroll', onScroll, { passive:true });
})();

// --- el aviso «Léelo antes de salir», en la insignia de la esquina ---
// La barra de ancho completo se cambia por una insignia que late. Todo se
// hace aqui y no en el HTML a proposito: si esto no llega a ejecutarse, la
// pagina se queda con la barra de siempre, que es un <details> nativo y
// funciona sin JavaScript.
//
// Late siempre. Se probo a que dejara de latir una vez abierto el aviso
// (guardado en localStorage) y el efecto era que, tras mirarlo una vez, ya
// no volvia a parpadear nunca: el autor lo quiere latiendo. Lo unico que lo
// para es que la persona haya pedido que no se mueva nada en pantalla
// (prefers-reduced-motion), que eso no es decoracion.
(function(){
  var seccion = document.getElementById('beforeYouGo');
  var insignia = document.getElementById('noticeBadge');
  if (!seccion || !insignia) return;
  var detalle = seccion.querySelector('details');
  var boton = insignia.querySelector('.aviso-boton');
  if (!detalle || !boton) return;

  seccion.classList.add('solo-insignia');
  insignia.hidden = false;

  // Va en la barra de arriba, entre «Mallabia · Bizkaia» y el idioma: en la
  // esquina de abajo pasaba por encima del texto de las tarjetas. El autor
  // la quiso ahi.
  var cabecera = document.querySelector('.masthead');
  var derecha = cabecera && cabecera.querySelector('.masthead-right');
  if (derecha) cabecera.insertBefore(insignia, derecha);

  // Si ya se ha leido el aviso en esta visita, la insignia sale directamente
  // apagada. Va en sessionStorage y no en localStorage a proposito: dura lo
  // que dure la pestaña abierta, asi que volver a la portada desde una ficha
  // no vuelve a encender las ondas, pero al entrar otro dia late otra vez.
  //
  // Recargar la pagina a mano la devuelve al principio. Es lo que pide quien
  // le da a recargar: volver a empezar. Se distingue de «he vuelto de una
  // ficha» por el tipo de navegacion que declara el propio navegador --
  // 'reload' solo cuando se ha recargado de verdad.
  try {
    var nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
    if (nav && nav.type === 'reload') sessionStorage.removeItem('rutas-mallabia-aviso');
  } catch(err){}
  try { if (sessionStorage.getItem('rutas-mallabia-aviso')) insignia.classList.add('ya-visto'); } catch(err){}

  detalle.addEventListener('toggle', function(){
    boton.setAttribute('aria-expanded', detalle.open ? 'true' : 'false');
  });

  boton.addEventListener('click', function(){
    var abrir = !detalle.open;
    detalle.open = abrir;
    // A partir de aqui las ondas bajan de intensidad: ya ha mirado el aviso.
    insignia.classList.add('ya-visto');
    try { sessionStorage.setItem('rutas-mallabia-aviso', '1'); } catch(err){}
    if (!abrir) return;
    var quieto = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    detalle.scrollIntoView({ block:'start', behavior: quieto ? 'auto' : 'smooth' });
  });
})();

// --- light/dark theme toggle ---
(function(){
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  var root = document.documentElement;
  try {
    if (!localStorage.getItem('rutas-mallabia-theme')) localStorage.setItem('rutas-mallabia-theme', 'dark');
  } catch(err){}
  function effectiveTheme(){
    return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }
  function updateLabel(){
    var eff = effectiveTheme();
    btn.setAttribute('aria-label', eff === 'dark' ? btn.dataset.labelLight : btn.dataset.labelDark);
  }
  // La barra de arriba del navegador, en el movil, llevaba siempre el color
  // oscuro: con el tema claro la pagina era clara y la barra negra. Se pone
  // el fondo de verdad, leido del CSS, que no es el mismo en la portada que
  // en una ficha.
  function pintarBarra(){
    var meta = document.querySelector('meta[name="theme-color"]');
    if (!meta) return;
    var fondo = getComputedStyle(root).getPropertyValue('--ground').trim();
    if (fondo) meta.setAttribute('content', fondo);
  }
  function applyTheme(theme){
    if (theme === 'light') root.setAttribute('data-theme', 'light');
    else root.removeAttribute('data-theme');
    updateLabel();
    pintarBarra();
  }
  updateLabel();
  pintarBarra();
  btn.addEventListener('click', function(){
    var next = effectiveTheme() === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('rutas-mallabia-theme', next); } catch(err){}
  });
})();

// --- incident report modal (route pages: fallen trees, cut paths, etc.) ---
(function(){
  var FORMSPREE_ENDPOINT = 'https://formspree.io/f/mqpkprpz';
  var trigger = document.getElementById('reportTrigger');
  var box = document.getElementById('reportModal');
  var close = document.getElementById('reportModalClose');
  var form = document.getElementById('reportForm');
  if (!trigger || !box || !close || !form) return;
  var status = document.getElementById('reportStatus');
  var submitBtn = form.querySelector('.report-submit');
  var routeNameEl = document.querySelector('h1');
  var routeField = form.querySelector('input[name="route"]');
  var subjectField = form.querySelector('input[name="_subject"]');
  function open(){
    var routeName = routeNameEl ? (routeNameEl.innerText || routeNameEl.textContent).replace(/\s+/g, ' ').trim() : document.title;
    if (routeField) routeField.value = routeName;
    if (subjectField) subjectField.value = form.dataset.subjectPrefix + ' ' + routeName;
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    close.focus();
  }
  function shut(){
    box.classList.remove('open');
    document.body.style.overflow = '';
    trigger.focus();
  }
  trigger.addEventListener('click', open);
  close.addEventListener('click', shut);
  box.addEventListener('click', function(e){ if(e.target === box) shut(); });
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), ' +
                  'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  function focusables(){
    return Array.prototype.filter.call(box.querySelectorAll(FOCUSABLE), function(el){
      var r = el.getBoundingClientRect();
      return r.width > 0 || r.height > 0;
    });
  }
  document.addEventListener('keydown', function(e){
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') { shut(); return; }
    if (e.key !== 'Tab') return;
    var items = focusables();
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (!box.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    else if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  form.addEventListener('submit', function(e){
    e.preventDefault();
    submitBtn.disabled = true;
    status.textContent = form.dataset.sending;
    status.className = 'report-status';
    fetch(FORMSPREE_ENDPOINT, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function(res){
      if (res.ok) {
        form.reset();
        status.textContent = form.dataset.success;
        status.className = 'report-status success';
      } else {
        status.textContent = form.dataset.error;
        status.className = 'report-status error';
      }
    }).catch(function(){
      status.textContent = form.dataset.error;
      status.className = 'report-status error';
    }).then(function(){
      submitBtn.disabled = false;
    });
  });
})();


/* Service worker: lo que hace que una ficha ya visitada se abra sin cobertura.
   Se registra despues de 'load' para no competir por el ancho de banda con lo
   que la persona ha venido a ver. Si falla, no pasa nada: la web funciona igual,
   solo que necesitando datos. */
(function(){
  if (!('serviceWorker' in navigator)) return;
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  });
})();


/* Mis rutas y Compartir.
   Mis rutas: un corazon en cada tarjeta de la portada y en cada ficha. Lo
   guardado se queda solo en este navegador (localStorage), no viaja a ningun
   sitio. El filtro «Mis rutas» de la portada lo lleva js/filters.js.
   Compartir: en la ficha, abre el menu de compartir del movil si existe; si
   no, WhatsApp con el nombre, los km, el desnivel y el enlace. */
(function(){
  var KEY = 'trabakutik_favs';
  var eu = document.documentElement.lang === 'eu';
  function read(){
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; }
    catch (_) { return []; }
  }
  function slugOf(href){
    return String(href || '').split('/').pop().split('?')[0].split('#')[0]
      .replace(/\.eu\.html$/, '').replace(/\.html$/, '');
  }
  var favs = read();
  function has(slug){ return favs.indexOf(slug) !== -1; }
  function toggle(slug){
    favs = has(slug) ? favs.filter(function(s){ return s !== slug; }) : favs.concat(slug);
    try { localStorage.setItem(KEY, JSON.stringify(favs)); } catch (_) {}
    document.dispatchEvent(new CustomEvent('favs:change', { detail: { favs: favs.slice() } }));
  }
  window.trabakutikFavs = { has: has, toggle: toggle, slugOf: slugOf, list: function(){ return favs.slice(); } };

  var HEART = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>';
  var SHARE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>';
  var W = eu
    ? { save: 'Gorde Nire ibilbideetan', remove: 'Kendu Nire ibilbideetatik', saveShort: 'Gorde', saved: 'Gordeta', share: 'Partekatu', copied: 'Esteka kopiatuta' }
    : { save: 'Guardar en Mis rutas', remove: 'Quitar de Mis rutas', saveShort: 'Guardar', saved: 'Guardada', share: 'Compartir', copied: 'Enlace copiado' };

  function paintHeart(btn, on){
    btn.classList.toggle('is-fav', on);
    btn.setAttribute('aria-pressed', String(on));
    btn.setAttribute('aria-label', on ? W.remove : W.save);
    btn.title = on ? W.remove : W.save;
  }

  // Portada: corazon en la esquina de arriba a la derecha de la foto (la de
  // la izquierda es la pastilla «Nueva», la de abajo la miniatura del mapa).
  document.querySelectorAll('.route-card[href] .route-card-photo').forEach(function(photo){
    var card = photo.closest('.route-card');
    var slug = slugOf(card.getAttribute('href'));
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'fav-heart'; btn.innerHTML = HEART;
    paintHeart(btn, has(slug));
    btn.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      toggle(slug); paintHeart(btn, has(slug));
    });
    photo.appendChild(btn);
  });

  // Ficha: Guardar y Compartir en la misma fila que GPX y KML.
  var row = document.querySelector('.wikiloc-row');
  if (!row) return;
  var slug = slugOf(location.pathname) || 'index';
  var fav = document.createElement('button');
  fav.type = 'button'; fav.className = 'wikiloc-link ghost fav-action';
  function paintFav(){
    var on = has(slug);
    fav.innerHTML = HEART.replace('width="18" height="18"', 'width="15" height="15"') + (on ? W.saved : W.saveShort);
    paintHeart(fav, on);
  }
  paintFav();
  fav.addEventListener('click', function(){ toggle(slug); paintFav(); });

  var share = document.createElement('button');
  share.type = 'button'; share.className = 'wikiloc-link ghost share-action';
  share.innerHTML = SHARE + W.share;
  share.addEventListener('click', function(){
    var h1 = document.querySelector('h1');
    var name = h1 ? (h1.innerText || h1.textContent).replace(/\s+/g, ' ').trim() : document.title;
    var facts = Array.from(document.querySelectorAll('.facts .fact .v')).map(function(v){ return v.textContent.trim(); });
    var km = facts.find(function(t){ return / km$/.test(t); }) || '';
    var up = facts.find(function(t){ return /^\+.* m$/.test(t); }) || '';
    var line = [name, km, up].filter(Boolean).join(' · ') + ' · Trabakutik';
    var url = location.href.split('#')[0];
    if (navigator.share) {
      navigator.share({ title: name, text: line, url: url }).catch(function(){});
      return;
    }
    var w = window.open('https://wa.me/?text=' + encodeURIComponent(line + '\n' + url), '_blank');
    if (w) { try { w.opener = null; } catch (_) {} }
    else if (navigator.clipboard) {
      navigator.clipboard.writeText(line + '\n' + url).then(function(){
        share.lastChild.textContent = W.copied;
        setTimeout(function(){ share.lastChild.textContent = W.share; }, 2000);
      });
    }
  });
  var gpx = row.querySelector('a[href$=".gpx"]');
  var after = row.querySelector('a[href$=".kml"]') || gpx;
  if (after) { after.after(share); after.after(fav); }
  else { row.appendChild(fav); row.appendChild(share); }
})();

/* «Lo mio»: favoritas, vistas hace poco y contacto, en la barra de todas las
   paginas. Las favoritas existian desde hacia tiempo -- el corazon de cada
   tarjeta y el filtro de la portada -- pero no habia ningun sitio donde
   verlas juntas, y desde una ficha no habia forma de llegar a ellas.

   Los nombres de las rutas salen de data/rutas.json, que se pide una sola vez
   al abrir el panel: guardar la tabla entera en las 128 paginas costaba 4 kB
   en cada una para algo que casi nunca se abre. */
(function(){
  var VISTAS = 'trabakutik_vistas';
  var MAX_VISTAS = 6;
  var eu = document.documentElement.lang === 'eu';
  var T = eu
    ? { guardando:'Gordetzen…', hecho:'Mendirako prest', fallo:'Ezin izan dira denak gorde' }
    : { guardando:'Guardando…', hecho:'Listas para el monte', fallo:'No se pudieron guardar todas' };

  function lee(clave){
    try { var v = JSON.parse(localStorage.getItem(clave) || '[]'); return Array.isArray(v) ? v : []; }
    catch (_) { return []; }
  }
  // Apuntar la ficha que se esta viendo. Se hace siempre, aunque el panel no
  // se abra nunca: es lo que lo llena cuando se abre.
  var aqui = location.pathname.split('/').pop().replace(/\.eu\.html$/,'').replace(/\.html$/,'');
  if (aqui && aqui !== 'index' && aqui !== 'agua' && aqui !== 'aviso-legal' && aqui !== '') {
    var vistas = lee(VISTAS).filter(function(s){ return s !== aqui; });
    vistas.unshift(aqui);
    try { localStorage.setItem(VISTAS, JSON.stringify(vistas.slice(0, MAX_VISTAS))); } catch (_) {}
  }

  var abrir = document.getElementById('mioAbrir');
  var panel = document.getElementById('mioDialog');
  if (!abrir || !panel || typeof panel.showModal !== 'function') return;
  abrir.hidden = false;

  var cuenta = document.getElementById('mioCuenta');
  var listaFavs = document.getElementById('mioFavs');
  var vacioFavs = document.getElementById('mioFavsVacio');
  var listaVistas = document.getElementById('mioVistas');
  var vacioVistas = document.getElementById('mioVistasVacio');
  var guardar = document.getElementById('mioGuardar');
  var nota = document.getElementById('mioGuardarNota');
  var cerrar = document.getElementById('mioCerrar');
  var rutas = null;

  function favoritas(){
    return (window.trabakutikFavs ? window.trabakutikFavs.list() : lee('trabakutik_favs'));
  }
  function pintaInsignia(){
    var n = favoritas().length;
    abrir.classList.toggle('tiene', n > 0);
    if (cuenta) { cuenta.textContent = n > 9 ? '9+' : String(n); cuenta.hidden = n === 0; }
  }
  pintaInsignia();
  document.addEventListener('favs:change', pintaInsignia);

  function pinta(lista, vacio, slugs){
    lista.innerHTML = '';
    var hay = 0;
    slugs.forEach(function(slug){
      var r = rutas && rutas[slug];
      if (!r) return;                       // una ruta que ya no existe no se ensena
      hay++;
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = r.h;
      a.innerHTML = '<span class="mio-nombre"></span><span class="mio-datos"></span>';
      a.querySelector('.mio-nombre').textContent = r.n;
      a.querySelector('.mio-datos').textContent = r.s;
      li.appendChild(a); lista.appendChild(li);
    });
    vacio.hidden = hay > 0;
    return hay;
  }

  function rellena(){
    var favs = favoritas();
    var n = pinta(listaFavs, vacioFavs, favs);
    pinta(listaVistas, vacioVistas, lee(VISTAS).filter(function(s){ return s !== aqui; }));
    if (guardar) guardar.hidden = n === 0;
    if (nota) nota.hidden = n === 0;
  }

  function abre(){
    panel.showModal();
    if (rutas) { rellena(); return; }
    fetch('data/rutas.json').then(function(r){ return r.json(); }).then(function(d){
      rutas = (d && d[eu ? 'eu' : 'es']) || {};
      rellena();
    }).catch(function(){ rellena(); });   // sin red se queda con los textos de «aun no hay»
  }
  abrir.addEventListener('click', abre);
  if (cerrar) cerrar.addEventListener('click', function(){ panel.close(); });
  panel.addEventListener('click', function(ev){ if (ev.target === panel) panel.close(); });

  /* Guardar para el monte: pedir cada favorita hace que el service worker la
     guarde, que es lo que luego la abre sin cobertura. No se inventa ninguna
     cache nueva: se usa la que ya hay. */
  if (guardar) guardar.addEventListener('click', function(){
    var favs = favoritas().filter(function(s){ return rutas && rutas[s]; });
    if (!favs.length) return;
    guardar.disabled = true;
    if (nota) { nota.hidden = false; nota.textContent = T.guardando; }
    var fallos = 0;
    Promise.all(favs.map(function(slug){
      return fetch(rutas[slug].h, { cache: 'reload' })
        .then(function(r){ if (!r.ok) fallos++; })
        .catch(function(){ fallos++; });
    })).then(function(){
      guardar.disabled = false;
      if (nota) nota.textContent = fallos ? T.fallo : T.hecho;
    });
  });
})();

/* La barra de filtros del movil se aparta al bajar, y vuelve al subir o en
   cuanto dejas de mover la pagina. Leyendo una lista de 60 tarjetas, 57 px
   fijos abajo se notan; en cuanto paras o haces ademan de volver atras, la
   barra ya esta ahi.

   Vuelve tambien al parar, y no solo al subir, porque el autor conto que en
   su movil desaparecia y no volvia. No se pudo reproducir aqui -- ni con
   rueda, ni con frames perdidos, ni subiendo de tres en tres pixeles -- asi
   que en vez de arreglar a ciegas lo que no se ve, se le quita al problema
   el sitio donde esconderse: si la pagina lleva 600 ms quieta, la barra
   vuelve, pase lo que pase con los eventos de scroll.

   Solo por debajo de 660 px, que es donde la barra esta abajo (en pantalla
   ancha sigue arriba y no estorba), y solo si no se ha pedido menos
   movimiento: ahi aparecer y desaparecer de golpe molesta mas que ayudar. */
(function(){
  var barra = document.querySelector('.finder-toolbar');
  if (!barra || !window.matchMedia) return;
  var movil = window.matchMedia('(max-width:659px)');
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)');
  var DESDE = 320;   // por encima del heroe; arriba del todo nunca se aparta
  var BAJA = 10;     // lo que hay que bajar para que se aparte
  var SUBE = 4;      // y lo que hay que subir para que vuelva
  var PARADA = 600;  // ms quieto tras los que vuelve sola
  var ultimo = window.pageYOffset || 0;
  var marco = 0, reloj = 0;

  function aparta(si){ barra.classList.toggle('se-aparta', si); }

  function mira(){
    marco = 0;
    if (!movil.matches || quieto.matches) { aparta(false); return; }
    var y = window.pageYOffset || 0;
    var fin = y + window.innerHeight >= document.documentElement.scrollHeight - 4;
    if (y <= DESDE || fin) { aparta(false); ultimo = y; return; }
    if (y - ultimo > BAJA) { aparta(true); ultimo = y; }
    else if (ultimo - y > SUBE) { aparta(false); ultimo = y; }
  }

  function alMover(){
    // cancelar y volver a pedir, en vez de una bandera: si el navegador deja
    // de dar frames (pestana al fondo, pantalla apagada), al volver se
    // atiende la ultima peticion en vez de quedarse trabada para siempre.
    if (marco) window.cancelAnimationFrame(marco);
    marco = window.requestAnimationFrame(mira);
    if (reloj) window.clearTimeout(reloj);
    reloj = window.setTimeout(function(){ aparta(false); ultimo = window.pageYOffset || 0; }, PARADA);
  }
  window.addEventListener('scroll', alMover, { passive: true });
  // Al volver a la pagina desde otra app, que no se quede escondida.
  document.addEventListener('visibilitychange', function(){ if (!document.hidden) aparta(false); });
  window.addEventListener('pageshow', function(){ aparta(false); });
  // Si se abre un dialogo o se toca la propia barra, que este a la vista.
  document.addEventListener('click', function(ev){
    if (ev.target.closest && ev.target.closest('.finder-toolbar, #mioAbrir, #openSearch')) aparta(false);
  });
  if (movil.addEventListener) movil.addEventListener('change', mira);
})();
