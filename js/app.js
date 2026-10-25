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
/* Abierta una foto, se pasa a la siguiente con el dedo, con las flechas del
   teclado o con los botones de los lados, y se sale tocando fuera. Antes
   habia que cerrar y volver a abrir para ver la de al lado.

   No pesa en el sitio: las fotos ya estaban publicadas y se piden igual que
   antes, una a una. Lo unico que se adelanta es la de delante y la de
   detras, para que al pasar no haya parpadeo; las demas no se tocan hasta
   que se llega a ellas. */
(function(){
  var box = document.getElementById('lightbox');
  var boxImg = document.getElementById('lightboxImg');
  var close = document.getElementById('lightboxClose');
  if (!box || !boxImg || !close) return; // page has no photo gallery
  var eu = document.documentElement.lang === 'eu';
  var T = eu ? { ant:'Aurrekoa', sig:'Hurrengoa', de:'/' }
             : { ant:'Anterior', sig:'Siguiente', de:'/' };
  var fotos = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox-src]'));
  if (!fotos.length) return;
  var indice = 0, lastTrigger = null;

  function fuente(el){ return el.dataset.lightboxSrc; }
  function adelanta(i){
    if (i < 0 || i >= fotos.length) return;
    var im = new Image(); im.src = fuente(fotos[i]);
  }
  function muestra(i){
    indice = (i + fotos.length) % fotos.length;
    var el = fotos[indice], src = fuente(el);
    // data-lightbox-src es el .webp de tamano completo, que es lo que ve
    // casi todo el mundo. El respaldo es el -800.jpg, lo unico que puede
    // abrir un navegador sin WebP: el original de 1600 ya no se publica
    // (vive en img/orig/, ver _config.yml).
    boxImg.onerror = function(){
      boxImg.onerror = null;
      boxImg.src = src.replace(/\.webp$/i, '-800.jpg');
    };
    boxImg.src = src;
    var triggerImg = el.querySelector('img');
    boxImg.alt = (triggerImg && triggerImg.alt) || '';
    lastTrigger = el;
    if (cuenta) cuenta.textContent = (indice + 1) + ' ' + T.de + ' ' + fotos.length;
    adelanta(indice + 1); adelanta(indice - 1);
  }
  function pasa(n){
    if (fotos.length > 1 && box.classList.contains('open')) muestra(indice + n);
  }

  // Los mandos se crean aqui y no en el HTML de las 63 fichas: sin
  // JavaScript la foto ampliada no se abre, asi que tampoco harian nada.
  var cuenta = null, antes = null, luego = null;
  if (fotos.length > 1) {
    cuenta = document.createElement('p');
    cuenta.className = 'lightbox-cuenta';
    box.appendChild(cuenta);
    var flecha = function(clase, etiqueta, d){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'lightbox-nav ' + clase;
      b.setAttribute('aria-label', etiqueta); b.title = etiqueta;
      b.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"'
        + ' stroke="currentColor" stroke-width="2" stroke-linecap="round"'
        + ' stroke-linejoin="round" aria-hidden="true"><path d="M'
        + (d < 0 ? '15 5 8 12l7 7' : '9 5 16 12l-7 7') + '"/></svg>';
      b.addEventListener('click', function(ev){ ev.stopPropagation(); pasa(d); });
      box.appendChild(b);
      return b;
    };
    antes = flecha('is-prev', T.ant, -1);
    luego = flecha('is-next', T.sig, 1);
  }

  function open(el){
    muestra(fotos.indexOf(el));
    box.classList.add('open');
    document.body.style.overflow = 'hidden';
    close.focus();
  }
  function shut(){
    box.classList.remove('open');
    // Quitar el respaldo antes de vaciar: si no, el src vacio cuenta como
    // error y se pedia un -800.jpg que ya no hacia falta.
    boxImg.onerror = null;
    boxImg.src='';
    document.body.style.overflow = '';
    if(lastTrigger) lastTrigger.focus();
  }
  fotos.forEach(function(el){
    el.addEventListener('click', function(){ open(el); });
  });
  close.addEventListener('click', shut);
  // Tocar fuera de la foto cierra. La foto no: ahi vive el gesto de pasar,
  // y un arrastre que se queda corto no puede cerrar sin querer.
  var pasadoHace = 0;
  box.addEventListener('click', function(e){
    // Un gesto de pasar termina con un click sintetico; si ese click cae en
    // el fondo cerraria la foto recien abierta. Se ignora lo que llegue
    // justo detras de un pase.
    if (Date.now() - pasadoHace < 400) return;
    if (e.target === box) shut();
  });

  // Arrastrar con el dedo. Se exige que el gesto sea mas horizontal que
  // vertical para no robarle el scroll a nadie, y un recorrido minimo para
  // que un toque torpe no cambie de foto sin querer.
  var x0 = 0, y0 = 0, movido = false;
  box.addEventListener('touchstart', function(e){
    if (e.touches.length !== 1) return;
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; movido = false;
  }, { passive: true });
  box.addEventListener('touchmove', function(e){
    if (e.touches.length !== 1) return;
    if (Math.abs(e.touches[0].clientX - x0) > 10) movido = true;
  }, { passive: true });
  box.addEventListener('touchend', function(e){
    if (!movido || !e.changedTouches.length) return;
    var dx = e.changedTouches[0].clientX - x0;
    var dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) {
      pasa(dx < 0 ? 1 : -1);
      pasadoHace = Date.now();
      movido = false;
    }
  });

  document.addEventListener('keydown', function(e){
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') { shut(); return; }
    if (e.key === 'ArrowRight') { pasa(1); return; }
    if (e.key === 'ArrowLeft') { pasa(-1); return; }
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

  // Va en la barra de arriba, la primera de todo, delante de «Mallabia ·
  // Bizkaia»: en la esquina de abajo pasaba por encima del texto de las
  // tarjetas, y en medio de la barra apretaba contra EU/ES, que es lo mas
  // pequeno que hay ahi y lo que mas cuesta acertar con el dedo.
  var cabecera = document.querySelector('.masthead');
  var sitio = cabecera && cabecera.querySelector('.place');
  var derecha = cabecera && cabecera.querySelector('.masthead-right');
  if (sitio) cabecera.insertBefore(insignia, sitio);
  else if (derecha) cabecera.insertBefore(insignia, derecha);

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

  function quieto(){
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /* Al cerrar, la pagina vuelve a donde estaba antes de abrir el aviso.
     El aviso se lee de arriba abajo y se cierra con su propio boton, que
     esta al final del texto: sin esto te quedabas a media pagina, en mitad
     del listado de rutas, mirando una tarjeta cualquiera. El boton «Cerrar
     aviso» ya intentaba subir, pero a la cabecera del <details>, que en este
     modo lleva display:none -- scrollIntoView sobre algo oculto no hace
     nada, asi que no subia. Se apunta la posicion al abrir y se vuelve a
     ella al cerrar, venga el cierre del propio boton o de la insignia. */
  var vuelta = null;
  detalle.addEventListener('toggle', function(){
    boton.setAttribute('aria-expanded', detalle.open ? 'true' : 'false');
    if (detalle.open) return;
    var destino = vuelta;
    vuelta = null;
    if (destino === null) { seccion.scrollIntoView({ block:'start' }); return; }
    window.scrollTo({ top: destino, behavior: quieto() ? 'auto' : 'smooth' });
  });

  boton.addEventListener('click', function(){
    var abrir = !detalle.open;
    if (abrir) vuelta = window.scrollY || window.pageYOffset || 0;
    detalle.open = abrir;
    // A partir de aqui las ondas bajan de intensidad: ya ha mirado el aviso.
    insignia.classList.add('ya-visto');
    try { sessionStorage.setItem('rutas-mallabia-aviso', '1'); } catch(err){}
    if (!abrir) return;
    detalle.scrollIntoView({ block:'start', behavior: quieto() ? 'auto' : 'smooth' });
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
  function clear(){
    if (!favs.length) return;
    favs = [];
    try { localStorage.removeItem(KEY); } catch (_) {}
    document.dispatchEvent(new CustomEvent('favs:change', { detail: { favs: [] } }));
  }
  window.trabakutikFavs = { has: has, toggle: toggle, clear: clear, slugOf: slugOf,
                            list: function(){ return favs.slice(); } };

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
    // Se pueden vaciar desde «Lo mio» sin tocar este corazon: hay que
    // repintarlo tambien cuando el cambio viene de fuera.
    document.addEventListener('favs:change', function(){ paintHeart(btn, has(slug)); });
    photo.appendChild(btn);
  });

  /* Ficha: Guardar y Compartir, arriba a la derecha, a la altura de
     «← Rutas». Estaban en la fila de descargas, a media pagina: para
     guardar una ruta recien abierta habia que bajar a buscarlos. Arriba
     estan a la vista desde el primer momento. Van sin rotulo, como el resto
     de la barra, con su title y su aria-label. */
  var barraDerecha = document.querySelector('.masthead .masthead-right');
  var row = document.querySelector('.wikiloc-row');
  if (!barraDerecha && !row) return;
  var slug = slugOf(location.pathname) || 'index';
  var arriba = !!barraDerecha && !!document.querySelector('.back-link');
  var fav = document.createElement('button');
  fav.type = 'button';
  fav.className = arriba ? 'mast-accion fav-action' : 'wikiloc-link ghost fav-action';
  function paintFav(){
    var on = has(slug);
    fav.innerHTML = arriba
      ? HEART.replace('width="18" height="18"', 'width="15" height="15"')
      : HEART.replace('width="18" height="18"', 'width="15" height="15"') + (on ? W.saved : W.saveShort);
    paintHeart(fav, on);
  }
  paintFav();
  fav.addEventListener('click', function(){ toggle(slug); paintFav(); });
  document.addEventListener('favs:change', paintFav);

  var share = document.createElement('button');
  share.type = 'button';
  share.className = arriba ? 'mast-accion share-action' : 'wikiloc-link ghost share-action';
  share.innerHTML = arriba ? SHARE : SHARE + W.share;
  if (arriba) { share.title = W.share; share.setAttribute('aria-label', W.share); }
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
        if (arriba) {
          share.title = W.copied;
          setTimeout(function(){ share.title = W.share; }, 2000);
        } else {
          share.lastChild.textContent = W.copied;
          setTimeout(function(){ share.lastChild.textContent = W.share; }, 2000);
        }
      });
    }
  });
  if (arriba) {
    // delante del idioma, para que los dos botones de la ruta queden juntos
    // y el idioma, «Lo mio» y el tema sigan en su orden de siempre.
    var idioma = barraDerecha.querySelector('.lang-switch');
    if (idioma && idioma.before) { idioma.before(fav); idioma.before(share); }
    else { barraDerecha.appendChild(fav); barraDerecha.appendChild(share); }
  } else if (row) {
    var gpx = row.querySelector('a[href$=".gpx"]');
    var after = row.querySelector('a[href$=".kml"]') || gpx;
    if (after) { after.after(share); after.after(fav); }
    else { row.appendChild(fav); row.appendChild(share); }
  }
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
    ? { guardando:'Gordetzen…', hecho:'Mendirako prest', fallo:'Ezin izan dira denak gorde',
        confirma:'Ziur?' }
    : { guardando:'Guardando…', hecho:'Listas para el monte', fallo:'No se pudieron guardar todas',
        confirma:'\u00bfSeguro?' };

  function lee(clave){
    try { var v = JSON.parse(localStorage.getItem(clave) || '[]'); return Array.isArray(v) ? v : []; }
    catch (_) { return []; }
  }
  // Apuntar la ficha que se esta viendo. Se hace siempre, aunque el panel no
  // se abra nunca: es lo que lo llena cuando se abre.
  // Ojo con el .es: la portada en castellano es index.es.html, y quitando
  // solo el .html se apuntaba a si misma como «index.es» — una ruta que no
  // existe, ocupando uno de los seis sitios de la lista.
  var aqui = location.pathname.split('/').pop().replace(/\.(eu|es)\.html$/,'').replace(/\.html$/,'');
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
  var borrarVistas = document.getElementById('mioBorrar');
  var borrarFavs = document.getElementById('mioBorrarFavs');
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
    var v = pinta(listaVistas, vacioVistas, lee(VISTAS).filter(function(s){ return s !== aqui; }));
    if (borrarVistas) borrarVistas.hidden = v === 0;
    if (borrarFavs) { borrarFavs.hidden = favs.length === 0; sinConfirmar(borrarFavs); }
    if (guardar) guardar.hidden = n === 0;
    if (nota) nota.hidden = n === 0;
  }

  /* Quitar todas las favoritas pide un segundo toque. Las vistas se apuntan
     solas y borrarlas no pierde nada; las favoritas las ha ido guardando el
     que mira la web, una a una, y un roce no puede llevarselas todas. */
  function sinConfirmar(b){
    if (!b) return;
    if (b.dataset) delete b.dataset.confirmando;
    if (b.textContent !== rotuloBorrar) b.textContent = rotuloBorrar;
    b.classList.remove('va-en-serio');
  }
  var rotuloBorrar = borrarFavs ? borrarFavs.textContent : '';
  if (borrarFavs) borrarFavs.addEventListener('click', function(){
    if (!(borrarFavs.dataset && borrarFavs.dataset.confirmando)) {
      if (borrarFavs.dataset) borrarFavs.dataset.confirmando = '1';
      borrarFavs.textContent = T.confirma;
      borrarFavs.classList.add('va-en-serio');
      setTimeout(function(){ sinConfirmar(borrarFavs); }, 4000);
      return;
    }
    sinConfirmar(borrarFavs);
    if (window.trabakutikFavs && window.trabakutikFavs.clear) window.trabakutikFavs.clear();
    else { try { localStorage.removeItem('trabakutik_favs'); } catch (_) {} }
    rellena();
  });

  /* Borrar las vistas hace poco. Es lo unico del panel que se apunta solo,
     sin que nadie lo pida, asi que tiene que poder quitarse. Las favoritas
     no llevan boton: esas se quitan con su propio corazon, una a una. */
  if (borrarVistas) borrarVistas.addEventListener('click', function(){
    try { localStorage.removeItem(VISTAS); } catch (_) {}
    pinta(listaVistas, vacioVistas, []);
    borrarVistas.hidden = true;
  });

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

/* ---- Al abrir una pregunta, ponerla a la vista -------------------------
   Lo pidio el autor. Con el <details name="faq"> nativo, abrir una de abajo
   CIERRA la de arriba en el mismo paso, y la pagina se encoge de golpe: la
   pregunta que acabas de tocar se te va hacia arriba, a veces debajo de la
   cabecera pegajosa y a veces fuera de la pantalla.

   Si la pregunta entera cabe en la pantalla se centra; si no cabe -- la guia
   paso a paso con sus ocho capturas no cabe en ningun movil -- se lleva el
   titulo justo debajo de la cabecera, que es lo util: centrar algo de tres
   pantallas de alto deja el titulo fuera. Se espera dos fotogramas porque en
   el primero el navegador todavia no ha recalculado el alto de la que se
   cierra, y la cuenta saldria sobre la pagina de antes. */
(function(){
  var items = document.querySelectorAll('details.faq-item');
  if (!items.length) return;
  var quieto = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cabecera = document.querySelector('.masthead');

  function pon(d){
    var alto = window.innerHeight;
    var margen = (cabecera ? cabecera.getBoundingClientRect().height : 0) + 12;
    var caja = d.getBoundingClientRect();
    var destino;
    if (caja.height + margen <= alto) {
      destino = caja.top + window.pageYOffset - (alto - caja.height) / 2;
    } else {
      destino = caja.top + window.pageYOffset - margen;
    }
    destino = Math.max(0, Math.round(destino));
    try {
      window.scrollTo({ top: destino, behavior: quieto ? 'auto' : 'smooth' });
    } catch (e) {
      window.scrollTo(0, destino);   // navegadores sin la forma de objeto
    }
  }

  Array.prototype.forEach.call(items, function(d){
    d.addEventListener('toggle', function(){
      if (!d.open) return;
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ pon(d); }); });
    });
  });
})();
