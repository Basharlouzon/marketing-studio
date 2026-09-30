---
name: mbk-brand-kit
description: Mr. Bookkeeper brand system — exact color tokens (oklch+hex), logo assets, voice rules, copy conventions, and layout laws for generating on-brand marketing assets and copy. Use whenever creating ANY Mr. Bookkeeper / mrbookkeeper.com / "Mr. B" / MBK marketing asset or copy, checking "is this on-brand", brand colors or brand voice questions, writing site or social copy, or reviewing brand compliance — even when the user doesn't say the word "brand".
---

# MR. BOOKKEEPER BRAND KIT

Brand-truth skill. Load before generating any asset or copy for this brand.

## 0. WORKSPACE GUARD
Workspace root: `/Users/basharlouzon/Desktop/dev/jackob` — all `promo/...` paths below are relative to it. Pre-flight: `ls promo` must show `brand social2 october mbk-promo`; if not, ask the user for the asset workspace before generating anything. Start-here doc for humans: `promo/STUDIO-SKILLS.md`.

## 1. THE BRAND IN ONE SENTENCE
Mr. Bookkeeper closes your books monthly — real people, plain English, one flat price — so you get your nights back.
Tagline: **"Books, handled."** (support: "Your nights, back." / "The team behind your books.")

## 2. REAL FACTS ONLY — inventing clients, metrics, or results is the one unforgivable error
Outsourced bookkeeping & accounting for small businesses, Los Angeles · human team: bookkeepers + a CPA + payroll specialists; books closed monthly · P&L + balance sheet monthly to a secure client portal (documents, e-sign, invoices — no email chains) · FREE snapshot: 3 months of statements → snapshot in 48 hours, $0, no commitment · free instant quote: 3 questions → flat price in seconds · flat pricing FROM $495/mo sized to revenue, no hourly billing, cancel anytime · integrations: QuickBooks, Stripe, Square, Shopify, Gusto, Xero, Wave, PayPal, FreshBooks, Expensify, Bill · verticals: restaurants, cafés, salons & spas, contractors, retail, clinics · archetypes: Guardian + Hero · mascot "Mr. B".

## 3. COLOR — canonical source is this skill's `assets/tokens.json` (+ tokens.css); recompute hexes only if the oklch values change
Banner Red oklch(0.56 0.22 27) #d8151e — CTAs, wordmark banner, chart highlights · Red Bright oklch(0.68 0.2 27) #fc5950 — red on dark, figures · Pie Gold oklch(0.84 0.16 95) #ebc831 — big numbers, dark-mode accents · Suit Navy oklch(0.23 0.055 265) #101b37 — deep sections (gradient to ~#0b1428) · Paper oklch(0.99 0.003 265) #fbfcfe · Ink #0f1624 · Gray Muted #5c6472 (light) / #9299a5 (dark) · Border #dde1ea · Success #008f56 · Cloud #f2f5fb.
Ratio 60% paper / 25% navy / 10% red / 5% gold. The old navy/orange promo palette (#0D1B38/#F05A33) is retired — don't use it. Dark cards need light headlines: add a global override (`.deep .headline { color: var(--fg) !important }`) because inline defaults leak dark text onto navy.

## 4. LOGO & ASSETS (folder: `promo/brand/assets/`)
- `logos/mascot.png` = `emblem.png` = `mark.png` — byte-identical today: one artwork, the 512² transparent circular emblem. Treat as ONE mark; don't promise distinct variants. `brand-banner.png` vertical lockup (1937×2052) · `logo.svg` 30×30 mark.
- Wordmark: white Geist 900 on red banner, tracked +5%, radius ~16–18. Never naked text, never recolored.
- Emblem: min 32px digital, 12mm print; clearspace = 1× ring width. Seasonal props (santa hat, pumpkin held BY the mascot) are fine as long as the emblem artwork itself is untouched — no recolor, no rotate, no stretch, no glow, no grayscale.
- `illustration/hero-illustration.png`: landscape 4:3 (1200×900). Its baked background is a gradient ~#fafbff → #e9eef8 — it blends on Paper Shade #ebf0fa (its baked gradient runs to ~#e9f0fa — measured off the PNG), and shows a rectangle edge on pure Paper #fbfcfe (put it in a rounded card instead, or match the page to #EDF1FA).
- `team/` portraits 864×1152 + team-photo 1344×768 (real people — attribute as "our team", never as fake testimonials) · `integrations/*.svg` 11 monochrome marks — white chips only.
- ⚠️ Other workspaces keep their own assets copies with DIFFERENT layouts (e.g. `promo/october/assets/mascot.png`, no `logos/` subdir). Verify the exact path exists (curl or ls) before rendering — a 404 mascot renders as a broken faint circle and fails QA.

## 5. VOICE
Principles: Owner to owner · Plain money English · The calm of handled · Prices in daylight.
CTAs, verb-first only: "Get your free snapshot" · "See your price in seconds" · "Hand it to Mr. B". Never "Submit" / "Click here" / "Contact us today" / "Learn more".
Banned words: solutions, utilize, seamless, esteemed, leverage (verb), synergy. Exclamation marks: ≤1 per document.
Formatting: sentence case everywhere; numerals ($495/mo, 48 hours, 3 questions); "&" only in "salons & spas"; Oxford comma; contractions on; emoji ≤1 per social post, none in email/portal/support.
Tone: Social punchy+wry · Website warm+direct · Email short+one ask · Portal spare · Support human-first · Bad news: own it early, name the fix.

## 6. COPY BUDGETS
Badge ≤20 · headline ≤55 (multi-line: write `"line1 || line2"`, render as `<br>` — this is the current convention; `themes2.py`'s literal `<br>` is legacy) · sub ≤95 · chips ≤20 · checklist item ≤48 · stats: number ≤6, label ≤28 · report row: left ≤18, right ≤40 · cta ≤22.
A "post" deliverable = 1080×1350 PNG + 1080×1920 story + caption (hook → one value line → verb-first CTA + 3–5 hashtags). Cadence default: ~3/week, weekends light, unless told otherwise.

## 7. SEASONAL MOMENTS (real calendar hooks)
Q-end (quarterly close) · Oct 15 extended filing deadline · Oct–Dec holiday quarter (restaurants/retail cash flow) · Dec year-end close + 1099/W-2 prep by Dec 31 · Jan 1 "opens clean" · Jan 31 filing runway · Apr tax season · launch/new-market beats. Halloween: gold accents + pumpkin props are on-brand.

## 8. GENERATORS
New month/campaign: `mkdir promo/<month>`, copy assets (`cp -R promo/october/assets promo/<month>/assets`), clone `promo/october/gen_october.py` → `gen_<month>.py`, swap the CARDS payloads. Layout builders live in that folder's `gen2.py` (19 builders; `render_all(CARDS)` writes `<this folder>/html/`). Never edit `promo/social2/themes2.py` — it's the frozen 30-theme library. Brand-book pages: `promo/brand/gen_brand.py` (18 pages → PDF).
