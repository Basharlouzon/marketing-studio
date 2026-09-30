# Marketing Studio

**An expert-agent marketing studio, packaged as ZCode skills.** Strategy, copy, images, brand books, and motion-designed videos — produced by named AI agents (Campaign Director, Content Writer, Video Director, Motion Designer…), rendered through a proven HTML→pixel pipeline, and gated by visual-judge QA on every asset.

Provenance: every pattern in here shipped in real campaigns — 80+ judged images, an 18-page brand book, a full monthly campaign, and 3 motion-designed videos — then survived a 13-agent audit (format, accuracy, fresh-agent simulation, red-team). Final sign-off: **SHIP, 9/10**.

---

## Install

```bash
git clone <this-repo> && cd marketing-studio
./install.sh          # copies the 5 skills into ~/.zcode/skills/
# restart ZCode — done.
```

`install.sh` is idempotent and safe to re-run (it overwrites the five skill folders in place).

## The five skills

| # | Skill | Owns |
|---|---|---|
| 0 | [`inspiration-intake`](skills/inspiration-intake/SKILL.md) | Asks the user what he's looking for (goal / look / channels), researches the internet for current trends, writes `INTAKE.md` + `INSPIRATION.md` before any concept lock |
| 1 | [`mbk-brand-kit`](skills/mbk-brand-kit/SKILL.md) | The brand truth: exact color tokens (oklch + hex), real product facts, voice + CTA conventions, layout laws. **This is the per-product file you clone for a new app** |
| 2 | [`social-image-studio`](skills/social-image-studio/SKILL.md) | The image factory: payload-driven generators → pixel-exact rendering (posts 1080×1350, stories 1080×1920, thumbnails, PDF pages) → visual-judge QA gate. Bundles `render_batch.mjs` + `preverify.py` |
| 3 | [`marketing-agent-studio`](skills/marketing-agent-studio/SKILL.md) | The orchestration playbook: which expert agent to dispatch, in what order, with what brief (copy-paste prompts in `references/role-prompts.md`), wave limits, solo-vs-full-studio rule |
| 4 | [`remotion-motion-studio`](skills/remotion-motion-studio/SKILL.md) | Real motion videos: Motion Designer spec → Motion Animator implementation → render, in a Remotion project. Bundles `extract_qa_frames.sh` |

## How a campaign runs

```
inspiration-intake (ask user + internet trends)
 └─> concept lock
      ├─> marketing-agent-studio  ──> Campaign Director / Content Writer briefs
      ├─> social-image-studio     ──> posts, stories, thumbnails, brand books
      └─> remotion-motion-studio  ──> Reels / TikToks / Shorts (real motion)
           every asset ──> visual-judge gate ──> fix loop ──> ship
```

## Onboard ANY app in 3 steps

The studio is product-agnostic except one file — the brand kit. To point it at a new app or web app:

1. **Copy the template**: `cp -r templates/brand-kit-template skills/<app>-brand-kit/` and fill every `{PLACEHOLDER}` — extract the app's exact colors from its CSS (oklch/hex), its logo files, its real product facts (never invent), its voice rules. The template walks you through it.
2. **Scaffold the workspace**: `<project>/assets/` + `strategy/` + `images/` + a `gen_*.py` generator (clone patterns live in the brand kit §8).
3. **Say "make N posts for {app}"** — the studio asks you what you're looking for, researches trends, and builds.

Full walkthrough: [`templates/brand-kit-template/SKILL.md`](templates/brand-kit-template/SKILL.md).

## Re-render / edit loop

Assets are code. Edit copy in the generator's payload file (or a skill's markdown), re-run the generator, re-render the affected files only. Commands for each medium are in the skill files (§ render sections).

## Validation

Trigger checks (each phrase must surface the named skill): "make 12 posts for December" → social-image-studio · "turn this script into a reel" → remotion-motion-studio · "plan November" → marketing-agent-studio · "is this on-brand?" → mbk-brand-kit · "something fresh" → inspiration-intake.
Mechanical checks: `python3 skills/social-image-studio/scripts/preverify.py <images-folder>` · `bash -n skills/remotion-motion-studio/scripts/extract_qa_frames.sh`.

## Docs

Live docs: **this repo deploys to Vercel** — the docs site renders the shipped SKILL.md files directly from `skills/`, so docs can never drift from the code.

## Out of scope

Publishing/scheduling to platforms — this studio produces and QA's assets; posting is manual or a future skill.

## Repository layout

```
skills/                     # the 5 skills (source of truth)
  <name>/SKILL.md           # each: frontmatter + body, loaded by ZCode
  <name>/scripts/           # bundled helpers (render_batch, preverify, extract_qa_frames)
  <name>/references/        # on-demand deep docs (role-prompts.md)
  mbk-brand-kit/assets/     # tokens.json + tokens.css
templates/brand-kit-template/   # fill-in brand kit for ANY new app
docs-site/                  # static docs site (Vercel root)
install.sh                  # idempotent installer → ~/.zcode/skills/
```
