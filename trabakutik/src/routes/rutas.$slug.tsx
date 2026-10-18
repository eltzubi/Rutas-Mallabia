import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowLeft,
  Bike,
  ChevronLeft,
  ChevronRight,
  Download,
  ExternalLink,
  Footprints,
  Heart,
  Layers,
  Share2,
  TriangleAlert,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { effortLabel, terrainLabel, type DiffKey } from "@/data/difficulty";
import { useFavorites } from "@/data/favorites";
import "leaflet/dist/leaflet.css";

type Ficha = {
  slug: string;
  distance: number;
  elevation: number;
  activity: "walk" | "bike";
  difficulty: "easy" | "medium" | "hard";
  effort: DiffKey;
  terrain: DiffKey;
  image: string;
  alt: string;
  title: string;
  wikiloc: string | null;
  minAlt: number | null;
  maxAlt: number | null;
  eyebrow: { es: string; eu: string };
  fullName: { es: string; eu: string };
  parada: { es: string; eu: string };
  paradaTag: { es: string; eu: string };
  body: { es: string[]; eu: string[] };
  facts: { es: [string, string][]; eu: [string, string][] };
  note: { es: string; eu: string };
};

type Neighbor = { slug: string; title: string; distance: number } | null;

type Track = {
  p: [number, number, number | null][];
  min: number | null;
  max: number | null;
  gain: number;
  km: number;
  n: number;
};

const loadFichas = () => import("@/data/fichas.json");

const esTitle = (title: string) =>
  title.replaceAll(" eta ", " y ").replace("Gereako ur-jauziak", "cascadas de Gerea");

export const Route = createFileRoute("/rutas/$slug")({
  loader: async ({ params }) => {
    const { default: fichas } = await loadFichas();
    const list = fichas as Ficha[];
    const i = list.findIndex((f) => f.slug === params.slug);
    if (i < 0) throw notFound();
    const ficha: Ficha = list[i]!;
    const toNeighbor = (f: Ficha): Neighbor =>
      ({ slug: f.slug, title: f.title, distance: f.distance });
    return {
      ficha,
      prev: toNeighbor(list[(i - 1 + list.length) % list.length]!),
      next: toNeighbor(list[(i + 1) % list.length]!),
    };
  },
  head: ({ loaderData }) => {
    const ficha = loaderData?.ficha;
    if (!ficha) return { meta: [] };
    const title = `${esTitle(ficha.title)} · Trabakutik`;
    const description = ficha.fullName.es;
    return {
      meta: [
        { title },
        { name: "description", content: description },
        { property: "og:title", content: title },
        { property: "og:description", content: description },
        { property: "og:type", content: "website" },
        { name: "twitter:card", content: "summary_large_image" },
      ],
    };
  },
  component: FichaPage,
});

function FichaPage() {
  const { ficha, prev, next } = Route.useLoaderData();
  const [lang, setLangState] = useState<"es" | "eu">("es");
  useEffect(() => {
    const stored = window.localStorage.getItem("trabakutik-lang");
    if (stored === "es" || stored === "eu") setLangState(stored);
  }, []);
  const setLang = (l: "es" | "eu") => {
    setLangState(l);
    window.localStorage.setItem("trabakutik-lang", l);
  };
  const eu = lang === "eu";
  const t = (es: string, basque: string) => (eu ? basque : es);
  const title = eu ? ficha.title : esTitle(ficha.title);

  const [track, setTrack] = useState<Track | null>(null);
  const [trackError, setTrackError] = useState(false);
  useEffect(() => {
    let alive = true;
    setTrack(null);
    setTrackError(false);
    fetch(`/tracks/${ficha.slug}.json`)
      .then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then((d: Track) => {
        if (alive) setTrack(d);
      })
      .catch(() => {
        if (alive) setTrackError(true);
      });
    return () => {
      alive = false;
    };
  }, [ficha.slug]);

  const [frac, setFrac] = useState<number | null>(null);
  const [atMap, setAtMap] = useState(false);
  useEffect(() => {
    const el = document.getElementById("mapa");
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => setAtMap(entries.some((e) => e.isIntersecting && e.intersectionRatio > 0.2)),
      { threshold: [0, 0.2, 0.5, 1] },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [ficha.slug]);

  const { isFav, toggle } = useFavorites();
  const fav = isFav(ficha.slug);
  const [shared, setShared] = useState(false);
  const share = async () => {
    const url = `https://trabakutik.com/${ficha.slug}${eu ? ".eu" : ""}.html`;
    const text = `${title} · ${ficha.distance.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} km · +${ficha.elevation.toLocaleString("es-ES")} m · Trabakutik`;
    if (navigator.share) {
      try {
        await navigator.share({ title: `${title} · Trabakutik`, text, url });
        return;
      } catch (err) {
        // El usuario cerró el menú del sistema: no hacer nada más.
        if (err instanceof DOMException && err.name === "AbortError") return;
        // Sin destinos reales (p. ej. escritorio): abrir WhatsApp directamente.
      }
    }
    const waUrl = `https://wa.me/?text=${encodeURIComponent(`${text}\n${url}`)}`;
    const win = window.open(waUrl, "_blank", "noopener,noreferrer");
    if (!win) {
      // Ventana bloqueada por el navegador: copiar como último recurso.
      try {
        await navigator.clipboard.writeText(`${text}\n${url}`);
        setShared(true);
        window.setTimeout(() => setShared(false), 2500);
      } catch {
        /* portapapeles no disponible */
      }
    }
  };

  return (
    <main className="site-shell ficha-shell">
      <header className="site-header ficha-header">
        <Link to="/" className="ficha-back" aria-label={t("Volver a las rutas", "Itzuli ibilbideetara")}>
          <ArrowLeft size={18} />
          <span className="wordmark">TRABAKUTIK</span>
        </Link>
        <nav className="language-switch" aria-label={t("Idioma", "Hizkuntza")}>
          <Button variant="ghost" aria-pressed={eu} onClick={() => setLang("eu")} className={eu ? "text-primary" : "text-muted-foreground"}>Euskara</Button>
          <span className="text-primary">/</span>
          <Button variant="ghost" aria-pressed={!eu} onClick={() => setLang("es")} className={!eu ? "text-foreground" : "text-muted-foreground"}>Castellano</Button>
        </nav>
      </header>

      <section className="ficha-hero">
        <img className="ficha-hero-image" src={ficha.image} alt={ficha.alt} fetchPriority="high" />
        <div className="ficha-hero-content">
          <p className="cover-eyebrow">{ficha.eyebrow[lang]}</p>
          <h1>{title}</h1>
          <p className="ficha-fullname">{ficha.fullName[lang]}</p>
          <div className="ficha-hero-stats">
            <span>{ficha.distance.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} km</span>
            <span aria-hidden="true">·</span>
            <span>+{ficha.elevation.toLocaleString("es-ES")} m</span>
            <span aria-hidden="true">·</span>
            <span className="ficha-hero-activity">
              {ficha.activity === "bike" ? <Bike size={14} /> : <Footprints size={14} />}
              {ficha.activity === "bike" ? "E-bike" : t("A pie", "Oinez")}
            </span>
          </div>
        </div>
      </section>

      <div className="ficha-diffs">
        <span className="diff-chip"><small>{t("Esfuerzo", "Esfortzua")}</small>{effortLabel[ficha.effort][lang]}</span>
        <span className="diff-chip"><small>{t("Terreno", "Lurra")}</small>{terrainLabel[ficha.terrain][lang]}</span>
      </div>

      <div className="action-row">
        <a className="action-btn action-primary" href={`https://trabakutik.com/src/${ficha.slug}.gpx`}>
          <Download size={18} />GPX
        </a>
        <a className="action-btn" href={`https://trabakutik.com/src/${ficha.slug}.kml`}>
          <Download size={18} />KML
        </a>
        <a className="action-btn" href="#mapa">
          <Layers size={18} />{t("Mapa", "Mapa")}
        </a>
        {ficha.wikiloc && (
          <a className="action-btn" href={ficha.wikiloc} target="_blank" rel="noreferrer">
            <ExternalLink size={18} />Wikiloc
          </a>
        )}
        <button type="button" className="action-btn" onClick={share}>
          <Share2 size={18} />{shared ? t("¡Enlace copiado!", "Esteka kopiatuta!") : t("Compartir", "Partekatu")}
        </button>
        <button type="button" className={`action-btn${fav ? " action-fav" : ""}`} aria-pressed={fav} onClick={() => toggle(ficha.slug)}>
          <Heart size={18} fill={fav ? "currentColor" : "none"} />{fav ? t("Guardada", "Gordeta") : t("Guardar", "Gorde")}
        </button>
      </div>

      <div className="facts-grid">
        {ficha.facts[lang].map(([value, label]) => (
          <div className="fact" key={label}>
            <strong>{value}</strong>
            <span>{label}</span>
          </div>
        ))}
      </div>
      <p className="ficha-note">
        <TriangleAlert size={14} aria-hidden="true" />
        {t(
          "Las rutas no están señalizadas: lleva el track cargado en tu GPS. ",
          "Ibilbideak ez daude seinalizatuta: eraman trackea GPSan. ",
        )}
        {ficha.note[lang]}
      </p>

      <article className="ficha-copy" aria-label={t("Descripción de la ruta", "Ibilbidearen azalpena")}>
        {(ficha.parada[lang] || ficha.paradaTag[lang]) && (
          <aside className={ficha.parada[lang] ? "parada-box" : "parada-box parada-tag"}>
            <h2>{t("¿Para quién es?", "Norentzat")}</h2>
            <p>{ficha.parada[lang] || ficha.paradaTag[lang]}</p>
          </aside>
        )}
        {ficha.body[lang].map((p, i) => (
          <p key={i}>{p}</p>
        ))}
      </article>

      <section id="mapa" className="map-section" aria-label={t("Mapa y perfil", "Mapa eta profila")}>
        <h2 className="section-title">{t("Mapa y perfil de desnivel", "Mapa eta desnibel-profila")}</h2>
        {track && <RouteMap points={track.p} frac={frac} />}
        {!track && !trackError && (
          <div className="map-skeleton" role="status">{t("Cargando mapa…", "Mapa kargatzen…")}</div>
        )}
        {trackError && (
          <div className="map-skeleton">{t("No se pudo cargar el mapa.", "Ezin izan da mapa kargatu.")}</div>
        )}
        {track && <ElevationProfile points={track.p} frac={frac} onFrac={setFrac} t={t} minAlt={track.min} maxAlt={track.max} gain={track.gain} km={track.km} />}
      </section>

      <nav className="next-nav" aria-label={t("Más rutas", "Ibilbide gehiago")}>
        {prev && (
          <Link to="/rutas/$slug" params={{ slug: prev.slug }} className="next-card" rel="prev">
            <ChevronLeft size={16} />
            <span className="next-copy">
              <span className="next-label">{t("Anterior", "Aurrekoa")}</span>
              <span className="next-title">{eu ? prev.title : esTitle(prev.title)}</span>
              <span className="next-meta">{prev.distance.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} km</span>
            </span>
          </Link>
        )}
        {next && (
          <Link to="/rutas/$slug" params={{ slug: next.slug }} className="next-card next-right" rel="next">
            <span className="next-copy">
              <span className="next-label">{t("Siguiente", "Hurrengoa")}</span>
              <span className="next-title">{eu ? next.title : esTitle(next.title)}</span>
              <span className="next-meta">{next.distance.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} km</span>
            </span>
            <ChevronRight size={16} />
          </Link>
        )}
      </nav>

      <footer className="site-footer">
        <span>TRABAKUTIK · MALLABIA · BIZKAIA</span>
        <Link className="hover:text-primary" to="/">{t("Todas las rutas", "Ibilbide guztiak")}</Link>
        <a className="hover:text-primary" href="https://trabakutik.com/src/todas-las-rutas.zip">
          {t("Descargar todos los tracks", "Track guztiak deskargatu")} ↓
        </a>
      </footer>

      <nav
        className={`ficha-quick${atMap ? " is-hidden" : ""}`}
        aria-label={t("Accesos rápidos", "Sarbide azkarrak")}
      >
        <a className="action-btn action-primary" href={`https://trabakutik.com/src/${ficha.slug}.gpx`}>
          <Download size={18} />GPX
        </a>
        <a className="action-btn" href="#mapa">
          <Layers size={18} />{t("Mapa", "Mapa")}
        </a>
        {ficha.wikiloc && (
          <a className="action-btn" href={ficha.wikiloc} target="_blank" rel="noreferrer">
            <ExternalLink size={18} />Wikiloc
          </a>
        )}
      </nav>
    </main>
  );
}

type Point = [number, number, number | null];

const primaryColor = () =>
  getComputedStyle(document.documentElement).getPropertyValue("--primary").trim() || "#a3e635";

function RouteMap({ points, frac }: { points: Point[]; frac: number | null }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const layersRef = useRef<Record<string, any> | null>(null);
  const markerRef = useRef<any>(null);
  const [ready, setReady] = useState(false);
  const [layer, setLayer] = useState<"topo" | "mapa" | "sat">("topo");

  const cumul = useMemo(() => {
    const c: number[] = [0];
    const R = 6371000;
    for (let i = 1; i < points.length; i++) {
      const a = points[i - 1]!, b = points[i]!;
      const la1 = (a[0] * Math.PI) / 180, la2 = (b[0] * Math.PI) / 180;
      const dla = la2 - la1, dlo = ((b[1] - a[1]) * Math.PI) / 180;
      const h = Math.sin(dla / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin(dlo / 2) ** 2;
      c.push(c[i - 1]! + 2 * R * Math.asin(Math.sqrt(h)));
    }
    return c;
  }, [points]);

  useEffect(() => {
    let map: any;
    let cancelled = false;
    (async () => {
      const L = (await import("leaflet")).default;
      if (cancelled || !containerRef.current) return;
      map = L.map(containerRef.current, {
        scrollWheelZoom: window.matchMedia("(pointer: fine)").matches,
        zoomControl: true,
        attributionControl: true,
      });
      const primary = primaryColor();
      map.attributionControl.setPrefix(false);
      const layers = {
        topo: L.tileLayer("https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png", {
          maxZoom: 18,
          attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · CyclOSM',
        }),
        mapa: L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }),
        sat: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
          maxZoom: 18,
          attribution: "Esri, Maxar, Earthstar Geographics",
        }),
      };
      layersRef.current = layers;
      map.addLayer(layers.topo);
      const latlngs = points.map((p) => [p[0], p[1]] as [number, number]);
      L.polyline(latlngs, { color: primary, weight: 4, opacity: 0.95 }).addTo(map);
      L.circleMarker(latlngs[0]!, { radius: 6, color: "#fff", weight: 2, fillColor: primary, fillOpacity: 1 }).addTo(map);
      map.fitBounds(L.latLngBounds(latlngs), { padding: [22, 22] });
      mapRef.current = map;
      setReady(true);
    })();
    return () => {
      cancelled = true;
      if (map) map.remove();
      mapRef.current = null;
      layersRef.current = null;
      markerRef.current = null;
    };
  }, [points]);

  useEffect(() => {
    const map = mapRef.current;
    const layers = layersRef.current;
    if (!map || !layers || !ready) return;
    for (const key of Object.keys(layers) as (keyof typeof layers)[]) {
      if (key === layer) map.addLayer(layers[key]);
      else map.removeLayer(layers[key]);
    }
  }, [layer, ready]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !ready) return;
    let disposed = false;
    (async () => {
      const L = (await import("leaflet")).default;
      if (disposed || !mapRef.current) return;
      if (frac == null) {
        if (markerRef.current) {
          map.removeLayer(markerRef.current);
          markerRef.current = null;
        }
        return;
      }
      const total = cumul[cumul.length - 1] ?? 1;
      const target = frac * total;
      let i = 1;
      while (i < cumul.length - 1 && cumul[i]! < target) i++;
      const at: [number, number] = [points[i]![0], points[i]![1]];
      if (markerRef.current) {
        markerRef.current.setLatLng(at);
      } else {
        markerRef.current = L.circleMarker(at, {
          radius: 7,
          color: "#fff",
          weight: 2,
          fillColor: primaryColor(),
          fillOpacity: 1,
        }).addTo(map);
      }
    })();
    return () => {
      disposed = true;
    };
  }, [frac, ready, cumul, points]);

  return (
    <div className="route-map-box">
      <div className="route-map" ref={containerRef} />
      <div className="map-layers" role="group" aria-label="Capas del mapa">
        {([["topo", "Topo"], ["mapa", "Mapa"], ["sat", "Sat"]] as const).map(([key, label]) => (
          <button key={key} type="button" aria-pressed={layer === key} className={layer === key ? "active" : ""} onClick={() => setLayer(key)}>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

function ElevationProfile({
  points,
  frac,
  onFrac,
  t,
  minAlt,
  maxAlt,
  gain,
  km,
}: {
  points: Point[];
  frac: number | null;
  onFrac: (f: number | null) => void;
  t: (es: string, eu: string) => string;
  minAlt: number | null;
  maxAlt: number | null;
  gain: number;
  km: number;
}) {
  const boxRef = useRef<HTMLDivElement>(null);

  const geo = useMemo(() => {
    const withEle = points.filter((p) => p[2] != null);
    const R = 6371000;
    const cum: number[] = [0];
    for (let i = 1; i < withEle.length; i++) {
      const a = withEle[i - 1]!, b = withEle[i]!;
      const la1 = (a[0] * Math.PI) / 180, la2 = (b[0] * Math.PI) / 180;
      const dla = la2 - la1, dlo = ((b[1] - a[1]) * Math.PI) / 180;
      const h = Math.sin(dla / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin(dlo / 2) ** 2;
      cum.push(cum[i - 1]! + 2 * R * Math.asin(Math.sqrt(h)));
    }
    const total = cum[cum.length - 1] || 1;
    const eles = withEle.map((p) => p[2] as number);
    const min = Math.min(...eles), max = Math.max(...eles);
    const span = max - min || 1;
    const coords = withEle.map((p, i) => [(cum[i]! / total) * 100, 94 - ((p[2] as number) - min) / span * 80] as const);
    const line = coords.map((c, i) => `${i === 0 ? "M" : "L"}${c[0].toFixed(2)},${c[1].toFixed(2)}`).join(" ");
    const area = `${line} L100,100 L0,100 Z`;
    return { line, area, min, max, total, coords, startEle: eles[0], endEle: eles[eles.length - 1] };
  }, [points]);

  const pick = (clientX: number) => {
    const el = boxRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    onFrac(Math.min(1, Math.max(0, (clientX - rect.left) / rect.width)));
  };

  const pointerType = useRef<"mouse" | "touch" | "pen" | null>(null);

  const markerLeft = frac != null ? frac * 100 : null;
  const markerEle =
    frac != null
      ? geo.coords[Math.min(geo.coords.length - 1, Math.max(0, Math.round(frac * (geo.coords.length - 1))))]![1]
      : null;

  return (
    <div className="profile-box">
      <div
        className="profile-visual"
        ref={boxRef}
        role="img"
        aria-label={`${t("Perfil de desnivel", "Desnibel-profila")}: ${minAlt ?? ""}–${maxAlt ?? ""} m`}
        onPointerMove={(e) => { pointerType.current = e.pointerType; pick(e.clientX); }}
        onPointerDown={(e) => { pointerType.current = e.pointerType; pick(e.clientX); }}
        onPointerLeave={() => { if (pointerType.current === "mouse" || pointerType.current == null) onFrac(null); }}
      >
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
          <path d={geo.area} fill="var(--color-primary)" fillOpacity="0.18" stroke="none" />
          <path d={geo.line} fill="none" stroke="var(--color-primary)" strokeWidth="2" vectorEffect="non-scaling-stroke" />
        </svg>
        {markerLeft != null && markerEle != null && (
          <div className="profile-marker" style={{ left: `${markerLeft}%`, top: `${markerEle}%` }} aria-hidden="true" />
        )}
        <span className="profile-elev profile-elev-max">{Math.round(geo.max)} m</span>
        <span className="profile-elev profile-elev-min">{Math.round(geo.min)} m</span>
      </div>
      <div className="profile-summary">
        <span>+{gain.toLocaleString("es-ES")} m {t("de desnivel", "gorantz")}</span>
        <span>{km.toLocaleString("es-ES", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} km</span>
        <span>{t("Pasa el dedo por el perfil para verlo en el mapa", "Pasatu hatza profilean mapan ikusteko")}</span>
      </div>
    </div>
  );
}
