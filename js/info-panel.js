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

  function positionPanel(){
    var rect = trigger.getBoundingClientRect();
    var top = Math.max(6, (rect.bottom !== undefined ? rect.bottom : rect.top + rect.height) + 8);
    dialog.style.setProperty('--trip-top', top + 'px');
    dialog.style.setProperty('--trip-max-height', Math.max(170, window.innerHeight - top - 12) + 'px');
  }
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
      positionPanel();
      if (typeof dialog.show === 'function') dialog.show();
      else dialog.showModal();
      trigger.setAttribute('aria-expanded', 'true');
      badge.classList.add('trip-open');
    }
    select(index || 0, false);
    tabs[index || 0].focus({ preventScroll: true });
  }
  function shut(){ if (dialog.open) dialog.close(); }
  trigger.addEventListener('click', function(){ if (dialog.open) shut(); else open(0); });
  close.addEventListener('click', shut);
  dialog.querySelectorAll('.notice-close').forEach(function(button){
    button.addEventListener('click', shut);
  });
  dialog.addEventListener('close', function(){
    trigger.setAttribute('aria-expanded', 'false');
    badge.classList.remove('trip-open');
    trigger.focus({ preventScroll: true });
  });
  document.addEventListener('pointerdown', function(ev){
    if (dialog.open && !dialog.contains(ev.target) && !badge.contains(ev.target)) shut();
  });
  window.addEventListener('resize', function(){ if (dialog.open) positionPanel(); });
  window.addEventListener('scroll', function(){ if (dialog.open) positionPanel(); }, { passive:true });
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
