# Synthesized sound: recipes and when to use them

On one launch film, four complete synthesized scores were built from detailed specs (swing jazz with a modelled sax, a cinematic
launch score, a "band warms up" funk show, a warm 115 BPM B♭ score). Every one hit its frames exactly; none replaced a
real recording as the bed. **Use synthesis for effects, stingers, risers, ticks and short accents; cut a real track
for the music bed.** If a synthesized score is requested anyway, build it, and use these recipes so it isn't harsh.

## What made generated music fail (from a real audio brief)

- A harsh, buzzy lead: raw square/saw energy at 3–5 kHz. Fix: band-limited oscillators (PolyBLEP), formant filters,
  a 4th-order low-pass around 4.2 kHz, soft saturation.
- The same loop repeated at two climaxes. Fix: new material at each peak.
- A typing loop running where nobody types. Fix: trigger key sounds only on frames where characters appear.
- Drops that miss the cuts (27.0, 48.2 s were late by ~2 s). Fix: measure the picture, anchor each section.
- An outro that hits a harsh static burst, then 5.5 s of dead silence. Fix: a musical resolution, then silence.

## Instrument recipes (numpy / scipy.signal)

| Voice | Recipe |
|---|---|
| **Sax lead** | Harmonics 1–8 with weights `[1.0, .75, .55, .35, .22, .12, .06, .03]` → `tanh(1.6·x)` reed saturation → three parallel formant band-passes at 650 Hz (body), 1400 Hz (warmth), 2600 Hz (presence) → 4th-order Butterworth low-pass 4.2 kHz. Notes > 0.4 s: 60 ms scoop from −1.5 semitones; 5.5 Hz vibrato ±12 cents fading in after 0.25 s. |
| **Upright bass** | Pluck envelope (attack 8 ms, exponential decay τ 0.22 s), fundamental + 2nd + 3rd harmonics, low-pass 380 Hz. Or Karplus–Strong for a real pluck. |
| **Brushes / ride / hats** | Filtered noise: brush swish band-pass 1.2–7 kHz; ride 5–11 kHz on swung 8ths; hat chicks on 2 and 4. |
| **Pads / keys** | FM electric piano (modulator ratio 1:1 and 14:1 for the tine); PolyBLEP saw through a ladder low-pass with slow cutoff movement. |
| **Space** | Velvet-noise reverb impulse (sparse ±1 impulses, exponential decay) instead of a long synthetic tail; light tape saturation on the bus. |

Engines that worked: PolyBLEP oscillators, a numba ladder filter, Karplus–Strong strings, FM e-piano, velvet-noise
IR, tape saturation. Keep render deterministic (seeded noise).

## Effect recipes (these did ship)

| Effect | Recipe | Placement |
|---|---|---|
| Key "thock" | 12 ms burst: 250 Hz body + 2.2 kHz click, small random pitch/level per key | only on frames where a character appears |
| UI click | short decaying sine ~1.8 kHz + a few ms of filtered noise | onset on the frame |
| Wooden tap (baton) | resonant impulse at 1.8 kHz, 3 taps | on the gesture frames |
| Low-end impact | 60–90 Hz sine, exponential decay, **plus a mid click** so laptops and phones hear it | on the hit frame |
| Riser | noise + rising band-pass and pitch over 2–4 s, ending exactly on the hit (an 80 ms breath before it) | end on the frame |
| Ticking pulse | dry ticks on the music's own beats, speeding up (quarters → 8ths → 16ths) under suspense | on the music grid |
| Arrival notes | short plucks in the track's key, rising (e.g. D5 · G5 · B5) for things appearing one by one | on the settle |
| Filter drop | music low-passed with a quick cutoff fall on a failure | on the failure frame |

## Arrangement ideas worth keeping

- **Band warm-up** ("one starts with an instrument, then the team joins, like a band showing off before the concert"):
  layered entries, one instrument per section, each solo on a story beat, everyone together on the success.
- **Low → high build** (Notion): bed first, drums only when the product arrives, steps up in pitch per added item.
- **Solo tag outro**: drums and bass stop on the closing line; a short unaccompanied phrase resolves to the root.
- **Even, warm variant** (~115 BPM, B♭, heavy bass, quiet, very even volume) was tried and not chosen: the final
  preference was dynamic music with clear sections.

## ElevenLabs (when generated sounds are wanted)

- Good for effects tied to a character (footsteps, jump, landing, activation) when no library sound fits; it was
  requested for mascot moments.
- Generated music tends to ignore its section plan and come out flat; profile it per half-second before using it,
  and build the dynamics in the mixer.
- Check the remaining credits first and say them (one music track ≈ 725 credits); the key lives in `.env`.

## Generate them with `scripts/sfx-synth.py`

`click`, `thock` (keys, varied per press), `tap`, `tick`, `pop`, `send`, `pluck=<note>`, `impact` (with a mid layer
so laptops hear it), `whoosh=<len>` (peak on the cue), `riser=<len>` (ends on the cue). Each is placed by its audible
point, so `--cue 42.833:impact` lands the hit on that frame. Verify with `audio-check.py --events`.
