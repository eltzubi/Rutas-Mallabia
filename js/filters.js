// One filter state feeds the list, map, result count and mobile dialog.
(function(){
  var finder = document.querySelector('.finder');
  if (!finder) return;
  var cards = Array.from(finder.querySelectorAll('.route-card[data-activity]'));
  var activityButtons = Array.from(finder.querySelectorAll('.activity-chip'));
  var distanceButtons = Array.from(finder.querySelectorAll('.distance-chip'));
  var viewButtons = Array.from(finder.querySelectorAll('.view-toggle-btn'));
  var difficulty = document.getElementById('difficultySelect');
  var elevation = document.getElementById('elevationSelect');
  var results = document.getElementById('routeResults');
  var mapWrap = document.getElementById('routeMapWrap');
  var dialog = document.getElementById('filterDialog');
  var openButton = document.getElementById('openFilters');
  var controls = document.getElementById('filterControls');
  var advanced = document.getElementById('advancedFilters');
  var empty = document.getElementById('filterEmpty');
  var recover = document.getElementById('recoverFilters');
  if (!cards.length || !difficulty || !elevation) return;
  var eu = document.documentElement.lang === 'eu';
  var words = eu ? {
    one: 'ibilbide', many: 'ibilbide', show: function(n){ return n + ' ibilbide ikusi'; },
    distance: 'Distantzia zabaldu', difficulty: 'Zailtasun guztiak ikusi',
    elevation: 'Desnibel guztiak ikusi', extra: 'Distantzia, zailtasuna eta desnibela kendu',
    all: 'Jarduera guztiak ikusi'
  } : {
    one: 'ruta', many: 'rutas', show: function(n){ return 'Ver ' + n + (n === 1 ? ' ruta' : ' rutas'); },
    distance: 'Ampliar distancia', difficulty: 'Ver todas las dificultades',
    elevation: 'Ver todos los desniveles', extra: 'Quitar distancia, dificultad y desnivel',
    all: 'Ver todas las actividades'
  };
  var defaults = {activity:'all', distance:'all', difficulty:'all', elevation:'all', view:'list'};
  var state = Object.assign({}, defaults);
  var allowed = {
    activity:['all','senderismo','bici'], distance:['all','corto','media1','media2','larga'],
    difficulty:['all','facil','media','dificil'], elevation:['all','low','medium','high'], view:['list','map']
  };
  try {
    var saved = JSON.parse(localStorage.getItem('trabakutik_filters'));
    if (saved && typeof saved === 'object') {
      if (saved.version !== 2) {
        saved.activity = Array.isArray(saved.activities) && saved.activities.length === 1 ? saved.activities[0] : 'all';
        saved.difficulty = Array.isArray(saved.difficulties) && saved.difficulties.length === 1 ? saved.difficulties[0] : 'all';
        saved.distance = saved.distancePreset || 'all';
      }
      Object.keys(defaults).forEach(function(k){ if (allowed[k].indexOf(saved[k]) !== -1) state[k] = saved[k]; });
    }
  } catch (_) { /* Storage may be unavailable or malformed. */ }

  function matches(card, s){
    var km = Number(card.dataset.distanceKm), gain = Number(card.dataset.desnivelM);
    var distanceOK = s.distance === 'all' ||
      (s.distance === 'corto' && km <= 10) ||
      (s.distance === 'media1' && km > 10 && km <= 20) ||
      (s.distance === 'media2' && km > 20 && km <= 30) ||
      (s.distance === 'larga' && km > 30);
    var elevationOK = s.elevation === 'all' ||
      (s.elevation === 'low' && gain <= 500) ||
      (s.elevation === 'medium' && gain > 500 && gain <= 1000) ||
      (s.elevation === 'high' && gain > 1000);
    return (s.activity === 'all' || card.dataset.activity.split(',').indexOf(s.activity) !== -1) &&
      (s.difficulty === 'all' || card.dataset.difficulty === s.difficulty) && distanceOK && elevationOK;
  }
  function selectedLabel(buttons, key, value){
    var button = buttons.find(function(b){ return b.dataset[key] === value; });
    return button ? button.textContent.trim() : '';
  }
  function optionLabel(select){
    var option = select.querySelector('option[value="' + select.value + '"]');
    return option ? option.textContent.trim() : '';
  }
  function paintButtons(buttons, key, value){
    buttons.forEach(function(b){
      var on = b.dataset[key] === value;
      b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on));
    });
  }
  function badge(id, n){
    var el = document.getElementById(id); el.textContent = n ? ' (' + n + ')' : ''; el.hidden = !n;
  }
  var recoveryState = null;
  function apply(){
    difficulty.value = state.difficulty; elevation.value = state.elevation;
    paintButtons(activityButtons, 'activity', state.activity);
    paintButtons(distanceButtons, 'distancePreset', state.distance);
    paintButtons(viewButtons, 'view', state.view);
    var visible = [];
    cards.forEach(function(card){
      var show = matches(card, state); card.classList.toggle('is-hidden', !show);
      if (show) visible.push(card.getAttribute('href').replace(/\.eu\.html$/, '.html'));
    });
    results.hidden = state.view !== 'list'; mapWrap.hidden = state.view !== 'map';
    var n = visible.length;
    document.getElementById('resultCount').textContent = n + ' ' + (n === 1 ? words.one : words.many);
    document.getElementById('showResults').textContent = words.show(n);
    var extraCount = ['distance','difficulty','elevation'].filter(function(k){return state[k] !== 'all';}).length;
    badge('filterBadge', extraCount);
    badge('advancedBadge', Number(state.difficulty !== 'all') + Number(state.elevation !== 'all'));
    var labels = [];
    if (state.activity !== 'all') labels.push(selectedLabel(activityButtons,'activity',state.activity));
    if (state.distance !== 'all') labels.push(selectedLabel(distanceButtons,'distancePreset',state.distance));
    if (state.difficulty !== 'all') labels.push(optionLabel(difficulty));
    if (state.elevation !== 'all') labels.push((eu ? 'Desnibela: ' : 'Desnivel: ') + optionLabel(elevation));
    var summary = document.getElementById('activeFilters');
    summary.textContent = labels.join(' · '); summary.hidden = !labels.length;
    finder.querySelectorAll('[data-filter-reset]').forEach(function(b){b.hidden = !labels.length;});
    finder.querySelectorAll('[data-extra-reset]').forEach(function(b){b.disabled = !labels.length;});
    empty.hidden = n !== 0; empty.classList.toggle('visible', n === 0);
    if (!n) {
      // Offer one relaxation that actually yields results. Keep the selected
      // activity unless there are no routes at all for that activity.
      recoveryState = null;
      ['distance','difficulty','elevation'].some(function(k){
        if (state[k] === 'all') return false;
        var candidate = Object.assign({}, state); candidate[k] = 'all';
        if (!cards.some(function(c){return matches(c,candidate);})) return false;
        recoveryState = candidate; recover.textContent = words[k]; return true;
      });
      if (!recoveryState) {
        recoveryState = Object.assign({}, defaults, {activity:state.activity, view:state.view});
        recover.textContent = words.extra;
        if (!cards.some(function(c){return matches(c,recoveryState);})) {
          recoveryState.activity = 'all'; recover.textContent = words.all;
        }
      }
    }
    window.trabakutikVisibleRoutes = visible.slice();
    document.dispatchEvent(new CustomEvent('routefilters:apply', {detail:{visibleHrefs:visible}}));
    try { localStorage.setItem('trabakutik_filters', JSON.stringify(Object.assign({version:2},state))); } catch (_) {}
  }
  activityButtons.forEach(function(b){b.addEventListener('click',function(){state.activity=b.dataset.activity;apply();});});
  distanceButtons.forEach(function(b){b.addEventListener('click',function(){state.distance=b.dataset.distancePreset;apply();});});
  difficulty.addEventListener('change',function(){state.difficulty=difficulty.value;apply();});
  elevation.addEventListener('change',function(){state.elevation=elevation.value;apply();});
  viewButtons.forEach(function(b){b.addEventListener('click',function(){state.view=b.dataset.view;apply();});});
  finder.querySelectorAll('[data-filter-reset]').forEach(function(b){b.addEventListener('click',function(){state=Object.assign({},defaults,{view:state.view});apply();});});
  finder.querySelectorAll('[data-extra-reset]').forEach(function(b){b.addEventListener('click',function(){state=Object.assign({},defaults,{view:state.view,activity:state.activity});apply();});});
  recover.addEventListener('click',function(){if(recoveryState){state=recoveryState;apply();}});

  // The same controls move into a native modal on small screens. Native
  // dialog supplies focus trapping, Escape, and an inert page behind it.
  var mobile = window.matchMedia('(max-width: 659px)');
  function placeControls(){
    if (dialog.open) dialog.close();
    document.getElementById(mobile.matches ? 'mobileFilters' : 'desktopFilters').appendChild(controls);
    advanced.open = mobile.matches || state.difficulty !== 'all' || state.elevation !== 'all';
  }
  openButton.addEventListener('click',function(){dialog.showModal();document.body.classList.add('filters-open');});
  function close(){dialog.close();}
  document.getElementById('closeFilters').addEventListener('click',close);
  document.getElementById('showResults').addEventListener('click',close);
  dialog.addEventListener('close',function(){document.body.classList.remove('filters-open');openButton.focus({preventScroll:true});});
  dialog.addEventListener('click',function(e){
    var r=dialog.getBoundingClientRect();
    if(e.target===dialog && (e.clientX<r.left || e.clientX>r.right || e.clientY<r.top || e.clientY>r.bottom))close();
  });
  if (mobile.addEventListener) mobile.addEventListener('change',placeControls);
  else if (mobile.addListener) mobile.addListener(placeControls);
  placeControls(); apply();
})();
