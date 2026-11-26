import sys, numpy as np, soundfile as sf, sherpa_onnx
import os
D = os.environ.get("ASR_DIR", "/home/claude/tts/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8")
_rec = None
def rec():
    global _rec
    if _rec is None:
        _rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{D}/encoder.int8.onnx", decoder=f"{D}/decoder.int8.onnx", joiner=f"{D}/joiner.int8.onnx", tokens=f"{D}/tokens.txt", model_type="nemo_transducer", num_threads=2)
    return _rec
def transcribe(path_or_audio, sr=None):
    if isinstance(path_or_audio, str):
        a, sr = sf.read(path_or_audio, dtype="float32")
    else:
        a = path_or_audio
    if a.ndim > 1: a = a.mean(1)
    s = rec().create_stream(); s.accept_waveform(sr, a); rec().decode_stream(s)
    r = s.result
    return r.text, list(r.tokens), list(r.timestamps)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        t, tok, ts = transcribe(p)
        print(p.split("/")[-1], "=>", t)
        print("   ", [(a, round(b,2)) for a,b in zip(tok, ts)][:40])
