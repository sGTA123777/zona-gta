# Shorts de GTA 6 que más pegan AHORA en cualquier idioma -> jobs/competencia.md
import json, subprocess, datetime, urllib.parse, sys
HOY = datetime.date.today()
Q = {"en": ["gta 6", "gta 6 secret", "gta 6 easter egg", "gta 6 funny", "gta 6 tips", "gta 6 money", "gta 6 details", "gta 6 physics", "gta 6 npc", "gta 6 glitch", "gta 6 free car"],
     "pt": ["gta 6 segredo", "gta 6 curiosidades"], "es": ["gta 6 secretos", "gta 6 truco", "gta 6 detalles"],
     "fr": ["gta 6 secret astuce"], "de": ["gta 6 geheimnis"], "it": ["gta 6 segreti"], "ru": ["гта 6"], "ar": ["قراند 6"]}
SP = {"shorts": "EgIQCQ%253D%253D"}
def buscar(q, sp):
    out = []
    for modo in ("ytsearch50", "ytsearchdate50"):
        r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", f"{modo}:{q} #shorts"], capture_output=True, text=True)
        try: ents = json.loads(r.stdout).get("entries", []) or []
        except Exception: print("fallo", q, r.stderr[-200:]); continue
        for e in ents:
            if e and ("/shorts/" in (e.get("url") or "") or 0 < (e.get("duration") or 999) <= 75):
                e["_reciente"] = modo.startswith("ytsearchdate"); out.append(e)
    return out
vis = {}
for lang, qs in Q.items():
    for q in qs:
        for e in buscar(q, SP["shorts"]):
            if e and e.get("id"):
                vis.setdefault(e["id"], dict(id=e["id"], vistas=e.get("view_count") or 0, titulo=e.get("title"), canal=e.get("channel") or e.get("uploader"), canal_id=e.get("channel_id"), lang=lang, reciente=False))
                if e.get("_reciente"): vis[e["id"]]["reciente"] = True
print("encontrados", len(vis))
OFICIAL = ("Rockstar", "IGN", "PlayStation", "Netflix", "Xbox")
top = [v for v in sorted(vis.values(), key=lambda x: -x["vistas"]) if not any(o in (v["canal"] or "") for o in OFICIAL)][:70]
rec = [v for v in sorted(vis.values(), key=lambda x: -x["vistas"]) if v["reciente"] and not any(o in (v["canal"] or "") for o in OFICIAL)][:40]
fmt = lambda v: f"{v['vistas']:,} | {v['lang']} | {v['canal']} | {v['titulo']} | {v['id']}"
L = [f"# Shorts de GTA 6 que más pegan (todos los idiomas, sin canales oficiales) — {HOY}", "",
     "## RECIENTES (de las búsquedas por fecha más nueva: lo que está pegando AHORA)", "vistas | idioma | canal | título | id"] + [fmt(v) for v in rec] + \
    ["", "## TOP de siempre", "vistas | idioma | canal | título | id"] + [fmt(v) for v in top]
open("jobs/competencia.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
