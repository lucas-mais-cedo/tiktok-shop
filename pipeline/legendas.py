"""Legenda na tela (estilo TikTok) para vídeos narrados: blocos curtos, letra branca grossa com contorno preto.

Modo 1, vídeos do make_post (tempos exatos de cada fala, sem Whisper; funciona no PC e na nuvem):
  python -I legendas.py roteiro <roteiro.json> <timeline.json> <pasta_falas> <entrada.mp4> <saida.mp4>

Modo 2, vídeo já pronto (ex.: o do fork): alinha o texto conhecido com o áudio usando o Whisper (só no PC):
  python -I legendas.py audio <texto.txt> <entrada.mp4> <saida.mp4> [--ate SEGUNDOS|auto]
  texto.txt = uma fala por linha, com o que a voz diz (números podem vir em algarismos).
  --ate corta o vídeo nesse ponto; "auto" corta 0,35 s depois da última palavra do texto.

A legenda fica na faixa central-baixa (acima do nome, da legenda do post e dos botões do TikTok).
"""
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

MAX_CHARS = 18  # por bloco: 2 a 4 palavras, lê de relance
ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TT,Arial,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,7,3,2,150,150,640,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if not unicodedata.combining(c)))


LIGACAO = {"a", "o", "e", "de", "do", "da", "um", "uma", "pra", "por", "com", "no", "na", "em", "que", "se", "seu", "sua"}


def blocos(palavras):
    """Agrupa palavras em blocos curtos, quebrando também depois de pontuação.
    Palavra de ligação ("de", "e", "um"...) no fim de um bloco passa para o próximo."""
    out, cur = [], []
    for w in palavras:
        if cur and len(" ".join(cur + [w])) > MAX_CHARS:
            leva = []
            while len(cur) > 1 and norm(cur[-1]) in LIGACAO:
                leva.insert(0, cur.pop())
            out.append(cur)
            cur = leva
        cur.append(w)
        if re.search(r"[,.:;?!…]$", w):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def limpa(txt):
    txt = re.sub(r"\.\.\.|…", "", txt)
    return re.sub(r"[,.;:]+$", "", txt).strip()


def ts(t):
    t = max(t, 0)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def escreve_ass(cues, path):
    linhas = [ASS_HEAD]
    for a, b, txt in cues:
        txt = limpa(txt)
        if txt:
            linhas.append(f"Dialogue: 0,{ts(a)},{ts(b)},TT,,0,0,0,,{{\\fad(40,0)}}{txt}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(linhas)


def cues_roteiro(rot_path, tl_path, falas_dir):
    with open(rot_path, encoding="utf-8") as f:
        falas = {x["id"]: x for x in json.load(f)["falas"]}
    with open(tl_path, encoding="utf-8") as f:
        voz = json.load(f)["voz"]
    cues = []
    for v in voz:
        fala = falas[v["id"]]
        texto = fala.get("legenda") or fala.get("texto_legivel") or fala["texto"]
        d = dur(os.path.join(falas_dir, v["id"] + ".wav")) - v.get("corte", 0)
        grupos = blocos(texto.split())
        pesos = [len(" ".join(g)) + 2 for g in grupos]
        t = v["t"]
        for g, p in zip(grupos, pesos):
            seg = d * p / sum(pesos)
            cues.append([t, t + seg, " ".join(g)])
            t += seg
    for i in range(len(cues) - 1):  # emenda pausas curtas para a legenda não piscar
        if cues[i + 1][0] - cues[i][1] < 0.35:
            cues[i][1] = cues[i + 1][0]
    cues[-1][1] += 0.25
    return cues


def alinha(script_words, asr):
    """Dá início/fim para cada palavra do texto usando as palavras com tempo do Whisper."""
    a = [norm(w) for w in script_words]
    b = [norm(w) for w, _, _ in asr]
    tempo = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            tempo[blk.a + k] = (asr[blk.b + k][1], asr[blk.b + k][2])
    if not any(tempo):
        raise SystemExit("não consegui alinhar o texto com o áudio")
    # palavras sem par: distribui entre a anterior e a próxima conhecidas, pelo tamanho
    i = 0
    while i < len(a):
        if tempo[i] is None:
            j = i
            while j < len(a) and tempo[j] is None:
                j += 1
            ini = tempo[i - 1][1] if i > 0 else (tempo[j][0] - 0.3 * (j - i) if j < len(a) else 0)
            fim = tempo[j][0] if j < len(a) else ini + 0.3 * (j - i)
            pesos = [len(script_words[k]) + 1 for k in range(i, j)]
            t = ini
            for k, p in zip(range(i, j), pesos):
                seg = (fim - ini) * p / sum(pesos)
                tempo[k] = (t, t + seg)
                t += seg
            i = j
        else:
            i += 1
    return tempo


def cues_audio(texto_path, video):
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from faster_whisper import WhisperModel
    with open(texto_path, encoding="utf-8") as f:
        linhas = [ln.split() for ln in f if ln.strip()]
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "a.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav], check=True)
        segs, _ = WhisperModel("base", device="cpu", compute_type="int8").transcribe(
            wav, language="pt", word_timestamps=True, beam_size=5)
        asr = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    # alinha o texto inteiro de uma vez (ordem garantida), depois separa por fala
    tempo = alinha([w for ln in linhas for w in ln], asr)
    cues, k = [], 0
    for ln in linhas:
        for g in blocos(ln):
            cues.append([tempo[k][0], tempo[k + len(g) - 1][1], " ".join(g)])
            k += len(g)
    for i in range(len(cues) - 1):
        if cues[i + 1][0] - cues[i][1] < 0.35:
            cues[i][1] = cues[i + 1][0]
    return cues


def queima(entrada, cues, saida, ate=None):
    entrada, saida = os.path.abspath(entrada), os.path.abspath(saida)
    with tempfile.TemporaryDirectory() as td:
        escreve_ass(cues, os.path.join(td, "legenda.ass"))
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", entrada]
        if ate:
            cmd += ["-t", str(ate)]
        cmd += ["-vf", "ass=legenda.ass", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"]
        tem_audio = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                                    "-of", "csv=p=0", entrada], capture_output=True, text=True).stdout.strip()
        if tem_audio:
            if ate:
                cmd += ["-af", f"afade=t=out:st={max(ate - 0.2, 0):.2f}:d=0.2", "-c:a", "aac", "-b:a", "192k"]
            else:
                cmd += ["-c:a", "copy"]
        cmd += ["-movflags", "+faststart", saida]
        subprocess.run(cmd, check=True, cwd=td)  # caminho relativo: o filtro ass não aceita "M:\(...)"
    print(f"legenda: {len(cues)} blocos -> {saida}")


def main():
    modo = sys.argv[1]
    if modo == "roteiro":
        rot, tl, falas, entrada, saida = sys.argv[2:7]
        queima(entrada, cues_roteiro(rot, tl, falas), saida)
    elif modo == "audio":
        texto, entrada, saida = sys.argv[2:5]
        ate = sys.argv[sys.argv.index("--ate") + 1] if "--ate" in sys.argv else None
        cues = cues_audio(texto, entrada)
        if ate == "auto":  # corta logo depois da última palavra do texto (descarta o resto do áudio)
            ate = round(cues[-1][1] + 0.35, 2)
            print(f"corte automático em {ate} s")
        ate = float(ate) if ate else None
        if ate:
            cues = [c for c in cues if c[0] < ate - 0.1]
            cues[-1][1] = min(cues[-1][1], ate)
        queima(entrada, cues, saida, ate)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
