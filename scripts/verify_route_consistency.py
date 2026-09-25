#!/usr/bin/env python3
"""Verify home-page route cards and overview-map tracks stay in sync."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD_RE = re.compile(
    r'<a class="route-card" href="([^"]+)"([^>]*)>([\s\S]*?)</a>'
)
REQUIRED_ATTRS = (
    "data-activity",
    "data-distance-km",
    "data-desnivel-m",
    "data-difficulty",
)


def attr(attrs: str, name: str) -> str | None:
    match = re.search(rf'{re.escape(name)}="([^"]*)"', attrs)
    return match.group(1) if match else None


def parse_cards(path: Path) -> list[dict[str, str | None]]:
    content = path.read_text(encoding="utf-8")
    cards = []
    for href, attrs, _body in CARD_RE.findall(content):
        card = {"href": href}
        for name in REQUIRED_ATTRS:
            card[name] = attr(attrs, name)
        cards.append(card)
    return cards


def normalized_eu_href(href: str) -> str:
    return re.sub(r"\.eu\.html$", ".html", href)


def duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return sorted(dupes)


def main() -> int:
    es_cards = parse_cards(ROOT / "index.es.html")
    eu_cards = parse_cards(ROOT / "index.html")
    trailhead = json.loads((ROOT / "data" / "trailhead.json").read_text(encoding="utf-8"))
    tracks = trailhead.get("tracks", [])

    es_hrefs = [str(card["href"]) for card in es_cards]
    eu_hrefs_raw = [str(card["href"]) for card in eu_cards]
    eu_hrefs = [normalized_eu_href(href) for href in eu_hrefs_raw]
    track_hrefs = [track.get("href") for track in tracks if track.get("href")]

    errors: list[str] = []

    for label, values in (
        ("Spanish cards", es_hrefs),
        ("Basque cards", eu_hrefs),
        ("overview-map tracks", track_hrefs),
    ):
        dupes = duplicates(values)
        if dupes:
            errors.append(f"{label}: duplicate routes: {', '.join(dupes)}")

    for label, cards in (("Spanish", es_cards), ("Basque", eu_cards)):
        for card in cards:
            missing = [name for name in REQUIRED_ATTRS if not card.get(name)]
            if missing:
                errors.append(
                    f"{label} card {card['href']}: missing {', '.join(missing)}"
                )

    es_set = set(es_hrefs)
    eu_set = set(eu_hrefs)
    track_set = set(track_hrefs)

    for href in sorted(es_set - eu_set):
        errors.append(f"Missing Basque card for {href}")
    for href in sorted(eu_set - es_set):
        errors.append(f"Missing Spanish card for {href}")
    for href in sorted(es_set - track_set):
        errors.append(f"Missing overview-map track for {href}")
    for href in sorted(track_set - es_set):
        errors.append(f"Overview-map track has no home-page card: {href}")

    for href in es_hrefs:
        if not (ROOT / href).is_file():
            errors.append(f"Spanish card target does not exist: {href}")
    for href in eu_hrefs_raw:
        if not (ROOT / href).is_file():
            errors.append(f"Basque card target does not exist: {href}")

    if len(tracks) != len(track_hrefs):
        errors.append(
            f"Overview map has {len(tracks) - len(track_hrefs)} track(s) without href"
        )

    if errors:
        print("Route consistency check FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Route consistency check passed: "
        f"{len(es_cards)} ES cards, {len(eu_cards)} EU cards, {len(tracks)} map tracks."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
