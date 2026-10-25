#!/usr/bin/env python3
"""Phase 4: no-cost source checks and optional built-site URL checks."""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAGES = [
    "index.html",
    "works/index.html",
    "works/anvil-bastion/index.html",
    "works/virtualqhdmirror/index.html",
    "404.html",
    "privacy.html",
    "app-ads.txt",
]
PLAY = "https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion"
GITHUB = "https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md"
MAIL = "burningarktis@gmail.com"

class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", action="store_true",
                        help="Also verify generated dist/ after npm run build")
    args = parser.parse_args()
    errors: list[str] = []
    def check(condition: bool, description: str) -> None:
        if condition:
            print("[PASS]", description)
        else:
            errors.append(description)
            print("[FAIL]", description)

    important = [
        "package.json", "astro.config.mjs", "src/content.config.ts",
        "src/lib/media.ts", "src/layouts/SiteLayout.astro",
        "src/components/MediaBlock.astro", "src/components/WorkCard.astro",
        "src/pages/index.astro", "src/pages/works/index.astro",
        "src/pages/works/[slug]/index.astro", "src/pages/404.astro",
        "src/styles/global.css", "docs/ASSET_GUIDE.md",
    ]
    for rel in important:
        check((ROOT / rel).is_file(), f"source exists: {rel}")
    if errors:
        return 1

    home = (ROOT / "src/pages/index.astro").read_text(encoding="utf-8")
    listing = (ROOT / "src/pages/works/index.astro").read_text(encoding="utf-8")
    detail = (ROOT / "src/pages/works/[slug]/index.astro").read_text(encoding="utf-8")
    shell = (ROOT / "src/layouts/SiteLayout.astro").read_text(encoding="utf-8")
    media = (ROOT / "src/lib/media.ts").read_text(encoding="utf-8")
    config = (ROOT / "astro.config.mjs").read_text(encoding="utf-8")
    css = (ROOT / "src/styles/global.css").read_text(encoding="utf-8")
    works = list((ROOT / "content/works").glob("*.md"))
    approved = {"anvil-bastion.md", "virtualqhdmirror.md"}

    check({p.name for p in works if "draft: false" in p.read_text(encoding="utf-8")} == approved,
          "only the two approved works are public")
    check('getCollection("works", ({ data }) => !data.draft)' in listing
          and 'getCollection("works", ({ data }) => !data.draft)' in detail,
          "draft entries excluded from lists and detail routes")
    check('data-i18n-key="home.hero.title"' in home and 'from "../lib/i18n"' in home,
          "headline uses external bilingual CSV")
    check('featured_works' in home and 'data.featured' in home, "featured entries derive from content")
    check("data.order - b.data.order" in listing, "Work sorting uses metadata")
    check('aria-pressed' in listing and 'data-filter' in listing
          and 'empty-results' in listing, "filters and empty state exist")
    check('media.screenshots' in detail and 'media.cover' in detail
          and 'getBrandMedia()' in shell, "build-time images and optional gallery connected")
    check('primary.label' in detail and 'primary.url' in detail
          and 'related-links' in detail, "prominent verified project CTA and secondary links")
    check('contact.data.email' in shell and 'contact.data.email' in home,
          "Gmail address bound to contact collection")
    check('prefers-reduced-motion' in css and ':focus-visible' in css
          and '@media(max-width:600px)' in css, "accessibility and mobile styles")
    check('output: "static"' in config and 'site: "https://arktis-p.github.io"' in config,
          "static output targets original Pages domain")
    check(not (ROOT / ".github/workflows").exists(), "no GitHub Actions workflow installed")

    root_privacy = (ROOT / "privacy.html").read_bytes()
    output_privacy = (ROOT / "public/privacy.html").read_bytes()
    expected = root_privacy.replace(b"burningarktis@proton.me", b"burningarktis@gmail.com")
    check(b"burningarktis@proton.me" in root_privacy and output_privacy == expected,
          "published privacy copy differs ONLY by authorized contact address")
    check((ROOT / "public/app-ads.txt").read_bytes()
          == (ROOT / "app-ads.txt").read_bytes(),
          "published app-ads authorization bytes unchanged")
    check(MAIL in (ROOT / "content/contact.yml").read_text(encoding="utf-8"),
          "approved Gmail contact in content")
    check(PLAY in (ROOT / "content/works/anvil-bastion.md").read_text(encoding="utf-8")
          and GITHUB in (ROOT / "content/works/virtualqhdmirror.md").read_text(encoding="utf-8"),
          "approved store and GitHub primary URLs in metadata")

    if args.dist:
        dist = ROOT / "dist"
        check(dist.is_dir(), "dist/ created by a real Astro build")
        if dist.is_dir():
            for page in EXPECTED_PAGES:
                check((dist / page).is_file(), f"built route: /{page}")
            if all((dist / page).is_file() for page in EXPECTED_PAGES):
                rendered = {page: (dist / page).read_text(encoding="utf-8", errors="replace")
                            for page in EXPECTED_PAGES if page.endswith(".html")}
                check(PLAY in rendered["works/anvil-bastion/index.html"],
                      "built game detail links to Google Play")
                check(GITHUB in rendered["works/virtualqhdmirror/index.html"],
                      "built software detail links to GitHub")
                check("Anvil Bastion" in rendered["works/index.html"]
                      and "VirtualQHDMirror" in rendered["works/index.html"]
                      and "SpartaPixelVerse" not in rendered["works/index.html"],
                      "built Works list matches approved scope")
                check(MAIL in rendered["index.html"] and MAIL in rendered["privacy.html"],
                      "built site and privacy have approved contact")
                check(not any("proton.me" in body.lower() for body in rendered.values()),
                      "no legacy Proton address in built HTML")
                check((dist / "app-ads.txt").read_bytes() == (ROOT / "app-ads.txt").read_bytes(),
                      "built app-ads.txt exact authorization preserved")
                for page, body in rendered.items():
                    links = Links()
                    links.feed(body)
                    for href in links.links:
                        if not href.startswith("/") or href.startswith("//"):
                            continue
                        route = href.split("#")[0].split("?")[0]
                        if route == "/":
                            target = dist / "index.html"
                        elif route.endswith("/"):
                            target = dist / route.lstrip("/") / "index.html"
                        else:
                            target = dist / route.lstrip("/")
                        check(target.exists(), f"internal link: {page} -> {href}")
    else:
        print("[NOTE] dist/ not checked; run 'npm run build' then re-run with --dist.")

    if errors:
        print(f"Phase 4: {len(errors)} checks failed.")
        return 1
    print("[PASS] Phase 4 source/build-artifact checks completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
