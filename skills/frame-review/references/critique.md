# Review loop: make the model watch its own frames

Iteration is the method, not a failure. Look at what was rendered, as a harsh motion director, before anyone else does.

## Make the images

```bash
scripts/review-sheets.sh out/film.mp4 review/v12                       # contact (2 fps) + phone (360 px)
scripts/review-sheets.sh out/film.mp4 review/v12 --strip 42.8          # 12 consecutive frames around a fast moment
scripts/review-sheets.sh out/film.mp4 review/v12 --stills 0.5,7,42.833,70
scripts/review-sheets.sh out/film.mp4 review/v12 --from 40 --to 48     # only the re-rendered section
python scripts/picture-events.py out/film.mp4                          # dead seconds, jumps
```

Open every PNG and look properly. Then play it at normal speed with sound.

## Score (1–10 each) and log it

Hook in the first 2 s · readability at phone size · motion quality (springs, no dead frames, no sliding) · variety (new
thing every 2–4 s) · composition · brand and product accuracy (real UI only) · sound sync · sound clarity (every event
audible, nothing stacked, music has shape).

Write scores and the 3 biggest problems with timestamps to `docs/review_log.md`. Fix those three, re-render only the
affected seconds, re-score. Stop at 8+ everywhere, not before.

## Hunt for

Text overlapping during swaps · anything sliding instead of easing · corner labels, frame borders · centered title on a
gradient · blurry scaled text · a beat with nothing happening · a hold too short to read aloud · the cursor crossing a
headline · a background changing mid-scene · UI the recording doesn't contain · a stutter at a loop seam · an effect
that can't be heard on a laptop · two effects at once · music flat for more than ~15 s.

## Critique prompt

```text
Open review/vN/contact.png, phone.png and strip-*.png and look at them properly. Be a harsh motion director, not a
proud author. Score 1–10: hook, phone readability, motion, variety, composition, product accuracy, sound sync, sound
clarity. List the 3 biggest problems with timestamps. Fix them, re-render only the affected seconds, show me the new
sheets and scores. Change nothing else.
```

For an independent critique, open a fresh session with the brief, the sheets and the extracted frames; accept up to
five frame-specific corrections and hand them to the builder.

## Local repair loop

```text
observed defect → one scoped edit → affected frames → the surrounding scene boundary → normal-speed playback
```

Label frames explicitly: local frame 30 of a sequence starting at global frame 120 is global frame 150. After a local
edit, check both neighbouring boundaries before watching the assembled film. Fix order: missing information and
unreadable text → timing → visual detail.

## How reviewers score and react

- Scores are blunt, out of 10 or 100 ("5/10", "45, make it 90"). Treat a low score as "go back to the references and
  the last approved version", not "polish more". A self-assigned score is never proof.
- Managers and teammates review too; carry their notes into the brief.
- "What if I say none of them I liked?" Before building many variants, agree on a reference or stills.
- "No sound" reports: check the playback device first (often Bluetooth earbuds) before touching the mix.

## Human review rounds

- Send the small copy (1280 wide) first; the full file when they ask.
- For choices, send samples: still galleries, 6–7 s clips of only the affected moments, the last 20 s for an ending.
- Expect notes as timestamps and feelings ("hitting too hard", "not smooth", "more cinematic"). Ask one clarifying
  question only when the note could mean two different sounds ("typing" meant the phone's typing, not the desktop's).
- If a version is rejected, go back to the approved one, not to the rejected one plus a patch ("after 1:02 the old one
  was better" → the old ending restored inside the new version).
