---
name: frame-review
description: >
  Make the agent watch its own rendered video before anyone else does: contact sheets with film time, phone-size
  sheets, frame strips around fast moments, exact stills, a loop check, then a harsh scored critique, the three worst
  problems with timestamps, a scoped fix and a re-render of only the affected seconds. Use after any render of a
  motion graphic, launch film or product video, when someone says "it looks mid", "5/10", "make it 90", "check the
  transition at 18 s", or before sending a version for review.
license: MIT
compatibility: Needs ffmpeg/ffprobe, bash and Python 3 with numpy; an image-capable model to read the sheets.
metadata:
  author: Md Meraj Alam
  version: "1.0.0"
  repository: https://github.com/Meraj-08/motion-studio-skills
---

# Frame review

Iteration is the method, not a failure. Look at what was rendered as a harsh motion director, not a proud author.

## Loop

1. **Make the images**
   ```bash
   scripts/review-sheets.sh film.mp4 review/vN                    # contact (2 fps, film time) + phone (360 px)
   scripts/review-sheets.sh film.mp4 review/vN --strip 18.2       # 12 consecutive frames around a transition
   scripts/review-sheets.sh film.mp4 review/vN --stills 0.5,7,42.833,70
   scripts/review-sheets.sh film.mp4 review/vN --from 40 --to 48  # only a re-rendered section
   python scripts/picture-events.py film.mp4                      # dead seconds, jumps, motion per second
   ```
2. **Open every image and look properly.** Then play it at normal speed with sound.
3. **Score 1–10**: hook in the first 2 s · readability at phone size · motion quality · variety (something new every
   2–4 s) · composition · product accuracy (real UI only) · sound sync · sound clarity.
4. **Log** scores and the 3 biggest problems with timestamps in `docs/review_log.md`.
5. **Fix those three** with one scoped edit each, re-render only the affected seconds, check both neighbouring scene
   boundaries, re-score. Stop at 8+ everywhere.

## Hunt for

Text overlapping during swaps · anything sliding instead of easing · corner labels, frame borders · a centered title
on a gradient · blurry scaled text · a beat with nothing happening · a hold too short to read aloud · the cursor
crossing a headline · a background changing mid-scene · UI the recording doesn't contain · a near-empty frame between
scenes · a stutter at a loop seam · an effect you can't hear on a laptop · two effects at once · music flat for 15 s.

## A fix request has four fields

Location (global frame) · observed problem · the change · what stays fixed. Order: missing information and unreadable
text → timing → visual detail. Local frame 30 of a sequence starting at global frame 120 is global frame 150.

Full critique prompt, scoring notes and how reviewers react: [references/critique.md](references/critique.md).

## Scripts

| Script | Use |
|---|---|
| `scripts/review-sheets.sh film out [--strip t] [--stills t,t] [--loop] [--from s --to s]` | The images to look at. |
| `scripts/picture-events.py film [--region x,y,w,h] [--compare b]` | Jumps, dead seconds, the frame a UI element changes. |
