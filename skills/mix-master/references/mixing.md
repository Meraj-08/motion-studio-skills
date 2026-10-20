# Balance, loudness and change-safe mixing

## Ducking and balance

- Music under typing −6 to −10 dB; under the phone typing −10 dB was right.
- The success moment is the loudest point of the film; when it "hits too hard", lower the whole hit group (the named
  sound alone moved the moment 0.5 dB because a low impact layer under it set the peak) and dip the music under it.
- A send on a drop: the effect lands on the drop and the drop on the frame.
- Report gain changes in the reviewer's terms and the final mix's terms (below).


## Loudness: read it the way the master hears it

- Social master: −14 LUFS integrated, ≤ −1 dBTP (`master-mux.sh`, two-pass, linear). Earlier internal masters at −16.
- **The master is normalized**, so lowering music 2 dB lowers it only 0.2–0.8 dB in the final mix; the rest shows up
  as louder effects. Always report the stem change *and* `audio-check.py new --vs old --sections …`.
- Dynamics: body p90–p10 ≥ ~8 dB on the music for a film with real ups and downs.


## Change-safe mixing (so one note never breaks the rest)

- Mixers take **opt-in switches** (env vars such as `MERGE_T`, `MERGE_DB`, `TYPING_DB`, `START_DB`, `MUSIC_DB`,
  `SEC_DB="a:b:dB,…"`, `END_FADE`). With no switches the mixer rebuilds the approved stem bit for bit; check that
  after every edit (`cmp` or a hash).
- **Edit by difference**: render the stem with and without the change, add the difference to the approved stem,
  confirm that only the intended span changed.
- **Gain window on the approved stem** when a fresh render no longer lines up with an older assembled stem (phone taps
  −3 dB over 53.80–55.55; Start task +4 dB over 55.69–56.40).
- Name every stem and soundtrack with its version (`stem-sfx-v67.wav`, `soundtrack-<track>-v71.wav`) and snapshot the
  mixer script with it in `review/v<N>/`.
- Rendering a mixer may overwrite shared intermediates: back them up before, restore after.


## Before you send a soundtrack

1. `audio-check.py mix.wav`: LUFS, true peak, body spread, end silence.
2. `audio-check.py sfx.wav --events …` on every event in `docs/EVENTS.md`.
3. `audio-check.py music.wav --duck …` on every typing span.
4. `audio-check.py new.wav --vs approved.wav --sections …`: only the sections you meant to change moved.
5. Listen once on laptop speakers and once on a phone, at the timestamps the reviewer named.
