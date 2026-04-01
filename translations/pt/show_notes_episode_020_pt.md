# EP020 — O Lançamento da Infraestrutura

**OpenClaw Daily** | 1 de abril de 2026 | ~32 min

A OpenClaw parou de ser uma ferramenta inteligente esta semana e passou a ser infraestrutura. Cinco histórias que explicam como isso aconteceu — e o que isso significa para todos que estão construindo em cima.

---

## Histórias deste Episódio

### 1. OpenClaw v2026.3.31 — O Lançamento da Plataforma
A atualização mais consequente da OpenClaw em meses. Principais mudanças:
- **Plano de controle de tarefas em segundo plano** — ACP, subagentes, cron e execução CLI em segundo plano unificados sob um único ledger respaldado por SQLite com `openclaw flows list|show|cancel`
- **Segurança de plugins falha fechada por padrão** — descobertas críticas de código perigoso agora bloqueiam instalações; `--dangerously-force-unsafe-install` explícito é necessário para sobrescrever
- **Pareamento de node vs. aprovação separado** — comandos de node permanecem desabilitados até que o pareamento seja explicitamente aprovado (pareamento sozinho não é mais suficiente)
- **Autenticação do Gateway reforçada** — proxy confiável rejeita configurações mistas de token compartilhado; fallback local-direct requer o token configurado
- **Canal QQ Bot** — caminho de primeira classe integrado ao ecossistema da Tencent
- **Respostas streaming no Matrix** — respostas parciais agora são atualizadas no lugar em vez de inundar o chat
- **Suporte MCP HTTP/SSE remoto** — superfícies de ferramentas servidas sobre transportes remotos
- **Encaminhamento de notificações Android** — filtragem de pacotes, horário silencioso, rate limiting
- **Timeout de stream ociosa** — streams de modelo travadas agora são abortadas de forma limpa
- **Ponte ACPX MCP reforçada** — config padrão explícita desligada, limite de confiança documentado
- Breaking: `qwen-portal-auth` removido; configs com mais de 2 meses não migram mais automaticamente

📎 [Notas de lançamento: openclaw/openclaw v2026.3.31](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31)

---

### 2. A Frenesi da OpenClaw na China — e a Resposta de Pequim
A OpenClaw ficou viral na China ("lagosta" no jargão tech chinês), com estrelas no GitHub superando brevemente o React. A Tencent sediou eventos de instalação pop-up. Então vieram as "vítimas da lagosta" — usuários que perderam arquivos, acumularam contas, ou expuseram dados sensíveis a agentes de IA sem proteções. Pequim respondeu banindo funcionários de empresas estatais de usarem a ferramenta.

📎 [The Wire China: Como a Frenesi da OpenClaw Está Testando o Compromisso da China com a IA](https://www.thewirechina.com/2026/03/29/how-the-openclaw-frenzy-is-testing-chinas-ai-commitment/)
📎 [Alerta de segurança PCWorld: Não instale a OpenClaw](https://www.pcworld.com/article/3064874/openclaw-ai-is-going-viral-dont-install-it.html)

---

### 3. Microsoft 365 + OpenClaw — Validação Empresarial
A Microsoft está ativamente integrando a OpenClaw ao Microsoft 365, trazendo agentes de IA pessoais para seus ~400 milhões de usuários empresariais. Isso posiciona a OpenClaw como a camada de agentes para produtividade corporativa — não apenas uma ferramenta para entusiastas.

📎 [Windows Central: Novos agentes de IA OpenClaw da Microsoft para Microsoft 365](https://www.windowscentral.com/artificial-intelligence/microsoft-openclaw-will-add-personal-ai-agents-in-microsoft-365)

---

### 4. Perplexity Personal Computer — IA Local que Vive Com Você
A Perplexity lançou "Personal Computer" — um agente de IA dedicado em um Mac mini com acesso persistente e contínuo aos seus arquivos e aplicativos locais. Sempre ativo, sempre ciente do contexto, totalmente local. Nenhum upload para a nuvem necessário.

📎 [r/LocalLLaMA: Stacks de agentes locais em 2026](https://www.reddit.com/r/LocalLLaMA/comments/1s6f15f/localfirst_agent_stacks_in_2026_whats_actually/)

---

### 5. O Trimestre de US$ 297 Bilhões
O Q1 de 2026 quebrou todos os recordes de financiamento de venture capital. US$ 297B investidos globalmente, 81% em empresas de IA. As quatro maiores rodadas: OpenAI (US$ 120B), Anthropic (US$ 30B), xAI (US$ 20B), Waymo (US$ 16B). A CoreWeave garantiu uma facility de financiamento de US$ 8,5B. O Crunchbase Unicorn Board adicionou US$ 900B em valor em um único trimestre.

📎 [Crunchbase: Q1 de 2026 Quebra Recordes de Financiamento de Venture](https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/)
📎 [TechFundingNews: CoreWeave consegue US$ 8,5B](https://techfundingnews.com/coreweave-lands-8-5b-wall-street-ai-cloud/)

---

## Capítulos

`[00:00]` Gancho — O Momento da Plataforma
`[02:30]` OpenClaw v2026.3.31 — Quando uma Ferramenta se Torna Infraestrutura
`[14:00]` A Frenesi da OpenClaw na China e a Repressão do Estado
`[21:00]` Integração com Microsoft 365 — Validação Empresarial ou Normalização de Riscos?
`[27:00]` Perplexity Personal Computer — IA Local que Vive Com Você
`[33:00]` O Trimestre de US$ 297 Bilhões — O Maior Investimento em IA
`[39:00]` Encerramento — Agentes no Ponto de Inflexão

---

## Encontre o OpenClaw Daily

- 🌐 [tobyonfitnesstech.com/pt/podcasts/episode-20/](https://tobyonfitnesstech.com/pt/podcasts/episode-20/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- Feeds disponíveis em EN, ES, PT, HI, DE

→ Reply on Telegram to approve.