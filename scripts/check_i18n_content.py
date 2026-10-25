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


EMPHASIS_RE = re.compile(r"\[\[(accent|ink|muted|#[0-9A-Fa-f]{6})\|([\s\S]*?)\]\]")
DARK_BACKGROUND = "#0c0d10"

def luminance(color: str) -> float:
    channels = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

def readable(color: str, background: str = DARK_BACKGROUND) -> bool:
    a, b = luminance(color), luminance(background)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05) >= 4.5

def validate_emphasis(value: str) -> str:
    """Validate safe CSV markers and return plain text (no markup or raw HTML)."""
    plain = []
    start = 0
    for match in EMPHASIS_RE.finditer(value):
        preceding = value[start:match.start()]
        if "[[" in preceding or "]]" in preceding:
            raise ValueError("unsupported or unclosed color tag")
        plain.append(preceding)
        color, content = match.groups()
        if not content.strip() or "[[" in content or "]]" in content:
            raise ValueError("empty or nested color tag")
        if color.startswith("#") and not readable(color):
            raise ValueError(f"color {color} has insufficient contrast on {DARK_BACKGROUND}")
        plain.append(content)
        start = match.end()
    tail = value[start:]
    if "[[" in tail or "]]" in tail:
        raise ValueError("unsupported or unclosed color tag")
    plain.append(tail)
    return "".join(plain)

def main() -> int:
    failures: list[str] = []
    # Bilingual, arbitrary-position markers must be safe and deterministic.
    positive = (
        ("Making things [[accent|worth exploring.]]", "Making things worth exploring."),
        ("[[accent|탐험할 가치가 있는 것]]을 만듭니다.", "탐험할 가치가 있는 것을 만듭니다."),
        ("[[ink|white]] and [[#FFD166|gold]]", "white and gold"),
        ("Normal text without markup", "Normal text without markup"),
    )
    negative = (
        "Unclosed [[accent|text", "[[accent|]]", "[[fake|invalid]]",
        "[[accent|outer [[ink|inner]]]]", "[[#000000|invisible]]",
        "[[accent|unclosed text]] ]]",
    )
    for value, expected in positive:
        try:
            if validate_emphasis(value) != expected:
                failures.append("plain-text rendering regression: " + value)
        except ValueError as exc:
            failures.append("valid emphasis was rejected: " + str(exc))
    for value in negative:
        try:
            validate_emphasis(value)
            failures.append("invalid emphasis was accepted: " + value)
        except ValueError:
            pass
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
                for language, text in (("en", en), ("ko", ko)):
                    if text:
                        try:
                            validate_emphasis(text)
                        except ValueError as exc:
                            failures.append(f"bad highlight syntax in {key} ({language}): {exc}")
                translations[key] = {"en": en or "", "ko": ko or ""}
    except (OSError, csv.Error) as exc:
        print("[FAIL] cannot parse CSV:", exc)
        return 1

    files = {name: (ROOT / name).read_text(encoding="utf-8") for name in FILES}
    required: set[str] = set()
    for name, source in files.items():
        for regex in (
            r'\bt\("([A-Za-z0-9._-]+)"\)',
            r'\bdata-i18n-(?:key|rich|split|alt|aria-label)="([A-Za-z0-9._-]+)"',
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
    hero = files["src/pages/index.astro"]
    loader = (ROOT / "src/lib/i18n.ts").read_text(encoding="utf-8")
    if 'data-i18n-rich="home.hero.title"' not in hero or 'richParts("home.hero.title")' not in hero:
        failures.append("Home headline must use editable rich text, not last-word logic")
    if "heroLastSpace" in hero or 'lastIndexOf(" ")' in switcher:
        failures.append("legacy positional highlighting is still present")
    if '"[data-i18n-rich]"' not in switcher or '"[data-i18n-key]"' not in switcher:
        failures.append("locale switcher cannot apply arbitrary highlighted segments")
    if "document.createTextNode" not in switcher or "replaceChildren" not in switcher:
        failures.append("rich text must render via safe DOM nodes, not HTML injection")
    if "parseStyledText" not in loader or "insufficient contrast" not in loader:
        failures.append("build-time emphasis validation missing")
    if "home.hero.title" not in translations or "[[accent|" not in translations["home.hero.title"]["en"]:
        failures.append("English homepage heading lacks explicit CSV highlight")
    if "home.hero.title" not in translations or "[[accent|" not in translations["home.hero.title"]["ko"]:
        failures.append("Korean homepage heading lacks independent CSV highlight")
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
    print(f"[PASS] {len(translations)} keys with complete EN/KO text, safe colors and matching placeholders")
    print(f"[PASS] {len(required)} direct/dynamic references resolve, all approved Works covered")
    print("[PASS] single-route switcher, localStorage, translated metadata/accessibility and filters")
    print("[NOTE] Browser QA still required for locale persistence, mobile overflow and Astro build.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
