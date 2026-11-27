# Hoja de cuadros de cada fuente (cada 1 s) para escoger los cortes:  python ver.py <id>
import sys, os, json, subprocess, pathlib
vid = sys.argv[1]; R = pathlib.Path(__file__).resolve().parent.parent
job = json.load(open(R / "jobs" / vid / "job.json", encoding="utf-8")); out = R / "out"; out.mkdir(exist_ok=True)
os.makedirs("/tmp/src", exist_ok=True)
for nombre, url in job["fuentes"].items():
    dst = f"/tmp/src/{nombre}"
    if "storage.googleapis.com" in url or url.endswith(".mp4"): subprocess.run(["curl", "-sSfL", "-o", dst, url], check=True)
    else: subprocess.run(["yt-dlp", "-q", "-f", "bv*+ba/b", "--merge-output-format", "mp4", "-o", dst, url], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip() or 0)
    base = nombre.rsplit(".", 1)[0]; paso = 1 if dur <= 120 else 2
    vf = f"fps=1/{paso},scale=320:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{{eif\\:t\\:d}}s':x=6:y=6:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.6"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-vf", vf + ",tile=6x5", f"{out}/hoja_{base}_%02d.jpg"], check=True)
    print(nombre, round(dur, 1), "s")
