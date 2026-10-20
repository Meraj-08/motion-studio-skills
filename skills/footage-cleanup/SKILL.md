---
name: footage-cleanup
description: >
  Prepare real app and phone screen recordings for a product film: cut actions at 1× and speed only travel, remove
  app re-layout flicker, rebuild a phone status bar (hotspot pill, wrong time) from a clean take, join takes with an
  eased hand-off, splice two versions where their frames agree, fill empty UI in the app's own style when asked, and
  sharpen the final picture lightly. Use when footage shows glitches, a status bar or notification that shouldn't be
  there, a jump between recordings, an empty-looking screen, soft text, or when two versions must be combined.
license: MIT
compatibility: Needs ffmpeg/ffprobe, bash and Python 3 with numpy.
metadata:
  author: Md Meraj Alam
  version: "1.0.0"
  repository: https://github.com/Meraj-08/motion-studio-skills
---

# Footage cleanup

The product is the evidence. Clean the recording once, in the source clip, and never invent a state it doesn't show.

## Rules

- **Real UI only.** Recording beats redrawing. If a needed state was never recorded, say which recording is missing.
- **Speed**: actions (typing, clicks, taps) at 1×; only travel and waiting sped up, ≤ 2.4×.
- **Crops at ≥ 1.0× source pixels**; replace footage rather than enlarging it soft.
- **Illustrative fill** (extra list rows, a fuller sidebar) only when asked: measure pitch, font sizes and RGB from
  the recording, keep the same rows in every shot, dim them on the exact frame a dialog backdrop appears, and
  disclose them as illustrative.
- **Never imply a relationship between recordings** the footage doesn't support: different sources join by a clean
  match cut, not as "the same task".

## Techniques

| Problem | Fix |
|---|---|
| App re-lays out for ~0.25 s when a status changes | replace those frames with the settled screen, then cut them from the source |
| Phone status bar wrong (hotspot pill, time, battery) | per frame: fill the strip with that frame's own background colour, redraw a plain Dynamic Island, composite the glyphs from a clean take sampled when it shows them; same time in every take |
| Two phone takes must join | an eased hand-off (scale 0.98, +78 px) and a 0.15 s dissolve; rebuild assembled sections inside the composition when anything behind them changes, then verify frame for frame |
| Combine two versions | `picture-events.py a.mp4 --compare b.mp4 --from 15 --to 25`: < 1.0 mean difference is encoding noise, an invisible straight cut |
| Soft UI text | `master-mux.sh --sharpen in out` (luma unsharp 5:5:0.5: +60–70 % edge contrast, no halos), once, on the picture master |
| The exact frame of a state change | `picture-events.py film --region x,y,w,h` with a tight box, then a frame strip to confirm by eye |

Details and the picture notes that came out of real reviews: [references/cleanup.md](references/cleanup.md).

## Scripts

| Script | Use |
|---|---|
| `scripts/picture-events.py film [--region x,y,w,h] [--compare b]` | Jumps, the frame a UI element changes, splice points. |
| `scripts/review-sheets.sh film out --strip t` | 12 consecutive frames to confirm a fix by eye. |
| `scripts/master-mux.sh --sharpen in out` | Light sharpen of the picture master. |
