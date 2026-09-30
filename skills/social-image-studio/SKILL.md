---
name: social-image-studio
description: Battle-tested pipeline for generating batches of pixel-perfect marketing images — Instagram posts, stories, carousels, YouTube thumbnails, og-images, banners, posters, infographics, key visuals, and multi-page brand PDFs — from HTML templates, rendered at exact pixel dimensions and gated by visual-judge QA. Use for ANY "generate/make N images / posts / stories / thumbnails / pictures / a brand book / a PDF" request, even when the user doesn't say "render" or "pipeline".
---

# SOCIAL IMAGE STUDIO — HTML → PNG → JUDGED

Proven across 100+ shipped assets. Python generator → HTML cards → local HTTP → in-app-browser screenshot → PNG → visual-judge QA. Companion skills: `mbk-brand-kit` (brand truth) for any Mr. Bookkeeper work.

## 0. WORKSPACE GUARD
The example paths assume the Mr. Bookkeeper workspace (`ls promo` shows brand/social2/october/mbk-promo). If they don't resolve, ask the user where the assets live before generating.

## 1. ARCHITECTURE
0. **Phase 0 (new campaigns/styles only):** run the `inspiration-intake` skill — ask the user what he is looking for and scan current design trends — before locking the design system. **Skip** for revisions, bug-fixes, or a user-locked concept/design ("keep it like last month") — go straight to step 1.
1. **Generator** (python): payload-driven builders → one self-sized HTML file per card. Copy lives in a data file (dict/JSON), never inline in layout code.
2. **Serve**: `cd <folder> && python3 -m http.server 8734` (default port; any free port works — keep goto URLs consistent with it).
3. **Render**: browser-use IAB (recipe + bundled script below).
4. **QA**: preverify scans, then visual-judge agents on every shipped image; fix → re-render → re-judge. Skipping the judge gate is how broken assets reach the user.

## 2. THE RENDER STEP
**Fast path — bundled script.** From a `mcp__node_repl__js` cell:
```js
const { pathToFileURL } = await import("node:url");
const m = await import(pathToFileURL("<this-skill-dir>/scripts/render_batch.mjs").href);
const { done, fails } = await m.renderBatch({ jobs: [
  { url: "http://localhost:8734/html/oct-01.html", w: 1080, h: 1350, out: "/abs/images/oct-01.png" },
  { url: "http://localhost:8734/html/oct-01-story.html", w: 1080, h: 1920, out: "/abs/images/oct-01-story.png" },
]});
done + " rendered, fails: " + fails.join(",");
```
The script implements everything below: plugin bootstrap, tab recovery, per-job viewport, `?v=` cache-buster, 2-attempt retry with 4s backoff, skip-if-exists resume.

**Manual cell** (when you need custom logic) — the bootstrap lines are the part everyone gets wrong; use exactly this shape:
```js
const { join } = await import("node:path");
const { pathToFileURL } = await import("node:url");
const browserClientUrl = pathToFileURL(join(process.env.ZCODE_PLUGIN_ROOT ?? process.env.CLAUDE_PLUGIN_ROOT, "scripts", "browser-client.mjs")).href;
const { setupBrowserRuntime } = await import(browserClientUrl);
await setupBrowserRuntime({ globals: globalThis });   // binds `agent` + `nodeRepl` globals
const browser = await agent.browsers.get("iab");
// tab recovery, viewport, goto, screenshot → fs.writeFileSync …
```
Facts (verified against the plugin contract): IAB `setViewportSize` accepts 320–3840 × 320–2160; `tab.screenshot()` returns 1x Uint8Array → `fs.writeFileSync` from the same cell; `file:` URLs are NOT navigable — serve over local HTTP.
Environment claims (headless Chrome CLI hangs; chrome-devtools MCP profile-lock + path restrictions) verified Oct 2026 — re-verify if the plugin set changes.

## 3. GENERATOR DISCIPLINE
- `ROOT = os.path.dirname(os.path.abspath(__file__))` in every generator — a hardcoded absolute ROOT silently writes output into another campaign's folder.
- After Phase 0, read `strategy/INSPIRATION.md` "Adopted" + `strategy/INTAKE.md` before writing payloads: each Adopted decision binds a generator choice (e.g. "checklists get a swipeable 3-page variant" → emit 3 `checklist` payloads); intake feature/avoid items bind `badge`/`head`/`cta` copy.
- Payload schema (the 19-builder library in `promo/social2/gen2.py`): `{name, layout, cta, payload:{badge, head, sub, items|chips|logos|emoji|img|report, deep, mascot, foot, hs}}`. Literal example:
```python
{"name":"dec-02-checklist","layout":"checklist","cta":"Get your free snapshot",
 "payload":{"badge":"Year-End Checklist","head":"Close the year before the ball drops.",
 "items":["Confirm vendor 1099 details by Dec 31","Reconcile every account before Jan 1",
 "Match receipts to December spend","Book the January close while it is quiet"],
 "sub":"Save this. Your January self says thanks."}}
```
- Headline multi-line: write `"line1 || line2"`; convert to `<br>` centrally in the headline helper. (`themes2.py`'s literal `<br>` is legacy.)
- New month/campaign = new folder with its own `assets/` copy, its own `gen2.py`, and its `strategy/` (INTAKE.md, INSPIRATION.md, CAMPAIGN-PLAN.md…); relative refs `../assets/...`. Never edit `promo/social2/themes2.py`.
- Photos in fixed-height cards: `object-fit:cover; object-position:50% 15%` — keeps faces in frame.
- Dark cards: global CSS override `.deep .headline { color: var(--fg) !important }` — inline dark defaults leak onto navy.
- Before any batch render: curl-check every referenced asset path (a 404 mascot renders as a broken faint circle).

## 4. QA GATE
1. **Preverify** (free): `python3 <this-skill-dir>/scripts/preverify.py images/` — prints size, dead-band and transparency findings. Plus your own Read of the 2–3 riskiest files.
2. **Judges**: dispatch judge agents (≤4 per wave, ≤20 files each; run_in_background, collect via TaskOutput). Judge prompt template — fill the braces:
```
Visual acceptance for rendered {medium} for "{brand one-liner}" (brand: {palette+mascot+font}).
Files: {absolute paths}
Bar: "would a business owner post this today?" — no truncated/overlapping text; no
collisions (footer on posts, CTA on stories); balanced composition (no dead band
>~250px on stories); assets render (no broken-image circles); readable contrast.
Tolerance: {mid-animation/mid-entrance states are motion, not bugs}.
Output one JSON line per file: {"file":"<basename>","verdict":"pass|fail","issues":["specific evidence"]}.
```
3. **Fix loop**: group fails by root cause (one CSS/asset fix cures many) → patch the generator → regenerate → re-render ONLY affected files (with `?v=` buster) → re-judge only the fixed files (a fresh judge pass over the failed list is fine — judges are stateless).
4. Multi-page docs: render A4-ratio pages (1440×2036) → `PIL Image.save(pdf, save_all=True, append_images=…)`.

## 5. REFERENCE IMPLEMENTATIONS (read before writing new generators)
- `promo/social2/gen2.py` — 19 layout builders, one payload → post + story
- `promo/october/gen_october.py` — month-campaign pattern on top of gen2
- `promo/october/gen_kv.py` — key visual + wide board + YT thumbnails in one file
- `promo/brand/gen_brand.py` — 18-page A4 brand document → PDF
