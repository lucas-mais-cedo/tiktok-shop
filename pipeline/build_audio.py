"""Monta o áudio do vídeo: narração + trilha sintetizada (original) + efeitos.

Uso: python -I build_audio.py <timeline.json> <pasta_falas> <pasta_saida>
Saídas: mix_com_musica.wav, mix_so_voz.wav, musica.wav (48 kHz, sem normalização final;
a normalização para -14 LUFS é feita no ffmpeg na hora de juntar com o vídeo).
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

SR = 48000
rng = np.random.default_rng(7)


def load_voice(path):
    """Lê a fala e converte para 48 kHz com o resampler do ffmpeg."""
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "v.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", str(SR), "-ac", "1", out], check=True)
        a, _ = sf.read(out, dtype="float32")
    return a


def place(buf, t, sig, gain=1.0):
    i = int(round(t * SR))
    if i < 0:
        sig, i = sig[-i:], 0
    n = min(len(sig), len(buf) - i)
    if n > 0:
        buf[i:i + n] += sig[:n] * gain


def band(x, lo, hi, soft=0.15):
    """Filtro passa-faixa suave no domínio da frequência."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if lo > 0:
        g *= 1 / (1 + (lo / np.maximum(f, 1)) ** (1 / soft * 0.5))
    if hi < SR / 2:
        g *= 1 / (1 + (f / hi) ** (1 / soft * 0.5))
    return np.fft.irfft(X * g, len(x))


def tt(d):
    return np.arange(int(d * SR)) / SR


# ---------- instrumentos ----------
def kick():
    t = tt(0.4)
    f = 48 + 110 * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    click = band(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.004) * 0.25
    return body + click


def clap():
    t = tt(0.3)
    n = band(rng.standard_normal(len(t)), 900, 5000)
    env = np.exp(-t / 0.09)
    for d in (0.0, 0.011, 0.022):  # três "batidas" curtas, típico de palma
        env = env + 0.6 * np.exp(-np.maximum(t - d, 0) / 0.006) * (t >= d)
    return n * env / 2.2


def hat(open_=False):
    t = tt(0.25 if open_ else 0.08)
    n = band(rng.standard_normal(len(t)), 7000, 16000)
    return n * np.exp(-t / (0.07 if open_ else 0.018))


def note(freq, d, nh=10, decay=0.25, bright=6.0, detune=0.0):
    """Nota estilo 'pluck': harmônicos de serra com decaimento mais rápido nos agudos."""
    t = tt(d)
    out = np.zeros_like(t)
    for det in ((-detune, detune) if detune else (0.0,)):
        f0 = freq * 2 ** (det / 1200)
        for k in range(1, nh + 1):
            if f0 * k > SR / 2 - 1000:
                break
            out += np.sin(2 * np.pi * f0 * k * t) / k * np.exp(-t * (1 / decay + bright * (k - 1)))
    att = np.minimum(t / 0.004, 1)
    rel = np.clip((d - t) / 0.02, 0, 1)
    return out * att * rel


def whoosh(d=0.5, peak=0.6, f_lo=400, f_hi=3500):
    """Ruído com faixa de frequência que sobe e desce (efeito de transição)."""
    n = int(d * SR)
    out = np.zeros(n)
    g = int(0.04 * SR)
    hop = g // 2
    win = np.hanning(g)
    for s in range(0, n - g, hop):
        p = s / n
        fc = f_lo * (f_hi / f_lo) ** (np.sin(np.pi * min(p / peak, 1) / 2) if p < peak else 1 - (p - peak) / (1 - peak) * 0.6)
        grain = band(rng.standard_normal(g), fc * 0.6, fc * 1.6)
        out[s:s + g] += grain * win
    t = np.arange(n) / n
    env = np.where(t < peak, (t / peak) ** 2, np.exp(-(t - peak) / (1 - peak) * 4))
    return out * env


def riser(d=1.0):
    n = int(d * SR)
    out = np.zeros(n)
    g = int(0.05 * SR)
    hop = g // 2
    win = np.hanning(g)
    for s in range(0, n - g, hop):
        p = s / n
        fc = 300 * (6000 / 300) ** p
        out[s:s + g] += band(rng.standard_normal(g), fc * 0.7, fc * 1.4) * win
    t = np.arange(n) / n
    return out * t ** 2


def impact():
    t = tt(1.6)
    f = 32 + 50 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    crash = band(rng.standard_normal(len(t)), 4000, 15000) * np.exp(-t / 0.6) * 0.35
    hit = band(rng.standard_normal(len(t)), 100, 1200) * np.exp(-t / 0.05) * 0.5
    return boom + crash + hit


def thump():
    t = tt(0.14)
    f = 50 + 70 * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)


# ---------- trilha ----------
def build_music(dur, bpm, g0, drop):
    N = int(dur * SR)
    kick_b, clap_b, hat_b, bass_b, stab_b = (np.zeros(N) for _ in range(5))
    beat = 60 / bpm
    e8 = beat / 2
    # Lá menor: Am - F - C - G (1 compasso cada)
    roots = [110.00, 87.31, 130.81, 98.00]
    chords = [[220.00, 261.63, 329.63], [174.61, 220.00, 261.63], [261.63, 329.63, 392.00], [196.00, 246.94, 293.66]]
    kicks = []
    n_beats = int((dur - g0) / beat) + 2
    for b in range(-1, n_beats):
        tb = g0 + b * beat
        bar = int(np.floor(b / 4)) % 4
        in_break = drop - 2 * beat <= tb < drop  # 2 tempos de pausa antes do "drop" do preço
        if not in_break:
            place(kick_b, tb, kick())
            kicks.append(tb)
            if b % 2 == 1:
                place(clap_b, tb, clap())
        for s in range(4):  # chimbal em semicolcheias, acento no contratempo
            th = tb + s * beat / 4
            if in_break and s % 2 == 0:
                continue
            place(hat_b, th, hat(open_=(s == 2)), 0.9 if s == 2 else 0.35)
        for s in range(2):  # baixo em colcheias
            tn = tb + s * e8
            r = roots[bar] * (2 if (b % 4 == 3 and s == 1) else 1)
            if not in_break:
                place(bass_b, tn, note(r, e8 * 0.95, nh=8, decay=0.18, bright=3.0))
    for bar_i in range(-1, int((dur - g0) / (4 * beat)) + 2):
        tb = g0 + bar_i * 4 * beat
        ch = chords[bar_i % 4]
        for pos in (0, 3, 6):  # ritmo 3-3-2 em colcheias
            ts = tb + pos * e8
            if drop - 2 * beat <= ts < drop:
                continue
            stab = sum(note(f, 0.3, nh=12, decay=0.12, bright=1.5, detune=7) for f in ch)
            place(stab_b, ts, stab)
    # "pump": baixo e acordes abaixam a cada bumbo
    t = np.arange(N) / SR
    pump = np.ones(N)
    for k in kicks:
        i = int(k * SR)
        if 0 <= i < N:
            seg = t[i:i + int(0.25 * SR)] - k
            pump[i:i + len(seg)] = np.minimum(pump[i:i + len(seg)], 1 - 0.65 * np.exp(-seg / 0.07))
    mix = kick_b * 0.9 + clap_b * 0.45 + hat_b * 0.18 + (bass_b * 0.5 + stab_b * 0.16) * pump
    place(mix, drop - 1.0, riser(1.0), 0.35)
    place(mix, drop, impact(), 0.55)
    place(mix, g0, band(rng.standard_normal(int(1.2 * SR)), 4000, 15000) * np.exp(-tt(1.2) / 0.5), 0.12)  # prato inicial
    return mix / (np.max(np.abs(mix)) + 1e-9) * 0.9


def envelope(x, win=0.05):
    w = int(win * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode="same"))
    # ataque rápido, soltura lenta
    out = np.zeros_like(e)
    a_rel = np.exp(-1 / (0.25 * SR))
    v = 0.0
    for i in range(0, len(e), 64):
        target = e[i:i + 64].max()
        v = target if target > v else v * a_rel ** 64
        out[i:i + 64] = v
    return out


def main(tl_path, falas_dir, out_dir):
    with open(tl_path, encoding="utf-8") as f:
        tl = json.load(f)
    dur = tl["dur"]
    N = int(dur * SR)
    os.makedirs(out_dir, exist_ok=True)

    voice = np.zeros(N)
    last_end = 0
    for v in tl["voz"]:
        a = load_voice(os.path.join(falas_dir, v["id"] + ".wav"))
        a = a[int(v.get("corte", 0) * SR):]
        a = a / (np.max(np.abs(a)) + 1e-9) * 0.9
        assert v["t"] >= last_end - 0.01, f'fala {v["id"]} sobrepõe a anterior'
        place(voice, v["t"], a)
        last_end = v["t"] + len(a) / SR
        print(f'{v["id"]:12s} {v["t"]:6.2f} -> {last_end:6.2f}')
    assert last_end < dur, "narração passa do fim do vídeo"

    cenas = tl["cenas"]
    sfx = np.zeros(N)
    for c in cenas:
        if c["entrada"] == "whip":
            w = whoosh(0.5, peak=0.55)
            place(sfx, c["ini"] - 0.5 * 0.55, w, 0.30)
        elif c["entrada"] == "punch" and c["ini"] > 0:
            place(sfx, c["ini"], thump(), 0.22)
    place(sfx, 0.0, whoosh(0.35, peak=0.35)[int(0.05 * SR):], 0.28)  # entrada do gancho

    # sem cena "flash" (sem fala de preço): o drop fica depois do fim e a música toca sem pausa
    drop = next((c["ini"] for c in cenas if c["entrada"] == "flash"), dur + 10)
    music = build_music(dur, tl["bpm"], tl["grade_inicio"], drop)
    sf.write(os.path.join(out_dir, "musica.wav"), music.astype(np.float32), SR)

    # abaixa a música quando há voz (ducking)
    env = envelope(voice)
    duck = 1 - 0.6 * np.clip(env / 0.08, 0, 1)
    fade = np.clip((dur - np.arange(N) / SR) / 0.3, 0, 1)

    mix_m = (voice * 1.0 + music * 0.32 * duck + sfx) * fade
    mix_v = (voice * 1.0 + sfx) * fade
    for name, m in (("mix_com_musica.wav", mix_m), ("mix_so_voz.wav", mix_v)):
        m = m / max(1.0, np.max(np.abs(m)) / 0.97)
        sf.write(os.path.join(out_dir, name), m.astype(np.float32), SR, subtype="FLOAT")
    print("ok:", out_dir)


if __name__ == "__main__":
    main(*sys.argv[1:4])
