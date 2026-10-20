#!/usr/bin/env python3
"""Check a soundtrack the way the reviewer hears it. Four modes:

  python audio-check.py mix.wav                       # LUFS, true peak, loudness every 0.5 s, dynamics spread
  python audio-check.py new.wav --vs old.wav [--sections 0-7,7-13,13-21,...]
                                                      # per-section dB change: report "44 s is 3.5 dB quieter"
  python audio-check.py sfx_stem.wav --events 12.9:send,42.833:merged[,t:label[:pre]]
                                                      # audible attack of each effect vs its picture frame (Δ ms),
                                                      # and how much of it is in 400 Hz–4 kHz (what laptops/phones play)
  python audio-check.py music_stem.wav --duck 10.1-12.9,45.6-48.3   # level inside each span vs the 2 s around it

Any audio or video file works (audio is read through ffmpeg). Needs ffmpeg, Python with numpy.
Targets that held up on real launch films: social master −14 LUFS integrated, ≤ −1 dBTP; body spread p90–p10 ≥ 8 dB (not monotonic);
every effect attack within ±20 ms of its frame; ≥ 50 % of an effect's energy in 400 Hz–4 kHz; duck under typing 6–10 dB.
"""
import sys, re, subprocess, numpy as np

SR = 48000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def ebur128(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = err[err.rfind("Summary:"):]
    g = lambda k: (re.search(k + r":\s+(-?[\d.]+)", summ) or [None, "nan"])[1]
    return float(g("I")), float(g("LRA")), float(g("Peak"))


def kweight_db(x, win=0.4, hop=0.1):
    """Momentary-style loudness (dB, relative) per hop: simple high-pass + RMS (close enough for comparisons)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= np.clip((f - 40) / 60, 0, 1)                     # drop sub-bass the listener can't hear on small speakers
    X *= 1 + 0.6 * (f > 1500)                             # gentle presence lift, like K-weighting's shelf
    y = np.fft.irfft(X, len(x))
    w, h = int(win * SR), int(hop * SR)
    n = max(1, 1 + (len(y) - w) // h)
    e = np.array([np.mean(y[i * h:i * h + w] ** 2) for i in range(n)])
    return np.arange(n) * hop + win / 2, 10 * np.log10(e + 1e-12)


def parse_spans(s):
    return [tuple(float(v) for v in p.split("-")) for p in s.split(",")]


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        print(__doc__); sys.exit(1)
    path = a[0]
    x = load(path)
    dur = len(x) / SR
    if len(x) == 0 or np.abs(x).max() < 10 ** (-60 / 20):
        print(f"{path.split('/')[-1]}: no audible audio (silent or missing track)"); return

    if "--events" in a:
        evs = a[a.index("--events") + 1].split(",")
        W = int(0.005 * SR)
        print(f"{path.split('/')[-1]}: effect attacks vs picture frames")
        for e in evs:
            parts = e.split(":")
            T, label = float(parts[0]), parts[1] if len(parts) > 1 else ""
            pre = float(parts[2]) if len(parts) > 2 else 0.15
            i0, i1 = int((T - pre) * SR), int((T + 0.25) * SR)
            seg = x[max(0, i0):i1]
            env = np.maximum(np.sqrt(np.array([np.mean(seg[k:k + W] ** 2) for k in range(0, len(seg) - W, W)])), 10 ** (-80 / 20))
            rise = 20 * np.log10(env[1:] / env[:-1])
            # the strongest rise NEAREST the frame (rises within 6 dB of the strongest), so fast typing doesn't match a neighbour
            strong = np.nonzero(rise >= max(rise.max() - 3, 0.75 * rise.max(), 3))[0]
            if len(strong) == 0: strong = np.array([int(np.argmax(rise))])
            times = (max(0, i0) + (strong + 1) * W) / SR
            k = int(strong[np.argmin(np.abs(times - T))]); ta = (max(0, i0) + (k + 1) * W) / SR
            # peak: the loudest local maximum nearest the frame (within 3 dB of the loudest), same reason as above
            envdb = 20 * np.log10(env)
            locs = [j for j in range(1, len(env) - 1) if env[j] >= env[j - 1] and env[j] >= env[j + 1] and envdb[j] >= envdb.max() - 3] or [int(np.argmax(env))]
            ptimes = np.array([(max(0, i0) + j * W + W / 2) / SR for j in locs])
            tp = float(ptimes[np.argmin(np.abs(ptimes - T))])
            body = x[max(0, int((tp - 0.15) * SR)):int((tp + 0.15) * SR)]          # audibility measured around the peak
            B = np.abs(np.fft.rfft(body)) ** 2; f = np.fft.rfftfreq(len(body), 1 / SR)
            share = B[(f >= 400) & (f <= 4000)].sum() / (B[f >= 20].sum() + 1e-12)
            pk = 20 * np.log10(np.abs(body).max() + 1e-12)
            flag = "" if min(abs(ta - T), abs(tp - T)) <= 0.02 else "  ← neither attack nor peak within 20 ms"
            flag += "" if share >= 0.5 else "  ← mostly outside 400 Hz–4 kHz (check it on a laptop/phone speaker)"
            print(f"  {label:14s} frame {T:7.3f} · attack {ta:7.3f} (Δ {1000 * (ta - T):+4.0f} ms, +{rise[k]:.0f} dB) · "
                  f"peak {tp:7.3f} (Δ {1000 * (tp - T):+4.0f} ms, {pk:5.1f} dBFS) · 400–4k {100 * share:3.0f} %{flag}")
        print("  Align clicks/taps by attack, whooshes/swells by peak, risers by their end (see references/sound-and-mix.md).")
        return

    if "--duck" in a:
        t, L = kweight_db(x)
        print(f"{path.split('/')[-1]}: level inside each span vs the 2 s before and after")
        for s0, s1 in parse_spans(a[a.index("--duck") + 1]):
            inside = L[(t >= s0) & (t < s1)].mean()
            around = np.r_[L[(t >= s0 - 2) & (t < s0)], L[(t >= s1) & (t < s1 + 2)]].mean()
            print(f"  {s0:6.2f}–{s1:6.2f}  inside {inside:6.1f} dB  around {around:6.1f} dB  duck {around - inside:+5.1f} dB")
        return

    if "--vs" in a:
        other = a[a.index("--vs") + 1]
        y = load(other)
        tA, LA = kweight_db(x); tB, LB = kweight_db(y)
        spans = parse_spans(a[a.index("--sections") + 1]) if "--sections" in a else \
            [(s, min(s + 5, dur)) for s in np.arange(0, dur, 5.0)]
        print(f"{path.split('/')[-1]} vs {other.split('/')[-1]}  (positive = new is louder)")
        for s0, s1 in spans:
            mA = LA[(tA >= s0) & (tA < s1)]; mB = LB[(tB >= s0) & (tB < s1)]
            if len(mA) and len(mB):
                d = 10 * np.log10(np.mean(10 ** (mA / 10))) - 10 * np.log10(np.mean(10 ** (mB / 10)))
                print(f"  {s0:6.2f}–{s1:6.2f}  {d:+5.1f} dB  {'▲' if d > 0.5 else '▼' if d < -0.5 else '='}")
        I1, _, P1 = ebur128(path); I2, _, P2 = ebur128(other)
        print(f"  integrated {I1:.1f} vs {I2:.1f} LUFS · true peak {P1:.1f} vs {P2:.1f} dBTP")
        return

    I, LRA, TP = ebur128(path)
    t, L = kweight_db(x, 3.0, 0.5)                            # short-term (3 s) every 0.5 s
    body = L[(t > 3) & (t < dur - 3)] if dur > 9 else L        # short clips: use all of it
    rel = L - np.percentile(body, 95)
    spread = np.percentile(body, 90) - np.percentile(body, 10)
    print(f"{path.split('/')[-1]}: {dur:.2f} s · integrated {I:.1f} LUFS · LRA {LRA:.1f} LU · true peak {TP:.1f} dBTP")
    print(f"  body dynamics p90–p10: {spread:.1f} dB  {'(has ups and downs)' if spread >= 8 else '(under 8 dB: listen for a flat, monotonic body)'}")
    print("  short-term loudness every second (dB below the loud sections):")
    for s in range(int(dur)):
        v = rel[(t >= s) & (t < s + 1)]
        if len(v):
            m = float(v.mean())
            print(f"    {s:4d}s  {m:6.1f}  {'█' * max(0, int(30 + m))}")
    tail = x[-int(min(dur, 4) * SR):]
    sil = np.nonzero(np.abs(x) > 10 ** (-60 / 20))[0]
    if len(sil):
        print(f"  last sound above −60 dBFS at {sil[-1] / SR:.2f} s → {dur - sil[-1] / SR:.2f} s of silence at the end")


if __name__ == "__main__":
    main()
