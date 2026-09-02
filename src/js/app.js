// Shared behaviour for every page (both languages).
// Built from src/js/app.js by src/build.py -- edit there, not in app.js.

// --- language switch: remember an explicit choice, sitewide -- so index.html's
// redirect to the Basque homepage (see mallabia_head.html) doesn't bounce
// someone straight back after they've picked castellano on purpose ---
(function(){
  var link = document.querySelector('.lang-switch');
  if (!link || !link.hreflang) return;
  link.addEventListener('click', function(){
    try { localStorage.setItem('rutas-mallabia-lang', link.hreflang); } catch(err){}
  });
})();

// --- photo lightbox ---
(function(){
  var box = document.getElementById('lightbox');
  var boxImg = document.getElementById('lightboxImg');
  var close = document.getElementById('lightboxClose');
  if (!box || !boxImg || !close) return; // page has no photo gallery
  var lastTrigger = null;
  function open(src, trigger){
    boxImg.src = src;
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
    // The close button is the only focusable control inside the dialog, so
    // trapping focus just means Tab/Shift+Tab always lands back on it.
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
  // Antes se escondia mientras se recorria el listado de rutas, para no
  // taparlas; el resultado era que justo donde mas se baja no habia forma
  // de volver arriba. Ahora aparece en cuanto se ha bajado algo y se queda.
  function onScroll(){
    if (window.scrollY > window.innerHeight * 0.6) btn.classList.add('visible');
    else btn.classList.remove('visible');
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
  btn.addEventListener('click', function(){
    // Collapse-on-scroll (below) fights a smooth scroll-to-top: it re-adds
    // is-compact on every scroll tick while scrollY is still high, so the
    // header would stay collapsed/empty through nearly the whole animation
    // and only pop back at the very end -- reads as stuck/broken. The
    // scrolling-to-top flag on <html> tells that handler to stand down
    // until we've actually reached the top.
    var root = document.documentElement;
    var masthead = document.querySelector('.masthead');
    root.classList.add('scrolling-to-top');
    if (masthead) masthead.classList.remove('is-compact');
    window.scrollTo({ top:0, behavior: reduceMotion() ? 'auto' : 'smooth' });
    var stop = function(){ root.classList.remove('scrolling-to-top'); };
    window.addEventListener('scrollend', stop, { once:true });
    setTimeout(stop, 1000); // fallback where scrollend isn't supported
  });
})();

// --- compact masthead on scroll (home page only -- the tall brand photos
// aren't worth the sticky header space once the visitor is reading) ---
(function(){
  var masthead = document.querySelector('.masthead');
  var brand = masthead && masthead.querySelector('.brand');
  if (!masthead || !brand) return;
  function onScroll(){
    if (document.documentElement.classList.contains('scrolling-to-top')) return;
    // A single threshold flips back and forth (and visibly judders the
    // header, since collapsing it shifts the sticky layout underneath the
    // scroll position) whenever scrollY hovers right at that pixel. Two
    // thresholds with a dead zone between them fix that: once compact,
    // scrolling back up has to clear a lower bar before it expands again.
    if (window.scrollY > 60) masthead.classList.add('is-compact');
    else if (window.scrollY < 20) masthead.classList.remove('is-compact');
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
})();

// --- light/dark theme toggle ---
(function(){
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  var root = document.documentElement;

  // Light is the default regardless of OS preference; data-theme="dark"
  // (i.e. no data-theme attribute) is the explicit opt-in, chosen via the
  // toggle. The initial choice (from localStorage) is applied synchronously
  // in <head>, before this script runs, so there is no flash of the wrong
  // theme.
  function effectiveTheme(){
    return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }
  function updateLabel(){
    var eff = effectiveTheme();
    btn.setAttribute('aria-label', eff === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
  }
  function applyTheme(theme){
    if (theme === 'light') root.setAttribute('data-theme', 'light');
    else root.removeAttribute('data-theme');
    updateLabel();
  }

  updateLabel();

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
  if (!trigger || !box || !close || !form) return; // page has no report form

  var status = document.getElementById('reportStatus');
  var submitBtn = form.querySelector('.report-submit');
  var routeNameEl = document.querySelector('h1');
  var routeField = form.querySelector('input[name="route"]');
  var subjectField = form.querySelector('input[name="_subject"]');

  function open(){
    // innerText (not textContent) so a <br> inside the <h1> (route names
    // wrap onto a second line) becomes a space instead of vanishing.
    var routeName = routeNameEl ? (routeNameEl.innerText || routeNameEl.textContent).replace(/\s+/g, ' ').trim() : document.title;
    if (routeField) routeField.value = routeName;
    if (subjectField) subjectField.value = 'Incidencia en ruta: ' + routeName;
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
  box.addEventListener('click', function(e){ if (e.target === box) shut(); });
  // El dialogo se declara aria-modal, que le dice al lector de pantalla que lo
  // de detras esta inerte -- pero con el tabulador si se llegaba: quedaban 31
  // enlaces alcanzables por debajo del modal, invisibles y activables. Aqui el
  // recorrido del tabulador da la vuelta dentro del dialogo.
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), ' +
                  'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  function focusables(){
    return Array.prototype.filter.call(box.querySelectorAll(FOCUSABLE), function(el){
      var r = el.getBoundingClientRect();
      return r.width > 0 || r.height > 0;   // fuera el señuelo antispam, que va oculto
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
    status.textContent = 'Enviando…';
    status.className = 'report-status';
    fetch(FORMSPREE_ENDPOINT, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function(res){
      if (res.ok) {
        form.reset();
        status.textContent = 'Gracias, he recibido el aviso y lo revisaré en persona antes de actualizar la ruta.';
        status.className = 'report-status success';
      } else {
        status.textContent = 'No se ha podido enviar. Prueba de nuevo o escribe a trabakutik@gmail.com.';
        status.className = 'report-status error';
      }
    }).catch(function(){
      status.textContent = 'No se ha podido enviar. Prueba de nuevo o escribe a trabakutik@gmail.com.';
      status.className = 'report-status error';
    }).then(function(){
      submitBtn.disabled = false;
    });
  });
})();
