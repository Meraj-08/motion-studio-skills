# What great launch films do (measured studies)

Studied in Oct 2026 while making a launch film (whatships.com, Ordinary Folk, X posts). Sound was measured, not heard (loudness per 0.5 s, low/mid/high bands, onsets, spectrograms,
cut ↔ onset coupling against chance) and checked against frames. Say the same when you report a study: what you
measured, what you watched, and what you could not access. Never claim to have watched a video you couldn't open.

## The films

| Film | Length · loudness | What to take |
|---|---|---|
| **Figma: Spec** | 41 s · −12.8 LUFS, LRA 2.2 · 128 BPM, C major | First frame is the product's own button; the press opens the film (press on beat 2, cut on beat 3). Camera stays very close; words cropped at the frame edge on purpose; real cursors keep the page alive. Short rhythmic dropouts each bar instead of UI clicks. Ends: Send → hard cut to black → two-line idea → logo, music falls away. |
| **Notion: Custom Agents** | 71 s · −13.6, LRA **14** · ~115 BPM, D major, warm | Opens on near-silence with tiny ticks; bass/pads bed at 4 s; a one-second breath (−12 dB) at 14 s; full music arrives **with the product**. Each agent added gets a rising note (every ~0.75 s): the build is the agents. **The click is the downbeat** (cut and hit same frame). Groove stays ±3 dB but changes chords (5 roots), +2–3 dB accent on each chapter title, one lighter passage, a snap gesture switches day→night. Ends on a real "+ New Agent" click, 3 s wind-down, silence on the logo. |
| **agentplay** | 39 s · −21.4 | Zero hard cuts: word → particles → dot → iris → UI, each scene grows out of the last. Dark field for statements, light for product. Sound follows the gestures. Weakest audio of the set (flat plateau). |
| **Procreate Dreams** (Ordinary Folk) | 34 s · −12.1 · G minor | Portal on black opens the world under a riser; a blink is the cut; every cut a match on shape or motion; loops seamlessly. Tightest sync: 60 % of strong hits within 100 ms of a picture event; **sound leads by ~130 ms** (the ear cues the eye). |
| **Solimar** (Ordinary Folk) | 48 s · −14.2 · D minor | The brand glyph (a sphere) is the hero object carrying every transition. Only 1 % still frames; whips heavily blurred; grain and gradients on the brand layer only. One continuous swell; **whooshes peak 230–270 ms before the cut**. |
| **Paper Mono** (+ making-of) | 60 s · −15.8, LRA 3.2 · 138 BPM, A minor | The edit is code on the song's grid. Sparse intro → drop at 10.5 s → plateau → **full stop at 24 s** → breakdown at 46 s (top filtered) → rebuild → stuttered ending. Bar-end hi-hat gates, a three-hit stutter into the breakdown. Almost no effects: the music carries the film. Its audio is the most-requested reference in the set. |
| Cluely mascot film | 46 s | **Near-silence one second before the reveal, a drop on the unveiling**; re-appearances get a music re-entry. |
| Claude Code Review | 45 s | First half breathes (music drops out every ~2 s), second half commits to a steady groove; breath → total silence on the logo. Mascot gets no cartoon effects: the music carries it. |
| Cognition: Devin | 34 s · 95 BPM | A drop on each title-card change; breath → fade to silence as the logo forms. |
| OpenAI launch | 70 s | A breath/drop or impact every 3–7 s; never still for more than 7 s; ends hit → breath → silence. |
| Cursor for iOS · Claude Mobile Tools | 74 s · 52 s | Mobile sections are the intimate moment: music low and even, highs rolled off, or a breakdown with bass out and −8 to −11 dB; a drop when the next screen appears. |

## Motion language from launch posts on X

Measured with the scripts in this repo (picture-events, audio-check, beatgrid) and read from contact sheets, 20 Oct 2026.

| Film | Measured | Visual grammar worth taking |
|---|---|---|
| **OpenCode 2** (Kit Langton, 47.7 s) | −14.3 LUFS, LRA **1.4** (dead even), 112 BPM; 2 hard cuts in the body | Opens on `$ opencode` typed in a terminal → glitch reveal of the logo → an accent line wipes into the product. **Captions typed char by char in monospace with a block cursor, bottom-left, in two beats** ("steer it now." → "or queue it for later.") while macro crops of the real UI show that exact action. One accent colour (orange) on key words. Ends: stats line ("3,869 commits · 47 contributors") → logo + the install command. |
| **Watchtower** (olucurious, 30 s) | −11.6 LUFS, LRA **13.6**, 120 BPM, true peak +0.7 (overs) | App icon pulses in a ring → name types in → tagline. **Hold the frame, let the state change**: one framed diagram or panel stays while the data inside updates (Unresolved → assigned → Resolved). Headlines with one accent word ("Errors, grouped by **cause**."), lists built word by word ("Slack. Linear. Email. Agents."). Dark purple vignette stage, one accent. Ends on lockup + GitHub URL. |
| **Cursor side chats** (17 s, silent) | no audio; 4 jumps | Real app on a landscape wallpaper → **extreme macro on the selected text** (selection highlighted in the accent colour) → oversized cursor hovers and clicks "Add to Side Chat" → macro on the composer chip → **snap back to the full window** → plain white end card "Side Chats · Available Now" → animated logo mark. The wide ↔ macro rhythm in 17 s. |
| **One** (Kyzo, 31.6 s) | −16.1 LUFS, LRA 7.5, 120 BPM; **opening cuts every 0.5 s = on the beat** (1.0, 1.5, 2.0, 2.5) | Supported tools as name chips over a new nature photo each beat → dots on a light grid assemble → "Every agent. One inbox." → a small mascot ("Agent needs you") → **left headline + right UI** ("Answer in a keystroke." with **keycap overlays showing the keys pressed**) → "Press to talk." → dark-mode switch for "Something's still waiting." → phone lock screen → "Nothing needs you." → mascot → lockup over the opening photo world. One idea per 3–4 s block, a long final hold. |
| Other downloaded launch clips | iamdavidhill 21 s: −32 LUFS ambient, 92 BPM; im_gusye 103 s: −20.9 LUFS, 115 BPM, 54 jumps; mattgapp 31 s: animated on twos at 24 fps, −16.2 LUFS; claudeai, cursor_ai: silent | Many polished launch clips are quiet or silent; loud, dynamic mixes (Watchtower, Notion) are the exception and feel the most cinematic. |

Takeaways added to the rules:
- **Captions as a typed sentence in two beats** that follow the product state (first half lands with the problem, second
  with the fix). Keep them in one corner, monospace if the product is a dev tool.
- **Keycap or gesture overlays** make an invisible action visible (keys pressed, a tap); keep them visibly separate
  from the product UI.
- **Wide ↔ macro**: establish the window, go macro on the one thing being acted on, snap back at the scene change.
- **Hold the frame and let the UI change** instead of moving the camera for every state.
- **Cutting a montage on every beat** works for a 2–3 s list (supported tools, integrations), not for product actions.
- Even loud social mixes should stay under 0 dBTP; Watchtower's +0.7 dBTP clips on some players.

## Workflow video (Lukas Margerie, "How to Make Insane Motion Graphics With Opus 5.5", 20 min, 29 Sep 2026)

From its description and chapter list (the transcript wasn't readable here): how Opus 5.5 makes video → motion-studio
rules that ban generic output → adding a real brand (brand and spec files) → a voiceover in a cloned voice (Fish
Audio MCP) → scoring to a 120 BPM beat → stealing a reference video's style → the director's brief and a critique loop
→ packaging the pipeline as a skill. Same harness as the Movez course; it adds **voiceover/voice cloning** for
narrated launch films, and names MagicPath and Diffusion Studio as other tools.

## What they have in common

1. **The first frame is the idea, not a logo.** The product's action, the problem, a portal, the brand glyph. Sound or
   a riser under frame 1. The hero object appears within ~1 s (a long character intro needs a reason).
2. **Every transition has a cause on screen**: a product action (a click cuts), a gesture (snap, blink, stroke), or a
   hero object crossing the cut. No transition is "just a wipe".
3. **Sound is phrase-level, with a few frame-exact heroes.** Most films cut on phrases and let music flow through cuts.
   Hero moments (the press, the reveal, the success) are frame-exact.
4. **Sound timing by type** (measured):
   - clicks and state changes: on the frame (0 ms)
   - whooshes into cuts: peak 100–250 ms **before** the cut
   - arrivals (cards, phone, a character landing): on the **settle**, ~250 ms after the move starts
5. **Silence is punctuation**: open from near-silence, a breath (0.2–1 s) before each reveal, a full stop before the
   success, silence on the final logo (6 of 8 films end in silence or a fade).
6. **One accent colour**; a light/dark switch marks a change of chapter.
7. **Clarity comes from scale and one thing at a time**: close crops on real UI, cursors larger than life, few labels.
   Texture (grain, brush, gloss) lives on the brand layer, never on the UI.
8. **Pace**: median shot 1.3–2.1 s for product films.
9. **Endings**: a two-line idea on a plain field → logo; or the CTA as a real product button being clicked.

## Why music sounds "monotonic" (and how to measure it)

Loudness range is not the cause. Notion's body is almost loudness-flat yet never monotonic; a generated score with a
17 dB arc still was. Monotony comes from (1) the same bar repeating, (2) no chord movement, (3) no new instrument at
section changes. Measured: loop score (bar vs 2 bars earlier) 0.988 with one chord root for 56 s = monotonic; Notion
0.951 with 5 roots; comastudio 0.919 with i–VI–V. Volume automation on a loop is still a loop: use produced music
with a progression and sections, edited to picture.

## Rules this gives a product launch film

- **Mascot / character opening**: foley-led (its own steps carry the first seconds, music barely there); a riser under
  the activation; a 0.2–0.5 s breath before the reveal; the drop on the reveal cut; the end-card character rhymes with
  the opening (same landing family, final hit on the lockup); no cartoon voices or boings.
- **Product demo**: harmony and texture change, not just level; a breath before each chapter title; a lighter passage
  under a mid section, full again on the next big reveal; a breakdown when something fails, a build toward the
  success click, a stop under the waiting state, the biggest drop on success; UI sounds few and musical (arrival notes
  in the track's key, the click on the beat where possible).
- **Mobile**: the most intimate section (low-pass, −3 to −5 dB, bass thinned), one small notification sound, a
  beat-aligned breath as the phone rises.
- **Lockup**: the final hit lands on the lockup, rings 2–3 s, the last ≥ 1.5 s near-silent.

## Where to find more

- whatships.com: launch films by product; the five used here were figma-specs, factory-environments, agentplay,
  notion-ipad, paper-mono-code. The pages link out to X, so download the clip (with the OK) to study frames.
- Ordinary Folk's studio work (Procreate Dreams, Solimar): motion-led edits with match cuts.
- The product's own X account and recent launch posts, checked against the running app (previews lag the product).
