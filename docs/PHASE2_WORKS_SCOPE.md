# Phase 2 — Works Publication Scope (Evidence Ledger)

> 2026-10-24. Research and design decisions only. This is not a publication approval. Existing production website and `main` remain unchanged.

## Publication policy
1. The existing official website is authoritative for **Anvil Bastion** as a BurningArktis-developed/published game. It does not prove a currently available storefront, price, downloads or exact release status.
2. Public GitHub visibility **is not evidence of Burning Arktis team ownership or approval for official promotion**. A personal exercise and a multi-person bootcamp project must not be presented as a studio-made game.
3. Private repositories, internal workstates, screenshots, future features and undisclosed projects must not appear in public HTML or published data unless separately approved.
4. A work is eligible for the initial public Works collection only when identity/ownership, public text, at least one valid public link, visibility permission and required images (or an agreed neutral fallback) are confirmed.
5. Pending candidates are **demonstration-only fixtures** inside `docs/wireframes/`, never part of the public published Works collection.
6. Unknown values are omitted (no invented availability, release dates, team size, store links or achievements).

## Candidate register

| Work | Category for layout testing | Evidence | Decision for initial live listing |
| --- | --- | --- | --- |
| **Anvil Bastion** | Game | Existing public `main/index.html` says developed and published by BurningArktis; support and privacy policy exist | **Baseline inclusion**. Only existing confirmed description/contact/policy; storefront and visual assets pending |
| **VirtualQHDMirror** | Software | Public [README](https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md) documents Windows 11 tool, release notes/packaging, and a public [releases](https://github.com/Arktis-P/VirtualQHDMirror/releases) path | **Candidate / owner approval needed** to brand as team work; do not treat as affiliated merely because account hosts repository |
| **SpartaPixelVerse** | Experiment | Public [README](https://github.com/Arktis-P/SpartaPixelVerse/blob/main/README.md) explicitly says individual Unity bootcamp project | **Candidate only** as openly labelled personal experiment, not official game |
| **FindGuguzo** | Experiment | Public [README](https://github.com/Arktis-P/FindGuguzo/blob/main/README.md) credits multiple project collaborators and bootcamp assignment | **Hold**: scope and collaborators' permission/attribution to be confirmed; not used as visible demo |
| **Other public repositories** | Unsorted | GitHub owner repo index exposes multiple public projects | **Hold** until individually reviewed; public repo alone is insufficient |
| **Private/undisclosed work** | N/A | No publishable evidence in official existing site | **Exclude**, including from review-page candidate identifiers |

## Publication gates (user review)
- [ ] Explicitly accept/reject adding VirtualQHDMirror under the **Software** category; specify team project vs personal authorship if accepted.
- [ ] Explicitly accept/reject adding personal learning projects (SpartaPixelVerse and other experiments). Default: exclude.
- [ ] Supply or approve the Anvil Bastion cover, logo and screenshots or explicitly accept a neutral typographic fallback.
- [ ] Verify an official store/download page URL for Anvil Bastion before adding a store CTA. No placeholder purchase button.
- [ ] Confirm preferred public site language: English default (matches the old page), Korean/Japanese later if wanted.
- [ ] Confirm public brand spelling (design proposal: **Burning Arktis**), and optional final logo/wordmark.
- [ ] Keep contact `burningarktis@proton.me`, policy route and AdMob route from existing production until instructed otherwise.

## Outcome
Phase 2 can finalize information architecture and layout without waiting for all approvals. The only **presumptively eligible** named work is Anvil Bastion (limited to facts already stated on official site). The prototype shows two conspicuously review-only GitHub candidates to demonstrate card/filter layouts; this does **not** approve them for release.

## Review decision superseding the initial candidate register — 2026-10-24

- **Anvil Bastion:** Public Google Play page was opened and verified: [Anvil Bastion: Idle Defense](https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion), developer **Team Burning Arktis**. Use **Google Play** as the prominent primary detail CTA. Privacy and support remain secondary. This **supersedes** the former "storefront pending" statements above. Do not copy changing review/download metrics.
- **VirtualQHDMirror:** User explicitly selected it for the public Works listing under **Software**. Primary CTA text: **GitHub**, destination: [public README](https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md). Listing approval is **not** evidence for describing it as an incorporated studio's original commercial release. This **supersedes** its former "candidate / approval needed" status.
- **Other public repositories:** Not selected for public portfolio listing; remain excluded. The SpartaPixelVerse card may be shown with the explicitly labelled design-only toggle in local wireframes, initially hidden. It must never be shipped as published content automatically.
- **Accepted:** Home section order, Works grid and categories, mobile page hierarchy, charcoal/cyan direction.
- **Still needed before production:** Verify details CTA layout on phone/desktop; obtain approved logo/cover images and decide final site copy. No CI, PR or main deployment authorized.

## Final Phase 2 sign-off — 2026-10-25

- The user confirmed that the Anvil Bastion **Google Play** button opens and displays correctly on mobile.
- The user confirmed that the VirtualQHDMirror **GitHub** button opens correctly.
- The user accepted the page hierarchy, filters, mobile layouts and charcoal/cyan palette. No further wireframe UI corrections requested.
- The user will supply assets incrementally; the exact filenames/dimensions and safe fallbacks are defined in [ASSET_GUIDE.md](ASSET_GUIDE.md).
- New-site support contact is **burningarktis@gmail.com**, independently confirmed on the [Google Play listing](https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion). **Do not publish Proton Mail** as a new-site contact. The current legal policy stays unmodified on the production branch until a contact-only update is reviewed.
- **Phase 2 CLOSED**. Phase 3: content schema and deterministic asset resolver; still no PR, Actions or production deployment.
