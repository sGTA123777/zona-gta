# Clips del trabajo actual (ZG_JOB): jobs/<id>/job.json -> "clips": {nombre: [archivo, inicio, centro_x, zoom]}
import subprocess, os, sys, json
from concurrent.futures import ThreadPoolExecutor
S = "src_in/"
_j = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "jobs", os.environ["ZG_JOB"], "job.json"), encoding="utf-8"))
C = {k: tuple(v) for k, v in _j["clips"].items()}
LIMPIO = set(_j.get("audio_juego", []))   # fuentes sin música encima (se usa su audio bajito)
def run(name):
    src, st, cx, z = C[name]; d = f"clips/{name}"; os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    vf = (f"fps=30,scale=-2:{int(1920*z)}:flags=lanczos,crop=1080:1920:'max(0,min(iw-1080,iw*{cx}-540))':'(ih-1920)/2',"
          f"tpad=stop_mode=clone:stop_duration=9,eq=contrast=1.04:saturation=1.06")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(st), "-i", S + src, "-t", "9", "-vf", vf, "-frames:v", "270", "-q:v", "2", f"{d}/f%04d.jpg"], check=True)
    print(name, len(os.listdir(d)))
if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex: list(ex.map(run, sys.argv[1:] or list(C)))
