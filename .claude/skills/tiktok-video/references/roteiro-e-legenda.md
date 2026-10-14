# Roteiro, ganchos, legenda e hashtags

## Fórmula do roteiro (18 a 30 s, 5 a 11 falas curtas)

| Tempo | Bloco | Regra |
|---|---|---|
| 0 a 2,5 s | **Gancho** | pergunta ou afirmação que para o dedo. Uma ideia só. Nunca começar com "Oi, gente". |
| 2,5 a 9 s | **Demonstração** | o "seis em um" virando halter, barra, kettlebell, apoio de flexão (cenas em sequência rápida). |
| 9 a 16 s | **Detalhe/prova** | peso ajustável, trava de segurança, não risca o piso, nota e vendidos (do dia). |
| 16 a 22 s | **Preço/valor** | preço do dia + frete grátis (se verificado). Sem "só hoje". |
| últimos 3 s | **Chamada** | **Fase 1 (sem carrinho):** "Segue o perfil pra ver mais achados de treino em casa", "Salva esse vídeo, e segue pra mais achados", "Comenta..., e segue pra ver mais". **Fase 2 (com produto ligado):** "Toca no carrinho laranja" e variações. |

Para variar entre posts do mesmo dia: mudar o gancho, a ordem de demonstração/prova, as cenas (`inverter`), e terminar às vezes sem falar preço.

## Banco de ganchos (todos verdadeiros para o Kit 6 em 1)

| Ângulo | Gancho |
|---|---|
| A. Preço | "Academia em casa por menos de duzentos reais, e com frete grátis?" (só se preço do dia < R$ 200 e frete grátis) |
| B. Rotina corrida | "Sem tempo pra ir pra academia?" |
| C. Mensalidade | "Pagando academia e não indo?" |
| D. Transformação | "Um conjunto só, seis jeitos de treinar." |
| E. Pergunta | "Halter, barra ou quétoubél: qual você usaria primeiro?" |
| F. Iniciante | "Quer começar a treinar em casa, mas não sabe que peso comprar?" |
| G. Espaço | "Mora em apartamento pequeno?" |
| H. Prova social | "Mais de sete mil pessoas já levaram esse aqui." (vendidos do dia) |
| I. Conteúdo do kit | "Olha tudo o que vem nessa caixa." |
| J. Presente | "Presente pra quem vive dizendo que segunda começa." |

Proibido no gancho e no roteiro: promessa de corpo/resultado, "milagre", "secar", antes e depois, "substitui a academia" como fato, contagem regressiva, valor de mensalidade de academia (não verificado).

## Legenda

- 1 a 3 frases, até ~150 caracteres antes das hashtags. Primeira frase = benefício ou pergunta (aparece na tela).
- Terminar com "Segue pra mais achados 🧡" (fase 1) ou "carrinho laranja 🧡" (só na fase 2), ou com pergunta que puxe comentário ("Qual você usaria primeiro? 👇").
- Não repetir o texto do vídeo palavra por palavra; complementar (ex.: o que vem no kit).
- Não copiar o título do anúncio: vídeos que fazem isso tiveram 1 a 9 curtidas.

**Legenda padrão (fork):**
> Academia em casa sem mensalidade 🏋️‍♀️ 8 anilhas, barras, alças de kettlebell e travas num kit só. Prático de montar e cabe no bolso. Segue pra ver mais achados 🧡

(Na fase 2, a última frase volta a ser "Tá no carrinho laranja 🧡", como no fork.)

## Legenda na tela (obrigatória em vídeo narrado)

- Blocos curtos (até ~18 caracteres, 2 a 4 palavras), branco grosso com contorno preto, na faixa central-baixa da tela (acima do nome, da legenda do post e dos botões).
- Números em algarismos (R$ 184,90, 15 kg, 4,6): a tabela `EXIBIR` em `pipeline/legendas.py` converte. Se o preço mudar, acrescente a nova frase falada nessa tabela ou ponha `"legenda"` na fala do roteiro.

## Hashtags (4 a 6)

- **Núcleo (sempre):** `#treinoemcasa #academiaemcasa #tiktokshop`
- **Produto (1 ou 2, alternar):** `#halteres` `#kettlebell` `#kitdetreino` `#musculacao`
- **Alcance (1, alternar):** `#ViralTikTokShop` `#achadinhos` `#achadostiktokshop`
- **Campanha:** a partir de 27/10, a hashtag oficial da Black Friday do TikTok Shop (confirmar no Seller Center/perfil oficial antes). Nunca usar campanha que já passou (`#TikTokShopBR1010`).
- **Afiliado:** `#publi` quando a conta ganha comissão.

Padrão do fork: `#treinoemcasa #academiaemcasa #halteres #kettlebell #ViralTikTokShop #tiktokshop`
