# Publicação e agendamento

## Quem publica

A sessão na nuvem **não tem acesso ao TikTok** (rede bloqueada e sem conector de postagem). A publicação acontece no PC ou no celular do usuário, por um destes caminhos:

1. **Sessão Claude no PC** (app desktop, com o navegador integrado já logado na conta @asadelta.shop): abre o TikTok Studio, envia o vídeo, cola legenda, liga o produto e agenda. Precisa da autorização do usuário nessa sessão.
2. **Usuário**, a partir do pacote pronto (vídeo + legenda + hashtags + link), no app ou no TikTok Studio.

A API oficial de postagem do TikTok (Content Posting API) exige app de desenvolvedor com auditoria, só posta como privado antes da auditoria e **não liga produto do TikTok Shop**. Por isso não é o caminho para esta conta.

## Agendamento nativo (TikTok Studio no computador)

- `tiktok.com/tiktokstudio/upload` → enviar vídeo → legenda → **Agendar** (de 15 min até 10 dias à frente; algumas contas veem 30 dias).
- Depois de agendado **não dá para editar** vídeo, legenda ou horário: corrigir = excluir e reenviar.
- Não há confirmação pública de que dá para ligar produto do TikTok Shop num post agendado: testar no 1º agendamento. Se não der, publicar na hora (lembrete) em vez de agendar.

## Checklist de cada post

- [ ] Vídeo `<post>_so-voz.mp4` conferido (sem texto embutido, sem erro de pronúncia).
- [ ] Preço/frete/vendidos citados no vídeo ainda batem com o anúncio (verificado hoje).
- [ ] Legenda + hashtags do slot (com `#publi` se for afiliado).
- [ ] **Produto linkado**: Adicionar link → Produtos → Kit 6 em 1 da **ART CADEIRAS** (`pdp 1737041809079633642`).
- [ ] **Conteúdo gerado por IA**: ligado (voz sintética).
- [ ] Capa: um quadro do produto inteiro (ex.: cena `abertura` ou `seis_em_um`), sem texto.
- [ ] Som: o vídeo já tem a voz; se usar som da biblioteca, só da **Biblioteca de Música Comercial** e com volume baixo.
- [ ] Horário: 10:00, 15:00 ou 20:00 de Brasília (ou o novo horário do último relatório).
- [ ] Depois de publicar: anotar o link do vídeo em `metricas/posts.csv`.

## Requisitos da conta (confirmar no app)

- Para ligar produto como **afiliado**, o TikTok Shop Brasil costuma pedir mínimo de seguidores (fontes citam 1.000; algumas 2.000) e 18+. Contas novas têm limite de vídeos com produto por dia. O requisito que vale é o que aparece no app (TikTok Studio → TikTok Shop para criadores).
- Se @asadelta.shop for a **conta oficial da loja vendedora**, não há mínimo de seguidores para ligar os próprios produtos.
- Sem permissão de produto, o vídeo ainda pode ir ao ar para ganhar seguidores, com a chamada trocada para "link na bio" ou "segue pra ver mais" (nunca prometer carrinho que não existe).
