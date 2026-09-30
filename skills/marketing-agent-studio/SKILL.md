---
name: marketing-agent-studio
description: Orchestration playbook for the expert marketing agent studio — Campaign Director, Content Writer, Video Director, Brand Strategist, Verbal Identity, Motion Designer, Motion Animator — for ANY marketing-production request: "create a marketing campaign", "content calendar", "content month", "make N posts/assets for {month}", "brand identity", "video scripts", "generate expert agents", or any batch of 6+ marketing assets — and for "surprise me" / "something fresh" / vague briefs. Starts with the user-intake + internet-inspiration phase (see inspiration-intake skill), then covers when the full studio is needed vs solo mode, agent-wave limits, and copy-paste role prompts.
---

# MARKETING AGENT STUDIO

Run marketing work as a studio of named expert agents. You are the executive + builder: agents produce strategy and copy; you produce rendered assets and enforce QA.

## 0. SCOPE — full studio vs solo mode (decide first)
- **Solo mode** (small batches, ≤12 post-units — see §5 — existing brand kit): lock the concept yourself, write copy yourself against `mbk-brand-kit` §5/§6, skip agent waves except judges. The studio still owns: folder layout (§3), caption schema, calendar shape, and the judge gate. Skip any role whose deliverable already exists frozen in the brand kit (strategist/verbal-identity/personas are already in there).
- **Full studio** (campaigns, new brand work, 3+ videos, multi-channel months): run the role pipeline below.
All `promo/...` paths assume the Mr. Bookkeeper workspace (see `mbk-brand-kit` §0 guard).

## 1. ORCHESTRATION RULES
- **Wave limit ≤4 agents**; independent agents in parallel (Agent tool, run_in_background: true); block on results with TaskOutput.
- **Order**: strategy/design → copy → build (you) → visual-judge QA → fix loop. To parallelize, lock the concept yourself first and brief every agent with it.
- **Self-contained prompts**: agents have zero session context. Inject the facts pack (`mbk-brand-kit` §2) + voice (`§5`) verbatim, the exact output format, character budgets, and "commit to decisions — no options, no process narration".
- **Validation demands**: copy agents return strict JSON/labeled copy only; code agents must self-validate (typecheck + rendered test stills viewed) before reporting done. You run the full renders.
- **Brand audit on every agent return**: check CTAs against brand-kit §5 and claims against §2 — agents drift (real example: an animator wrote "Book your 48-hour snapshot" where the brand says "Get your free snapshot").
- **Persist immediately**: agent output goes to `strategy/*.md` files as soon as it lands — it dies with the session context otherwise.

## 2. THE ROLES
Read the full copy-paste brief in `references/role-prompts.md` before dispatching any role. Summary:

| Role | Produces | Key constraints |
|---|---|---|
| Campaign Director | campaign-on-a-page, weekly arcs, day-by-day calendar, hashtag system, asset manifest | real seasonal moments only; realistic KPIs |
| Content Writer | strict-JSON display copy + captions + emails | char budgets; " \|\| " line-break markers; verb-first CTAs |
| Video Director | short-form scripts (hook/beats/CTA/caption/props) + YouTube packages | searchable titles; no fake testimonials |
| Brand Strategist | purpose/mission/vision/positioning, one tagline, 5 values, 5 personality sliders, 3 personas, archetypes | commit to decisions, ≤900 words |
| Verbal Identity | 4 voice principles, tone spectrum, say/not-that rows, 4 messaging pillars, 3-length boilerplate, formatting rules | ≤900 words |
| Motion Designer | frame-precise motion spec (timelines sum exactly; entrances; transitions; end-cards) | Remotion-feasible only |
| Motion Animator | implemented compositions, self-validated | no full renders; no off-brand CTAs |
| Visual judge | pass/fail + evidence per file | see `social-image-studio` §4 for the literal prompt |

Judge mechanism (real tooling): dispatch judge agents with the Agent tool (≤4 per wave, background), collect with TaskOutput. Judges are stateless — a re-judge is simply a new pass over only the failed files.

## 3. DEFINITIONS (so you never have to ask)
A **post** = 1080×1350 PNG + 1080×1920 story variant + caption (hook → value line → verb-first CTA + 3–5 hashtags) in a captions file. Default cadence ~3/week, weekends light. **Campaign folder** layout: `strategy/` (INTAKE.md, INSPIRATION.md, CAMPAIGN-PLAN.md, VIDEO-SCRIPTS.md, CAPTIONS-AND-EMAILS.md, MOTION-SPEC.md) + `images/` + `videos/out/` + `youtube/thumbnails/` + `README.md`.

## 4. FACTS + VOICE
Inject `mbk-brand-kit` §2 (real facts) and §5 (voice/CTA/banned words) verbatim into every brief. This is the single defense against invented clients and metrics.

## 5. SEQUENCING (phase 0 = inspiration-intake skill)
**Phase 0 — intake + inspiration:** unless the user already locked a full concept, run the `inspiration-intake` skill first: ask the user what he is looking for (goal / look / channels / feature-or-avoid), research current trends on the internet, and write `strategy/INTAKE.md` + `strategy/INSPIRATION.md`. Full studio runs the skill at full depth: one AskUserQuestion with all 3–4 questions, then the ≤8-call inspiration pass. Solo mode compresses phase 0 to one AskUserQuestion with 1–2 questions (goal + look & feel) and skips inspiration research unless the user asked for a new look. Precedence: if the request already answered the intake questions (e.g. "{month} was great — do the same"), skip the questions entirely, pre-fill INTAKE.md from the prior month, and let `inspiration-intake` §1 drive. §0's "lock the concept yourself" happens after phase 0, using the INTAKE.md answers. Asset counts are in post-units (a post-unit = post + story pair); solo = ≤12 post-units.

## 5b. SEQUENCING EXAMPLE (what worked for the October campaign)
1. Lock the concept yourself on real calendar moments ("CLOSE Q3. OWN Q4.").
2. Wave A parallel-background: Campaign Director + Video Director, both briefed with the locked concept.
3. Build images/videos while they run; on arrival, dispatch Wave B: Content Writer against the calendar.
4. Render → visual-judge waves → fix → re-judge.
5. Assemble `strategy/*.md` + README → deliver.

## 6. REFERENCE OUTPUTS (real examples worth imitating)
`promo/october/strategy/` — INTAKE.md, INSPIRATION.md (retroactive stubs), CAMPAIGN-PLAN.md, VIDEO-SCRIPTS.md, CAPTIONS-AND-EMAILS.md, MOTION-SPEC.md; `promo/brand/Mr-Bookkeeper-Brand-Guidelines.pdf` (18 pages).
