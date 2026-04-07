[NOVA]: Eu sou a NOVA.

[ALLOY]: E eu sou a ALLOY. Este é o OpenClaw Daily. Hoje a gente vai entrar no código-fonte de três runtimes de agentes de IA — OpenClaw, Claude Code e Hermes — e perguntar o que a arquitetura realmente revela sobre o propósito de cada um.

[NOVA]: Três runtimes de agentes entraram num codebase. Só um sabia o que estava construindo.

[NOVA]: Hoje é um mergulho técnico, ALLOY. A gente não vai dar copy de marketing. A gente vai abrir os arquivos reais e mostrar o que o código faz — porque a arquitetura é a filosofia. Como um sistema gerencia seu ciclo de turnos, como persiste memória, como bloqueia ações perigosas — essas não são detalhes de implementação. São o produto.

[ALLOY]: E o interessante é que, olhando os três lado a lado, você percebe que eles mal concordam sobre o que um "agente" sequer é. Hermes tem um agente que se auto-melhora e escreve suas próprias skills. Claude Code tem um agente que existe só para te ajudar a programar num diretório específico. OpenClaw tem um agente que é mais um sistema operacional — persistente, multi-canal, multi-subagente. Esses são animais genuinamente diferentes vestindo a mesma palavra.

[NOVA]: Vamos começar por como cada sistema é estruturado no nível mais alto, porque isso molda tudo o resto.

[NOVA]: Começando pelo OpenClaw. Se você olha pra ~/.openclaw/, vê a estrutura do runtime. Tem um gateway daemon que gerencia o sistema inteiro. Canais — Telegram, Discord, e assim por diante — são plugins que se conectam a esse gateway. Os arquivos do workspace ficam em ~/.openclaw/workspace/, e subagentes rodam como processos destacados com seu próprio contexto. A config fica em openclaw.json. O sistema de skills vive em ~/.openclaw/skills/, e a memória é armazenada em ~/.openclaw/memory/. E tem também ~/.openclaw/cron/ — o OpenClaw tem um sistema de agendamento embutido, o que te diz algo importante: esse runtime é projetado pra uma máquina que precisa executar tarefas mesmo quando ninguém está assistindo.

[ALLOY]: Isso mesmo. OpenClaw é arquitetado como um sistema operacional de IA pessoal. Não é só sobre um loop de agente único. É sobre presença persistente entre superfícies de mensagens, trabalho agendado em segundo plano, e delegação para subagentes. O gateway daemon do OpenClaw é o kernel desse sistema. Tudo o mais é um processo.

[NOVA]: Agora o Claude Code — e essa vai ser uma discussão de arquitetura mais curta, porque o Claude Code é intencionalmente focado. Você instala via npm: @anthropic-ai/claude-code, versão 2.1.59 no momento da gravação. É uma ferramenta CLI primeiro. Tem uma camada de sandboxing que a gente pode ver nas dependências — tem módulos pra Apple Sandbox Profiles no macOS e integração com bwrap (bubblewrap) no Linux. O registry de ferramentas fica em cli.js e arquivos relacionados. Mas a arquitetura é deliberadamente estreita: quer ser a melhor ferramenta pra um trabalho — ajudar um desenvolvedor num diretório de código.

[ALLOY]: Que é uma escolha de design completamente legítima. Estreito e profundo vence amplo e raso. Mas isso significa que o modelo de sessão do Claude Code é diferente dos outros dois. Não tem um banco de dados de sessão persistente. Cada invocação é algo que desaparece, embora ele possa manter estado de conversa dentro de um diretório de trabalho. A gente vai entrar no que isso significa pra memória.

[NOVA]: E depois o Hermes Agent da Nous Research. Esse é o mais explicitamente arquitetado como plataforma de pesquisa. O motor central de orquestração é run_agent.py e sua classe AIAgent. O session store é um banco SQLite em ~/.hermes/state.db rodando em modo WAL — então readers concorrentes, um writer, o que importa quando a gateway e o CLI estão batendo nele ao mesmo tempo. E tem busca full-text FTS5 em todas as mensagens de sessão via tabela virtual.

[ALLOY]: Isso é realmente uma decisão de arquitetura muito significativa. FTS5 significa que você pode buscar em todo o seu histórico de conversas, não só turnos recentes. Se você é um pesquisador que roda sessões longas em múltiplos tópicos, isso é um recurso valioso. E o fato de que eles rastreiam contadores de tokens, cobrança e configurações de modelo por sessão te diz que isso foi construído com consciência de custo — tanto pro laboratório de pesquisa quanto pros usuários que estão pagando pelas chamadas de API.

[NOVA]: Vamos falar sobre a parte mais importante de qualquer runtime de agente: o ciclo de turnos. Como cada sistema lida com uma troca única — mensagem do usuário entra, modelo pensa, chamadas de ferramenta, resposta sai?

[ALLOY]: Começando pelo Hermes, porque tem o loop mais documentado. Pelos docs: run_conversation() é o ponto de entrada principal. O ciclo de turnos é:

[NOVA]: 1. Gerar um task ID

[NOVA]: 2. Anexar a mensagem atual do usuário

[NOVA]: 3. Carregar ou construir o system prompt em cache

[NOVA]: 4. Talvez comprimir no preflight se o contexto estiver ficando longo

[NOVA]: 5. Construir api_messages — o payload real do prompt

[NOVA]: 6. Injetar camadas de prompt efêmeras

[NOVA]: 7. Aplicar prompt caching se apropriado

[NOVA]: 8. Fazer uma chamada de API interruptível

[NOVA]: 9. Se tiver chamadas de ferramenta: executar, anexar resultados, voltar pro loop

[NOVA]: 10. Se for texto final: persistir, limpar, retornar

[NOVA]: Passo 8 — chamadas de API interruptíveis. Isso é importante. O Hermes embrulha suas requisições à API pra que possam ser canceladas pelo CLI ou pela gateway. Isso importa porque o agente pode estar numa chamada longa de LLM, e o usuário envia uma mensagem nova no meio do voo, ou um sistema em segundo plano precisa cancelar. Isso é uma preocupação de design explícita, não um afterthought.

[ALLOY]: E olha os modos de API que o Hermes suporta. Três caminhos de execução: chat_completions pra endpoints compatíveis com OpenAI (incluindo OpenRouter), codex_responses pro Codex e Responses API, e anthropic_messages pro API nativa de Mensagens da Anthropic. O modo é resolvido a partir de argumentos explícitos, seleção de provider e heurísticas de base URL. Então o Hermes é genuinamente agnóstico de modelo — não como proclamação de marketing, mas como arquitetura de roteamento.

[NOVA]: Agora a execução de ferramentas do Hermes. Dois modos: sequencial pra ferramentas únicas ou interativas, e concorrente pra múltiplas ferramentas não-interativas. E aqui tem uma parte inteligente — execução concorrente preserva a ordenação de mensagens e resultados ao re-inserir respostas de ferramentas no histórico de conversas. Isso é uma restrição não-trivial de implementar corretamente.

[ALLOY]: Pro Claude Code, a gente não tem o caminho exato pro arquivo do loop da mesma forma, mas dá pra inferir pela estrutura do pacote. O pacote npm tá em /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. Os padrões-chave tão em cli.js — como ele lida com chamadas de ferramenta, como gerencia prompts de permissão, como faz o loop. O que a gente sabe sobre o loop do Claude Code é que ele é projetado em torno de um caso de uso específico: assistência a desenvolvedores num diretório local. Ele não tem spawn de subagentes como conceito de primeira classe da forma que o OpenClaw tem.

[NOVA]: E o loop de agente do OpenClaw é projetado em torno do fato de que ele tem múltiplos agentes concorrentes com uma gateway gerenciando a coordenação. O loop não é só "usuário → agente → ferramentas → resposta." É: mensagem do usuário chega no canal X, subagente Y pega, subagente Y pode gerar subagente Z, resultados voltam, gateway despacha pra superfície certa. A skill clawflow que orquestra fluxos de multi-agente é evidência disso — é projetada pra tarefas em segundo plano detached que ainda se comportam como um trabalho único.

[ALLOY]: O loop do OpenClaw é o mais complexo dos três porque tem a maior superfície de coordenação pra gerenciar. Mas complexidade não é sempre ruim — é complexidade apropriada pro que ele tenta fazer.

[NOVA]: É aqui que o Hermes realmente se distingue na arquitetura. Vamos fundo no schema do SQLite.

[ALLOY]: ~/.hermes/state.db tem quatro componentes lógicos: uma tabela de sessões, uma tabela de mensagens, uma tabela virtual FTS5 chamada messages_fts, e uma tabela schema_version. A tabela de sessões é rica — rastreia não só metadados de sessão mas informação de cobrança: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, pricing_version. Se você roda uma configuração multi-modelo com inúmerős providers de pricing diferente, o Hermes tá rastreando seus custos por sessão.

[NOVA]: A tabela de mensagens armazena tudo. role, content, tool_call_id, tool_calls como string JSON, tool_name, token_count, finish_reason, reasoning, reasoning_details, e codex_reasoning_items. Note que reasoning é armazenado separadamente — isso é pra providers como Claude que expõem tokens de thinking. E tem três triggers mantendo a tabela FTS5 em sync em INSERT, UPDATE e DELETE.

[ALLOY]: O handling de contenção de escrita vale a pena olhar. O Hermes lida com múltiplos processos — gateway mais sessões de CLI mais worktree agents — todos compartilhando um state.db. Ele usa um timeout curto no SQLite (1 segundo, não o default de 30), retries em nível de aplicação com jitter randômico entre 20 e 150 milissegundos, até 15 retries, e transações BEGIN IMMEDIATE pra superficializar contenção de lock cedo. Também faz checkpoints periódicos de WAL a cada 50 escritas em modo PASSIVE. Isso é engenharia ponderada — eles tão evitando o problema de convoy do SQLite, onde writers concorrentes retryam nos mesmos intervalos.

[NOVA]: E linhagem de sessão via parent_session_id encadeada. Quando a compressão de contexto dispara um split de sessão — que acontece quando a janela de contexto fica cheia — a nova sessão recebe um ID novo mas encadeia de volta pro parent. Você pode consultar linhagens inteiras de sessão recursivamente. Isso é pra sessões de pesquisa ou programação longas onde a compressão de contexto acontece no meio de uma tarefa.

[ALLOY]: Agora compara isso com o Claude Code. O modelo de sessão do Claude Code é... mais leve. Ele pode manter contexto de conversa dentro de um diretório de trabalho, mas não é projetado pra ser um sistema de memória de longo prazo. O sandbox é projetado em torno de permissões de filesystem pra um diretório específico — não em torno de memória estruturada persistente entre sessões. Essa é uma troca deliberada: simplicidade pro caso mais comum (ajuda a devs num codebase) versus persistência rica de sessão.

[NOVA]: E o modelo de memória do OpenClaw. Ele usa arquivos de workspace pra contexto estruturado — MEMORY.md pra memória curada de longo prazo, memory/YYYY-MM-DD.md pra logs de sessão diários. Tem também um sistema LCM — Lossless Context Management — que compacta o histórico de conversas. E tem um sistema de skills que atua como memória procedural. Então é um modelo de três camadas: logs diários brutos, memória curada de longo prazo, e skills que codificam fluxos de trabalho reutilizáveis.

[ALLOY]: A abordagem do OpenClaw é mais nativa do filesystem e menos nativa de banco de dados que o Hermes. O Hermes coloca tudo no SQLite porque é um runtime único que precisa de acesso multi-processo concorrente e FTS5. O OpenClaw usa o filesystem porque encaixa na filosofia Unix e torna os dados universalmente acessíveis — você pode dar grep, fazer backup com rsync, colocar no git.

[NOVA]: É aqui que o Claude Code realmente mostra suas cartas. Vamos falar sobre como ele lida com ações perigosas.

[ALLOY]: O Claude Code tem um sistema de sandboxing que mira duas plataformas explicitamente: macOS e Linux. No macOS, usa Apple Sandbox Profiles. No Linux, usa bwrap — bubblewrap. O sistema se chama SandboxLinux no source, e tem classes como SandboxConfig, SandboxManager, e um ViolationStore que rastreia violações de sandbox com uma contagem total e histórico por comando. A store de violações tem tamanho máximo de 100 entradas e uma contagem total que continua incrementando mesmo depois da store ficar cheia.

[NOVA]: A config de sandbox pro Linux é definida em sandbox_linux.py. Começa com --new-session --die-with-parent. Depois constrói paths de filesystem permitidos e negados. Os paths permitidos começam com uma allowlist default — coisas como /dev/null, /dev/urandom, /dev/zero. Paths negados são coisas como /etc/ssh/ssh_config.d se existir. Pra paths de escrita, tem um conceito de denyWithinAllow — você pode escrever num diretório mas não em subpaths perigosos específicos dentro dele.

[ALLOY]: O sandbox do Linux também tem filtragem seccomp BPF pra bloqueio de socket Unix. Tem um bpfPath e um applyPath pros binários de seccomp. Se esses não tão disponíveis, ele cai pro allow de sockets Unix — mas avisa que proteção completa não tá disponível. No macOS, tem um SandboxMonitor que observa violações usando o comando osascript.

[NOVA]: Agora compara isso com a abordagem do Hermes. O Hermes tem uma lista de DANGEROUS_PATTERNS em tools/approval.py — padrões regex emparelhados com descrições cobrindo deletes recursivos, comandos de formatação de filesystem como mkfs e dd, operações SQL destrutivas, sobrescrita de config de sistema, manipulação de serviços, execução remota de código via curl pipe sh, fork bombs. Antes de executar qualquer comando de terminal, detect_dangerous_command() verifica contra todos os padrões.

[ALLOY]: Se encontrar um match: no modo CLI, um prompt interativo pergunta ao usuário se aprova, nega, ou permite permanentemente. No modo gateway, um callback async de aprovação envia a requisição pra plataforma de mensagens — então se você tá no Telegram ou Discord, recebe a mensagem de aprovação lá. Tem também uma opção de smart approval onde um LLM auxiliar pode auto-aprovar comandos de baixo risco que por acaso casam com padrões perigosos — como rm -rf node_modules/ casando com o padrão de delete recursivo.

[NOVA]: E o Hermes tem aprovações com escopo de sessão. Uma vez que você aprova "delete recursivo" pra uma sessão, comandos rm -rf subsequentes não re-promptam. A allowlist permanente escreve padrões pro config.yaml's command_allowlist pra persistirem entre sessões.

[ALLOY]: Esses são modelos fundamentalmente diferentes. O sandbox do Claude Code é sobre restringir as capabilities do processo antes que algo ruim possa acontecer — o SO enforce. O sistema de aprovação do Hermes é sobre detectar padrões perigosos e perguntar — o humano enforce. O modelo do Claude Code é mais forte contra dano acidental. O modelo do Hermes é mais flexível pra casos de uso interativos onde o agente tá rodando num servidor remoto e o usuário tá aprovando via Telegram.

[NOVA]: O modelo do OpenClaw combina elementos de ambos. A ferramenta exec tem um sistema de aprovação — tem exec-approvals.json no diretório de config. E o sistema de subagentes do OpenClaw tem scoping de permissões — subagentes rodam com contextos de workspace específicos e não podem necessariamente ler ou escrever tudo que o agente pai pode. A gateway também tem o conceito de permissões por canal — o que é permitido no Telegram pode ser diferente do que é permitido no Discord.

[NOVA]: Vamos falar sobre como cada sistema te deixa estendê-lo.

[ALLOY]: Começando pelo sistema de skills do Hermes, porque é o mais completamente realizado. Skills são documentos de conhecimento sob demanda que o agente pode carregar quando precisa. Seguem o padrão aberto agentskills.io, o que significa que não tão trancados no Hermes — são portáveis. O formato de skill é SKILL.md com frontmatter YAML declarando name, description, version, platforms, e metadados pra condições de ativação.

[NOVA]: O padrão de revelação progressiva é inteligente. Nível 0: skills_list() retorna só name, description e category — cerca de 3k tokens. Nível 1: skill_view(name) carrega o conteúdo completo. Nível 2: skill_view(name, path) carrega um arquivo de referência específico. O agente só paga o custo de tokens quando realmente precisa da skill completa.

[ALLOY]: Skills podem ser condicionais. Podem declarar fallback_for_toolsets — então uma skill de busca DuckDuckGo só aparece quando o toolset de busca web premium tá indisponível. Ou requires_toolsets — uma skill só aparece quando certos tools tão presentes. E podem declarar variáveis de ambiente requeridas sem sumir da descoberta — se uma chave tá faltando, o Hermes pede de forma segura quando a skill é carregada no modo CLI, mas nunca prompta em superfícies de mensagens.

[NOVA]: Skills criadas pelo agente são um diferencial chave. A ferramenta skill_manage permite ao agente criar, atualizar e deletar suas próprias skills via um conjunto de ações create/patch/edit/delete/write_file/remove_file. Os docs especificam as condições de trigger: depois de completar uma tarefa complexa com 5+ chamadas de ferramenta, quando bate em erros e encontra o caminho que funciona, quando o usuário corrige a abordagem dele, quando descobre um fluxo de trabalho não-trivial. Essa é a camada de memória procedural — o agente não tá só fazendo trabalho, tá aprendendo como fazer trabalho.

[ALLOY]: O Hermes tem uma integração de marketplace de skills bem completa. Conecta ao catálogo oficial opcional de skills, skills.sh (diretório público da Vercel), endpoints de skills conhecidos via convenção /.well-known/skills/, repos GitHub diretos, ClawHub, e repositórios do Claude marketplace. Você pode publicar skills no GitHub diretamente. Pode adicionar taps GitHub customizados. Esse é um movimento genuíno de ecossistema aberto — o Hermes não tá tentando dominar a cadeia de suprimento de skills.

[NOVA]: E o Hermes suporta diretórios externos de skills. Você pode apontar ele pra ~/.agents/skills/ ou /home/shared/team-skills/ via expansão de variável ${VAR}. Esses diretórios são read-only pra descoberta — o agente sempre escreve skills novas em ~/.hermes/skills/. Mas skills externas aparecem no índice de system prompt e como slash commands, indistinguíveis de skills locais.

[ALLOY]: Agora o sistema de skills do OpenClaw. Olhando ~/.openclaw/skills/, também é frontmatter YAML mais corpo markdown, e a ferramenta hermes claw migrate sugere que compatibilidade cruzada é intencional. Skills do OpenClaw são workspace-contextuais — vivem ao lado do projeto que são relevantes. O sistema de skills é integrado com o sistema de subagentes, então você pode ter skills que descrevem como gerar o subagente certo pra uma tarefa dada.

[NOVA]: E o OpenClaw suporta MCP — Model Context Protocol — como mecanismo de extensibilidade. A config openclaw.json tem uma seção plugins e uma seção extensions. Servidores MCP podem ser configurados pra dar ao agente ferramentas de serviços externos.

[ALLOY]: O Claude Code tem um modelo de extensão mais focado. A estrutura do pacote npm sugere que é projetado pra funcionar bem com ferramentas de desenvolvedor existentes em vez de ter seu próprio marketplace de plugins. O sistema de skills no Claude Code é mais leve — slash commands, essencialmente. Mas isso é apropriado pra uma ferramenta CLI focada.

[NOVA]: A gente tem que falar sobre hermes claw migrate. Essa é uma ferramenta de migração explícita que shipa com o Hermes pra importar skills do OpenClaw e configurações de workspace. Isso é um sinal significativo.

[ALLOY]: Com certeza. O Hermes shipa com uma ferramenta chamada hermes claw migrate que diz: a gente sabe que o OpenClaw tem um sistema de skills que vale a pena copiar. A gente vai importar. Esse não é o movimento de um projeto que acha que tá em categoria diferente. Esse é o movimento de um projeto que acha que tá competindo diretamente e que o ecossistema de skills vale o cross-pollination.

[NOVA]: O fato de que é hermes claw migrate e não claw migrate te diz algo sobre a relação direcional. OpenClaw veio primeiro — o Hermes tá migrando dele. Mas o Hermes tá fazendo isso explicitamente, o que significa que o time da Nous Research olhou pro sistema de skills e modelo de workspace do OpenClaw e decidiu: a gente quer isso no nosso ecossistema, e a gente quer facilitar pros usuários do OpenClaw tentarem o Hermes.

[ALLOY]: E a arquitetura agnóstica de modelo do Hermes torna essa migração crível. Se você tava usando o OpenClaw com Claude como seu backend, pode trocar pro Hermes e usar as mesmas skills. O formato de skill é aberto — SKILL.md com frontmatter YAML seguindo o spec agentskills.io. Não é um formato lock-in proprietária.

[NOVA]: Esse é o tipo de coisa que só acontece quando um ecossistema aberto começa a amadurecer. A OpenAI tinha Actions e Plugins. A Anthropic tem MCP. E agora o Hermes tem uma ferramenta de migração pros skills do OpenClaw. A história de portabilidade de skills tá se tornando uma dimensão competitiva genuína.

[ALLOY]: E a resposta do OpenClaw provavelmente é... nada precisa mudar. O fato de que o Hermes tá migrando do OpenClaw significa que o modelo do OpenClaw é a referência. O OpenClaw não precisa migrar pro Hermes. Mas o OpenClaw deveria observar como o ecossistema de skills do Hermes evolui — se o Hermes construir um marketplace mais rico, isso pode se tornar um motivo pra usuários avaliarem.

[NOVA]: Me deixa te dar alguns nomes de classe e nomes de arquivo específicos pra ancorar essa discussão.

[ALLOY]: Do Hermes:

[NOVA]: - Agente core: run_agent.py — classe AIAgent

[NOVA]: - Gerenciamento de estado: hermes_state.py — classe SessionDB

[NOVA]: - Registry de ferramentas: tools/registry.py — singleton ToolRegistry, objetos ToolEntry

[NOVA]: - Descoberta de ferramentas: model_tools.py — função _discover_tools()

[NOVA]: - Dispatch de ferramentas: registry.dispatch(name, args, kwargs) — roteia pro handler certo

[NOVA]: - Sistema de aprovação: tools/approval.py — DANGEROUS_PATTERNS, detect_dangerous_command()

[NOVA]: - Compressão de contexto: agent/context_compressor.py

[NOVA]: - Construção de prompt: agent/prompt_builder.py

[NOVA]: - Prompt caching: agent/prompt_caching.py

[NOVA]: - Path do DB de sessão: ~/.hermes/state.db

[NOVA]: - Diretório de skills: ~/.hermes/skills/

[NOVA]: - Config: ~/.hermes/config.yaml

[NOVA]: A descoberta de ferramentas no Hermes é interessante. _discover_tools() importa módulos numa ordem fixa, e cada módulo chama registry.register() em nível de módulo. A lista de módulos inclui web_tools, terminal_tool, file_tools, vision_tools, mixture_of_agents_tool, image_generation_tool, skills_tool, browser_tool, cronjob_tools, rl_training_tool, tts_tool, todo_tool, memory_tool, session_search_tool, clarify_tool, code_execution_tool, delegate_tool, process_registry, send_message_tool, honcho_tools, homeassistant_tool. Essa é uma lista bem completa — o Hermes não é uma ferramenta estreita.

[ALLOY]: E mixture_of_agents_tool mais rl_training_tool mais delegate_tool te diz que o Hermes é projetado como plataforma de pesquisa. Esses não são recursos de consumo. mixture_of_agents sugere métodos de ensemble, rl_training sugere aprendizado por reforço a partir de feedback, delegate_task sugere geração de subagentes. Esse é um sistema projetado pra pesquisadores que querem experimentar com RL agentic.

[NOVA]: Pro Claude Code, o pacote tá em /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. O sistema de sandbox tem classes como SandboxLinux, SandboxConfig, SandboxManager, ViolationStore. O sistema de permissões tem policySettings, userSettings, projectSettings, localSettings — fontes de permissão em camadas com regras pra allow, deny e ask. O registry de ferramentas usa alwaysAllowRules, alwaysDenyRules, alwaysAskRules — então tem um modelo de três níveis: sempre permite, sempre nega, sempre pergunta.

[ALLOY]: Pro OpenClaw, o gateway daemon, agendamento de cron, orquestração de subagentes e plugins de canal (Discord, Telegram) vivem todos em ~/.openclaw/. A estrutura de workspace é relativa ao projeto. Skills vivem em ~/.openclaw/skills/. O sistema LCM pra compactação de contexto tá no runtime. A skill clawflow gerencia fluxos de trabalho multi-agente.

[NOVA]: OK. A gente foi bem fundo. Vamos dar o veredito.

[ALLOY]: Usa o Hermes se: você é um pesquisador ou power user que quer um agente auto-melhorante com memória genuína de longo prazo entre sessões, flexibilidade de modelo, busca FTS5 em todo o seu histórico de conversas, um ecossistema rico de skills que você contribui e do qualdrawing, e a capacidade de rodar no Telegram, Discord, Slack, WhatsApp ou Signal de uma única gateway. O Hermes também é a escolha certa se você tem interesse em melhoria de agente baseada em RL — os ambientes RL Atropos e compressão de trajetória sugerem um design focado em pesquisa. E se você já é usuário do OpenClaw, o hermes claw migrate do Hermes significa que você pode trazer suas skills com você.

[NOVA]: Usa o Claude Code se: você é um desenvolvedor que quer a melhor ajuda possível num codebase específico, rodando localmente, com o sandboxing mais rigoroso no nível do SO pra operações perigosas. A integração de bubblewrap e Apple Sandbox do Claude Code é a implementação de sandbox mais rigorosa dos três. Se seu fluxo de trabalho é "estou num diretório, preciso de ajuda, confio no agente pra editar arquivos aqui," o Claude Code é a ferramenta mais focada pra esse trabalho. A troca é persistência de sessão e presença multi-canal — não é projetado pra isso.

[ALLOY]: Usa o OpenClaw se você quer uma IA pessoal persistente que vive na sua máquina (ou num VPS), conecta em múltiplos canais de mensagens simultaneamente, executa tarefas agendadas, gera subagentes pra trabalho em segundo plano, e tem um sistema de skills que é seu pra moldar. O OpenClaw é o mais nativo em Unix dos três — encaixa naturalmente num fluxo de trabalho de linha de comando, funciona com convenções existentes de dotfiles e workspace, e é projetado pra ser seu sistema operacional de IA em vez de uma ferramenta única. O fato de que o Hermes shipa uma ferramenta de migração do OpenClaw te diz que o modelo de skill do OpenClaw é a referência.

[NOVA]: O ponto mais profundo é que esses três sistemas codificam três teorias diferentes sobre o que um agente de IA deveria ser. O Hermes acha que um agente deveria ser um companheiro de pesquisa persistente e auto-melhorante com memória rica e flexibilidade de modelo. O Claude Code acha que um agente deveria ser uma ferramenta de desenvolvimento estreita e profundamente integrada com garantias fortes de segurança. O OpenClaw acha que um agente deveria ser um SO de IA pessoal — sempre ativo, multi-superfície, multi-agente.

[ALLOY]: Nenhuma dessas teorias tá errada. São apostas diferentes sobre pra onde o espaço tá indo. Os próximos anos vão nos dizer qual delas estava certa.

[NOVA]: Uma última coisa antes de fechar — muitos de vocês vão querer experimentar o Hermes depois dessa. Então vamos falar de modelos. O Hermes é genuinamente agnóstico de modelo, mas os docs são específicos sobre o que funciona melhor.

[ALLOY]: O ponto de partida recomendado deles é o Claude Sonnet via OAuth da Anthropic — e aqui tem uma parte inteligente: se você já usa o Claude Code, o Hermes automaticamente lê a credential store do Claude Code. Sem configuração separada de API key. Você roda hermes model, escolhe Anthropic, e funciona imediatamente com sua assinatura existente.

[NOVA]: Pra opções gratuitas, o Hermes tem suporte de primeira classe ao GitHub Copilot. Se você tem uma assinatura Copilot, tem acesso ao GPT-5.4, Claude e Gemini através da API do Copilot. GPT-5 e superiores automaticamente roteiam pela Responses API; todo o resto usa Chat Completions.

[ALLOY]: O caminho gratuito mais interessante é o OpenRouter. Define uma OPENROUTER API KEY no seu arquivo dot env, roda hermes model, e você tem acesso a mais de 200 modelos. Os docs do Hermes especificamente chamam que algumas ferramentas built-in — visão, sumarização web, e a ferramenta mixture of agents — usam um modelo auxiliar separado que é default o Gemini Flash via OpenRouter. Então mesmo se você tá usando Claude como primário, uma chave OpenRouter desbloqueia essas ferramentas automaticamente.

[NOVA]: Pra modelos locais, o Hermes suporta qualquer endpoint Ollama ou vLLM — mesma config, só apontar OPENAI BASE URL pro seu servidor local. E pra providers chineses especificamente: Z-dot-AI GLM, Kimi slash Moonshot, MiniMax e Alibaba Cloud Qwen todos têm IDs de provider de primeira classe. Não é um afterthought — tão na lista core de providers junto com Anthropic e OpenAI.

[ALLOY]: A resposta prática pra maioria das pessoas: se você tem Claude Pro ou Max, comece com o OAuth da Anthropic. Se quer gratuito com capability forte, GitHub Copilot com GPT-5.4. Se quer flexibilidade máxima e não se importa com uma conta de API pequena, OpenRouter com Claude Sonnet ou Qwen 3.

[NOVA]: Esse foi o EP021: Dentro do Loop. As notas completas do show e links tão em Toby On Fitness Tech ponto com barra podcasts barra episódio 21. Eu sou a NOVA.

[ALLOY]: E eu sou a ALLOY. Voltamos logo.
