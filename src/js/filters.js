// Home page route list: every route is on the page from the start; the
// activity/difficulty chips and the range sliders just narrow it down, and
// the same selection drives the map view. Language-independent -- the labels
// it writes come from the page itself (data-* attributes carry the
// per-language text).
(function(){
  var activityChips = document.querySelectorAll('.activity-chip');
  var difficultyChips = document.querySelectorAll('.difficulty-chip');
  var distanceChips = document.querySelectorAll('.distance-chip');
  var moreFiltersToggle = document.getElementById('moreFiltersToggle');
  var moreFiltersPanel = document.getElementById('moreFiltersPanel');
  var viewBtns = document.querySelectorAll('.view-toggle-btn');
  var resultsList = document.getElementById('routeResults');
  var mapWrap = document.getElementById('routeMapWrap');
  var cards = document.querySelectorAll('.route-card[data-activity]');
  var emptyMsg = document.getElementById('filterEmpty');
  var resultCount = document.getElementById('resultCount');
  var activeFiltersDisplay = document.getElementById('activeFilters');
  var filterSuggestions = document.getElementById('filterSuggestions');
  var suggestionBtns = document.querySelectorAll('.suggestion-btn');
  var quickBtns = document.querySelectorAll('.quick-help-btn');
  var distanceMin = document.getElementById('distanceRangeMin');
  var distanceMax = document.getElementById('distanceRangeMax');
  var desnivelMin = document.getElementById('desnivelRangeMin');
  var desnivelMax = document.getElementById('desnivelRangeMax');
  var distanceVal = document.getElementById('distanceVal');
  var desnivelVal = document.getElementById('desnivelVal');
  var distanceFill = document.getElementById('distanceFill');
  var desnivelFill = document.getElementById('desnivelFill');
  var resetBtns = document.querySelectorAll('[data-filter-reset]');
  if (!activityChips.length || !cards.length) return;

  var view = 'list';

  // Se consulta en cada salto, no una vez al cargar: la preferencia puede
  // cambiar con la sesion abierta.
  function reduceMotion(){
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  var filters = document.querySelector('.range-filters') || document.body;
  var TXT_APPROX = filters.dataset.approx || 'aprox.';
  var TXT_ALL_DISTANCE = filters.dataset.allDistance || 'Todas';
  var TXT_ALL_DESNIVEL = filters.dataset.allDesnivel || 'Todos';
  var TXT_COUNT_ONE = filters.dataset.countOne || 'ruta encontrada';
  var TXT_COUNT_MANY = filters.dataset.countMany || 'rutas encontradas';

  function niceCeil(n, step){ return Math.ceil(n / step) * step; }

  var distances = Array.prototype.map.call(cards, function(c){ return parseFloat(c.dataset.distanceKm) || 0; });
  var desniveles = Array.prototype.map.call(cards, function(c){ return parseFloat(c.dataset.desnivelM) || 0; });
  var maxDistance = niceCeil(Math.max.apply(null, distances), 5) || 5;
  var maxDesnivel = niceCeil(Math.max.apply(null, desniveles), 100) || 100;

  function setupPair(minEl, maxEl, max, step){
    if (!minEl || !maxEl) return;
    minEl.max = maxEl.max = max;
    minEl.step = maxEl.step = step;
    minEl.value = 0;
    maxEl.value = max;
  }
  setupPair(distanceMin, distanceMax, maxDistance, 0.5);
  setupPair(desnivelMin, desnivelMax, maxDesnivel, 25);

  function linkPair(minEl, maxEl, onChange){
    if (!minEl || !maxEl) return;
    function clamp(){
      if (parseFloat(minEl.value) > parseFloat(maxEl.value)) minEl.value = maxEl.value;
    }
    minEl.addEventListener('input', function(){ clamp(); onChange(); apply(); });
    maxEl.addEventListener('input', function(){
      if (parseFloat(maxEl.value) < parseFloat(minEl.value)) maxEl.value = minEl.value;
      onChange(); apply();
    });
    [minEl, maxEl].forEach(function(el){
      ['mousedown', 'touchstart'].forEach(function(evt){
        el.addEventListener(evt, function(){
          minEl.classList.remove('range-top');
          maxEl.classList.remove('range-top');
          el.classList.add('range-top');
        });
      });
    });
  }
  linkPair(distanceMin, distanceMax, function(){ setActiveDistanceChip(null); });
  linkPair(desnivelMin, desnivelMax, function(){});

  function fillPair(minEl, maxEl, fillEl, max){
    if (!minEl || !maxEl || !fillEl || !max) return;
    var loPct = parseFloat(minEl.value) / max * 100;
    var hiPct = parseFloat(maxEl.value) / max * 100;
    fillEl.style.left = loPct + '%';
    fillEl.style.right = (100 - hiPct) + '%';
  }

  function fmtRange(minV, maxV, max, isElevation, allWord){
    if (minV <= 0 && maxV >= max) return allWord;
    var fmt = function(n){ return isElevation ? Math.round(n) : n.toFixed(1).replace('.0',''); };
    return fmt(minV) + '–' + fmt(maxV) + (isElevation ? ' m ' : ' km ') + TXT_APPROX;
  }

  function setActiveDistanceChip(chip){
    distanceChips.forEach(function(c){ c.classList.toggle('active', c === chip); });
  }

  var DISTANCE_PRESETS = {
    corto: [0, 10],
    media1: [10, 20],
    media2: [20, 30],
    larga: [30, Infinity]
  };

  distanceChips.forEach(function(chip){
    chip.addEventListener('click', function(){
      var already = chip.classList.contains('active');
      setActiveDistanceChip(already ? null : chip);
      var range = DISTANCE_PRESETS[chip.dataset.distancePreset];
      if (already || !range) {
        distanceMin.value = 0;
        distanceMax.value = maxDistance;
      } else {
        distanceMin.value = range[0];
        distanceMax.value = Math.min(range[1], maxDistance);
      }
      apply();
    });
  });

  if (moreFiltersToggle && moreFiltersPanel) {
    moreFiltersToggle.addEventListener('click', function(){
      var open = moreFiltersPanel.hasAttribute('hidden');
      if (open) moreFiltersPanel.removeAttribute('hidden');
      else moreFiltersPanel.setAttribute('hidden', '');
      moreFiltersToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Deja la fila de pestanas justo debajo de la cabecera y de la barra de
  // actividad, que van fijas arriba y taparian el principio del mapa.
  var STICKY_H = 132;

  function scrollToMap(){
    var anchor = document.querySelector('.view-toggle-row') || mapWrap;
    if (!anchor) return;
    // En dos pasos: el primero cuando ya se ha ocultado la lista, y el
    // segundo cuando el mapa termina de montarse y la pagina deja de
    // moverse bajo los pies.
    var go = function(smooth){
      var y = window.pageYOffset + anchor.getBoundingClientRect().top - STICKY_H;
      window.scrollTo({ top: Math.max(y, 0), behavior: (smooth && !reduceMotion()) ? 'smooth' : 'auto' });
    };
    requestAnimationFrame(function(){ go(true); });
    setTimeout(function(){ go(false); }, 700);
  }

  viewBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      view = btn.dataset.view;
      viewBtns.forEach(function(b){ b.classList.toggle('active', b === btn); });
      if (resultsList) resultsList.hidden = (view !== 'list');
      if (mapWrap) mapWrap.hidden = (view !== 'map');
      // Al pedir el mapa, llevar la vista hasta el; se salta a la fila de
      // pestanas (no al mapa) porque con la lista oculta la pagina se queda
      // corta y el scroll toparia con el final, dejando el mapa medio tapado
      // por la cabecera.
      if (view === 'map' && mapWrap) {
        scrollToMap();
      }
      saveFiltersToStorage();
    });
  });

  function updateActiveFiltersDisplay(){
    if (!activeFiltersDisplay) return;
    var activeDifficulty = Array.prototype.filter.call(difficultyChips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.difficulty; });
    var activeActivities = Array.prototype.filter.call(activityChips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.activity; });
    var minD = distanceMin ? parseFloat(distanceMin.value) : 0;
    var maxD = distanceMax ? parseFloat(distanceMax.value) : Infinity;
    var minE = desnivelMin ? parseFloat(desnivelMin.value) : 0;
    var maxE = desnivelMax ? parseFloat(desnivelMax.value) : Infinity;

    var parts = [];
    if (activeActivities.length !== activityChips.length) {
      parts.push(activeActivities.join(' + '));
    }
    if (activeDifficulty.length !== difficultyChips.length) {
      parts.push(activeDifficulty.join(' + '));
    }
    if (minD > 0 || maxD < maxDistance) {
      parts.push(fmtRange(minD, maxD, maxDistance, false, ''));
    }
    if (minE > 0 || maxE < maxDesnivel) {
      parts.push(fmtRange(minE, maxE, maxDesnivel, true, ''));
    }

    if (parts.length > 0) {
      activeFiltersDisplay.textContent = parts.join(' · ');
      activeFiltersDisplay.style.display = 'block';
    } else {
      activeFiltersDisplay.textContent = '';
      activeFiltersDisplay.style.display = 'none';
    }
  }

  function apply(){
    var activeDifficulty = Array.prototype.filter.call(difficultyChips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.difficulty; });
    var minD = distanceMin ? parseFloat(distanceMin.value) : 0;
    var maxD = distanceMax ? parseFloat(distanceMax.value) : Infinity;
    var minE = desnivelMin ? parseFloat(desnivelMin.value) : 0;
    var maxE = desnivelMax ? parseFloat(desnivelMax.value) : Infinity;
    if (distanceVal) distanceVal.textContent = fmtRange(minD, maxD, maxDistance, false, TXT_ALL_DISTANCE);
    if (desnivelVal) desnivelVal.textContent = fmtRange(minE, maxE, maxDesnivel, true, TXT_ALL_DESNIVEL);
    fillPair(distanceMin, distanceMax, distanceFill, maxDistance);
    fillPair(desnivelMin, desnivelMax, desnivelFill, maxDesnivel);

    var activeActivities = Array.prototype.filter.call(activityChips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.activity; });

    var visibleHrefs = [];
    var shown = 0;
    cards.forEach(function(card){
      var km = parseFloat(card.dataset.distanceKm) || 0;
      var m = parseFloat(card.dataset.desnivelM) || 0;
      var activities = card.dataset.activity.split(',');
      var matchesActivity = !activeActivities.length || activities.some(function(a){
        return activeActivities.indexOf(a) !== -1;
      });
      var matchesDifficulty = !activeDifficulty.length || activeDifficulty.indexOf(card.dataset.difficulty) !== -1;
      var matches = matchesActivity && matchesDifficulty && km >= minD && km <= maxD && m >= minE && m <= maxE;
      if (matches) {
        shown++;
        visibleHrefs.push(card.getAttribute('href').replace(/\.eu\.html$/, '.html'));
      }
      card.classList.toggle('is-hidden', !matches);
    });
    if (emptyMsg) emptyMsg.classList.toggle('visible', shown === 0);
    if (filterSuggestions) filterSuggestions.hidden = (shown > 0);
    if (resultCount) resultCount.textContent = shown + ' ' + (shown === 1 ? TXT_COUNT_ONE : TXT_COUNT_MANY);

    // Con los deslizadores en un extremo se llega a "0 rutas encontradas" y
    // antes no habia forma de salir de ahi sin recolocarlos a mano o recargar.
    // El boton solo aparece cuando hay algo que quitar.
    var filtrado = activeActivities.length !== activityChips.length ||
                   activeDifficulty.length !== difficultyChips.length ||
                   minD > 0 || maxD < maxDistance || minE > 0 || maxE < maxDesnivel;
    resetBtns.forEach(function(b){ b.hidden = !filtrado; });
    document.dispatchEvent(new CustomEvent('routefilters:apply', { detail: { visibleHrefs: visibleHrefs } }));
    saveFiltersToStorage();
    updateActiveFiltersDisplay();
  }

  // Apagar el ultimo chip encendido dejaba los botones apagados y la lista
  // entera igual ("sin filtro"), que no dice nada: mejor no dejar apagarlo.
  function toggleChip(chip, group){
    var activos = 0;
    group.forEach(function(c){ if (c.classList.contains('active')) activos++; });
    if (chip.classList.contains('active') && activos === 1) {
      // Un clic que no hace nada parece que la pagina se ha colgado: un
      // pulso corto deja claro que ese es el unico que queda encendido.
      chip.classList.remove('is-locked');
      void chip.offsetWidth;
      chip.classList.add('is-locked');
      setTimeout(function(){ chip.classList.remove('is-locked'); }, 400);
      return;
    }
    chip.classList.toggle('active');
    apply();
  }

  function saveFiltersToStorage(){
    try {
      var state = {
        activities: Array.prototype.filter.call(activityChips, function(c){ return c.classList.contains('active'); }).map(function(c){ return c.dataset.activity; }),
        difficulties: Array.prototype.filter.call(difficultyChips, function(c){ return c.classList.contains('active'); }).map(function(c){ return c.dataset.difficulty; }),
        distance: [distanceMin ? parseFloat(distanceMin.value) : 0, distanceMax ? parseFloat(distanceMax.value) : maxDistance],
        desnivel: [desnivelMin ? parseFloat(desnivelMin.value) : 0, desnivelMax ? parseFloat(desnivelMax.value) : maxDesnivel],
        view: view
      };
      localStorage.setItem('trabakutik_filters', JSON.stringify(state));
    } catch (e) {
      // localStorage might be disabled or full; silently continue
    }
  }

  function restoreFiltersFromStorage(){
    try {
      var saved = localStorage.getItem('trabakutik_filters');
      if (!saved) return;
      var state = JSON.parse(saved);

      // Restore activities
      if (state.activities && state.activities.length > 0) {
        activityChips.forEach(function(c){
          c.classList.toggle('active', state.activities.indexOf(c.dataset.activity) !== -1);
        });
      }

      // Restore difficulties
      if (state.difficulties && state.difficulties.length > 0) {
        difficultyChips.forEach(function(c){
          c.classList.toggle('active', state.difficulties.indexOf(c.dataset.difficulty) !== -1);
        });
      }

      // Restore distance range
      if (state.distance && state.distance.length === 2) {
        if (distanceMin) distanceMin.value = state.distance[0];
        if (distanceMax) distanceMax.value = state.distance[1];
        setActiveDistanceChip(null);
      }

      // Restore desnivel range
      if (state.desnivel && state.desnivel.length === 2) {
        if (desnivelMin) desnivelMin.value = state.desnivel[0];
        if (desnivelMax) desnivelMax.value = state.desnivel[1];
      }

      // Restore view preference
      if (state.view && state.view !== 'list') {
        viewBtns.forEach(function(btn){
          btn.classList.toggle('active', btn.dataset.view === state.view);
        });
        if (resultsList) resultsList.hidden = (state.view !== 'list');
        if (mapWrap) mapWrap.hidden = (state.view !== 'map');
        view = state.view;
      }

      return true;
    } catch (e) {
      return false;
    }
  }

  function resetFilters(){
    activityChips.forEach(function(c){ c.classList.add('active'); });
    difficultyChips.forEach(function(c){ c.classList.add('active'); });
    setActiveDistanceChip(null);
    if (distanceMin) distanceMin.value = 0;
    if (distanceMax) distanceMax.value = maxDistance;
    if (desnivelMin) desnivelMin.value = 0;
    if (desnivelMax) desnivelMax.value = maxDesnivel;
    view = 'list';
    viewBtns.forEach(function(b){ b.classList.toggle('active', b.dataset.view === 'list'); });
    if (resultsList) resultsList.hidden = false;
    if (mapWrap) mapWrap.hidden = true;
    apply();
    saveFiltersToStorage();
  }
  resetBtns.forEach(function(b){ b.addEventListener('click', resetFilters); });

  activityChips.forEach(function(chip){
    chip.addEventListener('click', function(){ toggleChip(chip, activityChips); });
  });

  difficultyChips.forEach(function(chip){
    chip.addEventListener('click', function(){ toggleChip(chip, difficultyChips); });
  });

  suggestionBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      var type = btn.dataset.suggestion;
      if (type === 'activities') {
        activityChips.forEach(function(c){ c.classList.add('active'); });
      } else if (type === 'difficulties') {
        difficultyChips.forEach(function(c){ c.classList.add('active'); });
      } else if (type === 'distance') {
        if (distanceMin) distanceMin.value = 0;
        if (distanceMax) distanceMax.value = maxDistance;
        setActiveDistanceChip(null);
      } else if (type === 'desnivel') {
        if (desnivelMin) desnivelMin.value = 0;
        if (desnivelMax) desnivelMax.value = maxDesnivel;
      }
      apply();
      if (resultsList) resultsList.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'start' });
    });
  });

  quickBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      var preset = btn.dataset.quickPreset;
      var range = DISTANCE_PRESETS[preset];
      var chip = null;
      distanceChips.forEach(function(c){ if (c.dataset.distancePreset === preset) chip = c; });
      setActiveDistanceChip(chip);
      if (range) {
        distanceMin.value = range[0];
        distanceMax.value = Math.min(range[1], maxDistance);
      }
      apply();
      if (resultsList) resultsList.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'start' });
    });
  });

  // Restore filters from localStorage and apply them
  if (!restoreFiltersFromStorage()) {
    // If no saved filters, just apply defaults
    apply();
  } else {
    // If restored, apply the restored state
    apply();
  }
})();
