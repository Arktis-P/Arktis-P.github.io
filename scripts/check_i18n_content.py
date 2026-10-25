#!/usr/bin/env python3
"""No-dependency test for full externalized EN/KO content and same-URL locale UI."""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "content/i18n/strings.csv"
FILES = [
    "src/layouts/SiteLayout.astro",
    "src/components/MediaBlock.astro",
    "src/components/WorkCard.astro",
    "src/components/LanguageSwitcher.astro",
    "src/pages/index.astro",
    "src/pages/works/index.astro",
    "src/pages/works/[slug]/index.astro",
    "src/pages/404.astro",
]
WORKS = ["anvil-bastion", "virtualqhdmirror"]
TRANSLATION_KEY_RE = re.compile(r"[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*")

REQUIRED_PARTS = [
    "title", "summary", "attribution", "platforms",
    "p1", "p2", "cover.alt", "screenshot.alt",
]

def main() -> int:
    failures: list[str] = []
    # Regression: keep camelCase a11y keys valid, reject malformed IDs.
    valid_examples = ("a11y.brandHome", "a11y.aboutContact", "a11y.projectInfo",
                      "work.anvil-bastion.cover.alt", "works.count.one")
    invalid_examples = ("a11y..brandHome", "a11y.brand home",
                        "a11y.brandHome!", ".a11y", "a11y.", "a11y/brandHome")
    for key in valid_examples:
        if not TRANSLATION_KEY_RE.fullmatch(key):
            failures.append(f"valid translation key rejected: {key}")
    for key in invalid_examples:
        if TRANSLATION_KEY_RE.fullmatch(key):
            failures.append(f"invalid translation key accepted: {key}")
    # Ensure the TS loader and the Astro secondary-link schema use the same rules.
    ts = (ROOT / "src/lib/i18n.ts").read_text(encoding="utf-8")
    schema = (ROOT / "src/content.config.ts").read_text(encoding="utf-8")
    expected_ts = "TRANSLATION_KEY_PATTERN = /^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$/"
    if expected_ts not in ts:
        failures.append("TypeScript translation-key validation differs from the Python checker")
    if "label_key: z.string().regex(/^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$/)" not in schema:
        failures.append("Astro label_key schema differs from the translation-key rule")
    try:
        with CSV_FILE.open(encoding="utf-8-sig", newline="") as file:
            table = csv.DictReader(file)
            if table.fieldnames != ["key", "en", "ko"]:
                failures.append("CSV header must be key,en,ko")
            translations: dict[str, dict[str, str]] = {}
            for number, row in enumerate(table, start=2):
                key = row.get("key", "")
                en, ko = row.get("en"), row.get("ko")
                if not key or not TRANSLATION_KEY_RE.fullmatch(key):
                    failures.append(f"invalid key on line {number}: {key}")
                if key in translations:
                    failures.append(f"duplicate key: {key}")
                if not en or not ko or not en.strip() or not ko.strip():
                    failures.append(f"missing translation for {key}")
                if None in row or None in (en, ko):
                    failures.append(f"invalid CSV fields on line {number}")
                if en and ko and set(re.findall(r"\{\w+\}", en)) != set(re.findall(r"\{\w+\}", ko)):
                    failures.append(f"interpolation mismatch: {key}")
                translations[key] = {"en": en or "", "ko": ko or ""}
    except (OSError, csv.Error) as exc:
        print("[FAIL] cannot parse CSV:", exc)
        return 1

    files = {name: (ROOT / name).read_text(encoding="utf-8") for name in FILES}
    required: set[str] = set()
    for name, source in files.items():
        for regex in (
            r'\bt\("([A-Za-z0-9._-]+)"\)',
            r'\bdata-i18n-(?:key|split|alt|aria-label)="([A-Za-z0-9._-]+)"',
            r'\b(?:titleKey|descriptionKey)="([A-Za-z0-9._-]+)"',
        ):
            required.update(re.findall(regex, source))
    for slug in WORKS:
        for part in REQUIRED_PARTS:
            required.add("work." + slug + "." + part)
    required.update({"common.category.game", "common.category.software", "common.category.experiment"})
    missing = sorted(required - set(translations))
    if missing:
        failures.append("keys referenced but absent: " + ", ".join(missing))
    if len(translations) < 70:
        failures.append(f"expected full copy migration, found {len(translations)} keys")
    layout = files["src/layouts/SiteLayout.astro"]
    switcher = files["src/components/LanguageSwitcher.astro"]
    listing = files["src/pages/works/index.astro"]
    for marker in ('data-locale="en"', 'data-locale="ko"', "localStorage.setItem",
                   'document.documentElement.lang = locale', 'data-i18n-title',
                   'data-i18n-description', 'data-i18n-count'):
        if marker not in switcher:
            failures.append("missing language-switch behavior: " + marker)
    if "<LanguageSwitcher />" not in layout:
        failures.append("language switcher not mounted in common header")
    if "site:refresh-translations" not in listing or "data-i18n-count" not in listing:
        failures.append("works filter does not refresh localized result count")
    if (ROOT / "src/pages/ko").exists() or (ROOT / "src/pages/en").exists():
        failures.append("unexpected duplicated language routes")
    if (ROOT / "content/about.md").exists():
        failures.append("obsolete about.md could confuse content editing")
    if failures:
        for item in failures:
            print("[FAIL]", item)
        return 1
    print(f"[PASS] {len(translations)} keys with complete EN/KO text and matching placeholders")
    print(f"[PASS] {len(required)} direct/dynamic references resolve, all approved Works covered")
    print("[PASS] single-route switcher, localStorage, translated metadata/accessibility and filters")
    print("[NOTE] Browser QA still required for locale persistence, mobile overflow and Astro build.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
