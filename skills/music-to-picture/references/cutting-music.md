# Music: choose, measure, cut to the story

On one launch film eleven soundtracks were tried. The ones that survived were **real tracks cut to the story**, never a
generated score played straight through. Synthesis is for effects and stingers; the bed is a real recording.

## Choose

- 2–3 candidates in the film's energy (launch films: 110–150 BPM, a clear drop, a breakdown, a real ending).
- Licence first. Pixabay: free, no credit. Uppbeat free tier: credit line required, limited downloads per month (the account holder declares the licence). AI-tool or video-rip audio (for example a music bed lifted from another video): internal
  review only. Keep `assets/music/LICENCES.md`.
- Reject flat material before cutting: `audio-check.py track` body spread under ~8 dB, or a loop that repeats one chord
  for a minute, reads as "monotonic" even with a volume arc. Reviewers want verses, tension, peaks, breakdown, finale.
- ElevenLabs/generated music tends to ignore its section plan and come out flat; profile it per half-second, and know
  the remaining credits before generating (one track ≈ 725 credits).

## Measure

`python scripts/beatgrid.py track.mp3 --json track.beats.json`

- Tempo comes from the onset autocorrelation and is then pinned by how sharply the whole track folds onto the beat
  period. Drift per 16 bars under ~15 ms means a fixed grid holds; big drift in one window usually means an intro or
  a half-time section, not a wrong tempo.
- Half/double tempo fold almost as sharply (SoundSurfer: 88 vs 176). Decide by ear, then pass `--bpm`.
- The downbeat guess (most kick energy on beat-of-4) is an estimate: confirm by listening at the first big section.
- Measured on real launch tracks: Product Launch 150.00, Swagger 120.00, Drive 110.00, Travel 118.00, GR0ZA 110.00 (an earlier
  144.4 reading was wrong), SoundSurfer 88/176, a user-supplied instrumental 130.00.

## Cut the track to the story points

Every track gets the same arrangement, so versions are interchangeable on one picture. Never stretch a track to fit;
cut it on its own downbeats and anchor each segment to one picture moment (segments `(film_from, film_to, offset)`
with `src = film + offset`):

| Film | From the track | Anchor |
|---|---|---|
| reveal → mid | its build, then drop and main groove | drop lands on the first real action (Send) |
| failure | its darkest bars, filtered (muffled), low heartbeat, dry ticks on its own beats speeding up | the failure frame |
| recovery | a passage on the SAME chord the suspense ends on, filter opening over ~0.9 s | "checks passing" |
| success | its biggest return; the loudest moment of the film | the success frame (Merged) |
| quiet section (phone) | its breakdown, crossfaded in | the section start |
| landing → end | its own final bars and natural decay | the landing hit |

Rules the ear confirmed:
- **Switch tracks inside motion, never mid-groove** (a cut at 9 s was audible; under a camera dive it disappears).
- **Never hand back to a track in another key or tempo.** Stay in one track to the end.
- **Recovery continues harmonically**; a brighter chord jump read as "too high".
- **Loop whole phrases at downbeats.** Product Launch needed 2.0 s more: at 150 BPM that's 5 beats, but its phrase is
  2 bars, so a 2-bar repeat at a downbeat plus a hand-off 3 beats earlier kept both seams on the beat (1-bar loop:
  waveform match 0.05; 2-bar: 0.5–0.64).
- **A level jump at a seam may be the track's own downbeat.** Compare with the approved version before calling it a bug.
- **Slowing a track**: rubberband time-stretch (pitch kept, e.g. 150 → 140 BPM), then re-anchor every segment on its
  own sync point so drop, success and landing stay on their frames.
- **A track without an ending gets one**: the landing takes its biggest hit, the groove after it fades by ~4 s.

## Endings

- Kept: the music keeps driving into the landing, a riser from ~4 s out, an 80 ms breath (dropout) just before the hit,
  the track's own final bars ring out, ~2.5 s of silence on the end card (start the final bars 2 beats later if needed).
- Rejected: "quieter and quieter, stop, then a swell" ("after 1:02 the old one was better"). A long synthetic reverb
  tail lost to the track's own decay. If the sound gets cut off, extend the picture.

## Shape the body (the review said "flat 13–50 s")

- Headline markers: on the beat nearest each scene change, a one-beat dropout (−15 dB) plus a short reverse swell.
- Duck under typing 6–10 dB (phone typing went from −4 to −10 dB and was better).
- A build into the end: from ~4 s before the landing, filter opens, +5 dB lift, riser, 80 ms breath.
- First seconds can carry more (+2 dB to 20 s was asked for); the success moment stays the loudest point.

## The opening and the theme

- **Effects only until the transition into the product.** No music under the walk; the music's build starts after
  the transition into the product (6.3 s in the case study) and its drop lands on the reveal or first action.
- **Start low.** Intro sounds in low notes at first, building up; jump and landing sounds stay (removing them was
  "not a great idea"); the first part should feel subtle.
- **One theme from intro to end.** "The music on the intro is completely off theme from the rest" was a real
  complaint: the opening music must belong to the same track or key as the body.
- **A transition between two tracks is heard** unless it happens inside motion; the 6→8 s and 47→50 s seams were
  both flagged "not smooth".
- **The brief can be grand and still be a launch film**: "sound like Hans Zimmer composed it" meant weight, tension and
  a build, while "it should still sound like a product launch".

## The body

- **Low → high**: start from near-silence or a bed, add layers as the product appears, go full on the first real
  action (Notion's pattern: "he started from low, then highs").
- **Suspense on failure, then pick it up**: muffled darkest bars, ticking on the beat, and a recovery that doesn't climb
  "too high too quickly". After checks pass, more energy "for a while".
- **Gentle, selective ducking**: no audible pumping, no dip for every tiny interaction; duck for typing and hero
  effects only.
- **Verify a generated or edited track's grid**; don't assume it holds a steady tempo.

## What the ear asked for on one film (in order, all kept)

| Note | Change |
|---|---|
| Background lower, effects louder | music −2 dB, effects +2 dB (~4 dB relative) |
| Slower, a little quieter | 150 → 140 BPM, music −2 dB |
| 44 s too loud | the push after Merged from +5 to +2 dB, then 0 |
| Music under the phone typing lower | duck −4 → −10 dB |
| Merged hits too hard | merge effects group −6 dB, music dipped 6 dB under the hit |
| First 20 s should carry more | music +2 dB to 20 s |
| 2.5 s silence at the end, not 1.5 | final bars start 2 beats later |
