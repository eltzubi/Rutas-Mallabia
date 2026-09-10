// Shared behaviour for every page (both languages).
// Built from src/js/app.js by src/build.py -- edit there, not in app.js.

// --- route connections: real geography from the recorded tracks ---
(function(){
  var section = document.querySelector('.next-routes');
  if (!section) return;

  var heading = section.querySelector('.eyebrow');
  var list = section.querySelector('.next-route-list');
  var isEu = document.documentElement.lang === 'eu';
  if (heading) heading.textContent = isEu ? 'Inguru honetako ibilbideak' : 'Rutas por esta zona';
  if (!list || !window.fetch || !window.DOMParser) return;

  var file = (location.pathname.split('/').pop() || '').split('?')[0];
  var slug = file.replace(/\.eu\.html$/, '').replace(/\.html$/, '');
  if (!slug || slug === 'index') return;

  function routeSlug(href){
    return (href || '').split('/').pop().split('?')[0]
      .replace(/\.eu\.html$/, '').replace(/\.html$/, '');
  }

  function meters(a, b){
    var rad = Math.PI / 180;
    var lat = ((a[0] + b[0]) / 2) * rad;
    var dy = (a[0] - b[0]) * 111320;
    var dx = (a[1] - b[1]) * 111320 * Math.cos(lat);
    return Math.sqrt(dx * dx + dy * dy);
  }

  // Ratio of points in A that run close to B. The JSON tracks are already
  // resampled, so point coverage is a useful approximation of shared terrain.
  function coverage(a, b, threshold){
    if (!a.length || !b.length) return 0;
    var stepA = Math.max(1, Math.floor(a.length / 120));
    var stepB = Math.max(1, Math.floor(b.length / 160));
    var close = 0, total = 0;
    for (var i = 0; i < a.length; i += stepA){
      total++;
      for (var j = 0; j < b.length; j += stepB){
        if (meters(a[i], b[j]) <= threshold){ close++; break; }
      }
    }
    return total ? close / total : 0;
  }

  function pointsOf(track){
    return track && Array.isArray(track.points) ? track.points : [];
  }

  var home = isEu ? 'index.eu.html' : 'index.html';
  Promise.all([
    fetch('data/trailhead.json').then(function(r){ if (!r.ok) throw new Error('tracks'); return r.json(); }),
    fetch(home).then(function(r){ if (!r.ok) throw new Error('home'); return r.text(); })
  ]).then(function(values){
    var tracks = (values[0] && values[0].tracks) || [];
    var doc = new DOMParser().parseFromString(values[1], 'text/html');
    var cards = {};
    doc.querySelectorAll('a.route-card').forEach(function(card){
      var s = routeSlug(card.getAttribute('href'));
      if (!s) return;
      var name = card.querySelector('.route-card-name');
      var stats = card.querySelector('.route-card-stats');
      cards[s] = {
        href: card.getAttribute('href'),
        name: name ? name.innerHTML : s,
        stats: stats ? stats.innerHTML : ''
      };
    });

    var mine = null;
    tracks.forEach(function(t){ if (routeSlug(t.href) === slug) mine = t; });
    if (!mine) return;
    var myPoints = pointsOf(mine);

    var scored = [];
    tracks.forEach(function(t){
      var s = routeSlug(t.href);
      if (!s || s === slug || !cards[s]) return;
      var pts = pointsOf(t);
      if (!pts.length) return;

      // 70 m rewards genuinely shared paths; 250 m keeps routes in the same
      // hillside/valley relevant even when they use parallel tracks.
      var shared = Math.max(coverage(myPoints, pts, 70), coverage(pts, myPoints, 70));
      var nearby = Math.max(coverage(myPoints, pts, 250), coverage(pts, myPoints, 250));
      var score = shared * 4 + nearby;
      if (shared >= 0.08 || nearby >= 0.22) scored.push({ slug:s, shared:shared, nearby:nearby, score:score });
    });

    scored.sort(function(a, b){
      return b.score - a.score || b.shared - a.shared || b.nearby - a.nearby;
    });
    scored = scored.slice(0, 3);
    if (!scored.length) return; // keep the static fallback from build.py

    list.innerHTML = '';
    scored.forEach(function(item){
      var c = cards[item.slug];
      var link = document.createElement('a');
      link.className = 'next-route';
      link.href = c.href;
      var name = document.createElement('span');
      name.className = 'next-route-name';
      name.innerHTML = c.name;
      var stats = document.createElement('span');
      stats.className = 'next-route-stats';
      stats.innerHTML = c.stats;
      link.appendChild(name);
      link.appendChild(stats);
      list.appendChild(link);
    });
  }).catch(function(){
    // The two cards written by build.py remain visible as a no-JS/network fallback.
  });
})();

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

// --- light/dark theme toggle ---
(function(){
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  var root = document.documentElement;
  function effectiveTheme(){
    return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }
  function updateLabel(){
    var eff = effectiveTheme();
    btn.setAttribute('aria-label', eff === 'dark' ? btn.dataset.labelLight : btn.dataset.labelDark);
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
