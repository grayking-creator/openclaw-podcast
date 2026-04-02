# EP021 — Dentro do Loop

**OpenClaw Daily** | 2 de abril de 2026 | ~37 min

Um mergulho técnico nos código-fonte de três runtimes de agentes de IA — OpenClaw, Claude Code e Hermes — para revelar o que a arquitetura de cada um realmente diz sobre o propósito de cada sistema.

---

## Histórias deste Episódio

### 1. OpenClaw — O Sistema Operacional de IA Pessoal
Estrutura em ~/.openclaw/ com gateway daemon, plugins de canal, subagentes como processos destacados, sistema de cron integrado e configuração em openclaw.json. O sistema é projetado para uma máquina que precisa executar tarefas mesmo quando ninguém está assistindo. O modelo de memória é de três camadas: logs diários, memória de longo prazo curada e skills como memória procedural.

📎 [Repositório: openclaw/openclaw](https://github.com/openclaw/openclaw)

---

### 2. Claude Code — Foco Deliberado
CLI para assistência a desenvolvedores em um diretório específico. Sandbox robusto com Apple Sandbox Profiles no macOS e bubblewrap (bwrap) no Linux. Sem subagentes, sem sessão persistente entre execuções. A escolha de design mais estreita e profunda em vez de ampla e rasa — e é deliberada.

📎 [npm: @anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code)

---

### 3. Hermes Agent — A Plataforma de Pesquisa
Daemon com SQLite em modo WAL (concurrent readers, um writer), FTS5 full-text search em todo o histórico, rastreamento de custos por sessão (input tokens, output tokens, cache tokens, custo estimado), parent_session_id para linhagem de sessões após compressão de contexto, e handle de write contention com retries e jitter. Suporta Chat Completions, Codex Responses e Anthropic Messages como caminhos de execução.

📎 [Nous Research: Hermes Agent](https://github.com/nousresearch/hermes-agent)

---

### 4. Dentro do Loop de Execução
Hermes: generate task ID → append user message → load/build cached system prompt → preflight compress → build api_messages → inject ephemeral layers → apply prompt caching → interruptible API call → execute tools (sequential or concurrent) → loop or persist. Claude Code: arquitetura de CLI focada com registry de ferramentas em cli.js. OpenClaw: gateway coordena múltiplos subagentes concurrentes com clawflow para orquestração de tarefas em segundo plano.

---

### 5. Modelos de Segurança
Claude Code: sandboxing via capabilities do SO — o processo é restringido antes que algo ruim possa acontecer. Hermes: DANGEROUS_PATTERNS em tools/approval.py com detecção de comandos perigosos via regex, prompts interativos no CLI, callbacks async na gateway para aprovação via Telegram/Discord. OpenClaw: combina ambos — exec-approvals.json com scoping de permissões por subagente e por canal.

---

### 6. Skills e Extensibilidade
Hermes: SKILL.md com YAML frontmatter seguindo o padrão agentskills.io, skills condicionais, agent-created skills, marketplace conectando ao catálogo oficial, skills.sh, ClawHub e repositórios GitHub. OpenClaw: skills com YAML frontmatter + markdown, workspace-contextuais, compatíveis com o padrão agentskills.io. Claude Code: modelo mais leve — slash commands integrados à CLI focada. **Sinal significativo:** Hermes inclui `hermes claw migrate` para importar skills e configurações do OpenClaw diretamente.

---

### 7. Qual Usar
**Hermes:** pesquisadores e power users que querem um agente auto-melhorante com memória persistente, flexibilidade de modelo, busca FTS5 em todo o histórico, e capacidade de rodar em múltiplas plataformas de mensagens. **Claude Code:** desenvolvedores que querem a melhor ajuda possível em um codebase específico, localmente, com sandboxing no nível do SO. **OpenClaw:** quem quer uma IA pessoal persistente que vive na máquina, conecta em múltiplos canais, executa tarefas agendadas e gera subagentes.

---

## Capítulos

`[00:00]` Gancho — Três Agentes, Três Filosofias
`[02:00]` Estrutura do OpenClaw — O Kernel do Sistema
`[07:00]` Claude Code — Arquitetura Focada
`[10:00]` Hermes — A Plataforma de Pesquisa com SQLite e FTS5
`[16:00]` Dentro do Loop de Execução — Hermes, Claude Code, OpenClaw
`[24:00]` Modelos de Segurança — Sandbox vs. Aprovação
`[28:00]` Skills e Extensibilidade — Hermes, OpenClaw, Claude Code
`[32:00]` O Sinal do hermes claw migrate
`[35:00]` Qual Runtime Escolher — Veredito
`[40:00]` Modelos Recomendados para Hermes

---

## Encontre o OpenClaw Daily

- 🌐 [tobyonfitnesstech.com/pt/podcasts/episode-21/](https://tobyonfitnesstech.com/pt/podcasts/episode-21/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- Feeds disponíveis em EN, ES, PT, HI, DE

→ Reply on Telegram to approve.
