# Shipping: versions, deliverables, licences, the offer

## Render once, mux many

The picture is the expensive part. Render it once per picture change, then put each soundtrack on it with the video
stream copied (`master-mux.sh picture.mp4 soundtrack.wav out.mp4`). Six music versions of one picture cost six muxes,
not six renders. Sharpen the picture master once (`--sharpen`), never inside every mux.

## Naming and backups

- `deliverables/<product>-<dur>s-v<N>-<track>.mp4` and `…-small.mp4`; the approved original is `…-FINAL.mp4`, the
  previous original keeps its own name (`…-71s-FINAL.mp4`).
- `review/v<N>/`: the exact composition, mixer scripts, stems, picture render and a `render.log` for that version.
  A `tools/rebuild-v<N>.sh` for the approved original.
- When someone says "make vN the new original": copy to `…-FINAL`, snapshot its sources, note it in the project log, and do
  all later changes on it.
- Version log (`docs/VERSIONS.md`): version, what changed, outcome (kept / option / rejected / picked).

## Before delivering

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate,duration -of json out.mp4
python scripts/audio-check.py out.mp4                 # −14 LUFS, ≤ −1 dBTP, end silence as agreed
scripts/review-sheets.sh out.mp4 review/vN            # last look
```

Watch the export once at normal speed: first message, product action, ending.

Deliver: final MP4 (+ small), a poster frame from an approved frame, the contact sheet, the licence/credit line for the
music, and one sentence on what you would improve next.

## Licences

| Source | Use |
|---|---|
| Pixabay music | free, no credit (some tracks are Content ID registered: whitelisting may be needed on YouTube) |
| Uppbeat free | credit line in the description; limited downloads a month; the account holder declares the licence |
| Openverse (api.openverse.org) | per-item licence (CC0, CC BY …): record the attribution |
| AI-tool or ripped audio | internal review only |
| Remotion | commercial use depends on its licence tier for the company size; check the terms |

## Storage

Renders, stems and frame-sequence recordings grow fast (one 73 s project reached 22 GB). Keep the approved original,
the current versions and their sources; move superseded review folders and stems to the Trash with a dated folder
(never hard-delete); convert JPEG frame sequences to one high-quality video per recording once clips are cut.

## Packaging it as a service (from public motion-studio playbooks)

- Start small: one feature, one approved script, one 20 s video at 1080×1080, one cover image from an approved frame,
  one revision round covering timing, copy and sound. An illustrative pilot price used publicly: $150.
- Build one complete sample first (your own product or one whose owner agreed), and time the whole job.
- Pitch a specific action: "Your export feature could be the entire 20-second clip."
- Agree script, assets, deadline, payment, revision scope, usage rights and portfolio use before starting. Feedback
  tied to frame numbers keeps the included revision bounded. Extra formats, scenes and source files are quoted
  separately.
