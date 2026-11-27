import subprocess, json
cfg = json.load(open("pruebas/prueba.json"))
def run(c, t=240):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t); return r.returncode, (r.stdout + r.stderr)[-700:]
for i, u in enumerate(cfg["urls"]):
    code, log = run(f'yt-dlp -f "bv*+ba/b" -S "res,fps" --merge-output-format mp4 -o "out/t{i}.%(ext)s" "{u}"')
    wh = run(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 out/t{i}.mp4')[1].strip()
    print("==", u, "codigo", code, "RES", wh); print(log[-300:])
    run(f"rm -f out/t{i}.mp4")

for u in cfg.get("canales", []):
    code, log = run(f'yt-dlp --skip-download --print "%(id)s|%(channel)s|%(uploader_id)s|%(title)s" "{u}"', 120)
    print("CANAL", log.strip()[-300:])
