# Burning Arktis — Image & Logo Asset Guide

> Phase 3 contract (2026-10-25). **No assets are required immediately**. The user can add each asset later; planned production templates will automatically load exactly named files if present and show a deliberate text/CSS placeholder otherwise. The current standalone Phase 2 wireframe is a separate review artifact and does not auto-read these files.

## 1. Copy files into these exact locations

All paths below are relative to the Git repository root, under **`public/images/`** (not `docs/`, `src/` or a release folder). Filenames are **case-sensitive** when deployed to GitHub Pages. Dimensions below are target pixel sizes after export.

| File path | Use | Export size | Format |
| --- | --- | --- | --- |
| `public/images/brand/wordmark.png` | Logo text in header (fallback: styled studio name) | **1200 × 300 px** | PNG with transparency |
| `public/images/brand/mark.png` | Compact symbol / optional site icon | **512 × 512 px** | PNG with transparency |
| `public/images/brand/hero.webp` | Home hero artwork (fallback: CSS graphic) | **1920 × 1080 px** (16:9) | WebP, sRGB |
| `public/images/works/anvil-bastion/cover.webp` | Anvil Bastion card and detail cover | **1280 × 720 px** (16:9) | WebP, sRGB |
| `public/images/works/anvil-bastion/shot-01.webp` … `shot-06.webp` | Optional Anvil Bastion gameplay gallery | **1080 × 1920 px** (9:16 portrait) | WebP, sRGB |
| `public/images/works/virtualqhdmirror/cover.webp` | VQM card and detail cover | **1280 × 720 px** (16:9) | WebP, sRGB |
| `public/images/works/virtualqhdmirror/shot-01.webp` … `shot-06.webp` | Optional VQM screenshots | **1600 × 900 px** (16:9 landscape) | WebP, sRGB |

**Examples**: To add just an Anvil card image, copy an exported 1280×720 WebP as `public/images/works/anvil-bastion/cover.webp`. To add the next portrait screenshot, save it as `shot-02.webp` in the same folder. `shot-01` … `shot-06` are discovered in ascending order; missing numbers are skipped without breaking the gallery.

## 2. Automatic display rules

The Phase 3 code contract is implemented by `src/lib/media.ts`:

- Header: if `brand/wordmark.png` exists, display it with appropriate alt text; otherwise display text `Burning Arktis`. The compact `mark.png` is optional.
- Home: use `brand/hero.webp` if present, otherwise retain a legible CSS-only visual.
- Work card and detail: find `works/{slug}/cover.webp` by the approved `slug`. If absent, display a typography-based placeholder; **never a broken image**.
- Detail gallery: automatically include whatever of `shot-01.webp` … `shot-06.webp` exist, in numerical order. If none exists, omit the gallery.
- There is **no filename entry to edit in a Markdown/YAML file**. After adding an asset, rebuild the site locally and publish the generated static output through the separately approved publishing process.
- The image source is local; no runtime fetching, CMS, CDN subscription or GitHub Actions is required.

**Important:** **Phase 4 Astro pages are now wired** to the asset-discovery helper. Run `npm run build` after adding files to regenerate static output; source-branch changes alone do not update the public site. These paths do **not** automatically change the standalone `docs/wireframes/index.html` preview.

## 3. Export recommendations

- Keep the principal subject and important text within the central ~80% of landscape covers, since responsive cards may crop the sides. Put readable text in HTML rather than baking it into an image when possible.
- Google Play portrait screenshots should be cropped/exported to 1080×1920 with correct aspect ratio; do not squash 9:16 game screenshots into 16:9.
- Use WebP quality ~80–85 with an sRGB color profile. Aim for approximately **200–500 KB** per cover and **under 800 KB** per screenshot where practical; these are guidance, not hard limits.
- Do not commit PSD/AI/CLIP source files into `public/`. Keep editable source assets outside the published web root.
- Only upload images for which the studio has publishing rights, and exclude personal data, debug consoles, unpublished features or internal UI notes.
- Lowercase ASCII filenames and **hyphens** in slugs; no spaces, date suffixes, `(1)`, `.jpg.webp`, or alternative extensions.
- The existing site can function without any images until the final art is ready.

## 4. Adding an image on Windows

```powershell
git switch gpt/site-redesign-implementation
# Example: copy your already-exported file to the exact expected path
Copy-Item "C:\path\to\your-export.webp" "public\images\works\anvil-bastion\cover.webp"
py scripts/check_phase3_content.py
git add public/images/works/anvil-bastion/cover.webp
git commit -m "🖼️ assets(site): add Anvil Bastion cover artwork"
```

Run `npm run build` after changing image assets to regenerate the static output. **Uploading a source image into the branch alone does not update the live GitHub Pages site**, which still serves `main` until deployment is authorized.

## 5. New work later

A new approved work gets `content/works/<slug>.md` and `public/images/works/<slug>/cover.webp` plus optional numbered screenshots. Slugs must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Only works with `draft: false` are published; explicit user approval is required first.

## 6. Checklist before publishing media

- [ ] Filenames and directories match exactly (lowercase).
- [ ] Pixel dimensions/aspect ratio match the table.
- [ ] Copyright and image permissions are confirmed.
- [ ] No personal information or secret/debug data appears in captures.
- [ ] Offline content/asset tests pass.
- [ ] The final built page is inspected on desktop and mobile.
