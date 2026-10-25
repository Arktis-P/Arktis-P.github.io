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
export function t(key: string, locale: Locale = "en"): string {
  const text = translations[key]?.[locale];
  if (text === undefined) throw new Error("Missing translation key: " + key);
  return text;
}
