import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export const GET: APIRoute = async ({ site }) => {
  const origin = (site ?? new URL("https://arktis-p.github.io")).toString().replace(/\/$/, "");
  const works = (await getCollection("works", ({ data }) => !data.draft))
    .sort((a, b) => a.data.order - b.data.order || a.data.slug.localeCompare(b.data.slug));

  const urls = [
    `${origin}/`,
    `${origin}/works/`,
    ...works.map((work) => `${origin}/works/${work.data.slug}/`),
    `${origin}/privacy.html`,
  ];

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls.map((url) => `  <url><loc>${url}</loc></url>`),
    "</urlset>",
    "",
  ].join("\n");

  return new Response(xml, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
