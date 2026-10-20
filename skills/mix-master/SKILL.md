---
name: mix-master
description: >
  Balance music and effects for a product or launch video and master it for social platforms (−14 LUFS, −1 dBTP)
  without touching the picture: ducking under typing, headline markers, a build into the end card, end silence, the
  success moment as the loudest point, and change-safe edits that move only what a note points at. Use when someone
  says the background is too loud, "44 s hits too hard", "make it quieter here", "it sounds flat", "louder for
  social", or wants a soundtrack muxed onto a rendered video, and when reporting before/after numbers.
license: MIT
compatibility: Needs ffmpeg/ffprobe (with loudnorm and ebur128 filters), bash and Python 3 with numpy.
metadata:
  author: Md Meraj Alam
  version: "1.0.0"
  repository: https://github.com/Meraj-08/motion-studio-skills
---

# Mix and master

A note names a timestamp and a feeling. The answer is one measured change, proven to touch nothing else, reported in
the reviewer's words.

## Workflow

1. **Translate the note into a measurement.** `scripts/audio-check.py mix.wav` (loudness per second) and
   `--events` around the timestamp: which group actually peaks there? ("Merged hits too hard" was a low impact layer
   under the named sound, not the sound itself.)
2. **Change one group, one span.** Use opt-in switches in the mixer, or a gain window on the approved stem, or add
   the difference of a re-render to the approved stem. With no switches the mixer must rebuild the approved stem
   bit for bit; check it after every edit.
3. **Prove nothing else moved:** `audio-check.py new.wav --vs approved.wav --sections 0-7,7-21,…`.
4. **Master and mux** with the picture copied: `scripts/master-mux.sh picture.mp4 soundtrack.wav out.mp4`
   (two-pass linear loudnorm to −14 LUFS / −1 dBTP, AAC 320k, plus a small review copy).
5. **Report** the stem change and what the final mix does: loudness normalization hides relative moves (music
   −2 dB changed the master by only 0.2–0.8 dB; the rest showed up as louder effects).

## Balance that held up

- Music under typing −6 to −10 dB; gentle, selective ducking (no pumping, no dip for every tiny interaction).
- Headline markers: on the beat nearest each scene change, a one-beat dropout (−15 dB) and a short reverse swell.
- A build into the end card: from ~4 s out, filter opens, +5 dB, a riser, an 80 ms breath before the hit.
- The success moment is the loudest point; if it "hits too hard", lower the whole hit group and dip the music under it.
- The opening can carry a little more (+2 dB for the first 20 s was asked for).
- Body dynamics p90–p10 ≥ ~8 dB on the music for a film with real ups and downs.
- ~2.5 s of silence at the end; social master −14 LUFS integrated, ≤ −1 dBTP (never above 0).

Details: [references/mixing.md](references/mixing.md).

## Sharpen once, not per mux

`scripts/master-mux.sh --sharpen picture.mp4 picture-sharp.mp4` (luma unsharp 5:5:0.5) on the picture master, then
mux every soundtrack onto the sharpened picture.

## Scripts

| Script | Use |
|---|---|
| `scripts/audio-check.py mix [--vs old --sections …] [--events …] [--duck a-b]` | Loudness, dynamics, section deltas, effect sync, duck depth. |
| `scripts/master-mux.sh pic wav out` · `--sharpen in out` | Two-pass master + mux (video copied) + small copy; light sharpen. |
