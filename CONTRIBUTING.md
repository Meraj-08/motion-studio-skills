# Contributing

Thanks for helping. New skills, sharper measurements and more reference studies are all welcome.

## Ground rules

- **Every rule should answer a real problem.** "Whooshes peak 100–250 ms before the cut" is useful because it was
  measured on real films. Add the evidence (a measurement, a reference, a review note) with the rule.
- **Measured, estimated, opinion: say which.** Skills must never claim to have watched or heard something they couldn't.
- **Real product UI only.** No skill may tell an agent to invent screens, states or results.
- **No private material**: no local paths, personal e-mail addresses, keys, client names, or footage/music you don't
  have the rights to. The validator scans for the common cases.

## Layout

```
skills/<name>/SKILL.md          frontmatter (name = folder, description with "Use when …"), body under 500 lines
skills/<name>/references/*.md   detail the SKILL.md links to (links must stay inside the skill folder)
skills/<name>/scripts/          copies of shared scripts (generated; do not edit here)
skills/<name>/evals/evals.json  prompts, expected behaviour, assertions, and prompts that should NOT trigger it
shared/scripts/                 the only place to edit scripts
shared/manifest.txt             which skill ships which script
```

## Workflow

```bash
pip install -r requirements.txt          # plus ffmpeg on PATH
# edit skills/… or shared/scripts/…
python3 scripts/sync_shared.py           # copy shared scripts into the skills that ship them
python3 scripts/validate_skills.py       # spec, links, evals, shared copies, privacy
python3 scripts/smoke_test.py            # every script, end to end, on generated media
```

Add a line to `CHANGELOG.md` and bump the version in both `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` (the validator checks they match).

## Writing a good skill

- The description decides whether an agent loads the skill: say what it does and list the phrases people actually use
  ("the music is monotonic", "44 s hits too hard").
- Keep `SKILL.md` to the workflow and the rules; move tables, recipes and studies into `references/`.
- Prefer a script that measures over a paragraph that guesses. Scripts print what they measured and what they assumed.
