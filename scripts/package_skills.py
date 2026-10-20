#!/usr/bin/env python3
"""Build one upload-ready zip per skill for claude.ai / Claude Desktop (Customize → Skills → Upload a skill).
Each archive contains a single top-level folder named after the skill (SKILL.md, references/, scripts/), without
evals. Output: dist/<skill>.zip and dist/SHA256SUMS.  Run: python3 scripts/package_skills.py"""
import hashlib, pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def main():
    DIST.mkdir(exist_ok=True)
    sums = []
    for d in sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists()):
        out = DIST / f"{d.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                rel = f.relative_to(d)
                if f.is_dir() or rel.parts[0] == "evals" or f.name in (".DS_Store",) or "__pycache__" in rel.parts:
                    continue
                info = zipfile.ZipInfo(f"{d.name}/{rel.as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = (0o755 if f.suffix in (".py", ".sh") else 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
        h = hashlib.sha256(out.read_bytes()).hexdigest()
        sums.append(f"{h}  {out.name}")
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")
    (DIST / "SHA256SUMS").write_text("\n".join(sums) + "\n")


if __name__ == "__main__":
    main()
