---
name: reference-study
description: >
  Study reference videos (launch films, showreels, product demos, motion posts) and turn them into measured,
  reusable decisions: cut rhythm, openings, transitions, caption style, sound timing, loudness, tempo and endings.
  Use when someone shares reference videos or links and says "make it like this", "learn from these", "why does
  theirs feel better", "analyse how they used sound", or before writing a brief for a new film. Produces
  docs/REFERENCE.md with measured values, estimates and creative choices kept separate.
license: MIT
compatibility: Needs ffmpeg/ffprobe and Python 3 with numpy to measure videos; an image-capable model to read contact sheets.
metadata:
  author: Md Meraj Alam
  version: "1.0.0"
  repository: https://github.com/Meraj-08/motion-studio-skills
---

# Reference study

Without a reference, generated motion falls back to the same default: centered text on a gradient, everything fading
in. A measured reference beats a described one. Take the grammar, never the content, logos or characters.

## Rules

- **Give each reference one job**: an entrance, a transition, pacing, a caption style, a sound arc.
- **Measure, then look, then say which is which.** Label every value *measured*, *estimated* or *creative choice*;
  for an uncertain value, name the frames that would settle it.
- **Never claim to have watched or heard what you couldn't open.** If a link won't play, say so and ask for the file.
  Ask before downloading (name, source, size).
- **Don't mix unrelated styles to use every reference.** Pick the strongest ideas for this film.

## Workflow

1. **Inventory**: `ffprobe` each file (size, fps, duration, audio or silent).
2. **Measure the picture**: `scripts/picture-events.py ref.mp4` → hard cuts, time between jumps, motion per second,
   dead seconds. Footage animated on twos is handled.
3. **Measure the sound**: `scripts/audio-check.py ref.mp4` (LUFS, LRA, loudness per second, end silence) and
   `scripts/beatgrid.py ref.mp4` (tempo, phase; do cuts land on beats?).
4. **Look**: `scripts/review-sheets.sh ref.mp4 out/` → contact sheet at 2 fps with film time; `--strip t` for 12
   consecutive frames around an entrance or transition. Open the images and describe what you see.
5. **Write `docs/REFERENCE.md`** per [references/measuring-a-reference.md](references/measuring-a-reference.md).
6. **Translate into rules for this film**: one line each ("captions in two beats that follow the product state").

## What great launch films measurably do

Read [references/reference-films.md](references/reference-films.md) before writing a brief. In short:
- The first frame is the idea, not a logo; the hero object appears within ~1 s.
- Every transition has a cause on screen: a click, a gesture, or a hero object crossing the cut.
- Sound timing by type: clicks on the frame; whooshes peak 100–250 ms before the cut; arrivals land on the settle.
- Silence is punctuation: a breath before reveals, silence on the final logo.
- Monotony comes from repeated bars and no chord changes, not from a flat volume.

## References

- [references/reference-films.md](references/reference-films.md): Figma, Notion, agentplay, Procreate Dreams, Solimar, Paper Mono, OpenCode 2, Watchtower, Cursor, One and more, measured.
- [references/measuring-a-reference.md](references/measuring-a-reference.md): the REFERENCE.md format and the analysis prompt.
- [references/toolkit.md](references/toolkit.md): frameworks, skills and repos worth knowing; prompt patterns that went viral.
