# Repository Working Rules — Burning Arktis Website

These rules apply to all work in this repository. Read this file before editing. The user may override them explicitly.

## Git and checkpoints
1. Work on a dedicated `gpt/...` feature branch. Do not write to `main` or publish the site without explicit user approval.
2. **Create a commit at each meaningful checkpoint**, including completed investigation, layout, implementation, content migration and validation. Commit only coherent, verified changes; report the branch, commit SHA and checks.
3. **Every commit message must start with a relevant emoji** followed by a conventional, scoped description, for example: `📝 docs(site): audit existing routes`, `✨ feat(site): add works grid`, `🐛 fix(site): restore privacy link`, `✅ test(site): verify static output`.
4. Prefer direct feature-branch commits. **Do not create pull requests by default**; create a PR only when explicitly requested or demonstrably required and approved.
5. Never force-push, rewrite shared history, or merge into `main` without approval.

## Costs, automation and verification
6. Default to **no newly enabled GitHub Actions, hosted CI, scheduled jobs or paid third-party services**. No additional cost, recurring execution, or cloud deployment automation without first identifying the cost/limits and obtaining approval. Existing repo settings may not be changed silently.
7. Prefer no-cost local/offline checks (scripts, static build, internal-link and artifact checks), run them at checkpoints, and record both passing and blocked checks. No PR is required for verification.
8. Do not assume an Astro or other framework adoption authorizes GitHub Actions. Choose the lowest-cost publishing path separately before deployment.

## Production safety and content
9. Preserve the public paths `/`, `/privacy.html` and `/app-ads.txt`. Until explicitly authorized, keep the **content bytes** of `privacy.html` and `app-ads.txt` unchanged; when moving them, verify hashes and generated public URLs.
10. Do not manufacture AdMob publisher IDs, company details, claims, titles, download/store links, official accounts, press material or project ownership. Label unverified material as draft and never publish it as fact.
11. Keep secrets, local paths, credentials and private project notes out of public files. Favor editable Markdown/YAML for content; treat site code and visitor content separately.
12. Protect existing public pages: build and inspect in a feature branch, document browser QA, and require an explicit release approval before production changes.

## Project reference
- Master plan: `docs/SITE_REDESIGN_PLAN.md`
- Initial source/route audit and manual checklist: `docs/PHASE1_BASELINE_AUDIT.md`
- Free baseline check: `python scripts/check_site_baseline.py`

## Approved project decisions (2026-10)
- The new site and its draft content use **burningarktis@gmail.com**, verified on Google Play; Proton Mail is legacy only. A legal-policy contact-only replacement must be reviewed before the published site switches over. Avoid modifying the existing privacy policy before that release gate.
- The only currently approved public Works are **Anvil Bastion** and **VirtualQHDMirror**. No other repositories are automatically featured.
- New site assets follow `docs/ASSET_GUIDE.md`; code must recognize fixed filenames automatically, tolerate missing images, and never require paid hosting.
