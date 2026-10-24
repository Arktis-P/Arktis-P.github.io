# Phase 1 — Existing Site Baseline & Route Inventory

- Audited: 2026-10-24 (KST)
- Project: `Arktis-P/Arktis-P.github.io`
- Production source reference: `main` @ `58fac4aac0f1cf27e97746f719d2998754bcd053`
- Planning reference: `gpt/site-redesign-plan` @ `2edc2c74781cc2f11e59da1267b77792b7713ce7`
- Implementation working branch: `gpt/site-redesign-implementation`
- Scope of this checkpoint: **audit, rules, and verification setup only**. No new site and no deployment.

## 1. Verified repository inventory

The entire `main` tree contains four files. The planning branch has the same four plus `docs/SITE_REDESIGN_PLAN.md`. There are no `.github/workflows` files, Astro/Node manifests, image assets, CSS/JS bundles, Works pages, deployment scripts or repository-level agent rules in these checked trees.

| Path | Purpose | Production baseline blob SHA |
| --- | --- | --- |
| `index.html` | English, single-page Anvil Bastion developer/support site; inline dark CSS | `6915ae7b841b98e3e12ef170b22fe31c0cb823e9` |
| `privacy.html` | Anvil Bastion privacy policy, 11 sections, dated 2026-08-17; original must be preserved | `adb10a5116c033c092fc2fc36b50eeb0d3c20a68` |
| `app-ads.txt` | **Populated** Google AdMob authorization record (not a placeholder); preserve exact content | `a895dcf3f08d0ceae76bba64205f6a1e17ab9808` |
| `README.md` | README, URLs and contact; originally had an out-of-date app-ads placeholder warning | `21ce564348ddd23149a4b5a07480b2c67bc080e9` |

`index.html` exposes About, Privacy and Support with an absolute `/privacy.html` link and a mailto contact. There is no navigation for Home/Works/Detail and no site asset pipeline. The privacy page points back to `/` and to Google's privacy policy.

## 2. Public route and link preservation matrix

| Route / link | Source evidence | Required behavior after redesign |
| --- | --- | --- |
| `https://arktis-p.github.io/` | README, `index.html` | Replaced with Home only after approval; must resolve |
| `https://arktis-p.github.io/privacy.html` | Root file and home link | **Same URL and same policy bytes** until explicitly approved |
| `https://arktis-p.github.io/app-ads.txt` | Root file and README | **Same URL and exact AdMob authorization bytes** until explicitly approved |
| `mailto:burningarktis@proton.me` | Current homepage and privacy | Keep public support contact unless explicitly changed |
| `https://policies.google.com/privacy` | Existing privacy page | Keep existing external reference in unchanged policy |

Planned, **not presently implemented**: `/works/`, `/works/{slug}/` and any new media or legal routes.

## 3. Hosting and test state

- The existing README states GitHub Pages is sourced from `main` repository root and HTTPS is enforced. This is **documented configuration**, not independently verified Pages API settings in this audit.
- The live `arktis-p.github.io` endpoints were attempted from the assessment environment, but HTTP access could not be obtained. **No live HTTP 200/redirect, rendered page, browser/mobile behavior or deployed contents are claimed verified.**
- No workflow YAML exists in either audited Git tree; this alone does not establish the absence of all externally configured automation.
- No PR, hosted CI, Actions workflow, dependency install or deployment is required for Phase 1.

## 4. Offline baseline check

No external dependency is needed. With the implementation branch checked out:

```powershell
git switch gpt/site-redesign-implementation
py scripts/check_site_baseline.py
```

The script checks the three existing route files, root guidance and the original Git blob SHA of `privacy.html` and `app-ads.txt`. It does not make network requests and does not certify production availability. When migrating protected files into Astro's `public/` directory, both source and destination copies are checked if present. When generated build output is available, add separate output/link checks in Phase 5.

Optional local inspection of the **current pre-redesign page**:

```powershell
py -m http.server 8000
```

Open `http://localhost:8000/`, `http://localhost:8000/privacy.html` and `http://localhost:8000/app-ads.txt`; terminate the temporary server with Ctrl+C. This does not publish anything.

## 5. User-visible manual production checklist

The runtime could not independently fetch the live Pages host. The user can check these links with a normal browser and report any failures; this is **not a blocker for Phase 2 design work**.

- [ ] Open `https://arktis-p.github.io/` and confirm the Anvil Bastion developer/support page loads.
- [ ] Open `https://arktis-p.github.io/privacy.html` and confirm the privacy policy loads (last updated 2026-08-17).
- [ ] Open `https://arktis-p.github.io/app-ads.txt` and confirm a nonempty Google authorization line is visible; do not post the publisher identifier to public issues.
- [ ] Optionally test the site on a phone and note any existing rendering problems for comparison.

## 6. Findings and release gates

**Verified:** Repository is a tiny 4-file static site; policy and AdMob path/byte baselines are recorded; the planned redesign has not begun; Git history already contains an AdMob authorization commit. Existing README's placeholder statement was stale and should be corrected in this working branch.

**Not yet verified:** Live Pages response, Pages administrative settings, external app/store backlinks, existing custom-domain usage, design asset rights, and public eligibility/ownership of any additional work.

**Phase 2 inputs / no need to block beginning the wireframe:**
- [ ] Confirm public list of Works: title, ownership (team vs. individual), kind (game/software/experiment), status, verified URL, and permission to publish.
- [ ] Supply approved logo/cover/screenshots when available; until then use labeled neutral placeholders.
- [ ] Review initial Home/Works/Detail layout choices and public site language (English default currently).
- [ ] Before **release**, verify all three live routes and GitHub Pages publishing source with repository Settings or a browser.

**Exit status:** Phase 1 repository audit and local test setup complete; live-site validation remains a recorded manual check. Begin Phase 2 wireframes and Works scope without editing `main`.
