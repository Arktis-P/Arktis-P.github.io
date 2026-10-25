/**
 * Content contract: localized copy is in content/i18n/strings.csv, not Markdown body.
 * Astro >= 5 uses the Content Layer API: glob/file loaders + z from astro/zod.
 * No CMS, runtime API calls, GitHub Actions or paid service is required.
 */
import { defineCollection } from "astro:content";
import { file, glob } from "astro/loaders";
import { z } from "astro/zod";

const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use a lowercase, URL-safe slug");
const publicUrl = z.string().url().refine((value) => {
  const u = new URL(value);
  return u.protocol === "https:";
}, "External links must use HTTPS");

const primaryLink = z.object({
  label: z.enum(["Google Play", "GitHub", "Website"]),
  label_key: z.string().regex(/^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$/).optional(),
  url: publicUrl,
}).superRefine((link, ctx) => {
  const hostname = new URL(link.url).hostname;
  if (link.label === "Google Play" && hostname !== "play.google.com") {
    ctx.addIssue({ code: "custom", message: "Google Play label must point to play.google.com" });
  }
  if (link.label === "GitHub" && hostname !== "github.com") {
    ctx.addIssue({ code: "custom", message: "GitHub label must point to github.com" });
  }
  if (link.label === "Website" && (hostname !== "spriteforge.cc" || new URL(link.url).pathname !== "/")) {
    ctx.addIssue({ code: "custom", message: "Website link is approved only for https://spriteforge.cc/" });
  }
  if (link.label === "Website" && link.label_key !== "work.spriteforge.cta") {
    ctx.addIssue({ code: "custom", message: "The SpriteForge website CTA must use the EN/KO CSV label" });
  }
});

const secondaryLink = z.object({
  label_key: z.string().regex(/^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$/),
  url: z.string().refine((value) =>
    /^\/(?!\/)[a-z0-9/_#.?-]+$/i.test(value) ||
    /^https:\/\/[^\s]+$/i.test(value),
  "Use a safe site-relative path or HTTPS URL"),
});

const works = defineCollection({
  loader: glob({ base: "./content/works", pattern: "**/*.md" }),
  schema: z.object({
    slug,
    category: z.enum(["game", "software", "experiment"]),
    featured: z.boolean().default(false),
    order: z.number().int().min(0),
    draft: z.boolean().default(true),
    status: z.enum(["available", "in-development", "archived"]),
    platforms: z.array(z.string().min(1)).default([]),
    links: z.object({
      primary: primaryLink,
      secondary: z.array(secondaryLink).default([]),
    }),
  }),
});

const home = defineCollection({
  // Astro file() expects an array of entries with explicit unique "id".
  loader: file("./content/home.yml"),
  schema: z.object({
    id: z.literal("home"),
    site_name: z.literal("Burning Arktis"),
    featured_works: z.array(slug),
  }),
});

const contact = defineCollection({
  loader: file("./content/contact.yml"),
  schema: z.object({
    id: z.literal("contact"),
    email: z.string().email(),
    github_url: publicUrl,
    privacy_url: z.literal("/privacy.html"),
  }),
});

export const collections = { home, contact, works };
