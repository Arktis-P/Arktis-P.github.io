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

## Phase 3: editable content and future image uploads

- [Image names, directories and pixel dimensions](docs/ASSET_GUIDE.md) — copy new files to `public/images/` using exact names; absent files fall back gracefully when production page templates are implemented.
- [Content schema and editing guide](docs/PHASE3_CONTENT_SCHEMA.md) — `content/home.yml`, `content/i18n/strings.csv`, `content/contact.yml`, `content/works/*.md`.
- Technical contracts: `src/content.config.ts` (Astro Content Collections) and `src/lib/media.ts` (local build-time asset lookup).
- No installation required for contract check: `py scripts/check_phase3_content.py`.

**Phase status:** content/data schema only; Astro pages, npm setup and actual build/visual QA are Phase 4. No production site is deployed from the feature branch.

## Phase 4: runnable Astro website (source branch only)

The source pages for Home, Works, and both approved project detail routes are now implemented in Astro and use the content files above. **Live GitHub Pages is unchanged.** Build verification is still required before release.

```powershell
git fetch origin
git switch gpt/site-redesign-implementation
node -v  # must be >=22.23.4
npm install
npm run build
py scripts/check_site_baseline.py
py scripts/check_phase3_content.py
py scripts/check_phase4_source.py --dist
npm run preview
```

See [Phase 4 Implementation and QA](docs/PHASE4_IMPLEMENTATION.md) for the test matrix and no-Actions publishing boundary. Commit the generated `package-lock.json` after the first successful local install, using an emoji-prefixed checkpoint commit. No PR or hosted CI is needed.

## Redesign references

- [Plan](docs/SITE_REDESIGN_PLAN.md)
- [Phase 1 baseline audit, route inventory and test checklist](docs/PHASE1_BASELINE_AUDIT.md)
- [Working rules](AGENTS.md)
- Free, offline baseline check: `py scripts/check_site_baseline.py`

Implementation branch: `gpt/site-redesign-implementation`, forked from the planning branch. Do not confuse branch commits with public deployment.

## Bilingual text editing (EN/KO)

All displayed copy, including About and project descriptions, is editable in `content/i18n/strings.csv`. The header language control switches without creating separate page URLs and remembers the choice. Configuration/data fields remain in `content/home.yml`, `content/works/*.md`, and `content/contact.yml`.

**[한국어 사용 안내 — 텍스트 관리 및 언어 전환](docs/TEXT_I18N_GUIDE.md)**

```powershell
py scripts/check_i18n_content.py
```

## SpriteForge portfolio entry

SpriteForge (`https://spriteforge.cc/`) is included as a third published work in the **Software** category, linking to the live service rather than its private 비공개 소스 저장소 source repository. Its text is in `content/i18n/strings.csv`; its optional images are documented in `docs/ASSET_GUIDE.md`. The new detail route is `/works/spriteforge/`.
