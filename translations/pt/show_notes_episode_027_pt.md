# Episódio 27: Pilha de Dreams, Prescrições de IA, Agentes Shell, e o Custo dos Secretários

**OpenClaw Daily** | 9 de abril de 2026 | ~33 min

## Título do Episódio
**Pilha de Dreams, Prescrições de IA, Agentes Shell, e o Custo dos Secretários**

## Tagline
O OpenClaw 2026.4.9 traz uma faixa de backfill REM grounded e timeline de diary estruturada, Utah permite que IA prescreva meds psiquiátricos, OpenAI dá aos agentes um shell real, STAT News reporta que secretários de IA estão silenciosamente inflando custos de saúde, e Yahoo aposta seu futuro de busca no Claude.

## Slate de Histórias

1. **OpenClaw 2026.4.9 — A Pilha de Memória Ganha uma Faixa de Dream Replay**
   O lançamento de hoje se concentra no sistema de memória e dreaming. A adição principal é uma faixa de backfill REM grounded com um CLI `rem-harness --path` — você agora pode alimentar notas diárias históricas de volta pelo pipeline de dreaming para que contexto antigo seja reproduzido em Dreams e memória durável sem manter uma pilha de memória separada. O Control UI ganha uma visão estruturada de diary com navegação por timeline, controles de backfill e reset, summaries de dreaming rastreáveis, e uma faixa de Scene com promotion hints. Também nesta versão: relatórios de avaliação de character-vibes para QA com comparação paralela de modelos, aliases de auth de provedor para que variantes de provedor possam compartilhar vars de ambiente e perfis de auth, e pinagem de CalVer para iOS para release trains. Correções de segurança: interações de browser não podem mais bypassar a Quarentena de SSRF via navegações de main-frame dirigidas por interação, e overrides de vars de ambiente de controle de runtime agora estão bloqueados de arquivos `.env` de workspace não confiáveis.

2. **Utah Permite que IA Prescreva Medicamentos Psiquiátricos**
   A Legion Health se tornou a primeira empresa de saúde mental autorizada sob a sandbox regulatória de IA do Utah a permitir que IA prescreva medicamentos psiquiátricos. Isso expande o piloto de janeiro de 2026 além de renewals de medicamentos de rotina para decisões completas de tratamento psiquiátrico. A IA prescreve sob supervisão médica dentro do framework de sandbox — mas a direção é clara: tomada de decisão médica autônoma de IA está se movendo upstream de renewals para diagnósticos. Vale discutir onde a responsabilidade fica quando a IA está errada, e se o enquadramento de "sandbox" está fazendo muito trabalho político aqui.

3. **OpenAI Responses API — Agentes Ganham um Shell Real**
   A OpenAI estendeu a Responses API com uma ferramenta de shell completa suportando Python, Node.js, Go, Java, Ruby e PHP rodando dentro de container workspaces hospedados. Agentes agora podem escrever código, executá-lo, inspecionar saída e iterar — tudo dentro de um ambiente server-side gerenciado com context compaction para tarefas de longa duração. Eles também introduziram "agent skills" reutilizáveis que podem ser empacotadas e referenciadas entre execuções. Esse é o sinal mais claro da OpenAI de que a Responses API é a superfície agentic séria, não a Assistants API.

4. **Secretários de IA Estão Aumentando Custos de Saúde — E Todos Sabem Disso**
   O STAT News reporta que seguradoras e hospitais privadamente concordam que secretários médicos de IA estão impulsionando custos — mas não há consenso sobre o que fazer. O mecanismo é "intensidade de codificação": secretários de IA são mais completos que anotadores humanos, captando mais detalhes faturáveis e codificando visitas mais completamente. Um estudo encontrou que secretários economizaram apenas 16 minutos por plantão de 8 horas apesar de aumentar despesas de visita. A parte desconfortável: ninguém na cadeia tem incentivo direto para empurrar de volta. Hospitais получают mais receita, fornecedores получают renewals, e seguradoras ficam segurando a conta que não conseguem atribuir limpa à IA.

5. **Yahoo Scout — Claude Potencializa uma Tentativa de Volta**
   O Yahoo lançou o Scout, um mecanismo de respostas de IA construído sobre o Claude da Anthropic com grounding do Microsoft Bing,rollout para 250 milhões de usuários americanos. É uma jogada direta contra o Google e busca estilo ChatGPT. Para a Anthropic, esse é mais um acordo major de distribuição além da Amazon, Google, e a stack enterprise. Para o Yahoo, é uma aposta de que o raciocínio do Claude em cima do índice do Bing pode carve out um nicho nas guerras de busca de IA. Se o Yahoo tem equity de marca suficiente sobrando para fazer isso importar é uma questão separada.

6. **Google Silenciosamente Lança um App de Dictação IA Offline-First**
   O Google lançou o AI Edge Eloquent — um app iOS gratuito que roda um modelo baseado em Gemma inteiramente on-device sem necessidade de conexão com a internet. Ele remove palavras de enchimento automaticamente e inclui ferramentas de transformação de texto: modos Pontos-Chave, Formal, Curto e Longo. Sem assinatura, uso ilimitado, Android vindo. O ângulo interessante não é o app em si — é que o Google lançou um produto Gemma completamente offline no iOS antes do Android, e fez isso silenciosamente. Sinais de um push de IA edge mais rápido.

## Notas do Episódio
```md
OPENCLAW DAILY — EPISÓDIO 027 — 9 de abril de 2026

[00:00] INTRO / HOOK
OpenClaw 2026.4.9 traz uma faixa de backfill REM grounded e timeline de diary.
Utah permite que IA prescreva meds psiquiátricos. OpenAI dá aos agentes um shell real.
Secretários de IA estão inflando custos de saúde e ninguém quer parar.
Yahoo aposta seu futuro de busca no Claude.

[02:00] HISTÓRIA 1 — OpenClaw 2026.4.9: Faixa de Dream Replay e Timeline do Diary
O lançamento de hoje é tudo sobre profundidade de memória.

A adição principal é a faixa de backfill REM grounded — um CLI `rem-harness
--path` que permite que notas diárias históricas voltem pelo pipeline
de dreaming. Se você tem o ARIA rodando por meses, seu contexto inicial
tem ficado inerte. Com o backfill, aquelas entradas antigas de diary
podem ser processadas em Dreams e promovidas para memória durável. A pilha
antiga e a pilha nova se tornam um registro contínuo.

O Control UI ganha uma visão estruturada de diary com navegação completa por
timeline: você pode rolar para trás pelas entradas de diary, rodar backfills,
resetar estado grounded, inspecionar summaries de dreaming rastreáveis, e ver
quais cenas estão na fila para promoção. A faixa de Scene agora mostra
promotion hints para que você possa ver o que está prestes a mover de short-term
para memória durável antes de acontecer.

QA recebe relatórios de avaliação de character-vibes — uma forma de rodar
comparações paralelas de modelos durante QA ao vivo para que você possa ver
diferenças comportamentais entre modelos candidatos lado a lado em vez de
sequencialmente.

Aliases de auth de provedor permitem que variantes de provedor compartilhem
vars de ambiente, perfis de auth, e fluxos de onboarding de chave API sem
precisar de fiação no nível do core. Se você roda múltiplas variantes do mesmo
provedor, a config de auth agora é compartilhada no nível do manifest.

iOS ganha pinagem de CalVer — rastreamento explícito de versão em
`apps/ios/version.json` com um workflow `pnpm ios:version:pin`
documentado para release trains. A iteração do TestFlight fica na mesma
versão curta até que mantenedores intencionalmente promovam para a próxima
versão de gateway.

Segurança: interações de browser não podem mais bypassar a Quarentena de SSRF
via navegações de main-frame dirigidas por interação — o check de segurança
agora roda novamente após cliques, evaluate, cliques triggered por hook, e
fluxos de ação em batch que pousam em um novo frame. E overrides de vars de
ambiente de controle de runtime estão bloqueados de arquivos `.env` de
workspace não confiáveis, fechando um path de escalação através de config
no nível de workspace.
→ github.com/openclaw/openclaw/releases/tag/v2026.4.9

[09:00] HISTÓRIA 2 — Utah Permite que IA Prescreva Medicamentos Psiquiátricos
A sandbox regulatória do Utah acabou de expandir de renewals de medicamentos
de rotina para prescrições psiquiátricas. A Legion Health é a primeira
empresa de saúde mental autorizada a permitir que IA emita ordens de
medicação psiquiátrica — ainda sob supervisão médica, mas a IA está tomando
a decisão inicial.

O piloto de janeiro de 2026 era para renewals de baixo risco. Prescrições
psiquiátricas são categoricamente diferentes: erros de dosagem, interações
medicamentosas e contraindicações em cuidados psiquiátricos carregam risco
clínico sério. Enquadrar isso como uma "sandbox" está fazendo trabalho
regulatório significativo.

A questão de responsabilidade é genuinamente não resolvida: quando uma IA
prescreve incorretamente e um paciente é prejudicado, quem é responsável?
O médico que supervisionou? A empresa rodando a sandbox? O estado que
autorizou? O Utah ainda não tem respostas claras, e eles estão adicionando
mais complexidade antes do framework ser testado.
→ distilinfo.com/2026/04/01/ai-now-prescribes-mental-health-drugs-in-utah/

[15:00] HISTÓRIA 3 — OpenAI Responses API: Agentes Ganham um Shell Real
A Responses API da OpenAI agora ships com uma ferramenta de shell hospedada —
Python, Node.js, Go, Java, Ruby, PHP — rodando dentro de container workspaces
gerenciados que o agente cria e executa. O agente escreve código, roda,
lê a saída e itera dentro de uma única sequência de chamada de API.
Context compaction server-side mantém tarefas de longa duração de bater
nos limites de tokens.

A outra adição são agent skills reutilizáveis — definições de capacidade
empacotadas que podem ser referenciadas entre execuções sem precisar
reespecificá-las cada vez.

Isso é a OpenAI desenhando uma linha dura: a Responses API é a superfície
agentic daqui para frente. A Assistants API não está recebendo isso. Se você
está construindo agentes autônomos na infraestrutura OpenAI, o caminho de
migração está claro.
→ openai.com/index/new-tools-for-building-agents/

[21:00] HISTÓRIA 4 — Secretários de IA Estão Aumentando Custos de Saúde, e Ninguém Quer Parar
O STAT News reporta que seguradoras e hospitais ambos privadamente reconhecem
que secretários médicos de IA estão aumentando custos — mas não há consenso
sobre o que fazer sobre isso.

O mecanismo é "intensidade de codificação": secretários de IA são mais
completos que anotadores humanos, captando mais detalhes faturáveis e
codificando visitas mais completamente. Codificação mais completa significa
sinistros de reembolso mais altos. Um estudo encontrou que secretários
economizaram 16 minutos por plantão de 8 horas apesar de aumentar despesas
de visita. Essa é uma troca muito ruim se o objetivo é eficiência de custo.

O dinâmica desconfortável: hospitais estão recebendo mais receita dos mesmos
encontros com pacientes, fornecedores de secretários estão recebendo renewals,
e seguradoras estão absorvendo custos que não conseguem atribuir limpi à IA.
Ninguém na cadeia tem incentivo financeiro direto para empurrar de volta.

Esse é um preview de um padrão que veremos em outros lugares: IA otimiza para
as métricas pelas quais é recompensada, e na saúde americana, a métrica é
códigos de faturamento.
→ statnews.com/2026/04/08/insurers-providers-agree-ai-scribes-raise-health-care-costs/

[26:00] HISTÓRIA 5 — Yahoo Scout Roda no Claude, Vai para 250M Usuários
O Yahoo lançou o Scout, um mecanismo de respostas de IA construído sobre o
Claude da Anthropic com grounding do Microsoft Bing, desplegando para 250
milhões de usuários americanos do Yahoo em desktop e mobile.

Para a Anthropic, esse é mais um canal major de distribuição — o Claude agora
é a camada de IA dentro da Amazon, Google Workspace e busca do Yahoo. O
despliegue comercial amplo está acelerando. Para o Yahoo, essa é a aposta de
produto mais crível que eles fizeram em anos. Se o Yahoo tem confiança de
usuário e hábito diário suficientes para converter buscas em sessões do Scout
é uma questão real. Mas a stack subjacente é sólida.
→ yahooinc.com/press/introducing-yahoo-scout-a-new-ai-answer-engine

[30:00] HISTÓRIA 6 — Google Lança Dictação Gemma Offline no iOS Antes do Android
O Google lançou o AI Edge Eloquent no iOS — um app gratuito de dictação
primeiro offline rodando um modelo Gemma inteiramente on-device. Sem internet,
sem assinatura, sem dados saindo do celular. Remoção de palavras de
enchimento, modos de transformação de texto Pontos-Chave / Formal / Curto /
Longo built in.

Duas coisas se destacam. Primeira: esse é um despliegue de Gemma on-device
sério, não um demo. Segunda: foi lançado no iOS antes do Android, o que
lhe diz algo sobre onde o campo de testes de IA edge do Google está agora.
Versão Android está vindo, mas os primeiros usuários reais estão em hardware
Apple. Lançamento silencioso, sinal significativo.
→ techcrunch.com/2026/04/07/google-quietly-releases-an-offline-first-ai-dictation-app-on-ios/

[33:00] ENCERRAMENTO
É isso para o OpenClaw Daily de hoje. Para notas do episódio e transcrições, vá para tobyonfitnesstech.com.
```

## Links
- Notas de lançamento do OpenClaw v2026.4.9: https://github.com/openclaw/openclaw/releases/tag/v2026.4.9
- Prescrições psiquiátricas de IA no Utah: https://distilinfo.com/2026/04/01/ai-now-prescribes-mental-health-drugs-in-utah/
- Ferramenta de shell da OpenAI Responses API: https://openai.com/index/new-tools-for-building-agents/
- Secretários de IA aumentando custos de saúde (STAT News): https://www.statnews.com/2026/04/08/insurers-providers-agree-ai-scribes-raise-health-care-costs/
- Anúncio do Yahoo Scout: https://www.yahooinc.com/press/introducing-yahoo-scout-a-new-ai-answer-engine
- Google AI Edge Eloquent (TechCrunch): https://techcrunch.com/2026/04/07/google-quietly-releases-an-offline-first-ai-dictation-app-on-ios/

## Capítulos
- **[00:00] Hook — Pilha de Dreams, Prescrições de IA, Agentes Shell, e o Custo dos Secretários**
- **[02:00] OpenClaw 2026.4.9: Faixa de Dream Replay e Timeline do Diary**
- **[09:00] Utah Permite que IA Prescreva Medicamentos Psiquiátricos**
- **[15:00] OpenAI Responses API: Agentes Ganham um Shell Real**
- **[21:00] Secretários de IA Estão Aumentando Custos de Saúde, e Ninguém Quer Parar**
- **[26:00] Yahoo Scout Roda no Claude, Vai para 250M Usuários**
- **[30:00] Google Lança Dictação Gemma Offline no iOS Antes do Android**
- **[33:00] Encerramento**
