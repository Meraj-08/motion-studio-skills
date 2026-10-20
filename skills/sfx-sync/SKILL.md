---
name: sfx-sync
description: >
  Design, synthesize and place sound effects so each one lands on the frame the eye sees and is heard on laptop and
  phone speakers: UI clicks, typing, taps, sends, arrivals, whooshes into cuts, risers, impacts, ticking under
  suspense. Use when someone says a sound is late or early, "I can't hear the typing", "the landing sound is missing",
  "sounds overlap", "too many whooshes", wants UI foley for a product video, or needs effects generated in code.
  Verifies timing with an attack/peak report against the picture's event table.
license: MIT
---

# SFX sync

Every event gets one sound; you can hear every one; none of them stack. Where a sound sits in time matters more
than which sample it is.

## Place by the point the ear hears

| Sound | Align its… | to |
|---|---|---|
| clicks, taps, keys, state changes | attack | the frame (0 ms) |
| hero hits (success, landing, reveal) | attack/peak | the frame |
| whooshes into a cut | peak | 100–250 ms **before** the cut (the ear cues the eye) |
| arrivals (cards, a phone, a character landing) | attack | the **settle**, ~250 ms after the move starts |
| risers | end | the hit, with an 80 ms breath before it |

Offset = picture frame − the audible point's position inside the file. Measure both; never trust a cue sheet.

## Workflow

1. Take the frames from `docs/EVENTS.md`. Confirm each with a frame strip (`review-sheets.sh --strip t`): a badge
   logged at 42.867 s turned out to flip at 42.833 s.
2. Choose or make the sound: real recorded foley for typing and taps where possible; otherwise
   `scripts/sfx-synth.py` (seeded variation per press, so typing never repeats one sample).
3. Place it, then check: `scripts/audio-check.py sfx.wav --events 12.9:send,42.833:merged` → attack or peak within
   ±20 ms, and at least half its energy in 400 Hz–4 kHz (what laptops and phones play).
4. Check overlaps: two effects audible at once within 12 dB of each other is clutter; keep one.
5. Listen once on laptop speakers and once on a phone.

## Generate effects

```bash
python scripts/sfx-synth.py sfx.wav --cue 10.2:thock --cue 10.34:thock --cue 12.9:send \
  --cue 14.28:pluck=D5 --cue 15.57:pluck=G5 --cue 16.72:pluck=B5 --cue 42.833:impact --cue 66.9:whoosh=0.8
python scripts/sfx-synth.py --gallery sfx-gallery/      # audition every voice
```

## Rules reviewers confirmed

- Every event needs a sound that sits above the music; the music ducks for it. One per event.
- Warm, varied, soft. No bright or whistly effects, no odd high tones, no cartoon boings on a mascot.
- Typing must pop: lower the bed under it, use real keyboard or phone recordings cleaned of music, and only on
  frames where characters appear.
- Ticking on the music's beats under a failure, speeding up; a distinct merge click; the success sound not too loud.
- Offer 3–4 landing or step options in a 10 s sample before choosing.
- If a sound effect gets cut off at the end, extend the picture 1–2 s.

## References

- [references/placement.md](references/placement.md): audibility, the sounds reviewers asked for, placement details.
- [references/synthesis-recipes.md](references/synthesis-recipes.md): DSP recipes (keys, clicks, impacts, risers, ticks, sax, bass, brushes), arrangement ideas, ElevenLabs notes.

## Scripts

| Script | Use |
|---|---|
| `scripts/sfx-synth.py out.wav --cue t:type[=param][:dB]` | Synthesize effects on exact times, aligned by attack, peak or end. |
| `scripts/audio-check.py sfx.wav --events t:label[:pre]` | Attack and peak vs the frame, and 400 Hz–4 kHz share. |
| `scripts/picture-events.py film --region x,y,w,h` | The exact frame a UI element changes. |
