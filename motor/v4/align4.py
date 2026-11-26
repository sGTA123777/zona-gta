# -*- coding: utf-8 -*-
"""Voz externa -> build4/<id>/voice.wav (silencios recortados) + words.json (palabras del guion con tiempos).
python3 v4/align4.py <id> ...   (lee voces_ext/<id>.wav y el texto de v4/content4.py)"""
import sys, os, re, json, difflib, unicodedata, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import asr, content4

MAX_GAP, KEEP_GAP = 0.26, 0.13          # pausas más largas que MAX_GAP se dejan en KEEP_GAP (corte de aire muerto)

def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)

NUM = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro", "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve", "10": "diez"}

def asr_words(tok, ts):
    out = []; cur = ""; t0 = None
    for tk, t in zip(tok, ts):
        if tk.startswith(" ") or tk.startswith("▁") or cur == "":
            if cur: out.append((cur, t0))
            cur = tk.strip(" ▁"); t0 = t
        else: cur += tk
    if cur: out.append((cur, t0))
    return [(norm(NUM.get(w, w)), t) for w, t in out if norm(w)]

def tighten(a, sr):
    """Recorta silencios largos. Devuelve audio nuevo y función de remapeo de tiempos."""
    win = int(0.01 * sr); k = len(a) // win
    env = np.sqrt((a[:k * win].reshape(k, win) ** 2).mean(1) + 1e-12)
    thr = max(np.percentile(env, 20) * 2.2, 0.006)
    quiet = env < thr
    segs = []; i = 0
    while i < k:
        if quiet[i]:
            j = i
            while j < k and quiet[j]: j += 1
            if (j - i) * 0.01 > MAX_GAP and i > 0 and j < k: segs.append((i * win, j * win))
            i = j
        else: i += 1
    # lead / tail
    nz = np.where(~quiet)[0]; start = max(0, nz[0] * win - int(0.05 * sr)); end = min(len(a), (nz[-1] + 1) * win + int(0.25 * sr))
    keep = []; cur = start
    for s, e in segs:
        if s < start or e > end: continue
        cut_from = s + int(KEEP_GAP / 2 * sr); cut_to = e - int(KEEP_GAP / 2 * sr)
        keep.append((cur, cut_from)); cur = cut_to
    keep.append((cur, end))
    pieces = []; fade = int(0.004 * sr)
    for s, e in keep:
        p = a[s:e].copy()
        if len(p) > 2 * fade: p[:fade] *= np.linspace(0, 1, fade); p[-fade:] *= np.linspace(1, 0, fade)
        pieces.append(p)
    out = np.concatenate(pieces)
    starts = np.cumsum([0] + [e - s for s, e in keep])
    def remap(t):
        x = t * sr
        for (s, e), o in zip(keep, starts):
            if x < s: return o / sr
            if x <= e: return (o + x - s) / sr
        return starts[-1] / sr
    return out, remap

def run(vid):
    v = content4.V[vid]
    a, sr = sf.read(f"voces_ext/{vid}.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    a = a * (0.089 / (np.sqrt((a[np.abs(a) > 0.01] ** 2).mean()) + 1e-9)); a = np.clip(a, -0.98, 0.98)
    a, remap = tighten(a, sr)
    text, tok, ts = asr.transcribe(a, sr); aw = asr_words(tok, ts)
    script = v["text"].split()
    sw = [norm(w) for w in script]
    idx = [i for i, w in enumerate(sw) if w]
    sm = difflib.SequenceMatcher(None, [sw[i] for i in idx], [w for w, _ in aw], autojunk=False)
    anc = {}
    for b in sm.get_matching_blocks():
        for j in range(b.size): anc[idx[b.a + j]] = aw[b.b + j][1]
    # interpolar los que faltan
    times = [None] * len(script); ks = sorted(anc)
    for i in range(len(script)):
        if i in anc: times[i] = anc[i]; continue
        prev = [k for k in ks if k < i]; nxt = [k for k in ks if k > i]
        if prev and nxt: i0, i1 = prev[-1], nxt[0]; times[i] = anc[i0] + (anc[i1] - anc[i0]) * (i - i0) / (i1 - i0)
        elif prev: times[i] = anc[prev[-1]] + 0.25 * (i - prev[-1])
        else: times[i] = max(0.0, anc[nxt[0]] - 0.25 * (nxt[0] - i))
    dur = len(a) / sr
    words = []
    for i, w in enumerate(script):
        t = max(0.0, times[i] - 0.03)
        e = (times[i + 1] - 0.03) if i + 1 < len(script) else dur - 0.2
        words.append({"w": w, "t": round(t, 3), "e": round(max(e, t + 0.08), 3)})
    d = f"build4/{vid}"; os.makedirs(d, exist_ok=True)
    sf.write(f"{d}/voice.wav", a, sr)
    json.dump({"duration": round(dur + 0.35, 3), "words": words, "heard": text}, open(f"{d}/words.json", "w"), ensure_ascii=False, indent=0)
    print(f"{vid}: {dur:.1f}s  ancladas {len(anc)}/{len(idx)} ({100*len(anc)/len(idx):.0f}%)")

if __name__ == "__main__":
    for vid in sys.argv[1:]: run(vid)
