# Phase 3 — Content schema and local media contract

> Working branch: `gpt/site-redesign-implementation` · Review date: 2026-10-25
> Status: **CONTENT SCHEMA READY**. This is the content-model stage, **not** the full production Astro page implementation.

## Files editors may change

| File | Purpose |
| --- | --- |
| `content/home.yml` | Public studio name, hero text, featured work slugs |
| `content/about.md` | Short, factual studio introduction |
| `content/contact.yml` | Verified public support email and GitHub links |
| `content/works/anvil-bastion.md` | Game copy, category, prominence, Google Play link |
| `content/works/virtualqhdmirror.md` | Software copy, category, GitHub link |
| `public/images/…` | New images, recognized by exact filename (see [Asset Guide](ASSET_GUIDE.md)) |

The content collection schema is in `src/content.config.ts`. Astro's recommended Content Layer API uses `glob()` and `file()` loaders and Zod validation. The software category does not claim studio-issued distribution; its attribution is the verified public Arktis-P repository.

## Editing rules

- Public works = every `content/works/*.md` entry with `draft: false`. `draft: true` excludes work from published pages.
- `category` = `game`, `software`, or `experiment`. Header navigation stays Home and Works only.
- `featured: true` may be shown on Home; `featured_works` in `home.yml` is the editorial ordering list. For initial Home, only Anvil Bastion is featured.
- `order` is the Works sorting key (lower first, then slug). It is not visible as a public number.
- Every primary action has a **platform label** and verified HTTPS URL: `Google Play` or `GitHub`.
- Secondary actions use a site-relative route (e.g. `/privacy.html`) or HTTPS. Public support email comes from `contact.yml`, not copied into each work.
- File name and frontmatter `slug` must match. No private data, unknown release dates, fake publisher claims or unpublished features.
- `home.yml` and `contact.yml` are single-element **YAML arrays** with `id: home` and `id: contact`. This is intentional for Astro `file()` loader.
- If the user later explicitly approves another work, add a Markdown file with the same frontmatter keys and its own verified primary link.
- No images required to pass this stage; image lookup is automatic via `src/lib/media.ts` at **build time**.

## Images: drop-in filenames

See **[ASSET_GUIDE.md](ASSET_GUIDE.md)** for the exact path, format and pixel dimensions. No YAML or TypeScript changes are necessary when only adding a cover, screenshots or logo. The build-time media helper omits missing images and supports design placeholders.

## Safety / release

- Approved new-site contact: `burningarktis@gmail.com` (Google Play developer support). The old main website and policy still show Proton Mail; don't present them as updated until the separately approved live release.
- `main/index.html`, `main/privacy.html`, `main/app-ads.txt` remain untouched at this checkpoint. **Before a new-site release**, create and review a contact-only amendment to `privacy.html` and verify the AdMob line is untouched. Do not publish two contradictory support contacts.
- No PR, Actions, hosted CI, paid dependencies or production deployment created for this schema checkpoint.
- Astro npm dependencies, templates and full build are Phase 4; **do not claim an Astro build passed during Phase 3**.
- GitHub Pages's source is currently documented as `main` root. The eventual deployment can be planned for locally-generated static output and GitHub Pages branch publishing without introducing GitHub Actions, subject to confirming repository settings and explicit user approval.

## Checkpoint tests

```powershell
git switch gpt/site-redesign-implementation
py scripts/check_site_baseline.py
py scripts/check_phase2_wireframe.py
py scripts/check_phase3_content.py
```

These tests require only Python's standard library. Actual Astro compilation and real web-browser visual checks belong to Phase 4.

## Phase 4 integration update (2026-10-25)
The `src/pages/` templates and `src/components/` views are now connected to these collection definitions. Home headline, featured Works, public contact, Works list, project details and optional media are consumed from the content files and local media resolver. New-site `public/privacy.html` keeps all original policy wording while substituting the authorized Gmail contact only; the protected root `privacy.html` remains unchanged. Source/logic tests passed; actual Astro build is **not** yet verified in the assistant environment (offline npm and older Node).
