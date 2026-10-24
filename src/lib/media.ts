/**
 * Phase 3 media resolution — use only from Astro server/build code.
 *
 * Images are picked up automatically if the user copies them to:
 *   public/images/brand/{wordmark.png,mark.png,hero.webp}
 *   public/images/works/<slug>/{cover.webp,shot-01.webp..shot-06.webp}
 * Missing files return null, allowing a safe typography/CSS fallback.
 * No external APIs, runtime fetches or image-server dependencies.
 */
import { statSync } from "node:fs";
import { resolve } from "node:path";

const MAX_SCREENSHOTS = 6;
const VALID_SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function staticImage(relativePath: string): string | null {
  if (!/^images\/[a-z0-9/_-]+\.(?:webp|png)$/.test(relativePath)) {
    throw new Error(`Unsafe static asset path: ${relativePath}`);
  }
  try {
    return statSync(resolve(process.cwd(), "public", relativePath)).isFile()
      ? `/${relativePath}`
      : null;
  } catch {
    return null;
  }
}

export function getBrandMedia() {
  return {
    wordmark: staticImage("images/brand/wordmark.png"),
    mark: staticImage("images/brand/mark.png"),
    hero: staticImage("images/brand/hero.webp"),
  };
}

export function getWorkMedia(slug: string) {
  if (!VALID_SLUG.test(slug)) throw new Error(`Invalid work slug: ${slug}`);
  const prefix = `images/works/${slug}/`;
  const cover = staticImage(prefix + "cover.webp");
  const screenshots: string[] = [];
  for (let n = 1; n <= MAX_SCREENSHOTS; n++) {
    const src = staticImage(prefix + `shot-${String(n).padStart(2, "0")}.webp`);
    if (src) screenshots.push(src);
  }
  return { cover, screenshots };
}
