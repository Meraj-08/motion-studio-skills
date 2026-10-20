# Stage and background around app footage


- **Tint the stage, never the screen.** The app's own UI (the black contrast) stays exactly as recorded.
- **Busy background under a fading window shows through** (the "ghost window"): put a dark plate shaped like the
  window under it so it fades up from black, and start the stage fade early.
- **Keep a background through a whole section, or switch where the window fills the frame.** A background that
  changes mid-scene reads as an error. A brand-blue stage ran only to 20.0 s, where the window covers the frame.
- **Choosing**: stills of the same frame per background → narrow → 6–7 s motion samples → full render. Generated
  wallpapers (silk folds, ribbons, ridges in numpy) are original and safe; photos need their licence and an OK
  before downloading.


## Generate original backgrounds

`scripts/wallpapers.py --gallery stages/ --size 1920x1080` renders every preset (silk folds, ribbons, ridges) as
stills of the same size, ready for a side-by-side choice. `--style silk --colors 04081a,0e286e,286edc,82c8ff` makes
one in brand colours. They are generated, so no licence is needed; use photos only with their licence and an OK.
