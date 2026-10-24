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
        candidates = [path for path in (ROOT / name, ROOT / "public" / name)
                      if path.is_file()]
        if not candidates:
            failures.append(f"[FAIL] {name} missing from root and public/")
            continue
        for path in candidates:
            actual = blob_sha(path.read_bytes())
            display = path.relative_to(ROOT).as_posix()
            if actual == expected:
                checks.append(f"[PASS] {display}: protected Git blob unchanged")
            else:
                failures.append(
                    f"[FAIL] {display}: baseline {expected}, actual {actual}")
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
