# Relatório diário (fim de cada dia, 23:20 de Brasília)

Objetivo da semana 1: **aumentar o alcance da conta** e descobrir o melhor horário e o melhor ângulo, sem perder de vista a conversão (cliques no produto e pedidos).

## 1. Coletar

**Automático (nuvem, conector TokScript, dados públicos):**
- `get_tiktok_user("asadelta.shop")`: seguidores, curtidas totais, nº de vídeos.
- `get_tiktok_user_videos` **exige plano pago do TokScript** (testado em 14/10): não usar. Os números por vídeo vêm do TikTok Studio, lidos pela sessão do PC às 22:40 (agendamento "Coleta de métricas no TikTok Studio (PC)").
- Gravar uma linha por vídeo em `metricas/snapshots.csv` com a idade do vídeo em horas (agora − hora de publicação).

**Do TikTok Studio / Seller Center (só o usuário ou a sessão do PC conseguem ver):**
- Retenção: tempo médio assistido, % que assistiu inteiro, % que passou dos 2 primeiros segundos.
- Origem do tráfego: % "Para você".
- Novos seguidores por vídeo.
- Loja: impressões e cliques no produto, pedidos, GMV, comissão.

Se esses dados não vierem, o relatório diz "não disponível" (nunca estimar). **Pedidos, GMV e comissão não vão para o git** (repositório público): ficam só no relatório entregue no chat.

## 2. Calcular

| Indicador | Fórmula | Leitura |
|---|---|---|
| Alcance 3 h / 24 h | visualizações com ~3 h e ~24 h de vida | comparar posts só na mesma idade |
| Engajamento | (curtidas + comentários + compart. + salvos) / visualizações | > 5% é bom para conta nova |
| Compartilhamento | compart. / visualizações | sinal forte de alcance |
| Retenção | tempo médio / duração; % até o fim | gancho bom = % que passa de 2 s alto |
| Clique no produto | cliques / visualizações | mede a chamada e o preço |
| Conversão | pedidos / cliques | mede anúncio, preço e frete |

## 3. Decidir (regras)

**Horários (10h, 15h, 20h):**
1. Comparar horários pela **mediana das visualizações com 24 h** de cada horário, e cada ângulo aparece em mais de um horário (o calendário já roda os ângulos) para não confundir horário com conteúdo.
2. Só mexer depois de **3 posts por horário** (primeira decisão possível no relatório de 17/10, valendo a partir de 18/10).
3. Se um horário ficar abaixo de **60% do melhor** em 2 relatórios seguidos: trocar esse horário por um candidato por 2 dias (candidatos: 07:30, 12:00, 18:00, 21:30) e ficar com o que for melhor.
4. Mudar **no máximo 1 horário por dia** e manter 3 posts por dia.
5. Quando a conta passar de 100 seguidores, usar também TikTok Studio → Seguidores → horários mais ativos.

**Conteúdo:**
- Ordenar os ângulos por retenção (ou, sem ela, por alcance 24 h) e depois por clique no produto.
- Dias 5 a 7: trocar os 2 piores ângulos por variações dos 2 melhores (novo gancho, mesmas ideias), mantendo a regra de não repetir o mesmo começo no mesmo dia.
- Se o alcance de todos os posts ficar abaixo de 200 visualizações com 24 h por 2 dias: checar sinais de conteúdo repetido (começos parecidos, mesma capa), rótulo de IA, limite de vídeos com produto, e propor ao usuário gravar tomadas reais do produto.

## 4. Modelo do relatório

```markdown
# Relatório TikTok @asadelta.shop: DD/MM/AAAA (dia N de 7)

**Resumo:** 3 linhas com o principal resultado e a decisão.

## Conta
Seguidores X (Δ +Y) · curtidas totais X · vídeos X

## Posts do dia
| Post | Hora | Ângulo | Idade (h) | Views | Curt. | Com. | Comp. | Salv. | Eng. | Retenção | Cliques | Pedidos |

## Por horário (semana até agora)
| Horário | Posts | Mediana views 24 h | Melhor post |

## Por ângulo
| Ângulo | Posts | Views médias | Retenção média | Cliques |

## O que aprendemos
- ...

## Decisões para amanhã
- Horários: mantém 10h/15h/20h (ou troca X por Y, motivo)
- Ajustes nos roteiros/legendas de amanhã: ...

## Dados que faltaram
- ...
```

Arquivo: `relatorios/AAAA-MM-DD.md` (só dados públicos) + resumo completo no chat.
