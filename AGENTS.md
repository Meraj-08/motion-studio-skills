# Working in this repo (for coding agents)

This repo is a library of agent skills for motion, video and audio work. Read CONTRIBUTING.md first.

- Edit scripts only in `shared/scripts/`, then run `python3 scripts/sync_shared.py`.
- After any change run `python3 scripts/validate_skills.py` and `python3 scripts/smoke_test.py`; both must pass.
- A skill's links must stay inside its own folder (each skill installs alone).
- Keep SKILL.md bodies under 500 lines; put detail in `references/`.
- Never add local paths, personal data, keys, or third-party footage/music.
- Do not commit or push unless the maintainer asks.
