// Un solo acceso para el aviso y la información práctica de la portada.
// Mueve el contenido existente: sin JS siguen funcionando los desplegables
// y sus enlaces originales. No duplica textos, teléfonos ni mapas.
(function(){
  'use strict';
  var dialog = document.getElementById('tripInfoDialog');
  var badge = document.getElementById('tripInfoBadge');
  var header = document.querySelector('.masthead');
  if (!dialog || !badge || !header || typeof dialog.showModal !== 'function') return;
  var trigger = badge.querySelector('button');
  var close = document.getElementById('tripInfoClose');
  var tabs = Array.prototype.slice.call(dialog.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(dialog.querySelectorAll('[role="tabpanel"]'));
  var sources = ['#beforeYouGo .info-details-body', '#info-aparcar .info-details-body',
    '#info-comer .info-details-body', '#info-dormir .info-details-body',
    '#info-agua .info-details-body', '#info-preguntas .info-details-body']
    .map(function(selector){ return document.querySelector(selector); });
  if (!trigger || !close || tabs.length !== 6 || panels.length !== 6 ||
      sources.some(function(source){ return !source; })) return;

  sources.forEach(function(source, i){ panels[i].appendChild(source); });
  header.insertBefore(badge, header.firstChild);
  badge.hidden = false;
  document.body.classList.add('trip-info-ready');

  try {
    var nav = window.performance && window.performance.getEntriesByType &&
      window.performance.getEntriesByType('navigation')[0];
    if (nav && nav.type === 'reload') sessionStorage.removeItem('rutas-mallabia-aviso');
    if (sessionStorage.getItem('rutas-mallabia-aviso')) badge.classList.add('ya-visto');
  } catch(err){}

  var overflowBefore = '';
  var scrollBefore = 0;
  function select(index, focus){
    tabs.forEach(function(tab, i){
      tab.setAttribute('aria-selected', i === index ? 'true' : 'false');
      tab.setAttribute('tabindex', i === index ? '0' : '-1');
      panels[i].hidden = i !== index;
      if (i === index) panels[i].scrollTop = 0;
    });
    if (focus) tabs[index].focus();
    if (index === 0) {
      badge.classList.add('ya-visto');
      try { sessionStorage.setItem('rutas-mallabia-aviso', '1'); } catch(err){}
    }
  }
  function open(index){
    if (!dialog.open) {
      overflowBefore = document.body.style.overflow;
      scrollBefore = window.scrollY || window.pageYOffset || 0;
      dialog.showModal();
      document.body.style.overflow = 'hidden';
      trigger.setAttribute('aria-expanded', 'true');
    }
    select(index || 0, false);
    close.focus({ preventScroll: true });
  }
  function shut(){ if (dialog.open) dialog.close(); }
  trigger.addEventListener('click', function(){ if (dialog.open) shut(); else open(0); });
  close.addEventListener('click', shut);
  dialog.querySelectorAll('.notice-close').forEach(function(button){
    button.addEventListener('click', shut);
  });
  dialog.addEventListener('close', function(){
    document.body.style.overflow = overflowBefore;
    trigger.setAttribute('aria-expanded', 'false');
    trigger.focus({ preventScroll: true });
    // El fondo queda inmóvil al leer; no hay salto al principio al cerrar.
    if (Math.abs((window.scrollY || 0) - scrollBefore) > 1) {
      window.scrollTo({ top: scrollBefore, behavior: 'instant' });
    }
  });
  dialog.addEventListener('click', function(ev){
    if (ev.target !== dialog) return;
    var rect = dialog.getBoundingClientRect();
    if (ev.clientX < rect.left || ev.clientX > rect.right ||
        ev.clientY < rect.top || ev.clientY > rect.bottom) shut();
  });
  tabs.forEach(function(tab, i){
    tab.addEventListener('click', function(){ select(i, false); });
    tab.addEventListener('keydown', function(ev){
      var columns = window.matchMedia('(min-width:600px)').matches ? 3 : 2;
      var delta = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: columns, ArrowUp: -columns };
      var index = ev.key === 'Home' ? 0 : ev.key === 'End' ? tabs.length - 1 :
        delta[ev.key] !== undefined ? (i + delta[ev.key] + tabs.length) % tabs.length : null;
      if (index === null) return;
      ev.preventDefault();
      select(index, true);
    });
  });
  // Conserva los enlaces que ya apuntaban a #info-aparcar, etc.
  function fromHash(){
    var ids = ['beforeYouGo', 'info-aparcar', 'info-comer', 'info-dormir', 'info-agua', 'info-preguntas'];
    var index = ids.indexOf((window.location.hash || '').slice(1));
    if (index !== -1) open(index);
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
