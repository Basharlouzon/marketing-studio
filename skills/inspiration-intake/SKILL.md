---
name: inspiration-intake
description: Pre-production phase for marketing work — asks the user what he is looking for (goal, look-and-feel, channels, avoid/feature) and researches the internet for current trends, design inspiration, and competitor patterns BEFORE locking any campaign concept or visual style. Use before starting a new campaign, content month, or new asset style; whenever the brief is vague ("make me something cool", "surprise me", "something fresh for {month}"); or when the user mentions trends, inspiration, "what's working now", or references. Skip for revision/bug-fix tasks or when the user already locked a full concept.
---

# INSPIRATION & INTAKE — ask first, look around, then build

Two steps before any concept lock: **intake** (ask the user) and **inspiration** (look at the internet). Both write into the campaign folder so decisions survive the session. Order: intake → inspiration → concept lock (see `marketing-agent-studio` §5).

## 0. WORKSPACE GUARD
Campaign folder convention: `promo/<month-or-name>/` with `strategy/` inside. If no campaign folder exists yet, create it — assets + generator recipe come from `mbk-brand-kit` §8, folder layout from `marketing-agent-studio` §3 — and put `strategy/INTAKE.md` + `strategy/INSPIRATION.md` there as the first two files.

## 1. INTAKE — ask the user what he is looking for
**When to ask:** new campaign/content month without a locked concept · new visual style · vague briefs ("something cool", "you decide", "fresh ideas") · a new channel the brand hasn't posted on.
**When NOT to ask:** the user already gave concept + count + style · revision/bug-fix tasks · autonomous correction loops (the user isn't watching — use brand-kit defaults instead). **Repeat-month case** ("{month} was great — do the same for December"): skip the questions AND the research — pre-fill INTAKE.md from the prior month's INTAKE.md + the user's count, write a one-line INSPIRATION.md skip-note, and lock a FRESH concept from mbk-brand-kit §7 hooks (the old concept was calendar-bound to the prior month). This precedence overrides any "never skip intake" rule elsewhere: intake means asking the USER, and the user already answered.

**How:** use the AskUserQuestion tool with 3–4 questions max, each with 2–4 concrete options — mark the brand-kit default "(Recommended)" AND list it first. One reconciliation rule: when the brief signals freshness ("something cool/fresh"), recommend "Seasonal twist" or "Bolder & playful" instead of "keep the current system" — recommending the stale formula back at a freshness request reads as not listening.
1. **Goal this month** — Leads (free-snapshot signups) [Recommended] / Awareness & reach / Engagement & followers / Announce something specific
2. **Look & feel** — Keep the current system [Recommended] / Seasonal twist (per mbk-brand-kit §7: gold accents + mascot props — §3 palette tokens stay canonical) / Bolder & playful / Match a reference the user names
3. **Channels** — Feed + stories [Recommended] / Add Reels-TikTok / Full (add YouTube + email)
4. **Feature or avoid** — Nothing specific this month (Recommended) / Feature the from-$495/mo flat pricing / Target a vertical (name it: restaurants, salons, contractors…) / Avoid holiday clichés — user refines via the automatic "Other" (still provide the 2–4 options; "Other" cannot replace them).

Write the answers to `strategy/INTAKE.md` (goal, look, channels, feature/avoid, date). If the user answers in free text, extract to the same structure. Never re-ask what the user already stated in the request — pre-fill and confirm instead.

## 2. INSPIRATION — look at the internet (timebox: ≤10 tool calls — 3–5 searches + 2–3 fetches)
**When:** after intake, before locking the concept or design system. **Skip when:** the user says "keep it exactly like last month" or this is a revision.
**Never:** copy text, images, or layouts wholesale — inspiration is patterns, filtered through `mbk-brand-kit` (§3 palette + §6 copy budgets win over any trend).

**Search set (WebSearch, pick 3–5; ≤5–6 words per query, ONE topic each — stuffed queries return sludge):**
- "{industry} social media trends {Year}" — use the current or a past month, never the future campaign month (future-month trend data doesn't exist; note the recency gap in INSPIRATION.md)
- "instagram feed design trends {Year}"
- "{vertical} content ideas {hook}" — hook from mbk-brand-kit §7, e.g. "bookkeeper year-end close checklist ideas"
- "IRS small business tax deadlines {Month Year}" — deadline dates come from the source, not listicles
- "reels / short-form video trends {Month Year}" — include whenever the channels answer includes Reels-TikTok; extract motion/transition/pacing patterns (feeds `remotion-motion-studio` §2)
**Then WebFetch** the 2–3 most promising results — pass a prompt like "extract concrete formats, hooks, and visual patterns with examples"; if it returns a redirect URL instead of content, re-call with that URL.
**Visual references (optional, 1–2 calls):** for the look & feel answer, use the image-search tool (`search_image`, params query/count/gl/rank) — e.g. query "instagram feed design {Year} {industry}", count 6, gl "us" — and list the 3–6 most useful image URLs in INSPIRATION.md under "Visual references" (composition/palette reference only; never copy assets).
**When a search fails or returns sludge** (rate limits, listicle farms — web search cannot show real Instagram accounts): mark it WEAK in INSPIRATION.md, lean on mbk-brand-kit §7 hooks, and move on — don't burn the timebox retrying.

**Extract, into `strategy/INSPIRATION.md`:**
1. **Trends found** — 5–8 bullets, each with source URL and a one-line "what it actually is".
2. **Adopted** — trends mapped to CONCRETE decisions in this campaign ("carousels for checklists → our checklist layouts get a swipeable 3-page variant"). Only adopt what survives the brand kit.
3. **Rejected & why** — trends that clash with the brand (e.g. "neo-brutalism: violates the calm-grid personality").
4. **Sources** — link list.

## 3. CONCEPT LOCK
With intake answers + inspiration in hand, lock the concept (concept name + weekly arcs + asset counts), then proceed per `marketing-agent-studio` §1 (wave planning) and §5b (sequencing). The INTAKE.md and INSPIRATION.md are the first two files in `strategy/` — reference them in the campaign README. If the locked concept includes video/Reels, continue into `remotion-motion-studio` §2 — its step 1 expects exactly this concept lock, and INSPIRATION.md's motion notes feed the MOTION-SPEC.

## 4. TRAPS
- Don't let search results overwrite brand truth — trends inform, the brand kit decides.
- Don't ask questions the user's request already answered (that reads as not listening).
- Don't skip intake on a vague brief even if a previous campaign exists — "something fresh" is an explicit signal the old formula is stale.
- Search results can be SEO sludge — prefer sources that show concrete examples (platform trend reports, design galleries) over listicle farms; say so in INSPIRATION.md when sources are weak.
