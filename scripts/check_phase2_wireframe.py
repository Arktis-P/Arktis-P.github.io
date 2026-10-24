#!/usr/bin/env python3
"""Dependency-free static checks for the Phase 2 interactive review wireframe."""
from pathlib import Path
from html.parser import HTMLParser
import sys

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "docs" / "wireframes" / "index.html"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.external_assets = []
        self.scripts = 0
        self.styles = 0
        self.lang = None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "style":
            self.styles += 1
        if tag == "script":
            self.scripts += 1
            if "src" in d:
                self.external_assets.append(d["src"])
        if tag == "link" and d.get("rel") in ("stylesheet", "preload", "modulepreload"):
            self.external_assets.append(d.get("href", ""))
        if tag in ("img", "iframe", "video", "audio", "source"):
            self.external_assets.append(d.get("src", ""))

def main():
    errors = []
    if not FILE.is_file():
        print("[FAIL] missing wireframe file")
        return 1
    data = FILE.read_text(encoding="utf-8")
    tags = Tags()
    try:
        tags.feed(data)
    except Exception as exc:
        errors.append(f"HTML parser failed: {exc}")
    for expected in ("app", "nav-home", "nav-works"):
        if expected not in tags.ids:
            errors.append(f"missing #{expected}")
    if tags.lang != "en":
        errors.append("expected English lang declaration")
    if tags.styles != 1 or tags.scripts != 1:
        errors.append("expected a single inline style and a single inline script")
    if tags.external_assets:
        errors.append(f"unapproved external asset dependency: {tags.external_assets}")
    for phrase in (
        "PHASE 02 / DESIGN REVIEW", "NOT THE PUBLISHED WEBSITE",
        "Anvil Bastion", "VirtualQHDMirror", "SpartaPixelVerse",
        "Review only", "review-only", "prefers-reduced-motion",
        'data-filter', 'aria-pressed', 'hashchange',
        "#home", "#works", "#work/anvil-bastion",
        "https://arktis-p.github.io/privacy.html",
        "mailto:burningarktis@proton.me",
    ):
        if phrase not in data:
            errors.append("missing required phrase: "+phrase)
    if "fetch(" in data or "XMLHttpRequest" in data:
        errors.append("wireframe must not call remote APIs")
    if errors:
        for err in errors:
            print("[FAIL]", err)
        return 1
    print("[PASS] single HTML wireframe, local only, no external media/JS/CSS")
    print("[PASS] navigation, category controls, demo labels, keyboard/reduced-motion anchors")
    print("[NOTE] Static checks only: open HTML in browser for interactive/mobile QA.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
