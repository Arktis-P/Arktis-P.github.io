# Phase 4 — Astro Static Website Implementation

> 2026-10-25 · branch: `gpt/site-redesign-implementation`
> Scope: Home, Works, Detail, CSS and protected legacy URLs. **No production deployment**.

## Implemented pages

| Route | Astro source | Functional scope |
| --- | --- | --- |
| `/` | `src/pages/index.astro` | Editable hero (headline, intro, CTA), selected featured works, Markdown About, Gmail contact |
| `/works/` | `src/pages/works/index.astro` | Approved Works, editable order, client-side All/Games/Software/Experiments filter; empty state |
| `/works/anvil-bastion/` | `src/pages/works/[slug]/index.astro` | Game info, **Google Play** primary CTA, policy link, optional images |
| `/works/virtualqhdmirror/` | Same dynamic Astro detail template | Software info, **GitHub** primary CTA, optional images |
| `/privacy.html` | `public/privacy.html` | Original policy text with **only** four approved support-email substitutions |
| `/app-ads.txt` | `public/app-ads.txt` | Exact bytes of production AdMob authorization |
| `/404.html` | `src/pages/404.astro` | Not-found page, Works link |

Published content is exclusively `content/works/*.md` with `draft: false`. **Other personal projects remain excluded**. Root `index.html`, `privacy.html`, `app-ads.txt` remain untouched in the source branch. Astro ignores the old root `index.html` and builds from `src/pages/index.astro`.

Media paths are documented in [ASSET_GUIDE.md](ASSET_GUIDE.md). If a brand visual, cover or screenshot file does not exist, the Astro component displays a CSS text placeholder or skips the gallery. No paid image service, CDN, backend or CMS is required.

## Local Windows setup

Astro 7.4.2 (fixed exact version in `package.json`) requires **Node.js 22.23.4 or later**. Check `node -v`. If lower, update Node.js on the local PC before continuing. This avoids hosted compute costs.

```powershell
git fetch origin
git switch gpt/site-redesign-implementation
node --version
npm install
npm run dev
```

Open `http://localhost:4321/`, `http://localhost:4321/works/`, `http://localhost:4321/works/anvil-bastion/`, and `http://localhost:4321/works/virtualqhdmirror/`.

To test the final static output:

```powershell
npm run build
py scripts/check_site_baseline.py
py scripts/check_phase3_content.py
py scripts/check_phase4_source.py --dist
npm run preview
```

The default preview server also uses localhost port 4321 (or the next free port). **After the first successful `npm install`, commit the generated `package-lock.json` with an emoji-prefixed checkpoint message** for reproducible future builds.

## Release pathway (NOT EXECUTED)

- GitHub Pages currently serves a `main` root site. A new Astro source tree **does not** replace its public index just by pushing `main`.
- Astro's official automatic Pages solution uses Actions, but the repo owner opted out of new hosted CI. Prepare a **manual local build** of `dist/`, commit **only the generated static output** to a designated publishing branch after approval, then adjust GitHub Pages publishing settings in a separate release checkpoint.
- Do **not** replace existing production or change Pages source without explicit approval. Keep `/privacy.html` and `/app-ads.txt` stable and test them before/after switching.
- The source branch remains `gpt/site-redesign-implementation`. Do not make a PR unless the owner requests it.

## Functional and visual QA checklist

- [ ] Source-only check: `py scripts/check_phase4_source.py`.
- [ ] `npm install` and `npm run build` complete without errors.
- [ ] `py scripts/check_phase4_source.py --dist` passes all routes, links and protected bytes.
- [ ] Home hero, featured Anvil Bastion, About, Contact, Footer render correctly.
- [ ] Works All/Games/Software/Experiments filter buttons change visible items; zero matches show a message.
- [ ] Google Play and GitHub buttons open correct official/existing destinations.
- [ ] Desktop (e.g. 1440 px) and mobile (390 px) have no clipping/overflow and clear focus styles.
- [ ] Drop-in brand/cover/screenshot display, and missing files safely fallback.
- [ ] Verify Gmail appears in home/footer and new policy; no Proton address in built output.
- [ ] Verify privacy content and app-ads bytes remain correct on the eventual live URL.

## Source checks completed in connected repository

- Verified the default Works output is limited to the two approved content files.
- Simulated the Works client-side category filter (All, Games, empty Experiments) in JavaScript; all three behavior cases passed.
- Checked the links, Gmail binding, media placeholders, static build configuration, mobile/reduced-motion CSS, root-file preservation and exact contact-only policy substitution. This is source-level evidence, **not** a successful Astro build or rendered-browser test.

## Validation honesty

At authoring time, the GitHub connector can write and read the code, and static contract/source audits can be performed without hosted infrastructure. **The current assistant execution environment cannot download npm dependencies**, so an actual Astro build and Playwright screenshot review were **not completed**. This is a concrete gate, not a claim that build succeeded. Completion of the implementation source should not be confused with release-ready verified output.

## Phase 4 extension — brand and localization (2026-10-25)

- Logo reference: vibrant flame red/black/white; UI palette uses `#FF5344` accent, `#0C0D10` background, `#F5F7FA` foreground. Cards/content keep a high-contrast neutral surface.
- Every current visible UI/description paragraph is now an EN/KO CSV key, including menu, filters, Home copy, About, two work titles/summary/details, 404, meta description/title and accessibility labels.
- The header locale selector remembers EN/KO via localStorage and never changes the route. The no-JS static default remains English.
- `content/about.md` removed; translated copy in `content/i18n/strings.csv`. Structure/links are still in Markdown/YAML.
- Run `py scripts/check_i18n_content.py` before `npm run build`; see [TEXT_I18N_GUIDE.md](TEXT_I18N_GUIDE.md).
- Actual Astro compilation and responsive screenshot QA are still separate release gates; no hosted CI or deployment initiated.
