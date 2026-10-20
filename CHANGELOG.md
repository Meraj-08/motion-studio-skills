# Changelog

## 1.0.0 — 2026-10-20

First public version.
- 8 skills: launch-film-studio, reference-study, music-to-picture, sfx-sync, mix-master, frame-review,
  footage-cleanup, stage-and-camera.
- 7 tested scripts: beatgrid.py (fold-verified tempo, sample-accurate beat phase), picture-events.py (cuts, region
  changes, splice finder; robust to footage animated on twos), audio-check.py (loudness, section deltas, effect
  attack/peak and audibility, ducks), review-sheets.sh, master-mux.sh (two-pass −14 LUFS, explains peak-limited
  results), sfx-synth.py (effects placed by their audible point), wallpapers.py (original stage backgrounds).
- Evals for every skill; validator (Agent Skills spec, links, evals, shared copies, privacy); end-to-end smoke test;
  CI on every push and pull request.
