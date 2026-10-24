# Phase 2 — Wireframe & Interaction Specification

> Concept: `Editorial / studio dossier` · 2026-10-24 · draft for user visual review
> Detailed reference: [SITE_REDESIGN_PLAN.md](SITE_REDESIGN_PLAN.md).
> Publication scope/evidence: [PHASE2_WORKS_SCOPE.md](PHASE2_WORKS_SCOPE.md).

## Goal / visual hierarchy
A credible indie studio website emphasizing actual works instead of aspirational company claims. Use Berker Games for economical content ordering and Aggro Crab only for deliberate typographic rhythm and strong project presence; do not copy their assets, branding, layout composition or code.

- **Navigation:** header wordmark + exactly `Home` and `Works`. Work-detail is a nested view, not another top-level nav tab.
- **Home:** hero with studio name / short neutral English line / view works → **Featured Work** (Anvil Bastion) → **About** (small fact-safe explanation) → **Contact & Support** → footer legal links.
- **Works:** page title and short explanation → `All / Games / Software / Experiments` categories → explicit card grid and separate review-only state for pending candidates. Empty filter must be a friendly explanation, not a blank screen.
- **Detail:** back to Works → category + approval state + title → landscape key art placeholder → brief confirmed description → minimal fact panel → verified actions only → more works / footer. Never imply missing media exist.
- **Legal:** support email and original `/privacy.html` prominently linked; exact `/app-ads.txt` route preserved for hosting, not necessarily promoted as a primary visitor CTA.

## Draft desktop wireframes

```text
HOME — desktop (~1440 px; content max ~1160)
┌───────────────────────────────────────────────────────────┐
│ BURNING / ARKTIS                      Home   Works         │
├───────────────────────────────────────────────────────────┤
│ INDEPENDENT GAME & SOFTWARE STUDIO      ┌──────────────┐  │
│                                         │ abstract     │  │
│ Games, software                         │ visual       │  │
│ & creative experiments.                 │ placeholder  │  │
│ [Explore works →]                       └──────────────┘  │
├───────────────────────────────────────────────────────────┤
│ FEATURED WORK                                              │
│ [ Anvil Bastion visual placeholder ]  [copy + View details]│
├───────────────────────────────────────────────────────────┤
│ ABOUT                         CONTACT & SUPPORT            │
│ neutral, fact-safe summary    public mail / GitHub         │
├───────────────────────────────────────────────────────────┤
│ Copyright       Privacy Policy / support                    │
└───────────────────────────────────────────────────────────┘

WORKS
┌───────────────────────────────────────────────────────────┐
│ BURNING / ARKTIS                       Home   Works         │
│ OUR WORKS  / neutral description                           │
│ [ All ] [ Games ] [ Software ] [ Experiments ]              │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│ │ ANVIL BASTION  │ │ VQM / REVIEW   │ │ PIXEL / REVIEW │   │
│ └────────────────┘ └────────────────┘ └────────────────┘   │
└───────────────────────────────────────────────────────────┘

DETAIL
┌───────────────────────────────────────────────────────────┐
│ BURNING / ARKTIS                       Home   Works         │
│ ← Back to Works                                            │
│ GAME / TITLE                          [verified link only]  │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ key art / brand-safe abstract placeholder            │ │
│ └───────────────────────────────────────────────────────┘ │
│ Introduction                 Facts / links                  │
│ More works / footer                                         │
└───────────────────────────────────────────────────────────┘
```

## Mobile (~390 px)
- Header wordmark left; **Home / Works still visible** if feasible; no hamburger needed for two items.
- Hero visual below content; one-column featured card and Works card stack.
- Filters wrap horizontally/scroll responsibly with visible focus states.
- Detail facts and CTAs stack vertically; no horizontal overflow; touch targets at least ~40–44 px.

## Visual tokens (proposal, not final brand approval)
- Background `#0A0E13` / surface `#111A22` / stronger surface `#182630`
- Foreground `#ECF3F6` / muted `#A6B6BF` / hairline `#314550`
- Point `#59D6E5` (light cyan); restrained amber on review-state ONLY. High-contrast, no saturated neon wall.
- Use system font stack for zero font licensing/network/CDN dependency. Bold headings; subtle tracked uppercase metadata.
- Media: CSS-only abstract blocks for layout testing; **not actual screenshots**. Final logo/artwork requires approved assets.
- Accessible text hierarchy, keyboard controls, focus ring, `prefers-reduced-motion`, informative alt for real assets later.

## Prototype behavior and boundaries
- Source: `docs/wireframes/index.html` — portable, **single static HTML file, zero external dependencies or network requests**. Open as a file or with Python HTTP server.
- Interactive Home / Works / Details navigation and category filters exercise information hierarchy.
- Review-only candidates are visibly labeled and **must not** be copied into real public project content automatically.
- Prototype links to existing public resources are illustrative and never signal team affiliation.
- This file is intentionally a **design artifact, not a production Astro page**. No routing, auto-publish, GitHub Actions or paid tool is created in phase 2.

## Approval checklist for Phase 3
- [ ] Information order Home → Featured → About → Contact is acceptable.
- [ ] Works and detail layout, card density, page navigation and mobile hierarchy are acceptable.
- [ ] Charcoal/cyan design direction is acceptable, or specify a color/type treatment.
- [ ] Decide which review-only candidates, if any, belong to published Works.
- [ ] Confirm wordmark/brand language, optional approved artwork and working release/store links.

## Phase 2 exit
Deliver wireframe + evidence ledger + offline checks in a checkpoint commit. User visual approval gates beginning final style/production content, but does not block Phase 3 technical schema scaffolding. Preserve `main` and original legal/ad files.

## Accepted design corrections — 2026-10-24

- Default public Works: **Anvil Bastion (Game)** and **VirtualQHDMirror (Software)**. The initial review-only status of VQM and the prior default display of personal bootcamp examples are superseded.
- **Detail hierarchy:** Back → title/category + prominent primary outbound CTA → wide media placeholder → overview + facts → secondary resource links. Do not bury the main outbound action beside policy links.
- **Anvil Bastion primary CTA:** `Google Play` → https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion (verified from Google's actual listing on 2026-10-24). Secondary: privacy policy and support.
- **VirtualQHDMirror primary CTA:** `GitHub` → https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md. Do not use the longer label `Public README`.
- **Accepted:** Home, Works grid and filters, mobile baseline, charcoal/cyan design. Final detail CTA placement awaits one more visual review.
- **Unapproved:** Other personal/team projects and artwork; no automatic transfer of demonstration data to the published site.

## Phase 2 final review sign-off (2026-10-25)

- The previously pending detail CTA re-review is **completed**, including the game Google Play button on mobile and the software GitHub button.
- Home/Works/detail design, category filters, mobile, and charcoal/cyan direction are approved. Initial public works: Anvil Bastion and VirtualQHDMirror.
- Final media is deferred; fixed paths and sizes: [ASSET_GUIDE.md](ASSET_GUIDE.md).
- Use **burningarktis@gmail.com** in all newly authored site content, not the legacy Proton Mail address.
- This closes Phase 2 design approval, **not** Phase 4 implementation, browser acceptance testing of a new deployed site, or release approval.
