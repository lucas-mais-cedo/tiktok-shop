"""Gera o calendário legível e os arquivos de cada post a partir do plano da semana (fonte única).

Uso: python -I gerar_plano.py plano/semana-01.json
Cria: plano/semana-01.md e plano/semana-01/<post>/roteiro.json + legenda.txt
"""
import json
import os
import sys

DIAS = {0: "seg", 1: "ter", 2: "qua", 3: "qui", 4: "sex", 5: "sáb", 6: "dom"}


def main(src):
    import datetime as dt
    with open(src, encoding="utf-8") as f:
        plano = json.load(f)
    base = os.path.splitext(src)[0]
    nome = os.path.basename(base)
    linhas = [
        f"# Calendário {nome}: Kit 6 em 1 (ART CADEIRAS)",
        "",
        f"Produto: {plano['produto']} · dados verificados em {plano['verificado_em']} · horários em {plano['fuso']}.",
        "Gerado por `pipeline/gerar_plano.py` a partir de `" + os.path.basename(src) + "` (edite o JSON, não este arquivo).",
        "",
        "Cada ângulo aparece em mais de um horário, para comparar horários sem confundir com o conteúdo.",
        "Posts marcados *provisório* podem mudar conforme o relatório diário.",
        "",
        "| Post | Dia | Data | Hora | Ângulo | Gancho | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    detalhes = []
    for p in plano["posts"]:
        d = dt.date.fromisoformat(p["data"])
        falas = p.get("falas")
        gancho = p.get("gancho") or (falas[0].get("texto_legivel", falas[0]["texto"]) if falas else "")
        status = "pronto (vídeo do fork)" if p.get("pronto") else ("provisório" if p.get("provisorio") else "roteiro pronto")
        linhas.append(f"| {p['id']} | {DIAS[d.weekday()]} {p['dia']} | {d.strftime('%d/%m')} | {p['hora']} | {p['angulo']} | {gancho} | {status} |")

        det = [f"### {p['id']}: {d.strftime('%d/%m')} às {p['hora']} · {p['angulo']}", ""]
        if p.get("pronto"):
            det.append(f"**Vídeo:** `{p['pronto']}`")
        if falas:
            det.append("**Narração:** " + " ".join(x.get("texto_legivel", x["texto"]) for x in falas))
            det.append("")
            det.append("**Cenas:** " + " → ".join(x["cena"] for x in falas if x.get("cena")))
            pasta = os.path.join(base, p["id"])
            os.makedirs(pasta, exist_ok=True)
            rot = {"id": p["id"], "voz": "pf_dora", "velocidade": 1.08, "produto": plano["produto"],
                   "verificado_em": plano["verificado_em"], "falas": falas}
            with open(os.path.join(pasta, "roteiro.json"), "w", encoding="utf-8") as f:
                json.dump(rot, f, ensure_ascii=False, indent=1)
            with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
                f.write(p["legenda"] + "\n\n" + p["hashtags"] + "\n")
            det.append("")
            det.append(f"**Arquivos:** `{nome}/{p['id']}/roteiro.json`, `{nome}/{p['id']}/legenda.txt`")
        det += ["", "**Legenda:**", f"> {p['legenda']}", "", f"`{p['hashtags']}` (+ `#publi` se a conta for afiliada)",
                "", f"**Capa:** {p.get('capa', '1º quadro')}", ""]
        detalhes += det
    md = linhas + ["", "## Posts", ""] + detalhes
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("ok:", base + ".md")


if __name__ == "__main__":
    main(sys.argv[1])
