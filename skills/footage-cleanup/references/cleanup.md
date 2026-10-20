# Footage cleanup

## Footage cleanup (do it in the source clip, once)

- **Empty UI** (when asked): add rows in the app's own style, measured from the recording: row pitch, font sizes,
  RGB of title/age/dots, truncation x. Same added rows in every shot that shows them, dimmed on the exact frame a
  dialog backdrop appears, shifted when real rows arrive. Disclose as illustrative.
- **Re-layout flicker** (an app re-lays out for ~0.25 s when a status changes): replace those frames with the settled
  screen, then cut them from the source.
- **Phone status bar** (hotspot pill, wrong time/battery): per frame, fill the strip with that frame's own background
  colour, redraw a plain Dynamic Island, composite the glyphs ("12:20 · Wi-Fi · 78 %") from a clean take, sampled at a
  time the clean take actually shows them (not frame 0). Same time in every take.
- **Joining takes**: an eased hand-off (scale 0.98, +78 px) plus a 0.15 s dissolve hid the join between two phone
  recordings. Rebuild assembled sections inside the composition (one shot per take with its original camera moves)
  when anything behind them must change; verify frame-for-frame against the old render.
- **Splicing two versions**: find frames where both agree (`picture-events.py a --compare b`); < 1.0 mean difference
  is an invisible straight cut.


## Sharpness

A light luma unsharp mask on the final picture (`unsharp=5:5:0.5:5:5:0.0`, `master-mux.sh --sharpen`) adds 60–70 %
edge contrast on UI text with no halos. Rendering at 4K and downscaling is cleaner but needs ~18 GB of temp disk;
only do it when asked and `df -h` allows.


## Picture notes from real reviews (each one was a fix)

- **Opening character**: distinct steps and weight shifts, legs attached at every pose (fix joint anchoring), a contact
  shadow that follows walk, take-off and landing, a stable floor and intentional scale (the character must not seem to
  shrink), anticipation → clear airborne pose → squash → settle. Red only as the activation accent, then back to the
  brand palette. The first part should feel subtle.
- **Into the product**: the eye (later the baton's line) must match the destination window in position and shape; no
  frame of old UI or dark bars during the hand-over; short red overlay; the UI readable promptly.
- **Introduce the product before features**: one clean title + one verified benefit line, settled before the next
  action.
- **Readability**: wide to establish, then close on the action; enlarge the request, picker, cards, failing checks and
  merge; remove tiny category labels; phone-size check. A reviewer called a CLI section "a bit mockup-type": show the
  real app instead.
- **Transitions**: no near-empty frame between scenes; keep the new task card as the anchor into the board; consistent
  window position, scale, background and direction across cuts; a match cut when recordings can't join, never a fake
  morph or an implied relationship between different recordings; editorial annotations visibly separate from the UI.
- **Highlights**: no blue circles on the first frames; at a result, a ring instead of zooming in and out.
- **CI → merge**: failing → fix → passing → Merge → Merged, each readable, Merged held ~2 s; labels switch exactly when
  the UI does; if the footage contradicts the story (an agent saying it couldn't open the PR), replace it.
- **Scheduling/automation**: shorten routine typing, show the saved result, don't end while the viewer waits.
- **Mobile**: ~10 s max but not rushed (+1–2 s when it felt fast); establish the whole phone, then crop; desktop leaves
  as the phone rises in one move; start → "generating/thinking" → the answer writing out → smooth scroll that doesn't
  jump back up → back → the new task highlighted; skip opening an older task. Use the latest app build.
- **Lockup**: larger logo, CTA and URL, readable at phone size; held ≥ 3 s; no black gap before it.
- **Product accuracy**: record the current app (model names and features shown must be the current ones, e.g. the
  model picker); keep accurate older footage.

