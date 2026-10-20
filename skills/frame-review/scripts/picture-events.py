#!/usr/bin/env python3
"""Measure picture events on the RENDERED video (never trust a brief's timecodes): cuts, change spans, the exact frame a
UI element changes, and where two versions agree (invisible splice points).

Needs: ffmpeg, Python with numpy. Usage:
  python picture-events.py film.mp4                         # cuts + busiest/stillest spans, whole film
  python picture-events.py film.mp4 --from 40 --to 46       # limit the window
  python picture-events.py film.mp4 --region 1500,80,300,60 # watch one UI area (x,y,w,h in video pixels):
                                                            #   prints every frame where it changes (badge flips, labels)
  python picture-events.py a.mp4 --compare b.mp4 --from 15 --to 25   # per-frame difference between two versions:
                                                            #   lowest-difference frames = where to splice with a straight cut
Times are frame START times (frame n at n/fps). Differences are mean absolute luma difference on a 0–255 scale.
"""
import sys, json, subprocess, numpy as np


def arg(a, k, d=None, f=str):
    return f(a[a.index(k) + 1]) if k in a else d


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", path], capture_output=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return s["width"], s["height"], float(n) / float(d)


def frames(path, t0, t1, crop=None, w=240, h=135):
    vf = []
    if crop:
        x, y, cw, ch = crop
        vf.append(f"crop={cw}:{ch}:{x}:{y}")
        w, h = min(cw, 480), max(1, round(min(cw, 480) * ch / cw))
    vf += [f"scale={w}:{h}:flags=area", "format=gray"]
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-i", path]
    if t1 is not None:
        cmd += ["-t", str(t1 - t0)]
    cmd += ["-vf", ",".join(vf), "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        print(__doc__); sys.exit(1)
    path = a[0]
    if not __import__('os').path.isfile(path):
        sys.exit(f"{path}: file not found")
    W, H, fps = probe(path)
    t0 = arg(a, "--from", 0.0, float); t1 = arg(a, "--to", None, float)
    region = arg(a, "--region")
    other = arg(a, "--compare")
    if other and not __import__('os').path.isfile(other):
        sys.exit(f"{other}: file not found")

    if other:
        A = frames(path, t0, t1); B = frames(other, t0, t1)
        n = min(len(A), len(B))
        d = np.abs(A[:n] - B[:n]).mean((1, 2))
        order = np.argsort(d)[:10]
        print(f"{path.split('/')[-1]} vs {other.split('/')[-1]} · {t0:.3f}–{(t0 + n / fps):.3f} s · {fps:g} fps")
        print(f"  difference: median {np.median(d):.2f}, max {d.max():.2f} at {t0 + np.argmax(d) / fps:.3f} s")
        print("  best splice frames (time · difference; < 1.0 is encoding noise = invisible straight cut):")
        for i in sorted(order):
            print(f"    {t0 + i / fps:8.3f} s   {d[i]:.2f}")
        return

    crop = tuple(int(v) for v in region.split(",")) if region else None
    F = frames(path, t0, t1, crop)
    d = np.r_[0, np.abs(np.diff(F, axis=0)).mean((1, 2))]
    t = t0 + np.arange(len(d)) / fps
    print(f"{path.split('/')[-1]}: {W}x{H} @ {fps:g} fps · window {t0:.3f}–{t[-1]:.3f} s" + (f" · region {region}" if region else ""))

    if crop:
        thr = max(1.0, 4 * np.median(d))
        ev = [i for i in range(1, len(d)) if d[i] > thr]
        print(f"  frames where the region changes (diff > {thr:.1f}):")
        last = -10
        for i in ev:
            mark = "  ← starts" if i - last > 2 else ""
            print(f"    {t[i]:8.3f} s  frame {round(t[i] * fps):5d}  diff {d[i]:6.1f}{mark}")
            last = i
        if not ev:
            print("    none")
        return

    # cuts: a frame much more different than its neighbourhood
    med = np.array([np.percentile(d[max(0, i - 15):i + 16], 75) for i in range(len(d))])   # 75th pct: robust to footage animated on twos
    cuts = [i for i in range(1, len(d) - 1) if d[i] > 4 and d[i] > 8 * (med[i] + 0.3) and d[i] >= d[i - 1] and d[i] >= d[i + 1]]
    print(f"  hard cuts / sudden jumps ({len(cuts)}; dissolves and camera moves show in the motion profile instead):")
    for i in cuts:
        print(f"    {t[i]:8.3f} s  frame {round(t[i] * fps):5d}  diff {d[i]:5.1f}")
    if len(cuts) > 1:
        shots = np.diff([t[0]] + [t[i] for i in cuts] + [t[-1]])
        print(f"  time between jumps (= shot length when they are cuts): median {np.median(shots):.2f} s, shortest {shots.min():.2f} s, longest {shots.max():.2f} s")
    # motion profile per second: where the eye is busy vs where the picture rests
    sec = {}
    for ti, di in zip(t, d):
        sec.setdefault(int(ti), []).append(di)
    print("  motion per second (mean frame diff):")
    for s in sorted(sec):
        v = float(np.mean(sec[s]))
        print(f"    {s:4d}s  {v:5.2f}  {'█' * min(60, int(v * 4))}")
    still = [s for s in sorted(sec) if np.mean(sec[s]) < 0.05]
    if still:
        print("  seconds with almost no change (dead air unless it's a deliberate hold): " + ", ".join(map(str, still)))


if __name__ == "__main__":
    main()
