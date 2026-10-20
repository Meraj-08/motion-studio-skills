# Toolkit: frameworks, skills and repos worth knowing

Check each repo before installing, and ask before installing anything. Pick only what the film needs.
All links were checked reachable on 2026-10-19.

## Frameworks

- **HyperFrames** (HTML + GSAP): https://github.com/heygen-com/hyperframes — best when you think in web pages.
- **Remotion** (React): https://www.remotion.dev/docs/ai/skills — best for series, templates, data-driven videos.
- **GSAP** timelines (now fully free): https://github.com/greensock/GSAP
- Plain seek(t) + Playwright + ffmpeg: zero dependencies; the route a one-shot prompt picks by default.

## Skills from the motion-studio threads (Oct 2026)

| Skill / repo | What it adds | Link |
|---|---|---|
| /anatomy-reveal | exploded product views, product-reveal MP4 | https://typingmind.com/skills/annnguyentt-anatomy-reveal |
| /anatomy | machines and systems as isometric figures | https://skills.wheresryan.sh/anatomy |
| /hairline | line figures from an idea or SVG | https://hairline.lucasmarkes.com/skills |
| motion-design-skill | timing, easing, Disney's 12 principles for UI | https://github.com/LottieFiles/motion-design-skill |
| ai-kit (Motion) | motion docs, CSS springs, animation audits | https://github.com/motiondivision/ai-kit |
| blender plugin | AI 3D team inside Blender via MCP | https://github.com/scenario-labs/blender-plugin |
| react-three-rapier | real physics for React Three Fiber | https://github.com/pmndrs/react-three-rapier |
| react-postprocessing | bloom, depth of field, film effects | https://github.com/pmndrs/react-postprocessing |
| Openverse API | 5M+ openly licensed sounds and images (record each licence) | https://api.openverse.org/v1/ |
| claude-animation-skill | Node canvas rigs, pens, synthesized sound | https://github.com/buildwithhanif/claude-animation-skill |

## Examples to study

- Starter: https://github.com/JohnHeibel/ClaudeAnimationBase · music video with subagents per chapter
  (`ANIMATION_GUIDE.md`, `STORYBOARD.md`): https://github.com/JohnHeibel/PDoomVideo
- Long form: https://github.com/WinterArc21/Battle-of-Austerlitz-Film
- Prompt library: https://github.com/guanmo-ai/awesome-ai-motion · dataset of Opus 5.5 videos:
  https://github.com/athemeroy/awesome-opus-5-5-videos

## Prompt patterns worth reusing

- **Showreel one-liner** (tests the engine, not the idea): "make a dynamic 15-second motion graphics video that shows
  what an incredible motion designer you are, like it's your showreel for a résumé. go all out." Hundreds of people
  used it, so the results rhyme ("brief contagion"): move on after the first test.
- **Brand reel**: product URL + "use actual product screenshots, logo, assets" + "must have music"; one session per
  brand so the renderer and audio pipeline are reused.
- **One shape, never cut** (UI morph spec): a single container morphs through 8–12 product states on a 120 BPM grid,
  a cursor drives every change, the last frame equals the first.
- **Director's brief for long pieces**: logline, references, tools and keys, character bible, beat sheet, text rules,
  workflow gates, critique loop, deliverables. Generate-then-trace (a video model renders base motion, code redraws it)
  gives physics that's hard to hand-code with a consistent drawn look.
- **Subagents per chapter**: write `ANIMATION_GUIDE.md` first so every subagent codes in the same style.

## Workflow sources

- Movez, "How to build motion design studio with Opus 5.5 (Full-course)": x.com/0xMovez/status/2104216919033192746
- beamnxw, "Motion Engineering with Opus 5.5": x.com/beamnxw/status/2108616740846420354
- Movez, "10 must-have skills and repos": x.com/0xMovez/status/2111841847408517282
- Lukas Margerie, "How to Make Insane Motion Graphics With Opus 5.5": youtube.com/watch?v=747ZnEtsRbg (adds voiceover
  with a cloned voice, MagicPath, Diffusion Studio)
- whatships.com (launch films by product) · Ordinary Folk (studio motion work)
