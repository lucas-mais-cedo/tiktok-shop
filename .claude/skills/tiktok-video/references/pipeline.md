# Pipeline de vídeo (fotos do anúncio + narração + legenda na tela)

Formato: 1080x1920, 30 fps, H.264, AAC 48 kHz, -14 LUFS, 16 a 30 s. A oferta vem pela narração, com a **legenda na tela** (obrigatória em vídeo narrado). Fora a legenda, nenhum texto: o texto embutido nas fotos do anúncio é recortado. A trilha em alta entra depois, no editor do TikTok.

## Arquivos

| Script (`pipeline/`) | Faz |
|---|---|
| `make_post.py` | roda tudo em ordem para um post (use este) |
| `tts.py` | voz de cada fala (Kokoro `pf_dora`, velocidade 1,08); no PC usa `kokoro`, na nuvem `kokoro-onnx` |
| `check_asr.py` | transcreve cada fala com o Whisper e marca "REVISAR" quando a pronúncia sai errada |
| `auto_timeline.py` | monta `timeline.json` a partir do roteiro, das cenas prontas e da duração real das falas |
| `build_audio.py` | posiciona as falas, cria trilha original (sem direitos de terceiros), whooshes e ducking; gera `mix_so_voz.wav` e `mix_com_musica.wav` |
| `render.py` | anima as fotos (zoom/pan, cartões sem o texto embutido, transições punch/whip/flash); `--preview` gera 2 quadros por cena |
| `legendas.py` | queima a legenda na tela. Modo `roteiro` (usado pelo make_post, tempos exatos) e modo `audio` (vídeo pronto: alinha o texto com o Whisper; `--ate auto` corta depois da última palavra) |
| `mux.py` | junta vídeo + áudio normalizando para -14 LUFS (duas passadas) |

Cenas prontas do produto: `produtos/kit-6-em-1/cenas.json` (recortes nas fotos `foto01..foto10.jpg` da LarLuxo). Nomes: `abertura`, `seis_em_um`, `halteres`, `barra`, `kettlebell`, `flexao`, `peso`, `rosca`, `em_uso`, `preco`, `pratico`, `fechamento`.

## Formato do roteiro (`roteiro.json`)

```json
{
  "id": "D1-20h",
  "voz": "pf_dora",
  "velocidade": 1.08,
  "produto": "https://shop.tiktok.com/br/pdp/1737041809079633642",
  "verificado_em": "2026-10-14",
  "falas": [
    {"id": "01", "texto": "Academia em casa, com frete grátis?", "cena": "abertura"},
    {"id": "02", "texto": "Vira um par de halteres...", "cena": "halteres"},
    {"id": "03", "texto": "barra...", "cena": "barra"},
    {"id": "04", "texto": "Tudo isso por cento e oitenta e quatro reais e noventa.", "cena": "preco", "preco": true},
    {"id": "05", "texto": "Toca no carrinho laranja!", "cena": "fechamento"}
  ]
}
```

- `cena`: troca de imagem nessa fala. Sem `cena`, a imagem anterior continua.
- `preco: true`: entra com clarão e a música faz o "drop" (na versão com música).
- `inverter: true`: inverte o movimento da câmera (zoom de saída), bom para variar cenas repetidas.
- `entrada`: força `punch`, `whip` ou `flash`. `pausa`: silêncio depois da fala (padrão 0,25 s; 0,13 s em itens terminados em "...").
- `texto_legivel` (opcional): o texto "normal" para a conferência do Whisper quando `texto` usa grafia fonética.

## Rodar no PC (Windows, PowerShell)

Uma vez: clonar o repositório para `M:\(tiktok shop)\tiktok-shop` (ou baixar o ZIP do GitHub). Depois, para cada post:

```powershell
cd "M:\(tiktok shop)\tiktok-shop"; git pull
$env:HF_HUB_OFFLINE = '1'
M:\jarvis\.venv\Scripts\python.exe -I pipeline\make_post.py plano\semana-01\D1-20h\roteiro.json "M:\(tiktok shop)\video-kit-6-em-1\fotos-anuncio"
```

- Prévia rápida (sem renderizar tudo): acrescentar `--preview` e olhar `saida\preview\`.
- Render completo leva ~5 min (CPU). O vídeo final fica em `plano\semana-01\D1-20h\saida\D1-20h_so-voz.mp4`.
- A pasta `saida\` não vai para o git (vídeos pesados).

## Rodar na nuvem (sessão Claude Code na web)

Funciona para a voz (modelo Kokoro ONNX baixado do GitHub). Para as imagens, a nuvem precisa acessar as fotos do anúncio: o domínio `p16-oec-sg.ibyteimg.com` está **bloqueado** pela política de rede do ambiente (liberar em Network access → Allowed domains). O Whisper também não baixa (huggingface.co bloqueado): usar `--pular-asr`.

```bash
python3 -m venv venv && ./venv/bin/pip install numpy soundfile kokoro-onnx torch
mkdir kmodel && cd kmodel
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd .. && KOKORO_ONNX_DIR=$PWD/kmodel ./venv/bin/python -I pipeline/make_post.py <roteiro.json> <pasta_fotos> --pular-asr
```

## Pronúncia (Kokoro pf_dora): escrever assim

| Palavra | Problema | Grafia no roteiro |
|---|---|---|
| kit | sai "catch" | evitar ("seis em um", "esse conjunto"); o fork usou "kíti" |
| kettlebell | sai "Kettler Bell" | `quétoubél` |
| halteres | sai "altérios" (aceitável) | `um par de halteres` |
| preço | — | por extenso: `cento e oitenta e quatro reais e noventa` |
| nota | — | `quatro vírgula seis` |
| vendidos | — | `mais de sete mil vendidos` (arredondar para baixo) |
| 15 kg | — | `quinze quilos` |

Sempre conferir com `check_asr.py`. A 1ª fala tem um estalo no começo: o `auto_timeline` já corta 0,07 s.

## Problemas conhecidos

- Python com `-I` ignora `PYTHONIOENCODING`: os scripts chamam `sys.stdout.reconfigure(encoding="utf-8")`.
- O ffmpeg do Windows não aceita `-pattern_type glob`: numerar arquivos (`m%02d.png`).
- `Remove-Item` em `M:\` é bloqueado pela proteção de caminho: sobrescrever em vez de apagar.
- O fork "Editor de Videos" instalou a voz **Chatterbox pt-BR** num ambiente separado (`scripts\tts_chatterbox.py`). Se a qualidade for melhor, trocar o motor em `tts.py` mantendo a saída (1 wav por fala, 24 kHz).
- Vídeo só com fotos do anúncio alcança menos que vídeo gravado com o produto real. Quando houver o produto em mãos, gravar 3 a 5 tomadas curtas (montagem, troca halter→barra→kettlebell, close na trava) e usar como cenas `modo: "cheio"`.
