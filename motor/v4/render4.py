# -*- coding: utf-8 -*-
"""python3 v4/render4.py frames <id> t1 t2 ...  |  python3 v4/render4.py video <id>"""
import sys, os, json, base64, subprocess, time
from playwright.sync_api import sync_playwright
W, H, FPS = 1080, 1920, 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "60", "-bf", "2"]
CHUNK = 4.0

def open_page(p, vid):
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files", "--force-color-profile=srgb", "--hide-scrollbars", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    pg.goto("file://" + ROOT + "/player/v4.html")
    pg.evaluate("""async()=>{for(const f of ['900 80px Mont','800 40px Mont','900 80px MontI','400 80px Bebas'])await document.fonts.load(f,'ÁÉÑ¿a1');await document.fonts.ready}""")
    tl = json.load(open(f"{ROOT}/build4/{vid}/timeline.json"))
    pg.evaluate("tl=>build(tl)", tl)
    pg.evaluate("Promise.all([...document.images].map(i=>i.decode().catch(()=>0)))")
    pg.evaluate("async()=>{await window.ready}")
    return b, pg, tl

def frames(vid, times):
    with sync_playwright() as p:
        b, pg, tl = open_page(p, vid)
        os.makedirs(f"{ROOT}/build4/{vid}/stills", exist_ok=True)
        for t in times:
            pg.evaluate("t=>seek(t)", float(t))
            pg.screenshot(path=f"{ROOT}/build4/{vid}/stills/t{float(t):06.2f}.jpg", type="jpeg", quality=88)
        b.close()

def video(vid):
    t_all = time.time()
    out = f"{ROOT}/build4/{vid}/chunks"; os.makedirs(out, exist_ok=True)
    tl = json.load(open(f"{ROOT}/build4/{vid}/timeline.json"))
    nframes = int(round(tl["duration"] * FPS)); step = int(CHUNK * FPS)
    bounds = list(range(0, nframes, step)) + [nframes]; files = []
    with sync_playwright() as p:
        b, pg, tl = open_page(p, vid)
        cdp = pg.context.new_cdp_session(pg)
        for ci in range(len(bounds) - 1):
            f0, f1 = bounds[ci], bounds[ci + 1]; final = f"{out}/c{ci:02d}.mp4"; files.append(final)
            if os.path.exists(final): continue
            tmp = f"{out}/c{ci:02d}.part.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-"] + ENC + [tmp], stdin=subprocess.PIPE)
            for f in range(f0, f1):
                pg.evaluate("t=>seek(t)", f / FPS)
                r = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": 96, "optimizeForSpeed": False})
                ff.stdin.write(base64.b64decode(r["data"]))
            ff.stdin.close()
            if ff.wait() != 0: raise SystemExit(f"ffmpeg falló en el tramo {ci}")
            os.replace(tmp, final)
        b.close()
    with open(f"{out}/list.txt", "w") as f:
        for x in files: f.write(f"file '{x}'\n")
    silent = f"{ROOT}/build4/{vid}/video_silent.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", silent + ".part.mp4"])
    os.replace(silent + ".part.mp4", silent)
    print(f"{vid}: {nframes} fotogramas en {time.time()-t_all:.0f}s")

if __name__ == "__main__":
    mode, vid = sys.argv[1], sys.argv[2]
    if mode == "frames": frames(vid, sys.argv[3:])
    else: video(vid)
