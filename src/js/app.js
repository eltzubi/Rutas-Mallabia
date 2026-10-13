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
