# Changelog

## 1.0.0 — 2026-10-20

First public version.
- 8 skills: launch-film-studio, reference-study, music-to-picture, sfx-sync, mix-master, frame-review,
  footage-cleanup, stage-and-camera.
- 7 tested scripts: beatgrid.py (fold-verified tempo, sample-accurate beat phase), picture-events.py (cuts, region
  changes, splice finder; robust to footage animated on twos), audio-check.py (loudness, section deltas, effect
  attack/peak and audibility, ducks), review-sheets.sh, master-mux.sh (two-pass −14 LUFS, explains peak-limited
  results), sfx-synth.py (effects placed by their audible point), wallpapers.py (original stage backgrounds).
- Evals for every skill; validator (Agent Skills spec incl. compatibility/metadata, links, evals, shared copies,
  plugin versions, privacy); end-to-end smoke test; CI on every push and pull request.
- Installs: Claude Code plugin, Codex plugin, `gh skill`, `npx skills`, git submodule, and one zip per skill for
  claude.ai / Claude Desktop (built and attached by the release workflow).
- README with generated visuals (banner, timing diagram, backgrounds), FAQ and a real revision walkthrough;
  CODE_OF_CONDUCT, SECURITY, issue and pull-request templates.
