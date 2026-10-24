# Burning Arktis — Official Site (Current: Anvil Bastion)

> **Development rules:** Read [AGENTS.md](AGENTS.md) before editing. Use emoji-prefixed commits at each checkpoint, feature branches, no PR or new paid/hosted CI by default, and no `main` deploy without approval.

Official public site for Burning Arktis / Anvil Bastion. A broader team portfolio redesign is being developed separately from the current production source.

- Public website: https://arktis-p.github.io/
- Anvil Bastion privacy policy: https://arktis-p.github.io/privacy.html
- AdMob app-ads authorization: https://arktis-p.github.io/app-ads.txt
- New-site public support email (verified on Google Play): burningarktis@gmail.com

**Migration note:** the unchanged `main/index.html` and `main/privacy.html` currently show the legacy Proton Mail address. They are production-protected until the redesigned site and the contact-only privacy-policy amendment are approved for release. Do not treat the legacy contact as the new-site address.

## Existing production source

The currently documented GitHub Pages configuration publishes from the `main` branch, repository root, with HTTPS. The repository's root contains:

- `index.html` — current Anvil Bastion developer/support page.
- `privacy.html` — existing privacy policy. Preserve its URL and contents unless explicitly approved.
- `app-ads.txt` — **already contains the personalized AdMob authorization line**. It is not a placeholder. Preserve its URL and contents unless explicitly approved.

The exact live Pages settings/HTTP responses still need manual verification; see the Phase 1 audit. Do not modify these protected files merely to redesign the homepage.

## Phase 2: visual review (development branch only)

- [Interactive standalone wireframe](docs/wireframes/index.html) — Home, Works and Work Detail, browser-openable with zero installation.
- [Preview instructions](docs/wireframes/README.md) — open on Windows and complete desktop/mobile checklist.
- [Wireframe specification](docs/PHASE2_WIREFRAME_SPEC.md) — visual rules and information architecture.
- [Works scope/evidence ledger](docs/PHASE2_WORKS_SCOPE.md) — approved baseline vs. review-only candidates.
- Offline static check: `py scripts/check_phase2_wireframe.py`.

The candidate entries inside the design preview are **not approved for publication**. Work happens on `gpt/site-redesign-implementation`. No PR, hosted CI or deployment is involved.

## Redesign references

- [Plan](docs/SITE_REDESIGN_PLAN.md)
- [Phase 1 baseline audit, route inventory and test checklist](docs/PHASE1_BASELINE_AUDIT.md)
- [Working rules](AGENTS.md)
- Free, offline baseline check: `py scripts/check_site_baseline.py`

Implementation branch: `gpt/site-redesign-implementation`, forked from the planning branch. Do not confuse branch commits with public deployment.
