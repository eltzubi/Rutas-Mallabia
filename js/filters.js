// Home page finder: pick an activity, then filter/browse routes as a
// compact list or a map. Language-independent -- the labels it writes
// come from the page itself (data-* attributes carry the per-language text).
(function(){
  var activityBtns = document.querySelectorAll('.activity-big-btn');
  var finderFilters = document.getElementById('finderFilters');
  var difficultyChips = document.querySelectorAll('.difficulty-chip');
  var distanceChips = document.querySelectorAll('.distance-chip');
  var moreFiltersToggle = document.getElementById('moreFiltersToggle');
  var moreFiltersPanel = document.getElementById('moreFiltersPanel');
  var viewBtns = document.querySelectorAll('.view-toggle-btn');
  var resultsList = document.getElementById('routeResults');
  var mapWrap = document.getElementById('routeMapWrap');
  var cards = document.querySelectorAll('.route-card[data-activity]');
  var emptyMsg = document.getElementById('filterEmpty');
  var showAllBtn = document.getElementById('showAllBtn');
  var resultCount = document.getElementById('resultCount');
  var quickBtns = document.querySelectorAll('.quick-help-btn');
  var distanceMin = document.getElementById('distanceRangeMin');
  var distanceMax = document.getElementById('distanceRangeMax');
  var desnivelMin = document.getElementById('desnivelRangeMin');
  var desnivelMax = document.getElementById('desnivelRangeMax');
  var distanceVal = document.getElementById('distanceVal');
  var desnivelVal = document.getElementById('desnivelVal');
  var distanceFill = document.getElementById('distanceFill');
  var desnivelFill = document.getElementById('desnivelFill');
  if (!activityBtns.length || !cards.length) return;

  var INITIAL_COUNT = 6;
  var expanded = false;
  var activeActivity = null; // null = none chosen yet
  var view = 'list';

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
      expanded = false;
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

  viewBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      view = btn.dataset.view;
      viewBtns.forEach(function(b){ b.classList.toggle('active', b === btn); });
      if (resultsList) resultsList.hidden = (view !== 'list');
      if (mapWrap) mapWrap.hidden = (view !== 'map');
    });
  });

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

    var visibleHrefs = [];
    var shown = 0;
    cards.forEach(function(card){
      var km = parseFloat(card.dataset.distanceKm) || 0;
      var m = parseFloat(card.dataset.desnivelM) || 0;
      var activities = card.dataset.activity.split(',');
      var matchesActivity = !activeActivity || activities.indexOf(activeActivity) !== -1;
      var matchesDifficulty = !activeDifficulty.length || activeDifficulty.indexOf(card.dataset.difficulty) !== -1;
      var matches = matchesActivity && matchesDifficulty && km >= minD && km <= maxD && m >= minE && m <= maxE;
      var show = matches && (expanded || shown < INITIAL_COUNT);
      if (matches) {
        shown++;
        visibleHrefs.push(card.getAttribute('href').replace(/\.eu\.html$/, '.html'));
      }
      card.classList.toggle('is-hidden', !show);
    });
    if (emptyMsg) emptyMsg.classList.toggle('visible', shown === 0 && !!activeActivity);
    if (showAllBtn) showAllBtn.hidden = expanded || shown <= INITIAL_COUNT;
    if (resultCount) resultCount.textContent = shown + ' ' + (shown === 1 ? TXT_COUNT_ONE : TXT_COUNT_MANY);
    document.dispatchEvent(new CustomEvent('routefilters:apply', { detail: { visibleHrefs: visibleHrefs } }));
  }

  activityBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      var already = btn.classList.contains('active');
      activeActivity = already ? null : btn.dataset.activity;
      activityBtns.forEach(function(b){ b.classList.toggle('active', b === btn && !already); });
      if (finderFilters) finderFilters.hidden = !activeActivity;
      expanded = false;
      if (activeActivity) apply();
    });
  });

  difficultyChips.forEach(function(chip){
    chip.addEventListener('click', function(){
      chip.classList.toggle('active');
      apply();
    });
  });

  if (showAllBtn) {
    showAllBtn.addEventListener('click', function(){
      expanded = true;
      apply();
    });
  }

  quickBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      if (!activeActivity) {
        activeActivity = null; // both activities allowed
        activityBtns.forEach(function(b){ b.classList.remove('active'); });
      }
      if (finderFilters) finderFilters.hidden = false;
      var preset = btn.dataset.quickPreset;
      var range = DISTANCE_PRESETS[preset];
      var chip = null;
      distanceChips.forEach(function(c){ if (c.dataset.distancePreset === preset) chip = c; });
      setActiveDistanceChip(chip);
      if (range) {
        distanceMin.value = range[0];
        distanceMax.value = Math.min(range[1], maxDistance);
      }
      expanded = false;
      apply();
      if (finderFilters) finderFilters.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  apply();
})();
