# OpenClaw Daily - Episódio 9: OpenClaw v2026.3.1 — Quando seu assistente começa a agir como infraestrutura
# Data: 2 de março de 2026
# Hosts: Nova (britânica calorosa) & Alloy (americano)

[NOVA]: Bem-vindos de volta ao OpenClaw Daily. Eu sou a Nova.

[ALLOY]: E eu sou o Alloy.

[NOVA]: Hoje é um episódio de release sobre o OpenClaw v2026.3.1. E já aviso: não é um episódio de “novo modelo brilhante”. É um episódio de “amanhã o seu sistema fica menos frágil”.

[ALLOY]: É aquele tipo de atualização em que você não percebe uma feature gigante. Você percebe que três pequenas dores que você já aceitava… simplesmente param de acontecer.

[NOVA]: Exato. É uma release de infraestrutura.

[ALLOY]: Que parece chata… até você ser a pessoa operando o sistema.

[NOVA]: Quando você roda OpenClaw de verdade — em Discord, Telegram, talvez um node no celular, talvez um servidor, talvez Docker — você não quer surpresa. Você quer ciclos de vida previsíveis, sinal de health, streaming que não quebra, e automação que não spamma canal.

[ALLOY]: E essa versão entrega isso.

[NOVA]: Hoje vamos cobrir: ciclo de vida de sessões em threads do Discord, tópicos em DMs do Telegram, ações e health de device em nodes Android, probes para containers, streaming WebSocket-first para OpenAI Responses e cron com execuções de “contexto leve”. E alguns extras como a ferramenta de diffs e melhorias de UI.

[ALLOY]: Com um tema central: isso não é aleatório. O OpenClaw está apertando os parafusos para a máquina rodar mais rápido sem se desmontar.

[NOVA]: Vamos lá.

## Segmento 1 — O padrão em v2026.3.1: OpenClaw está virando um sistema

[ALLOY]: Todo projeto open source bom passa por uma transição.

[NOVA]: Qual?

[ALLOY]: Primeiro ele impressiona por ser esperto. Depois impressiona por ser confiável.

[NOVA]: Confiabilidade é o verdadeiro “flex”.

[ALLOY]: Exato. Esperteza dá estrela e demo. Confiabilidade dá adoção.

[NOVA]: As release notes parecem escritas por alguém que já ficou de plantão: “por que a thread resetou?”, “por que o cron postou lixo?”, “por que o stream travou?”, “por que eu não consigo fazer probe do container?”.

[ALLOY]: Perguntas que só aparecem quando você realmente usa.

## Segmento 2 — Discord threads: de TTL fixo para workspaces por inatividade

[NOVA]: Threads do Discord são um dos melhores front-ends para OpenClaw.

[ALLOY]: Porque thread é projeto.

[NOVA]: Em v2026.3.1, o ciclo de vida deixa de ser TTL fixo e vira por inatividade.

[ALLOY]: O default certo: mantém vivo enquanto eu uso, expira quando eu paro.

[NOVA]: Você tem idleHours (padrão 24) e maxAgeHours opcional.

[ALLOY]: idleHours: “se ninguém falar por X horas, expira”.

[NOVA]: maxAgeHours: “mesmo ativo, não passa de X”.

[ALLOY]: Isso evita contaminação de contexto e dá higiene.

## Segmento 3 — Telegram DM Topics: uma pessoa, vários workstreams

[ALLOY]: DM do Telegram sem compartimentos vira gaveta de bagunça.

[NOVA]: v2026.3.1 traz tópicos em DM, com políticas por tópico: skills, systemPrompt, allowlists, requireTopic.

[ALLOY]: Skills por tópico é enorme. Dá pra ter um tópico “modo seguro” (só pensar) e outro “ops” (ferramentas), com confirmações.

[NOVA]: E requireTopic ajuda a não cair de volta na gaveta.

## Segmento 4 — Android nodes: ações em notificações + device health

[NOVA]: Integração mobile costuma falhar sem guardrails.

[ALLOY]: Novos comandos: camera.list, device.permissions, device.health e notifications.actions (abrir, dispensar, responder).

[NOVA]: Notificações são onde o mundo fala com você. Mas responder sem controle é perigoso.

[ALLOY]: Padrão seguro: resumir → sugerir resposta → pedir confirmação clara → executar → reportar.

## Segmento 5 — Health probes: liveness e readiness

[NOVA]: Se você roda em Docker/Kubernetes, você quer probe.

[ALLOY]: v2026.3.1 adiciona health/healthz e ready/readyz, com fallback para não quebrar rotas existentes.

## Segmento 6 — Streaming: OpenAI Responses vira WebSocket-first

[NOVA]: Streaming é UX — e é onde as coisas quebram (proxy, timeout, rede móvel).

[ALLOY]: WebSocket-first com fallback para SSE e cleanup por sessão = mais confiança.

## Segmento 7 — Cron/automação: contexto leve para evitar spam

[NOVA]: Automação que funciona mas faz barulho é automação que você desliga.

[ALLOY]: Contexto leve reduz o “mundo inteiro” injetado em runs de cron, diminuindo vazamento de contexto e texto explicativo.

[NOVA]: Combine com política de saída: uma mensagem final, sem logs.

## Segmento 8 — Extras: diffs, i18n, QoL

[ALLOY]: Plugin diffs (somente leitura) para renderizar diffs bonitos.

[NOVA]: Web UI com locale em alemão.

[ALLOY]: CLI agora imprime qual arquivo de config está ativo.

## Segmento 9 — Checklist de upgrade

[NOVA]: Atualize e reinicie de forma limpa.

[ALLOY]: Discord: ajuste idleHours e considere maxAgeHours.

[NOVA]: Telegram: defina tópicos (Build/Admin/Pessoal) e, se precisar, requireTopic.

[ALLOY]: Android: comece com permissions/health e só responda notificação com confirmação.

[NOVA]: Teste streaming longo e revise cron com contexto leve.

## Encerramento

[ALLOY]: Essa release reduz “saída estranha” porque o sistema em volta do modelo fica menos vazado.

[NOVA]: Confiança não é problema de modelo. É engenharia.

[ALLOY]: OpenClaw está virando a infraestrutura do seu assistente.
