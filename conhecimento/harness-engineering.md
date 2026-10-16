# Engenharia de harness (harness engineering)

Nota de conhecimento mantida pelo agente Gerente. Última atualização: 16/10/2026.

## 1. Definição de trabalho

**Harness** é tudo o que envolve o modelo num agente, exceto o próprio modelo: o laço de execução, as ferramentas e suas descrições, a gestão de contexto, a memória e o estado, as permissões, a verificação e a observabilidade. A ideia central: o modelo pensa, o harness organiza e limita a ação.

Fórmula usada em vários textos: **Agente = Modelo + Harness**.

## 2. Fontes verificadas e como usar cada uma

| Fonte | Tipo | Status |
|---|---|---|
| [Anthropic, "Harness design for long-running apps"](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Post oficial | Lido direto |
| [Anthropic, "Building effective agents"](https://www.anthropic.com/engineering/building-effective-agents) | Post oficial | Lido direto |
| [Böckeler, harness engineering for coding agent users (martinfowler.com)](https://martinfowler.com/articles/harness-engineering.html) | Artigo de referência | Lido por completo, em imagens enviadas pelo usuário (15 partes) |
| [arXiv 2606.20683, survey sobre harness](https://arxiv.org/pdf/2606.20683) | Survey acadêmico | Só o resumo nas buscas. Não lido na íntegra |

Blogs e agregadores (glossários, SEO, cursos) foram usados só como pista. Números e limites que aparecem neles (por exemplo, "gatilho de compactação em 40%") não são confirmados pela Anthropic e não devem orientar decisões.

## 3. O que as fontes oficiais dizem

**Anthropic, agentes eficazes (padrões):**
- Comece pela opção mais simples: uma chamada ao modelo com recuperação e exemplos. Só acrescente complexidade se melhorar o resultado de forma mensurável.
- Padrões de fluxo de trabalho, em que o código controla o caminho: encadeamento de prompts, roteamento, paralelização, orquestrador com trabalhadores, avaliador-otimizador.
- Agente é o modelo que direciona o próprio processo e usa ferramentas em laço. Exige caixas de proteção, condições de parada e testes em sandbox.
- Ferramentas merecem tanto cuidado de design quanto as interfaces humanas: descrições claras, exemplos, casos de borda, e formato que o modelo usa com naturalidade. Tornar a ferramenta difícil de usar errado (por exemplo, exigir caminho absoluto) elimina classes inteiras de erro.
- Torne visíveis as etapas de planejamento.

**Anthropic, harness para apps de longa duração:**
- Quando o contexto enche, o modelo pode perder coerência e encerrar o trabalho cedo ("ansiedade de contexto"). Há dois remédios: **reset de contexto** (agente novo com resumo estruturado do estado) e **compactação** (resumo no mesmo contexto). O reset dá um começo limpo; a compactação preserva continuidade.
- Separar papéis: planejador (escopo), gerador (produz) e avaliador (testa e critica).
- Agentes tendem a elogiar o próprio trabalho. Um avaliador separado é mais fácil de calibrar para ser cético do que pedir ao gerador que se critique. O avaliador também é um LLM e pode ser leniente: precisa de critérios explícitos, exemplos de calibração e leitura dos rastros.
- Todo componente do harness é uma suposição sobre o que o modelo não faz sozinho. Essas suposições envelhecem: ao sair um modelo novo, reavalie e remova o que não serve mais.
- Comece simples; acrescente complexidade só com evidência. Leia os rastros do modelo em problemas reais e ajuste contra eles.
- Resultado citado: uma execução solo de 20 minutos (US$ 9) produziu um jogo quebrado; o harness completo (6 horas, US$ 200) produziu um jogo jogável. O avaliador vale o custo em tarefas que o modelo não resolve bem sozinho; com modelos mais novos, ele pode ser simplificado.

**Böckeler, "Harness engineering for coding agent users" (lido por completo):**

*Enquadramento*
- Para deixar agentes de código trabalharem com menos supervisão, precisamos de confiança no resultado. A barreira de confiança existe porque LLMs não são determinísticos, não conhecem o contexto, não entendem o código de fato e "pensam em tokens".
- "Agent = Modelo + Harness" é uma definição ampla demais. Para agentes de código, o harness tem duas partes: o **harness interno** (construído por quem fez o agente: prompt de sistema, busca de código, orquestração) e o **harness externo** (construído pelo usuário para o próprio sistema). A autora trata o externo como o que importa para nós.
- Objetivos do harness externo: aumentar a chance de acerto na primeira tentativa, corrigir o máximo de problemas antes de chegar ao humano, reduzir o trabalho de revisão e gastar menos tokens com retrabalho.

*Modelo de controle*
- **Guias (feedforward):** antecipam o comportamento e orientam antes da ação. Ex.: princípios, regras, documentos de referência, how-tos, servidores de linguagem, CLIs e scripts, modificações automáticas de código.
- **Sensores (feedback):** observam depois da ação para o agente se corrigir. Ex.: análise estática, agentes revisores, logs, navegador. Mensagens de linter escritas para o próprio LLM são um tipo "positivo" de injeção de prompt.
- Só guias: o agente repete os mesmos erros sem saber se as regras funcionaram. Só sensores: o agente corrige, mas não aprende a evitar o erro. Os dois juntos são necessários.
- **Computacional** (determinístico, rápido, confiável; roda a cada mudança) e **inferencial** (semântico, LLM como juiz; mais caro e menos determinístico; melhor com um modelo forte).
- Exemplos: convenções em AGENTS.md ou skills são guias inferenciais; uma skill com instruções e script de bootstrap é ambos; modificações com OpenRewrite são guia computacional; testes de arquitetura (ArchUnit) num hook de pré-commit são sensor computacional; instruções de revisão em skill são sensor inferencial.

*Timing: "manter a qualidade à esquerda"*
- Rápido (antes do commit): linters, testes rápidos, revisor básico. Caro (após a integração): mutation testing, revisão ampla, revisão de arquitetura.
- Laço de autocorreção com controles rápidos, revisão humana, e o pipeline rodando tudo.
- Deriva contínua: código morto, qualidade da cobertura, scanners de dependência, fora do ciclo de mudanças.
- Feedback de execução: latência, taxa de erro, disponibilidade, anomalias de log e amostragem de qualidade de resposta por um juiz de IA.

*Steering loop (direção humana)*
- O trabalho humano é dirigir o agente ajustando o harness: quando um problema se repete, melhore guias e sensores para que ele seja menos provável ou impossível.
- A IA também ajuda a criar controles: testes estruturais, regras a partir de padrões observados, linters, guias a partir da arqueologia do código.

*Relação com engenharia de contexto*
- Engenharia de contexto dá os meios para tornar guias e sensores disponíveis ao agente. O harness de um agente de código é uma forma específica dela.

*Categorias de regulação*
- O harness age como um governador cibernético que combina antecipação e feedback para levar o código a um estado desejado. Separar as dimensões desse estado torna a linguagem mais precisa.
- **Manutenibilidade:** a mais madura, porque há ferramental pronto. Sensores computacionais pegam bem código duplicado, complexidade ciclomática, falta de cobertura de testes, deriva de arquitetura e violações de estilo, com custo baixo e resultado determinístico. LLMs cobrem parte do que exige julgamento semântico (código semanticamente duplicado, testes redundantes, soluções de força bruta, superengenharia), mas de forma cara e probabilística, e não em todo commit. Nenhum dos dois pega de forma confiável diagnóstico errado, superengenharia por funcionalidade desnecessária ou instrução mal entendida. Correção fica fora de qualquer sensor se o humano não especificou o que queria.
- **Adequação da arquitetura (fitness functions):** guias que definem as características da aplicação e sensores que as verificam. Ex.: requisitos de desempenho como guia, testes de desempenho como sensor; padrões de logging como guia, e instruções para o agente avaliar a qualidade dos próprios logs.
- **Comportamento:** a parte mais difícil ("o elefante na sala"). Guias: especificação funcional, de prompt curto a descrições de vários arquivos. Sensores: a suíte de testes gerada pela IA passar, ter boa cobertura, e às vezes mutation testing, combinados com teste manual. A autora diz que isso ainda depende demais de testes gerados por IA, que não são bons o bastante. O padrão de fixtures aprovadas ajuda em algumas áreas. Ainda há muito a resolver.

*Harnessability*
- Nem todo código é igualmente "harnessável". Linguagem tipada permite checagem de tipos como sensor. Limites de módulo claros permitem regras de arquitetura. Frameworks escondem detalhes que o agente nem precisa considerar.
- Projetos novos (greenfield) podem embutir harnessability desde o início, com decisões de tecnologia e arquitetura. Sistemas legados, com muita dívida técnica, enfrentam o problema mais difícil: o harness é mais necessário onde é mais difícil construí-lo.

*Templates de harness*
- Empresas têm poucas topologias de serviço que cobrem a maioria das necessidades. Um template de harness empacota guias e sensores para a estrutura, convenções e stack de uma topologia.
- Os mesmos problemas dos templates de serviço: quando instanciados, saem de sincronia com melhorias upstream. Como guias e sensores de harness são não determinísticos e difíceis de testar, o problema pode ser pior.

**Survey arXiv 2606.20683 (resumo):** divide o harness em seis responsabilidades de execução: observação, contexto, controle, ação, estado e verificação/governança. Pergunta se o gargalo está no modelo, no harness ou no acoplamento entre eles.

## 4. Princípios práticos (consolidados)

1. **Simplicidade primeiro.** Um laço com poucas ferramentas bem descritas vence um sistema complexo mal testado.
2. **Ferramentas à prova de erro.** Parâmetros claros, caminhos absolutos, validação na entrada.
3. **Guias antes, sensores depois.** Impeça o erro com instruções, permissões e formato antes da ação; verifique com testes e revisão depois.
4. **Separe quem produz de quem confere.** O avaliador precisa de critérios escritos e de calibração com exemplos.
5. **Estado explícito.** Handoff estruturado entre sessões: o que está feito, o que falta, o que travou.
6. **Limites e paradas.** Toda ação com efeito externo (publicar, agendar, excluir) precisa de condição de parada e de confirmação humana.
7. **Reavaliação a cada modelo novo.** Remova o que virou desnecessário; teste o que o modelo novo permite.
8. **Medir, não achar.** Avalie o harness com tarefas reais e métricas, não com impressão.

## 5. Aplicação no nosso projeto (@asadelta.shop)

O nosso fluxo já tem partes de um harness:

| Peça do harness | No projeto |
|---|---|
| Guias (antes da ação) | Regras da skill `tiktok-video`, o checklist de publicação, a política de personagens, a regra de legenda na tela |
| Sensores (depois da ação) | Conferência da nuvem (duração, LUFS, quadros, legenda), checagem do Studio, folha de quadros |
| Avaliador separado | Conferência do Atendimento e do Gerente antes de agendar |
| Estado e handoff | `plano/estado.json`, o arquivo "Onde paramos" no vault, as notas de decisão |
| Limites e paradas | Nada publicado ou agendado sem o OK da nuvem e do usuário; verificação de retomada com condição de desligamento |
| Permissões | Permissões por ferramenta no `.claude/settings.json` |

Lacunas identificadas:
- Sensores inferenciais (LLM como juiz) só existem de forma informal. Falta critério escrito e calibração com exemplos aprovados e reprovados.
- O estado entre sessões depende de notas manuais; falta um formato de handoff padronizado para cada função.
- Não há medição do harness: não sabemos quantas revisões um pacote exige nem quanto cada etapa custa em tempo.

## 6. Próximos passos sugeridos (para o Gerente)

1. ~~Abrir e ler o artigo de Böckeler / Fowler diretamente~~ — feito em 16/10, por imagens enviadas pelo usuário.
2. Ler na íntegra o survey arXiv 2606.20683 e registrar a taxonomia de seis responsabilidades contra o nosso fluxo.
3. Escrever um critério de avaliação por tipo de post (gancho, legenda, segurança, marca) com exemplos aprovados e reprovados, para o avaliador humano-LLM.
4. Padronizar o handoff entre funções (formato fixo: feito, pendente, bloqueio, próxima ação).
5. Medir por pacote: número de revisões, tempo de render, tempo até o agendamento.
