---
name: tiktok-video
description: TikTok-Video. Gestão de social media da conta @asadelta.shop no TikTok Shop Brasil, do roteiro à análise. Use para criar vídeos de venda (narração pt-BR + fotos do anúncio, sem texto na tela), escrever legenda e hashtags, montar e seguir o calendário de postagens (10h, 15h e 20h de Brasília), preparar o pacote de publicação e fazer o relatório diário de alcance, retenção e conversão. Foco atual - Kit 6 em 1 da loja ART CADEIRAS.
---

# TikTok-Video

Skill de gerente de social media da conta **@asadelta.shop** (TikTok Shop Brasil). Junta o que foi feito nos chats "TikTok Shop fitness hidden gems" (pesquisa), "Vídeo promocional TikTok Shop fitness" (1º vídeo) e o fork "Editor de Videos" (versão de referência e legenda final).

## Antes de tudo

- **Idioma:** responder sempre em português do Brasil, com linguagem simples. Antes de cada passo, um aviso de uma frase.
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
9. **Repositório público:** este repositório (`lucas-mais-cedo/tiktok-shop`) é público. Não gravar aqui senha, e-mail, dados pessoais, nem faturamento/pedidos. Números de vendas ficam no relatório entregue ao usuário (artifact/chat), não no git, até o repositório virar privado.

## Fluxo de um post (checklist)

1. **Pegar o slot** em `plano/semana-01.md` (ângulo, gancho, roteiro, cenas, legenda).
2. **Revalidar o anúncio** (preço, frete, vendidos, nota). Se mudou, ajustar a fala de preço/prova no `roteiro.json` e a legenda. Se não der para verificar, **tirar** a fala de preço/prova (não chutar).
3. **Gerar o vídeo** (ver `references/pipeline.md`):
   `python -I pipeline/make_post.py plano/semana-01/<post>/roteiro.json <pasta_fotos>`
   Saída principal: `<post>_so-voz.mp4` (prioridade: só voz). Também sai `<post>_com-musica.mp4`.
4. **Conferir:** a conferência de pronúncia não pode ter "REVISAR"; a `folha.png` não pode mostrar texto embutido das fotos; 1080x1920, 30 fps, 18 a 30 s, cerca de -14 LUFS.
5. **Montar o pacote**: vídeo + legenda + hashtags + link do produto + horário (ver `references/publicacao.md`).
6. **Publicar ou agendar** no horário do slot, com o produto linkado (carrinho laranja) e o rótulo de IA.
7. **Registrar** em `metricas/posts.csv`: id do post, data/hora, link do vídeo publicado, ângulo, gancho, duração.

## Ritmo da semana 1 (14/10 a 21/10/2026)

- 3 posts por dia: **10:00, 15:00 e 20:00 (horário de Brasília, UTC-3)**. Os horários podem mudar com base nos dados (regras em `references/relatorio.md`).
- **Relatório diário** no fim de cada dia (23:20 de Brasília): alcance, retenção e conversão por post e por horário, decisão do dia seguinte.
- Variar ângulo, gancho e ordem das cenas a cada post: 3 vídeos por dia do mesmo produto, com a mesma voz e as mesmas fotos, viram "conteúdo repetido" se o começo for igual.

## Referências

- `references/pesquisa.md`: como pesquisar produtos e concorrentes no TikTok (método da skill tiktok-shop-research).
- `references/pipeline.md`: como gerar o vídeo no PC ou na nuvem, ajustes de pronúncia e problemas conhecidos.
- `references/roteiro-e-legenda.md`: fórmula de roteiro, banco de ganchos, regras de legenda e hashtags.
- `references/publicacao.md`: checklist de publicação e agendamento.
- `references/relatorio.md`: como coletar as métricas, modelo do relatório e regras para mudar horários.
