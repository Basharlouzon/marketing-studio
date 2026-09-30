---
name: {app}-brand-kit
description: {App} brand system — exact color tokens (oklch+hex), logo assets, real product facts, voice rules, copy conventions, and layout laws for generating on-brand marketing assets and copy. Use whenever creating ANY {App} marketing asset or copy, checking "is this on-brand", brand colors or brand voice questions — even when the user doesn't say the word "brand".
---

# {APP} BRAND KIT

Brand-truth skill. Load before generating any asset or copy for this brand.

## 0. WORKSPACE GUARD
Workspace root: `{/absolute/path/to/project}`. Pre-flight: verify the asset folder exists (`ls {assets-path}`); if not, ask the user where the assets live before generating anything.

## 1. THE BRAND IN ONE SENTENCE
{One sentence anyone can repeat: what it does, for whom, the payoff.}

Tagline: **"{3-5 words}"** (support lines if any).

## 2. REAL FACTS ONLY — inventing clients, metrics, or results is the one unforgivable error
Extract from the product/site/codebase. List 6–12 bullet facts:
- What the product is + who it's for + where (if local)
- The 2–4 core features/deliverables, in plain words
- Pricing model + entry price (exact)
- The lead magnet / free offer, if any (with its real numbers)
- Integrations / platforms it works with
- The top 3–6 customer verticals or personas
- Any real proof points (team credentials, guarantees) — nothing invented

## 3. COLOR — canonical source: `assets/tokens.json` in this skill folder
Extract from the app's CSS (`globals.css`, tailwind config, or computed styles). For each token: name, oklch or hex, one-line use.
| Token | Value | Use |
|---|---|---|
| Primary | {…} | CTAs, key accents |
| … | | |

Ratio rule (default 60/25/10/5: neutral / secondary / primary / accent). Dark-surface rule: state how text behaves on dark backgrounds.

## 4. LOGO & ASSETS
Folder: `{assets-path}`. For each file: name → what it is → where it's used. State: minimum sizes, clearspace, one "never" list (recolor/rotate/stretch/glow), and whether seasonal props on the logo are allowed.
⚠️ Every workspace keeps its own asset copy with its own layout — verify the exact path exists (curl or ls) before rendering; a 404 logo renders as a broken circle and fails QA.

## 5. VOICE
3–4 principles (name + meaning + one example line each).
CTA conventions (verb-first only, list them; list the never-CTAs).
Banned words. Formatting rules (sentence case, numerals, punctuation habits, emoji policy).
Tone per channel (one line each).

## 6. COPY BUDGETS
Badge ≤20 · headline ≤55 (multi-line marker: `"line1 || line2"` → `<br>`) · sub ≤95 · chips ≤20 · checklist item ≤48 · stats: number ≤6, label ≤28 · cta ≤22.
A "post" deliverable = feed image + story variant + caption (hook → value → CTA + 3–5 hashtags). Default cadence if unspecified: ~3/week, weekends light.

## 7. SEASONAL MOMENTS (the product's real calendar hooks — never retail-only holidays)
List the dates/moments that genuinely matter to this product's customers.

## 8. GENERATORS
Where the layout library + campaign pattern live for this brand (clone from an existing month folder; never edit a frozen theme library).
