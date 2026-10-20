#!/usr/bin/env python3
"""Validate every skill against the Agent Skills spec and this repo's own rules. Run: python3 scripts/validate_skills.py

Checks
  SKILL.md   frontmatter opens on line 1 and closes; name = folder, lowercase a-z 0-9 '-', ≤ 64; description 1–1024 chars;
             body under 500 lines
  links      every relative link in a skill's markdown resolves INSIDE that skill (each skill must install on its own)
  scripts    every `scripts/<file>` a skill mentions exists in that skill; Python compiles; shell passes `bash -n`
  evals      evals/evals.json is valid, names the skill, and each eval has prompt, expected_output, assertions
  shared     skill copies of shared scripts match shared/scripts (scripts/sync_shared.py --check)
  plugin     .claude-plugin/plugin.json and marketplace.json are valid JSON with matching versions
  privacy    no local home paths, e-mail addresses, private keys or API-key-looking strings anywhere in the repo
Exit code 1 on any error; warnings don't fail.
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors, warnings = [], []
err = lambda m: errors.append(m)
warn = lambda m: warnings.append(m)


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    return None, None


def parse_yaml(lines):
    """Enough YAML for skill frontmatter: key: value, and folded/literal blocks (> or |)."""
    out, key, block = {}, None, []
    for ln in lines + ["__end__: x"]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", ln)
        if m and not ln.startswith(" "):
            if key is not None and block is not None and out.get(key) in (">", "|", ">-", "|-"):
                out[key] = " ".join(b.strip() for b in block).strip()
            key, val = m.group(1), m.group(2).strip()
            out[key] = val.strip('"').strip("'"); block = []
        elif key is not None:
            block.append(ln)
    out.pop("__end__", None)
    return out


def check_skill(d):
    name = d.name
    sk = d / "SKILL.md"
    if not sk.exists():
        err(f"{name}: missing SKILL.md"); return
    text = sk.read_text()
    fm, body = frontmatter(text)
    if fm is None:
        err(f"{name}: SKILL.md frontmatter must start on line 1 and close with ---"); return
    meta = parse_yaml(fm)
    if meta.get("name") != name:
        err(f"{name}: frontmatter name {meta.get('name')!r} must equal the folder name")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        err(f"{name}: name must be lowercase letters, digits and single hyphens, ≤ 64 chars")
    desc = meta.get("description", "")
    if not desc:
        err(f"{name}: description is empty")
    elif len(desc) > 1024:
        err(f"{name}: description is {len(desc)} chars (max 1024)")
    elif not re.search(r"\b(Use when|Use after|Use for)\b", desc):
        warn(f"{name}: description should say when to use the skill ('Use when …')")
    if len(body) >= 500:
        err(f"{name}: SKILL.md body is {len(body)} lines (keep it under 500; move detail to references/)")
    # links stay inside the skill
    for md in d.rglob("*.md"):
        for link in re.findall(r"\]\(([^)\s#]+)(?:#[^)]*)?\)", md.read_text()):
            if re.match(r"^[a-z]+://", link) or link.startswith("mailto:"):
                continue
            target = (md.parent / link).resolve()
            if not target.exists():
                err(f"{name}: broken link {link!r} in {md.relative_to(ROOT)}")
            elif d.resolve() not in target.parents and target != d.resolve():
                err(f"{name}: link {link!r} in {md.relative_to(ROOT)} leaves the skill folder (skills must install alone)")
    # scripts mentioned exist; syntax
    for ref in set(re.findall(r"scripts/([\w.-]+\.(?:py|sh))", "\n".join(p.read_text() for p in d.rglob("*.md")))):
        if not (d / "scripts" / ref).exists():
            err(f"{name}: mentions scripts/{ref} but the skill doesn't ship it (add it to shared/manifest.txt)")
    for py in (d / "scripts").glob("*.py") if (d / "scripts").exists() else []:
        try:
            compile(py.read_text(), str(py), "exec")
        except SyntaxError as e:
            err(f"{name}: {py.name} has a syntax error at line {e.lineno}: {e.msg}")
    for sh in (d / "scripts").glob("*.sh") if (d / "scripts").exists() else []:
        r = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True)
        if r.returncode:
            err(f"{name}: {sh.name} has a shell syntax error: {r.stderr.strip()[:120]}")
    # evals
    ev = d / "evals" / "evals.json"
    if not ev.exists():
        warn(f"{name}: no evals/evals.json")
    else:
        try:
            data = json.loads(ev.read_text())
            if data.get("skill_name") != name:
                err(f"{name}: evals.json skill_name is {data.get('skill_name')!r}")
            if not data.get("evals"):
                err(f"{name}: evals.json has no evals")
            for e in data.get("evals", []):
                for k in ("prompt", "expected_output", "assertions"):
                    if not e.get(k):
                        err(f"{name}: eval {e.get('id')} is missing {k}")
        except json.JSONDecodeError as e:
            err(f"{name}: evals.json is not valid JSON ({e})")
    print(f"  {'✓' if not any(x.startswith(name + ':') for x in errors) else '✗'} {name}  ({len(body)} lines, description {len(desc)} chars)")


PRIVATE = [
    (r"/Users/[A-Za-z]", "a macOS home path"), (r"/home/[a-z][\w-]+/", "a Linux home path"),
    (r"[\w.+-]+@(?:gmail|yahoo|outlook|hotmail|icloud)\.com", "a personal e-mail address"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"\bsk-[A-Za-z0-9_-]{20,}", "an API-key-looking string"), (r"\bxi-api-key\b|\bELEVENLABS_API_KEY\s*=\s*\S{8,}", "an ElevenLabs key"),
    (r"\bghp_[A-Za-z0-9]{20,}", "a GitHub token"),
]


def privacy():
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix in (".png", ".jpg", ".mp4", ".wav", ".gif"):
            continue
        if p.name == "validate_skills.py":
            continue
        try:
            t = p.read_text()
        except UnicodeDecodeError:
            continue
        for pat, what in PRIVATE:
            for m in re.finditer(pat, t):
                line = t[:m.start()].count("\n") + 1
                err(f"privacy: {what} in {p.relative_to(ROOT)}:{line}")


def plugin():
    try:
        pj = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        mj = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        err(f"plugin: {e}"); return
    mv = (mj.get("metadata") or {}).get("version")
    if pj.get("version") != mv:
        err(f"plugin: plugin.json version {pj.get('version')} ≠ marketplace.json version {mv}")
    for pl in mj.get("plugins", []):
        for s in pl.get("skills", []):
            if not (ROOT / s / "SKILL.md").exists():
                err(f"plugin: marketplace lists {s} but it has no SKILL.md")


def main():
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    print(f"Validating {len(skills)} skills")
    for d in skills:
        check_skill(d)
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_shared.py"), "--check"], capture_output=True, text=True)
    if r.returncode:
        err("shared: " + r.stdout.strip().replace("\n", "; "))
    plugin()
    privacy()
    for w in warnings:
        print("  ⚠", w)
    for e in errors:
        print("  ✗", e)
    print(f"\n{len(skills)} skills · {len(errors)} errors · {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
