# Motion Studio Skills

**Agent skills for making launch films, product videos and motion graphics that look and sound finished.**
Real product screens in, music cut to the picture, every sound on its frame, a review loop that makes the agent
watch its own frames — plus seven tested measurement tools so the agent works from numbers, not guesses.

Works with Claude Code and any agent that supports the [Agent Skills](https://agentskills.io) format (Codex,
Cursor, Copilot and others through `npx skills`). Built on top of composition frameworks like
[HyperFrames](https://github.com/heygen-com/hyperframes) and [Remotion](https://www.remotion.dev); these skills are
the director, editor, sound designer and reviewer around them.

> Built while making one 73.5-second launch film through 85 versions in 8 days: every rule here answers a real
> review note ("44 s hits too hard", "the merge sound is late", "it sounds monotonic", "the intro is off-theme").

[![validate](https://github.com/Meraj-08/motion-studio-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Meraj-08/motion-studio-skills/actions/workflows/validate.yml)
![skills](https://img.shields.io/badge/skills-8-6aa6f8) ![license](https://img.shields.io/badge/license-MIT-green)

## Why

Most "one-prompt" motion videos look the same: centered text on a gradient, everything fading in, a logo, a stock
track playing straight through. The prompt is 10 % of a good film. The other 90 % is the harness:

1. **Measure the picture**, never trust a brief's timecodes.
2. **Cut real music to the story**, on its own downbeats.
3. **Put one audible sound on each event**, placed by the point the ear hears.
4. **Look at your own frames**, score them, fix the three worst problems, repeat.
5. **Change one thing per version**, prove nothing else moved, report it in the reviewer's words.

## The skills

```
                         ┌───────────────────────────┐
                         │    launch-film-studio      │  the director: inputs, gates, revision rounds
                         └─────────────┬─────────────┘
        ┌───────────────┬──────────────┼───────────────┬────────────────┐
        ▼               ▼              ▼               ▼                ▼
 reference-study   footage-cleanup  stage-and-camera  music-to-picture  sfx-sync
  study refs        real UI, fixes   stage, camera,    measure & cut     effects on
  into rules        splices, sharpen springs, formats  tracks to story   the frame
                                                           └──────┬───────┘
                                                                  ▼
                                          frame-review  ◄──  mix-master
                                          look, score, fix     balance, −14 LUFS
```

| Skill | Use it when you… | Ships |
|---|---|---|
| [`launch-film-studio`](skills/launch-film-studio/SKILL.md) | want a launch or product film from real screens, or have timestamped notes on one | brief templates, a full case study, shipping checklist |
| [`reference-study`](skills/reference-study/SKILL.md) | share reference videos: "make it like this" | measured studies of 15+ launch films, REFERENCE.md format, toolkit |
| [`music-to-picture`](skills/music-to-picture/SKILL.md) | need a track fitted, swapped, slowed or re-cut to the picture | `beatgrid.py`, the story-point arrangement |
| [`sfx-sync`](skills/sfx-sync/SKILL.md) | need UI and motion sound effects on exact frames | `sfx-synth.py`, placement rules, DSP recipes |
| [`mix-master`](skills/mix-master/SKILL.md) | hear "too loud at 44 s" or need a social master | `master-mux.sh`, change-safe mixing |
| [`frame-review`](skills/frame-review/SKILL.md) | just rendered something and want it checked properly | `review-sheets.sh`, critique prompt, scoring |
| [`footage-cleanup`](skills/footage-cleanup/SKILL.md) | have glitches, wrong status bars, joins, soft text | splice finder, cleanup techniques |
| [`stage-and-camera`](skills/stage-and-camera/SKILL.md) | find the screen flat or want 3D, backgrounds, vertical cuts | `wallpapers.py`, springs, shot grammar |

## Install

**Claude Code plugin**
```
/plugin marketplace add Meraj-08/motion-studio-skills
/plugin install motion-studio@motion-studio-skills
```

**Any agent ([skills CLI](https://github.com/vercel-labs/skills))**
```bash
npx skills add Meraj-08/motion-studio-skills                         # all skills
npx skills add Meraj-08/motion-studio-skills --skill music-to-picture sfx-sync
```

**Manual**: copy any folder from `skills/` into `~/.claude/skills/` (or your agent's skills folder). Each skill is
self-contained: its scripts travel with it.

**Tools the scripts need**: `ffmpeg` and `ffprobe`, and Python with numpy (scipy for backgrounds):
`pip install -r requirements.txt`.

## Try it

```text
Make a 30-second launch film for our app from these recordings (rec/*.mp4). Site: https://example.com.
Study refs/notion.mp4 for pacing first, and show me the shot list before you build.
```
```text
v12 is approved. At 44 s the music hits too hard and the merge sound feels late. Fix only that.
```
```text
Give me three versions of the same film with these licensed tracks: a.mp3, b.mp3, c.mp3.
```
More in [examples/prompts.md](examples/prompts.md).

## The tools

All seven are tested end to end in CI on media they generate themselves (`scripts/smoke_test.py`).

| Script | What it measures or makes |
|---|---|
| `beatgrid.py` | tempo pinned by a full-track fold (150.00 / 120.00 / 110.00 on real tracks), sample-accurate beat phase, bar loudness, section changes, where the music ends |
| `picture-events.py` | hard cuts, motion per second, dead seconds, the exact frame a UI element changes, frames where two versions agree (invisible splices) |
| `audio-check.py` | LUFS and true peak, dynamics spread, per-section before/after, effect attack and peak vs the frame, audibility on small speakers, duck depth |
| `review-sheets.sh` | contact sheet labelled with film time, phone-size sheet, 12-frame strips, exact stills, loop check |
| `master-mux.sh` | two-pass −14 LUFS / −1 dBTP master muxed with the picture copied, a small review copy, a light sharpen |
| `sfx-synth.py` | clicks, varied key thocks, taps, sends, plucks in key, impacts audible on laptops, whooshes peaking on the cue, risers ending on it |
| `wallpapers.py` | original silk, ribbon and ridge backgrounds in any colours, so a stage never needs a licence |

## What the reference films taught (short version)

- The first frame is the idea, not a logo. Every transition has a cause on screen.
- Clicks land on the frame; whooshes peak 100–250 ms before the cut; arrivals land on the settle.
- Silence is punctuation: a breath before reveals, silence on the final logo.
- Monotony comes from repeated bars and no chord changes, not from a flat volume.

Full measured studies (Figma, Notion, agentplay, Procreate Dreams, Solimar, Paper Mono, OpenCode 2, Watchtower,
Cursor, One…) in [`reference-study`](skills/reference-study/references/reference-films.md).

## Contributing

Issues and PRs welcome — new skills, better measurements, more reference studies. Read
[CONTRIBUTING.md](CONTRIBUTING.md); run `python3 scripts/validate_skills.py` and `python3 scripts/smoke_test.py`
before opening a PR. Shared scripts live in `shared/scripts` and are copied into skills by
`python3 scripts/sync_shared.py`.

## Credits

The working method stands on public work by
[Movez](https://x.com/0xMovez/status/2104216919033192746) (the motion-studio course and the
[10-tool list](https://x.com/0xMovez/status/2111841847408517282)),
[beamnxw](https://x.com/beamnxw/status/2108616740846420354) (frame-numbered motion engineering),
[Lukas Margerie](https://www.youtube.com/watch?v=747ZnEtsRbg), [whatships.com](https://whatships.com) and
[Ordinary Folk](https://ordinaryfolk.co). Skill format from [Anthropic's skills](https://github.com/anthropics/skills).
Reference films are analysed for technique only; no footage or music from them is included.

## License

[MIT](LICENSE) © 2026 Md Meraj Alam
