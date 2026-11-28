# Shorts de GTA 6 que más pegan AHORA en cualquier idioma -> jobs/competencia.md
import json, subprocess, datetime, urllib.parse, sys
HOY = datetime.date.today()
Q = {"en": ["gta 6", "gta 6 secret", "gta 6 easter egg", "gta 6 funny", "gta 6 tips", "gta 6 money", "gta 6 details", "gta 6 physics", "gta 6 npc", "gta 6 glitch", "gta 6 free car"],
     "pt": ["gta 6 segredo", "gta 6 curiosidades"], "es": ["gta 6 secretos", "gta 6 truco", "gta 6 detalles"],
     "fr": ["gta 6 secret astuce"], "de": ["gta 6 geheimnis"], "it": ["gta 6 segreti"], "ru": ["гта 6"], "ar": ["قراند 6"]}
SP = {"shorts": "EgIQCQ%253D%253D"}
def buscar(q, sp):
    u = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=" + sp
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", "60", u], capture_output=True, text=True)
    try: return json.loads(r.stdout).get("entries", []) or []
    except Exception: print("fallo", q, r.stderr[-200:]); return []
vis = {}
for lang, qs in Q.items():
    for q in qs:
        for e in buscar(q, SP["shorts"]):
            if e and e.get("id"):
                vis.setdefault(e["id"], dict(id=e["id"], vistas=e.get("view_count") or 0, titulo=e.get("title"), canal=e.get("channel") or e.get("uploader"), canal_id=e.get("channel_id"), lang=lang))
print("encontrados", len(vis))
OFICIAL = ("Rockstar", "IGN", "PlayStation", "Netflix", "Xbox")
top = [v for v in sorted(vis.values(), key=lambda x: -x["vistas"]) if not any(o in (v["canal"] or "") for o in OFICIAL)][:70]
for v in top:  # fecha de subida (para saber qué pega AHORA)
    r = subprocess.run(["yt-dlp", "-J", "--skip-download", "--no-warnings", f"https://www.youtube.com/shorts/{v['id']}"], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout); d = j.get("upload_date"); v["fecha"] = d; v["vistas"] = j.get("view_count") or v["vistas"]
        v["subs"] = j.get("channel_follower_count"); v["dur"] = j.get("duration")
        dias = max(1, (HOY - datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))).days) if d else None
        v["por_dia"] = int(v["vistas"] / dias) if dias else None
    except Exception: v["fecha"] = None; v["por_dia"] = None
L = [f"# Shorts de GTA 6 que más pegan (todos los idiomas, sin canales oficiales) — {HOY}", "",
     "## Por vistas por día (lo que pega AHORA)", "vistas/día | vistas | subido | dur | idioma | canal (subs) | título | id"]
fmt = lambda v: f"{v.get('por_dia') or '?'} | {v['vistas']:,} | {v.get('fecha') or '?'} | {v.get('dur') or '?'}s | {v['lang']} | {v['canal']} ({v.get('subs') or '?'}) | {v['titulo']} | {v['id']}"
L += [fmt(v) for v in sorted(top, key=lambda x: -(x.get("por_dia") or 0))]
open("jobs/competencia.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
