#!/usr/bin/env python3
"""Original, seeded stage backgrounds for app footage (no third-party artwork, so no licence questions).

Three families:
  silk     broad satin folds: a lit height field (diffuse + soft specular), coloured by height
  ribbons  wide flowing diagonal bands, each with its own gradient and a soft shadow on the one below
  ridges   layered hills under a sky, far layers hazed into the sky colour

Usage:
  wallpapers.py --preset midnight --out stage.png                  # 2560x1440 by default
  wallpapers.py --style silk --colors 040814,0e2870,2870dc,82c8ff --seed 3 --out blue.png
  wallpapers.py --style ridges --colors ffbe98,f0a0ac,aa96e8 --layers 7 --out dusk.png
  wallpapers.py --gallery out_dir --size 1280x720                  # every preset, to compare as stills
Presets: midnight, sunrise, emerald, graphite, ribbons-blue, ribbons-dusk, ridges-dusk, pastel.
Needs: Python with numpy + scipy, and ffmpeg (writes PNG).
Tip: keep the app's own UI untouched; put this behind it, and a dark plate under any fading window.
"""
import sys, subprocess, numpy as np
from scipy import ndimage


def hexrgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def stops_from(colors):
    n = len(colors)
    return [(i / (n - 1), hexrgb(c)) for i, c in enumerate(colors)]


class Canvas:
    def __init__(self, w, h):
        self.W, self.H = w, h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
        self.X, self.Y = xx / h, yy / h

    def noise(self, seed, cells=2):
        r = np.random.default_rng(seed).standard_normal((cells + 3, int(cells * self.W / self.H) + 3))
        z = ndimage.zoom(r, (self.H / cells, self.H / cells), order=3)
        return ndimage.gaussian_filter(z[:self.H, :self.W], self.H / cells / 3)


def ramp(t, stops):
    t = np.clip(t, 0, 1); out = np.zeros(t.shape + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t >= p0) & (t <= p1); k = ((t - p0) / max(p1 - p0, 1e-6))[m][:, None]
        out[m] = np.array(c0) * (1 - k) + np.array(c1) * k
    return out


def finish(c, rgb, vignette, seed):
    v = 1 - vignette * (((c.X - c.W / c.H / 2) / (c.W / c.H / 2)) ** 2 * 0.6 + ((c.Y - 0.5) / 0.5) ** 2 * 0.4)
    rgb = rgb * v[..., None] + np.random.default_rng(seed).uniform(-0.6, 0.6, rgb.shape)   # dither: no banding
    return np.clip(rgb, 0, 255).astype(np.uint8)


def silk(c, stops, seed=1, ang=0.6, light=(-0.45, -0.55, 0.7), spec=0.35, shine=14, spec_col=(255, 255, 255), vig=0.3):
    n1, n2 = c.noise(seed), c.noise(seed + 1)
    ca, sa = np.cos(ang), np.sin(ang); U = c.X * ca + c.Y * sa; V = -c.X * sa + c.Y * ca
    h = np.sin(2.4 * U + 0.9 * np.sin(1.3 * V + 0.5) + 0.6 * n1) + 0.45 * np.sin(1.3 * V - 0.8 * U + 0.5 * n2)
    h = ndimage.gaussian_filter(h, 6 * c.H / 1440)
    gy, gx = np.gradient(h); k = 160 * c.H / 1440
    nx, ny, nz = -gx * k, -gy * k, np.ones_like(h); nn = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx, ny, nz = nx / nn, ny / nn, nz / nn
    L = np.array(light) / np.linalg.norm(light); Hh = (L + [0, 0, 1]) / np.linalg.norm(L + [0, 0, 1])
    diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    sp = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1) ** shine
    base = ramp(0.55 * (h - h.min()) / (h.max() - h.min()) + 0.45 * (1 - c.Y), stops)
    return finish(c, base * (0.45 + 0.7 * diff[..., None]) + spec * sp[..., None] * np.array(spec_col), vig, seed)


def ribbons(c, bg, bands, seed=7, vig=0.25):
    r = np.random.default_rng(seed)
    rgb = ramp(0.5 * c.X / (c.W / c.H) + 0.5 * c.Y, bg)
    for i, (ca, cb) in enumerate(bands):
        ph = r.uniform(0, 6.3, 2); off = -0.25 + 1.5 * i / len(bands)
        edge = off + 0.33 * c.X + 0.12 * np.sin(2.2 * c.X + ph[0]) + 0.05 * np.sin(5.1 * c.X + ph[1])
        inside = np.clip((c.Y - edge) * c.H / 1.6, 0, 1)[..., None]
        g = np.clip((c.Y - edge) / 0.45, 0, 1)[..., None]
        col = np.array(ca) * (1 - g) + np.array(cb) * g
        shadow = 1 - 0.28 * np.exp(-np.clip(edge - c.Y, 0, None) * c.H / 45)[..., None] * (1 - inside)
        rgb = rgb * shadow * (1 - inside) + col * inside
    return finish(c, ndimage.gaussian_filter(rgb, (1.2, 1.2, 0)), vig, seed)


def ridges(c, sky, layers, haze, seed=3, vig=0.22):
    r = np.random.default_rng(seed); rgb = ramp(c.Y, sky); n = len(layers)
    for i, col in enumerate(layers):
        base = 0.36 + 0.6 * i / max(n - 1, 1); ph = r.uniform(0, 6.3, 3); amp = 0.075 * (1 - 0.3 * i / n)
        curve = base + amp * np.sin(1.7 * c.X + ph[0]) + amp * 0.5 * np.sin(3.9 * c.X + ph[1]) + amp * 0.18 * np.sin(8.1 * c.X + ph[2])
        inside = np.clip((c.Y - curve) * c.H / 1.4, 0, 1)[..., None]
        hz = 0.55 * (1 - i / max(n - 1, 1)) ** 1.6
        cc = np.array(col) * (1 - hz) + np.array(haze) * hz
        rim = np.exp(-np.clip(c.Y - curve, 0, None) * c.H / 26)[..., None] * 0.22
        depth = np.clip(1.05 - 0.5 * (c.Y - curve) / 0.45, 0.62, 1.05)[..., None]
        shadow = 1 - 0.16 * np.exp(-np.clip(curve - c.Y, 0, None) * c.H / 70)[..., None] * (1 - inside)
        rgb = rgb * shadow * (1 - inside) + (cc * depth + 255 * rim) * inside
    return finish(c, rgb, vig, seed)


PRESETS = {
    "midnight": lambda c: silk(c, stops_from(["04081a", "0e286e", "286edc", "82c8ff"]), seed=11, ang=0.55),
    "sunrise": lambda c: silk(c, stops_from(["240a30", "8c2464", "f06858", "ffc48c"]), seed=21, ang=-0.5, light=(0.4, -0.5, 0.75)),
    "emerald": lambda c: silk(c, stops_from(["021212", "064642", "1a967a", "96e8c6"]), seed=31, ang=0.7, spec_col=(220, 255, 240)),
    "graphite": lambda c: silk(c, stops_from(["06070a", "1a1c22", "3e4452", "8c96af"]), seed=41, ang=0.45, spec=0.3, spec_col=(200, 220, 255)),
    "pastel": lambda c: silk(c, stops_from(["a096d7", "cdb2e8", "f8ced6", "ffecde"]), seed=51, ang=0.6, spec=0.25, vig=0.1),
    "ribbons-blue": lambda c: ribbons(c, stops_from(["0a143c", "040818"]),
                                      [((40, 110, 240), (20, 50, 150)), ((70, 170, 250), (30, 90, 200)), ((120, 210, 255), (40, 130, 230)),
                                       ((30, 70, 190), (12, 28, 90)), ((16, 40, 120), (6, 14, 50))]),
    "ribbons-dusk": lambda c: ribbons(c, stops_from(["3c1e5a", "140a28"]),
                                      [((250, 140, 120), (200, 70, 120)), ((230, 100, 160), (140, 50, 150)), ((170, 90, 220), (90, 50, 170)),
                                       ((90, 70, 200), (40, 30, 120)), ((40, 30, 110), (16, 12, 50))]),
    "ridges-dusk": lambda c: ridges(c, stops_from(["ffbe98", "f0a0ac", "aa96e8"]),
                                    [(186, 120, 214), (146, 100, 210), (108, 80, 196), (78, 60, 170), (52, 42, 138), (32, 28, 100), (20, 18, 68)],
                                    haze=(235, 170, 200)),
}


def save(img, path):
    h, w, _ = img.shape
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-i", "-",
                    "-frames:v", "1", path], input=img.tobytes(), check=True)
    print("wrote", path)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    w, h = (int(v) for v in get("--size", "2560x1440").lower().split("x"))
    c = Canvas(w, h)
    if "--gallery" in a:
        import os
        d = get("--gallery"); os.makedirs(d, exist_ok=True)
        for name, fn in PRESETS.items():
            save(fn(c), f"{d}/{name}.png")
        return
    out = get("--out") or sys.exit("add --out file.png")
    if get("--preset"):
        img = PRESETS[get("--preset")](c)
    else:
        style = get("--style", "silk"); colors = (get("--colors") or "04081a,0e286e,286edc,82c8ff").split(",")
        seed = int(get("--seed", "1"))
        if style == "silk":
            img = silk(c, stops_from(colors), seed=seed)
        elif style == "ribbons":
            cols = [hexrgb(x) for x in colors]
            bands = [(cols[i], cols[min(i + 1, len(cols) - 1)]) for i in range(len(cols))]
            img = ribbons(c, stops_from([colors[0], colors[-1]]), bands, seed=seed)
        elif style == "ridges":
            sky = colors[:3]; n = int(get("--layers", "7")); top, bot = np.array(hexrgb(colors[-1])), np.array((20, 18, 60))
            layers = [tuple((top * (1 - i / (n - 1)) + bot * i / (n - 1)).astype(int)) for i in range(n)]
            img = ridges(c, stops_from(sky), layers, haze=hexrgb(sky[1]), seed=seed)
        else:
            sys.exit("style must be silk, ribbons or ridges")
    save(img, out)


if __name__ == "__main__":
    main()
