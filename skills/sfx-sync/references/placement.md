# Placing sound effects

The effect set rarely needs to change; what matters is where each sound sits in time and how loud it is next to
the music.

## Every event gets one sound, and you can hear it

- **Every event needs a sound** that sits clearly above the music; the music ducks under it. A reviewer could
  "understand everything by sound" in the version where every step, landing and transition had its own cue.
- **One sound per event, never stacked.** Several effects on one hero moment read as clutter. Check overlaps: two
  effects whose audible spans overlap within 12 dB of each other are both heard at once.
- **Warm, varied, soft.** Soft clicks on real actions; typing and taps varied (several samples, small pitch and level
  changes), never one sample repeated. No bright or whistly effects.
- **Audible on laptops and phones.** At least half an effect's energy in 400 Hz–4 kHz (`audio-check.py --events`
  prints the share). Sub-bass-only jumps and landings were reported as "missing". Listen through a 300 Hz high-pass as
  a phone proxy.
- **Synthesize effects in code when nothing fits** (click = short decaying sine ~1.8 kHz; pop = rising sine; thump =
  falling 90→30 Hz sine plus a mid click so it reads on small speakers; whoosh = shaped noise). Use real recorded foley
  for typing and taps where you can (a real phone recording became the phone taps).


## Sounds reviewers asked for by name

- **Typing must pop.** If typing can't be heard, lower the bed under it and raise the typing; use real recorded
  phone/Mac typing and send sounds (a screen-recorded clip of real typing became the phone taps and the send on
  the drop), cleaned of any music, drum or clap in the recording. Key sounds only while characters appear.
- **Ticking in the failure section** (on the music's beats, speeding up), as in the version they liked.
- **The merge click** gets its own distinct sound; the success sound must not be too loud (halved, then −6 dB group).
- **No odd tones**: a "cut" sound and a high tone at 4 s were rejected.
- **Landing**: offer 3–4 high-quality step and landing options in a 10 s sample before choosing (the reviewer picked a
  specific library impact); the landing can sit a little louder than the steps.
- **Mobile**: soft taps, a clear send, a small notification, the music thin underneath.
- **Endings** spread across the last seconds rather than one late hit; if a sound effect gets cut off, extend the
  picture 1–2 s.


## Place by the point the ear hears

- **Clicks, taps, keys: onset (attack) on the frame.** **Hero hits: on the frame.** **Whooshes into a cut: peak
  100–250 ms before the cut** (the ear cues the eye). **Arrivals (cards, phone, landing): on the settle, ~250 ms after
  the move starts.** **Risers: their end on the hit.** (Measured on Procreate Dreams, Solimar and Notion; see
  the `reference-study` skill.)
- **On the frame the eye sees.** Measure the frame with `picture-events.py --region` (tight box around the element),
  and the sound's audible point in its file; offset = frame − (point within the file).
- Check: `audio-check.py sfx_stem.wav --events 12.9:send,42.833:merged` → Δ within ±20 ms of attack or peak.
- Never "fix" a suspected offset before checking the picture: the phone effects looked 0.3 s late against a fresh
  render, but the fresh render was the stale one.

