#!/usr/bin/env python3
"""Phase 1 offline baseline checks; uses only Python's standard library."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_BLOBS = {
    "privacy.html": "adb10a5116c033c092fc2fc36b50eeb0d3c20a68",
    "app-ads.txt": "a895dcf3f08d0ceae76bba64205f6a1e17ab9808",
}


def blob_sha(data: bytes) -> str:
    """Compute a Git blob object's SHA-1 (not the raw file SHA-1)."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def canonical_checkout_bytes(data: bytes) -> bytes:
    """Normalize ONLY Windows CRLF checkouts to Git's original LF bytes.

    The normalized content still must match the pinned original Git blob SHA;
    arbitrary content edits, added spaces and non-newline mutations still fail.
    """
    return data.replace(b"\r\n", b"\n")


def main() -> int:
    failures: list[str] = []
    checks: list[str] = []
    for name in ("AGENTS.md", "README.md", "docs/SITE_REDESIGN_PLAN.md",
                 "docs/PHASE1_BASELINE_AUDIT.md", "index.html"):
        if (ROOT / name).is_file():
            checks.append(f"[PASS] {name} exists")
        else:
            failures.append(f"[FAIL] {name} missing")
    for name, expected in PROTECTED_BLOBS.items():
        origin = ROOT / name
        publish = ROOT / "public" / name
        if not origin.is_file():
            failures.append(f"[FAIL] missing protected root {name}")
            continue
        original = origin.read_bytes()
        canonical = canonical_checkout_bytes(original)
        if blob_sha(canonical) != expected:
            failures.append(
                f"[FAIL] original {name} changed beyond Windows CRLF normalization "
                f"(expected protected Git blob {expected}, "
                f"actual normalized {blob_sha(canonical)})")
        elif original != canonical:
            checks.append(f"[PASS] original {name} matches protected Git blob "
                          f"after Windows CRLF normalization")
        else:
            checks.append(f"[PASS] original {name} matches protected Git blob")
        if not publish.is_file():
            failures.append(f"[FAIL] missing public/{name} (Astro output source)")
            continue
        published = canonical_checkout_bytes(publish.read_bytes())
        if name == "privacy.html":
            # Only allow the approved email substitutions, plus checkout CRLF.
            approved = canonical.replace(b"burningarktis@proton.me",
                                         b"burningarktis@gmail.com")
            ok = (b"burningarktis@proton.me" in canonical
                  and b"burningarktis@gmail.com" in published
                  and published == approved)
        else:
            ok = published == canonical
        if ok:
            checks.append(f"[PASS] public/{name} equals approved protected variant")
        else:
            failures.append(f"[FAIL] public/{name} differs beyond authorized changes")
    home = ROOT / "index.html"
    if home.is_file():
        html = home.read_text(encoding="utf-8")
        if 'href="/privacy.html"' in html:
            checks.append("[PASS] root homepage includes /privacy.html link")
        else:
            failures.append("[FAIL] root homepage lacks /privacy.html link")

    for item in checks + failures:
        print(item)
    print(f"Phase 1 baseline: {len(checks)} passed; {len(failures)} failed.")
    print("Offline only: live Pages and future generated dist/ are NOT tested.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
