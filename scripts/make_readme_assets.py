#!/usr/bin/env python3
"""Regenerate the README images in assets/ with this repo's own tools (no third-party footage or art).

  assets/banner.png       title banner on a generated ribbons background
  assets/backgrounds.jpg  every wallpapers.py preset, labelled
  assets/sfx-timing.png   a sfx-synth.py track: waveform, cue lines and where each sound is aligned

Needs ffmpeg, Python with numpy + scipy. Uses macOS fonts when present (Avenir Next / Helvetica Neue / Menlo),
otherwise ffmpeg's default font.   Run: python3 scripts/make_readme_assets.py
"""
import os, pathlib, subprocess, sys, tempfile, numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "shared" / "scripts"
OUT = ROOT / "assets"
PY = sys.executable


def font(*cands):
    for c in cands:
        if os.path.exists(c):
            return c
    return None


BOLD = font("/System/Library/Fonts/Avenir Next.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
REG = font("/System/Library/Fonts/HelveticaNeue.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
MONO = font("/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def dt(text, x, y, size, color="white", f=None, extra=""):
    ff = f"fontfile='{f}':" if f else ""
    return f"drawtext={ff}text='{esc(text)}':x={x}:y={y}:fontsize={size}:fontcolor={color}{extra}"


def run(args, **kw):
    subprocess.run([str(a) for a in args], check=True, **kw)


def banner(tmp):
    bg = tmp / "bg.png"
    run([PY, S / "wallpapers.py", "--preset", "ribbons-blue", "--size", "1280x400", "--out", bg], stdout=subprocess.DEVNULL)
    vf = ",".join([
        "drawbox=x=0:y=0:w=1280:h=400:color=black@0.35:t=fill",
        dt("Motion Studio Skills", 64, 92, 74, "white", BOLD),
        dt("Agent skills for launch films, product videos and motion graphics", 68, 196, 30, "0xdce6f5", REG),
        dt("music cut to the picture  ·  every sound on its frame  ·  agents that watch their own frames", 68, 252, 22, "0xa9bbd6", REG),
        dt("8 skills  ·  7 tested tools  ·  Claude Code, Codex, Cursor, Copilot, Gemini", 68, 318, 22, "0x8fd3ff", MONO),
    ])
    run(["ffmpeg", "-v", "error", "-y", "-i", bg, "-vf", vf, "-frames:v", "1", OUT / "banner.png"])


def backgrounds(tmp):
    names = ["midnight", "sunrise", "emerald", "graphite", "pastel", "ribbons-blue", "ribbons-dusk", "ridges-dusk"]
    tiles = []
    for n in names:
        raw = tmp / f"{n}.png"; lab = tmp / f"{n}-l.png"
        run([PY, S / "wallpapers.py", "--preset", n, "--size", "480x270", "--out", raw], stdout=subprocess.DEVNULL)
        run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-vf",
             "drawbox=x=0:y=226:w=480:h=44:color=black@0.45:t=fill," + dt(n, 16, 236, 22, "white", MONO), lab])
        tiles.append(lab)
    inputs = sum([["-i", t] for t in tiles], [])
    fc = "".join(f"[{i}]" for i in range(4)) + "hstack=4[a];" + "".join(f"[{i}]" for i in range(4, 8)) + "hstack=4[b];[a][b]vstack"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-q:v", "3", OUT / "backgrounds.jpg"])


def sfx_timing(tmp):
    cues = [(1.0, "click", "click · attack on the frame"), (2.1, "thock", "keys · varied, attack on the frame"),
            (2.28, "thock", None), (2.43, "thock", None), (3.6, "whoosh=0.8", "whoosh · peak on the cue"),
            (4.7, "impact", "impact · mid layer, heard on phones"), (6.9, "riser=1.6", "riser · ends on the hit"),
            (7.4, "pluck=D5", "pluck · in key")]
    wav = tmp / "fx.wav"
    run([PY, S / "sfx-synth.py", wav] + sum([["--cue", f"{t}:{c}"] for t, c, _ in cues], []) + ["--duration", "8.4"],
        stdout=subprocess.DEVNULL)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    W, H, top, mid, amp = 1600, 520, 110, 300, 150
    img = np.zeros((H, W, 3), np.uint8); img[:] = (16, 19, 24)
    dur = len(x) / 48000
    cols = np.array_split(np.abs(x), W)
    for i, c in enumerate(cols):
        a = float(np.sqrt(np.mean(c ** 2)) * 2.2 if len(c) else 0); pk = float(c.max() if len(c) else 0)
        h1, h2 = int(min(pk, 1) * amp), int(min(a, 1) * amp)
        img[mid - h1:mid + h1 + 1, i] = (52, 92, 160)
        img[mid - h2:mid + h2 + 1, i] = (138, 196, 255)
    for t, _, lab in cues:
        xx = int(t / dur * W)
        for y in range(top - 20, H - 70, 8):
            img[y:y + 4, xx] = (255, 178, 92)
    pr = tmp / "wave.png"
    run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", "-frames:v", "1", pr],
        input=img.tobytes())
    labels, row = [], 0
    for t, _, lab in cues:
        if not lab:
            continue
        xx = int(t / dur * W) + 8; yy = 30 + (row % 2) * 34; row += 1
        labels.append(dt(lab, xx, yy, 21, "0xffd2a0", REG))
        labels.append(dt(f"{t:.2f} s", int(t / dur * W) + 6, H - 60, 18, "0x9aa7b8", MONO))
    labels.append(dt("sfx-synth.py places each sound by the point the ear hears; audio-check.py --events verifies it", 24, H - 30, 20, "0x9aa7b8", REG))
    run(["ffmpeg", "-v", "error", "-y", "-i", pr, "-vf", ",".join(labels), "-frames:v", "1", OUT / "sfx-timing.png"])


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        t = pathlib.Path(td)
        banner(t); backgrounds(t); sfx_timing(t)
    for f in ("banner.png", "backgrounds.jpg", "sfx-timing.png"):
        print(f"assets/{f}  {(OUT / f).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
