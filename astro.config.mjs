import { defineConfig } from "astro/config";
// GitHub Pages user site, served from the domain root.
export default defineConfig({ site: "https://arktis-p.github.io", output: "static", trailingSlash: "always", build: { format: "directory" } });
