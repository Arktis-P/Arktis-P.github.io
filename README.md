# Burning Arktis — Official Site (Current: Anvil Bastion)

> **Development rules:** Read [AGENTS.md](AGENTS.md) before editing. Use emoji-prefixed commits at each checkpoint, feature branches, no PR or new paid/hosted CI by default, and no `main` deploy without approval.

Official public site for Burning Arktis / Anvil Bastion. A broader team portfolio redesign is being developed separately from the current production source.

- Public website: https://arktis-p.github.io/
- Anvil Bastion privacy policy: https://arktis-p.github.io/privacy.html
- AdMob app-ads authorization: https://arktis-p.github.io/app-ads.txt
- Public support email: burningarktis@proton.me

## Existing production source

The currently documented GitHub Pages configuration publishes from the `main` branch, repository root, with HTTPS. The repository's root contains:

- `index.html` — current Anvil Bastion developer/support page.
- `privacy.html` — existing privacy policy. Preserve its URL and contents unless explicitly approved.
- `app-ads.txt` — **already contains the personalized AdMob authorization line**. It is not a placeholder. Preserve its URL and contents unless explicitly approved.

The exact live Pages settings/HTTP responses still need manual verification; see the Phase 1 audit. Do not modify these protected files merely to redesign the homepage.

## Redesign references

- [Plan](docs/SITE_REDESIGN_PLAN.md)
- [Phase 1 baseline audit, route inventory and test checklist](docs/PHASE1_BASELINE_AUDIT.md)
- [Working rules](AGENTS.md)
- Free, offline baseline check: `py scripts/check_site_baseline.py`

Implementation branch: `gpt/site-redesign-implementation`, forked from the planning branch. Do not confuse branch commits with public deployment.
