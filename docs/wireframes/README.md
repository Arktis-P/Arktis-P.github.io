# Phase 2 — Browser Wireframe Review

This folder contains a **self-contained, interactive, dark-theme HTML wireframe** for the proposed Burning Arktis website. It is NOT the public website and uses **no external fonts, frameworks, APIs, images, hosted services, or CI**.

## Preview on Windows (no build required)

```powershell
git fetch origin
git switch gpt/site-redesign-implementation
start docs/wireframes/index.html
```

Opening the HTML file locally in any up-to-date browser is sufficient. You can also open a local server:

```powershell
py -m http.server 8000 --directory docs/wireframes
```

Open `http://localhost:8000/#home` and press Ctrl+C when done.

## What to check

1. **Home:** header, abstract brand-image placeholder, featured Anvil Bastion, short About section, Contact and policy footer.
2. **Works:** All / Games / Software / Experiments filters; the initial selection is **Anvil Bastion and VirtualQHDMirror**.
3. **Show review-only examples** optionally reveals one educational, unapproved layout fixture (SpartaPixelVerse, dashed amber).
4. **Detail: Anvil Bastion:** a prominent **Google Play** button opens the [verified official app](https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion); Privacy Policy and Support stay in secondary links.
5. **Detail: VirtualQHDMirror:** a prominent **GitHub** button opens the [public README](https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md). The old label `Public README` is removed.
6. **Mobile:** narrow the browser to ~390 px or use browser developer device mode. Check one-column cards, visible Home/Works navigation, legible copy and no horizontal overflow.
7. **Keyboard:** Tab through navigation and filters; focus indicator must remain clearly visible.
8. No project art is included. All visual graphics are intentionally CSS-only placeholders; no claims of released builds or studio ownership beyond the existing website.

## Review decisions before production content

See [Works scope](../PHASE2_WORKS_SCOPE.md) and [Wireframe specification](../PHASE2_WIREFRAME_SPEC.md). Approve public candidate works, authorized visuals, wordmark/color direction, default language and any working store URLs. No decision is needed merely to keep prototyping.

## Notes

- Existing `main/index.html` is untouched. Opening this file does not update GitHub Pages.
- The real `/privacy.html` and `/app-ads.txt` sources are untouched.
- Phase 3 will implement production Astro components only after separate requirements/data schema decisions.

## Review update — 2026-10-24

Home structure, Works cards/filters, mobile behavior and charcoal/cyan palette were accepted by the user. VirtualQHDMirror was selected as the only additional public GitHub work for now. Re-review the prominent detail CTAs and verify mobile behavior after this revision. Production publication remains a separate approval.
