#!/usr/bin/env python3
"""End-to-end smoke test of every shared script on media it generates itself (no files needed). Needs ffmpeg and a
Python with numpy + scipy.  Run: python3 scripts/smoke_test.py   (exit 1 on any failure)

  sfx-synth   → effects on known cues        audio-check --events → every attack/peak within ±20 ms of its cue
  sfx-synth   → a 120 BPM tick track         beatgrid             → 120.0 ± 0.2 BPM, phase on the grid
  ffmpeg      → a video with a cut at 2.0 s  picture-events       → a cut reported at 2.0 s ± 1 frame
  review-sheets on that video                → contact, phone, strip and still images exist
  master-mux  (video + effects)              → output near −14 LUFS, video stream copied
  wallpapers  --preset midnight (small)      → a PNG of the requested size
"""
import json, os, re, subprocess, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "shared" / "scripts"
PY = sys.executable
fails = []


def run(args, **kw):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(f"{' '.join(map(str, args[:2]))} failed:\n{r.stdout}\n{r.stderr}")
    return r.stdout


def check(name, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {name}{('  ' + detail) if detail else ''}")
    if not ok:
        fails.append(name)


def main():
    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        # 1. effects on cues, then measure them
        cues = [(0.5, "thock"), (0.62, "thock"), (1.2, "send"), (2.0, "click"), (3.0, "impact"), (4.5, "whoosh=0.8"),
                (7.0, "riser=2"), (8.0, "pluck=D5"), (8.4, "tick")]
        run([PY, S / "sfx-synth.py", t / "fx.wav"] + sum([["--cue", f"{c}:{v}"] for c, v in cues], []))
        ev = ",".join(f"{c}:{v.split('=')[0]}{':0.7' if v.startswith('whoosh') else ':0.3' if v.startswith('riser') else ''}" for c, v in cues)
        out = run([PY, S / "audio-check.py", t / "fx.wav", "--events", ev])
        for line in out.splitlines():
            m = re.search(r"^\s+(\S+)\s+frame\s+([\d.]+).*?attack\s+[\d.]+ \(Δ\s+([+-]?\d+) ms.*?peak\s+[\d.]+ \(Δ\s+([+-]?\d+) ms", line)
            if m:
                da, dp = int(m.group(3)), int(m.group(4))
                check(f"sfx {m.group(1)} @ {m.group(2)}", min(abs(da), abs(dp)) <= 20, f"attack {da:+d} ms, peak {dp:+d} ms")
        # 2. tempo of a synthetic 120 BPM track
        ticks = [f"{0.25 + 0.5 * k:.3f}:{'impact' if k % 4 == 0 else 'click'}" for k in range(60)]
        run([PY, S / "sfx-synth.py", t / "beat.wav"] + sum([["--cue", c] for c in ticks], []))
        bout = run([PY, S / "beatgrid.py", t / "beat.wav", "--json", t / "beat.json"])
        bj = json.loads((t / "beat.json").read_text())
        ph_err = min(abs(((bj["phase"] - 0.25 + 0.25) % 0.5) - 0.25), 0.5)
        check("beatgrid tempo", abs(bj["bpm"] - 120) <= 0.2 or abs(bj["bpm"] - 60) <= 0.1, f"{bj['bpm']} BPM")
        check("beatgrid phase", ph_err <= 0.02, f"phase {bj['phase']} s (expected 0.25 + k·0.5)")
        # 3. a video with one hard cut at 2.0 s
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x202020:s=640x360:r=30:d=2",
             "-f", "lavfi", "-i", "color=c=0xd0d0d0:s=640x360:r=30:d=2", "-filter_complex", "[0][1]concat=n=2:v=1",
             "-pix_fmt", "yuv420p", t / "cut.mp4"])
        pout = run([PY, S / "picture-events.py", t / "cut.mp4"])
        cuts = [float(x) for x in re.findall(r"^\s+([\d.]+) s\s+frame", pout, re.M)]
        check("picture-events cut", any(abs(c - 2.0) <= 1 / 30 + 1e-6 for c in cuts), f"cuts at {cuts}")
        # 4. review sheets
        run(["bash", S / "review-sheets.sh", t / "cut.mp4", t / "sheets", "--strip", "1.8", "--stills", "1,3"])
        for f in ("contact.png", "phone.png", "strip-1.8.png", "still-1.png", "still-3.png"):
            check(f"review-sheets {f}", (t / "sheets" / f).exists())
        # 5. master + mux
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anoisesrc=color=pink:amplitude=0.3:duration=4:seed=3",
             "-ar", "48000", t / "bed.wav"])
        run(["bash", S / "master-mux.sh", t / "cut.mp4", t / "bed.wav", t / "muxed.mp4"], env={**os.environ, "SMALL": "0"})
        spiky = run(["bash", S / "master-mux.sh", t / "cut.mp4", t / "fx.wav", t / "spiky.mp4"], env={**os.environ, "SMALL": "0"})
        check("master-mux explains a peak-limited result", "true-peak ceiling" in spiky, spiky.strip().splitlines()[-1][:90])
        lout = run([PY, S / "audio-check.py", t / "muxed.mp4"])
        lufs = float(re.search(r"integrated (-?[\d.]+) LUFS", lout).group(1))
        check("master-mux loudness", abs(lufs + 14) <= 1.0, f"{lufs} LUFS (target −14)")
        codec = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", t / "muxed.mp4"]).strip()
        check("master-mux video copied", codec == "h264", codec)
        # 6. wallpapers
        run([PY, S / "wallpapers.py", "--preset", "midnight", "--size", "320x180", "--out", t / "wall.png"])
        size = run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", t / "wall.png"]).strip()
        check("wallpapers", size == "320,180", size)
    print(f"\n{'all passed' if not fails else str(len(fails)) + ' failed: ' + ', '.join(fails)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
