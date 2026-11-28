# Busca los Shorts de GTA 6 con más vistas (de otros canales) y escribe jobs/competencia.md
import json, subprocess, sys, datetime
Q = ["gta 6 shorts", "gta 6 secretos shorts", "gta 6 easter egg shorts", "gta 6 truco shorts", "gta 6 español shorts",
     "gta 6 rockstar escondió", "gta 6 secret", "gta 6 easter egg", "gta 6 hidden details", "gta 6 tips tricks",
     "gta 6 funny moments", "gta 6 cosas que no sabías", "gta 6 detalles increíbles", "gta 6 physics", "gta 6 npc"]
vis = {}
for q in Q:
    for modo in ("ytsearch40", "ytsearchdate40"):
        r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", f"{modo}:{q}"], capture_output=True, text=True)
        try: ents = json.loads(r.stdout).get("entries", [])
        except Exception: print("fallo", q, r.stderr[-300:]); continue
        for e in ents:
            if not e or not e.get("id"): continue
            d = e.get("duration") or 0; u = e.get("url") or ""
            if not ("/shorts/" in u or (d and d <= 180)): continue
            vis[e["id"]] = dict(id=e["id"], vistas=e.get("view_count") or 0, titulo=e.get("title"), canal=e.get("channel") or e.get("uploader"),
                                canal_id=e.get("channel_id"), dur=d, q=q)
top = sorted(vis.values(), key=lambda x: -x["vistas"])[:60]
# suscriptores de los canales que más aparecen
canales = {}
for v in top: canales.setdefault(v["canal_id"], []).append(v)
subs = {}
for cid in list(canales)[:25]:
    if not cid: continue
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "--playlist-items", "1", f"https://www.youtube.com/channel/{cid}/shorts"], capture_output=True, text=True)
    try: subs[cid] = json.loads(r.stdout).get("channel_follower_count")
    except Exception: subs[cid] = None
L = [f"# Shorts de GTA 6 con más vistas (otros canales) — {datetime.date.today()}", "", "vistas | duración | canal (subs) | título | id"]
for v in top:
    L.append(f"{v['vistas']:,} | {int(v['dur'] or 0)}s | {v['canal']} ({subs.get(v['canal_id']) or '?'}) | {v['titulo']} | {v['id']}")
open("jobs/competencia.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[:70]))
