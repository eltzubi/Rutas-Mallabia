#!/usr/bin/env python3
"""Prepara una ruta nueva a partir de la travesía existente y los textos del autor.
Se ejecuta solo en la rama de Lekeitio. No publica si fallan las verificaciones.
"""
from pathlib import Path
import json, re, html, math, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"src"; DATA=ROOT/"data"; IMG=ROOT/"img"
SLUG="lekeitio"
ES_TITLE="Trabakua, Mendibil, Mallukitoki, Urregarai, Bedartzandi y Lekeitio"
EU_TITLE="Trabakua, Mendibil, Mallukitoki, Urregarai, Bedartzandi eta Lekeitio"
ES_DESC="Travesía a pie desde Trabakua hasta Lekeitio, por Mendibil, el búnker de Mallukitoki, Zapola, Urregarai, Bedartzandi y Amoroto."
EU_DESC="Trabakuatik Lekeitiorako oinezko zeharkaldia, Mendibil, Mallukitokiko bunkerra, Zapola, Urregarai, Bedartzandi eta Amorototik."
assert (SRC/"lekeitio.gpx").is_file()
assert all((IMG/f"lekeitio-{i:02d}.webp").is_file() and (IMG/f"lekeitio-{i:02d}-800.webp").is_file() for i in range(1,26))
def load(p): return (ROOT/p).read_text(encoding="utf8")
def save(p,s):
    f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding="utf8")
def block(s,a,b,new):
    assert a in s and b in s and s.index(a)<s.index(b),(a,b)
    return s[:s.index(a)]+new+"\n\n  "+s[s.index(b):]
def escaped(s): return html.escape(s,quote=True)
def paras(name):
    raw=load(f"docs/borradores/lekeitio.{name}.md").strip().split("\n\n")
    ps=[p.strip().replace("\n"," ") for p in raw if p.strip() and not p.startswith("# ")]
    def fmt(p):
        t=escaped(p)
        return re.sub(r"\*\*(.*?)\*\*",r"<b>\1</b>",t)
    assert len(ps)>=20,(name,len(ps))
    return "\n".join("    <p>"+fmt(p)+"</p>" for p in ps)
def photos():
    rows=[]
    for p in ("lekeitio-fotos-recibidas-05-11.md","lekeitio-fotos-recibidas-05-11-lote-2.md","lekeitio-fotos-recibidas-05-11-lote-3.md"):
        for l in load("docs/borradores/"+p).splitlines():
            m=re.match(r"^\|\s*(\d+)\s*\|\s*(100012\d+\.jpg)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|?$",l)
            if m:rows.append((int(m.group(1)),m.group(2),m.group(3),m.group(4)))
    rows.sort()
    assert len(rows)==25 and [x[0] for x in rows]==list(range(1,26)),rows
    return rows
ROWS=photos()
COVER=23
def image_html(i,alt):
    return (f'<button type="button" class="gallery-item" data-lightbox-src="img/lekeitio-{i:02d}.webp">'
      f'<picture><source srcset="img/lekeitio-{i:02d}-800.webp 800w, img/lekeitio-{i:02d}.webp 1600w" sizes="(min-width:1024px) 520px, (min-width:768px) 350px, 45vw" type="image/webp">'
      f'<img src="img/lekeitio-{i:02d}-800.webp" alt="{escaped(alt)}" loading="lazy" decoding="async"></picture>'
      '<span class="photo-zoom">&#10530;</span></button>')
def tail(lang):
    eu=lang=="eu"
    s=load(f"src/trabakuaondarroa_tail{'.eu' if eu else ''}.html")
    prefix="Trabakuatik Lekeitiorako zeharkaldia" if eu else "Travesía de Trabakua a Lekeitio"
    title=EU_TITLE if eu else ES_TITLE
    s=s.replace("trabakuaondarroa","lekeitio")
    eyebrow=('<p class="eyebrow"><span>Oinez</span><span class="sep">/</span><span>Mendibil, Urregarai eta Bedartzandi</span><span class="sep">/</span><span>Zeharkaldia</span></p>' if eu else '<p class="eyebrow"><span>A pie</span><span class="sep">/</span><span>Mendibil, Urregarai y Bedartzandi</span><span class="sep">/</span><span>Travesía</span></p>')
    hero=f'''      <div class="hero-label">
        {eyebrow}
        <h1>Trabakua, Mendibil,<br><em>{'Urregarai, Bedartzandi eta Lekeitio' if eu else 'Urregarai, Bedartzandi y Lekeitio'}</em></h1>
        <p class="full-name">{prefix}</p>
      </div>'''
    s=block(s,'<div class="hero-label">','</div>\n    </div>\n  </div>',hero.rsplit("</div>",1)[0])
    # Retirar marcadores de la ruta de plantilla: las cifras no son de Lekeitio.
    s=re.sub(r'<g class="elev-marker">.*?</g>','',s,flags=re.S)
    s=re.sub(r'<div class="elev-legend">.*?</div>', '', s, flags=re.S)
    s=block(s,'<div class="elev-tags">','<div class="hero-label">',
        '<div class="elev-tags"><span class="end left"><span class="v">—</span><span class="k">'+('Gutxieneko altitudea' if eu else 'Altitud mín.')+'</span></span><span class="mid">'+('trackaren profila' if eu else 'perfil real del track')+' · 32,74 km</span><span class="end right"><span class="v">—</span><span class="k">'+('Gehieneko altitudea' if eu else 'Altitud máx.')+'</span></span></div>')
    cover_alt=ROWS[COVER-1][3 if eu else 2]
    portada=(f'<button type="button" class="photo-slot" id="photoTrigger" data-lightbox-src="img/lekeitio-{COVER:02d}.webp" aria-haspopup="dialog">'
      f'<picture><source srcset="img/lekeitio-{COVER:02d}-800.webp 800w, img/lekeitio-{COVER:02d}.webp 1600w" sizes="(min-width:1024px) 1050px, (min-width:768px) 710px, 92vw" type="image/webp">'
      f'<img src="img/lekeitio-{COVER:02d}-800.webp" alt="{escaped(cover_alt)}"></picture>'
      '<span class="photo-zoom">&#10530; '+('Handitu' if eu else 'Ampliar')+'</span></button>')
    s=block(s,'<button type="button" class="photo-slot"','<div class="lightbox"',portada)
    s=s.replace('Foto ampliada del recorrido de Trabakua a Ondarroa',
        'Foto ampliada del recorrido de Trabakua a Lekeitio').replace(
        'Trabakuatik Ondarroarako ibilbidearen argazki handitua',
        'Trabakuatik Lekeitiorako ibilbidearen argazki handitua')
    facts=(
       '<div class="facts">'
       f'<div class="fact"><span class="v">32,74 km</span><span class="k">{"Distantzia" if eu else "Distancia"}</span></div>'
       f'<div class="fact"><span class="v">+1.533 m</span><span class="k">{"Desnibela +" if eu else "Desnivel +"}</span></div>'
       f'<div class="fact"><span class="v">{"Zaila" if eu else "Difícil"}</span><span class="k">{"Ahalegina" if eu else "Esfuerzo"}</span></div>'
       f'<div class="fact"><span class="v">{"Nahasia" if eu else "Mixta"}</span><span class="k">{"Zorua" if eu else "Superficie"}</span></div>'
       f'<div class="fact"><span class="v">{"Zeharkaldia" if eu else "Travesía"}</span><span class="k">{"Mota" if eu else "Tipo"}</span></div>'
       f'<div class="fact"><span class="v">{"Mendi-ibilaldia" if eu else "Senderismo"}</span><span class="k">{"Jarduera" if eu else "Actividad"}</span></div>'
       f'<div class="fact"><span class="v">Trabakua</span><span class="k">{"Irteera" if eu else "Salida"}</span></div>'
       '</div>'
       '<p class="facts-note">'+
       ('Distantzia GPX trackean oinarrituta dago. +1.533 metroko desnibela ibilbidearen egileak baieztatu du.' if eu else 'Distancia medida sobre el GPX. El desnivel positivo de +1.533 m está confirmado por el autor de la ruta.')+'</p>'
    )
    s=block(s,'<div class="facts">','<div class="parada">',facts)
    parada=('<div class="parada"><span class="k">Norentzat</span><h2>Oinezko zeharkaldia</h2><p>Harkaitzezko eta karsteko eremu zailak ditu. Santa Eufemiarako igoera zuzena ez da gomendagarria; deskribapenean bide alternatiboa azaltzen da.</p></div>' if eu else '<div class="parada"><span class="k">Para quién es</span><h2>Travesía exigente a pie</h2><p>Hay tramos rocosos y de terreno kárstico complicados. No se recomienda repetir la subida directa hacia Santa Eufemia; el texto explica la alternativa por pista.</p></div>')
    s=block(s,'<div class="parada">','<div class="gallery-grid">',parada)
    gallery='<div class="gallery-grid">\n'+ '\n'.join(image_html(i,row[3 if eu else 2]) for i,row in enumerate(ROWS,1) if i!=COVER)+'\n</div>'
    s=block(s,'<div class="gallery-grid">','<div class="report-modal"',gallery)
    s=block(s,'<div class="body-copy">','<section class="map-section">','<div class="body-copy">\n'+paras(lang)+'\n</div>')
    s=s.replace('data-map-src="data/trabakuaondarroa.json"','data-map-src="data/lekeitio.json"')
    # El bloque de plantilla ya se renombró a lekeitio: retirar el enlace de Wikiloc de otra ruta.
    s=re.sub(r'<p class="wikiloc-credit">.*?</p>',
             '<p class="wikiloc-credit">'+('Benetako GPX tracka' if eu else 'Track GPX real')+' · <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a></p>',s,flags=re.S)
    s=s.replace('termina en Ondarroa, no en la salida','termina en Lekeitio, no en la salida').replace('Ondarroan amaitzen da, ez irteeran','Lekeition amaitzen da, ez irteeran')
    # Verificar que no queda contenido descriptivo de la ruta modelo.
    assert 'data/lekeitio.json' in s
    assert s.count('data-lightbox-src="img/lekeitio-')==25
    return s
for lang in ("es","eu"):
    save("src/lekeitio_tail"+(".eu" if lang=="eu" else "")+".html",tail(lang))
head=load("src/trabakuaondarroa_head.html").replace("trabakuaondarroa","lekeitio")
head=head.replace("Trabakua, Atxagarai y Ondarroa &middot; Traves&iacute;a &mdash; Rutas Mallabia",escaped(ES_TITLE)+" &middot; Travesía &mdash; Rutas Mallabia")
head=head.replace("Traves&iacute;a de 32 km del alto de Trabakua a Ondarroa por Muniozguren, Atxagarai y Kurutzegana, bajando a la costa de Bizkaia",escaped(ES_DESC))
head=head.replace("img/lekeitio-01.jpg","img/lekeitio-23.jpg")
save("src/lekeitio_head.html",head)
# Alta de idioma y traducción manual de esta ficha ya entregada por el autor.
p="src/i18n/eu.py";t=load(p)
assert "'lekeitio': {}" not in t
t=t.replace("PAGE_STRINGS = {","PAGE_STRINGS = {\n    'lekeitio': {},",1)
t=t.replace("TITLES = {","TITLES = {\n    'lekeitio': "+repr(EU_TITLE+" · Oinezko zeharkaldia — Herriko ibilbideak")+",",1)
t=t.replace("DESCRIPTIONS = {","DESCRIPTIONS = {\n    'lekeitio': "+repr(EU_DESC)+",",1)
t += "\n# Traducciones de la nueva tarjeta de Lekeitio\nHOME.update(" + repr({ES_TITLE: EU_TITLE, ES_DESC: EU_DESC, "Puente de piedra junto al río Lea": "Harrizko zubia Lea ibaiaren ondoan"}) + ")\n"
save(p,t)
p="src/i18n/make_eu.py";t=load(p)
t=t.replace('PAGES = ["mallabia",','PAGES = ["mallabia", "lekeitio",',1)
t=t.replace('ROUTE_PAGES = {"trabakua",','ROUTE_PAGES = {"lekeitio", "trabakua",',1)
t=t.replace('MANUAL_EU_PAGES = set()','MANUAL_EU_PAGES = {"lekeitio"}',1)
save(p,t)
p="src/build.py";t=load(p).replace('PAGES = ["mallabia",','PAGES = ["mallabia", "lekeitio",',1)
t=re.sub(r'(?m)^ULTIMA_ENTRADA[^\\n]*$', 'ULTIMA_ENTRADA = ("lekeitio", "2026-11-06")', t, count=1)
save(p,t)
# Marcadores del mapa: sin waypoints numerados porque no están verificados individualmente.
import importlib.util
spec=importlib.util.spec_from_file_location("md",ROOT/"scripts/make_map_data.py")
md=importlib.util.module_from_spec(spec);spec.loader.exec_module(md)
pts=md.puntos_gpx(str(SRC/"lekeitio.gpx"))
assert len(pts)>20000 and all(p[2] is not None for p in pts)
detail={"tracks":[{"points":md.redondea(md.simplifica(pts,1),True)}],"marker":list(pts[0][:2]),"waypoints":[]}
save("data/lekeitio.json",json.dumps(detail,separators=(",",":")))
trail=json.loads(load("data/trailhead.json"))
base=next(t for t in trail["tracks"] if t.get("href")=="trabakuaondarroa.html")
new={k:v for k,v in base.items() if k not in ("points","chart","href")}
new["href"]="lekeitio.html";new["points"]=md.redondea(md.simplifica(pts,10),False)
trail["tracks"].insert(0,new)
save("data/trailhead.json",json.dumps(trail,separators=(",",":")))
# Portada: tarjeta nueva a partir de una travesía existente.
p="src/mallabia_tail.html";t=load(p)
a=t.index('<a class="route-card" href="trabakuaondarroa.html"')
b=t.index('</a>',a)+4
card=t[a:b]
card=card.replace("trabakuaondarroa","lekeitio")
card=re.sub(r'data-distance-km="[^"]*"', 'data-distance-km="32.74"',card)
card=re.sub(r'data-desnivel-m="[^"]*"', 'data-desnivel-m="1533"',card)
card=re.sub(r'data-tiempo-corriendo-min="[^"]*"', '',card)
card=re.sub(r'data-places="[^"]*"', 'data-places="Trabakua, Arteta, Mendibil, Meabe, Mallukitoki, Zapola, Urregarai, Santa Eufemia, Bedartzandi, Amoroto, Oleta, Lekeitio"',card)
card=re.sub(r'<div class="route-card-photo">.*?</div>',
 f'<div class="route-card-photo"><picture><source srcset="img/lekeitio-23-800.webp 800w, img/lekeitio-23.webp 1600w" sizes="(min-width:1024px) 340px, (min-width:768px) 46vw, 92vw" type="image/webp"><img src="img/lekeitio-23-800.webp" alt="Puente de piedra junto al río Lea" loading="lazy" decoding="async"></picture></div>',card,flags=re.S)
card=re.sub(r'<h3 class="route-card-name">.*?</h3>','<h3 class="route-card-name">'+escaped(ES_TITLE)+'</h3>',card,flags=re.S)
card=re.sub(r'<p class="route-card-desc">.*?</p>','<p class="route-card-desc">'+escaped(ES_DESC)+'</p>',card,flags=re.S)
card=re.sub(r'<p class="route-card-stats">.*?</p>','<p class="route-card-stats">32,74 km &middot; +1.533 m</p>',card,flags=re.S)
# No reutilizar el perfil de la tarjeta de Ondarroa: ocultarlo hasta obtener el de este GPX.
card=re.sub(r'<div class="route-card-chart".*?</div>','',card,flags=re.S)
pos=t.index('<a class="route-card" ')
t=t[:pos]+card+"\n      "+t[pos:]
save(p,t)
# Metadatos GPS con título y distancia en los dos idiomas.
p="data/rutas.json";r=json.loads(load(p))
r["es"]["lekeitio"]={"h":"lekeitio.html","n":ES_TITLE,"s":"32,74 km · +1.533 m"}
r["eu"]["lekeitio"]={"h":"lekeitio.eu.html","n":EU_TITLE,"s":"32,74 km · +1.533 m"}
save(p,json.dumps(r,ensure_ascii=False,separators=(",",":")))
print("Fuentes, tarjeta, datos de mapa y nombres GPS creados en la rama")
