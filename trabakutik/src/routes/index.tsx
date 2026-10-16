import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { ArrowDown, ArrowUpRight, Bike, ChevronDown, ChevronRight, Footprints, Heart, Map, Search, SlidersHorizontal, TriangleAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import hero from "@/assets/hero.jpg.asset.json";
import routes from "@/data/routes.json";
import { effortLabel, terrainLabel, type DiffKey } from "@/data/difficulty";
import { useFavorites } from "@/data/favorites";

export const Route = createFileRoute("/")({
  head: () => ({ meta: [
    { title: "Trabakutik · Rutas a pie y en e-bike por Mallabia" },
    { name: "description", content: "Explora 59 rutas documentadas por Mallabia y alrededores. Encuentra tu recorrido a pie o en e-bike por distancia y dificultad." },
    { property: "og:title", content: "Trabakutik · A pie y en e-bike" },
    { property: "og:description", content: "59 rutas por los montes y pueblos de Mallabia, documentadas sobre el terreno." },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: "summary_large_image" },
  ] }),
  component: Index,
});

function Index() {
  const [langState, setLangState] = useState<"es" | "eu">("es");
  const lang = langState;
  const setLang = (l: "es" | "eu") => {
    setLangState(l);
    window.localStorage.setItem("trabakutik-lang", l);
  };
  useEffect(() => {
    const stored = window.localStorage.getItem("trabakutik-lang");
    if (stored === "es" || stored === "eu") setLangState(stored);
  }, []);
  const [search, setSearch] = useState("");
  const [activity, setActivity] = useState("all");
  const [distance, setDistance] = useState("all");
  const [difficulty, setDifficulty] = useState("all");
  const [sort, setSort] = useState("original");
  const [more, setMore] = useState(false);
  const [safety, setSafety] = useState(false);
  const [favOnly, setFavOnly] = useState(false);
  const { favs, isFav, toggle } = useFavorites();
  const eu = lang === "eu";
  const t = (es: string, basque: string) => eu ? basque : es;
  const visible = useMemo(() => routes.filter(r => {
    const slug = r.url.replace("https://trabakutik.com/", "").replace(".eu.html", "");
    const nameMatch = r.title.toLocaleLowerCase().includes(search.toLocaleLowerCase());
    const activityMatch = activity === "all" || activity === r.activity;
    const distanceMatch = distance === "all" || (distance === "short" ? r.distance <= 10 : distance === "medium" ? r.distance > 10 && r.distance <= 20 : distance === "long" ? r.distance > 20 && r.distance <= 30 : r.distance > 30);
    const favMatch = !favOnly || favs.includes(slug);
    return nameMatch && activityMatch && distanceMatch && favMatch && (difficulty === "all" || difficulty === r.difficulty);
  }).sort((a,b) => sort === "distance" ? a.distance-b.distance : sort === "elevation" ? a.elevation-b.elevation : 0), [search,activity,distance,difficulty,sort,favOnly,favs]);
  const routeTitle = (title: string) => eu ? title : title.replaceAll(" eta ", " y ").replace("Gereako ur-jauziak", "cascadas de Gerea");
  return (
    <main className="site-shell">
      <header className="site-header">
        <a href="/" aria-label="Trabakutik"><div className="wordmark">TRABAKUTIK</div><div className="brand-place">MALLABIA · BIZKAIA</div></a>
        <nav className="language-switch" aria-label="Idioma">
          <Button variant="ghost" aria-pressed={eu} onClick={() => setLang("eu")} className={eu ? "text-primary" : "text-muted-foreground"}>Euskara</Button>
          <span className="text-primary">/</span>
          <Button variant="ghost" aria-pressed={!eu} onClick={() => setLang("es")} className={!eu ? "text-foreground" : "text-muted-foreground"}>Castellano</Button>
        </nav>
      </header>
      <section className="cover" aria-labelledby="cover-title">
        <img className="cover-image" src={hero.url} alt={t("Senderista y ciclista en la cima al atardecer, con el valle y el mar al fondo", "Bi pertsona mendi baten gailurrean ilunabarrean, harana eta itsasoa atzealdean")} fetchPriority="high" />
        <div className="cover-content">
          <p className="cover-eyebrow">{t("MALLABIA Y ALREDEDORES", "MALLABIA ETA INGURUAK")}</p>
          <h1 id="cover-title">Trabakutik<span>{t("A pie y en e-bike", "Oinez eta e-bikez")}</span></h1>
          <p className="cover-description">{t("Rutas documentadas sobre el terreno por los montes y pueblos de Mallabia.", "Mallabia inguruko mendiak eta herriak zeharkatzen dituzten ibilbideak. Bertatik bertara dokumentatuak.")}</p>
          <div className="cover-actions flex flex-wrap gap-3">
            <Button variant="hero" size="lg" asChild><a href="#rutas">{t("Explorar rutas", "Ibilbideak ikusi")}<ArrowDown /></a></Button>
            <Button variant="photo" size="lg" asChild><a href={`https://trabakutik.com/${eu ? "" : "index.html"}#mapa`}><Map />{t("Ver mapa", "Mapa ikusi")}</a></Button>
          </div>
        </div>
        <div className="cover-stats"><span>59 {t("rutas", "ibilbide")}</span><span>·</span><span>1.321 km</span><span>·</span><span>54.247 m {t("de desnivel", "gorantz")}</span></div>
      </section>
      <div className="mx-0 sm:mx-5">
        <Button variant="ghost" className="safety-bar" aria-expanded={safety} onClick={() => setSafety(!safety)}><TriangleAlert /><span>{t("Antes de salir: lleva el track en tu GPS", "Irten aurretik: eraman trackea GPSan")}</span>{safety ? <ChevronDown /> : <ChevronRight />}</Button>
        {safety && <div className="safety-copy"><p>{t("Las rutas no están señalizadas. Es imprescindible llevar el track cargado en un GPS, reloj o dispositivo de navegación. La información de la web no sustituye al track.", "Ibilbideak ez daude seinalizatuta. Ezinbestekoa da trackea GPS, erloju edo nabigazio-gailu batean kargatuta eramatea.")}</p><p className="mt-3">{t("Valora las condiciones del terreno. Si un paso no te parece seguro, busca otro camino o da la vuelta. Respeta el entorno y deja las puertas y cierres como los encontraste.", "Balioetsi unean uneko baldintzak. Pauso bat seguru iruditzen ez bazaizu, bilatu beste bide bat edo egin atzera. Errespetatu ingurua.")}</p></div>}
      </div>
      <section id="rutas" className="catalogue" aria-label={t("Rutas", "Ibilbideak")}>
        <label className="search-box"><Search size={18} className="text-muted-foreground" /><input aria-label={t("Buscar ruta o lugar", "Bilatu ibilbidea")} value={search} onChange={e => setSearch(e.target.value)} placeholder={t("Buscar ruta o lugar…", "Bilatu ibilbidea izenez…")} type="search" /></label>
        <div className="filter-row">
          <div className="activity-switch">{([{value:"all",label:t("Todas","Guztiak")},{value:"walk",label:t("A pie","Oinez")},{value:"bike",label:"E-bike"}]).map(({value,label}) => <Button key={value} variant={activity === value ? "selected" : "ghost"} aria-pressed={activity === value} onClick={() => setActivity(value)}>{label}</Button>)}</div>
          <label className="select-control"><select aria-label={t("Distancia", "Distantzia")} value={distance} onChange={e => setDistance(e.target.value)}><option value="all">{t("Distancia", "Distantzia")}</option><option value="short">≤ 10 km</option><option value="medium">10–20 km</option><option value="long">20–30 km</option><option value="extra">&gt; 30 km</option></select></label>
          <Button variant="filter" aria-expanded={more} onClick={() => setMore(!more)}><SlidersHorizontal />{t("Más filtros", "Iragazki gehiago")}</Button>
          <Button variant={favOnly ? "selected" : "filter"} aria-pressed={favOnly} onClick={() => setFavOnly(!favOnly)}><Heart fill={favOnly ? "currentColor" : "none"} />{t("Mis rutas", "Nire ibilbideak")}{favs.length > 0 ? ` (${favs.length})` : ""}</Button>
          <label className="select-control sort-control"><span>{t("Ordenar por:", "Ordenatu:")}</span><select aria-label={t("Ordenar rutas", "Ibilbideak ordenatu")} value={sort} onChange={e => setSort(e.target.value)}><option value="original">{t("Destacadas", "Nabarmenduak")}</option><option value="distance">{t("Distancia", "Distantzia")}</option><option value="elevation">{t("Desnivel", "Desnibela")}</option></select></label>
        </div>
        {more && <div className="advanced-filters"><label className="select-control"><span>{t("Dificultad:", "Zailtasuna:")}</span><select aria-label={t("Dificultad", "Zailtasuna")} value={difficulty} onChange={e => setDifficulty(e.target.value)}><option value="all">{t("Todas", "Guztiak")}</option><option value="easy">{t("Fácil", "Erraza")}</option><option value="medium">{t("Media", "Ertaina")}</option><option value="hard">{t("Difícil", "Zaila")}</option></select></label><Button variant="ghost" onClick={() => {setActivity("all");setDistance("all");setDifficulty("all");setSearch("");}}>{t("Restablecer", "Berrezarri")}</Button></div>}
        <p className="route-count" aria-live="polite">{visible.length} {t("rutas", "ibilbide")}</p>
        <div className="route-grid">{visible.map(r => { const slug = r.url.replace("https://trabakutik.com/", "").replace(".eu.html", ""); const fav = isFav(slug); return <Link key={r.url} to="/rutas/$slug" params={{ slug }} className="route-card"><img src={r.image} alt={r.alt} loading="lazy" /><button type="button" className={`fav-btn${fav ? " is-fav" : ""}`} aria-pressed={fav} aria-label={fav ? t("Quitar de Mis rutas", "Kendu Nire ibilbideetatik") : t("Guardar en Mis rutas", "Gorde Nire ibilbideetan")} onClick={(e) => { e.preventDefault(); e.stopPropagation(); toggle(slug); }}><Heart size={18} fill={fav ? "currentColor" : "none"} /></button><div className="route-card-copy"><h2>{routeTitle(r.title)}</h2><p>{r.distance.toLocaleString(eu ? "eu-ES" : "es-ES", {minimumFractionDigits:2,maximumFractionDigits:2})} km · +{r.elevation.toLocaleString("es-ES")} m</p><p className="route-activity">{r.activity === "bike" ? <Bike size={14} /> : <Footprints size={14} />}{r.activity === "bike" ? "E-bike" : t("A pie", "Oinez")}</p><p className="route-diffs"><span className="route-diff"><small>{t("Esfuerzo", "Esfortzua")}</small>{effortLabel[r.effort as DiffKey][lang]}</span><span className="route-diff"><small>{t("Terreno", "Lurra")}</small>{terrainLabel[r.terrain as DiffKey][lang]}</span></p></div></Link>; })}</div>
        {!visible.length && <div className="py-10 text-center"><p>{t("No hay rutas con estos filtros.", "Ez dago iragazki hauekin bat datorren ibilbiderik.")}</p><Button variant="link" onClick={() => {setSearch("");setDistance("all");setActivity("all");setDifficulty("all");}}>{t("Ver todas las rutas", "Ibilbide guztiak ikusi")}</Button></div>}
      </section>
      <footer className="site-footer"><span>TRABAKUTIK · MALLABIA · BIZKAIA</span><a className="flex items-center gap-2 hover:text-primary" href="https://www.google.com/maps/dir/?api=1&destination=43.210466,-2.5460838">{t("Cómo llegar a Trabakua", "Nola iritsi Trabakura")}<ArrowUpRight size={16} /></a><a className="hover:text-primary" href="https://trabakutik.com/src/todas-las-rutas.zip">{t("Descargar todos los tracks", "Track guztiak deskargatu")} ↓</a></footer>
    </main>
  );
}
