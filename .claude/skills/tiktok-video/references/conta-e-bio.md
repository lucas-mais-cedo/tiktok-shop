# Conta @asadelta.shop: link na bio, afiliação, comentários e limites do acesso

Decidido pelo usuário em 14/10/2026: sem CNPJ nem MEI e abaixo de 1.000 seguidores, o caminho de venda é **o link de afiliado na bio do perfil** (direto ou por um Linktree com o nome de cada produto). Até chegar a 1.000 seguidores, **o objetivo nº 1 é ganhar seguidores**; vender é bônus.

Estado atual: `plano/estado.json`. Os roteiros só falam "link na bio" quando `bio_link_ativo` for `true`.

## O que decide se o plano do link na bio funciona

Fontes de terceiros (não encontrei texto oficial do TikTok, e elas divergem):

- A maioria diz que o campo **"Site"** do perfil só aparece em **conta pessoal com 1.000+ seguidores**. Uma fonte diz que o mínimo acabou em 2024.
- **Conta Business** libera o link sem mínimo de seguidores, mas **só deixa usar a Biblioteca de Música Comercial**: isso conflita com "trilha em alta" (pedido do usuário). Não verifiquei se mudar para Business afeta o programa de afiliados/criadores do TikTok Shop. **Não trocar de tipo de conta sem decisão do usuário.**

**Teste (1 minuto, no app, em conta pessoal):** Perfil → Editar perfil → campo **Site**.
- Aparece: o plano funciona já. Usar.
- Não aparece: o link na bio só existe aos 1.000 seguidores. Nesse ponto o cadastro de afiliado com carrinho no vídeo também abre, e o carrinho passa a ser o caminho principal. Até lá, a chamada continua "segue/salva/comenta". Ou o usuário escolhe migrar para Business, ciente de que perde as músicas em alta.

## Ordem para ativar o link (o que só o usuário pode fazer)

1. **Verificação de identidade (PKYC) concluída.** Fontes dizem que, sem ela, os cliques não geram comissão. Documentos e selfie: só o usuário faz, no app. A IA nunca lida com documentos.
2. **Linkshare disponível na conta** (aparece no app depois do PKYC; confirmar o caminho no app).
3. **Produto elegível:** gerar o link do Kit 6 em 1 da ART CADEIRAS. Nem todo produto tem comissão de afiliado liberada. Conferir a **% de comissão** e se o link é do anúncio certo (`pdp 1737041809079633642`). Fontes citam atribuição de 14 dias após o clique e link válido por até 100 dias.
4. **Campo Site** liberado (teste acima).
5. Colocar o link: **1 produto** = o link do Linkshare direto no campo Site (menos etapas, menos risco). **2 ou mais produtos** = Linktree (ou página própria) com o nome do produto e o link de cada um.
6. Mudar `plano/estado.json` para `bio_link_ativo: true`, `bio_link_tipo` e `linkshare...`. A partir daí os roteiros e legendas passam a usar a chamada "link na bio".

Regras do link:
- Só links oficiais que levem ao TikTok Shop. O guia do TikTok Seller BR diz que a plataforma não responde por links de terceiros; não achei regra oficial que proíba ou autorize Linktree na bio. Risco baixo a moderado: se a bio ou os vídeos forem limitados, voltar ao link direto.
- Não gravar o link de afiliado em repositório público. O repositório vai ficar privado.
- Divulgar a comissão: com link de afiliado na bio, usar **`#publi`** na legenda e acionar, ao publicar, a opção de **divulgação de conteúdo/conteúdo de marca** do TikTok quando ela se aplicar à publicação (a opção pode limitar o som à Biblioteca de Música Comercial: confirmar no 1º post e avisar o usuário).
- Comissão recebida como pessoa física pode ter regra de imposto de renda; confirmar com contador. Não sou contador, não vou orientar sobre isso.

## Chamadas (CTA) por estado

| Estado | Última fala do vídeo | Final da legenda |
|---|---|---|
| `bio_link_ativo: false` | "Segue o perfil pra ver mais achados." | "Segue pra mais achados 🧡" |
| `bio_link_ativo: true` | "Segue, e o link tá na bio." | "Link na bio 🧡 #publi" |

Nunca escrever "link na bio" antes de o link estar ativo e testado (abrir o perfil de fora e clicar).

## Acesso à conta: como funciona e o que ficou combinado

**Sem senha.** O usuário entra **uma vez**, ele mesmo, no navegador do app Claude Desktop (tiktok.com). O navegador guarda o login; a IA usa a sessão aberta e nunca vê nem digita a senha. Verificação em duas etapas, CAPTCHA e desafios de segurança: o usuário resolve. Aprovar o site `tiktok.com` (escopo "site") quando o app perguntar evita pedido a cada ação.

### O que a IA faz sozinha (dentro do plano)
- Publicar e agendar os posts do calendário, com trilha, rótulo de IA e legenda.
- Editar a **bio** só com o texto aprovado pelo usuário (modelo abaixo).
- **Responder comentários** de dúvida sobre o produto e agradecer, pela política abaixo.
- Fixar um comentário útil e **ocultar spam e links suspeitos** nos comentários.
- Ler métricas do TikTok Studio e entregar o relatório.

### O que sempre pede "ok" do usuário (cada vez)
- Mudar **nome, foto, @usuário** ou tipo de conta (Pessoal ↔ Business).
- Publicar algo **fora do calendário** ou trocar o produto em foco.
- Responder **reclamação, pedido de reembolso, problema de entrega, ameaça ou assunto jurídico**: a IA só prepara a resposta.
- Mudar o **link da bio** para outro destino.
- Qualquer ação em **Shop/Linkshare**: cadastro, aceitar termos, vincular conta bancária, saque.

### O que a IA nunca faz
- Alterar senha, e-mail, telefone, verificação em duas etapas, dados de pagamento ou documentos.
- Comprar, pagar, sacar, apagar a conta ou vídeos já publicados sem pedido explícito.
- Seguir, curtir ou comentar **em massa**, **iniciar** conversa por DM (responder quem escreveu primeiro é permitido: ver `atendimento-dm.md`), usar bot de engajamento, comprar seguidores.
- Inventar experiência pessoal ("eu usei e amei", "já comprei"), fingir ser a loja vendedora, prometer prazo, estoque ou desconto que o anúncio não mostra.

### Ritmo humano (proteção da conta)
O TikTok pode limitar contas com atividade que parece automática. Por isso: no máximo ~10 respostas por hora e ~30 por dia nas primeiras semanas, com texto diferente em cada uma e intervalos de alguns minutos; nada de ações repetidas em sequência rápida; se aparecer aviso de "atividade incomum", **parar** e avisar o usuário.

## Política de respostas a comentários

- Responder em português, curto, simpático e igual ao tom do vídeo. Sem emoji em excesso.
- Só falar do que está no anúncio verificado (conteúdo do kit, peso ajustável até 15 kg, preço/frete do dia). Prazo de entrega, estoque, garantia, devolução e cor: "Confere na página do produto pelo link da bio" (quando ativo) ou "Vou confirmar e te respondo" (e avisar o usuário).
- Pergunta "é anúncio?" / "você ganha comissão?": responder **a verdade** ("Sim, sou afiliado: se comprar pelo link, eu recebo uma comissão, sem custo extra pra você").
- Pergunta sobre resultado físico ("emagrece?", "dá massa?"): "O kit é um equipamento de treino; resultado depende da sua rotina."
- Comentário ofensivo, spam ou golpe: ocultar/denunciar, não responder. Reclamação: preparar resposta e pedir ok.
- Cada resposta é registrada em `metricas/comentarios.csv` (data, vídeo, tipo, resumo, respondido: sim/não/pendente). Sem nome ou @ de terceiros no repositório.

## Modelo de bio (precisa do ok do usuário antes de aplicar)

Até 80 caracteres no TikTok. Sugestão para `bio_link_ativo: false`:
> Achados de treino em casa 🏋️‍♀️ Dicas e ofertas

Quando o link estiver ativo:
> Achados de treino em casa 🏋️‍♀️ Link do kit abaixo 👇

(A bio atual está vazia, em 14/10/2026. Foto e nome "Asa Delta Shop" já existem.)
