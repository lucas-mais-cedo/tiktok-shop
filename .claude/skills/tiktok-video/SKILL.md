---
name: tiktok-video
description: TikTok-Video. Gestão de social media da conta @asadelta.shop no TikTok Shop Brasil, do roteiro à análise. Use para criar vídeos de venda (narração pt-BR + fotos do anúncio, com legenda na tela), escrever legenda e hashtags, montar e seguir o calendário de postagens (10h, 15h, 18h, 20h e 23h55 de Brasília), preparar o pacote de publicação e fazer o relatório diário de alcance, retenção e conversão. Foco atual - Kit 6 em 1 da loja ART CADEIRAS.
---

# TikTok-Video

Skill de gerente de social media da conta **@asadelta.shop** (TikTok Shop Brasil). Junta o que foi feito nos chats "TikTok Shop fitness hidden gems" (pesquisa), "Vídeo promocional TikTok Shop fitness" (1º vídeo) e o fork "Editor de Videos" (versão de referência e legenda final).

## Situação da conta (atualizada em 14/10/2026)

- @asadelta.shop é uma conta **afiliada iniciante**, sem relação com a loja oficial: **0 seguidores, sem permissão para ligar produto** (sem carrinho laranja).
- **Fase 1 (até 1.000 seguidores):** o objetivo nº 1 é **ganhar seguidores**; vender é bônus. Sem CNPJ/MEI, a venda acontece pelo **link de afiliado (Linkshare) na bio** do perfil, direto ou por Linktree com o nome de cada produto. Detalhes, pré-requisitos e o teste do campo "Site": `references/conta-e-bio.md`. O estado atual está em `plano/estado.json`.
- **Chamada final (CTA):** com `bio_link_ativo: false` = seguir/salvar/comentar; com `bio_link_ativo: true` = seguir + "link na bio". **Nunca** falar ou escrever "carrinho laranja" na fase 1, nem "link na bio" antes de o link estar ativo e testado.
- Caminho de afiliação: com menos de 1.000 seguidores, só o **Linkshare** (link de comissão para divulgar fora do TikTok, se aparecer no app e após a verificação de identidade). A partir de 1.000 seguidores (algumas contas veem 2.000), pedir o cadastro de criador afiliado no TikTok Studio. Novos afiliados entram num piloto de 30 dias com até 10 vídeos com produto por dia. Ao liberar: afiliar-se ao Kit 6 em 1 da ART CADEIRAS (e a outros produtos lucrativos) e voltar a chamada para o carrinho.
- **Quem gera o vídeo (desde 14/10, pedido do usuário):** o chat local **"Editor de Videos"** no PC (`local_2759ef03-23ce-4b7e-8e94-823793ce9de3`). A nuvem não alcança sessões locais: o pedido vai pela sessão do PC, que repassa ao Editor e devolve o pacote (arquivo, duração, LUFS, transcrição, texto do post). A nuvem confere e só então manda agendar. Os dados de performance voltam ao Editor depois de cada relatório.
- **Quem publica:** a sessão Claude no PC do usuário ("Vídeo promocional TikTok Shop fitness", `session_017q2VWPpsvQbTUxJa5Th6hg`), pelo TikTok Studio no navegador integrado. A sessão na nuvem manda os pacotes por `send_message` (ver `references/publicacao.md`).

## Antes de tudo

- **Idioma:** responder sempre em português do Brasil, com linguagem simples. Antes de cada passo, um aviso de uma frase.
- **Estado da conta:** `plano/estado.json` (seguidores, link na bio, PKYC). Atualizar sempre que mudar.
- **Produto em foco:** `produtos/kit-6-em-1/produto.md` (link, preço do dia, o que pode e o que não pode falar).
- **Calendário da semana:** `plano/semana-01.md`. Cada post tem roteiro, cenas, legenda e hashtags.
- **Últimos números:** o relatório mais recente em `relatorios/` e o histórico em `metricas/posts.csv`.

## Regras que não podem ser quebradas

1. **Nunca digitar senha. Nunca resolver CAPTCHA.** Pausar e avisar o usuário.
2. **Pesquisa é só leitura**: não comprar, não seguir, não comentar, não mandar mensagem.
3. **Publicar só na conta @asadelta.shop** e só o que está no calendário aprovado. Qualquer post fora do calendário precisa de "ok" do usuário.
4. **Só afirmações do anúncio ou verificadas no dia.** Sem promessa de emagrecimento ou resultado físico, sem antes e depois corporal, sem falsa urgência ("últimas unidades", "só hoje"), sem desconto inventado.
5. **"Vendidos" é o total acumulado** do anúncio, nunca "vendas da semana".
6. **Voz sintética:** marcar "Conteúdo gerado por IA" ao publicar (a regra do TikTok cobre fala gerada por IA).
7. **Afiliado:** se a conta ganha comissão pelo link, usar `#publi` na legenda (recomendação do CONAR).
8. **Não reaproveitar vídeo de outro criador** (nem trechos). Fotos do anúncio só com autorização do usuário (já dada para o Kit 6 em 1).
9. **Repositório:** não gravar senha, e-mail nem dados pessoais. Enquanto o repositório estiver público, pedidos, faturamento e comissão ficam só no relatório entregue no chat.
10. **Vídeo narrado sempre com legenda na tela** (pedido do usuário em 14/10): `make_post.py` já queima a legenda; para vídeo pronto, usar `legendas.py audio`. Texto embutido nas fotos do anúncio continua proibido (recortar).
12. **Acesso à conta:** sem senha (o usuário entra no navegador; a IA usa a sessão aberta). O que faz sozinha, o que pede "ok" e o que nunca faz (nada de ação em massa, mexer em senha/pagamento/documentos, inventar experiência pessoal) está em `references/conta-e-bio.md`. Respostas a comentários seguem a política desse arquivo.
13. **Divulgação:** com link de afiliado na bio, `#publi` na legenda e a opção de divulgação de conteúdo do TikTok quando se aplicar.
11. **Trilha em alta do TikTok** em todo post (pedido do usuário): escolhida no editor do TikTok na hora de publicar, com o som adicionado baixo (~10 a 15%) e o som original em 100%. A narração tem que continuar clara. Se o TikTok só oferecer a Biblioteca de Música Comercial, usar a mais em alta de lá.

## Fluxo de um post (checklist)

1. **Pegar o slot** em `plano/semana-01.md` (ângulo, gancho, roteiro, cenas, legenda).
2. **Revalidar o anúncio** (preço, frete, vendidos, nota). Se mudou, ajustar a fala de preço/prova no `roteiro.json` e a legenda. Se não der para verificar, **tirar** a fala de preço/prova (não chutar).
3. **Gerar o vídeo** (ver `references/pipeline.md`):
   `python -I pipeline/make_post.py plano/semana-01/<post>/roteiro.json <pasta_fotos>`
   Saída principal: `<post>_so-voz.mp4` (prioridade: só voz). Também sai `<post>_com-musica.mp4`.
4. **Conferir:** a conferência de pronúncia não pode ter "REVISAR"; na `folha.png` a legenda tem que estar legível e as fotos não podem mostrar texto embutido; 1080x1920, 30 fps, 16 a 30 s, cerca de -14 LUFS.
5. **Montar o pacote**: vídeo + legenda + hashtags + link do produto + horário (ver `references/publicacao.md`).
6. **Publicar ou agendar** no horário do slot pela sessão do PC: trilha em alta em volume baixo, rótulo de IA ligado; produto linkado só quando a conta tiver permissão.
7. **Registrar** em `metricas/posts.csv`: id do post, data/hora, link do vídeo publicado, ângulo, gancho, duração.

## Ritmo da semana 1 (14/10 a 21/10/2026)

- A partir de 15/10: **3 posts por dia, 12:00, 18:00 e 21:00 (horário de Brasília, UTC-3)**, provisórios (não há dados confiáveis de vendedores do nicho; testar com as métricas). Séries: "Treino de 5 minutos em casa" (12:00, 1 por dia), "Mito ou verdade" sobre treinar em casa (18:00), e às 21:00 "Achado da semana" aos sábados e demonstração de treino em casa de segunda a sexta. O produto aparece em no máximo 1 de cada 3 posts. Em 14/10 valem ainda o 18:00 (P02, mantido) e os posts cancelados por pedido do usuário (P03 e P29). Os horários podem mudar com base nos dados (regras em `references/relatorio.md`).
- **Relatório diário** no fim de cada dia (23:20 de Brasília): alcance, retenção e conversão por post e por horário, decisão do dia seguinte.
- Variar ângulo, gancho e ordem das cenas a cada post: 3 vídeos por dia do mesmo produto, com a mesma voz e as mesmas fotos, viram "conteúdo repetido" se o começo for igual.

## Referências

- `references/pesquisa.md`: como pesquisar produtos e concorrentes no TikTok (método da skill tiktok-shop-research).
- `references/pipeline.md`: como gerar o vídeo no PC ou na nuvem, ajustes de pronúncia e problemas conhecidos.
- `references/roteiro-e-legenda.md`: fórmula de roteiro, banco de ganchos, regras de legenda e hashtags.
- `references/publicacao.md`: checklist de publicação e agendamento.
- `references/relatorio.md`: como coletar as métricas, modelo do relatório e regras para mudar horários.
- `references/conta-e-bio.md`: estratégia do link na bio, afiliação, acesso à conta, política de comentários e limites.
- `references/atendimento-dm.md`: resposta às DMs de interessados (link de afiliado da semana, plano B Linktree, transparência, limites).
