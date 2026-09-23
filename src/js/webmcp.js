// --- WebMCP: expose route search to AI agents, when the browser supports it ---
// Experimental W3C API (document.modelContext) -- Chrome Canary only as of
// early 2026, no stable browser support yet. Fully feature-detected: on any
// browser without it this is a silent no-op, nothing else on the page
// depends on it.
(function(){
  if (!('modelContext' in document)) return;
  var cards = document.querySelectorAll('.route-card[data-activity]');
  if (!cards.length) return;

  function routeFromCard(card){
    var nameEl = card.querySelector('.route-card-name');
    return {
      name: nameEl ? nameEl.textContent.trim() : '',
      url: new URL(card.getAttribute('href'), location.href).href,
      distanceKm: parseFloat(card.dataset.distanceKm) || 0,
      elevationGainM: parseInt(card.dataset.desnivelM, 10) || 0,
      difficulty: card.dataset.difficulty,
      activities: card.dataset.activity.split(',')
    };
  }

  document.modelContext.registerTool({
    name: 'search_mallabia_routes',
    description: 'Search the hiking and biking routes around Mallabia (Bizkaia, Spain) documented on trabakutik.com. Every route is personally walked/ridden and GPS-tracked -- distance and elevation gain are real, measured values. Filter by activity, distance range and/or difficulty; omit a filter to leave it unrestricted.',
    inputSchema: {
      type: 'object',
      properties: {
        activity: {
          type: 'string',
          enum: ['senderismo', 'bici'],
          description: '"senderismo" for hiking/trail-running routes, "bici" for mountain-bike/e-bike routes.'
        },
        minDistanceKm: { type: 'number', description: 'Minimum route distance in kilometers.' },
        maxDistanceKm: { type: 'number', description: 'Maximum route distance in kilometers.' },
        difficulty: {
          type: 'string',
          enum: ['facil', 'media', 'dificil'],
          description: 'facil = easy, media = moderate, dificil = hard.'
        }
      }
    },
    async execute(params){
      params = params || {};
      var results = [];
      cards.forEach(function(card){
        var r = routeFromCard(card);
        if (params.activity && r.activities.indexOf(params.activity) === -1) return;
        if (params.difficulty && r.difficulty !== params.difficulty) return;
        if (typeof params.minDistanceKm === 'number' && r.distanceKm < params.minDistanceKm) return;
        if (typeof params.maxDistanceKm === 'number' && r.distanceKm > params.maxDistanceKm) return;
        results.push(r);
      });
      return {
        content: [{ type: 'text', text: JSON.stringify(results) }]
      };
    }
  });

  document.modelContext.registerTool({
    name: 'get_mallabia_route',
    description: 'Look up one specific Mallabia route by name (or part of its name) and return its real distance, elevation gain, difficulty, activity and page URL.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Route name or a distinctive part of it, e.g. "Urko" or "Zengotitagane".' }
      },
      required: ['query']
    },
    async execute(params){
      var q = ((params && params.query) || '').toLowerCase();
      var match = null;
      cards.forEach(function(card){
        if (match || !q) return;
        var nameEl = card.querySelector('.route-card-name');
        if (nameEl && nameEl.textContent.toLowerCase().indexOf(q) !== -1) match = routeFromCard(card);
      });
      return {
        content: [{
          type: 'text',
          text: match ? JSON.stringify(match) : 'No route found matching "' + (params && params.query) + '".'
        }]
      };
    }
  });
})();
