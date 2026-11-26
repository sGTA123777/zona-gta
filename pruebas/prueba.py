import subprocess, json, time, os, pathlib
out = pathlib.Path("out")
cfg = json.load(open("pruebas/prueba.json"))
def run(c, t=300):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
    return r.returncode, (r.stdout + r.stderr)[-1500:]

print("== 1. Bajar video de vidIQ (link de storage) ==")
t = time.time()
code, log = run(f'curl -sL -o out_vidiq.mp4 "{cfg["vidiq_url"]}" && ffprobe -v error -show_entries stream=width,height -of csv=p=0 out_vidiq.mp4')
print("codigo", code, "seg", round(time.time()-t,1), log)

print("== 2. Bajar clips de X con yt-dlp ==")
for u in cfg["x_urls"]:
    code, log = run(f'yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o "x_%(id)s.%(ext)s" "{u}"', 180)
    print(u, "codigo", code); print(log[-600:])

print("== 3. Bajar de YouTube directo (para comparar) ==")
code, log = run(f'yt-dlp -f "bv*[height<=1080]+ba/b" -o yt.mp4 "{cfg["yt_url"]}"', 180)
print("codigo", code); print(log[-400:])

print("== 4. Edicion: recorte vertical + texto con navegador ==")
code, log = run('ffmpeg -y -v error -ss 20 -t 4 -i out_vidiq.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -preset veryfast -an out/muestra.mp4 && ls -la out/muestra.mp4')
print("ffmpeg codigo", code, log)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 540, "height": 960})
    pg.set_content('<body style="margin:0;background:#12151C;color:#FFE14D;font:900 64px sans-serif;display:grid;place-items:center;height:100vh">PRUEBA ZONA GTA</body>')
    pg.screenshot(path="out/cuadro.png"); b.close()
print("playwright ok", os.path.exists("out/cuadro.png"))
