# Case study: a 73.5 s launch film, 85 versions in 8 days

A launch film for a developer tool that runs a fleet of coding agents. HyperFrames composition, 1920×1080 @ 60 fps,
real app recordings (desktop and phone). It went from a 25–30 s brief to 73.5 s as the story grew, then through about
40 rounds of sound and picture notes. Everything below was measured on the rendered picture.

## The film, second by second

| Time | On screen | Sound |
|---|---|---|
| 0.0–7.0 | The logo as a character walks in, lands (3.0), raises a baton, tosses it; the sticks collapse into the app's input box | footsteps and landing only; the music enters at the transition (6.3) |
| 7.0 | The app appears, product title | reveal; music building |
| 10.1–12.9 | A request typed, then sent | typing; the music ducks; the drop lands on Send (12.9) |
| 14.28 · 15.57 · 16.72 | Three workers appear in the sidebar | three soft rising plucks |
| 21.0 · 27.0 | Agent picker · task board | headline markers: a one-beat dropout and a short swell |
| 33.1 → 38.39 | Checks fail → the agent fixes it → checks pass | suspense: dark muffled bars, ticks and a heartbeat on the beat; lift at 38.39 |
| 41.45 · 42.833 | Merge click · the badge flips to "Merged" | a short stop under "Merging…", the biggest return on the badge |
| 45.0 → 48.35 | Automations: dialog, fields typed, Create | headline marker; typing duck |
| 51.95 → 66.4 | Phone: task typed → Start → thinking → the answer writes out → scroll → back → new task circled | the track's breakdown, building from 63 into the landing |
| 66.3 · 67.0 | The character drops in · lands with the end card | the closing's loudest hit, on the landing |
| 67.0–73.5 | Two-line idea + Download button | the track's own final bars, then ~2.5 s of silence |

## How the review notes were answered

| Note | Change |
|---|---|
| "The sound is 5/10: clicks and transitions aren't placed right" | studied reference films frame by frame; one sound per event, every event audible |
| "Too monotonic" (twice, even with a 17 dB volume arc) | real produced tracks with chord changes and sections, instead of generated loops |
| "Sounds overlap; the success sound is too loud" | one sound per event; the success group −6 dB with the music dipped under it |
| "The intro music is off-theme from the rest" | no music under the walk; the track's build starts after the transition |
| "The transition from 6 to 8 s / 47 to 50 s isn't smooth" | switch tracks inside motion, never mid-groove; stay in one track to the end |
| "Make a suspense on the failure, then pick it up" | darkest bars, ticks speeding up; the recovery starts on the same chord |
| "I can't hear the typing" | the bed −6 to −10 dB under typing; real recorded keyboard and phone sounds |
| "Phone part: show it thinking, smoother scroll, ~10 s" | recorded the real thinking state, a paced answer reveal, a stitched smooth scroll |
| "At 49 s, a ring instead of zooming in and out" | ring highlights at results |
| "Flat 13–50 s; the quiet section loses people; −16 LUFS is quiet" | headline markers, a riser into the end card, master −14 LUFS / −1 dBTP |
| "2.5 s of silence at the end, not 1.5" | the final bars start 2 beats later |
| "The website shots look empty; keep the black contrast" | illustrative sidebar rows matched from the recording; the stage tinted, never the UI |
| "Blue only before 20 s" | spliced at 20.0 s, where the two versions differ by 0.5/255 |
| "Just sharpen it a little" | a light luma unsharp mask on the final picture instead of a 4K render |
| A phone status bar showed a hotspot pill | rebuilt per frame with a clean take's Wi-Fi bar |

## Soundtracks on one picture

Six licensed tracks were cut with the same story-point arrangement, so each became a version of the same film:
150 BPM future bass (slowed to 140 with rubberband), 120 BPM hip-hop, 110 BPM drive, 118 BPM travel pop, 88/176 BPM
product groove, 110 BPM brand track. Measured with `beatgrid.py`; one tempo logged earlier as 144.4 BPM folded sharply
only at 110.00, and its headline markers had to be re-snapped.

Four fully synthesized scores (swing jazz with a modelled sax, a cinematic score, a "band warms up" funk show, a warm
115 BPM score) hit every frame and were all set aside for real tracks. Synthesis stayed for effects and stingers.

## What each phase taught

| Phase | Lesson |
|---|---|
| First drafts | Generated beds read as monotonic; sub-bass effects vanish on laptops. |
| 10 opening variants, all rejected before one was picked | Agree on a reference or stills before building variants. |
| The approved original | Rebuild an assembled section inside the composition when anything behind it must change. |
| Generated scores | Exact sync is not enough; a real track wins. |
| Fitting the approved music to a longer cut | Loop whole phrases at downbeats; one measured change per version. |
| Six licensed tracks | The same arrangement makes soundtracks interchangeable on one picture. |
| Review suggestions applied | Turn suggestions into measurable rules (markers, riser, loudness, end silence). |
| Stage colour across the film, then only before 20 s | Reviewers narrow, then pull back; splice where frames agree. |
| Final round | Render once, mux many; a frame strip caught a 3-frame sync slip the logs had missed. |
