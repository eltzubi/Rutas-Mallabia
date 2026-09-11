// Run with node scripts/test_ui.cjs. Executes production JS against generated
// HTML in a minimal DOM/Leaflet test double; does not test browser layout.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const {test} = require('node:test');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
class Element {
  constructor(node, doc) {
    this.tag = node.tag; this.attrs = {...node.attrs}; this.ownerDocument = doc;
    this.listeners = {}; this.style = {setProperty(k,v){this[k]=v;}};
    this.children = (node.children || []).map(c => {
      if(typeof c === 'string') return c;
      const el = new Element(c,doc); el.parentElement = this; return el;
    });
    this.classList = {
      contains: c => this.className.split(/\s+/).includes(c),
      add: c => this.classList.toggle(c,true), remove: c => this.classList.toggle(c,false),
      toggle: (c,on) => {
        const set = new Set(this.className.split(/\s+/).filter(Boolean));
        on = on === undefined ? !set.has(c) : !!on;
        if(on) set.add(c); else set.delete(c);
        this.className = [...set].join(' '); return on;
      }
    };
  }
  get className(){return this.attrs.class || '';}
  set className(v){this.attrs.class=v;}
  get dataset(){return Object.fromEntries(Object.entries(this.attrs).filter(([k])=>k.startsWith('data-')).map(([k,v])=>[k.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase()),v]));}
  get textContent(){return this.children.map(c=>typeof c==='string'?c:c.textContent).join('');}
  set textContent(v){this.children=[String(v)];}
  get innerText(){return this.textContent;}
  set innerHTML(v){this.textContent=v;}
  get outerHTML(){return `<${this.tag}>${this.textContent}</${this.tag}>`;}
  get hidden(){return this.hasAttribute('hidden');}
  set hidden(v){if(v)this.setAttribute('hidden','');else this.removeAttribute('hidden');}
  get lang(){return this.attrs.lang;}
  get hreflang(){return this.attrs.hreflang;}
  get value(){return this.attrs.value || '';}
  set value(v){this.attrs.value=String(v);}
  hasAttribute(k){return k in this.attrs;}
  getAttribute(k){return this.attrs[k] ?? null;}
  setAttribute(k,v){this.attrs[k]=String(v);}
  removeAttribute(k){delete this.attrs[k];}
  matches(selector){return selector.split(/,\s*/).some(s=>{
    s=s.trim();
    if(s.includes(' ')) {const parts=s.split(/\s+/);return this.matches(parts.pop()) && !!this.parentElement?.closest(parts.join(' '));}
    let valid=true;
    s=s.replace(/:not\(([^)]+)\)/g,(_,q)=>{if(this.matches(q))valid=false;return '';});
    s=s.replace(/\[([^=\]]+)(?:="([^"]*)")?\]/g,(_,k,v)=>{if(!this.hasAttribute(k)||(v!==undefined&&this.getAttribute(k)!==v))valid=false;return '';});
    s=s.replace(/([.#])([\w-]+)/g,(_,kind,key)=>{if(kind==='.'?!this.classList.contains(key):this.attrs.id!==key)valid=false;return '';});
    return valid && (!s || s===this.tag);
  });}
  querySelectorAll(s){return this.children.flatMap(c=>typeof c==='string'?[]:[...(c.matches(s)?[c]:[]),...c.querySelectorAll(s)]);}
  querySelector(s){return this.querySelectorAll(s)[0] || null;}
  closest(s){return this.matches(s)?this:this.parentElement?.closest(s)||null;}
  addEventListener(t,fn){(this.listeners[t] ||= []).push(fn);}
  removeEventListener(t,fn){this.listeners[t]=(this.listeners[t]||[]).filter(f=>f!==fn);}
  dispatchEvent(e){e.target ||= this; e.preventDefault ||= ()=>{};e.stopPropagation ||= ()=>{};(this.listeners[e.type]||[]).slice().forEach(fn=>fn(e));}
  click(){this.dispatchEvent({type:'click'});}
  focus(){this.ownerDocument.activeElement=this;}
  contains(el){return el===this || this.children.some(c=>typeof c!=='string'&&c.contains(el));}
  appendChild(el){if(el.parentElement)el.remove();el.parentElement=this;this.children.push(el);return el;}
  remove(){this.parentElement.children=this.parentElement.children.filter(c=>c!==this);}
  getBoundingClientRect(){return {top:0,width:800,height:200};}
  scrollIntoView(){}
  reset(){}
  showModal(){this.open=true;}
  close(){this.open=false;this.dispatchEvent({type:'close'});}
}
const fixtures = new Map();
function env(page='index.html', storage=new Map()) {
  if(!fixtures.has(page)) fixtures.set(page, JSON.parse(execFileSync('python3',[path.join(__dirname,'check_site.py'),'--fixture',page],{maxBuffer:8e6})));
  const doc=new Element(fixtures.get(page));
  function attach(el){el.ownerDocument=doc;el.children.filter(c=>typeof c!=='string').forEach(attach);} attach(doc);
  doc.documentElement=doc.querySelector('html'); doc.documentElement.clientWidth=1348;
  doc.body=doc.querySelector('body'); doc.activeElement=doc.body;
  doc.getElementById=id=>doc.querySelector('#'+id);
  doc.createElement=tag=>new Element({tag,attrs:{},children:[]},doc);
  const timers=new Map(); let timerId=0;
  const win=new Element({tag:'window',attrs:{},children:[]},doc);
  Object.assign(win,{document:doc,scrollY:0,pageYOffset:0,innerHeight:800,scrollTo(){},matchMedia:()=>({matches:false}),location:{reload(){win.reloaded=true;}}});
  const maps=[],lines=[],errors=[];
  const L={
    map(el){const m={el,on(){return this;},getContainer(){return el;},invalidateSize(){},fitBounds(){},flyToBounds(){},removeLayer(){},remove(){this.removed=true;}};maps.push(m);return m;},
    tileLayer(){return {addTo(){return this;}};},
    polyline(points,style){const line={points,style:{...style},events:{},path:doc.createElement('path'),addTo(m){m.el.appendChild(this.path);return this;},getElement(){return this.path;},getBounds(){return {extend(){return this;}};},setStyle(s){Object.assign(this.style,s);},on(t,fn){this.events[t]=fn;return this;}};lines.push(line);return line;},
    marker(){return {addTo(){return this;}};},divIcon:o=>o,DomEvent:{stopPropagation(){}}
  };
  const context=vm.createContext({window:win,document:doc,L,AbortController,
    localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
    CustomEvent:class {constructor(type,options){this.type=type;Object.assign(this,options);}},
    FormData:class {constructor(form){this.form=form;}},
    getComputedStyle:()=>({getPropertyValue:()=>''}),requestAnimationFrame:fn=>fn(),
    setTimeout:(fn,ms)=>{timers.set(++timerId,{fn,ms});return timerId;},clearTimeout:id=>timers.delete(id),
    console:{error:(...args)=>errors.push(args)},
    fetch:async()=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,'data/trailhead.json'),'utf8'))})
  });
  win.console=context.console;
  return {doc,win,context,storage,timers,maps,lines,errors,
    run(file){vm.runInContext(fs.readFileSync(path.join(root,'src/js',file),'utf8'),context,{filename:file});},
    one:s=>doc.querySelector(s),all:s=>doc.querySelectorAll(s)};
}
const settle=async()=>{for(let i=0;i<15;i++)await Promise.resolve();};
const visible=e=>e.all('.route-card').filter(c=>!c.classList.contains('is-hidden'));
const totalRoutes=e=>e.all('.route-card').length;
const activityRoutes=(e,activity)=>e.all('.route-card').filter(c=>c.dataset.activity.split(',').includes(activity)).length;
const shortActivityRoutes=(e,activity)=>e.all('.route-card').filter(c=>c.dataset.activity.split(',').includes(activity)&&Number(c.dataset.distanceKm)<=10).length;

test('exclusive filters persist across languages and list/map',()=>{
  const e=env();e.run('filters.js');assert.equal(visible(e).length,totalRoutes(e));
  e.one('.activity-chip[data-activity="bici"]').click();assert.equal(visible(e).length,activityRoutes(e,'bici'));
  assert.equal(e.all('.activity-chip.active').length,e.all('.activity-filter').length);
  e.one('[data-distance-preset="larga"]').click();
  e.one('#difficultySelect').value='dificil';e.one('#difficultySelect').dispatchEvent({type:'change'});
  e.one('#elevationSelect').value='high';e.one('#elevationSelect').dispatchEvent({type:'change'});
  const selected=Array.from(e.win.trabakutikVisibleRoutes);assert(selected.length>0);
  e.one('[data-view="map"]').click();const eu=env('index.eu.html',e.storage);eu.run('filters.js');
  assert.deepEqual(Array.from(eu.win.trabakutikVisibleRoutes),selected);
  assert.match(eu.one('[data-route-totals]').textContent,/ibilbide/);
  assert.equal(eu.one('#difficultySelect').value,'dificil');assert.equal(eu.one('#elevationSelect').value,'high');
  assert.equal(eu.one('[data-view="map"]').getAttribute('aria-pressed'),'true');
  eu.one('.activity-chip[data-activity="all"]').click();
  eu.one('[data-distance-preset="all"]').click();
  eu.one('#difficultySelect').value='all';eu.one('#difficultySelect').dispatchEvent({type:'change'});
  eu.one('#elevationSelect').value='all';eu.one('#elevationSelect').dispatchEvent({type:'change'});
  assert.equal(visible(eu).length,totalRoutes(eu));
  assert.equal(eu.one('#routeMapWrap').hidden,false);
});
test('empty-result recovery finds results while keeping activity',()=>{
  const e=env();e.run('filters.js');e.one('.activity-chip[data-activity="bici"]').click();
  e.one('#difficultySelect').value='dificil';e.one('#difficultySelect').dispatchEvent({type:'change'});
  e.one('[data-distance-preset="corto"]').click();assert.equal(visible(e).length,0);
  assert.equal(e.one('#recoverFilters').textContent,'Ampliar distancia');
  e.one('#recoverFilters').click();assert(visible(e).length>0);
  assert.equal(e.one('.activity-chip[data-activity="bici"]').getAttribute('aria-pressed'),'true');
});
test('invalid storage is safe; old preferences migrate',()=>{
  for(const value of ['null','{broken',JSON.stringify({activities:['unknown'],view:'unknown'})]){
    const e=env('index.html',new Map([['trabakutik_filters',value]]));e.run('filters.js');assert.equal(visible(e).length,totalRoutes(e));
  }
  const e=env('index.html',new Map([['trabakutik_filters',JSON.stringify({activities:['bici'],distancePreset:'media1',view:'map'})]]));e.run('filters.js');
  assert(visible(e).length>0);assert(visible(e).every(c=>Number(c.dataset.distanceKm)>10&&Number(c.dataset.distanceKm)<=20));
  assert.equal(e.one('#routeMapWrap').hidden,false);
});
test('mobile dialog reuses controls and reset keeps activity',()=>{
  const e=env();let changed;const media={matches:true,addEventListener(t,fn){changed=fn;}};
  e.win.matchMedia=()=>media;e.run('filters.js');
  assert.equal(e.one('#filterControls').parentElement,e.one('#mobileFilters'));
  e.one('.activity-chip[data-activity="bici"]').click();e.one('#openFilters').click();assert.equal(e.one('#filterDialog').open,true);
  e.one('[data-distance-preset="corto"]').click();
  const shortBici=shortActivityRoutes(e,'bici');
  assert.equal(e.one('#showResults').textContent,shortBici===1?'Ver 1 ruta':`Ver ${shortBici} rutas`);
  e.one('[data-extra-reset]').click();assert.equal(visible(e).length,activityRoutes(e,'bici'));
  e.one('#showResults').click();assert.equal(e.one('#filterDialog').open,false);assert.equal(e.doc.activeElement,e.one('#openFilters'));
  media.matches=false;changed();assert.equal(e.one('#filterControls').parentElement,e.one('#desktopFilters'));
  assert.equal(e.all('#filterControls').length,1);
});
test('map catches filters loaded earlier; keyboard opens/closes and hidden routes leave tab order',async()=>{
  const e=env();e.run('filters.js');e.one('.activity-chip[data-activity="bici"]').click();
  e.run('map.js');await settle();assert.equal(e.errors.length,0);assert.equal(e.lines.length,totalRoutes(e));
  assert.equal(e.lines.filter(l=>l.path.getAttribute('tabindex')==='0').length,activityRoutes(e,'bici'));
  const line=e.lines.find(l=>l.path.getAttribute('tabindex')==='0');line.path.focus();
  line.path.dispatchEvent({type:'keydown',key:'Enter'});
  const panel=e.one('.route-info-panel');assert.equal(panel.hidden,false);
  assert.equal(line.path.getAttribute('aria-pressed'),'true');assert.equal(e.doc.activeElement,e.one('.route-info-panel-close'));
  panel.dispatchEvent({type:'keydown',key:'Escape'});assert.equal(panel.hidden,true);assert.equal(e.doc.activeElement,line.path);
  e.one('[data-distance-preset="corto"]').click();assert.equal(e.lines.filter(l=>l.path.getAttribute('tabindex')==='0').length,shortActivityRoutes(e,'bici'));
  e.one('[data-distance-preset="all"]').click();assert.equal(e.lines.filter(l=>l.path.getAttribute('tabindex')==='0').length,activityRoutes(e,'bici'));
  const layers=e.one('.map-layers-btn');layers.click();assert.equal(layers.getAttribute('aria-pressed'),'true');
  e.one('.map-expand-btn').click();assert.equal(e.one('[data-map-src]').parentElement.style['--map-viewport-width'],'1348px');
});
test('map also catches filters changed while its request is pending',async()=>{
  const e=env();let release;e.context.fetch=()=>new Promise(r=>{release=r;});e.run('map.js');e.run('filters.js');
  e.one('.activity-chip[data-activity="bici"]').click();
  release({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.join(root,'data/trailhead.json')))});await settle();
  assert.equal(e.errors.length,0);assert.equal(e.lines.filter(l=>l.path.getAttribute('tabindex')==='0').length,activityRoutes(e,'bici'));
});
test('HTTP, invalid JSON, invalid data and stalled map requests display an error and can retry',async()=>{
  for(const failure of ['http','json','data','timeout']){
    const e=env();const success=e.context.fetch;
    e.context.fetch=()=>failure==='timeout'?new Promise(()=>{}):Promise.resolve({ok:failure!=='http',status:500,json:async()=>{if(failure==='json')throw Error('bad JSON');return {};}});
    e.run('map.js');if(failure==='timeout')[...e.timers.values()].find(t=>t.ms===15000).fn();await settle();
    assert.match(e.one('[data-map-src]').querySelector('[role="status"]').textContent,/No se ha podido cargar/);assert(e.one('.map-retry'));assert.equal(e.one('.map-expand-btn').hidden,true);
    e.context.fetch=success;e.one('.map-retry').click();await settle();
    assert.equal(e.one('.map-retry'),null);assert.equal(e.lines.length,totalRoutes(e));
    assert.equal(e.all('.map-layers-btn').length,1);assert.equal(e.one('.map-expand-btn').hidden,false);
  }
});
test('missing Leaflet provides a localized reload action',()=>{
  const e=env('index.eu.html');delete e.context.L;e.run('map.js');
  assert.match(e.one('[data-map-src]').querySelector('[role="status"]').textContent,/Ezin izan da mapa/);
  e.one('.map-retry').click();assert.equal(e.win.reloaded,true);
});
test('theme and report runtime messages use the page language without sending real reports',async()=>{
  const e=env('trabakuamallabia.eu.html');e.run('app.js');const theme=e.one('#themeToggle');
  theme.click();assert.match(theme.getAttribute('aria-label'),/^Aldatu gai/);
  e.one('#reportTrigger').click();assert.match(e.one('input[name="_subject"]').value,/^Ibilbideko gorabehera:/);
  const form=e.one('#reportForm');let release;e.context.fetch=()=>new Promise(r=>{release=r;});
  form.dispatchEvent({type:'submit'});assert.equal(e.one('#reportStatus').textContent,'Bidaltzen…');
  release({ok:true});await settle();assert.equal(e.one('#reportStatus').textContent,form.dataset.success);
  e.context.fetch=async()=>({ok:false});form.dispatchEvent({type:'submit'});await settle();
  assert.equal(e.one('#reportStatus').textContent,form.dataset.error);assert.equal(e.one('.report-submit').disabled,false);
});
