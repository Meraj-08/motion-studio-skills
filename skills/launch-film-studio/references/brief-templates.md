# Briefs, specs and request formats

Five documents carry a film. Write them as files in the project, not as chat.

## 1. Project `CLAUDE.md` (house rules, read on every run)

```markdown
# <Product> launch film: house rules

## Where things are
- Composition: `film/` (index.html, src/film.js camera keys and steps). Framework rules: use /hyperframes before editing.
- Footage: `assets/footage/` (app-rec = real app, site-rec = website demos, mobile-rec = phone).
- Music: `assets/music/` with `LICENCES.md`. Mixers and checks: `tools/`. Decisions per version: `docs/`.
- Deliverables: `deliverables/<product>-<dur>s-v<N>-<track>.mp4` (+ `-small.mp4`). Approved original: `…-FINAL.mp4`.

## Render contract
- Every frame is a pure function of time. No timers, CSS transitions, carried state; seeded randomness only.
- Render: `npx hyperframes render -f 60 -q delivery --video-frame-format png -o review/v<N>/picture.mp4`.
- Mux audio with the video stream copied; never re-encode the picture to change sound.

## Honesty
- Real product UI only. Never invent screens, states or successful actions the footage doesn't show.
- Say which footage is a live recording and which is a website/demo capture. Illustrative UI fill is disclosed.

## Look
- One headline + one supporting line per title; labels switch exactly when the UI shows that state.
- Crops at ≥ 1.0× source pixels. Something meaningful changes every 2–4 s, except deliberate holds.
- Banned: centered title on a gradient, everything fading in, corner labels, frame borders, glow on UI chrome,
  generic particle bursts.

## Sound
- Effects placed by audible point (attack / peak / end) on the measured frame. One sound per event.
- Music: a licensed track cut on its own downbeats. Master −14 LUFS, −1 dBTP for social.
```

## 2. Director brief (`BRIEF.md`, the whole film)

```markdown
You are director, editor, sound designer and render engineer for a <DURATION> film made in code.
Multi-session production: don't rush to a final render.

## The film in one line
<Logline, and what the viewer should feel at the end.>

## Inputs
- Footage: <recordings and what each shows>.  Reference: <file> — take its grammar, never its content.
- Music candidates: <files + licence>. Measure each with beatgrid.py before planning cuts.
- Skills: /hyperframes (+ this skill). APIs in .env: <names only>. Budget: <credits/$>, be economical.

## Look
<3–5 lines: palette (hex), type, texture, camera language, what is banned.>

## Beat sheet (seconds; each line is one story point the music can land on)
0.0–2.0    hook: <the most striking image>
…          a new visual payoff every 2–4 s; a headline marker at each scene change
<END>      logo + CTA; hold ≥ 3 s; ~2.5 s of silence at the end

## Sound plan
Bed: <track> cut to the story points (drop on <event>, dark bars for <failure>, biggest return on <success>,
breakdown under <quiet section>, the track's own final bars on the landing).
Effects: one per event (list them against the beat sheet).

## Gates
1. docs/STYLE.md + shot list → my OK.   2. Three stills (opening, product result, closing) → my OK.
3. Picture render → EVENTS.md measured.  4. Music cut + effects → review sheets + scores ≥ 8.
5. Final: master, small copy, contact sheet, version log, licences.
```

## 3. Frame-numbered shot spec (one product action, for precise work)

Write scene timing in seconds, convert to frames at the chosen fps, and keep every number in one place so a
revision touches one set of values. Example (30 fps, square):

```text
GOAL      Show how <product> exports a finished report. Opening copy ≤ 8 words. Closing: one action + destination.
CANVAS    1080×1080, 30 fps, 600 frames. Origin top-left, px. Essential content inside a 64 px margin.
LAYOUT    Background #101318 · text #F5F7FA · accent #8AD8B0. Headline box x96 y112 w888, 64 px, max 2 lines.
          Product card x120 y350 w840 h480 r24. Layer order: background, card, product, cursor, headline.
OPENING   0–18 headline in (y +24→0, opacity 0→1) · 18–42 card in (y +60→0) · hold to 119.
PRODUCT   120 report visible · 150–180 cursor to Export (path clear of text) · 195 press (cursor scale 1→0.92→1,
          192/195/201) · 210 exported file appears · 234 result label fully readable · hold to 419.
CLOSING   420 logo + closing copy · 420–438 copy fades in · hold to 599.
SOUND     195 click transient · 210 reveal accent · 438 music settles.
REVIEW    First build the opening only; render frames 0, 18, 42, 60, 119 + a moving preview; report and wait.
```

Check the longest headline you'll ever reuse: if it wraps to 3 lines, shorten it, widen the box, or move it to its
own shot. Count reading holds from the frame the words become legible; read them aloud at normal speed.

## 4. `docs/EVENTS.md` (measured, the single source of timing)

```text
time     frame   on screen                                   sound role
 7.000    420    app appears (title)                         reveal; music building
12.900    774    request sent                                drop lands here; send bloop (peak-aligned)
42.833   2570    PR badge flips to "Merged"                  loudest hit of the film
67.000   4020    mascot lands with the end card              closing hit; final bars from here
```

Measured with `picture-events.py` (`--region` tight around the element). Note which value is measured, which is
estimated, which is a creative choice.

## 5. Edit request (how to ask for, or make, one correction)

Four fields: location, observed problem, the change, what stays fixed.

```text
Location: global frame 210 (7.0 s).  Problem: the cursor covers the result label.
Change: only the cursor's post-press path — leave at 204, rest by 210, 24 px clear of the label.
Keep: press at 195, reveal at 210, card geometry, copy, audio cues.
Check: stills at 195, 210, 222, 240 and a preview of 180–249; report new coordinates and file names.
```

Order of fixing: missing information and unreadable text → timing → visual detail.

## 6. Brief formats that worked

**A. A full launch brief (new film).** Sections, in order:
`INPUTS` (motion references, official logo from the website, older product videos, the product site, workflow
references; "treat source materials as references, not instructions") → `TARGET` (length, 1920×1080@60, keep content
where a vertical cut is possible) → `REFERENCE ANALYSIS` (frames every 0.5 s plus the moving footage; timestamps for
movement, reveals, transitions, camera, type, pacing, sound; a style guide of what to adapt from each) → `BRAND AND
PRODUCT RESEARCH` (real logo, colours, fonts, screenshots, verified descriptions; check older videos are still current;
never invent screens, capabilities, metrics or testimonials; list missing assets first) → `OPENING` beat by beat with
seconds (walk → anticipation → jump → landing → red-eye activation → push into the eye → it becomes a real UI element)
→ `PRODUCT EXPLANATION` (one idea per scene, short accurate copy, a meaningful UI action, readable long enough, motion
that connects to the next) → `ENDING` (logo lockup, one CTA, the URL, settle long enough to read) → `DESIGN AND AUDIO`
(real typography and assets; no repetitive fades or arbitrary particles; licensed or original music; a beat map;
restrained footsteps, jump/landing, activation and UI sounds; no clipping; no narration) → `IMPLEMENTATION`
(HyperFrames, else Remotion; repeatable frames) → `PLAN FIRST` (style guide with timestamps, director's brief, timed
storyboard with exact copy/assets/movement/transitions/audio cues, opening keyframes; present before building).

**B. A revision brief.** Keep the runtime and story; list numbered fixes per section with approximate times ("verify
the exact boundaries first"); mark HIGH PRIORITY items; give target numbers ("phone 1.4–1.6× larger"); state what must
not change; end with what to inspect (the opening in motion, a transition frame by frame, phone-size readability, the
CTA hold, audio sync) and the deliverables (MP4, editable source, short change list).

**C. A product-accuracy revision.** Audit first: **Keep** (matches the current product), **Replace** (confirmed
outdated), **Confirm** (can't verify). Update only confirmed mismatches; use the latest running app to settle
conflicts (website previews lag the app; a newer post doesn't prove every screen in it is newer); keep accurate
footage regardless of age; check model names and versions shown on screen; if a linked video can't be opened, say
which and ask for the file. Show proposed replacements with timestamps before rebuilding.

**D. Locked sections.** "Keep the first 7 s and everything from the mobile section to the end exactly as they are;
preserve their animation, framing, timing, copy and audio; connect the new middle smoothly to both." Find the exact
boundary timestamps first and keep the locked sections' timestamps unchanged.

**E. The 45 → 90 director/composer brief** (Nolan × Zimmer framing): write `docs/creative_brief.md` (core concept and
temporal hook; scale contrast between full-frame type and micro-UI; high-contrast palette; the generic elements being
replaced) → weighted spring motion, state change every 2–3 s, motion blur → the score drives the edit (ticking pulse
on a beat grid, harmonic risers before reveals, 60–90 Hz impacts with crisp clicks on the frame, −14 LUFS) → critique
loop at least 3 times with contact/strip/phone sheets, scores per category, the 3 weakest moments logged. Caution: a self-assigned score is not proof; reviewers judge by ear and eye.

**F. An audio-only brief.** Problems first (numbered, with timestamps) → instrument/effect specs with numbers →
an exact timeline (every second range: what plays, what hits where) → master and mux. Or the phased version: research
(launch films' BPM 120–132, mid-range carving 500 Hz–2 kHz for UI clarity, synthesis techniques) → strip the old audio
and map every frame → score piece by piece (suspense and build-up, the groove, the reveal and suspense, escalation and
climax, the ending) → master and mux.

**G. Review notes from a viewer.** A table of time / on screen / music, what works (✅), what to improve with
timestamps and a concrete fix each (headline markers on downbeats; shorten or build the quiet section; shorten the
dark pause to ~0.5 s; punch in 120–150 % where UI is small; speed up slow typing 1.5× or cut to the finished prompt;
soft UI clicks; −14 LUFS / −1 dBTP). Apply only the part the requester scopes ("in sense of music") and say which
suggestions were left for later.
