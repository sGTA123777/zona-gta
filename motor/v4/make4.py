# -*- coding: utf-8 -*-
"""python3 v4/make4.py <id> ...  -> out/v4/ZONA_GTA_<id>_<slug>.mp4"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render4, mix4
os.makedirs("out/v4", exist_ok=True)
for vid in sys.argv[1:]:
    tl = json.load(open(f"build4/{vid}/timeline.json"))
    render4.video(vid); mix4.build(vid)
    out = f"out/v4/ZONA_GTA_{vid}_{tl['slug']}.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"build4/{vid}/video_silent.mp4", "-i", f"build4/{vid}/audio.wav", "-map", "0:v", "-map", "1:a",
                           "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out + ".part.mp4"])
    os.replace(out + ".part.mp4", out)
    print("OK", out, round(os.path.getsize(out) / 1e6, 1), "MB")
