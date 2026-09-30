---
name: remotion-motion-studio
description: Real motion-design video production with the existing Remotion project at promo/mbk-promo — Motion Designer agent writes a frame-precise spec, Motion Animator agent implements self-validated compositions, then render final vertical/horizontal MP4s (Reels, TikToks, YouTube Shorts, promos) with music. Use the moment an MP4/video/animation is wanted for Mr. Bookkeeper ("animate this", "make a reel/tiktok/short", "turn this script into a video"). If the user only wants a video SCRIPT (no render), that's marketing-agent-studio; the moment pixels must move, this skill owns it.
---

# REMOTION MOTION STUDIO

Real choreographed motion via the proven Remotion project. Never ship static-slide zoompan as motion — it was rejected by the user ("looks awful"). Pipeline: Motion Designer (spec) → Motion Animator (implementation) → you (brand check → final render → frame QA). For a single short video, you may implement the spec yourself using the existing primitives — the two-agent split pays off at 3+ videos.

## 0. WORKSPACE GUARD
Project: `/Users/basharlouzon/Desktop/dev/jackob/promo/mbk-promo`. If `ls promo/mbk-promo` fails, ask for the video project location before writing code.

## 1. THE PROJECT (verified)
Remotion 4.0.531 + React 19 + TS 5.9.
- `src/anim.tsx`: **Word / Words** (mask-rise 13f, cubic-bezier(0.16,1,0.3,1)), **Rise** (fade + 28px, 16f) — reuse.
- `src/theme.ts`: `C` (C.primary #D8151E red, C.paper #FBFCFE, navyDeep #0C1734, navy2 #152A5E…), `darkBg`, `gridOverlay`, `FONT`. Note: bright red #fc5950 and gold #ebc831 are NOT in theme.ts — they're `BRIGHT_RED`/`GOLD` in `src/october/shared.tsx`; the #101b37 navy lives in the brand CSS, not this project (project navy = #0C1734).
- `src/october/shared.tsx`: `Pop`, `pulse`, `SceneShell`, `TopHeader`, `Footer`, `CtaPill`, `EndCard`, `MascotVisual`, `PumpkinVisual`, `MONO` (mono font stack), `BRIGHT_RED`, `GOLD` — clone these patterns.
- `src/fonts.ts`: Geist from `public/fonts/Geist-Variable.woff2`.
- Assets: `public/october/mascot.png` → `staticFile("october/mascot.png")`; music bed `public/music.wav` (35.46s) → `<Audio src={staticFile("music.wav")} />` in every composition — keep videos ≤35s or add `loop`.
- CLI: `./node_modules/.bin/remotion`, `./node_modules/.bin/tsc`, eslint.
- Palette source of truth: `mbk-brand-kit` skill `assets/tokens.json`.

## 2. PIPELINE
1. **Lock copy per scene** (verb-first CTAs; you will audit the animator's copy anyway — it drifts). No locked *campaign* concept yet (the `inspiration-intake` §3 lock — distinct from this copy lock)? Run `inspiration-intake` first, then return to this step.
2. **Motion Designer agent** (worth it for multi-scene work) → frame-precise spec: per-scene timeline table (in/out frames summing EXACTLY to total), per-element entrances (type/start/duration/stagger), transitions (never the same presentation twice in a row; end-card cut = flip), end-card ≥60f settled hold with exactly one ambient loop + one CTA pulse pair, global motion rules. Durations: shorts default **30s = 900f @30fps** (the 450f/15s October figure was a spec-math example, not a rule). Persist the spec to the campaign's `strategy/MOTION-SPEC.md`. Full brief template: `marketing-agent-studio/references/role-prompts.md` (MOTION DESIGNER).
3. **Motion Animator agent** → implement. Brief must include: project facts above, locked copy, full spec, and required self-validation — `tsc --noEmit` clean, eslint clean, `remotion still <Id> out/test.png --frame=<N>` at 2–3 key frames per comp VIEWED for overlap/broken assets/copy — plus: no full renders, no off-brand CTAs. Conventions: new composition id `<Month><Concept>` (e.g. DecemberYearEnd), code in `src/<month>/`, register in `src/Root.tsx` following the October block; never mutate the original Promo.
4. **You**: brand-audit CTAs/claims → render finals → frame QA → deliver.

## 3. RENDER + QA
- `cd promo/mbk-promo && ./node_modules/.bin/remotion render <CompositionId> out/<name>.mp4 --codec=h264` (450f ≈ 2.5MB, a few minutes).
- Frame QA: `<remotion-motion-studio>/scripts/extract_qa_frames.sh <video.mp4>` (samples t=1,5,10,14; set `EXTRA_TIMES="20 25 29"` for longer videos) → judge the frames. Tolerance to state in the judge prompt: mid-entrance states at t=1s are motion, not bugs; end-cards must be fully settled (visual + headline + CTA all present).
- Copy finished MP4s to the campaign `videos/out/` with descriptive names.

## 4. MOTION RULES (default spec language)
- Easing: cubic-bezier(0.16,1,0.3,1) or spring damping ≥14; linear ONLY for counters.
- ≤2 entrance types per scene; word stagger 2–4f; list-row cascade 6–7f; all entrances complete by f40 of a scene; scenes >84f hold ≥30f static before the cut.
- Nothing moves without purpose (bars grow = data; cascades = lists; a count = time; float/breath = life).
- Transitions 12–16f linearTiming; vary presentations; the cut into every end-card is the flip.
- Color as accent: red on figures/CTA only; gold on the single hero accent; paper cards on navy.
- End-card: mascot/pumpkin + headline + CTA; ≥60f settled; one ambient loop; CTA double-pulse in the last 30f.

## 5. TRAPS
- Broken asset = faint circle in renders (judges fail it) — confirm `public/` paths before animating; new assets go through `staticFile`.
- Agents write off-brand CTAs — audit every string before render.
- t=1s partially-masked headlines are correct motion — tell the judge, or it fails healthy frames.
- Don't leave test stills in `out/` when delivering.
- Reference implementation: `src/october/` (OctoberQ3 / OctoberSnapshot / OctoberHalloween, each exactly 450f net).
