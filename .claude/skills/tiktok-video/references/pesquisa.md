# Pesquisa de produto e concorrência (método da skill tiktok-shop-research)

Só leitura. Usar o navegador onde a conta do usuário já está conectada (o TikTok Shop mostra CAPTCHA para visitante). Se aparecer "Verify to continue" ou quebra-cabeça: parar e avisar.

## Passo a passo

1. **Páginas de descoberta:** `tiktok.com/discover/<slug>`. Slugs inventados caem na home; achar slugs reais com WebSearch usando `allowed_domains: ["tiktok.com"]`. Fechar o popup de login ("Pular").
2. **Cada vídeo candidato:** abrir a página do vídeo e ler (trecho abaixo):
   - Data: `BigInt(idDoVideo) >> 32n` = timestamp Unix em segundos.
   - Métricas: `data-e2e` = `like-count`, `comment-count`, `favorite-count`, `share-count`. Visualizações não aparecem na página do vídeo.
   - Descrição: `data-e2e="browse-video-desc"` ou `video-desc`.
   - Produto linkado: procurar `shop.tiktok.com/br/pdp/<id de 15+ dígitos>` no HTML (trocar `/` por `/` antes).
   - "Parceria paga" perto da descrição = conteúdo pago pela marca.
3. **Cada produto:** `https://shop.tiktok.com/br/pdp/<id>`: título, preço de venda, frete, "N vendido(s)", nota e nº de avaliações. Conferir o preço com captura de tela (o texto às vezes traz preço de variação ou preço riscado).
4. **Concorrência:** `tiktok.com/search?q=<termo>`: quantos criadores falam do mesmo produto e quantos são "Parceria paga".
5. **Janela de tempo:** só chamar de "últimos 7 dias" o que tem data dentro do período.

```js
(async () => {
  for (let i = 0; i < 20 && !document.querySelector('[data-e2e="like-count"]'); i++) await new Promise(r => setTimeout(r, 500));
  const bs = String.fromCharCode(92);
  const html = document.documentElement.innerHTML.split(bs + 'u002F').join('/').split(bs).join('');
  const ids = [...new Set([...html.matchAll(/shop\.tiktok\.com\/br\/pdp\/(\d{15,})/g)].map(m => m[1]))];
  const vid = location.pathname.split('/video/')[1] || '';
  const date = vid ? new Date(Number(BigInt(vid.split('?')[0]) >> 32n) * 1000).toISOString().slice(0, 10) : null;
  const e = s => (document.querySelector('[data-e2e="' + s + '"]') || {}).innerText || null;
  const descEl = document.querySelector('[data-e2e="browse-video-desc"], [data-e2e="video-desc"]');
  return { author: location.pathname.split('/')[1], date, likes: e('like-count'), comments: e('comment-count'),
           favorites: e('favorite-count'), shares: e('share-count'), desc: descEl && descEl.innerText, productIds: ids };
})()
```

## Sem navegador (sessão na nuvem)

A rede da nuvem bloqueia tiktok.com. Para dados públicos de perfis e vídeos, usar o conector **TokScript**:
- `get_tiktok_user` (seguidores, curtidas, nº de vídeos) e `get_tiktok_user_videos` (vídeos com visualizações, curtidas, comentários, compartilhamentos).
- Não dá preço nem vendidos do anúncio: isso exige o navegador do PC.

## Critério de "hidden gem" (4 sinais juntos)

Demanda forte em vídeos recentes; poucos criadores no mesmo produto; preço e margem viáveis para CPF (ticket baixo/médio, frete que não destrói a margem); fácil de demonstrar em vídeo curto e de enviar/devolver.

**Alertas:** muitos vídeos "Parceria paga"; produto grande/pesado ou ticket acima de ~R$ 150 sem prova de vendas; engajamento só em vídeo "faça você mesmo"; nota baixa ou poucas avaliações.

## Limitações conhecidas (14/10/2026)

- Sem Kalodata, FastMoss, EchoTik (pagos) nem Creative Center Top Products.
- `tiktok.com/shop/k/...` pede CAPTCHA; `shop.tiktok.com/br/search` dá 404.
