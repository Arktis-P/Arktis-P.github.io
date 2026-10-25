import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export type Locale = "en" | "ko";
export type Translation = { en: string; ko: string };
export type Dictionary = Record<string, Translation>;

/** Keys can use existing camelCase segments, e.g. a11y.brandHome. */
export const TRANSLATION_KEY_PATTERN = /^[a-z][A-Za-z0-9]*(?:[._-][A-Za-z0-9]+)*$/;

/** Strict comma-separated parser supporting quoted commas/newlines/double quotes. */
export function parseCsv(input: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  const text = input.replace(/^\uFEFF/, "");
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (char === '"') {
      if (quoted && text[i + 1] === '"') { field += '"'; i++; }
      else if (quoted) quoted = false;
      else if (field.length === 0) quoted = true;
      else throw new Error("Unexpected CSV quote at offset " + i);
    } else if (char === "," && !quoted) {
      row.push(field); field = "";
    } else if (!quoted && (char === "\n" || char === "\r")) {
      if (char === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      if (row.some((cell) => cell.trim().length > 0)) rows.push(row);
      row = [];
      field = "";
    } else field += char;
  }
  if (quoted) throw new Error("Unterminated quoted CSV value");
  row.push(field);
  if (row.some((cell) => cell.trim().length > 0)) rows.push(row);
  return rows;
}

const source = readFileSync(resolve(process.cwd(), "content/i18n/strings.csv"), "utf8");
const rows = parseCsv(source);
if (rows.shift()?.join(",") !== "key,en,ko") throw new Error("i18n CSV header must be key,en,ko");
export const translations: Dictionary = {};
for (const [index, row] of rows.entries()) {
  if (row.length !== 3) throw new Error("i18n CSV row " + (index + 2) + " must have 3 columns");
  const [key, en, ko] = row;
  if (!TRANSLATION_KEY_PATTERN.test(key)) throw new Error("Invalid translation key: " + key);
  if (Object.prototype.hasOwnProperty.call(translations, key)) throw new Error("Duplicate translation key: " + key);
  if (!en.trim() || !ko.trim()) throw new Error("Missing bilingual value for " + key);
  translations[key] = { en, ko };
}
/**
 * Editable inline emphasis:
 *   [[accent|accented words]]
 *   [[ink|white words]]
 *   [[muted|secondary words]]
 *   [[#FFD166|custom readable color]]
 * Multiple independent segments can occur in one locale-specific CSV value.
 * No HTML or nested markup is parsed or injected into the document.
 */
export type ColorToken = "accent" | "ink" | "muted" | `#${string}`;
export type StyledPart = { text: string; color: ColorToken | null };
const STYLE = /\[\[(accent|ink|muted|#[0-9a-fA-F]{6})\|([\s\S]*?)\]\]/g;
const DARK_BACKGROUND = "#0c0d10";

function luminance(hex: string): number {
  const rgb = [1, 3, 5].map((index) => parseInt(hex.slice(index, index + 2), 16) / 255);
  const linear = rgb.map((v) => v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}
function contrast(a: string, b: string): number {
  const first = luminance(a);
  const second = luminance(b);
  return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
}
export function parseStyledText(input: string): StyledPart[] {
  const parts: StyledPart[] = [];
  const pattern = new RegExp(STYLE.source, "g");
  let start = 0;
  for (const match of input.matchAll(pattern)) {
    const at = match.index;
    const preceding = input.slice(start, at);
    if (preceding.includes("[[") || preceding.includes("]]")) {
      throw new Error("Malformed emphasis syntax; use [[accent|text]]");
    }
    if (preceding) parts.push({ text: preceding, color: null });
    const token = match[1] as ColorToken;
    const content = match[2];
    if (!content.trim() || content.includes("[[") || content.includes("]]")) {
      throw new Error("Empty or nested emphasis is not supported");
    }
    if (token.startsWith("#") && contrast(token, DARK_BACKGROUND) < 4.5) {
      throw new Error("Text color " + token + " has insufficient contrast on #0c0d10 (minimum 4.5:1)");
    }
    parts.push({ text: content, color: token });
    start = at + match[0].length;
  }
  const last = input.slice(start);
  if (last.includes("[[") || last.includes("]]")) {
    throw new Error("Malformed emphasis syntax; use [[accent|text]]");
  }
  if (last || parts.length === 0) parts.push({ text: last, color: null });
  return parts;
}
// Fail a build before publishing malformed syntax in either translation.
for (const [key, entry] of Object.entries(translations)) {
  for (const locale of ["en", "ko"] as const) {
    try { parseStyledText(entry[locale]); }
    catch (err) { throw new Error("Invalid emphasis in " + key + " (" + locale + "): " + String(err)); }
  }
}
export function t(key: string, locale: Locale = "en"): string {
  const value = translations[key]?.[locale];
  if (value === undefined) throw new Error("Missing translation key: " + key);
  return parseStyledText(value).map((part) => part.text).join("");
}
export function richParts(key: string, locale: Locale = "en"): StyledPart[] {
  const value = translations[key]?.[locale];
  if (value === undefined) throw new Error("Missing translation key: " + key);
  return parseStyledText(value);
}
