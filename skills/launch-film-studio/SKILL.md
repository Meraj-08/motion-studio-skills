---
name: launch-film-studio
description: >
  Direct a product launch film, promo, showreel or motion ad made in code (HyperFrames, Remotion or a seek(t) page)
  from the product's REAL screens, with music cut to the picture and frame-accurate sound, then run the revision
  rounds. Use when someone wants a launch or product video built from their app or site, wants a soundtrack fitted,
  swapped or re-cut on an existing film, gives timestamped notes ("44 s hits too hard", "the merge sound is late",
  "make the ending more cinematic"), or wants several music versions of one picture. This is the director: it plans,
  sets the gates and routes to the other motion-studio skills (reference-study, music-to-picture, sfx-sync,
  mix-master, frame-review, footage-cleanup, stage-and-camera).
license: MIT
---

# Launch film studio

The prompt is 10 % of a film; the harness is the other 90 %: real assets in, measure the picture, cut real music to
it, put every sound on a frame, look at your own frames, fix the three worst problems, repeat. This skill is the
director. The craft lives in the sibling skills; this one decides the order and holds the gates.

## Hard rules

1. **Real product UI only.** Capture the real app or site. Never redraw screens or show states the footage doesn't
   contain. Filling empty UI is allowed only when asked: match it from the recording and say it is illustrative.
2. **Measure the rendered picture; never trust a brief's timecodes.** One event table (`docs/EVENTS.md`) drives
   music, effects and titles. When a brief and the picture disagree, the picture wins. Confirm key frames by eye.
3. **Every frame is a pure function of time.** No timers, CSS transitions or unseeded randomness in render mode.
4. **One change per version.** Everything not pointed at stays bit-identical; prove it. Report measured before and
   after in the reviewer's words ("44 s is now 3.5 dB quieter; nothing else moved").
5. **Licences decide what ships.** Record the source and licence of every track and asset; add credit lines.
   Anything without a release licence is labelled "internal review only".
6. **Ask first** before downloading anything (name, source, size), recording flows that trigger real side effects,
   spending paid API credits, or publishing. Keys live in `.env` and are never printed.
7. **Be honest about references.** Say what you measured, what you watched, and what you couldn't open or hear.
8. **Never overwrite an approved deliverable.** New version number for every change; back up sources and settings.

## Collect before building

| Input | Notes |
|---|---|
| Product + URL, the one story to tell | One feature per short film; one story point per scene in longer ones. |
| Duration, formats, frame rate | 1920×1080@60 master; 9:16 and 1:1 reframed from the same timeline, never cropped. |
| Real footage, or access to record it | App recordings at native resolution; phones via screen mirroring. |
| References | Give each one job (pacing, an entrance, a transition). See the `reference-study` skill. |
| Music | 2–3 licensed candidates, or "you choose". |
| Brand | Logo, colours (hex), fonts, the CTA line, and any earlier official film as the brand reference. |
| What must not change | The approved version, in a revision round. |

Effort: new film or treatment → high/xhigh; small fixes and remixes → medium; a flagship opening → max.

## Pipeline (do not skip gates)

1. **Study, then brief.** Run `reference-study` on the references. Write `BRIEF.md` from
   [references/brief-templates.md](references/brief-templates.md). **Gate:** the shot list is approved.
2. **Capture and clean.** Record the real flows; actions at 1×, only travel and waiting sped up (≤ 2.4×). Clean
   them with `footage-cleanup`.
3. **Build the picture.** Each product shot is an event: start state → cursor to the control → press → result →
   a reading hold. Stage, camera and motion: `stage-and-camera`. Render three stills (opening, product result,
   closing) first. **Gate:** stills approved.
4. **Lock the moments.** `scripts/picture-events.py` on the render, tight `--region` checks on every UI change that
   gets a sound, a frame strip to confirm by eye. Write `docs/EVENTS.md`.
5. **Music.** `music-to-picture`: measure each candidate, cut it to the story points on its own downbeats.
6. **Effects.** `sfx-sync`: one audible sound per event, placed by the point the ear hears.
7. **Mix and master.** `mix-master`: ducks, headline markers, a build into the end card, −14 LUFS / −1 dBTP.
8. **Review loop.** `frame-review`: sheets → scores → fix the three worst → repeat until every score is 8+.
9. **Deliver.** Render the picture once, mux one soundtrack per version. See [references/shipping.md](references/shipping.md).

## Revision rounds (most of the work)

Reviewers judge by ear and eye, in small steps, pointing at timestamps. Every fix that lands answers one timestamp.

- **Translate the note into a measurement.** "44 s hits too hard" → which group peaks there (often a low layer under
  the named sound), by how much → change that group only.
- **Find the frame, and check it by eye.** A badge logged at 42.867 s actually flipped at frame 2570 = 42.833 s;
  the hit sat 3 frames late until a frame strip showed it.
- **Verify a suspected offset against the picture before fixing it.** A fresh render can be the stale one.
- **Loudness normalization hides relative changes.** Report the stem change and what the final mix does.
- **Options as samples, not films:** a still gallery (same frame, only the variable changes) → 6–7 s motion samples
  of the affected moments → the full render of the chosen one.
- **Reviewers narrow, then pull back** ("only before 20 s"). Splice versions where the frames agree.
- **If a version is rejected,** go back to the approved one, not to the rejected one plus a patch.
- **Reply with:** what changed, the measured numbers, file paths (full + small), what was left alone.

## What costs time (don't repeat)

- Taking brief timecodes on trust; assuming a fresh render matches an older assembled picture.
- Changing two things in one version, so neither can be judged.
- A synthesized or generated music bed instead of a real track: it hits every frame and still reads as monotonic.
- Building ten variants before agreeing on a reference or stills.
- Sub-bass-only effects (silent on laptops), stacked effects, mascot cameos mid-film, music under a character's walk.
- A "fade, stop, swell" ending; an intro on a different musical theme from the body.
- A 4K render on a nearly full disk (it needs ~18 GB of temp). Check `df -h` first.

## Scripts (Python needs numpy; `pip install -r requirements.txt` at the repo root)

| Script | Use |
|---|---|
| `scripts/beatgrid.py track [--json f] [--bpm n]` | Tempo (fold-verified), beat phase, downbeats, bar loudness, sections, end. |
| `scripts/picture-events.py film [--region x,y,w,h] [--compare b]` | Cuts, motion per second, the frame a UI element changes, splice points. |
| `scripts/audio-check.py mix [--vs old] [--events t:label] [--duck a-b]` | LUFS/TP, dynamics, section deltas, effect sync and audibility, duck depth. |
| `scripts/review-sheets.sh film out [--strip t] [--stills t,t] [--loop]` | Contact sheet, phone sheet, frame strip, stills, loop check. |
| `scripts/master-mux.sh pic wav out` · `--sharpen in out` | Two-pass −14 LUFS master + mux (video copied) + small copy; light sharpen. |

## References

- [references/brief-templates.md](references/brief-templates.md): project house rules, director's brief, frame-numbered shot spec, `EVENTS.md`, edit requests, and seven brief formats that worked.
- [references/case-study.md](references/case-study.md): a 73.5 s launch film second by second, every review note and what fixed it.
- [references/shipping.md](references/shipping.md): versions, deliverables, licences, storage, packaging the service.
