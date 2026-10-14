"""Gera o vídeo de um post do início ao fim: voz -> conferência da pronúncia -> linha do tempo -> áudio -> imagem -> arquivos finais.

Uso (no PC, com o Python do Jarvis):
  M:\\jarvis\\.venv\\Scripts\\python.exe -I pipeline\\make_post.py <roteiro.json> <pasta_fotos> [opções]

Opções:
  --cenas <cenas.json>   cenas prontas do produto (padrão: produtos/kit-6-em-1/cenas.json)
  --saida <pasta>        onde salvar (padrão: <pasta do roteiro>/saida)
  --preview              para depois da linha do tempo e gera só a folha de prévia (rápido)
  --pular-asr            não roda a conferência de pronúncia (Whisper)
  --sem-legenda          não queima a legenda na tela (padrão: com legenda)

Saídas na pasta de saída: <id>_so-voz.mp4 (principal, com legenda na tela), <id>_com-musica.mp4, folha.png (1 quadro por segundo).
"""
import argparse
import math
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def run(*args):
    print("\n>>", os.path.basename(args[0]), *args[1:], flush=True)
    subprocess.run([sys.executable, "-I", *args], check=True)


def folha(video, png, dur):
    n = max(1, int(math.ceil(dur)))
    cols = min(n, 13)
    rows = int(math.ceil(n / cols))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
                    f"fps=1,scale=220:-1,tile={cols}x{rows}:padding=4:color=gray", "-frames:v", "1", png], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro")
    ap.add_argument("fotos")
    ap.add_argument("--cenas", default=os.path.join(RAIZ, "produtos", "kit-6-em-1", "cenas.json"))
    ap.add_argument("--saida")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--pular-asr", action="store_true")
    ap.add_argument("--sem-legenda", action="store_true")
    a = ap.parse_args()

    import json
    with open(a.roteiro, encoding="utf-8") as f:
        pid = json.load(f)["id"]
    out = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.roteiro)), "saida")
    falas, audio = os.path.join(out, "falas"), os.path.join(out, "audio")
    os.makedirs(audio, exist_ok=True)
    tl = os.path.join(out, "timeline.json")

    run(os.path.join(AQUI, "tts.py"), a.roteiro, falas)
    if not a.pular_asr:
        run(os.path.join(AQUI, "check_asr.py"), falas, a.roteiro)
    run(os.path.join(AQUI, "auto_timeline.py"), a.roteiro, falas, a.cenas, tl)
    if a.preview:
        run(os.path.join(AQUI, "render.py"), tl, a.fotos, os.path.join(out, "preview"), "--preview")
        print("\nprévia em", os.path.join(out, "preview"))
        return
    run(os.path.join(AQUI, "build_audio.py"), tl, falas, audio)
    mudo = os.path.join(out, "video_sem_audio.mp4")
    run(os.path.join(AQUI, "render.py"), tl, a.fotos, mudo)
    if not a.sem_legenda:  # vídeo narrado sempre com legenda na tela
        legendado = os.path.join(out, "video_legendado.mp4")
        run(os.path.join(AQUI, "legendas.py"), "roteiro", a.roteiro, tl, falas, mudo, legendado)
        mudo = legendado
    final = os.path.join(out, f"{pid}_so-voz.mp4")
    run(os.path.join(AQUI, "mux.py"), mudo, os.path.join(audio, "mix_so_voz.wav"), final)
    run(os.path.join(AQUI, "mux.py"), mudo, os.path.join(audio, "mix_com_musica.wav"), os.path.join(out, f"{pid}_com-musica.mp4"))
    with open(tl, encoding="utf-8") as f:
        folha(final, os.path.join(out, "folha.png"), json.load(f)["dur"])
    print("\npronto:", final)


if __name__ == "__main__":
    main()
