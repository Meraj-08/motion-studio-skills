# Security

## What these skills can do

Skills are instructions plus small local scripts. The scripts only read the media files you point them at, call
`ffmpeg`/`ffprobe`, and write images, audio or video to the output paths you give. They make no network requests,
read no credentials, and need no API keys. The skills tell agents to keep any keys in `.env` and never print them.

As with any skill, read what you install: `gh skill preview Meraj-08/motion-studio-skills <skill>` shows the files
before installing.

## Reporting a vulnerability

Please report security issues privately through a
[GitHub security advisory](https://github.com/Meraj-08/motion-studio-skills/security/advisories/new), not in a public
issue. Include the skill or script, what you ran, and what happened. You'll get a reply within a week.
