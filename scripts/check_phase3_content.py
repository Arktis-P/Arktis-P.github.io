#!/usr/bin/env python3
"""Offline Phase 3 content/asset contract checks (Python standard library only)."""
from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKS = ROOT / "content" / "works"
VALID_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GMAIL = "burningarktis@gmail.com"
GOOGLE_PLAY = "https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion"
GITHUB = "https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md"

# Exact accepted names and dimensions; screenshots are individually optional.
DIMENSIONS: dict[str, tuple[int, int]] = {
    "brand/wordmark.png": (1200, 300),
    "brand/mark.png": (512, 512),
    "brand/hero.webp": (1920, 1080),
    "works/anvil-bastion/cover.webp": (1280, 720),
    "works/virtualqhdmirror/cover.webp": (1280, 720),
}
for number in range(1, 7):
    DIMENSIONS[f"works/anvil-bastion/shot-{number:02}.webp"] = (1080, 1920)
    DIMENSIONS[f"works/virtualqhdmirror/shot-{number:02}.webp"] = (1600, 900)


def image_size(path: Path) -> tuple[int, int] | None:
    """Parse only PNG and WebP file dimensions without external dependencies."""
    data = path.read_bytes()
    if path.suffix == ".png":
        if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
            return struct.unpack(">II", data[16:24])
        return None
    if len(data) < 30 or data[0:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    kind = data[12:16]
    if kind == b"VP8X":
        return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
    if kind == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
        return (int.from_bytes(data[26:28], "little") & 0x3fff,
                int.from_bytes(data[28:30], "little") & 0x3fff)
    if kind == b"VP8L" and data[20] == 0x2f:
        bits = int.from_bytes(data[21:25], "little")
        return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
    return None


def header(content: str) -> str | None:
    if not content.startswith("---\n"):
        return None
    sections = content.split("---\n", 2)
    return sections[1] if len(sections) == 3 else None


def value(block: str, name: str) -> str | None:
    match = re.search(r"^" + re.escape(name) + r":\s*(.*?)\s*$", block, re.MULTILINE)
    return match.group(1).strip("\"'") if match else None


def main() -> int:
    errors: list[str] = []
    notices: list[str] = []

    home = (ROOT / "content/home.yml").read_text(encoding="utf-8")
    contact = (ROOT / "content/contact.yml").read_text(encoding="utf-8")
    if home.count("id: home") != 1 or "featured_works:" not in home:
        errors.append("home.yml must have one home entry and featured works list")
    if "anvil-bastion" not in home:
        errors.append("home.yml must feature the verified game")
    if contact.count("id: contact") != 1 or f"email: {GMAIL}" not in contact:
        errors.append("contact.yml must contain the one verified Gmail address")
    if "proton.me" in contact.lower():
        errors.append("legacy Proton contact found in new-site contact data")
    if "/privacy.html" not in contact or "https://github.com/Arktis-P" not in contact:
        errors.append("contact.yml is missing existing public routes")

    expected = {
        "anvil-bastion": ("game", "Google Play", GOOGLE_PLAY),
        "virtualqhdmirror": ("software", "GitHub", GITHUB),
    }
    found: set[str] = set()
    for path in sorted(WORKS.glob("*.md")):
        name = path.stem
        body = header(path.read_text(encoding="utf-8"))
        if body is None:
            errors.append(f"{path.name} frontmatter missing")
            continue
        slug = value(body, "slug")
        if not slug or not VALID_SLUG.fullmatch(slug) or slug != name:
            errors.append(f"{path.name} slug must match lowercase file name")
        if name not in expected:
            if value(body, "draft") == "false":
                errors.append(f"unapproved published work: {name}")
            continue
        if value(body, "draft") != "false":
            errors.append(f"approved {name} must have draft: false")
        for field in ("title", "summary", "attribution", "featured", "order", "status", "platforms", "links"):
            if value(body, field) is None and (field + ":") not in body:
                errors.append(f"{name} missing {field}")
        category, label, url = expected[name]
        if value(body, "category") != category:
            errors.append(f"{name} category should be {category}")
        if f"label: {label}" not in body or f"url: {url}" not in body:
            errors.append(f"{name} primary link incorrect")
        found.add(name)
    if found != set(expected):
        errors.append(f"approved work files mismatch: {sorted(found)}")

    for relative, expected_size in DIMENSIONS.items():
        filename = ROOT / "public/images" / relative
        if not filename.exists():
            continue  # Images are optional until supplied by the user.
        try:
            actual = image_size(filename)
        except OSError as exc:
            errors.append(f"cannot read {relative}: {exc}")
            continue
        if actual != expected_size:
            errors.append(f"{relative} dimensions {actual}, expected {expected_size}")
        else:
            notices.append(f"image OK: {relative} = {actual[0]}x{actual[1]}")
    for filename in (ROOT / "public/images").rglob("*"):
        if not filename.is_file() or filename.name == ".gitkeep":
            continue
        relative = filename.relative_to(ROOT / "public/images").as_posix()
        if relative not in DIMENSIONS:
            errors.append(f"unrecognized public image path: {relative}")

    schema = (ROOT / "src/content.config.ts").read_text(encoding="utf-8")
    media = (ROOT / "src/lib/media.ts").read_text(encoding="utf-8")
    for required in ('defineCollection', 'glob(', 'file(', 'draft:', 'featured:', 'category:'):
        if required not in schema:
            errors.append(f"missing Astro schema fragment: {required}")
    for required in ('getBrandMedia', 'getWorkMedia', 'shot-', 'cover.webp', 'wordmark.png'):
        if required not in media:
            errors.append(f"missing media helper fragment: {required}")

    for msg in notices:
        print("[PASS]", msg)
    if errors:
        for err in errors:
            print("[FAIL]", err)
        print(f"Phase 3: {len(errors)} failure(s).")
        return 1
    print("[PASS] approved 2-work content contract and verified Gmail contact")
    print("[PASS] image paths/dimensions valid for all currently supplied assets (optional absent files allowed)")
    print("[PASS] Astro content schema and local media lookup sources present")
    print("[NOTE] Python check is not an Astro compiler/build; run npm build after Phase 4.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
