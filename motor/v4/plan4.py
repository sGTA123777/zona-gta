# -*- coding: utf-8 -*-
"""words.json + content4 -> build4/<id>/timeline.json (tomas, subtítulos, palabras clave, golpes, efectos)."""
import sys, os, re, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content4
from align4 import norm

TRS = ["whip", "glitch", "zoom", "whip", "flash", "glitch", "zoom"]
MONEY = {"dolares", "millones", "pesos", "dinero", "mil"}

def find(words, phrase, start=0):
    toks = [norm(x) for x in phrase.split() if norm(x)]
    nw = [norm(w["w"]) for w in words]
    for i in range(start, len(nw) - len(toks) + 1):
        if nw[i:i + len(toks)] == toks: return i
    raise SystemExit(f"ancla no encontrada: {phrase!r} desde {start}")

def captions(words, kwidx):
    caps = []; cur = []
    def flush():
        if cur: caps.append(cur.copy()); cur.clear()
    for i, w in enumerate(words):
        txt = w["w"]
        clean = re.sub(r"[¿¡]", "", txt)
        if not cur and caps and len(re.sub(r"\W", "", clean)) <= 2 and len(caps[-1]) < 4 and re.search(r"[.?!…:,]$", txt):
            caps[-1].append({"w": clean.rstrip(",:;.").replace("…", ""), "t": w["t"], "k": i in kwidx}); continue
        if cur and (len(cur) >= 3 or sum(len(c["w"]) for c in cur) + len(clean) > 15): flush()
        cur.append({"w": clean.rstrip(",:;.").replace("…", ""), "t": w["t"], "k": i in kwidx or bool(re.search(r"\d", clean))})
        if re.search(r"[.?!…:,]$", txt): flush()
    flush()
    merged = []
    for g in caps:
        if merged and len(g) == 1 and len(re.sub(r"\W", "", g[0]["w"])) <= 2 and len(merged[-1]) < 4: merged[-1].append(g[0])
        else: merged.append(g)
    caps = merged
    out = []
    for j, g in enumerate(caps):
        end = caps[j + 1][0]["t"] if j + 1 < len(caps) else words[-1]["e"] + 0.3
        out.append({"t": g[0]["t"], "end": round(end, 3), "words": g})
    return out

def plan(vid):
    v = content4.V[vid]; d = f"build4/{vid}"
    W = json.load(open(f"{d}/words.json")); words = W["words"]; dur = W["duration"]
    # tomas
    anchors = []; pos = 0
    for sh in v["shots"]:
        ph, img, mv = sh[:3]; lay = sh[3] if len(sh) > 3 else None
        i = find(words, ph, pos); pos = i + 1; anchors.append((max(0.0, words[i]["t"] - 0.04), img, mv, lay))
    hook_end = anchors[0][0]
    shots = []
    mont = v["montage"]; n = len(mont)
    seg = [0.0] + [hook_end * (0.32 + 0.30 * k) for k in range(n - 1)] + [hook_end]   # cortes rápidos en el gancho
    for k, img in enumerate(mont):
        shots.append(dict(t0=seg[k], t1=seg[k + 1], img=img, move="punch" if k == 0 else ("push" if k % 2 else "right"), tr="cut" if k == 0 else "flash"))
    import random; rnd = random.Random((int(vid) if str(vid).isdigit() else __import__("zlib").crc32(str(vid).encode()) % 1000) * 7 + 1)
    for j, (t0, img, mv, lay) in enumerate(anchors):
        t1 = anchors[j + 1][0] if j + 1 < len(anchors) else dur
        tr = "cut" if (mv == "punch" or lay) else rnd.choice(TRS)
        if v.get("v5"):
            tr = "flash" if (j % 5 == 4 and not lay) else "cut"
            if not lay and mv not in ("punch", "hold"): mv = rnd.choice(["snap", "snap", "push"])
        shots.append(dict(t0=t0, t1=t1, img=img, move=mv, tr=tr, lay=lay))
    for s in shots:
        if s["img"].startswith("clip:"):
            nm = s["img"][5:]; cs = 0.0
            sp = 1.0
            if "~" in nm: nm, sp = nm.split("~"); sp = float(sp)
            if "@" in nm: nm, cs = nm.split("@"); cs = float(cs)
            s["clip"], s["cs"], s["img"] = nm, cs, None; fx, fy = .5, .5
            if sp != 1.0: s["speed"] = sp
        else: fx, fy = content4.FX[s["img"]]
        s["fx"], s["fy"] = fx, fy; s["t0"] = round(s["t0"], 3); s["t1"] = round(s["t1"], 3)
    # palabras clave
    kws = []; pos = 0; kwidx = set()
    for item in v["kw"]:
        ph, text, c = item[:3]; ex = item[3] if len(item) > 3 else {}
        i = find(words, ph, pos); pos = i + 1
        for j in range(i, i + len(ph.split())): kwidx.add(j)
        t = round(words[i]["t"], 3)
        if ex.get("list") and kws and kws[-1].get("list") == ex["list"]:
            kws[-1]["items"].append(dict(text=text, c=c, t=t)); continue
        if ex.get("list"): kws.append(dict(list=ex["list"], t=t, items=[dict(text=text, c=c, t=t)]))
        else: kws.append(dict(text=text, c=c, t=t))
    blockers = [s_["t0"] for s_ in shots if s_.get("lay") and s_["lay"]["k"] in (("news", "count", "slam", "split", "card", "anim", "shot") if v.get("v7") else ("news", "count", "slam", "split", "card", "focus", "anim", "shot"))]
    for j, k in enumerate(kws):
        last = k["items"][-1]["t"] if k.get("list") else k["t"]
        nxt = kws[j + 1]["t"] if j + 1 < len(kws) else dur
        nxt = min([nxt] + [b for b in blockers if b > k["t"] + 0.05])
        k["end"] = round(min(nxt - 0.02, last + (2.4 if k.get("list") else 2.0)), 3)
        if v.get("v7"):
            nb = [s_["t0"] for s_ in shots if s_["t0"] > last + 0.5]
            k["end"] = round(min([k["end"], last + 1.4] + ([nb[0] - 0.02] if nb and not k.get("list") else [])), 3)
    # golpes de cámara
    hits = []
    for i, w in enumerate(words):
        if norm(w["w"]) in v["hits"] and (not hits or w["t"] - hits[-1] > 0.7): hits.append(round(w["t"], 3))
    caps = captions(words, kwidx)
    # efectos de sonido
    rnd = random.Random((int(vid) if str(vid).isdigit() else __import__("zlib").crc32(str(vid).encode()) % 1000) * 13 + 5)
    sfx = [{"k": "boom", "t": 0.0, "v": rnd.randrange(3)}, {"k": "riser", "t": max(0, hook_end - 0.9), "v": rnd.randrange(3)}]
    mgaps = []
    LAYS = {"anim": "pop", "split": "swish", "card": "swoosh_up", "shot": "swoosh_up", "focus": "zoom_in", "slam": "bass_drop", "count": "counter", "news": "typing", "cine": "boom_soft", "mono": "scratch"}
    for j, s_ in enumerate(shots[1:], 1):
        L = s_.get("lay")
        if L:
            sfx.append({"k": LAYS[L["k"]], "t": s_["t0"], "v": rnd.randrange(3)})
            if L["k"] == "slam": mgaps.append([round(s_["t0"] - 0.35, 3), round(s_["t0"], 3)])
            if L["k"] == "focus": sfx.append({"k": "ding", "t": round(s_["t0"] + 0.55, 3), "v": rnd.randrange(3)})
            if L["k"] == "count": sfx.append({"k": "ding", "t": round(s_["t0"] + 0.9, 3), "v": rnd.randrange(3)})
            continue
        if j <= len(mont) - 1 or rnd.random() < (0.85 if v.get('v5') else 0.62):
            k = {"whip": "whip", "glitch": "glitch", "zoom": "whoosh", "flash": "camera", "cut": "thump"}[s_["tr"]]
            if v.get("v5"): k = "whoosh" if s_["tr"] == "cut" else "swish"
            sfx.append({"k": k, "t": round(max(0, s_["t0"] - (0.12 if s_["tr"] in ("whip", "zoom") else 0)), 3), "v": rnd.randrange(3)})
    for k in kws:
        sfx.append({"k": "impact", "t": k["t"], "v": rnd.randrange(3)})
        if k.get("list"):
            for it in k["items"][1:]: sfx.append({"k": "pop", "t": it["t"], "v": rnd.randrange(3)})
    for h in hits:
        if not any(abs(e["t"] - h) < 0.25 for e in sfx): sfx.append({"k": "thump", "t": h, "v": rnd.randrange(3)})
    for w in words:
        if norm(w["w"]) in MONEY: sfx.append({"k": "cash", "t": w["t"], "v": 0})
    sfx.sort(key=lambda e: e["t"])
    if v.get("v6"): sfx = [e for e in sfx if e["k"] in ("impact", "ding", "counter", "cash")]
    if v.get("v7"):
        strong = [k["t"] for k in kws if not k.get("list") and k.get("c") in ("yellow", "cyan", "green")]
        sfx = []
    tl = dict(id=vid, slug=v["slug"], tone=v.get("tone", "#22E3D6"), duration=dur, hook=v["hook"], hookEnd=round(hook_end + 0.25, 3),
              shots=shots, kw=kws, hits=hits, caps=caps, sfx=sfx, mgaps=mgaps, banner=v.get('banner'), parallax=not v.get('v5'), style=v.get('music', ['phonk','trap','synth'][(int(vid) if str(vid).isdigit() else __import__("zlib").crc32(str(vid).encode()) % 1000) % 3]), song=v.get('song'), song_start=v.get('song_start', 0.0), v6=bool(v.get('v6')), v7=bool(v.get('v7')))
    json.dump(tl, open(f"{d}/timeline.json", "w"), ensure_ascii=False, indent=1)
    print(f"{vid}: {dur:.1f}s  tomas={len(shots)} (cada {dur/len(shots):.1f}s)  claves={len(kws)}  golpes={len(hits)}  subtítulos={len(caps)}")

if __name__ == "__main__":
    for vid in sys.argv[1:]: plan(vid)
