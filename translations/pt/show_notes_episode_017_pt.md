# OpenClaw Daily — Episódio 017: Agentes em todo o caminho

**"Como o novo OpenClaw muda seu fluxo de trabalho diário"**

O lançamento do OpenClaw em 24 de março marca uma mudança significativa do polimento para a possibilidade. Neste episódio, NOVA e ALLOY abordam as mudanças concretas no fluxo de trabalho que são importantes para usuários avançados e construtores - desde subagentes aninhados que decompõem tarefas de forma autônoma, até um sistema de memória híbrido que finalmente resolve o problema de esquecimento no meio da sessão, até uma camada de compatibilidade OpenAI que torna a infraestrutura auto-hospedada uma realidade, até a maturidade da plataforma Teams e Feishu que sinaliza a evolução do OpenClaw além de uma estrutura de bot do Telegram.

## O que cobrimos

- **Subagentes aninhados com profundidade configurável** — como os agentes agora podem gerar especialistas, agregar resultados e operar sem orquestração do usuário
- **A ferramenta `config_manager`** — leitura/gravação de configuração em tempo de execução que permite a especialização dinâmica do agente
- **BM25 híbrido + pesquisa vetorial** — por que a recuperação de correspondência exata agora funciona de maneira confiável junto com a similaridade semântica
- **Incorporação de cache e compactação adaptativa** — as mudanças na infraestrutura que evitam a perda de contexto no meio da sessão
- **Interface ContextEngine conectável** — a saída de escape do construtor para back-ends de memória personalizados
- **Camada de compatibilidade OpenAI** — `/v1/models` e `/v1/embeddings` como endpoints de gateway nativos
- **Auto-hospedagem com clusters EXO** — destilação Qwen3.5-27B em execução como um substituto imediato do OpenAI
- **Migração do SDK do Microsoft Teams** — respostas de streaming, cartões de boas-vindas, indicadores de digitação, rotulagem de IA
- **Discord Components v2** — botões nativos, menus suspensos e modais interativos
- **Suporte Feishu/Lark** — OpenClaw alcançando mercados empresariais asiáticos
- **aplicativo de nó alfa para iOS** — OpenClaw rodando como um nó ativo no iPhone

## Links e recursos

- **Documentação do OpenClaw** — [https://docs.openclaw.dev](https://docs.openclaw.dev)
- **GitHub OpenClaw** — [https://github.com/openclaw-dev/openclaw](https://github.com/openclaw-dev/openclaw)
- **Destilação Qwen3.5-27B** — [https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill](https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill)
- **LangChain** — [https://www.langchain.com](https://www.langchain.com)
- **LlamaIndex** — [https://www.llamaindex.ai](https://www.llamaindex.ai)
- **WebUI aberta** — [https://openwebui.com](https://openwebui.com)
- **SDK do Microsoft Teams** — [https://learn.microsoft.com/en-us/microsoftteams/platform/](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- **Feishu/Lark** — [https://www.feishu.cn](https://www.feishu.cn) / [https://www.larksuite.com](https://www.larksuite.com)
- **Documentação do cluster EXO** — [https://docs.openclaw.dev/hardware/exo-cluster](https://docs.openclaw.dev/hardware/exo-cluster)
- **Aplicativo OpenClaw iOS (Alfa)** — [https://openclaw.dev/ios](https://openclaw.dev/ios)
- **Documentos da interface ContextEngine** — [https://docs.openclaw.dev/core/context-engine](https://docs.openclaw.dev/core/context-engine)
- **Mostrar notas e arquivos de episódios** — [https://tobyonfitnesstech.com](https://tobyonfitnesstech.com)

## Capítulos

- `[00:00]` Hook — The Shift: Por que 24 de março é diferente de .22/.23
- `[02:30]` Segmento 1 — Agents Spawning Agents: Subagentes aninhados, config_manager, cenários de fluxo de trabalho, riscos de limite de profundidade
- `[10:00]` Segmento 2 - A memória se torna real: pesquisa híbrida BM25 + vetor, incorporação de cache, compactação adaptativa, capacidade de conexão do ContextEngine
- `[19:00]` Segmento 3 — Camada de compatibilidade OpenAI e auto-hospedagem: `/v1/models` e `/v1/embeddings` nativos, encaminhamento de substituição de modelo, cluster EXO como substituto de OpenAI, aplicativo de nó iOS
- `[24:00]` Segmento 4 — Maturidade da plataforma: Teams SDK (streaming, cartões de boas-vindas, indicadores de digitação, rotulagem de IA), Discord Components v2, suporte Feishu/Lark
- `[30:00]` Outro / Builder's Take: A abordagem quente da NOVA sobre agentes aninhados + memória, contraponto de complexidade do ALLOY, CTA para tobyonfitnesstech.com

## Anfitriões

- **NOVA** — Anfitrião, analítico e conciso
- **ALLOY** — Co-anfitrião, prático e um pouco cético