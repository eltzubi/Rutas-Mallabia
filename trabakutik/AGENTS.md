<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

- Keep the homepage presentation in the index route and the route data (cards, fichas) in data modules under `src/data/` (`routes.json`, `fichas.json`); ficha content is scraped from trabakutik.com in both es+eu, and downloads (GPX/KML) plus Wikiloc keep pointing at the original site.
- Store downloaded original photographs as Lovable Assets pointers to preserve the source imagery without bundling binary files.
- Store per-route track geometry only as simplified JSON in `public/tracks/<slug>.json` (`{p:[[lat,lon,ele]],min,max,gain,km,n}`); never bundle raw GPX files — downloads link to trabakutik.com.
- Route difficulty is split into `effort` (physical, from km + elevation, e-bike weighted 0.8) and `terrain` (technical, from surface keywords + activity); both are precomputed keys (`low|mid|high`) stored in `routes.json`/`fichas.json` and labeled via `src/data/difficulty.ts` — recompute with a script if route data changes.
