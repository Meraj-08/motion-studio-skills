# Motion: engine, springs, shot grammar, camera, formats

## Engine: one clock, any frame on demand

Whatever the framework, the film is `render(t)`: paint the exact frame for time t, no state carried between frames.

- **HyperFrames (HTML + GSAP)**: the default here. One GSAP timeline/clock calls `film.render(t)`; clips are
  `<video>` elements with `data-start` and `data-media-start` (trim). Render:
  `npx hyperframes render -c <file>.html -f 60 -q delivery --video-frame-format png --quiet -o out.mp4 .`
  A sample composition can remap time (play 6.6–11.0 then 44.6–46.9) to preview two moments cheaply.
  If `film.js` looks up element ids, every composition (samples too) must contain them, or the render dies with
  "Cannot read properties of null". Generate samples from the current `index.html`, don't hand-copy old ones.
- **Remotion (React)**: drive everything from `useCurrentFrame()`; `npx remotion still Comp out.png --frame=N` for
  stills, `--frames=90-149` for a partial render.
- **Plain seek(t) page**: `window.seek = t => draw(t)`; Playwright calls it per frame and pipes PNGs to ffmpeg. Wait
  for `document.fonts.ready` first. Optional motion blur: render 4 subframes per frame and blend (`tmix`) — apply blur
  only to fast entrances, keep reading holds sharp.

Determinism check: render the same 5 s twice and compare hashes. Seeded noise only (mulberry32 or similar).


## Springs (motion that feels expensive)

Closed form, so any frame can be computed directly:

```js
function spring(t, k = 170, d = 26) {             // 0 → 1
  if (t <= 0) return 0;
  const w0 = Math.sqrt(k), z = d / (2 * w0);
  if (z < 1) { const wd = w0 * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t)); }
  return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
}
// A value with several targets: add one spring per change, never restart. keys = [[time, value], ...]
const track = (t, keys, k, d) => keys.slice(1).reduce((v, [tk, vk], i) => v + (vk - keys[i][1]) * spring(t - tk, k, d), keys[0][1]);
// Tab indicator that stretches: leading edge stiffer (320/30) than trailing edge (140/22).
// Text inside a morphing box: enters ~0.08 s after the morph starts, leaves 0.1 s before the next one.
```

Feel: snappy UI 300+/28 · default containers and camera 170/26 · heavy type and logos 120/24 (no overshoot) ·
mascots and stickers visible overshoot. Tiny overshoot on UI, none on type.


## Shot grammar

- **A product shot is an event**: starting state → cursor to the control → the press registers → result appears →
  hold. The viewer must be able to follow one thing.
- **Main object first**, supporting information ~0.1 s later. Keep attention on the control until its response
  appears, then let the result own the reading window.
- **Reading holds**: count from the frame the words are legible; read aloud at normal speed; extend any hold that ends
  first. 8 frames at 30 fps is 0.27 s, too short for anything.
- **Speed**: actions (typing, clicks, taps) at 1×; only travel and waiting sped up (≤ 2.4×). Give UI actions time:
  a reviewer asked for +2 s on an automation scene.
- **Something meaningful every 2–4 s**, except deliberate holds (intro title, the success moment, the end card ≥ 3 s).
- **Highlights**: few, identical in shape and timing. Rings or highlights point at a result better than zooming in
  and out.
- **Titles**: one headline + one supporting line, top-centred; switch exactly when the UI shows that state.
- **Mascots/characters**: opening and ending only. Mid-film cameos were "totally not needed".


## Camera and depth

- One 3D moment reads as a choice; two read as a gimmick (the side angle was kept on the first scene only).
- A side angle that worked: CSS perspective 2600 px, about −16° turn and 7° tilt; flat on the hand-over frame (7.0, where the
  baton's line becomes the input box); squares up before the push into the prompt (10.5).
- Wide establishing → push in on the action → ease out. Don't zoom a UI below 1.0× source pixels (soft text);
  replace footage rather than enlarging it.
- Never `will-change` on anything the camera scales (blurry text). A slow push: 1.00 → 1.03 over 3 s; constant
  percentage changes compound.


## Formats

Write scenes against a layout function (safe area, title box, product box), not fixed pixels, and render 16:9, 1:1
and 9:16 from the same timeline. Reframe type and UI per format; never crop a 16:9 render to vertical. Check text at
360 px wide (`review-sheets.sh` phone sheet).
