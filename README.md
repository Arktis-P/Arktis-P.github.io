# BurningArktis developer site

Public site source for BurningArktis / Anvil Bastion.

## Why Firebase Hosting instead of this repository's GitHub Pages URL

This repository is owned by GitHub user `Arktis-P`. A GitHub Pages user site at `burningarktis.github.io` would require the GitHub account itself to be named `BurningArktis`. A project Pages URL from this repository would still use the hostname `arktis-p.github.io`.

AdMob discovers `app-ads.txt` from the hostname in the Play developer website and checks `/app-ads.txt` at that hostname root. Therefore this repository is used as source control, while the recommended final host is Firebase Hosting or a future custom BurningArktis domain.

## Files

- `public/index.html` — developer website
- `public/privacy.html` — Play privacy policy
- `public/app-ads.txt` — replace with the exact AdMob-provided line before verification
- `firebase.json` — Firebase Hosting configuration

## Remaining inputs before public deployment

1. Replace every `SUPPORT_EMAIL_PLACEHOLDER` with a verified public BurningArktis support email.
2. Create a Firebase project / Hosting site and deploy this repository's `public/` directory.
3. Record the resulting stable HTTPS hostname as the Play developer website.
4. Set Anvil Bastion's in-app privacy-policy URL to `<developer-host>/privacy.html`.
5. Once AdMob provides the personalized app-ads.txt line, replace `public/app-ads.txt` and redeploy.

Do not invent AdMob IDs or publish a fake publisher line.
