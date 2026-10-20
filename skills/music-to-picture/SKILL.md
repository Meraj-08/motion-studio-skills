---
name: music-to-picture
description: >
  Measure a music track and cut it to a video's story points: tempo and beat grid, downbeats, sections, where it ends,
  then an arrangement that lands the drop on the first real action, suspense on a failure, the biggest return on
  success, a breakdown under a quiet section and the track's own ending on the end card. Use when someone wants a
  soundtrack fitted, swapped, slowed, re-cut or made "more cinematic" on an existing video, wants several music
  versions of one picture, says the music is "monotonic", "not smooth", "off-theme" or "too loud at 44 s", or asks
  which licensed track fits.
license: MIT
compatibility: Needs ffmpeg and Python 3 with numpy; rubberband (CLI) for tempo changes with pitch kept.
metadata:
  author: Md Meraj Alam
  version: "1.0.0"
  repository: https://github.com/Meraj-08/motion-studio-skills
---

# Music to picture

A real produced track, cut on its own downbeats to the story, beats any generated score played straight through.
Synthesis is for effects and stingers; the bed is a recording with chord changes and sections.

## Workflow

1. **Licence first.** Record source and licence for every candidate (Pixabay: free, no credit; Uppbeat free tier:
   credit line; AI-tool or ripped audio: internal review only). Ask before downloading.
2. **Measure each candidate**: `scripts/beatgrid.py track.mp3 --json track.beats.json`.
   - The tempo is pinned by how sharply the whole track folds onto the beat; drift < 15 ms per 16 bars = fixed grid.
   - Half and double tempo fold almost as sharply: decide by ear, then pass `--bpm`.
   - The downbeat guess is an estimate: confirm it by listening at the first big section.
   - `audio-check.py track.mp3`: a body spread under ~8 dB, or one chord for a minute, will read as monotonic.
3. **Take the picture's events** from `docs/EVENTS.md` (measured on the render).
4. **Cut the track to the story points** with segments `(film_from, film_to, offset)`, `src = film + offset`, each
   anchored to one picture moment. Never stretch to fit; loop only whole phrases at downbeats.
5. **Shape the body**: headline markers, ducks, a build into the end card (see the reference).
6. **Check**: every seam on a downbeat, `audio-check.py new --vs approved --sections …` shows only intended changes,
   and listen at every seam on laptop speakers.

## The arrangement that works for launch films

| Film | From the track | Anchor |
|---|---|---|
| intro (character, logo) | nothing, or its sparse intro; effects carry the first seconds | — |
| reveal → feature tour | its build, then the drop and main groove | the drop on the first real action |
| failure | its darkest bars, filtered, ticks on its own beats speeding up | the failure frame |
| recovery | a passage on the SAME chord the suspense ends on, filter opening over ~0.9 s | "checks passing" |
| success | its biggest return; the loudest moment of the film | the success frame |
| quiet section (mobile) | its breakdown, crossfaded in | the section start |
| end card | its own final bars and natural decay; ~2.5 s of silence at the very end | the landing hit |

## Rules the ear confirmed

- Switch tracks inside motion, never mid-groove; never hand back to a track in another key or tempo.
- One theme from intro to end: an intro "off theme from the rest" was a real complaint.
- The recovery continues harmonically; a brighter chord jump reads as "too high, too quickly".
- A level jump at a seam may be the track's own downbeat: compare with the approved version before calling it a bug.
- Slowing a track: rubberband (pitch kept), then re-anchor every segment on its own sync point.
- A track without an ending gets one: the landing takes its biggest hit, the groove after it fades within ~4 s.
- Keep the music driving into the end hit (riser, 80 ms breath, hit). A "fade, stop, swell" ending was rejected.

Details, numbers and the full list of review notes: [references/cutting-music.md](references/cutting-music.md).

## Scripts

| Script | Use |
|---|---|
| `scripts/beatgrid.py track [--json f] [--bpm n]` | Tempo, phase, downbeats, bar loudness, section changes, hits, where the music ends. |
| `scripts/audio-check.py mix [--vs old --sections a-b,…] [--duck a-b]` | Loudness, dynamics spread, per-section before/after, duck depth. |
