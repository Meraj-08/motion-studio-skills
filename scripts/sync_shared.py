#!/usr/bin/env python3
"""Copy the shared scripts into every skill that ships them (shared/manifest.txt), so each skill folder works on its
own when installed alone. Edit scripts only in shared/scripts, then run:  python3 scripts/sync_shared.py
With --check it changes nothing and exits 1 if any skill's copy is missing or out of date (used by CI)."""
import sys, shutil, filecmp, pathlib, os, stat

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared" / "scripts"


def manifest():
    for line in (ROOT / "shared" / "manifest.txt").read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            skill, files = line.split(":", 1)
            yield skill.strip(), files.split()


def main():
    check = "--check" in sys.argv
    bad = 0
    for skill, files in manifest():
        dst = ROOT / "skills" / skill / "scripts"
        if not check:
            dst.mkdir(parents=True, exist_ok=True)
        wanted = set(files)
        for f in files:
            src, out = SHARED / f, dst / f
            if not src.exists():
                print(f"✗ {skill}: {f} is not in shared/scripts"); bad += 1; continue
            if out.exists() and filecmp.cmp(src, out, shallow=False):
                continue
            if check:
                print(f"✗ {skill}/scripts/{f} is missing or stale (run scripts/sync_shared.py)"); bad += 1
            else:
                shutil.copy2(src, out); os.chmod(out, os.stat(out).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                print(f"→ {skill}/scripts/{f}")
        if dst.exists():
            for extra in dst.iterdir():
                if extra.name not in wanted and extra.name in {p.name for p in SHARED.iterdir()}:
                    if check:
                        print(f"✗ {skill}/scripts/{extra.name} is not in the manifest"); bad += 1
                    else:
                        extra.unlink(); print(f"× removed {skill}/scripts/{extra.name}")
    if check:
        print("shared scripts in sync" if not bad else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
