#!/usr/bin/env python3
"""Publish the locally VERIFIED Astro dist/ to the existing GitHub Pages main root.

This script NEVER deploys unbuilt Astro source, creates workflows/PRs,
or modifies the development branch. Requires a local clone, Python, Node
and the existing git credentials. Use --publish only after --dry-run passes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SOURCE_BRANCH = "gpt/site-redesign-implementation"
MAIN_BRANCH = "main"
EXPECTED_REPO = "arktis-p/arktis-p.github.io"
PUBLISH_FILES = (
    "index.html",
    "works/index.html",
    "works/anvil-bastion/index.html",
    "works/virtualqhdmirror/index.html",
    "works/spriteforge/index.html",
    "privacy.html",
    "app-ads.txt",
    "404.html",
)
PUBLIC_PROTECTION_FILES = ("privacy.html", "app-ads.txt")
EXPECTED_LINKS = {
    "works/anvil-bastion/index.html": "https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion",
    "works/virtualqhdmirror/index.html": "https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md",
    "works/spriteforge/index.html": "https://spriteforge.cc/",
}
MANIFEST_FILE = "DEPLOYED_FILES.txt"
RELEASE_FILE = "RELEASE_INFO.json"
EXCLUDED_PREFIXES = ("images/original/",)


class PublishError(RuntimeError):
    pass


def run(*args: str, cwd: Path, capture: bool = False) -> str:
    print(">", " ".join(args))
    proc = subprocess.run(
        args, cwd=cwd, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=False,
    )
    if proc.returncode:
        tail = (proc.stderr or proc.stdout or "").strip()
        raise PublishError(f"Command failed ({proc.returncode}): {' '.join(args)}\n{tail}")
    return (proc.stdout or "").strip()


def git(repo: Path, *args: str, capture: bool = False) -> str:
    return run("git", *args, cwd=repo, capture=capture)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise PublishError(reason)


def validate_repo(repo: Path) -> tuple[str, str]:
    root = Path(git(repo, "rev-parse", "--show-toplevel", capture=True)).resolve()
    require(root == repo, f"Run this tool from repository root: {root}")
    remote = git(repo, "remote", "get-url", "origin", capture=True)
    normalized = re.sub(r"^git@github\.com:", "", remote).replace("https://github.com/", "").rstrip("/")
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    require(normalized.lower() == EXPECTED_REPO, "origin is not Arktis-P/Arktis-P.github.io")
    branch = git(repo, "branch", "--show-current", capture=True)
    require(branch == SOURCE_BRANCH, f"Check out {SOURCE_BRANCH} before publishing (now: {branch})")
    # Refuse tracked edits; prevent compiling unreproducible unpublished work.
    dirty = git(repo, "status", "--porcelain", "--untracked-files=no", capture=True)
    require(not dirty, f"Uncommitted tracked changes must be committed or saved first:\n{dirty}")
    git(repo, "fetch", "origin", SOURCE_BRANCH, MAIN_BRANCH)
    head = git(repo, "rev-parse", "HEAD", capture=True)
    remote_head = git(repo, "rev-parse", f"origin/{SOURCE_BRANCH}", capture=True)
    require(head == remote_head, "Local source differs from origin feature branch. Fetch/push first.")
    main_head = git(repo, "rev-parse", f"origin/{MAIN_BRANCH}", capture=True)
    return head, main_head


def validate_output(repo: Path) -> tuple[Path, list[str]]:
    dist = repo / "dist"
    require(dist.is_dir(), "Missing dist/; run npm run build first")
    for rel in PUBLISH_FILES:
        require((dist / rel).is_file(), "Missing built page / file: dist/" + rel)
    require("burningarktis@gmail.com" in (dist / "index.html").read_text(encoding="utf-8"),
            "Home is missing the approved Gmail address")
    require("proton.me" not in (dist / "privacy.html").read_text(encoding="utf-8").lower(),
            "Built privacy file still contains the old Proton address")
    for filename in PUBLIC_PROTECTION_FILES:
        current = (dist / filename).read_bytes()
        approved = (repo / "public" / filename).read_bytes()
        require(current == approved, f"dist/{filename} differs from the approved source")
    for rel, link in EXPECTED_LINKS.items():
        html = (dist / rel).read_text(encoding="utf-8")
        require(link in html, f"Built {rel} missing expected outbound link: {link}")
    works = (dist / "works/index.html").read_text(encoding="utf-8")
    for name in ("Anvil Bastion", "VirtualQHDMirror", "SpriteForge"):
        require(name in works, f"Missing approved work in Works listing: {name}")
    files: list[str] = []
    for file in sorted(dist.rglob("*")):
        if file.is_symlink():
            raise PublishError(f"Symlinks are not allowed in dist: {file}")
        if not file.is_file():
            continue
        relative = file.relative_to(dist).as_posix()
        if any(relative.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue  # source logo references aren't live page assets
        if relative.startswith(".git/") or relative in (MANIFEST_FILE, RELEASE_FILE):
            raise PublishError("dist contains a reserved publish path: " + relative)
        files.append(relative)
    require(all(x in files for x in PUBLISH_FILES), "Required output file excluded")
    require(any(x.startswith("_astro/") for x in files), "No Astro asset bundle found in dist/_astro")
    return dist, files


def local_qa(repo: Path) -> None:
    print("\n[1/3] Running the existing offline checks")
    for filename in ("check_site_baseline.py", "check_i18n_content.py", "check_phase3_content.py"):
        run(sys.executable, "scripts/" + filename, cwd=repo)
    print("\n[2/3] Building the actual Astro site")
    npm = shutil.which("npm.cmd" if os.name == "nt" else "npm")
    require(npm is not None, "npm not found; install/update Node.js")
    run(npm, "run", "build", cwd=repo)
    print("\n[3/3] Checking generated HTML, links, privacy, AdMob")
    run(sys.executable, "scripts/check_phase4_source.py", "--dist", cwd=repo)


def safe_manifest_paths(base: Path) -> list[Path]:
    manifest = base / MANIFEST_FILE
    if not manifest.exists():
        return []
    output: list[Path] = []
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        value = raw.strip()
        if not value:
            continue
        candidate = Path(value)
        require(not candidate.is_absolute() and ".." not in candidate.parts and
                value not in {"README.md", "CNAME"},
                "Unsafe entry in previous deployment manifest: " + value)
        output.append(base / candidate)
    return output


def deploy(repo: Path, dist: Path, files: list[str], source_head: str, old_main: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    release = {
        "source_branch": SOURCE_BRANCH,
        "source_commit": source_head,
        "published_at_utc": timestamp,
        "renderer": "Astro npm run build (locally verified)",
        "asset_policy": "images/original/ excluded from live site",
    }
    with tempfile.TemporaryDirectory(prefix="burning-arktis-pages-") as folder:
        worktree = Path(folder) / "publish"
        git(repo, "worktree", "add", "--detach", str(worktree), old_main)
        try:
            require(git(worktree, "rev-parse", "HEAD", capture=True) == old_main,
                    "Remote main changed before staging")
            # Remove ONLY files listed as deployed in a previous release.
            for p in safe_manifest_paths(worktree):
                if p.is_symlink():
                    raise PublishError("Symlink in release manifest: " + str(p))
                if p.is_file():
                    p.unlink()
            for rel in files:
                dest = worktree / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dist / rel, dest)
            (worktree / ".nojekyll").write_bytes(b"")
            (worktree / RELEASE_FILE).write_text(
                json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            (worktree / MANIFEST_FILE).write_text(
                "\n".join(sorted([*files, ".nojekyll", RELEASE_FILE])) + "\n",
                encoding="utf-8",
            )
            git(worktree, "add", "-A")
            staged = git(worktree, "diff", "--cached", "--name-only", capture=True)
            require("index.html" in staged and "privacy.html" in staged,
                    "Unexpected publish diff; refused to push")
            print("\nFiles staged for deployment:\n" + staged)
            git(worktree, "commit", "-m",
                "🚀 deploy(site): publish verified Astro static release " + source_head[:7])
            commit = git(worktree, "rev-parse", "HEAD", capture=True)
            # Fast-forward-only server protection. NEVER force-push main.
            git(worktree, "push", "origin", "HEAD:refs/heads/main")
            print("\nPublished main commit:", commit)
            return commit
        finally:
            git(repo, "worktree", "remove", "--force", str(worktree))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify local Astro build; optionally publish dist/ to GitHub Pages main root"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Build and QA only; do not push")
    mode.add_argument("--publish", action="store_true", help="Build, QA and push static dist to main")
    args = parser.parse_args()
    repo = Path.cwd().resolve()
    try:
        source_head, main_head = validate_repo(repo)
        local_qa(repo)
        dist, files = validate_output(repo)
        print(f"\n[PASS] Validated {len(files)} generated files from {source_head[:12]}")
        print("Protection: privacy.html / app-ads.txt preserved; no new Actions, PR or paid CI.")
        if args.dry_run:
            print("[DRY RUN] Nothing published. Run with --publish to deploy.")
            return 0
        commit = deploy(repo, dist, files, source_head, main_head)
        print(f"[PUSHED] {commit} to main. Check https://arktis-p.github.io/ after GitHub Pages deploys.")
        return 0
    except PublishError as exc:
        print("\n[STOP] " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
