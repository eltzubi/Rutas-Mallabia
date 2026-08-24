// Shared behaviour for every page (both languages).
// Built from src/js/app.js by src/build.py -- edit there, not in app.js.

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

// --- "before you leave" info modal (home page only) ---
(function(){
  var trigger = document.getElementById('infoTrigger');
  var box = document.getElementById('infoModal');
  var close = document.getElementById('infoModalClose');
  if (!trigger || !box || !close) return;
  function open(){
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
  document.addEventListener('keydown', function(e){
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') shut();
  });
})();

// --- back-to-top button ---
(function(){
  var btn = document.getElementById('toTop');
  if (!btn) return;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function onScroll(){
    if (window.scrollY > window.innerHeight * 0.6) btn.classList.add('visible');
    else btn.classList.remove('visible');
  }
  window.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
  btn.addEventListener('click', function(){
    window.scrollTo({ top:0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });
})();

// --- compact masthead on scroll (home page only -- the tall brand photos
// aren't worth the sticky header space once the visitor is reading) ---
(function(){
  var masthead = document.querySelector('.masthead');
  var brand = masthead && masthead.querySelector('.brand');
  if (!masthead || !brand) return;
  function onScroll(){
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
