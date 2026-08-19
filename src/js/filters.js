// Home page: activity chips + distance/elevation range filters.
// Language-independent -- the labels it writes come from the page itself.
(function(){
  var chips = document.querySelectorAll('.activity-chip');
  var panels = document.querySelectorAll('.feat-panel[data-activity]');
  var signs = document.querySelectorAll('.signpost-sign[data-activity]');
  var emptyMsg = document.getElementById('filterEmpty');
  var distanceRange = document.getElementById('distanceRange');
  var desnivelRange = document.getElementById('desnivelRange');
  var distanceVal = document.getElementById('distanceVal');
  var desnivelVal = document.getElementById('desnivelVal');
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

  if (distanceRange) { distanceRange.max = maxDistance; distanceRange.value = maxDistance; }
  if (desnivelRange) { desnivelRange.max = maxDesnivel; desnivelRange.value = maxDesnivel; }

  function apply(){
    var active = Array.prototype.filter.call(chips, function(c){ return c.classList.contains('active'); })
      .map(function(c){ return c.dataset.activity; });
    var maxD = distanceRange ? parseFloat(distanceRange.value) : Infinity;
    var maxE = desnivelRange ? parseFloat(desnivelRange.value) : Infinity;
    if (distanceVal) distanceVal.textContent = (maxD >= maxDistance ? maxDistance + ' km ' + TXT_NO_LIMIT : maxD.toFixed(1).replace('.0','') + ' km ' + TXT_APPROX);
    if (desnivelVal) desnivelVal.textContent = (maxE >= maxDesnivel ? maxDesnivel + ' m ' + TXT_NO_LIMIT : '+' + Math.round(maxE) + ' m ' + TXT_APPROX);

    var anyVisible = false;
    function filterOne(p){
      var km = parseFloat(p.dataset.distanceKm) || 0;
      var m = parseFloat(p.dataset.desnivelM) || 0;
      var show = active.indexOf(p.dataset.activity) !== -1 && km <= maxD && m <= maxE;
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
  if (distanceRange) distanceRange.addEventListener('input', apply);
  if (desnivelRange) desnivelRange.addEventListener('input', apply);

  apply();
})();
