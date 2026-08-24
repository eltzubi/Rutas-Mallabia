// Home page: activity chips + distance/elevation range filters.
// Language-independent -- the labels it writes come from the page itself.
(function(){
  var chips = document.querySelectorAll('.activity-chip');
  var panels = document.querySelectorAll('.feat-panel[data-activity]');
  var signs = document.querySelectorAll('.signpost-sign[data-activity]');
  var emptyMsg = document.getElementById('filterEmpty');
  var distanceMin = document.getElementById('distanceRangeMin');
  var distanceMax = document.getElementById('distanceRangeMax');
  var desnivelMin = document.getElementById('desnivelRangeMin');
  var desnivelMax = document.getElementById('desnivelRangeMax');
  var distanceVal = document.getElementById('distanceVal');
  var desnivelVal = document.getElementById('desnivelVal');
  var distanceFill = document.getElementById('distanceFill');
  var desnivelFill = document.getElementById('desnivelFill');
  if (!chips.length || !panels.length) return;

  // Wording lives in the HTML so each language supplies its own.
  var filters = document.querySelector('.range-filters') || document.body;
  var TXT_NO_LIMIT = filters.dataset.noLimit || '(sin límite)';
  var TXT_APPROX = filters.dataset.approx || 'aprox.';

  function niceCeil(n, step){ return Math.ceil(n / step) * step; }

  var distances = Array.prototype.map.call(panels, function(p){ return parseFloat(p.dataset.distanceKm) || 0; });
  var desniveles = Array.prototype.map.call(panels, function(p){ return parseFloat(p.dataset.desnivelM) || 0; });
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

  // Keeps the two thumbs from crossing, and raises whichever one is being
  // dragged above the other so a click near the middle grabs the right one.
  function linkPair(minEl, maxEl){
    if (!minEl || !maxEl) return;
    function clamp(){
      if (parseFloat(minEl.value) > parseFloat(maxEl.value)) minEl.value = maxEl.value;
    }
    minEl.addEventListener('input', function(){ clamp(); apply(); });
    maxEl.addEventListener('input', function(){
      if (parseFloat(maxEl.value) < parseFloat(minEl.value)) maxEl.value = minEl.value;
      apply();
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
  linkPair(distanceMin, distanceMax);
  linkPair(desnivelMin, desnivelMax);

  function fillPair(minEl, maxEl, fillEl, max){
    if (!minEl || !maxEl || !fillEl || !max) return;
    var loPct = parseFloat(minEl.value) / max * 100;
    var hiPct = parseFloat(maxEl.value) / max * 100;
    fillEl.style.left = loPct + '%';
    fillEl.style.right = (100 - hiPct) + '%';
  }

  function fmtRange(minV, maxV, max, isElevation){
    if (minV <= 0 && maxV >= max) return max + (isElevation ? ' m ' : ' km ') + TXT_NO_LIMIT;
    var fmt = function(n){ return isElevation ? Math.round(n) : n.toFixed(1).replace('.0',''); };
    return fmt(minV) + '–' + fmt(maxV) + (isElevation ? ' m ' : ' km ') + TXT_APPROX;
  }

  function apply(){
    var active = Array.prototype.filter.call(chips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.activity; });
    var minD = distanceMin ? parseFloat(distanceMin.value) : 0;
    var maxD = distanceMax ? parseFloat(distanceMax.value) : Infinity;
    var minE = desnivelMin ? parseFloat(desnivelMin.value) : 0;
    var maxE = desnivelMax ? parseFloat(desnivelMax.value) : Infinity;
    if (distanceVal) distanceVal.textContent = fmtRange(minD, maxD, maxDistance, false);
    if (desnivelVal) desnivelVal.textContent = fmtRange(minE, maxE, maxDesnivel, true);
    fillPair(distanceMin, distanceMax, distanceFill, maxDistance);
    fillPair(desnivelMin, desnivelMax, desnivelFill, maxDesnivel);

    var anyVisible = false;
    function filterOne(p){
      var km = parseFloat(p.dataset.distanceKm) || 0;
      var m = parseFloat(p.dataset.desnivelM) || 0;
      // A route can list more than one activity (comma-separated, e.g. a
      // route done both hiking and by bike) -- show it if any of them is active.
      var activities = p.dataset.activity.split(',');
      var matchesActivity = activities.some(function(a){ return active.indexOf(a) !== -1; });
      var show = matchesActivity && km >= minD && km <= maxD && m >= minE && m <= maxE;
      p.classList.toggle('is-hidden', !show);
      if (show) anyVisible = true;
    }
    panels.forEach(filterOne);
    signs.forEach(filterOne);
    if (emptyMsg) emptyMsg.classList.toggle('visible', !anyVisible);
  }

  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      chip.classList.toggle('active');
      apply();
    });
  });

  apply();
})();
