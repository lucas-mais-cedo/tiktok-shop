# Publicação e agendamento

## Quem publica (decidido pelo usuário em 14/10/2026)

**A sessão Claude no PC do usuário** publica: "Vídeo promocional TikTok Shop fitness" (`session_017q2VWPpsvQbTUxJa5Th6hg`, app desktop, navegador integrado logado na @asadelta.shop). A sessão na nuvem não acessa o TikTok (rede bloqueada, sem conector de postagem).

Como a nuvem entrega cada pacote:
1. `send_message` para a sessão do PC (use `priority: "later"` para não interromper o que ela estiver fazendo), com: post, horário, como gerar ou onde está o vídeo, legenda + hashtags e o checklist abaixo. A autorização do usuário ("publique pela sessão claude do meu PC") vai citada; a sessão do PC pode confirmar com ele antes de publicar.
2. Vídeo: enquanto a nuvem não baixar as fotos do anúncio, a sessão do PC gera o vídeo com os **scripts locais dela** (`M:\(tiktok shop)\video-kit-6-em-1\scripts`: tts.py, build_audio.py, render.py, mux.py; fotos em `fotos-anuncio`) e faz a legenda na tela com Whisper + ffmpeg locais. **A proteção de segurança do PC bloqueia download do GitHub** (14/10): mande tudo no corpo da mensagem (falas com a grafia para a voz, ordem das cenas pelos nomes do `timeline.json` original do PC, texto do post, estilo da legenda). Mapa de cenas: `abertura`=A_gancho, `seis_em_um`=B_6em1, `halteres`=C_halteres, `barra`=D_barra, `kettlebell`=E_kettle, `flexao`=F_flexao, `peso`=G1_peso, `rosca`=G2_rosca, `em_uso`=H_prova, `preco`=I_preco, `pratico`=J_pratico, `fechamento`=K_cta.
   - **Fuso:** no PC, `TZ=America/Sao_Paulo date` (Git Bash) devolve UTC. Sempre escreva o horário em Brasília **e** em UTC na mensagem (Brasília = UTC−3).
3. A sessão do PC não tem `send_message`: ela escreve o resultado como resposta final. Ler com `list_events` (kinds `assistant`) e registrar o link em `metricas/posts.csv`.
4. Se o PC estiver desligado ou a sessão desconectada, avisar o usuário no chat com o pacote pronto para ele postar pelo celular.

A API oficial de postagem do TikTok (Content Posting API) exige app de desenvolvedor com auditoria, só posta como privado antes da auditoria e **não liga produto do TikTok Shop**. Por isso não é o caminho para esta conta.

## Agendamento nativo (TikTok Studio no computador)

- `tiktok.com/tiktokstudio/upload` → enviar vídeo → legenda → **Agendar** (de 15 min até 10 dias à frente; algumas contas veem 30 dias).
- Depois de agendado **não dá para editar** vídeo, legenda ou horário: corrigir = excluir e reenviar.
- Não há confirmação pública de que dá para ligar produto do TikTok Shop num post agendado: testar no 1º agendamento. Se não der, publicar na hora (lembrete) em vez de agendar.

## Checklist de cada post

- [ ] Vídeo `<post>_so-voz.mp4` conferido: legenda na tela legível e sincronizada, sem texto embutido das fotos, sem erro de pronúncia.
- [ ] Preço/frete/vendidos citados no vídeo ainda batem com o anúncio (verificado hoje).
- [ ] Legenda + hashtags do slot (com `#publi` se for afiliado).
- [ ] **Produto**: na fase 1 (sem permissão), **não** ligar nada e conferir que o vídeo e a legenda não citam carrinho/link. Quando liberar: Adicionar link → Produtos → Kit 6 em 1 da **ART CADEIRAS** (`pdp 1737041809079633642`).
- [ ] **Conteúdo gerado por IA**: ligado (voz sintética).
- [ ] Capa: um quadro do produto inteiro (ex.: cena `abertura` ou `seis_em_um`), sem texto.
- [ ] **Som**: trilha **em alta** do TikTok (pedido do usuário), som adicionado em ~10 a 15% e original em 100%; ouvir a prévia e garantir que a narração está clara. Se o TikTok só oferecer a Biblioteca de Música Comercial (acontece em post com produto/conteúdo de marca), escolher a mais em alta de lá.
- [ ] Horário: 10:00, 15:00 ou 20:00 de Brasília (ou o novo horário do último relatório).
- [ ] Depois de publicar: anotar o link do vídeo em `metricas/posts.csv`.

## Requisitos da conta (confirmar no app)

- @asadelta.shop é **afiliada iniciante** (não é a conta da loja), com 0 seguidores em 14/10/2026: ainda **não pode ligar produto**.
- Para ligar produto como afiliado, o TikTok Shop Brasil pede **1.000 seguidores** (algumas contas veem 2.000) e 18+, com verificação de identidade. Depois, um piloto de 30 dias com até 10 vídeos com produto por dia. O requisito que vale é o do app (TikTok Studio → TikTok Shop para criadores).
- Antes disso, o único caminho de comissão é o **Linkshare** (link para divulgar fora do TikTok, se a opção aparecer no app). Não dá para pôr esse link no vídeo nem na legenda.
- Enquanto não houver permissão: vídeo sem produto, chamada "segue/salva/comenta", sem "carrinho laranja", sem "link na bio" e sem `#publi`.
