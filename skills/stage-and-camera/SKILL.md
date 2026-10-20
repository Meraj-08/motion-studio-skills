---
name: stage-and-camera
description: >
  Stage, camera and motion for app footage in a product film: the background around the app window (generated
  wallpapers, brand colour, photos), a dark plate under fading windows, a 3D side angle, wide-to-macro camera moves,
  closed-form springs instead of easing, shot grammar for product actions, and reframing for 9:16 and 1:1. Use when
  someone says the screen looks flat or empty, wants a modern or 3D look, a website-style background behind the app,
  "something like Apple", smoother camera moves, or vertical versions.
license: MIT
---

# Stage and camera

Tint the stage, never the screen. One camera trick per film reads as a choice; two read as a gimmick.

## Rules

- **The app's own UI stays exactly as recorded** (its black contrast included). Colour and texture go around it.
- **A busy background under a fading window shows through** ("ghost window"): put a dark plate shaped like the window
  under it so it fades up from black.
- **Keep a background through a whole section**, or switch where the window fills the frame.
- **Choose with stills, then samples**: a gallery of the same frame with only the background changing → 6–7 s motion
  samples of the affected moments → the full render.
- **Every frame is a pure function of time**; springs are closed-form, so any frame can be rendered directly.

## Camera

- Wide to establish, then macro on the one thing being acted on, then snap back at the scene change.
- Hold the frame and let the UI change, rather than moving the camera for every state.
- A side angle that worked: CSS perspective 2600 px, about −16° turn and 7° tilt; flat on any hand-over frame,
  squared up before a push into the action.
- Never zoom UI below 1.0× source pixels; no `will-change` on scaled elements (blurry text).

## Motion

Closed-form spring, and one spring per change for values with several targets:

```js
const track = (t, keys, k = 170, d = 26) =>
  keys.slice(1).reduce((v, [tk, vk], i) => v + (vk - keys[i][1]) * spring(t - tk, k, d), keys[0][1]);
```

Snappy UI 300+/28 · containers and camera 170/26 · heavy type and logos 120/24 (no overshoot). Full engine notes,
spring code, shot grammar and formats: [references/motion.md](references/motion.md).

## Backgrounds

```bash
python scripts/wallpapers.py --gallery stages/ --size 1920x1080          # every preset as a still, to compare
python scripts/wallpapers.py --style silk --colors 04081a,0e286e,286edc,82c8ff --out brand-stage.png
python scripts/wallpapers.py --style ridges --colors ffbe98,f0a0ac,aa96e8 --out dusk.png
```

Rules for choosing and placing them: [references/stage.md](references/stage.md).

## Scripts

| Script | Use |
|---|---|
| `scripts/wallpapers.py --preset name --out f.png` · `--gallery dir` | Original silk, ribbon and ridge backgrounds. |
| `scripts/review-sheets.sh film out --stills t,t` | Same-frame stills to compare treatments. |
