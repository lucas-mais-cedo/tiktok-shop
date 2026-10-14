"""Gera a narração (uma fala por arquivo) com Kokoro, 100% local.

Uso: M:\\jarvis\\.venv\\Scripts\\python.exe -I tts.py <narracao.json> <pasta_saida>

Motor: usa o pacote `kokoro` (PC, venv do Jarvis). Se ele não estiver instalado, usa `kokoro-onnx`
com os arquivos kokoro-v1.0.onnx e voices-v1.0.bin da pasta indicada em KOKORO_ONNX_DIR (nuvem).
"""
import json
import os
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")

import numpy as np
import soundfile as sf

SR = 24000
sys.stdout.reconfigure(encoding="utf-8")


def motor_kpipeline(voz):
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
    voice = pipe.load_voice(voz)

    def falar(texto, speed):
        chunks, phon = [], []
        for res in pipe(texto, voice=voice, speed=speed, split_pattern=None):
            chunks.append(np.asarray(res.audio, dtype=np.float32))
            phon.append(res.phonemes)
        return np.concatenate(chunks), " ".join(phon)
    return falar


def motor_onnx(voz):
    from kokoro_onnx import Kokoro
    d = os.environ["KOKORO_ONNX_DIR"]
    k = Kokoro(os.path.join(d, "kokoro-v1.0.onnx"), os.path.join(d, "voices-v1.0.bin"))

    def falar(texto, speed):
        audio, sr = k.create(texto, voice=voz, speed=speed, lang="pt-br")
        assert sr == SR
        return np.asarray(audio, dtype=np.float32), "(onnx)"
    return falar


def main(cfg_path, out_dir):
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    try:
        falar = motor_kpipeline(cfg["voz"])
    except ImportError:
        falar = motor_onnx(cfg["voz"])
    report = []
    for fala in cfg["falas"]:
        speed = fala.get("velocidade", cfg["velocidade"])
        audio, phon = falar(fala["texto"], speed)
        # corta silêncio no começo/fim (limiar baixo para não comer consoantes)
        idx = np.where(np.abs(audio) > 0.01)[0]
        if len(idx):
            a, b = max(idx[0] - int(0.02 * SR), 0), min(idx[-1] + int(0.06 * SR), len(audio))
            audio = audio[a:b]
        path = os.path.join(out_dir, fala["id"] + ".wav")
        sf.write(path, audio, SR, subtype="PCM_16")
        report.append({"id": fala["id"], "dur": round(len(audio) / SR, 2), "fonemas": phon})
    for r in report:
        print(f'{r["id"]:12s} {r["dur"]:5.2f}s  {r["fonemas"]}')
    print("TOTAL fala:", round(sum(r["dur"] for r in report), 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
