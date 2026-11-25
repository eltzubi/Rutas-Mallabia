#!/usr/bin/env python3
"""Build labeled route-card maps from published tracks, route waypoints and OpenFreeMap vector tiles."""
import concurrent.futures as cf
import gzip, html, json, math, re, subprocess, sys, unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from make_places import load_osm, fold, MAX_M, kind, names
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'.cache-card-tiles';CACHE.mkdir(exist_ok=True)
W,H=640,400
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD=ImageFont.truetype(FONT.replace('.ttf','-Bold.ttf'),15)
SMALL=ImageFont.truetype(FONT,11)
def read(p):return json.loads(p.read_text())
def merc(lat,lon):return ((lon+180)/360,(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2)
def var(b,i):
 v=k=0
 while True:
  c=b[i];i+=1;v|=(c&127)<<k
  if c<128:return v,i
  k+=7
def fields(b):
 i=0
 while i<len(b):
  t,i=var(b,i);f,w=t>>3,t&7
  if w==0:v,i=var(b,i)
  elif w==2:n,i=var(b,i);v=b[i:i+n];i+=n
  elif w in (1,5):n=8 if w==1 else 4;v=b[i:i+n];i+=n
  else:raise ValueError(w)
  yield f,v
def packed(b):
 i=0
 while i<len(b):
  v,i=var(b,i);yield v
def geometry(b):
 a=list(packed(b));i=x=y=0;paths=[]
 while i<len(a):
  cmd=a[i]&7;n=a[i]>>3;i+=1
  if cmd==7:continue
  if cmd not in (1,2):raise ValueError(cmd)
  for _ in range(n):
   dx,dy=a[i:i+2];i+=2;x+=(dx>>1)^-(dx&1);y+=(dy>>1)^-(dy&1)
   if cmd==1:paths.append([])
   paths[-1].append((x,y))
 return paths
def decode(b):
 b=gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
 out=[]
 for k,layer in fields(b):
  if k!=3:continue
  fs=list(fields(layer));name=next(v.decode() for k,v in fs if k==1);ext=next((v for k,v in fs if k==5),4096);keys=[v.decode() for k,v in fs if k==3];vals=[next((a.decode() if isinstance(a,bytes) and i==1 else a for i,a in fields(v)),None) for k,v in fs if k==4]
  if name not in ('landuse','landcover','park','water','waterway','transportation','place'):continue
  for k,f in fs:
   if k!=2:continue
   d=dict(fields(f));tags=list(packed(d.get(2,b'')));tags={keys[a]:vals[b] for a,b in zip(tags[::2],tags[1::2])}
   if 4 in d:out.append((name,tags,d.get(3),ext,geometry(d[4])))
 return out
def tile(t):
 z,x,y=t;p=CACHE/f'{z}-{x}-{y}.pbf'
 if not p.exists():
  subprocess.run(['curl','-fLs','--retry','2','--max-time','20',URL.format(z=z,x=x,y=y),'-o',str(p)],check=True)
 return t,decode(p.read_bytes())
def frame(tracks):
 pts=[merc(*p[:2]) for track in tracks for p in track];lo=[min(p[i] for p in pts) for i in (0,1)];hi=[max(p[i] for p in pts) for i in (0,1)]
 s=min(516/max(hi[0]-lo[0],1e-10),300/max(hi[1]-lo[1],1e-10));x0=(lo[0]+hi[0])/2-W/2/s;y0=(lo[1]+hi[1])/2-H/2/s
 z=max(9,min(14,round(math.log2(s/256))));n=2**z;tiles=[(z,x,y) for x in range(int(x0*n),int((x0+W/s)*n)+1) for y in range(int(y0*n),int((y0+H/s)*n)+1)]
 return s,x0,y0,tiles
def short(s):
 s=re.sub(r'^Humedal de ', '',s,flags=re.I);s=re.sub(r'^Acceso al hayedo de ', '',s,flags=re.I);s=re.sub(r'^Cascada de ', '',s,flags=re.I)
 return s
def canonical(s):
 f=fold(s)
 if f in {'arietxu','aretxu','areatxua','aretxua','areatsu','ariatzu','arietzu'}:return 'Arietzu'
 if f=='zengotitagana':return 'Zengotitagane'
 if f=='santamarinazar':return 'Santamañazar'
 return s
def route_info(slug):
 r=read(ROOT/'data'/f'{slug}.json');tracks=[t['points'] for t in r['tracks'] if t.get('points')]
 text=(ROOT/'src'/f'{slug}_tail.html').read_text()
 legend={}
 for i,n in re.findall(r'<span class="num">(\d+)</span>([^<]+)</span>',text):legend.setdefault(int(i),html.unescape(n).strip())
 # Numbered points are paired only by their documented index.
 labels=[(short(legend[i]),q,0) for i,q in enumerate(r.get('waypoints',[]),1) if i in legend and len(q)>=2]
 start=re.search(r'data-marker-title="([^"]+)"',text)
 if start:
  title=html.unescape(start[1]).split(' (')[0].strip()
  if title and len(title)<=40:labels.insert(0,(title,tracks[0][0],0))
 ends={'lekeitio':'Lekeitio','trabakuadeba':'Deba','trabakuaondarroa':'Ondarroa'}
 if slug in ends:labels.insert(1,(ends[slug],tracks[-1][-1],0))
 if slug=='markinaurjauziak':labels.insert(1,('Trabakua',tracks[-1][-1],0))
 return tracks,labels
def rect_overlap(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
def render(slug,tracks,labels,frame,activity):
 s,x0,y0,tiles=frame
 def project(q):return ((q[0]-x0)*s,(q[1]-y0)*s)
 def coord(q):return project(merc(*q[:2]))
 paths=[[coord(p) for p in tr] for tr in tracks]
 features=[]
 for z,x,y in tiles:
  n=2**z
  for name,t,k,ext,geom in TILES[z,x,y]:
   features.append((name,t,k,[[project(((x+a/ext)/n,(y+b/ext)/n)) for a,b in path] for path in geom]))
 im=Image.new('RGB',(W,H),'#f4f2e9');d=ImageDraw.Draw(im)
 for layer in ['landuse','landcover','park','water','waterway']:
  for name,t,k,ps in features:
   if name!=layer:continue
   c=t.get('class','')
   if layer=='landcover':color={'wood':'#b9d9aa','grass':'#d7e9c9','farmland':'#edf0d9','wetland':'#c8e0d9'}.get(c)
   elif layer=='landuse':color={'residential':'#e7e1dc','industrial':'#e1d9df','commercial':'#e6dce1','farmland':'#edead6'}.get(c)
   elif layer=='park':color='#d0e6c3'
   else:color='#a7cde3'
   if color:
    for path in ps:
     if k==3 and len(path)>=3:d.polygon(path,fill=color)
     elif k==2 and len(path)>=2:d.line(path,fill=color,width=2)
 for classes,width,color in [(['path','track','service'],1,'#d7d1c5'),(['minor','tertiary'],2,'#fff'),(['secondary'],3,'#f8e7a7'),(['primary','trunk'],4,'#f1bda5'),(['motorway'],5,'#e6a1a8')]:
  for name,t,k,ps in features:
   if name=='transportation' and t.get('class') in classes and k==2:
    for path in ps:
     if len(path)>=2:d.line(path,fill=color,width=width)
 color='#A75C00' if activity=='bici' else '#3f6b14'
 for path in paths:
  d.line(path,fill='white',width=10,joint='curve');d.line(path,fill=color,width=5,joint='curve')
 # Only add OSM points that match a real track, with thresholds by feature type.
 flat=[q for p in paths for q in p];lat0=tracks[0][0][0];mpp=40075016.686*math.cos(math.radians(lat0))/s
 for lat,lon,maxm,ns in OSM:
  x,y=coord((lat,lon))
  if not (10<x<W-10 and 10<y<H-20):continue
  distance=min(math.hypot(x-a,y-b) for a,b in flat)*mpp
  if distance<=maxm:
   n=ns[0]
   if len(n)<=45:labels.append((n,(lat,lon),1+distance/maxm))
 used=[];seen=set();markers=[];placed=[]
 for name,q,priority in sorted(labels,key=lambda a:a[2]):
  name=canonical(name);key=fold(name)
  if key in seen or not name:continue
  x,y=coord(q)
  if not (5<x<W-5 and 5<y<H-12):continue
  if any(math.hypot(x-a,y-b)<9 for a,b in markers):continue
  opts=[(11,-12,'lm'),(-11,-12,'rm'),(11,12,'lm'),(-11,12,'rm'),(0,-13,'ms'),(0,24,'ms'),(13,0,'lm'),(-13,0,'rm')]
  possible=[]
  for dx,dy,a in opts:
   box=d.textbbox((x+dx,y+dy),name,font=BOLD,anchor=a,stroke_width=2);l,t,r,b=box;pad=(l-3,t-2,r+3,b+2)
   if l<4 or t<4 or r>W-4 or b>H-17 or any(rect_overlap(pad,old) for old in used):continue
   if any(l-4<px<r+4 and t-4<py<b+4 for px,py in markers):continue
   hits=sum(l<px<r and t<py<b for px,py in flat[::3])
   # Prefer labels outside the track.
   possible.append((hits,dx,dy,a,pad))
  if not possible:continue
  _,dx,dy,a,box=min(possible,key=lambda a:a[0]);used.append(box);seen.add(key);markers.append((x,y));placed.append(name)
  d.ellipse((x-5,y-5,x+5,y+5),fill=color,outline='white',width=2);d.text((x+dx,y+dy),name,font=BOLD,anchor=a,fill='#302c26',stroke_width=2,stroke_fill='white')
 for name,t,k,ps in features:
  if name!='place' or k!=1 or t.get('class') not in ['town','city','village']:continue
  n=t.get('name:eu') or t.get('name')
  if not n or fold(canonical(n)) in seen:continue
  n=canonical(n)
  for path in ps:
   x,y=path[0];box=d.textbbox((x,y),n,font=SMALL,anchor='mm',stroke_width=1);l,t,rr,b=box
   if l<5 or rr>635 or t<5 or b>380 or any(rect_overlap(box,o) for o in used) or any(l-2<px<rr+2 and t-2<py<b+2 for px,py in flat[::3]):continue
   d.text((x,y),n,font=SMALL,anchor='mm',fill='#666',stroke_width=1,stroke_fill='white');used.append(box);seen.add(fold(n))
 d.text((635,393),'© OpenStreetMap contributors · OpenFreeMap',font=SMALL,anchor='rs',fill='#555',stroke_width=1,stroke_fill='white')
 im.save(ROOT/'img'/f'mapa-{slug}.webp',quality=84,method=6)
 return placed
if __name__=='__main__':
 URL=read(Path(sys.argv[1]))['tiles'][0];OSM=load_osm()
 home=(ROOT/'src/mallabia_tail.html').read_text()
 routes=[]
 for t in read(ROOT/'data/trailhead.json')['tracks']:
  slug=t['href'].removesuffix('.html');tracks,labels=route_info(slug);f=frame(tracks);act=re.search(r'href="'+re.escape(slug)+r'\.html" data-activity="([^"]+)"',home)
  routes.append((slug,tracks,labels,f,act[1].split(',')[0] if act else 'senderismo'))
 tiles=set(t for _,_,_,f,_ in routes for t in f[3]);print('Routes',len(routes),'tiles',len(tiles),flush=True)
 TILES={}
 with cf.ThreadPoolExecutor(max_workers=12) as e:
  futures={e.submit(tile,t):t for t in tiles}
  for i,f in enumerate(cf.as_completed(futures),1):
   try:t,decoded=f.result();TILES[t]=decoded
   except Exception as ex:print('tile failed',futures[f],ex,flush=True)
   if i%20==0:print('tiles',i,'/',len(tiles),flush=True)
 report={}
 for a in routes:
  if not all(t in TILES for t in a[3][3]):print('skip missing tiles',a[0],flush=True);continue
  report[a[0]]=render(*a);print(a[0],len(report[a[0]]),', '.join(report[a[0]]),flush=True)
 (ROOT/'map-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
