#!/usr/bin/env python3
"""Measure a music track before cutting it to picture: tempo, beat phase, downbeats, bar loudness, section changes, hits.

Method (proven on a 73 s launch film and seven licensed tracks): spectral-flux onset curve at 5.8 ms resolution → tempo from its autocorrelation
(with the 2x / 0.5x alternatives printed) → beat phase by folding the onset curve over the beat period → downbeat = the
beat-of-4 with the most low-end (kick) onsets. Produced tracks keep a fixed tempo, so the grid is one phase + k·period;
the per-section drift line tells you if that assumption fails.

Needs: ffmpeg, Python with numpy (no librosa). Usage:
  python beatgrid.py track.mp3 [--json beats.json] [--bpm 150] [--downbeat 1.914]
  --bpm forces the tempo search near a known value; --downbeat sets the bar grid from one bar start you marked by ear
  (the downbeat estimate is right on some tracks and one beat off on others).
"""
import sys, json, subprocess, numpy as np

SR, N, HOP = 22050, 1024, 128


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def spectra(y):
    win = np.hanning(N)
    n = 1 + (len(y) - N) // HOP
    idx = np.arange(N)[None, :] + HOP * np.arange(n)[:, None]
    return np.abs(np.fft.rfft(y[idx] * win, axis=1))


def flux(S, lo=0, hi=None):
    L = np.log1p(100 * S[:, lo:hi])
    d = np.diff(L, axis=0, prepend=L[:1])
    o = np.maximum(d, 0).sum(1)
    o = o - np.convolve(o, np.ones(64) / 64, "same")      # remove slow trend (local mean over ~0.37 s)
    return np.maximum(o, 0)


def fold_contrast(o, fps, period, bins=160):
    """How sharply the whole onset curve folds onto one beat period: peak / mean of the folded profile.
    A tempo that is off by even 0.1 % smears over a 2-minute track, so this pins the exact period."""
    t_end = len(o) / fps
    k = np.arange(int(t_end / period))
    ph = np.linspace(0, period, bins, endpoint=False)
    idx = np.clip(((ph[:, None] + k[None, :] * period) * fps).astype(int), 0, len(o) - 1)
    prof = o[idx].sum(1)
    prof = np.convolve(np.r_[prof[-2:], prof, prof[:2]], np.ones(3) / 3, "same")[2:-2]
    return float(prof.max() / (prof.mean() + 1e-12))


def refine_phase(y, period, coarse, search=0.08):
    """Beat phase from sample-accurate attacks: fold the rise of a 2 ms RMS envelope over the beat period, ±80 ms
    around the spectral estimate, at 1 ms resolution."""
    w = int(0.002 * SR)
    n = len(y) // w
    env = np.sqrt((y[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12)
    rise = np.maximum(np.diff(20 * np.log10(env), prepend=20 * np.log10(env[0])), 0)
    t = (np.arange(n) * w + w) / SR                  # the rise is complete at the END of the window
    k = np.arange(int(t[-1] / period))
    best, bp = -1.0, coarse
    for p in np.arange(coarse - search, coarse + search, 0.001):
        sc = np.interp(((p % period) + k * period), t, rise).sum()
        if sc > best:
            best, bp = sc, p % period
    return float(bp)


def tempo(o, fps, bpm_hint=None):
    oc = o - o.mean()
    ac = np.correlate(oc, oc, "full")[len(oc) - 1:]
    ac /= ac[0] + 1e-12
    bpms = np.arange(60.0, 200.0, 0.05)
    lags = 60.0 * fps / bpms
    val = np.interp(lags, np.arange(len(ac)), ac)
    # comb: a true period also correlates at 2x and 3x the lag
    val = val + 0.5 * np.interp(2 * lags, np.arange(len(ac)), ac) + 0.33 * np.interp(3 * lags, np.arange(len(ac)), ac)
    if bpm_hint:
        m = np.abs(np.log2(bpms / bpm_hint)) < 0.06
        val = np.where(m, val, -1)
    # candidates: the strongest local maxima of the autocorrelation comb, then each refined on the full-track fold
    peaks = [i for i in range(1, len(val) - 1) if val[i] >= val[i - 1] and val[i] >= val[i + 1] and val[i] > 0]
    peaks = sorted(peaks, key=lambda i: -val[i])[:8]
    cands = []
    for i in peaks:
        b0 = float(bpms[i])
        fine = np.arange(b0 * 0.994, b0 * 1.006, 0.005)
        sc = [fold_contrast(o, fps, 60.0 / b) for b in fine]
        j = int(np.argmax(sc))
        cands.append((round(float(fine[j]), 3), float(sc[j]), float(val[i])))
    # prefer the sharpest fold; between octave-related tempos with similar sharpness, prefer the one nearer 120 BPM
    def rank(c):
        return c[1] * np.exp(-0.5 * (np.log2(c[0] / 120.0) / 1.2) ** 2)
    cands.sort(key=rank, reverse=True)
    best = cands[0]
    alts = {c[0]: round(c[1], 2) for c in cands[1:5]}
    return best[0], best[1], alts


def fold_phase(o, fps, period):
    """Phase (s) of the beat grid: the offset whose comb of beats collects the most onset energy."""
    t = np.arange(len(o)) / fps
    steps = 400
    ph = np.linspace(0, period, steps, endpoint=False)
    k = np.arange(int(t[-1] / period) + 1)
    sc = np.array([np.interp(p + k * period, t, o).sum() for p in ph])
    sc = np.convolve(np.r_[sc[-3:], sc, sc[:3]], np.ones(5) / 5, "same")[3:-3]    # circular smooth
    return float(ph[np.argmax(sc)]), sc


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        print(__doc__); sys.exit(1)
    path = a[0]
    if not __import__('os').path.isfile(path):
        sys.exit(f"{path}: file not found")
    out = a[a.index("--json") + 1] if "--json" in a else None
    hint = float(a[a.index("--bpm") + 1]) if "--bpm" in a else None

    y = load(path); dur = len(y) / SR
    if len(y) == 0 or np.abs(y).max() < 10 ** (-60 / 20):
        print(f"{path.split('/')[-1]}: no audible audio (silent or missing track); nothing to measure"); return
    S = spectra(y); fps = SR / HOP
    o = flux(S)
    lowbin = int(150 / (SR / N)) + 1
    o_low = flux(S, 1, lowbin)

    bpm, conf, alts = tempo(o, fps, hint)
    period = 60.0 / bpm
    phase_spec, _ = fold_phase(o, fps, period)
    phase = refine_phase(y, period, phase_spec)     # spectral frames smear onsets ~40 ms early; re-measure in time domain
    beats = np.arange(phase, dur, period)

    # downbeat: the beat-of-4 whose beats carry the most low-end onsets (kick on 1). The low-end flux lives on the
    # spectral (early) grid, so read it there, then map each spectral beat to the nearest refined beat.
    t = np.arange(len(o_low)) / fps
    beats_spec = np.arange(phase_spec, dur, period)
    low_at = np.interp(beats_spec, t, np.convolve(o_low, np.ones(5), "same"))
    k4 = [float(low_at[i::4].mean()) for i in range(4)]
    d_spec = int(np.argmax(k4))
    first = beats_spec[d_spec]
    d0 = int(np.argmin(np.abs(beats[:8] - first))) % 4
    known = float(a[a.index("--downbeat") + 1]) if "--downbeat" in a else None
    if known is not None:                            # a bar start marked by ear wins over the estimate
        d0 = int(round((known - phase) / period)) % 4
    downbeats = beats[d0::4]

    # drift check: phase measured per ~16-bar window should agree with the global phase
    drift = []
    win = 64 * period
    for s in np.arange(0, max(dur - win / 2, 1), win):
        m = (t >= s) & (t < s + win)
        if m.sum() > fps * 4:
            p, _ = fold_phase(o[m], fps, period)
            dp = ((p + s - phase_spec + period / 2) % period) - period / 2      # same method on both sides
            drift.append((round(float(s), 1), round(dp * 1000)))

    # loudness and colour per bar, and the biggest bar-to-bar changes (cut candidates)
    rms_t = np.arange(S.shape[0]) * HOP / SR
    frame_rms = np.sqrt((S ** 2).sum(1) / N ** 2 * 2 + 1e-12)
    freqs = np.fft.rfftfreq(N, 1 / SR)
    cent = (S * freqs).sum(1) / (S.sum(1) + 1e-9)
    bars = []
    for i, b0 in enumerate(downbeats):
        b1 = b0 + 4 * period
        m = (rms_t >= b0) & (rms_t < b1)
        if m.sum() == 0: continue
        bars.append(dict(bar=i + 1, t=round(float(b0), 3), db=round(float(20 * np.log10(frame_rms[m].mean())), 1),
                         centroid=round(float(cent[m].mean()))))
    ch = []
    for i in range(1, len(bars)):
        dd = abs(bars[i]["db"] - bars[i - 1]["db"]) + 6 * abs(np.log2((bars[i]["centroid"] + 1) / (bars[i - 1]["centroid"] + 1)))
        ch.append((dd, bars[i]["t"]))
    sections = sorted(t for _, t in sorted(ch, reverse=True)[:8])

    # hits: strong isolated onsets (sound-effect / accent candidates)
    thr = o.mean() + 3 * o.std()
    w = int(0.05 * fps)
    hits = [round(i / fps, 3) for i in range(w, len(o) - w) if o[i] > thr and o[i] == o[i - w:i + w + 1].max()]

    # where the music actually ends (last moment within 40 dB of the loudest bar)
    env = 20 * np.log10(frame_rms + 1e-12)
    end_t = float(rms_t[np.nonzero(env > env.max() - 40)[0][-1]])

    name = path.split("/")[-1]
    print(f"{name}: {dur:.2f} s · {bpm:.2f} BPM (fold sharpness {conf:.2f}) · beat {period*1000:.1f} ms · bar {4*period:.3f} s")
    print(f"  other candidates (fold sharpness): " + ", ".join(f"{b} ({v})" for b, v in alts.items())
          + "   [half/double tempo folds almost as sharply: pick by ear, then pass --bpm]")
    print(f"  beat phase {phase:.3f} s → beats at {phase:.3f} + k·{period:.4f}")
    src = f"from --downbeat {known:g}" if known is not None else "ESTIMATE (most low-end onsets); confirm by ear, then pass --downbeat <a bar start>"
    print(f"  downbeats: beat k ≡ {d0} (mod 4) → first {downbeats[0]:.3f} s   {src}   [low-end per beat-of-4: " + " ".join(f"{v:.2f}" for v in k4) + "]")
    print(f"  drift per 16 bars (ms vs global phase): " + " ".join(f"{s}s:{d:+d}" for s, d in drift) + "   [|drift| < 15 ms = fixed grid holds]")
    print(f"  music audible until {end_t:.2f} s")
    print(f"  biggest bar-to-bar changes (section cut candidates): " + ", ".join(f"{s:.2f}" for s in sections))
    lo = max(min(b["db"] for b in bars), max(b["db"] for b in bars) - 40) if bars else 0   # bars span at most 40 dB
    print("  bar loudness (dB, bar start):")
    for b in bars:
        print(f"    bar {b['bar']:3d}  {b['t']:7.3f}s  {b['db']:6.1f} dB  {'█' * min(41, int(max(0, b['db'] - lo + 1)))}  centroid {b['centroid']} Hz")
    if out:
        json.dump(dict(file=name, duration=round(dur, 3), bpm=round(bpm, 3), period=round(period, 5), phase=round(phase, 4),
                       beats=[round(float(b), 3) for b in beats], downbeats=[round(float(b), 3) for b in downbeats],
                       downbeat_index=d0, bars=bars, sections=sections, hits=hits, end=round(end_t, 3), drift_ms=drift),
                  open(out, "w"), indent=1)
        print("wrote", out)


if __name__ == "__main__":
    main()
