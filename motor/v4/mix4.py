# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
"""Voz + beat original (estilo phonk/trap oscuro) + diseño de sonido -> build4/<id>/audio.wav"""
import sys, os, json, numpy as np, soundfile as sf
from scipy import signal
SR = 48000
def env(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def sos(kind, f, order=2): return signal.butter(order, f, btype=kind, fs=SR, output="sos")
def lp(x, f, o=2): return signal.sosfilt(sos("low", f, o), x)
def hp(x, f, o=2): return signal.sosfilt(sos("high", f, o), x)
def bp(x, lo, hi, o=2): return signal.sosfilt(sos("band", [lo, hi], o), x)
def add(buf, x, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i < 0 or i >= len(buf): return
    x = x[: len(buf) - i]
    if x.ndim == 1:
        buf[i:i + len(x), 0] += x * g * (1 - max(pan, 0)); buf[i:i + len(x), 1] += x * g * (1 + min(pan, 0))
    else: buf[i:i + len(x)] += x * g

def beat(dur, seed):
    rng = np.random.default_rng(seed)
    bpm = 140; b = 60 / bpm; bar = 4 * b
    tr = [0, -2, 3, -3, 2][seed % 5]
    f = lambda m: 440 * 2 ** ((m + tr - 69) / 12)
    roots = [33, 33, 29, 31]       # La, La, Fa, Sol (graves)
    n = int((dur + 2) * SR); out = np.zeros((n, 2))
    # 808 con deslizamiento
    def s808(m, L, glide_to=None):
        k = int(L * SR); t = np.arange(k) / SR
        fr = np.full(k, f(m))
        if glide_to is not None: g = np.clip((t - L * 0.6) / (L * 0.3), 0, 1); fr = f(m) * (f(glide_to) / f(m)) ** g
        ph = 2 * np.pi * np.cumsum(fr) / SR
        x = np.sin(ph) + 0.18 * np.sin(2 * ph)
        x = np.tanh(x * 2.2) / np.tanh(2.2)
        a = np.minimum(1, np.arange(k) / (0.004 * SR)) * env(k, L * 0.55)
        return lp(x * a, 900)
    kn = int(0.35 * SR); tk = np.arange(kn) / SR
    kick = np.sin(2 * np.pi * (50 * tk + 160 * 0.025 * (1 - np.exp(-tk / 0.025)))) * env(kn, 0.12)
    sn = int(0.3 * SR); snare = (bp(rng.standard_normal(sn), 1200, 8000) * env(sn, 0.07) + np.sin(2 * np.pi * 185 * np.arange(sn) / SR) * env(sn, 0.04) * 0.6)
    clap = np.zeros(int(0.25 * SR))
    for d in (0, 0.011, 0.023):
        c = bp(rng.standard_normal(len(clap)), 900, 5000) * env(len(clap), 0.05); clap[int(d * SR):] += c[: len(clap) - int(d * SR)] * 0.6
    hn = int(0.05 * SR); hat = hp(rng.standard_normal(hn), 8000, 4) * env(hn, 0.010)
    # campana estilo phonk (cowbell) sobre una escala menor
    def bell(m, L=0.28):
        k = int(L * SR); t = np.arange(k) / SR
        x = (np.sign(np.sin(2 * np.pi * f(m) * t)) + np.sign(np.sin(2 * np.pi * f(m) * 1.48 * t))) * 0.5
        return bp(x, 500, 4500) * env(k, 0.08)
    mel = [69, 72, 76, 74, 72, 69, 67, 69,  69, 72, 76, 79, 77, 76, 74, 72]
    pat = [0, 0.75, 1.5, 2.0, 2.5, 3.0, 3.25, 3.5]
    nb = int(np.ceil((dur + 2) / bar))
    for i in range(nb):
        t0 = i * bar; r = roots[i % 4]
        nxt = roots[(i + 1) % 4]
        add(out, s808(r, bar * 0.95, nxt if i % 4 == 3 else None), t0, 0.42)
        for q in (0, 2.5) if i % 2 == 0 else (0, 1.75, 2.5):
            add(out, kick, t0 + q * b, 0.65)
        add(out, snare, t0 + 2 * b, 0.20); add(out, clap, t0 + 2 * b, 0.32)
        for s in range(16):                     # hi-hats en semicorcheas con redobles
            g = 0.10 if s % 2 == 0 else 0.055
            add(out, hat, t0 + s * b / 4, g, 0.25)
            if i % 2 == 1 and s in (13, 14, 15):
                for r3 in range(1, 3): add(out, hat, t0 + s * b / 4 + r3 * b / 12, 0.05, -0.25)
        for j, q in enumerate(pat):
            m = mel[(j + 8 * (i % 2)) % 16]
            add(out, bell(m), t0 + q * b, 0.075, -0.35 if j % 2 else 0.35)
    return out[: int(dur * SR)], 60 / bpm


def beat_style(dur, seed, style):
    if style == "phonk": return beat(dur, seed)[0]
    rng = np.random.default_rng(seed + 99)
    n = int((dur + 2) * SR); out = np.zeros((n, 2))
    tr = [0, -2, 3, -3, 2][seed % 5]; f = lambda m: 440 * 2 ** ((m + tr - 69) / 12)
    kn = int(0.4 * SR); tk = np.arange(kn) / SR
    if style == "trap":
        bpm = 150; b = 60 / bpm; bar = 4 * b
        kick = np.sin(2 * np.pi * (45 * tk + 120 * 0.03 * (1 - np.exp(-tk / 0.03)))) * env(kn, 0.2)
        hn = int(0.04 * SR); hat = hp(noise(rng, hn), 9000, 4) * env(hn, 0.008)
        sn = int(0.25 * SR); snr = bp(noise(rng, sn), 1500, 9000) * env(sn, 0.06)
        prog = [57, 53, 55, 52]           # La m, Fa, Sol, Mi
        def pluck(m, L=0.5):
            k = int(L * SR); t = np.arange(k) / SR
            x = sum(np.sin(2 * np.pi * f(m) * h * t) / h ** 1.6 for h in (1, 2, 3, 4)) * env(k, 0.18)
            return x
        for i in range(int(np.ceil((dur + 2) / bar))):
            t0 = i * bar; r = prog[i % 4]
            k8 = int(bar * SR); t8 = np.arange(k8) / SR
            add(out, np.tanh(np.sin(2 * np.pi * f(r - 24) * t8) * 2) * env(k8, bar * .5) * .9, t0, 0.38)
            for q in ((0, 1.5, 2.75) if i % 2 else (0, 2.25)): add(out, kick, t0 + q * b, 0.6)
            add(out, snr, t0 + 2 * b, 0.28)
            roll = i % 4 == 3
            for s_ in range(8 if not roll else 16):
                add(out, hat, t0 + s_ * b / (2 if not roll else 4), 0.09, 0.3)
            for j, (q, iv) in enumerate([(0, 12), (0.5, 15), (1, 19), (1.5, 15), (2, 12), (2.5, 15), (3, 19), (3.5, 22)]):
                add(out, pluck(r + iv), t0 + q * b, 0.06, 0.3 if j % 2 else -0.3)
        return out[: int(dur * SR)]
    # synthwave / outrun
    bpm = 112; b = 60 / bpm; bar = 4 * b
    kick = np.sin(2 * np.pi * (52 * tk + 150 * 0.02 * (1 - np.exp(-tk / 0.02)))) * env(kn, 0.15)
    sn = int(0.4 * SR); snr = bp(noise(rng, sn), 800, 7000) * env(sn, 0.15)
    hn = int(0.06 * SR); hat = hp(noise(rng, hn), 7000, 4) * env(hn, 0.02)
    prog = [45, 41, 43, 40]
    def saw(m, L):
        k = int(L * SR); t = np.arange(k) / SR; ph = (f(m) * t) % 1
        x = (2 * ph - 1) + (2 * ((f(m) * 1.005 * t) % 1) - 1)
        return lp(x, 2200) * env(k, L * 0.7)
    for i in range(int(np.ceil((dur + 2) / bar))):
        t0 = i * bar; r = prog[i % 4]
        for q in range(4): add(out, kick, t0 + q * b, 0.55)
        for q in (1, 3): add(out, snr, t0 + q * b, 0.22)
        for q in range(8): add(out, hat, t0 + q * b / 2 + b / 4, 0.06, 0.2)
        for q in range(8): add(out, saw(r, b / 2 * 0.9), t0 + q * b / 2, 0.10)
        for j, iv in enumerate([24, 31, 36, 31, 27, 31, 36, 39] * 2):
            add(out, saw(r + iv, b / 4 * 0.8), t0 + j * b / 4, 0.035, 0.4 if j % 2 else -0.4)
    return out[: int(dur * SR)]

def noise(rng, n): return rng.standard_normal(n)
def SFX(kind, rng):
    if kind == "whoosh" or kind == "whip":
        L = 0.32 if kind == "whoosh" else 0.22
        n = int(L * SR); x = noise(rng, n); u = np.linspace(0, 1, n)
        y = np.zeros(n); low = band = 0.0
        fc = (300 * (25 ** u)) if kind == "whoosh" else (900 * (12 ** u))
        for i in range(n):
            fk = 2 * np.sin(np.pi * min(fc[i], 11000) / SR); low += fk * band; high = x[i] - low - 0.45 * band; band += fk * high; y[i] = band
        y *= np.sin(np.pi * u) ** (2 if kind == "whoosh" else 1.2)
        st = np.stack([y, np.roll(y, int(0.004 * SR))], 1)
        return st * (0.9 if kind == "whip" else 0.7)
    if kind == "glitch":
        n = int(0.20 * SR); y = np.zeros(n)
        for k in range(6):
            a = int(rng.random() * n * 0.8); L = int((0.01 + rng.random() * 0.03) * SR)
            seg = np.sign(np.sin(2 * np.pi * (200 + rng.random() * 2500) * np.arange(L) / SR)) * 0.5 + noise(rng, L) * 0.3
            y[a:a + L] += seg[: n - a]
        y = np.round(y * 6) / 6
        return hp(y, 300) * 0.55
    if kind == "impact":
        n = int(0.9 * SR); t = np.arange(n) / SR
        sub = np.sin(2 * np.pi * (38 * t + 110 * 0.05 * (1 - np.exp(-t / 0.05)))) * env(n, 0.28)
        crack = bp(noise(rng, n), 1500, 9000) * env(n, 0.025) * 0.8
        body = lp(noise(rng, n), 600) * env(n, 0.12) * 0.6
        rev = lp(noise(rng, n), 3000) * env(n, 0.35) * 0.08
        return np.tanh((sub + crack + body + rev) * 1.4) * 0.9
    if kind == "thump":
        n = int(0.3 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * (48 * t + 80 * 0.03 * (1 - np.exp(-t / 0.03)))) * env(n, 0.09) + bp(noise(rng, n), 2000, 7000) * env(n, 0.006) * 0.4) * 0.9
    if kind == "boom":
        n = int(1.4 * SR); t = np.arange(n) / SR
        return np.tanh((np.sin(2 * np.pi * (32 * t + 140 * 0.08 * (1 - np.exp(-t / 0.08)))) * env(n, 0.45) + bp(noise(rng, n), 300, 5000) * env(n, 0.06) * 0.7) * 1.5)
    if kind == "riser":
        n = int(0.9 * SR); u = np.linspace(0, 1, n); t = np.arange(n) / SR
        x = bp(noise(rng, n), 800, 9000) * u ** 2.5 * 0.6 + np.sin(2 * np.pi * (200 * t + 900 * t * t)) * u ** 2 * 0.25
        return x
    if kind == "camera":
        n = int(0.16 * SR); y = np.zeros(n)
        for d in (0, 0.055):
            k = int(0.04 * SR); c = bp(noise(rng, k), 2000, 9000) * env(k, 0.006); y[int(d * SR):int(d * SR) + k] += c
        return y * 0.9
    if kind == "pop":
        n = int(0.1 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (500 * t + 1800 * t * t)) * env(n, 0.025) * 0.6
    if kind == "tick":
        n = int(0.03 * SR); return bp(noise(rng, n), 3000, 8000) * env(n, 0.003) * 0.6
    if kind == "cash":
        n = int(0.9 * SR); t = np.arange(n) / SR
        bellx = (np.sin(2 * np.pi * 2637 * t) + 0.6 * np.sin(2 * np.pi * 3520 * t) + 0.4 * np.sin(2 * np.pi * 5274 * t)) * env(n, 0.22)
        clink = bp(noise(rng, n), 4000, 10000) * env(n, 0.01)
        return (bellx * 0.35 + clink * 0.5)
    return np.zeros(10)


def SFX2(kind, rng, v):
    """Variantes nuevas y versiones de las viejas."""
    if kind == "swish":
        n = int(0.28 * SR); u = np.linspace(0, 1, n); x = bp(noise(rng, n), 2500, 9000) * np.sin(np.pi * u) ** 1.5
        return np.stack([x * (1 - u), x * u], 1) * 0.8
    if kind == "swoosh_up":
        n = int(0.45 * SR); u = np.linspace(0, 1, n); t = np.arange(n) / SR
        x = bp(noise(rng, n), 400, 6000) * u ** 1.8 * (1 - u) ** .3 + np.sin(2 * np.pi * (150 * t + 600 * t * t)) * u * 0.2
        return x * 0.9
    if kind == "zoom_in":
        n = int(0.55 * SR); u = np.linspace(0, 1, n); t = np.arange(n) / SR
        x = np.sin(2 * np.pi * (80 * t + 700 * t * t)) * u ** 2 * 0.35 + bp(noise(rng, n), 1500, 8000) * u ** 3 * 0.5
        return x
    if kind == "bass_drop":
        n = int(1.2 * SR); t = np.arange(n) / SR
        return np.tanh(np.sin(2 * np.pi * (28 * t + 220 * 0.12 * (1 - np.exp(-t / 0.12)))) * env(n, 0.5) * 2.2) * 0.9 + bp(noise(rng, n), 200, 3000) * env(n, 0.04) * 0.5
    if kind == "counter":
        n = int(0.95 * SR); y = np.zeros(n); k = int(0.02 * SR)
        click = bp(noise(rng, k), 2500, 7000) * env(k, 0.003)
        tt = 0.0; i = 0
        while tt < 0.88:
            a = int(tt * SR); y[a:a + k] += click[: n - a] * (0.5 + 0.5 * tt); tt += 0.025 + 0.11 * (tt / 0.9) ** 2; i += 1
        return y * 0.8
    if kind == "ding":
        n = int(0.8 * SR); t = np.arange(n) / SR; f0 = [1568, 1760, 2093][v % 3]
        return (np.sin(2 * np.pi * f0 * t) + 0.4 * np.sin(2 * np.pi * f0 * 2.01 * t)) * env(n, 0.18) * 0.35
    if kind == "typing":
        n = int(0.85 * SR); y = np.zeros(n); k = int(0.025 * SR)
        for j in range(16):
            a = int((0.2 + j * 0.037 + rng.random() * 0.01) * SR)
            if a + k < n: y[a:a + k] += bp(noise(rng, k), 1500 + rng.random() * 2500, 9000) * env(k, 0.004) * (0.6 + 0.4 * rng.random())
        return y * 0.9
    if kind == "boom_soft":
        n = int(1.5 * SR); t = np.arange(n) / SR
        return lp(np.sin(2 * np.pi * 42 * t) * env(n, 0.6) + noise(rng, n) * env(n, 0.3) * 0.3, 300) * 0.9
    if kind == "scratch":
        n = int(0.42 * SR); t = np.arange(n) / SR
        rate = 1 + 0.9 * np.sin(2 * np.pi * 6 * t); ph = np.cumsum(rate) / SR
        x = bp(noise(rng, n), 600, 4000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * t))) + np.sin(2 * np.pi * 300 * ph) * 0.3
        return x * env(n, 0.25) * 0.8
    return None

def make_sfx(kind, rng, v):
    x = SFX2(kind, rng, v)
    if x is None:
        x = SFX(kind, rng)
    # variación: tono distinto en cada aparición
    f = [0.86, 1.0, 1.14][v % 3] * (0.95 + 0.1 * rng.random())
    if abs(f - 1) > 0.01:
        L = int(len(x) / f)
        x = signal.resample(x, L, axis=0)
    return x


AMB = dict(vc_skyline_noche="city", gasolinera_neon="city", lucia_auto_neon="city", azotea_coctel_noche="city", lucia_checks_cashing="city", port_gellhorn_motel="night",
  vc_letrero_avion="traffic", vc_noria_dia="traffic", jl_auto_pistolas="car", jason_manejando_copiloto="car", jl_convertible_costa="car", lucia_persecucion_tunel="car",
  jl_moto_policia_helicoptero="police", jason_reja_policia="police", jl_abrazo_pantano_policia="police",
  vc_helicoptero_atardecer="heli", jason_hidroavion="heli", marina_yates="sea", leonida_keys_aereo="sea", port_gellhorn_atardecer="sea",
  grassrivers_skyline="nature", mount_kalaga_canon="nature", jason_rifle_perro="nature", ambrosia_fiesta_lodo="party", lucia_gimnasio="gym", jl_gimnasio_pelea="gym",
  jl_auto_llamas_bolsas="fire", jl_cubriendose_armas="tense", jason_capucha_rifle="tense", jason_pistola_balas_dinero="tense", pitbull_cadena="night",
  vc_torres_agua="wind", jl_escalera_metal="wind")

def ambience(kind, n, rng):
    t = np.arange(n) / SR
    brown = np.cumsum(rng.standard_normal(n)); brown = hp(brown - np.convolve(brown, np.ones(4800) / 4800, "same"), 30)
    brown /= np.abs(brown).max() + 1e-9
    wn = rng.standard_normal(n)
    if kind in ("city", "traffic", "night"):
        x = lp(brown, 350) * 1.0 + bp(wn, 400, 2500) * 0.04
        for k in range(int(n / SR / 3) + 1):                         # autos que pasan
            a = int((rng.random() * 3 + k * 3) * SR); L = int(2.2 * SR)
            if a + L < n: u = np.linspace(0, 1, L); x[a:a + L] += bp(rng.standard_normal(L), 200, 1800) * np.sin(np.pi * u) ** 2 * 0.25
        if kind == "night": x = x * 0.6 + np.sin(2 * np.pi * 4600 * t) * (np.sin(2 * np.pi * 18 * t) > 0.6) * (np.sin(2 * np.pi * 0.7 * t) > 0) * 0.02
        return x
    if kind == "car":
        eng = np.sin(2 * np.pi * (38 + 4 * np.sin(2 * np.pi * 0.3 * t)) * t) * 0.3 + lp(brown, 180) * 0.8
        return eng + bp(wn, 600, 4000) * 0.05
    if kind == "police":
        f = 950 + 350 * np.sin(2 * np.pi * 0.45 * t)
        siren = lp(np.sin(2 * np.pi * np.cumsum(f) / SR), 2500) * 0.06
        return lp(brown, 300) * 0.7 + siren
    if kind == "heli":
        chop = (0.5 + 0.5 * np.sin(2 * np.pi * 11.5 * t)) ** 3
        return lp(wn, 500) * chop * 0.6 + lp(brown, 200) * 0.5
    if kind == "sea":
        sw = 0.55 + 0.45 * np.sin(2 * np.pi * 0.12 * t + 1.3) ** 2
        return lp(wn, 900) * sw * 0.35 + hp(wn, 4000) * sw * 0.03 + lp(brown, 150) * 0.3
    if kind in ("nature", "wind"):
        w = bp(wn, 200, 900) * (0.4 + 0.3 * np.sin(2 * np.pi * 0.17 * t)) * 0.5
        if kind == "nature":
            w += np.sin(2 * np.pi * 4200 * t) * (np.sin(2 * np.pi * 22 * t) > 0.3) * (np.sin(2 * np.pi * 0.9 * t) > -0.2) * 0.015
        return w
    if kind in ("party", "gym"):
        bab = sum(bp(rng.standard_normal(n), 250 + 150 * j, 1800 + 300 * j) * (0.6 + 0.4 * np.sin(2 * np.pi * (0.3 + 0.2 * j) * t + j)) for j in range(3)) * 0.12
        return bab + lp(brown, 120) * 0.3
    if kind == "fire":
        cr = np.zeros(n); idx = rng.integers(0, n, int(n / SR * 40)); cr[idx] = rng.standard_normal(len(idx)) * 1.5
        return hp(np.convolve(cr, np.exp(-np.arange(200) / 30), "same"), 1500) * 0.3 + lp(brown, 200) * 0.6
    if kind == "tense":
        return np.sin(2 * np.pi * 55 * t) * 0.12 + lp(brown, 250) * 0.5
    return lp(brown, 300) * 0.5

def amb_track(tl, n, rng):
    out = np.zeros(n); cache = {}
    for s_ in tl["shots"]:
        L = s_.get("lay") or {}
        if L.get("k") in ("slam", "count", "news") or not s_.get("img"): continue
        k = AMB.get(s_["img"], "city")
        if k not in cache: cache[k] = ambience(k, n, rng)
        a, b = int(s_["t0"] * SR), min(n, int(s_["t1"] * SR))
        if b <= a: continue
        g = np.ones(b - a); f = min(int(0.06 * SR), (b - a) // 2)
        if f > 0: g[:f] = np.linspace(0, 1, f); g[-f:] = np.linspace(1, 0, f)
        out[a:b] += cache[k][a:b] * g
    r = np.sqrt(np.mean(out ** 2)) + 1e-9
    return out / r

G = {"swish": 0.22, "swoosh_up": 0.25, "zoom_in": 0.28, "bass_drop": 0.45, "counter": 0.25, "ding": 0.22, "typing": 0.25, "boom_soft": 0.35, "scratch": 0.30, "whoosh": 0.22, "whip": 0.30, "glitch": 0.20, "impact": 0.42, "thump": 0.30, "boom": 0.50, "riser": 0.22, "camera": 0.30, "pop": 0.20, "tick": 0.05, "cash": 0.22}

def load_song(path, start, n):
    import subprocess, tempfile
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-i", path, "-t", str(n / SR + 1), "-ac", "2", "-ar", str(SR), tmp])
    m, _ = sf.read(tmp, dtype="float64"); os.remove(tmp)
    m = np.pad(m, ((0, max(0, n - len(m))), (0, 0)))[:n]
    m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * 0.25
    fi = int(0.05 * SR); m[:fi] *= np.linspace(0, 1, fi)[:, None]
    return m

def game_audio(tl, n):
    """Audio original del gameplay de cada toma, bajito bajo la voz."""
    import subprocess, tempfile, importlib
    try:
        M = importlib.import_module("mkclips21"); C = {k: v for k, v in M.C.items() if v[0] in M.LIMPIO}
    except Exception:
        return None
    out = np.zeros((n, 2)); got = False
    for s_ in tl["shots"]:
        c = s_.get("clip")
        if not c or c not in C: continue
        src, st, _, _ = C[c]; a0 = st + float(s_.get("cs", 0)); d = s_["t1"] - s_["t0"]
        if d <= 0.05: continue
        tmp = tempfile.mktemp(suffix=".wav")
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a0), "-i", "src_in/" + src, "-t", str(d + 0.05), "-vn", "-ac", "2", "-ar", str(SR), tmp])
        if r.returncode != 0 or not os.path.exists(tmp): continue
        x, _ = sf.read(tmp, dtype="float64"); os.remove(tmp)
        if x.ndim == 1: x = np.stack([x, x], 1)
        i0 = int(s_["t0"] * SR); L = min(len(x), n - i0)
        if L <= 0: continue
        x = x[:L]; f = min(int(0.03 * SR), L // 2)
        if f > 0: x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        out[i0:i0 + L] += x; got = True
    if not got: return None
    r = np.sqrt(np.mean(out ** 2)) + 1e-9
    return out / r * 0.06

def build(vid):
    d = f"build4/{vid}"; tl = json.load(open(f"{d}/timeline.json")); dur = tl["duration"]
    v, sr = sf.read(f"{d}/voice.wav", dtype="float64")
    v = signal.resample_poly(v, SR, sr); v = hp(v, 80)
    v = v + 0.30 * bp(v, 2500, 7000, 1) + 0.15 * bp(v, 120, 260, 1)          # presencia + cuerpo
    v = v / (np.abs(v).max() + 1e-9) * 0.9
    e = np.sqrt(np.maximum(lp(v * v, 15), 0)); g = np.clip(0.17 / (e + 0.035), 0.6, 2.5); v = np.tanh(v * g * 1.2) * 0.92
    n = int(dur * SR); v = np.pad(v, (0, max(0, n - len(v))))[:n]
    if tl.get("song"):
        mus = load_song(tl["song"], tl.get("song_start", 0.0), n)
    else:
        mus = beat_style(dur, int(vid), tl.get("style", "phonk"))
    he0 = int(tl["hookEnd"] * SR)
    if not tl.get("song"): mus[:he0] = np.stack([lp(mus[:he0, 0], 500), lp(mus[:he0, 1], 500)], 1) * 1.6     # intro filtrado, luego cae el beat
    for a, b2 in tl.get("mgaps", []):                                                     # silencio antes de un golpe
        i0, i1 = int(a * SR), int(b2 * SR); mus[i0:i1] *= 0.05
    # entrada: el beat cae después del gancho con un corte seco; ducking bajo la voz
    act = np.sqrt(np.maximum(lp(v * v, 6), 0)); duck = 0.55 + 0.45 * (1 - np.clip(act / 0.07, 0, 1))
    he = int(tl["hookEnd"] * SR); pre = np.ones(n); pre[:he] = 0.55
    fo = int(0.8 * SR); pre[-fo:] *= np.linspace(1, 0.4, fo)
    if tl.get("song"):
        pre[:he] = 1.0
        duck = 0.42 + 0.58 * (1 - np.clip(act / 0.07, 0, 1))
        mus = mus * (duck * pre)[:, None] * 0.30
    else:
        mus = mus * (duck * pre)[:, None] * 0.30
    fx = np.zeros((n, 2)); rng = np.random.default_rng(int(vid))
    for ev in tl["sfx"]:
        k = ev["k"]; x = make_sfx(k, rng, ev.get("v", 0))
        add(fx, x, ev["t"], G.get(k, 0.2) * (0.85 + 0.3 * rng.random()), pan=(rng.random() - 0.5) * 0.5 if x.ndim == 1 else 0)
    am = np.zeros(n) if tl.get("v7") else amb_track(tl, n, np.random.default_rng(int(vid) + 7)) * (10 ** (-31 / 20))     # ambiente de la escena, ~13 dB bajo la voz
    # pequeña sala en la voz para que no suene 'en el vacío'
    ir = np.random.default_rng(3).standard_normal(int(0.25 * SR)) * np.exp(-np.arange(int(0.25 * SR)) / (0.05 * SR)); ir = lp(ir, 5000)
    room = signal.fftconvolve(v, ir)[:n]; room = room / (np.sqrt(np.mean(room ** 2)) + 1e-9) * np.sqrt(np.mean(v ** 2)) * 0.12
    v = v + room
    ga = game_audio(tl, n) if tl.get("v7") else None
    if ga is not None:
        gd = 0.35 + 0.65 * (1 - np.clip(act / 0.07, 0, 1))
        ga = ga * gd[:, None]
        am = am * 0.3
    mix = mus + fx * 0.75 + v[:, None] + np.stack([am, np.roll(am, 240)], 1) + (ga if ga is not None else 0)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1) * 0.95
    sf.write(f"{d}/audio.wav", mix.astype("float32"), SR)
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    print(f"{vid}: voz {db(v):.1f} dB  beat {db(mus):.1f} dB  efectos {db(fx):.1f} dB  pico {np.abs(mix).max():.2f}")

if __name__ == "__main__":
    for vid in sys.argv[1:]: build(vid)
