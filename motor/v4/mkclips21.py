# Clips del trabajo actual (ZG_JOB): jobs/<id>/job.json -> "clips": {nombre: [archivo, inicio, centro_x, zoom]}
import subprocess, os, sys, json
from concurrent.futures import ThreadPoolExecutor
S = "src_in/"
_j = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "jobs", os.environ["ZG_JOB"], "job.json"), encoding="utf-8"))
C = {k: tuple(v) for k, v in _j["clips"].items()}
ENC = _j.get("encuadre", "auto")   # auto | banda | recorte
_asp = {}
def horizontal(src):
    if src not in _asp:
        wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", S + src], capture_output=True, text=True).stdout.strip().split(",")
        _asp[src] = int(wh[0]) > int(wh[1])
    return _asp[src]
LIMPIO = set(_j.get("audio_juego", []))   # fuentes sin música encima (se usa su audio bajito)
def run(name):
    src, st, cx, z = C[name][:4]; modo = C[name][4] if len(C[name]) > 4 else ENC; d = f"clips/{name}"; os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    vf = (f"fps=30,scale=-2:{int(1920*z)}:flags=lanczos,crop=1080:1920:'max(0,min(iw-1080,iw*{cx}-540))':'(ih-1920)/2',"
          f"tpad=stop_mode=clone:stop_duration=9,eq=contrast=1.04:saturation=1.06")
    if modo == "banda" or (modo == "auto" and horizontal(src)):
        # Video horizontal: NO se agranda. Franja nítida (se reduce 1920->1440, se ven 3/4 del ancho) sobre fondo desenfocado.
        vf = (f"fps=30,split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=36:2,eq=brightness=-0.13:saturation=1.15[bg];"
              f"[b]scale={int(1440*z)}:-2:flags=lanczos,crop=1080:ih:'max(0,min(iw-1080,iw*{cx}-540))':0,eq=contrast=1.04:saturation=1.06[fg];"
              f"[bg][fg]overlay=0:(H-h)/2,tpad=stop_mode=clone:stop_duration=9")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(st), "-i", S + src, "-t", "9", "-filter_complex" if "[bg]" in vf else "-vf", vf, "-frames:v", "270", "-q:v", "2", f"{d}/f%04d.jpg"], check=True)
    print(name, len(os.listdir(d)))
if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex: list(ex.map(run, sys.argv[1:] or list(C)))
