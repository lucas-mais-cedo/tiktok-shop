"""Confere a pronúncia: transcreve cada fala (.wav) com o Whisper local e compara com o texto do roteiro.

Uso: python -I check_asr.py <pasta_falas> [roteiro.json]
Saída: uma linha por fala. "REVISAR" aparece quando a transcrição difere muito do texto.
"""
import difflib
import glob
import json
import os
import re
import sys
import unicodedata

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.stdout.reconfigure(encoding="utf-8")

from faster_whisper import WhisperModel  # noqa: E402


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def main(falas_dir, roteiro=None):
    textos = {}
    if roteiro:
        with open(roteiro, encoding="utf-8") as f:
            textos = {x["id"]: x.get("texto_legivel", x["texto"]) for x in json.load(f)["falas"]}
    m = WhisperModel("base", device="cpu", compute_type="int8")
    ruins = 0
    for p in sorted(glob.glob(os.path.join(falas_dir, "*.wav"))):
        fid = os.path.splitext(os.path.basename(p))[0]
        segs, _ = m.transcribe(p, language="pt", beam_size=5)
        ouvido = " ".join(s.text.strip() for s in segs)
        flag = ""
        if fid in textos:
            r = difflib.SequenceMatcher(None, norm(textos[fid]), norm(ouvido)).ratio()
            if r < 0.6:
                flag = f"  <-- REVISAR (semelhança {r:.2f})"
                ruins += 1
        print(f"{fid:14s} -> {ouvido}{flag}")
    if ruins:
        print(f"\n{ruins} fala(s) para revisar. Veja a tabela de pronúncia em references/pipeline.md.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
