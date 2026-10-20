#!/usr/bin/env python3
"""Synthesize UI and motion sound effects on exact times, so every sound lands where the ear hears it.

Each cue is placed by its AUDIBLE point, matching the sync rules in the skills:
  click, thock, tap, tick, impact   → the attack starts on the cue time
  pop, send, pluck                  → the onset is on the cue time
  whoosh                            → the PEAK is on the cue time (it starts earlier)
  riser                             → it ENDS on the cue time (it starts `len` seconds earlier)
Every repeat is slightly different (seeded pitch and level variation), so typing never sounds like one sample looped.
Impacts carry a mid-range click so they are heard on laptop and phone speakers, not just on headphones.

Usage:
  sfx-synth.py out.wav --cue 0.50:thock --cue 0.62:thock --cue 1.20:send --cue 3.00:impact
  sfx-synth.py out.wav --cue 2.0:whoosh=0.8 --cue 6.0:riser=3 --cue 4.1:pluck=D5 --cue 5.0:click:-6
  sfx-synth.py out.wav --cues cues.json        # [{"t": 1.0, "type": "pluck", "param": "G5", "db": -3}, ...]
  sfx-synth.py --gallery out_dir               # one file per voice, to audition
Options: --seed N (variation), --duration S (default: last cue + 2 s), --sr 48000.
Needs: Python with numpy. Writes 16-bit stereo WAV.
"""
import sys, json, wave, numpy as np

SR = 48000
NOTES = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def note_hz(name):
    name = name.strip()
    pitch, octave = (name[:-1], int(name[-1])) if name[-1].isdigit() else (name, 5)
    return 440.0 * 2 ** ((NOTES[pitch] + 12 * (octave + 1) - 69) / 12)


def env_exp(n, rate):
    return np.exp(-rate * np.arange(n) / SR)


def ramp_in(x, ms):
    k = max(1, int(ms * SR / 1000)); x[:k] *= np.linspace(0, 1, k); return x


def band(noise, lo, hi):
    """Static band-pass by FFT mask (soft edges)."""
    X = np.fft.rfft(noise); f = np.fft.rfftfreq(len(noise), 1 / SR)
    m = np.clip((f - lo * 0.7) / (lo * 0.3 + 1), 0, 1) * np.clip((hi * 1.3 - f) / (hi * 0.3 + 1), 0, 1)
    return np.fft.irfft(X * m, len(noise))


def moving_band(noise, centres, width_oct=0.9):
    """Time-varying band-pass (STFT): centres = centre frequency per sample."""
    N, H = 1024, 256
    win = np.hanning(N); out = np.zeros(len(noise) + N); norm = np.zeros(len(noise) + N)
    f = np.fft.rfftfreq(N, 1 / SR)
    for s in range(0, len(noise) - N, H):
        c = centres[min(s + N // 2, len(centres) - 1)]
        m = np.exp(-0.5 * (np.log2((f + 1) / c) / (width_oct / 2)) ** 2)
        out[s:s + N] += np.fft.irfft(np.fft.rfft(noise[s:s + N] * win) * m, N) * win
        norm[s:s + N] += win ** 2
    return out[:len(noise)] / np.maximum(norm[:len(noise)], 1e-3)


def norm_peak(x, db):
    p = np.abs(x).max()
    return x / p * 10 ** (db / 20) if p > 0 else x


# ---- voices: return (signal, offset) where offset = samples BEFORE the cue time that the sound starts ----------------

def v_click(rng, p):
    n = int(0.06 * SR); t = np.arange(n) / SR; f = 1800 * rng.uniform(0.96, 1.04)
    x = np.sin(2 * np.pi * f * t) * env_exp(n, 90)
    x[:int(0.003 * SR)] += band(rng.standard_normal(int(0.003 * SR)), 2000, 7000) * 0.4
    return norm_peak(ramp_in(x, 0.3), -9), 0


def v_thock(rng, p):
    n = int(0.05 * SR); t = np.arange(n) / SR
    body = np.tanh(2.5 * np.sin(2 * np.pi * 250 * rng.uniform(0.95, 1.05) * t)) * env_exp(n, 160) * 0.45   # driven: audible harmonics
    mid = np.sin(2 * np.pi * 1100 * rng.uniform(0.95, 1.05) * t) * env_exp(n, 260) * 0.5
    tick = np.sin(2 * np.pi * 2200 * rng.uniform(0.94, 1.06) * t) * env_exp(n, 500) * 0.8
    nz = band(rng.standard_normal(n), 1200, 4000) * env_exp(n, 350) * 0.35
    tick = tick + mid
    return norm_peak(ramp_in(body + tick + nz, 0.4), -12 + rng.uniform(-1.5, 1.5)), 0


def v_tap(rng, p):
    n = int(0.05 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 900 * rng.uniform(0.95, 1.05) * t) * env_exp(n, 160) + band(rng.standard_normal(n), 800, 3000) * env_exp(n, 300) * 0.3
    return norm_peak(ramp_in(x, 0.5), -14 + rng.uniform(-1.5, 1.5)), 0


def v_tick(rng, p):
    n = int(0.012 * SR)
    x = band(rng.standard_normal(n), 2500, 6000) * env_exp(n, 900)
    return norm_peak(ramp_in(x, 0.2), -16), 0


def v_pop(rng, p):
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 600 + 900 * np.clip(t / 0.06, 0, 1)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 30)
    return norm_peak(ramp_in(x, 1.0), -12), 0


def v_send(rng, p):
    n = int(0.16 * SR); t = np.arange(n) / SR
    f = 420 + 520 * (1 - np.exp(-t / 0.03))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 22) * np.clip(t / 0.004, 0, 1)
    return norm_peak(x, -10), 0


def v_pluck(rng, p):
    """Karplus-Strong string, tuned to `param` (e.g. D5)."""
    f = note_hz(p or "D5"); n = int(0.9 * SR); L = max(2, int(round(SR / f)))
    buf = rng.uniform(-1, 1, L); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % L]
        buf[i % L] = 0.996 * 0.5 * (buf[i % L] + buf[(i + 1) % L])
    return norm_peak(ramp_in(out, 1.0), -12), 0


def v_impact(rng, p):
    n = int(0.9 * SR); t = np.arange(n) / SR
    f = 90 * np.exp(-t * 2.5) + 45
    low = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 7) * 0.24
    drive = np.tanh(4 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR)) * env_exp(n, 9) * 0.35         # harmonics a laptop can play
    body = np.sin(2 * np.pi * 440 * t) * env_exp(n, 14) * 0.45 + np.sin(2 * np.pi * 880 * t) * env_exp(n, 20) * 0.3
    k = int(0.12 * SR); hit = np.zeros(n); hit[:k] = band(rng.standard_normal(k), 600, 3500) * env_exp(k, 30) * 1.0
    return norm_peak(ramp_in(low + drive + body + hit, 0.5), -4), 0


def v_whoosh(rng, p):
    L = float(p or 0.6); n = int(L * SR); t = np.arange(n) / SR; pk = 0.7 * L
    envl = np.where(t < pk, (t / pk) ** 2, np.exp(-(t - pk) / (0.12 * L)))
    centres = 400 * 2 ** (3.2 * np.clip(t / pk, 0, 1)) * np.where(t > pk, np.exp(-(t - pk) * 3), 1)
    x = moving_band(rng.standard_normal(n), centres) * envl
    return norm_peak(x, -10), int(pk * SR)           # peak on the cue


def v_riser(rng, p):
    L = float(p or 3.0); n = int(L * SR); t = np.arange(n) / SR
    centres = 500 * 2 ** (2.9 * (t / L) ** 1.5)                       # 500 Hz → ~3.7 kHz: stays where small speakers play
    x = moving_band(rng.standard_normal(n), centres, 0.7) * (t / L) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(440 * 2 ** (1.5 * t / L)) / SR) * (t / L) ** 3 * 0.35
    y = x + tone
    w = int(0.03 * SR); rms = np.sqrt(np.convolve(y ** 2, np.ones(w) / w, "same")) + 1e-6
    y = y / rms * (t / L) ** 2                       # re-impose a clean rise so the loudest point is the end, on the cue
    y[-int(0.004 * SR):] *= np.linspace(1, 0, int(0.004 * SR))
    return norm_peak(y, -10), n                       # ends on the cue


VOICES = {"click": v_click, "thock": v_thock, "tap": v_tap, "tick": v_tick, "pop": v_pop, "send": v_send,
          "pluck": v_pluck, "impact": v_impact, "whoosh": v_whoosh, "riser": v_riser}
ALIGN = {"whoosh": "peak", "riser": "end"}


def parse_cue(s):
    parts = s.split(":")
    t = float(parts[0]); typ, _, param = parts[1].partition("=")
    db = float(parts[2]) if len(parts) > 2 else 0.0
    return dict(t=t, type=typ, param=param or None, db=db)


def render(cues, seed, dur=None):
    rng = np.random.default_rng(seed)
    dur = dur or max(c["t"] for c in cues) + 2.0
    out = np.zeros(int(dur * SR) + SR)
    report = []
    for c in sorted(cues, key=lambda c: c["t"]):
        if c["type"] not in VOICES:
            sys.exit(f"unknown sound type {c['type']!r}; choose from {', '.join(VOICES)}")
        x, off = VOICES[c["type"]](rng, c.get("param"))
        x = x * 10 ** (c.get("db", 0) / 20)
        start = int(round(c["t"] * SR)) - off
        if start < 0:
            x = x[-start:]; start = 0
        end = min(len(out), start + len(x)); out[start:end] += x[:end - start]
        report.append(f"  {c['t']:8.3f}  {c['type']:7s} {('=' + c['param']) if c.get('param') else '':6s} "
                      f"{ALIGN.get(c['type'], 'attack')} on cue · starts {start / SR:.3f} · {len(x) / SR:.2f} s")
    return out[:int(dur * SR)], report


def write_wav(path, x):
    peak = np.abs(x).max()
    if peak > 0.99:
        x = x / peak * 0.99
        print(f"  (scaled down {20 * np.log10(peak / 0.99):.1f} dB to avoid clipping)")
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, 1).tobytes())


def main():
    global SR
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 7
    if "--sr" in a: SR = int(a[a.index("--sr") + 1])
    if a[0] == "--gallery":
        import os
        d = a[1]; os.makedirs(d, exist_ok=True)
        demo = {"whoosh": "0.6", "riser": "3", "pluck": "D5"}
        for name in VOICES:
            p = demo.get(name)
            t = float(p) if name in ("whoosh", "riser") and p else 0.1
            x, _ = render([dict(t=max(t, 0.1), type=name, param=p, db=0)], seed, dur=max(t, 0.1) + 1.2)
            write_wav(f"{d}/{name}.wav", x); print("wrote", f"{d}/{name}.wav")
        return
    out = a[0]
    cues = [parse_cue(a[i + 1]) for i, v in enumerate(a) if v == "--cue"]
    if "--cues" in a:
        for c in json.load(open(a[a.index("--cues") + 1])):
            cues.append(dict(t=float(c["t"]), type=c["type"], param=c.get("param"), db=float(c.get("db", 0))))
    if not cues:
        sys.exit("no cues: add --cue t:type or --cues file.json")
    dur = float(a[a.index("--duration") + 1]) if "--duration" in a else None
    x, report = render(cues, seed, dur)
    write_wav(out, x)
    print(f"wrote {out} · {len(x) / SR:.2f} s · {len(cues)} cues")
    print("\n".join(report))


if __name__ == "__main__":
    main()
