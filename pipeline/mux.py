"""Junta o vídeo sem áudio com a mixagem, normalizando o volume para -14 LUFS (duas passadas de loudnorm).

Uso: python -I mux.py <video_sem_audio.mp4> <mix.wav> <saida.mp4>
"""
import json
import re
import subprocess
import sys


def measure(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav,
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1]
    return json.loads(blob)


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    s = r.stderr[r.stderr.rindex("Summary"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)
    return float(i), float(p)


def main(video, wav, out):
    j = measure(wav)
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:linear=true,aresample=48000").format(**j)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out],
                   check=True)
    i, p = lufs(out)
    print(f"{out}: {i} LUFS, pico {p} dBFS")


if __name__ == "__main__":
    main(*sys.argv[1:4])
