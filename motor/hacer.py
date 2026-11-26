# Hace un Short completo en GitHub Actions:  python hacer.py <id>
import sys, os, json, re, subprocess, base64, time, pathlib, requests
vid = sys.argv[1]; os.environ["ZG_JOB"] = vid
AQUI = pathlib.Path(__file__).resolve().parent; os.chdir(AQUI)
job = json.load(open(AQUI.parent / "jobs" / vid / "job.json", encoding="utf-8"))
OUT = AQUI.parent / "out"; OUT.mkdir(exist_ok=True)
def sh(c): print("+", c[:160], flush=True); subprocess.run(c, shell=True, check=True)

# 1) Fuentes: links de vidIQ (storage) o de X/otros con yt-dlp
os.makedirs("src_in", exist_ok=True)
for nombre, url in job["fuentes"].items():
    dst = f"src_in/{nombre}"
    if os.path.exists(dst): continue
    if "storage.googleapis.com" in url or url.endswith(".mp4"):
        sh(f'curl -sSfL -o "{dst}" "{url}"')
    else:
        sh(f'yt-dlp -q -f "bv*[height<=2160]+ba/b" --merge-output-format mp4 -o "{dst}" "{url}"')
    sh(f'ffprobe -v error -show_entries stream=width,height -of csv=p=0 "{dst}"')

# 2) Canción (opcional): link de vidIQ de un video de YouTube -> mp3
if job.get("cancion_url"):
    os.makedirs("musica", exist_ok=True)
    sh(f'curl -sSfL -o /tmp/cancion.mp4 "{job["cancion_url"]}" && ffmpeg -v error -y -i /tmp/cancion.mp4 -vn -ac 2 -ar 48000 -b:a 192k musica/{vid}.mp3')
    job["song"] = f"musica/{vid}.mp3"
    p = AQUI.parent / "jobs" / vid / "job.json"; j2 = json.load(open(p, encoding="utf-8")); j2["song"] = job["song"]; json.dump(j2, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 3) Voz con Gemini TTS
os.makedirs("voces_ext", exist_ok=True)
key = os.environ["GEMINI_KEY"].strip()
body = {"model": "gemini-3.8-flash-tts",
        "input": [{"type": "user_input", "content": [{"type": "text", "text": job["texto"], "annotations": [{"type": "speech_metadata",
                   "style": "Native Mexican Spanish speaker, energetic young gaming YouTuber narrating a viral Short: fast-paced, confident, conversational"}]}]}],
        "response_format": {"type": "audio"},
        "generation_config": {"temperature": 1.75, "speech_config": [{"voice": "Sadaltager"}]}}
def buscar(o):
    if isinstance(o, dict):
        d = o.get("data")
        if isinstance(d, str) and len(d) > 1000: return d
        o = list(o.values())
    if isinstance(o, list):
        for x in o:
            v = buscar(x)
            if v: return v
data = None
for intento in range(4):
    r = requests.post("https://generativelanguage.googleapis.com/v1beta/interactions", headers={"x-goog-api-key": key, "Content-Type": "application/json"}, data=json.dumps(body), timeout=300)
    if r.status_code == 200:
        data = buscar(r.json())
        if data: break
    print("voz: intento", intento, r.status_code, r.text[:300], flush=True)
    if "temperature" in r.text: body["generation_config"].pop("temperature", None)
    time.sleep(20)
if not data: raise SystemExit("No se pudo generar la voz")
raw = base64.b64decode(data); open("/tmp/voz.bin", "wb").write(raw)
sh(f"ffmpeg -v error -y -i /tmp/voz.bin -ac 1 -ar 24000 voces_ext/{vid}.wav || ffmpeg -v error -y -f s16le -ar 24000 -ac 1 -i /tmp/voz.bin voces_ext/{vid}.wav")
sh(f"cp voces_ext/{vid}.wav {OUT}/voz.wav")

# 4) Alinear, clips, plan, video
sh(f"python v4/align4.py {vid}")
sh("python v4/mkclips21.py")
sh(f"python v4/plan4.py {vid}")
sh(f"python v4/make4.py {vid}")
final = next(pathlib.Path("out/v4").glob(f"ZONA_GTA_{vid}_*.mp4"))
sh(f'cp "{final}" {OUT}/short.mp4')
tl = json.load(open(f"build4/{vid}/timeline.json"))
dur = tl["duration"]; ts = [0.3, 1.2] + [round(s["t0"] + 0.4, 2) for s in tl["shots"]][:10] + [round(dur - 0.5, 2)]
for i, t in enumerate(ts):
    subprocess.run(f"ffmpeg -v error -y -ss {t} -i {OUT}/short.mp4 -frames:v 1 -vf scale=540:-2 -q:v 3 {OUT}/cuadro_{i:02d}_{t:05.2f}.jpg", shell=True)
json.dump({"id": vid, "duracion": dur, "escuchado": json.load(open(f"build4/{vid}/words.json")).get("heard")}, open(OUT / "info.json", "w"), ensure_ascii=False, indent=1)
print("LISTO", final, round(final.stat().st_size / 1e6, 1), "MB")
