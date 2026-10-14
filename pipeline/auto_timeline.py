"""Monta o timeline.json de um post a partir do roteiro e da duração real de cada fala gerada.

Uso: python -I auto_timeline.py <roteiro.json> <pasta_falas> <cenas.json> <saida_timeline.json>

No roteiro, cada fala pode ter:
  "cena": nome de uma cena do cenas.json (sem "cena", a cena anterior continua na tela)
  "entrada": punch | whip | flash (padrão: o da cena; a 1ª é sempre punch)
  "inverter": true  -> troca início e fim do movimento de câmera (zoom de saída em vez de entrada)
  "preco": true     -> fala do preço: a cena entra com clarão (flash) e a música faz o "drop" aí
  "pausa": segundos de silêncio depois da fala (padrão 0,25 s; 0,13 s em itens de lista terminados em "...")
"""
import json
import os
import subprocess
import sys

TAIL = 1.4  # respiro depois da última fala
MAX_DUR = 30.0


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main(rot_path, falas_dir, cenas_path, out_path):
    with open(rot_path, encoding="utf-8") as f:
        rot = json.load(f)
    with open(cenas_path, encoding="utf-8") as f:
        presets = json.load(f)["cenas"]
    falas = rot["falas"]
    assert falas[0].get("cena"), "a primeira fala precisa de uma cena"

    t = 0.10
    voz, cenas = [], []
    for i, fala in enumerate(falas):
        corte = fala.get("corte", 0.07 if i == 0 else 0.0)
        d = dur(os.path.join(falas_dir, fala["id"] + ".wav")) - corte
        v = {"id": fala["id"], "t": round(t, 2)}
        if corte:
            v["corte"] = corte
        voz.append(v)

        nome = fala.get("cena")
        if nome:
            if nome not in presets:
                raise SystemExit(f'cena "{nome}" não existe em {cenas_path}')
            p = presets[nome]
            entrada = "punch" if i == 0 else ("flash" if fala.get("preco") else fala.get("entrada", p.get("entrada", "punch")))
            r0, r1 = (p["r1"], p["r0"]) if fala.get("inverter") else (p["r0"], p["r1"])
            c = {"id": f"{len(cenas) + 1:02d}_{nome}", "foto": p["foto"], "modo": p["modo"],
                 "ini": 0.0 if i == 0 else round(t - 0.06, 2), "entrada": entrada, "r0": r0, "r1": r1}
            if "card" in p:
                c["card"] = p["card"]
            if "ease" in p:
                c["ease"] = p["ease"]
            cenas.append(c)

        texto = fala["texto"].rstrip()
        pausa = fala.get("pausa", 0.13 if texto.endswith("...") else 0.25)
        if fala.get("preco"):
            pausa = max(pausa, 0.40)
        if i + 1 < len(falas) and falas[i + 1].get("preco"):
            pausa = max(pausa, 0.31)
        t += d + pausa

    fim_fala = voz[-1]["t"] + dur(os.path.join(falas_dir, falas[-1]["id"] + ".wav")) - voz[-1].get("corte", 0)
    total = round(fim_fala + TAIL, 2)
    if total > MAX_DUR:
        print(f"AVISO: vídeo com {total:.1f} s (acima de {MAX_DUR:.0f} s). Encurte o roteiro.")
    tl = {"fps": 30, "w": 1080, "h": 1920, "dur": total, "bpm": 120, "grade_inicio": 0.32, "voz": voz, "cenas": cenas}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tl, f, ensure_ascii=False, indent=1)
    print(f"timeline: {len(voz)} falas, {len(cenas)} cenas, {total:.2f} s -> {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
